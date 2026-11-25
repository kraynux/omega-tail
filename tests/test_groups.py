# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Regroupements et modes (lot 6) : base AS / pays compacte (Python et Lua d'HAProxy identiques), mode attaque
automatique, reference apprise des empreintes, observation puis application, ecrans."""
from __future__ import annotations

import contextlib
import gzip
import shutil
import socket
import subprocess
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest
from funnel_sim import FunnelSim
from hello_bytes import chrome_like, python_hello
from test_gate import PRODUCTION, TARGET, FakeAdmin
from test_gate import gate as make_gate

from omega_tail.application.groups import GroupsTools, parse_rows
from omega_tail.domain.gate import MODE_OBSERVATION, GatePolicy, render_config
from omega_tail.domain.geo import Range, asn_numbers, compact, countries, lookup
from omega_tail.domain.groups import (
    GROUPS_APPLY,
    GROUPS_OBSERVE,
    KNOWN_JA4_LIST,
    GroupsPolicy,
    Learning,
    groups_from,
    learn,
    learning_left,
    reference,
)
from omega_tail.domain.report import summarize
from omega_tail.infrastructure.gate import proxy_v2_header
from omega_tail.infrastructure.geo_base import GeoReader, build, lua_scripts
from omega_tail.infrastructure.settings.json_store import JsonSettingsStore

NOW = datetime(2026, 11, 23, 12, 0, tzinfo=timezone.utc)
CLOUD, HOME = "3.5.140.9", "90.12.3.4"


def write_base(folder: Path) -> Path:
    """Petite base DB-IP fictive : 3.0.0.0/8 chez un nuage (AS16509, US), 90.0.0.0/8 chez un FAI (AS3215, FR)."""
    country = [("0.0.0.0", "2.255.255.255", "ZZ"), ("3.0.0.0", "3.255.255.255", "US"),
               ("90.0.0.0", "90.255.255.255", "FR"), ("2a01:cb00::", "2a01:cbff:ffff:ffff:ffff:ffff:ffff:ffff", "FR")]
    asn = [("3.0.0.0", "3.255.255.255", "16509", "Amazon.com, Inc."), ("90.0.0.0", "90.255.255.255", "3215", "Orange")]
    for name, rows in (("country.csv.gz", country), ("asn.csv.gz", asn)):
        with gzip.open(folder / name, "wt") as handle:
            handle.writelines(",".join(f'"{cell}"' if " " in cell or "," in cell else cell for cell in row) + "\n"
                              for row in rows)
    build(folder / "country.csv.gz", folder / "asn.csv.gz", folder / "geo.bin", folder / "as-noms.tsv", min_rows=1)
    return folder / "geo.bin"


def test_compact_fills_gaps_and_merges() -> None:
    records = compact([Range(10, 19, "A"), Range(20, 29, "A"), Range(40, 49, "B")], "-", 99)
    assert records == [(0, "-"), (10, "A"), (30, "-"), (40, "B"), (50, "-")]
    assert [lookup(records, value) for value in (0, 15, 29, 30, 45, 99)] == ["-", "A", "A", "-", "B", "-"]
    assert countries("fr, cn ru; xx1 --") == ("CN", "FR", "RU")
    assert asn_numbers("AS16509, 24940 foo") == (16509, 24940)


def test_base_lookup(tmp_path: Path) -> None:
    reader = GeoReader(write_base(tmp_path))
    assert reader.lookup(CLOUD) == ("US", 16509) and reader.lookup(HOME) == ("FR", 3215)
    assert reader.lookup("::ffff:90.1.1.1") == ("FR", 3215) and reader.lookup("2a01:cb00::7")[0] == "FR"
    assert reader.lookup("10.0.0.1") == ("--", 0) and reader.lookup("pas une adresse") == ("--", 0)


def test_learning_needs_seven_days_and_ignores_attacks() -> None:
    state = Learning()
    for day in range(8):
        moment = NOW + timedelta(days=day)
        state = learn(state, {"chrome": 100 * (day + 1), "rare": 1 + (day >= 6)}, moment, attack=False)
        state = learn(state, {"outil": 5000 * (day + 1)}, moment, attack=True)  # attaque : jamais apprise
    assert learning_left(Learning(), NOW) == 7 and learning_left(state, NOW + timedelta(days=3)) == 4
    assert learning_left(state, NOW + timedelta(days=8)) == 0
    assert reference(state) == ("chrome",)  # « rare » : 2 jours et une part infime ; « outil » : jamais


def test_config_rules_observation_then_enforced() -> None:
    observe = render_config(GatePolicy(), TARGET, gate_port=9443, folder="/v", groups=GroupsPolicy())
    assert "lua-load /v/omega_ja4.lua" in observe and "track-sc7 int(1) table porte_attaque" in observe
    assert "reject if { var(sess.groupe) -m found }" not in observe and "!client_connu" not in observe
    assert "str(empreinte)" not in observe  # apprentissage pas fini : pas de regle des empreintes
    applied = render_config(GatePolicy(), TARGET, gate_port=9443, folder="/v",
                            groups=GroupsPolicy(mode=GROUPS_APPLY, countries=("CN",)), ja4_ready=True)
    assert "reject if { var(sess.groupe) -m found }" in applied and "!client_connu" in applied
    assert "str(empreinte) if attaque !{ var(sess.motif) -m found } !navigateur" in applied
    global_observe = render_config(GatePolicy(mode=MODE_OBSERVATION), TARGET, gate_port=9443, folder="/v",
                                   groups=GroupsPolicy(mode=GROUPS_APPLY))
    assert "reject if { var(sess.groupe)" not in global_observe  # porte en observation : rien n'est refuse
    assert "lua-load" not in render_config(GatePolicy(), TARGET, gate_port=9443, folder="/v")  # sans Lua
    assert groups_from({"attack_per_s": "1", "countries": "fr", "hosting": "AS1 2"}).hosting == (1, 2)


class GroupAdmin(FakeAdmin):
    tables: dict[str, str] = {}

    def command(self, line: str) -> str:
        if line.startswith("show table "):
            self.lines.append(line)
            return self.tables.get(line.removeprefix("show table "), "")
        return super().command(line)


class FakeSource:
    def __init__(self, folder: Path) -> None:
        self.refreshed = 0
        self.folder = folder

    def refresh(self, folder: Path, today: object) -> tuple[int, int]:
        self.refreshed += 1
        write_base(folder)
        return 4, 3

    def lookup(self, folder: Path, address: str) -> tuple[str, int]:
        return GeoReader(folder / "geo.bin").lookup(address)

    def names(self, folder: Path) -> dict[int, str]:
        return {16509: "Amazon.com, Inc.", 3215: "Orange"}


def groups_tools(tmp_path: Path, admin: GroupAdmin, clock: list[datetime]) -> GroupsTools:
    folder = tmp_path / "porte"
    folder.mkdir(parents=True, exist_ok=True)
    return GroupsTools(folder=folder, settings=JsonSettingsStore(tmp_path / "settings.json"), admin=admin,
                       source=FakeSource(folder), now=lambda: clock[0], lua=lambda: True, scripts=lua_scripts)


def test_tools_write_files_learn_and_refresh_the_base(tmp_path: Path) -> None:
    admin, clock = GroupAdmin(), [NOW]
    admin.tables = {"porte_ja4": "0x1: key=t13d1516h2_8daaf6152771_e5627efa2ab1 use=0 exp=1 conn_cnt=40 "
                                 "conn_rate(10000)=4\n0x2: key=t13d171200_ab0a1bf427ad_ecd0401ec68b use=0 exp=1 "
                                 "conn_cnt=3 conn_rate(10000)=0\n",
                    "porte_groupes": "0x3: key=empreinte use=0 exp=1 conn_cnt=37 conn_rate(60000)=37\n",
                    "porte_as": "0x4: key=AS16509 use=0 exp=1 conn_cnt=40 conn_rate(10000)=40\n"}
    tools = groups_tools(tmp_path, admin, clock)
    args = tools.render_args()
    assert args["ja4_ready"] is False and (tools.folder / "omega_ja4.lua").exists()
    assert (tools.folder / "navigateurs.lst").read_text() == "5b57614c22b0\n8daaf6152771\n"
    assert "AS16509\n" in (tools.folder / "as-hebergeurs.lst").read_text()
    for day in range(8):
        clock[0] = NOW + timedelta(days=day)
        admin.tables["porte_ja4"] = admin.tables["porte_ja4"].replace(
            f"conn_cnt={40 + 10 * day} ", f"conn_cnt={40 + 10 * (day + 1)} ")
        tools.learn(force=True)
    assert tools.ready() and tools.render_args()["ja4_ready"] is True
    assert "t13d1516h2_8daaf6152771_e5627efa2ab1" in (tools.folder / KNOWN_JA4_LIST).read_text()
    status = tools.status()
    assert status.learning_days_left == 0 and status.known == 1 and status.reasons == {"empreinte": 37}
    assert status.base_days is None and tools.base_due()
    outcome = tools.refresh_base()
    assert outcome.ok and admin.master_lines == ["reload"] and not tools.base_due()
    assert tools.top_as()[0].label == "Amazon.com, Inc." and tools.top_as()[0].hosting  # « (hébergeur) » : interface
    assert tools.top_fingerprints()[0].label == "Chrome, Edge, Firefox récent"
    assert tools.locate(CLOUD) == ("US", 16509)
    assert parse_rows("0x1: key=FR use=0 exp=1 conn_cnt=9 conn_rate(10000)=2\n")[0].count == 9


def test_gate_applies_groups_hot(tmp_path: Path) -> None:
    admin, clock = GroupAdmin(), [NOW]
    tools = make_gate(tmp_path, FunnelSim(PRODUCTION), admin=admin)
    tools.groups = groups_tools(tmp_path / "var", admin, clock)
    assert tools.prepare().ok
    assert "lua-load" in tools.config_path.read_text()
    tools.switch()
    # apprentissage en cours : « appliqués » reste en observation (lien apprentissage -> observation)
    outcome = tools.apply_groups({"mode": GROUPS_APPLY, "countries": "cn ru"})
    assert outcome.ok and outcome.params == {"days": 7, "warning": True}
    assert tools.groups.policy().mode == GROUPS_OBSERVE and tools.groups.policy().countries == ("CN", "RU")
    assert "reject if { var(sess.groupe) -m found }" not in tools.config_path.read_text()
    # apprentissage fini : « appliqués » s'applique
    clock[0] = NOW - timedelta(days=8)
    tools.groups.restart_learning()
    clock[0] = NOW
    outcome = tools.apply_groups({"mode": GROUPS_APPLY, "countries": "cn ru"})
    assert outcome.ok and outcome.params == {"mode": "appliqués"}  # libellé traduit à l'affichage (lot 9)
    text = tools.config_path.read_text()
    assert "reject if { var(sess.groupe) -m found }" in text
    assert (tools.folder / "pays-limites.lst").read_text() == "CN\nRU\n"
    # recommencer l'apprentissage remet en observation, a chaud
    reloads = admin.master_lines.count("reload")
    outcome = tools.restart_learning()
    assert outcome.ok and outcome.params == {"days": 7}
    assert tools.groups.policy().mode == GROUPS_OBSERVE and admin.master_lines.count("reload") == reloads + 1
    assert "reject if { var(sess.groupe) -m found }" not in tools.config_path.read_text()
    # deja en observation : seul l'apprentissage repart, sans rechargement
    assert tools.restart_learning().params == {"days": 7} and admin.master_lines.count("reload") == reloads + 1


def make_certificate(folder: Path) -> None:
    """Certificat jetable (auto-signe) pour le second etage de la porte."""
    key, cert = folder / "k.pem", folder / "c.pem"
    made = subprocess.run(["openssl", "req", "-x509", "-newkey", "ec", "-pkeyopt", "ec_paramgen_curve:P-256",
                           "-nodes", "-days", "2", "-subj", "/CN=essai", "-keyout", str(key), "-out", str(cert)],
                          capture_output=True)
    if made.returncode != 0:
        pytest.skip("openssl absent")
    (folder / "certificat.pem").write_text(cert.read_text() + key.read_text())


def _haproxy_with_lua() -> str:
    binary = shutil.which("haproxy")
    if not binary or "USE_LUA=1" not in subprocess.run([binary, "-vv"], capture_output=True, text=True).stdout:
        pytest.skip("HAProxy avec Lua absent")
    return binary


def test_real_haproxy_attack_mode_spares_browsers(tmp_path: Path) -> None:
    """Le vrai HAProxy avec les scripts de la porte : rafale dispersee d'un outil depuis un nuage, puis des
    navigateurs pendant l'attaque. Le Lua donne le meme pays / AS que Python."""
    binary = _haproxy_with_lua()
    folder = tmp_path / "p"
    folder.mkdir()
    write_base(folder)
    for name, text in lua_scripts().items():
        (folder / name).write_text(text)
    for name in ("confiance.lst", "ja4-connus.lst", "pays-limites.lst"):
        (folder / name).touch()
    (folder / "noire.lst").write_text("6.6.6.6\n")
    (folder / "navigateurs.lst").write_text("8daaf6152771\n")
    (folder / "as-hebergeurs.lst").write_text("AS16509\n")
    make_certificate(folder)
    with socket.socket() as probe:
        probe.bind(("127.0.0.1", 0))
        port = probe.getsockname()[1]
    config = render_config(GatePolicy(check_sni=False), TARGET, gate_port=port, folder=str(folder),
                           groups=GroupsPolicy(mode=GROUPS_APPLY, attack_per_s=5, ja4_per_10s=3, as_per_10s=3),
                           ja4_ready=True)
    config = config.replace("log stdout format short local0 info", "log stdout format raw local0 info")
    (folder / "haproxy.cfg").write_text(config)
    process = subprocess.Popen([binary, "-db", "-f", str(folder / "haproxy.cfg")], stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT, text=True)

    def send(address: str, hello: bytes) -> None:
        with socket.create_connection(("127.0.0.1", port), timeout=3) as connection:
            connection.sendall(proxy_v2_header(address) + hello)
            with contextlib.suppress(OSError):
                connection.recv(1)
    try:
        for _ in range(50):
            try:
                socket.create_connection(("127.0.0.1", port), timeout=1).close()
                break
            except OSError:
                time.sleep(0.1)
        bot, browser = python_hello(), chrome_like()
        send("6.6.6.6", browser)  # liste noire : refusee des la session (regle du lot 4), journalisee aussi
        started = time.monotonic()
        for index in range(30):
            send(f"3.5.{index}.9", bot)
        for index in range(20):
            send(f"90.1.{index}.4", browser)
        elapsed = time.monotonic() - started
        time.sleep(0.5)
    finally:
        process.terminate()
        output = process.communicate(timeout=10)[0]
    lines = [line for line in output.splitlines() if "motif=" in line]
    cloud = [line for line in lines if "as=AS16509" in line]
    homes = [line for line in lines if "as=AS3215" in line]
    assert all("pays=US" in line for line in cloud) and all("pays=FR" in line for line in homes)
    assert sum("groupe=empreinte" in line for line in cloud) >= 20, output
    assert len(homes) == 20 and not any("groupe=-" not in line for line in homes)  # navigateurs : jamais
    assert elapsed < 10, f"connexions retenues ({elapsed:.1f} s) : une condition attend la fin de l'inspection"
    # rapport (lot 7) : les refus se relisent dans le journal de la porte, motifs du lot 4 compris
    found = summarize(output.splitlines(), datetime.now().date())
    assert found.by_reason.get("liste-noire") == 1, output
    assert found.groups.get("empreinte", 0) >= 20
    assert found.addresses[0][1] == 1 and all(asn in ("AS16509", "") for _a, _c, asn, _p in found.addresses
                                               if _a.startswith("3.5."))


async def test_screens_show_groups_and_apply_them(tmp_path: Path) -> None:
    from test_tui import gate_app, settle
    from textual.widgets import Button, Input, Select, Static

    from omega_tail.interfaces.tui.screens.attacks import AttacksScreen
    from omega_tail.interfaces.tui.screens.firewall import FirewallScreen
    from omega_tail.interfaces.tui.widgets.tables import WideTable

    admin, clock = GroupAdmin(), [NOW]
    admin.tables = {"porte_ja4": "0x1: key=t13d1516h2_8daaf6152771_e5627efa2ab1 use=0 exp=1 conn_cnt=40 "
                                 "conn_rate(10000)=4\n",
                    "porte_attaque": "0x2: key=1 use=0 exp=240000 shard=0 conn_cnt=64\n",
                    "porte_groupes": "0x3: key=empreinte use=0 exp=1 conn_cnt=37 conn_rate(60000)=37\n",
                    "porte_ip": "0x4: key=::ffff:3.5.140.9 use=0 exp=3599731 shard=0 gpc0=0 conn_rate(10000)=57\n"}
    app = gate_app(tmp_path, FunnelSim(PRODUCTION), admin)
    assert app.gate is not None
    app.gate.groups = groups_tools(tmp_path / "var", admin, clock)
    write_base(app.gate.groups.folder)
    async with app.run_test(size=(130, 60)) as pilot:
        await settle(pilot)
        app.open_key("firewall")
        await settle(pilot)
        screen = app.screen
        assert isinstance(screen, FirewallScreen)
        state = str(screen.query_one("#groups-state", Static).render())
        assert "en observation" in state and "ATTAQUE" in state and "auraient été refusées (7 j) : empreinte 37" in state
        assert "DB-IP" in state
        screen.query_one("#groups-mode", Select).value = GROUPS_APPLY
        screen.query_one("#g-countries", Input).value = "cn, ru"
        screen.query_one("#apply-groups", Button).press()
        await settle(pilot)
        await pilot.pause(0.3)
        # apprentissage en cours : reste en observation, et la liste deroulante le montre
        assert app.gate.groups.policy().mode == GROUPS_OBSERVE and app.gate.groups.policy().countries == ("CN", "RU")
        assert screen.query_one("#groups-mode", Select).value == GROUPS_OBSERVE
        assert "restent en observation jusqu'à la fin" in str(screen.query_one("#groups-state", Static).render())
        clock[0] = NOW - timedelta(days=8)
        app.gate.groups.restart_learning()
        clock[0] = NOW
        screen.query_one("#groups-mode", Select).value = GROUPS_APPLY
        screen.query_one("#apply-groups", Button).press()
        await settle(pilot)
        await pilot.pause(0.3)
        assert app.gate.groups.policy().mode == GROUPS_APPLY
        app.open_key("attacks")
        await settle(pilot)
        await pilot.pause(0.3)
        attacks = app.screen
        assert isinstance(attacks, AttacksScreen)
        table = attacks.query_one("#attacks-table", WideTable)
        assert [str(cell) for cell in table.get_row_at(0)][:3] == ["3.5.140.9", "US", "AS16509"]
        assert "MODE ATTAQUE" in str(attacks.query_one("#counters", Static).render())
        attacks.query_one("#view-ja4", Button).press()
        await settle(pilot)
        await pilot.pause(0.3)
        assert str(table.get_row_at(0)[0]).startswith("t13d1516h2_8daaf6152771")
        assert attacks.query_one("#block", Button).disabled


def test_real_haproxy_accepts_every_variant(tmp_path: Path) -> None:
    binary = _haproxy_with_lua()
    folder = tmp_path / "v"
    folder.mkdir()
    for name, text in lua_scripts().items():
        (folder / name).write_text(text)
    for name in ("confiance.lst", "noire.lst", "ja4-connus.lst", "pays-limites.lst", "navigateurs.lst",
                 "as-hebergeurs.lst"):
        (folder / name).touch()
    make_certificate(folder)
    variants = [(GatePolicy(), None, False), (GatePolicy(), GroupsPolicy(), False),
                (GatePolicy(mode=MODE_OBSERVATION), GroupsPolicy(mode=GROUPS_APPLY), True),
                (GatePolicy(), GroupsPolicy(mode=GROUPS_APPLY, countries=("CN",)), True)]
    for index, (policy, groups, ready) in enumerate(variants):
        path = folder / f"{index}.cfg"
        text = render_config(policy, TARGET, gate_port=9443, folder=str(folder), groups=groups, ja4_ready=ready)
        path.write_text(text)
        done = subprocess.run([binary, "-c", "-q", "-f", str(path)], capture_output=True, text=True)
        assert done.returncode == 0, (index, done.stderr)
