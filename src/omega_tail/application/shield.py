# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Bouclier du port WireGuard (lot 8) : quoi montrer, et quelles commandes lancer dans le terminal sudo.

Qui lance les commandes :
- omega-fire 3.7.0 ou plus recent, relie par omega-connect, et le bouclier absent ou gere par omega-fire :
  `omega-fire.sh bouclier-wg ... --pour omega-tail` (omega-fire en devient le gestionnaire, l'origine reste
  omega-tail) ;
- sinon omega-tail lance lui-meme les commandes d'omega-lib (meme table, memes fichiers, meme service).
« Confier a omega-fire » passe la gestion a omega-fire ; si omega-fire n'est plus relie, « Reprendre la gestion »
la rend a omega-tail. Dans les deux cas la table en service n'est pas touchee."""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, replace
from enum import Enum

from omega_lib.shield.models import ShieldMode, ShieldSettings, ShieldSpec
from omega_lib.shield.policies import kernel_supports_egress, validate
from omega_lib.shield.system import (
    install_commands,
    manager_commands,
    mode_commands,
    remove_commands,
    repose_commands,
    staged_files,
    with_sudo,
)

from omega_tail.domain.init import InitSystem
from omega_tail.domain.shield import OMEGA_FIRE, OMEGA_TAIL, FireLink, ShieldFacts
from omega_tail.ports.shield import ShieldMachine

Command = tuple[str, ...]


class Action(str, Enum):
    POSE = "poser"
    MODE = "mode"
    HAND_OVER = "confier"
    """Confier a omega-fire (omega-fire `reprendre`)."""
    TAKE_BACK = "reprendre"
    """omega-tail reprend la gestion (omega-fire n'est plus relie)."""
    REPOSE = "reposer"
    REMOVE = "retirer"


@dataclass(frozen=True)
class ShieldView:
    facts: ShieldFacts
    port: int
    devices: tuple[str, ...]
    egress: bool
    fire: FireLink
    init: InitSystem
    modules_ready: bool = True
    """Faux : noyau mis a jour sans redemarrage, la table serait refusee (redemarrer d'abord)."""

    @property
    def fire_handles(self) -> bool:
        """Les commandes passent par omega-fire."""
        facts = self.facts
        return self.fire.ready and (not facts.installed or facts.manager == OMEGA_FIRE)

    @property
    def actions(self) -> tuple[Action, ...]:
        facts = self.facts
        if not facts.installed:
            return (Action.REMOVE,) if facts.present else (Action.POSE,)
        if facts.manager == OMEGA_FIRE and not self.fire.ready:
            return Action.TAKE_BACK, Action.REMOVE
        found: list[Action] = []
        if facts.present:
            found.append(Action.MODE)
        if facts.missing:
            found.append(Action.REPOSE)
        if facts.manager != OMEGA_FIRE and self.fire.ready:
            found.append(Action.HAND_OVER)
        found.append(Action.REMOVE)
        return tuple(found)


@dataclass(frozen=True)
class ShieldPlan:
    action: Action
    commands: list[Command]
    via_fire: bool
    refusal: str = ""
    """Raison de ne rien lancer (port-aleatoire, aucune-carte, invalide, absent) ; vide : commandes pretes."""


@dataclass(frozen=True)
class ShieldTools:
    machine: ShieldMachine
    clock: Callable[[], float]
    init: InitSystem = InitSystem.SYSTEMD
    runit_dir: str = "/var/service"
    as_root: bool = False

    def facts(self) -> ShieldFacts:
        machine = self.machine
        return ShieldFacts(machine.settings(), machine.status(), self.clock(), machine.requested())

    def view(self) -> ShieldView:
        machine = self.machine
        return ShieldView(self.facts(), machine.tailscaled_port(), machine.devices(),
                          kernel_supports_egress(machine.kernel_release()), machine.fire(), self.init,
                          machine.modules_ready())

    def _sudo(self, commands: list[Command]) -> list[Command]:
        return commands if self.as_root else with_sudo(commands)

    def _fire(self, view: ShieldView, *arguments: str) -> list[Command]:
        command = (view.fire.launcher, "bouclier-wg", *arguments, "--pour", OMEGA_TAIL, "--format", "json")
        return [command if self.as_root else ("sudo", *command)]

    def _own(self, settings: ShieldSettings, commands: Callable[[str], list[Command]]) -> list[Command]:
        staging = self.machine.stage(staged_files(settings, self.init.value))
        return self._sudo(commands(staging))

    def plan(self, action: Action, mode: ShieldMode | None = None) -> ShieldPlan:
        view = self.view()
        settings = self.machine.settings()
        if action is Action.HAND_OVER:
            return ShieldPlan(action, self._fire(view, "reprendre"), True)
        if action in (Action.POSE, Action.REPOSE) and not view.modules_ready:
            return ShieldPlan(action, [], view.fire_handles, "redemarrage")
        if view.fire_handles and action is not Action.TAKE_BACK:
            arguments = {Action.POSE: ("poser", "--mode", ShieldMode.OBSERVE.value),
                         Action.MODE: ("mode", (mode or ShieldMode.OBSERVE).value),
                         Action.REPOSE: ("reposer",), Action.REMOVE: ("retirer",)}[action]
            return ShieldPlan(action, self._fire(view, *arguments), True)
        if action is Action.POSE:
            if view.port == 0:
                return ShieldPlan(action, [], False, "port-aleatoire")
            if not view.devices:
                return ShieldPlan(action, [], False, "aucune-carte")
            try:
                spec = validate(ShieldSpec(view.port, view.devices, ShieldMode.OBSERVE, OMEGA_TAIL,
                                           egress=view.egress))
            except ValueError:
                return ShieldPlan(action, [], False, "invalide")
            return ShieldPlan(action, self._own(ShieldSettings(spec, OMEGA_TAIL), lambda staging: install_commands(
                staging, self.init.value, self.runit_dir)), False)
        if action is Action.REMOVE:
            return ShieldPlan(action, self._sudo(remove_commands(self.init.value, self.runit_dir)), False)
        if settings is None:
            return ShieldPlan(action, [], False, "absent")
        if action is Action.REPOSE:
            return ShieldPlan(action, self._sudo(repose_commands()), False)
        if action is Action.TAKE_BACK:
            return ShieldPlan(action, self._own(ShieldSettings(settings.spec, OMEGA_TAIL), manager_commands), False)
        chosen = mode or ShieldMode.OBSERVE
        updated = ShieldSettings(replace(settings.spec, mode=chosen), OMEGA_TAIL)
        return ShieldPlan(action, self._own(updated, lambda staging: mode_commands(staging, chosen)), False)

    def finished(self, action: Action, ok: bool) -> None:
        """Note locale : omega-tail a demande un bouclier (pour dire « retire depuis omega-fire » ensuite)."""
        if ok and action is Action.POSE:
            self.machine.set_requested(True)
        elif ok and action is Action.REMOVE:
            self.machine.set_requested(False)
