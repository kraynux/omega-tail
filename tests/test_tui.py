# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Interface pilotee (Textual) avec de faux lecteurs : jamais le vrai Tailscale, systemd, journal ou sudo."""
from __future__ import annotations

from pathlib import Path

from conftest import (
    FUNNEL_HTTPS,
    NOW,
    FakeJournal,
    FakeService,
    FakeTailscale,
    service_state,
    tailscale_state,
    tools,
)
from funnel_sim import FunnelSim
from omega_lib.terminal.models import RenderProfile
from test_survival import MIXED
from textual.widgets import Button, Checkbox, RichLog, Static

from omega_tail.application.actions import ActionTools
from omega_tail.application.settings import SettingsTools
from omega_tail.application.survival import SurvivalTools
from omega_tail.application.watch import WatchTools
from omega_tail.domain.funnel import handlers_of
from omega_tail.domain.service import ServiceAction
from omega_tail.domain.tailscale import Publication, PublishMode
from omega_tail.infrastructure.exports.writer import FileExportWriter
from omega_tail.infrastructure.settings.directories import clear_directory
from omega_tail.infrastructure.settings.json_store import JsonSettingsStore
from omega_tail.infrastructure.survival_store import FileCutStore
from omega_tail.interfaces.tui.app import OmegaTailApp
from omega_tail.interfaces.tui.screens.breaker_proposal import BreakerProposalScreen
from omega_tail.interfaces.tui.screens.confirm import ConfirmScreen
from omega_tail.interfaces.tui.screens.dashboard import DashboardScreen
from omega_tail.interfaces.tui.screens.home import HomeScreen
from omega_tail.interfaces.tui.screens.journals import JournalsScreen
from omega_tail.interfaces.tui.screens.service import ServiceScreen
from omega_tail.interfaces.tui.screens.splash import SplashScreen
from omega_tail.interfaces.tui.screens.survival import SurvivalScreen
from omega_tail.interfaces.tui.widgets.status_band import StatusBand
from omega_tail.interfaces.tui.widgets.tables import WideTable


def make_app(tmp_path: Path, *, tailscale: FakeTailscale | None = None, service: FakeService | None = None,
             through: bool = False, splash: bool = False, journal: FakeJournal | None = None,
             ran: list[tuple[str, ...]] | None = None) -> OmegaTailApp:
    settings = SettingsTools(JsonSettingsStore(tmp_path / "settings.json"), tmp_path / "exports",
                             tmp_path / "shots", lambda d: clear_directory(d, tmp_path), tmp_path)
    record = ran if ran is not None else []
    return OmegaTailApp(snapshots=tools(tailscale, service, through), journal=journal or FakeJournal(),
                        actions=ActionTools(run=lambda argv: record.append(tuple(argv)) or 0),
                        version="0.1.0", render_profile=RenderProfile.STANDARD, settings=settings, splash=splash,
                        writer=FileExportWriter(settings.exports_dir),
                        refresh_seconds=0)


async def settle(pilot) -> None:  # type: ignore[no-untyped-def]
    await pilot.app.workers.wait_for_complete()
    await pilot.pause()


async def test_splash_then_menu_of_two_columns_of_six(tmp_path: Path) -> None:
    app = make_app(tmp_path, splash=True)
    async with app.run_test(size=(100, 40)) as pilot:
        assert isinstance(app.screen, SplashScreen)
        await pilot.press("x")
        assert isinstance(app.screen, HomeScreen)
        buttons = [button.id for button in app.screen.query(Button)]
        assert len(buttons) == 12 and "menu-quit" not in buttons
        await settle(pilot)
        band = str(app.screen.query_one(StatusBand).render())
        assert "tailscaled actif 1.104.7" in band and "Funnel fermé" in band and "78 °C" in band and "CPU tailscaled 6 %" in band


async def test_screen_without_its_tools_says_so(tmp_path: Path) -> None:
    app = make_app(tmp_path)  # sans outils reseau : l'ecran n'est pas ouvert, une notification le dit
    async with app.run_test(size=(100, 40)) as pilot:
        await settle(pilot)
        app.screen.query_one("#menu-network", Button).press()
        await pilot.pause()
        assert isinstance(app.screen, HomeScreen)
        assert app._notifications


async def test_dashboard_shows_alerts_and_fix_opens_service(tmp_path: Path) -> None:
    app = make_app(tmp_path, tailscale=FakeTailscale(tailscale_state(daemon_version="1.104.4"), (FUNNEL_HTTPS,)))
    async with app.run_test(size=(120, 45)) as pilot:
        await settle(pilot)
        app.screen.query_one("#menu-dashboard", Button).press()
        await settle(pilot)
        screen = app.screen
        assert isinstance(screen, DashboardScreen)
        table = screen.query_one("#alerts-table", WideTable)
        assert table.row_count == 4  # demon en retard, Funnel sans porte, temperature 78 °C, non confine
        publication = str(screen.query_one("#publication-box", Static).render())
        assert "Internet (Funnel)" in publication and "HTTPS (TLS par tailscaled)" in publication
        assert not screen.query_one("#operator", Button).parent.display  # deja operateur : pas de cadre vide
        table.move_cursor(row=0)
        screen.query_one("#fix", Button).press()
        await settle(pilot)
        assert isinstance(app.screen, ServiceScreen)
        text = str(app.screen.query_one("#service-box", Static).render())
        assert "« Redémarrer » l'applique" in text


async def test_become_operator_shows_the_command_then_runs_it(tmp_path: Path) -> None:
    ran: list[tuple[str, ...]] = []
    app = make_app(tmp_path, tailscale=FakeTailscale(operator=""), ran=ran)
    async with app.run_test(size=(120, 45)) as pilot:
        await settle(pilot)
        app.screen.query_one("#menu-dashboard", Button).press()
        await settle(pilot)
        button = app.screen.query_one("#operator", Button)
        assert button.parent.display
        button.press()
        await pilot.pause()
        assert isinstance(app.screen, ConfirmScreen)
        assert "sudo tailscale set --operator=kraynux" in str(app.screen.query_one("#confirm-text", Static).render())
        app.screen.query_one("#confirm", Button).press()
        await settle(pilot)
        assert ran == [("sudo", "tailscale", "set", "--operator=kraynux")]


async def test_stop_through_tailscale_needs_a_second_confirmation(tmp_path: Path) -> None:
    ran: list[tuple[str, ...]] = []
    app = make_app(tmp_path, through=True, ran=ran)
    async with app.run_test(size=(120, 45)) as pilot:
        await settle(pilot)
        app.open_key("service")
        await settle(pilot)
        assert app.screen.query_one("#do-start", Button).disabled
        app.screen.query_one("#do-stop", Button).press()
        await pilot.pause()
        assert "passe par Tailscale" in str(app.screen.query_one("#confirm-text", Static).render())
        app.screen.query_one("#confirm", Button).press()
        await pilot.pause()
        assert isinstance(app.screen, ConfirmScreen)  # seconde confirmation
        app.screen.query_one("#cancel", Button).press()
        await settle(pilot)
        assert ran == []


async def test_restart_runs_after_one_confirmation(tmp_path: Path) -> None:
    ran: list[tuple[str, ...]] = []
    app = make_app(tmp_path, ran=ran, service=FakeService(service_state()))
    async with app.run_test(size=(120, 45)) as pilot:
        await settle(pilot)
        app.open_key("service")
        await settle(pilot)
        app.screen.query_one(f"#do-{ServiceAction.RESTART.value}", Button).press()
        await pilot.pause()
        app.screen.query_one("#confirm", Button).press()
        await settle(pilot)
        assert ran == [("sudo", "systemctl", "restart", "tailscaled.service")]


async def test_journals_filter_and_export(tmp_path: Path) -> None:
    journal = FakeJournal()
    app = make_app(tmp_path, journal=journal)
    async with app.run_test(size=(120, 45)) as pilot:
        await settle(pilot)
        app.open_key("journals")
        await settle(pilot)
        screen = app.screen
        assert isinstance(screen, JournalsScreen)
        assert journal.calls == [("tailscaled", 300)]
        assert len(screen.query_one("#journal-log", RichLog).lines) == 3
        await pilot.click("#journal-filter")
        await pilot.press(*"error")
        await pilot.pause()
        assert len(screen.query_one("#journal-log", RichLog).lines) == 1
        screen.query_one("#export", Button).press()
        await pilot.pause()
        exported = list((tmp_path / "exports").glob("omega-tail-journal-tailscaled-*.txt"))
        assert len(exported) == 1 and exported[0].read_text() == "magicsock: error sending\n"


async def test_help_and_settings_open_from_anywhere(tmp_path: Path) -> None:
    app = make_app(tmp_path)
    async with app.run_test(size=(120, 45)) as pilot:
        await settle(pilot)
        await pilot.press("a")
        assert type(app.screen).__name__ == "HelpScreen"
        await pilot.press("escape")
        await pilot.press("s")
        assert type(app.screen).__name__ == "SettingsScreen"


# ---- lot 2 : Survie ----



class HotMachine:
    def state(self, tailscaled_pid: int):  # type: ignore[no-untyped-def]
        from omega_tail.domain.machine import MachineState
        return MachineState(hostname="omega-server", cpu_count=4, temperature_c=70.0, tailscaled_cpu_percent=130.0)


def survival_app(tmp_path: Path, sim: FunnelSim, ran: list[tuple[str, ...]], *, hot: bool = False,
                 clock: list[float] | None = None, watch: WatchTools | None = None) -> OmegaTailApp:
    store = FileCutStore(tmp_path / "var")
    published = (Publication(443, True, PublishMode.HTTPS, "x", "http://localhost:80", "/"),)
    snapshots = tools(FakeTailscale(publications=published), FakeService(), False)
    snapshots = type(snapshots)(tailscale=snapshots.tailscale, service=snapshots.service,
                                machine=HotMachine() if hot else snapshots.machine, user=snapshots.user,
                                through_tailscale=snapshots.through_tailscale, now=snapshots.now, cut=store.current,
                                watch=watch.status if watch is not None else (lambda: None))
    survival = SurvivalTools(store=store, serve_config=sim.serve_config, quiet=sim.quiet, now=lambda: NOW,
                             python="/x/python", user=lambda: "kraynux")
    settings = SettingsTools(JsonSettingsStore(tmp_path / "settings.json"), tmp_path / "exports",
                             tmp_path / "shots", lambda d: clear_directory(d, tmp_path), tmp_path)
    ticks = clock if clock is not None else [0.0]
    return OmegaTailApp(snapshots=snapshots, journal=FakeJournal(),
                        actions=ActionTools(run=lambda argv: ran.append(tuple(argv)) or 0), version="0.2.0",
                        render_profile=RenderProfile.STANDARD, settings=settings, splash=False, refresh_seconds=0,
                        survival=survival, ssh_unit="sshd.service", clock=lambda: ticks[0], watch=watch)




async def test_survival_confinement_shows_the_commands_then_runs_them(tmp_path: Path) -> None:
    ran: list[tuple[str, ...]] = []
    app = survival_app(tmp_path, FunnelSim(MIXED), ran)
    async with app.run_test(size=(130, 50)) as pilot:
        await settle(pilot)
        app.open_key("survival")
        await settle(pilot)
        screen = app.screen
        assert isinstance(screen, SurvivalScreen)
        assert "CPUQuota=100%" in str(screen.query_one("#confinement-preview", Static).render())
        assert screen.query_one("#ssh-priority", Checkbox).value
        assert screen.query_one("#unconfine", Button).disabled  # rien de pose par omega-tail
        screen.query_one("#confine", Button).press()
        await pilot.pause()
        text = str(app.screen.query_one("#confirm-text", Static).render())
        assert "install -D -m 0644" in text and "sshd.service.d/50-omega-tail.conf" in text
        app.screen.query_one("#confirm", Button).press()
        await settle(pilot)
        assert [command[:3] for command in ran] == [("sudo", "install", "-D"), ("sudo", "install", "-D"),
                                                     ("sudo", "systemctl", "daemon-reload"),
                                                     ("sudo", "systemctl", "restart")]


async def test_manual_total_cut_and_restore_from_the_survival_screen(tmp_path: Path) -> None:
    sim = FunnelSim(MIXED)
    app = survival_app(tmp_path, sim, [])
    async with app.run_test(size=(130, 50)) as pilot:
        await settle(pilot)
        app.open_key("survival")
        await settle(pilot)
        app.screen.query_one("#cut-total", Button).press()
        await pilot.pause()
        app.screen.query_one("#confirm", Button).press()
        await settle(pilot)
        assert not any(handler.public for handler in handlers_of(sim.config))
        assert "COUPÉ" in str(app.screen.query_one("#breaker-state", Static).render())
        assert not app.screen.query_one("#restore", Button).disabled
        app.screen.query_one("#restore", Button).press()
        await settle(pilot)
        assert sim.config == MIXED


async def test_breaker_proposes_after_the_window_and_snoozes(tmp_path: Path) -> None:
    ticks = [0.0]
    app = survival_app(tmp_path, FunnelSim(MIXED), [], hot=True, clock=ticks)
    async with app.run_test(size=(130, 50)) as pilot:
        await settle(pilot)
        for second in range(5, 70, 5):
            ticks[0] = float(second)
            app.request_refresh()
            await settle(pilot)
        assert isinstance(app.screen, BreakerProposalScreen)
        assert "130" in str(app.screen.query_one("#proposal-text", Static).render())
        app.screen.query_one("#later", Button).press()
        await settle(pilot)
        ticks[0] = 80.0
        app.request_refresh()
        await settle(pilot)
        assert not isinstance(app.screen, BreakerProposalScreen)  # « Pas maintenant » : 15 min de silence


async def test_breaker_proposal_timed_cut_schedules_the_timer(tmp_path: Path) -> None:
    ticks = [0.0]
    ran: list[tuple[str, ...]] = []
    sim = FunnelSim(MIXED)
    app = survival_app(tmp_path, sim, ran, hot=True, clock=ticks)
    async with app.run_test(size=(130, 50)) as pilot:
        await settle(pilot)
        for second in range(5, 70, 5):
            ticks[0] = float(second)
            app.request_refresh()
            await settle(pilot)
        app.screen.query_one("#minutes", Button).press()
        await settle(pilot)
        assert ran and ran[0][:3] == ("sudo", "systemd-run", "--on-active=10min")
        assert not any(handler.public for handler in handlers_of(sim.config))


# ---- lot 4 : pare-feu Funnel ----
def gate_app(tmp_path: Path, sim: FunnelSim, admin: object | None = None) -> OmegaTailApp:
    from test_gate import FakeAdmin
    from test_gate import gate as make_gate

    from omega_tail.domain.tailscale import Publication as Pub

    tools_gate = make_gate(tmp_path, sim, admin=admin or FakeAdmin())  # type: ignore[arg-type]
    published = (Pub(443, True, PublishMode.HTTPS, "kraynux.tailnet-exemple.ts.net", "http://127.0.0.1:8080", "/"),)
    settings = SettingsTools(JsonSettingsStore(tmp_path / "settings.json"), tmp_path / "exports",
                             tmp_path / "shots", lambda d: clear_directory(d, tmp_path), tmp_path)
    return OmegaTailApp(snapshots=tools(FakeTailscale(publications=published)), journal=FakeJournal(),
                        actions=ActionTools(run=lambda argv: 0), version="0.3.0",
                        render_profile=RenderProfile.STANDARD, settings=settings, splash=False, refresh_seconds=0,
                        gate=tools_gate)


async def test_firewall_screen_states_and_hot_action(tmp_path: Path) -> None:
    from test_gate import PRODUCTION, FakeAdmin

    from omega_tail.interfaces.tui.screens.firewall import FirewallScreen

    admin = FakeAdmin()
    app = gate_app(tmp_path, FunnelSim(PRODUCTION), admin)
    async with app.run_test(size=(130, 50)) as pilot:
        await settle(pilot)
        app.open_key("firewall")
        await settle(pilot)
        screen = app.screen
        assert isinstance(screen, FirewallScreen)
        state = str(screen.query_one("#gate-state", Static).render())
        assert "Protection inactive" in state and "127.0.0.1:8080 : pris en charge" in state
        assert not screen.query_one("#activate", Button).disabled
        assert screen.query_one("#deactivate", Button).disabled
        assert not screen.query_one("#install", Button).parent.display  # HAProxy present : bouton et cadre caches
        screen.query_one("#address").value = "203.0.113.7"  # type: ignore[attr-defined]
        screen.query_one("#blacklist", Button).press()
        await settle(pilot)
        assert any(line.endswith("noire.lst 203.0.113.7") for line in admin.lines)
        assert "203.0.113.7" in str(screen.query_one("#lists", Static).render())


async def test_attacks_screen_lists_and_unblocks(tmp_path: Path) -> None:
    from test_gate import PRODUCTION, FakeAdmin

    from omega_tail.interfaces.tui.screens.attacks import AttacksScreen

    class TableAdmin(FakeAdmin):
        def command(self, line: str) -> str:
            if line.startswith("show table"):
                self.lines.append(line)
                return ("0x1: key=::ffff:37.67.116.15 use=0 exp=3599731 shard=0 gpc0=1 conn_rate(10000)=57\n"
                        "0x2: key=2001:db8::5 use=0 exp=3599893 shard=0 gpc0=0 conn_rate(10000)=1\n")
            return super().command(line)

    admin = TableAdmin()
    app = gate_app(tmp_path, FunnelSim(PRODUCTION), admin)
    async with app.run_test(size=(130, 50)) as pilot:
        await settle(pilot)
        app.open_key("attacks")
        await settle(pilot)
        await pilot.pause(0.3)
        screen = app.screen
        assert isinstance(screen, AttacksScreen)
        assert screen.query_one("#attacks-table", WideTable).row_count == 2
        state, expiry = screen.state_of(screen._rows[0], {})
        assert str(state) == "bloquée" and expiry == "59 min"
        assert "refusées avant chiffrement : 1" in str(screen.query_one("#counters", Static).render())
        screen.query_one("#unblock", Button).press()
        await settle(pilot)
        assert "set table porte_ip key 37.67.116.15 data.gpc0 0" in admin.lines
