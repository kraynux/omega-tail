# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Veille automatique : paliers 15 / 30 / 60 min (renouvelable), fenetre de 10 min, retour a zero apres 24 h,
remise en route par la veille elle-meme, services systemd / OpenRC / runit sous le compte de l'utilisateur."""
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from conftest import snapshot
from funnel_sim import FunnelSim
from test_survival import MIXED

from omega_tail.application.survival import SurvivalTools
from omega_tail.application.watch import Watcher, WatchTools
from omega_tail.domain.alerts import Target, alerts_for
from omega_tail.domain.breaker import BreakerPolicy
from omega_tail.domain.funnel import handlers_of
from omega_tail.domain.init import InitSystem
from omega_tail.domain.publication import backup_from
from omega_tail.domain.watch import (
    CALM_SECONDS,
    WatchState,
    WatchStatus,
    can_strike,
    on_strike,
    status_of,
)
from omega_tail.infrastructure.survival_store import FileCutStore
from omega_tail.infrastructure.watch_store import FileWatchStore

START = datetime(2026, 11, 23, 12, 0, tzinfo=timezone.utc).timestamp()
POLICY = BreakerPolicy(cpu_percent=80, seconds=60, temperature_c=85, minutes=10)


def test_three_strikes_in_the_window_cut_by_steps_then_reset_after_a_day() -> None:
    state, now, cuts = WatchState(), START, []
    for _round in range(4):
        for _strike in range(3):
            now += 70
            state, minutes = on_strike(state, now, 10)
        cuts.append(minutes)
        now += minutes * 60  # coupure finie
    assert cuts == [15, 30, 60, 60]  # 1 h renouvelable
    state, minutes = on_strike(state, now + 24 * 3600 + 1, 10)  # 24 h sans coupure : premier palier
    assert minutes is None and state.level == 0
    spread = WatchState()
    for step in range(3):  # trois depassements etales sur plus de 10 min : jamais trois dans la fenetre
        spread, minutes = on_strike(spread, START + step * 400, 10)
    assert minutes is None and len(spread.strikes) == 2
    assert not can_strike(WatchState(strikes=(START,)), START + 30, 60) and can_strike(WatchState(), START, 60)


class Clock:
    def __init__(self) -> None:
        self.now = START

    def __call__(self) -> float:
        return self.now


def watcher(tmp_path: Path, sim: FunnelSim, clock: Clock, cpu: list[float]) -> Watcher:
    survival = SurvivalTools(store=FileCutStore(tmp_path / "var"), serve_config=sim.serve_config, quiet=sim.quiet,
                             now=lambda: datetime.fromtimestamp(clock.now, tz=timezone.utc),
                             python="/opt/omega-tail/.venv/bin/python", user=lambda: "kraynux")
    return Watcher(store=FileWatchStore(tmp_path / "var"), survival=survival, measure=lambda: (cpu[0], 50.0),
                   policy=lambda: POLICY, window=lambda: 10, clock=clock)


def run(watch: Watcher, clock: Clock, seconds: float) -> None:
    end = clock.now + seconds
    while clock.now < end:
        clock.now += 5
        watch.tick()


def test_watcher_cuts_alone_restores_alone_and_climbs_the_steps(tmp_path: Path) -> None:
    sim, clock, cpu = FunnelSim(MIXED), Clock(), [5.0]
    watch = watcher(tmp_path, sim, clock, cpu)
    run(watch, clock, 120)
    assert watch.survival.store.current() is None  # au repos : rien
    cpu[0] = 150.0  # attaque continue
    run(watch, clock, 200)
    cut = watch.survival.store.current()
    assert cut is not None and cut.cut_id.startswith("veille-") and cut.until  # 3 depassements : coupure
    assert not any(handler.public for handler in handlers_of(sim.config))
    assert backup_from(cut.saved, ()).origin == "veille automatique"
    run(watch, clock, 14 * 60)
    assert watch.survival.store.current() is not None  # 15 min pas encore passees
    run(watch, clock, 90)
    assert watch.survival.store.current() is None and sim.config == MIXED  # remis seul, a l'identique
    state = watch.store.load()
    assert state.level == 1 and state.calm_until > clock.now - 10 and state.heartbeat
    run(watch, clock, CALM_SECONDS + 200)  # l'attaque reprend apres le calme : 30 min cette fois
    cut = watch.survival.store.current()
    assert cut is not None
    assert round((datetime.fromisoformat(cut.until).timestamp() - datetime.fromisoformat(cut.cut_at).timestamp())
                 / 60) == 30
    journal = "\n".join(watch.store.last_lines(50))
    assert "dépassement 1/3" in journal and "Funnel coupé 15 min" in journal and "Funnel coupé 30 min" in journal
    assert "remis en route" in journal


def test_watcher_restores_a_cut_due_after_its_own_restart(tmp_path: Path) -> None:
    """Service relance pendant une coupure : la remise en route due est faite aussitot."""
    sim, clock = FunnelSim(MIXED), Clock()
    first = watcher(tmp_path, sim, clock, [150.0])
    run(first, clock, 200)
    assert first.survival.store.current() is not None
    clock.now += 16 * 60
    second = watcher(tmp_path, sim, clock, [5.0])
    second.tick()
    assert second.survival.store.current() is None and sim.config == MIXED


def test_nothing_to_cut_keeps_the_step(tmp_path: Path) -> None:
    sim, clock = FunnelSim({"TCP": {"3389": {"TCPForward": "localhost:3389"}}}), Clock()
    watch = watcher(tmp_path, sim, clock, [150.0])
    run(watch, clock, 200)
    assert watch.survival.store.current() is None and watch.store.load().level == 0
    assert "coupure impossible" in "\n".join(watch.store.last_lines(10))


def test_services_run_under_the_user_for_each_init(tmp_path: Path) -> None:
    def tools(init: InitSystem) -> WatchTools:
        return WatchTools(store=FileWatchStore(tmp_path / init.value), window=lambda: 10, clock=lambda: START,
                          python="/home/k/omega-tail/.venv/bin/python", user=lambda: "kraynux", init=init)
    systemd = tools(InitSystem.SYSTEMD).start_commands()
    unit = Path(systemd[0][4]).read_text()
    assert "User=kraynux" in unit and "-m omega_tail veille lancer" in unit and "Restart=always" in unit
    assert systemd[-2] == ("sudo", "systemctl", "enable", "--now", "omega-tail-veille.service")
    openrc = tools(InitSystem.OPENRC).start_commands()
    assert 'command_user="kraynux"' in Path(openrc[0][4]).read_text()
    assert openrc[1] == ("sudo", "rc-update", "add", "omega-tail-veille", "default")
    runit = tools(InitSystem.RUNIT).start_commands()
    assert "chpst -u kraynux" in Path(runit[0][5]).read_text()
    assert runit[-1] == ("sudo", "ln", "-sfn", "/etc/sv/omega-tail-veille", "/var/service/omega-tail-veille")
    assert tools(InitSystem.SYSTEMD).stop_commands() == [
        ("sudo", "systemctl", "disable", "--now", "omega-tail-veille.service")]
    marked = tools(InitSystem.SYSTEMD)
    marked.mark_installed(True)
    assert marked.status().installed and not marked.status().alive  # active mais pas encore de signe de vie


def test_a_stopped_watch_is_signalled() -> None:
    assert status_of(WatchState(installed=True, heartbeat=START), START + 60, 10).alive
    assert not status_of(WatchState(installed=True, heartbeat=START), START + 200, 10).alive
    stopped = snapshot(watch=WatchStatus(installed=True, alive=False, level=0, strikes=0, next_minutes=15))
    found = [alert for alert in alerts_for(stopped, stopped.taken_at) if alert.code == "watch-stopped"]
    assert found and found[0].target is Target.SURVIVAL
    running = snapshot(watch=WatchStatus(installed=True, alive=True, level=0, strikes=0, next_minutes=15))
    assert not [alert for alert in alerts_for(running, running.taken_at) if alert.code == "watch-stopped"]


async def test_survival_screen_turns_the_watch_on(tmp_path: Path) -> None:
    from test_tui import settle, survival_app
    from textual.widgets import Button, Static

    from omega_tail.interfaces.tui.screens.survival import SurvivalScreen

    ran: list[tuple[str, ...]] = []
    tools = WatchTools(store=FileWatchStore(tmp_path / "var"), window=lambda: 10, clock=lambda: START,
                       python="/x/python", user=lambda: "kraynux")
    app = survival_app(tmp_path, FunnelSim(MIXED), ran, watch=tools)
    async with app.run_test(size=(130, 60)) as pilot:
        await settle(pilot)
        app.open_key("survival")
        await settle(pilot)
        screen = app.screen
        assert isinstance(screen, SurvivalScreen)
        assert "Désactivée" in str(screen.query_one("#watch-state", Static).render())
        assert not screen.query_one("#watch-off", Button).parent.display
        screen.query_one("#watch-on", Button).press()
        await pilot.pause()
        text = str(app.screen.query_one("#confirm-text", Static).render())
        assert "15 min, 30 min, puis 1 h" in text and "systemctl enable --now omega-tail-veille.service" in text
        app.screen.query_one("#confirm", Button).press()
        await settle(pilot)
        assert ("sudo", "systemctl", "enable", "--now", "omega-tail-veille.service") in ran
        assert tools.status().installed and "veille activée" in tools.journal()[-1]
