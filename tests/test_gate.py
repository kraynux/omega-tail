# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Pare-feu Funnel (lot 4) : configuration HAProxy, publication prise en charge, pilotage avec de faux HAProxy et
Tailscale. Les regles elles-memes ont ete validees en reel sur le J3455 le 2026-11-22 (injecteur PROXY v2 puis
Funnel public)."""
from __future__ import annotations

import io
from contextlib import redirect_stdout
from datetime import datetime, timezone
from pathlib import Path

import pytest
from conftest import NOW, snapshot
from funnel_sim import HOST, FunnelSim

from omega_tail.application.gate import GateTools, parse_counters, parse_table
from omega_tail.domain.alerts import Level, Target, alerts_for
from omega_tail.domain.funnel import handlers_of
from omega_tail.domain.gate import (
    MODE_OBSERVATION,
    Backend,
    GatePolicy,
    GateTarget,
    UnsupportedPublication,
    backend_of,
    gate_target,
    is_gate_publication,
    policy_from,
    render_config,
    switch_commands,
    unit_text,
)
from omega_tail.domain.service import ServiceState
from omega_tail.domain.tailscale import Publication, PublishMode
from omega_tail.infrastructure.gate import proxy_v2_header
from omega_tail.infrastructure.settings.json_store import JsonSettingsStore
from omega_tail.infrastructure.survival_store import FileCutStore
from omega_tail.interfaces.cli.main import main_with

PRODUCTION = {"TCP": {"443": {"HTTPS": True}, "3389": {"TCPForward": "localhost:3389"}},
              "Web": {f"{HOST}:443": {"Handlers": {"/": {"Proxy": "http://127.0.0.1:8080"}}}},
              "AllowFunnel": {f"{HOST}:443": True}}
TARGET = GateTarget(443, HOST, Backend("127.0.0.1:8080"))


def test_backend_and_supported_publication() -> None:
    assert backend_of("http://localhost:80") == Backend("127.0.0.1:80")
    assert backend_of("https://127.0.0.1:8443") == Backend("127.0.0.1:8443", tls=True, verify=True)
    assert backend_of("https+insecure://localhost:8443") == Backend("127.0.0.1:8443", tls=True)
    assert backend_of("localhost:3000") == Backend("127.0.0.1:3000")
    with pytest.raises(UnsupportedPublication):
        backend_of("http://127.0.0.1:80/sous-chemin")
    assert gate_target(PRODUCTION, HOST) == TARGET
    two_paths = {**PRODUCTION, "Web": {f"{HOST}:443": {"Handlers": {"/": {"Proxy": "http://127.0.0.1:1"},
                                                                    "/b": {"Proxy": "http://127.0.0.1:2"}}}}}
    for bad, reason in ((two_paths, "chemin"), ({"TCP": {"3389": {"TCPForward": "x:1"}}}, "aucun port"),
                        ({"TCP": {"443": {"TCPForward": "127.0.0.1:9443", "ProxyProtocol": 2}},
                          "AllowFunnel": {f"{HOST}:443": True}}, "déjà")):
        with pytest.raises(UnsupportedPublication, match=reason):
            gate_target(bad, HOST)
    with pytest.raises(UnsupportedPublication, match="nom"):
        gate_target(PRODUCTION, "nom; inattendu")


def test_policy_is_bounded() -> None:
    assert policy_from({}) == GatePolicy()
    policy = policy_from({"ip_per_10s": "15", "global_per_s": "0", "mode": "observation", "check_sni": "False"})
    assert (policy.ip_per_10s, policy.global_per_s, policy.mode, policy.check_sni) == (15, 100, MODE_OBSERVATION,
                                                                                         False)
    assert policy_from({"mode": "n'importe quoi; reject"}).mode == "normal"


def test_config_rules_run_after_proxy_and_before_tls() -> None:
    text = render_config(GatePolicy(ip_per_10s=25), TARGET, gate_port=9443, folder="/v/porte")
    assert "bind 127.0.0.1:9443 accept-proxy" in text
    assert "tcp-request connection" not in text  # avant la lecture de PROXY : constate en reel, interdit
    assert "tcp-request session sc-inc-gpc0(0) if !{ var(sess.motif) -m found } { sc0_conn_rate gt 25 }" in text
    assert "tcp-request session reject if { var(sess.motif) -m found }" in text
    assert f"!{{ req.ssl_sni -i {HOST} }}" in text
    assert "stick-table type ipv6" in text and "ipmask(24,64)" in text
    assert "bind abns@omega-tail-tls-9443 accept-proxy ssl crt /v/porte/certificat.pem" in text
    assert "http-request set-header X-Forwarded-For %[src]" in text  # remplace, jamais ajoute
    assert "server origine 127.0.0.1:8080\n" in text
    assert "localpeer omega-tail" in text and "peer omega-tail unix@/v/porte/pairs.sock" in text  # tables gardees (F4)
    assert text.count("peers omega_tail_pairs") == 3  # la section et ses deux tables
    observe = render_config(GatePolicy(mode=MODE_OBSERVATION, check_sni=False), TARGET, gate_port=9443,
                            folder="/v/porte")
    assert "reject" not in observe and "req.ssl_sni" not in observe


def test_switch_commands_and_unit() -> None:
    assert switch_commands(TARGET, 9443) == (
        ("tailscale", "funnel", "--https=443", "off"),
        ("tailscale", "funnel", "--bg", "--yes", "--tcp=443", "--proxy-protocol=2", "tcp://127.0.0.1:9443"))
    unit = unit_text(user="kraynux", haproxy="/usr/bin/haproxy", folder="/home/k/omega-tail/var/porte")
    assert "User=kraynux" in unit and "ReadWritePaths=/home/k/omega-tail/var/porte" in unit
    assert "-S /home/k/omega-tail/var/porte/master.sock" in unit and "root" not in unit.split("[Service]")[1]


def test_parse_table_and_counters() -> None:
    table = ("# table: porte_ip, type: ipv6, size:1048576, used:2\n"
             "0x1: key=::ffff:37.67.116.15 use=0 exp=3599731 shard=0 gpc0=1 conn_rate(10000)=57\n"
             "0x2: key=2001:db8::5 use=0 exp=3599893 shard=0 gpc0=0 conn_rate(10000)=1\n")
    rows = parse_table(table)
    assert rows[0].address == "37.67.116.15" and rows[0].blocked and rows[0].rate_10s == 57
    assert rows[0].expires_s == 3599 and rows[1].address == "2001:db8::5" and not rows[1].blocked
    stat = ("# pxname,svname,scur,stot,dcon,dses,dreq\nporte,FRONTEND,1,46,0,22,1\nporte_tls,FRONTEND,0,23,0,0,0\n"
            "service,BACKEND,0,23,,,\n")
    counters = parse_counters(stat)
    assert (counters.total, counters.current, counters.refused, counters.admitted) == (46, 1, 23, 23)
    assert parse_counters("") == parse_counters("# pxname\n")


def test_local_probe_header_is_proxy_v2() -> None:
    header = proxy_v2_header("192.0.2.1")
    assert header.startswith(b"\r\n\r\n\x00\r\nQUIT\n\x21\x11") and len(header) == 28
    assert proxy_v2_header("2001:db8::1")[13] == 0x21 and len(proxy_v2_header("2001:db8::1")) == 52


class FakeAdmin:
    def __init__(self, running: bool = True) -> None:
        self.running, self.lines, self.master_lines = running, [], []

    def command(self, line: str) -> str:
        if not self.running:
            raise OSError("porte arretee")
        self.lines.append(line)
        return "# pxname,svname,scur,stot,dcon,dses,dreq\nporte,FRONTEND,0,3,0,1,0\n" if line == "show stat" else ""

    def master(self, line: str) -> str:
        self.master_lines.append(line)
        return "Success=1"


class FakeMachine:
    def __init__(self, *, public_ok: bool = True, local_ok: bool = True, config_ok: bool = True) -> None:
        self.public_ok, self.local_ok, self.config_ok = public_ok, local_ok, config_ok

    def haproxy(self) -> str:
        return "/usr/bin/haproxy"

    def check_config(self, path: str) -> tuple[bool, str]:
        return self.config_ok, "" if self.config_ok else "[ALERT] parsing"

    def fetch_certificate(self, dns_name: str, cert: str, key: str) -> tuple[bool, str]:
        Path(cert).write_text("CERT\n")
        Path(key).write_text("KEY\n")
        return True, ""

    def certificate_expiry_days(self, pem: str) -> int | None:
        return 80

    def local_probe(self, gate_port: int, dns_name: str) -> tuple[bool, str]:
        return self.local_ok, "HTTP/1.1 200 OK"

    def public_probe(self, dns_name: str, port: int) -> tuple[bool, str]:
        return self.public_ok, "HTTP/1.1 200 OK via 176.58.90.145"

    def install_command(self) -> tuple[str, ...]:
        return ("sudo", "pacman", "-S", "--needed", "--noconfirm", "haproxy")


def gate(tmp_path: Path, sim: FunnelSim, *, machine: FakeMachine | None = None,
         admin: FakeAdmin | None = None) -> GateTools:
    folder = tmp_path / "var" / "porte"
    folder.mkdir(parents=True)
    return GateTools(folder=folder, settings=JsonSettingsStore(tmp_path / "var" / "settings.json"),
                     admin=admin or FakeAdmin(), machine=machine or FakeMachine(), store=FileCutStore(tmp_path / "var"),
                     serve_config=sim.serve_config, quiet=sim.quiet, dns_name=lambda: HOST, user=lambda: "kraynux",
                     python="/x/python", now=lambda: datetime(2026, 11, 22, 23, 0, tzinfo=timezone.utc))


def test_prepare_writes_everything_and_service_commands(tmp_path: Path) -> None:
    tools = gate(tmp_path, FunnelSim(PRODUCTION))
    assert tools.prepare().ok
    folder = tmp_path / "var" / "porte"
    assert (folder / "certificat.pem").read_text() == "CERT\nKEY\n"
    assert (folder / "certificat.pem").stat().st_mode & 0o777 == 0o600
    assert "server origine 127.0.0.1:8080" in (folder / "haproxy.cfg").read_text()
    assert (folder / "confiance.lst").exists() and (folder / "noire.lst").exists()
    assert "porte certificat --si-besoin" in (folder / "omega-tail-porte-certificat.service").read_text()
    commands = tools.service_commands()
    assert commands[0][:4] == ("sudo", "install", "-m", "0644") and commands[-2][:3] == ("sudo", "systemctl", "enable")
    assert all("/etc/systemd/system/" in command[-1] for command in commands[:3])
    refused = gate(tmp_path / "b", FunnelSim(PRODUCTION), machine=FakeMachine(config_ok=False)).prepare()
    assert not refused.ok and "refusée par HAProxy" in refused.message


def test_switch_then_unswitch_restores_the_original(tmp_path: Path) -> None:
    sim = FunnelSim(PRODUCTION)
    tools = gate(tmp_path, sim)
    assert tools.prepare().ok
    outcome = tools.switch()
    assert outcome.ok and is_gate_publication(sim.config, 9443)
    assert tools.state() is not None and tools.state().backend == "127.0.0.1:8080"
    assert not tools.switch().ok  # deja active
    assert tools.unswitch().ok and sim.config == PRODUCTION and tools.state() is None


def test_failed_public_probe_rolls_back(tmp_path: Path) -> None:
    sim = FunnelSim(PRODUCTION)
    waits: list[float] = []
    tools = gate(tmp_path, sim, machine=FakeMachine(public_ok=False))
    assert tools.prepare().ok
    outcome = tools.switch(wait=waits.append)
    assert not outcome.ok and "remise" in outcome.message and len(waits) == 5
    assert sim.config["TCP"]["443"] == {"HTTPS": True} and tools.state() is None
    assert any(handler.public and handler.kind == "https" for handler in handlers_of(sim.config))


def test_local_probe_failure_switches_nothing(tmp_path: Path) -> None:
    sim = FunnelSim(PRODUCTION)
    tools = gate(tmp_path, sim, machine=FakeMachine(local_ok=False))
    assert not tools.switch().ok and sim.calls == [] and sim.config == PRODUCTION


def test_hot_actions(tmp_path: Path) -> None:
    admin = FakeAdmin()
    tools = gate(tmp_path, FunnelSim(PRODUCTION), admin=admin)
    assert tools.block("203.0.113.7").ok and admin.lines[-1] == "set table porte_ip key 203.0.113.7 data.gpc0 1"
    assert tools.block("198.51.100.0/24").ok and tools.lists()[1] == ["198.51.100.0/24"]
    assert admin.lines[-1].startswith("add acl ") and admin.lines[-1].endswith("noire.lst 198.51.100.0/24")
    assert tools.unblock("198.51.100.0/24").ok and tools.lists()[1] == []
    assert tools.trust("2001:db8::1").ok and tools.lists()[0] == ["2001:db8::1"]
    assert not tools.block("1.2.3.4; reject").ok  # jamais de texte libre vers HAProxy
    assert tools.counters().refused == 1


def test_lists_stay_exclusive_and_say_where_the_address_is(tmp_path: Path) -> None:
    from omega_tail.application.gate import BLACK, TRUSTED, TableRow, decision_rows, place
    tools = gate(tmp_path, FunnelSim(PRODUCTION), admin=FakeAdmin())
    trusted = tools.trust("203.0.113.7")
    assert trusted.ok and "→ confiance" in trusted.message and trusted.params["inactive"]  # porte arrêtée
    refused = tools.block("203.0.113.7")  # la confiance passe avant : le blocage ne servirait à rien
    assert not refused.ok and "Retirez-la de la confiance" in refused.message
    moved = tools.block("203.0.113.7", forever=True)
    assert moved.ok and "→ liste noire" in moved.message and "retirée de la confiance" in moved.message
    assert tools.lists() == ([], ["203.0.113.7"])
    back = tools.trust("203.0.113.7")
    assert "→ confiance" in back.message and "retirée de la liste noire" in back.message and tools.lists() == (["203.0.113.7"], [])
    assert place("198.51.100.9", [], ["198.51.100.0/24"]) == BLACK
    assert place("2001:db8::1", ["2001:db8::/48"], ["2001:db8::/32"]) == TRUSTED
    rows = decision_rows([TableRow("198.51.100.9", 3, False, 0), TableRow("192.0.2.1", 90, True, 600)],
                         ["203.0.113.7"], ["198.51.100.0/24"])
    assert [(row.address, row.listed, row.seen) for row in rows] == [
        ("198.51.100.9", BLACK, True), ("198.51.100.0/24", BLACK, False), ("192.0.2.1", "", True),
        ("203.0.113.7", TRUSTED, False)]


def test_tailnet_is_always_admitted(tmp_path: Path) -> None:
    """Decision (2026-11-24) : la porte protege Funnel d'Internet et laisse le tailnet tranquille.
    Constate sur serveur-web : 300 requetes d'essai depuis une machine du tailnet l'avaient bloquee 60 min."""
    from omega_tail.application.gate import TRUSTED, in_tailnet, place
    for mode in (GatePolicy(), GatePolicy(mode=MODE_OBSERVATION)):
        text = render_config(mode, TARGET, gate_port=9443, folder="/v/porte")
        assert "    acl tailnet src 100.64.0.0/10 fd7a:115c:a1e0::/48\n" in text
        accept = text.index("tcp-request session accept if confiance or tailnet\n")
        assert accept < text.index("track-sc0 src table porte_ip")  # avant tout compteur et tout refus
    assert place("100.64.10.47", [], []) == TRUSTED and place("fd7a:115c:a1e0::2601:3d3d", [], []) == TRUSTED
    assert place("100.64.10.47", [], ["100.0.0.0/8"]) == TRUSTED  # le tailnet passe avant la liste noire
    assert place("92.92.129.57", [], []) == ""  # un visiteur de Funnel garde ses regles
    assert in_tailnet("100.64.0.0/10") and not in_tailnet("100.0.0.0/8") and not in_tailnet("100.63.255.1")
    tools = gate(tmp_path, FunnelSim(PRODUCTION), admin=FakeAdmin())
    for entry in ("100.64.10.47", "fd7a:115c:a1e0::1"):
        refused = tools.block(entry)
        assert not refused.ok and "fait partie du tailnet" in refused.message
        assert not tools.block(entry, forever=True).ok
    assert tools.lists() == ([], [])
    assert tools.block("100.0.0.0/8").ok  # reseau plus large : sa part publique reste refusable
    assert tools.trust("100.64.0.0/10").ok
    removed = tools.trust("100.64.0.0/10", add=False)
    assert removed.ok and "→ toujours admise" in removed.message


def test_apply_policy_reloads_only_a_valid_config(tmp_path: Path) -> None:
    admin = FakeAdmin()
    sim = FunnelSim(PRODUCTION)
    tools = gate(tmp_path, sim, admin=admin)
    assert tools.apply_policy({"ip_per_10s": "30"}).message.startswith("Règles enregistrées")  # pas encore active
    assert tools.prepare().ok and tools.switch().ok
    assert tools.apply_policy({"mode": "observation"}).ok and admin.master_lines == ["reload"]
    assert "reject" not in (tmp_path / "var" / "porte" / "haproxy.cfg").read_text()
    tools.machine = FakeMachine(config_ok=False)
    refused = tools.apply_policy({"mode": "normal"})
    assert not refused.ok and "reject" not in (tmp_path / "var" / "porte" / "haproxy.cfg").read_text()


def test_gate_down_is_critical() -> None:
    gated = Publication(443, True, PublishMode.TCP, HOST, "tcp://127.0.0.1:9443", "", 2)
    shot = snapshot(publications=(gated,), gate_service=ServiceState(known=True, active="failed"))
    (alert,) = [alert for alert in alerts_for(shot, NOW) if alert.code == "gate-down"]
    assert alert.level is Level.CRITICAL and alert.target is Target.FIREWALL
    running = snapshot(publications=(gated,), gate_service=ServiceState(known=True, active="active"))
    assert "gate-down" not in [alert.code for alert in alerts_for(running, NOW)]


def test_cli_porte(tmp_path: Path) -> None:
    tools = gate(tmp_path, FunnelSim(PRODUCTION))
    assert tools.prepare().ok
    out = io.StringIO()
    with redirect_stdout(out):
        assert main_with(["porte", "bloquer", "203.0.113.9"], version="x", state=lambda: None,  # type: ignore[arg-type]
                         dashboard=lambda: 0, gate=lambda: tools) == 0
        assert main_with(["porte", "etat"], version="x", state=lambda: None,  # type: ignore[arg-type]
                         dashboard=lambda: 0, gate=lambda: tools) == 0
        assert main_with(["porte", "certificat", "--si-besoin"], version="x", state=lambda: None,  # type: ignore[arg-type]
                         dashboard=lambda: 0, gate=lambda: tools) == 0
    text = out.getvalue()
    assert "203.0.113.9 → bloquée 60 min (blocage temporaire" in text and "Porte inactive" in text and "valable encore 80" in text
    assert "Certificat : 80 jour(s) restants" in text
