# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Piege du demarrage (serveur-web, 2026-11-23) : un ExecStartPost `tailscale up` incomplet fait tomber tailscaled au
redemarrage des qu'un reglage a change (ici l'operateur). omega-tail le signale, le corrige sur demande (« - »
devant la commande, original garde), et le corrige d'abord avant tout redemarrage qu'il lance."""
from __future__ import annotations

from pathlib import Path

from conftest import NOW, FakeJournal, FakeService, FakeTailscale, service_state, snapshot, tools
from funnel_sim import FunnelSim
from omega_lib.terminal.models import RenderProfile
from test_survival import MIXED
from textual.widgets import Button, Static

from omega_tail.application.actions import ActionTools
from omega_tail.application.survival import SurvivalTools
from omega_tail.domain.alerts import Target, alerts_for
from omega_tail.domain.startup import risky_hooks, soften
from omega_tail.infrastructure.survival_store import FileCutStore
from omega_tail.infrastructure.system.systemd import parse_show
from omega_tail.interfaces.tui.app import OmegaTailApp

OVERRIDE = "/etc/systemd/system/tailscaled.service.d/override.conf"
OVERRIDE_TEXT = """[Service]
ExecStart=
ExecStart=/usr/bin/tailscaled --state=/var/lib/tailscale/tailscaled.state --socket=/run/tailscale/tailscaled.sock
ExecStartPost=/usr/bin/tailscale up --accept-dns=false --accept-routes=true
[Unit]
After=nordvpnd.service
"""
UP = "/usr/bin/tailscale up --accept-dns=false --accept-routes=true"
SHOW = f"""Id=tailscaled.service
LoadState=loaded
ActiveState=active
DropInPaths=/etc/systemd/system/tailscaled.service.d/50-omega-tail.conf {OVERRIDE}
FragmentPath=/usr/lib/systemd/system/tailscaled.service
ExecStartPost={{ path=/usr/bin/tailscale ; argv[]={UP} ; ignore_errors=no ; start_time=[n/a] ; pid=0 ; code=(null) }}
ExecStartPre={{ path=/usr/bin/true ; argv[]=/usr/bin/true ; ignore_errors=yes ; pid=0 }}
"""


def test_the_failing_tailscale_up_is_read_and_signalled() -> None:
    state = parse_show(SHOW)
    assert state.start_hooks == (UP,) and risky_hooks(state) == (UP,)
    assert not risky_hooks(parse_show(SHOW.replace("ignore_errors=no", "ignore_errors=yes")))
    assert not risky_hooks(service_state(start_hooks=("/usr/bin/tailscale up --reset --operator=k",)))
    assert not risky_hooks(service_state(start_hooks=("/usr/bin/tailscale set --operator=k",)))
    found = [alert for alert in alerts_for(snapshot(service=state), NOW) if alert.code == "startup-up"]
    assert found and found[0].target is Target.SERVICE
    assert not [alert for alert in alerts_for(snapshot(), NOW) if alert.code == "startup-up"]


def test_soften_adds_the_dash_and_nothing_else() -> None:
    fixed = soften(OVERRIDE_TEXT)
    assert f"ExecStartPost=-{UP}\n" in fixed
    assert fixed.replace(f"ExecStartPost=-{UP}", f"ExecStartPost={UP}") == OVERRIDE_TEXT
    assert soften(fixed) == fixed  # deja corrige : rien
    assert soften("ExecStartPost=/usr/bin/other up\nExecStartPre=@-/usr/bin/tailscale up\n") == \
        "ExecStartPost=/usr/bin/other up\nExecStartPre=@-/usr/bin/tailscale up\n"


def survival(tmp_path: Path) -> SurvivalTools:
    sim = FunnelSim(MIXED)
    return SurvivalTools(store=FileCutStore(tmp_path / "var"), serve_config=sim.serve_config, quiet=sim.quiet,
                         now=lambda: NOW, python="/x/python", user=lambda: "kraynux")


def test_fix_commands_keep_the_original_and_never_touch_package_files(tmp_path: Path) -> None:
    files = {OVERRIDE: OVERRIDE_TEXT, "/usr/lib/systemd/system/tailscaled.service": f"ExecStartPost={UP}\n"}
    state = parse_show(SHOW)
    commands = survival(tmp_path).startup_fix_commands(state, lambda path: files.get(path, ""))
    assert [command[:3] for command in commands] == [("sudo", "install", "-m"), ("sudo", "systemctl", "daemon-reload")]
    assert commands[0][-1] == OVERRIDE
    assert f"ExecStartPost=-{UP}" in Path(commands[0][-2]).read_text()
    kept = [path for path in (tmp_path / "var" / "survie").iterdir() if ".avant-" in path.name]
    assert len(kept) == 1 and kept[0].read_text() == OVERRIDE_TEXT
    assert survival(tmp_path).startup_fix_commands(service_state(), lambda path: "") == []


def risky_app(tmp_path: Path, ran: list[tuple[str, ...]]) -> OmegaTailApp:
    state = parse_show(SHOW)
    return OmegaTailApp(snapshots=tools(FakeTailscale(), FakeService(state)), journal=FakeJournal(),
                        actions=ActionTools(run=lambda argv: ran.append(tuple(argv)) or 0), version="0.4.0",
                        render_profile=RenderProfile.STANDARD, splash=False, refresh_seconds=0,
                        survival=survival(tmp_path), ssh_unit="sshd.service",
                        read_file=lambda path: OVERRIDE_TEXT if path == OVERRIDE else "")


async def test_restart_and_confinement_fix_the_startup_first(tmp_path: Path) -> None:
    from test_tui import settle

    ran: list[tuple[str, ...]] = []
    app = risky_app(tmp_path, ran)
    async with app.run_test(size=(130, 60)) as pilot:
        await settle(pilot)
        app.open_key("service")
        await settle(pilot)
        assert app.screen.query_one("#fix-startup", Button).parent.display
        assert "tailscale up" in str(app.screen.query_one("#service-box", Static).render())
        app.screen.query_one("#do-restart", Button).press()
        await pilot.pause()
        text = str(app.screen.query_one("#confirm-text", Static).render())
        assert "ajoute « - »" in text and OVERRIDE in text
        app.screen.query_one("#confirm", Button).press()
        await settle(pilot)
        assert [command[:3] for command in ran] == [("sudo", "install", "-m"), ("sudo", "systemctl", "daemon-reload"),
                                                     ("sudo", "systemctl", "restart")]
        ran.clear()
        app.confine(restart=True, ssh_unit="")
        await pilot.pause()
        app.screen.query_one("#confirm", Button).press()
        await settle(pilot)
        assert ran[0][-1] == OVERRIDE and ran[-1] == ("sudo", "systemctl", "restart", "tailscaled.service")


def test_status_band_shows_firewall_and_watch() -> None:
    from conftest import FUNNEL_HTTPS

    from omega_tail.domain.tailscale import Publication, PublishMode
    from omega_tail.domain.watch import WatchStatus
    from omega_tail.interfaces.tui.widgets.status_band import BAD, OFF, OK, WARN, band_parts

    def parts(**changes: object) -> dict[str, str]:
        return dict(band_parts(snapshot(**changes)))

    gated = Publication(443, True, PublishMode.TCP, "x", "tcp://127.0.0.1:9443", "", proxy_protocol=2)
    assert parts(publications=(gated,), gate_service=service_state())["Pare-feu actif"] == OK
    assert parts(publications=(gated,), gate_service=service_state(active="failed"))["Pare-feu arrêté"] == BAD
    assert parts(publications=(FUNNEL_HTTPS,))["Pare-feu inactif"] == WARN
    assert parts()["Pare-feu inactif"] == OFF
    status = WatchStatus(installed=True, alive=True, level=0, strikes=0, next_minutes=15)
    assert parts(watch=status)["Veille active"] == OK
    assert parts(watch=WatchStatus(True, False, 0, 0, 15))["Veille arrêtée"] == BAD
    assert parts(watch=WatchStatus(False, False, 0, 0, 15))["Veille inactive"] == OFF
    assert not [label for label in parts() if label.startswith("Veille")]  # veille inconnue : rien


def test_status_band_shows_memory_next_to_temperature() -> None:
    from omega_tail.domain.machine import MachineState
    from omega_tail.infrastructure.system.machine import memory
    from omega_tail.interfaces.tui.widgets.status_band import BAD, OK, WARN, band_parts

    total, available = memory("MemTotal:        8000000 kB\nMemFree:  100 kB\nMemAvailable:    5000000 kB\n")
    assert (total, available) == (8000000 * 1024, 5000000 * 1024)
    assert memory("") == (None, None)

    def labels(available_kb: int) -> list[tuple[str, str]]:
        machine = MachineState(temperature_c=60.0, memory_total_bytes=1000 * 1024,
                               memory_available_bytes=available_kb * 1024)
        return band_parts(snapshot(machine=machine))

    found = labels(625)
    names = [label for label, _ in found]
    assert names[names.index("60 °C") + 1] == "RAM 38 %" and dict(found)["RAM 38 %"] == OK
    assert dict(labels(100))["RAM 90 %"] == WARN and dict(labels(20))["RAM 98 %"] == BAD
    assert not [label for label, _ in band_parts(snapshot()) if label.startswith("RAM")]


def test_status_band_wraps_between_lights_only() -> None:
    from omega_tail.interfaces.tui.widgets.status_band import band_content

    full = band_content(snapshot()).plain
    assert "\n" not in full
    narrow = band_content(snapshot(), 40).plain
    assert all(len(line) <= 40 for line in narrow.splitlines()) and len(narrow.splitlines()) > 1
    assert all(line.startswith("●") for line in narrow.splitlines())  # jamais coupee au milieu d'un voyant
