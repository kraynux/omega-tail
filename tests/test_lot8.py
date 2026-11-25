# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Lot 8 : bouclier du port WireGuard (omega-lib D-018). Qui lance les commandes (omega-fire relie ou omega-tail),
reprise dans les deux sens, alertes, veille, ecran. La table elle-meme est essayee sur le vrai noyau dans omega-lib
(tests/test_shield.py) ; jamais de vraie commande root ici."""
from __future__ import annotations

from dataclasses import replace
from pathlib import Path

from conftest import NOW, FakeJournal, snapshot, tools
from omega_lib.shield.models import ShieldCounters, ShieldMode, ShieldSettings, ShieldSpec, ShieldStatus
from omega_lib.shield.policies import parse_settings
from omega_lib.shield.system import SCRIPT_PATH, SETTINGS_PATH
from omega_lib.terminal.models import RenderProfile
from textual.widgets import Button, DataTable, Static

from omega_tail.application.actions import ActionTools
from omega_tail.application.shield import Action, ShieldTools
from omega_tail.application.survival import SurvivalTools
from omega_tail.application.watch import Watcher
from omega_tail.domain.alerts import alerts_for
from omega_tail.domain.init import InitSystem
from omega_tail.domain.shield import OMEGA_FIRE, OMEGA_TAIL, FireLink, ShieldFacts, version_tuple
from omega_tail.infrastructure.shield import ShieldSystem
from omega_tail.infrastructure.survival_store import FileCutStore
from omega_tail.infrastructure.watch_store import FileWatchStore
from omega_tail.interfaces.shared.presentation import shield_summary
from omega_tail.interfaces.tui.app import OmegaTailApp

SPEC = ShieldSpec(41641, ("enp5s0", "wlan0"), ShieldMode.OBSERVE, OMEGA_TAIL)
FIRE = FireLink("/opt/omega-fire/omega-fire.sh", "3.7.0")
OLD_FIRE = FireLink("/opt/omega-fire/omega-fire.sh", "3.6.3")
NO_FIRE = FireLink()


class Machine(ShieldSystem):
    """Vraie preparation de fichiers (dossier de test), lectures de /etc et /run simulees."""

    def __init__(self, folder: Path, settings: ShieldSettings | None = None, present: bool = False,
                 fire: FireLink = NO_FIRE, port: int = 41641, modules: bool = True) -> None:
        super().__init__(folder)
        self._modules = modules
        self._settings, self._fire, self._port = settings, fire, port
        self._status = (ShieldStatus(True, 1000.0, settings.spec.mode, settings.spec.requested_by, 4,
                                     ShieldCounters(peer=90, other=12)) if settings is not None and present else None)

    def settings(self) -> ShieldSettings | None:
        return self._settings

    def status(self) -> ShieldStatus | None:
        return self._status

    def tailscaled_port(self) -> int:
        return self._port

    def devices(self) -> tuple[str, ...]:
        return ("enp5s0", "wlan0")

    def kernel_release(self) -> str:
        return "7.2.14-zen"

    def fire(self) -> FireLink:
        return self._fire

    def modules_ready(self) -> bool:
        return self._modules


def shield_tools(machine: Machine) -> ShieldTools:
    return ShieldTools(machine=machine, clock=lambda: 1010.0, init=InitSystem.SYSTEMD)


def test_versions_and_fire_link() -> None:
    assert version_tuple("3.7.0") == (3, 7, 0) and version_tuple("3.10") == (3, 10, 0) and version_tuple("x") == ()
    assert FIRE.ready and not OLD_FIRE.ready and not FireLink().linked


def test_without_omega_fire_omega_tail_poses_the_same_table(tmp_path: Path) -> None:
    machine = Machine(tmp_path / "bouclier-wg")
    tools_ = shield_tools(machine)
    assert tools_.view().actions == (Action.POSE,)
    plan = tools_.plan(Action.POSE)
    assert not plan.via_fire and not plan.refusal
    assert all(command[0] == "sudo" for command in plan.commands)
    assert ("sudo", SCRIPT_PATH, "installer") in plan.commands
    staged = (tmp_path / "bouclier-wg" / "reglages").read_text()
    settings = parse_settings(staged)
    assert settings is not None and (settings.manager, settings.spec.requested_by) == (OMEGA_TAIL, OMEGA_TAIL)
    assert settings.spec.mode is ShieldMode.OBSERVE and settings.spec.devices == ("enp5s0", "wlan0")
    assert oct((tmp_path / "bouclier-wg").stat().st_mode & 0o777) == "0o700"
    old = shield_tools(Machine(tmp_path / "b2", fire=OLD_FIRE))
    assert not old.plan(Action.POSE).via_fire   # omega-fire trop ancien : il prendrait la table pour une autre


def test_with_omega_fire_the_commands_go_through_it(tmp_path: Path) -> None:
    tools_ = shield_tools(Machine(tmp_path / "b", fire=FIRE))
    plan = tools_.plan(Action.POSE)
    assert plan.via_fire
    assert plan.commands == [("sudo", FIRE.launcher, "bouclier-wg", "poser", "--mode", "observation",
                              "--pour", OMEGA_TAIL, "--format", "json")]
    managed = shield_tools(Machine(tmp_path / "c", ShieldSettings(SPEC, OMEGA_FIRE), present=True, fire=FIRE))
    assert managed.view().actions == (Action.MODE, Action.REMOVE)
    assert managed.plan(Action.MODE, ShieldMode.ACTIVE).commands[0][3:5] == ("mode", "actif")


def test_hand_over_and_take_back(tmp_path: Path) -> None:
    ours = shield_tools(Machine(tmp_path / "a", ShieldSettings(SPEC, OMEGA_TAIL), present=True, fire=FIRE))
    assert Action.HAND_OVER in ours.view().actions
    assert ours.plan(Action.HAND_OVER).commands[0][2:4] == ("bouclier-wg", "reprendre")
    # omega-fire desinstalle apres avoir repris le bouclier : omega-tail propose de le reprendre
    orphan = shield_tools(Machine(tmp_path / "b", ShieldSettings(SPEC, OMEGA_FIRE), present=True))
    assert orphan.view().actions == (Action.TAKE_BACK, Action.REMOVE)
    plan = orphan.plan(Action.TAKE_BACK)
    assert plan.commands[-1] == ("sudo", SCRIPT_PATH, "etat")
    assert plan.commands[0][-1] == SETTINGS_PATH and ("sudo", SCRIPT_PATH, "poser") not in plan.commands
    taken = parse_settings((tmp_path / "b" / "reglages").read_text())
    assert taken is not None and taken.manager == OMEGA_TAIL and taken.spec.requested_by == OMEGA_TAIL


def test_mode_repose_remove_and_refusals(tmp_path: Path) -> None:
    machine = Machine(tmp_path / "a", ShieldSettings(SPEC, OMEGA_TAIL), present=True)
    tools_ = shield_tools(machine)
    plan = tools_.plan(Action.MODE, ShieldMode.ACTIVE)
    assert plan.commands[-1] == ("sudo", SCRIPT_PATH, "mode", "actif")
    assert "drop" in (tmp_path / "a" / "bouclier.nft").read_text().split("chain refus")[1]
    machine._status = ShieldStatus(False, 1000.0)
    assert tools_.view().actions == (Action.REPOSE, Action.REMOVE)
    assert tools_.plan(Action.REPOSE).commands == [("sudo", SCRIPT_PATH, "poser")]
    assert tools_.plan(Action.REMOVE).commands[0][:3] == ("sudo", "sh", "-c")
    assert shield_tools(Machine(tmp_path / "b", port=0)).plan(Action.POSE).refusal == "port-aleatoire"
    assert shield_tools(Machine(tmp_path / "c")).plan(Action.MODE).refusal == "absent"
    stale_kernel = shield_tools(Machine(tmp_path / "d", modules=False))   # serveur-web 2026-11-24
    assert stale_kernel.plan(Action.POSE).refusal == "redemarrage"
    assert stale_kernel.plan(Action.POSE).commands == []
    assert shield_tools(Machine(tmp_path / "e", fire=FIRE, modules=False)).plan(Action.POSE).refusal == "redemarrage"


def test_removed_from_omega_fire_is_said(tmp_path: Path) -> None:
    machine = Machine(tmp_path / "a")
    tools_ = shield_tools(machine)
    tools_.finished(Action.POSE, True)
    facts = tools_.facts()
    assert facts.removed_elsewhere
    assert "retiré depuis omega-fire" in shield_summary(facts)
    tools_.finished(Action.REMOVE, True)
    assert not tools_.facts().removed_elsewhere


def test_alerts_and_summary() -> None:
    settings = ShieldSettings(SPEC, OMEGA_TAIL)
    missing = ShieldFacts(settings, ShieldStatus(False, 1000.0), 1010.0)
    stale = ShieldFacts(settings, ShieldStatus(True, 1000.0, ShieldMode.OBSERVE), 1300.0)
    fine = ShieldFacts(settings, ShieldStatus(True, 1000.0, ShieldMode.OBSERVE, OMEGA_TAIL, 3,
                                              ShieldCounters(other=5)), 1010.0)
    codes = {alert.code for alert in alerts_for(replace(snapshot(), shield=missing), NOW)}
    assert "shield-missing" in codes
    assert "shield-stale" in {alert.code for alert in alerts_for(replace(snapshot(), shield=stale), NOW)}
    assert not {"shield-missing", "shield-stale"} & {alert.code for alert in
                                                     alerts_for(replace(snapshot(), shield=fine), NOW)}
    assert "5 paquet(s) auraient été refusés" in shield_summary(fine)


def test_watch_notes_a_missing_shield_once(tmp_path: Path) -> None:
    settings = ShieldSettings(SPEC, OMEGA_TAIL)
    states = [ShieldFacts(settings, ShieldStatus(True, 1000.0, ShieldMode.OBSERVE), 1010.0),
              ShieldFacts(settings, ShieldStatus(False, 1000.0), 1010.0),
              ShieldFacts(settings, ShieldStatus(False, 1000.0), 1010.0),
              ShieldFacts(settings, ShieldStatus(True, 1000.0, ShieldMode.OBSERVE), 1010.0)]
    store = FileWatchStore(tmp_path / "var")
    survival = SurvivalTools(store=FileCutStore(tmp_path / "var"), serve_config=lambda: {},
                             quiet=lambda argv: (0, ""), now=lambda: NOW, python="python3", user=lambda: "k")
    from omega_tail.domain.breaker import BreakerPolicy

    watcher = Watcher(store=store, survival=survival, measure=lambda: (1.0, 40.0), policy=BreakerPolicy,
                      window=lambda: 10, clock=lambda: 1000.0, shield=lambda: states.pop(0))
    for _round in range(4):
        watcher.tick()
    journal = store.last_lines(10)
    assert sum("ABSENT" in line for line in journal) == 1
    assert sum("de nouveau en place" in line for line in journal) == 1


async def test_shield_screen_and_survival_button(tmp_path: Path) -> None:
    from test_tui import settle

    from omega_tail.interfaces.tui.screens.confirm import ConfirmScreen
    from omega_tail.interfaces.tui.screens.shield import ShieldScreen

    machine = Machine(tmp_path / "bouclier-wg", ShieldSettings(SPEC, OMEGA_TAIL), present=True, fire=FIRE)
    ran: list[tuple[str, ...]] = []
    app = OmegaTailApp(snapshots=tools(), journal=FakeJournal(), actions=ActionTools(run=lambda argv: ran.append(
        tuple(argv)) or 0), version="0.7.0", render_profile=RenderProfile.STANDARD, splash=False, refresh_seconds=0,
        shield=shield_tools(machine))  # type: ignore[arg-type]
    async with app.run_test(size=(130, 50)) as pilot:
        await settle(pilot)
        app.open_key("survival")
        await settle(pilot)
        app.screen.query_one("#open-shield", Button).press()
        await settle(pilot)
        screen = app.screen
        assert isinstance(screen, ShieldScreen)
        state = str(screen.query_one("#shield-state", Static).render())
        assert "géré par omega-tail" in state and "omega-fire 3.7.0 relié" in state
        assert screen.query_one("#shield-counters", DataTable).row_count == 7
        shown = {action: screen.query_one(f"#frame-{action.value}").display for action in Action}
        assert shown == {Action.POSE: False, Action.MODE: True, Action.REPOSE: False, Action.HAND_OVER: True,
                         Action.TAKE_BACK: False, Action.REMOVE: True}
        screen.query_one("#shield-confier", Button).press()
        await settle(pilot)
        assert isinstance(app.screen, ConfirmScreen)
        assert "bouclier-wg reprendre" in str(app.screen.query_one("#confirm-text", Static).render())
        app.screen.query_one("#confirm", Button).press()
        await settle(pilot)
        assert ran == [("sudo", FIRE.launcher, "bouclier-wg", "reprendre", "--pour", OMEGA_TAIL, "--format", "json")]
