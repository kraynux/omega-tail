# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Connexion et reglages (lot 5, proposition §3.3) : se connecter, se deconnecter, changer de compte, deconnexion
definitive, et les preferences de `tailscale set`.

Ces commandes passent par le vrai terminal (adresse de connexion a ouvrir, questions de Tailscale, mot de passe
sudo) : sans sudo pour l'operateur de Tailscale, avec sudo sinon. Changer l'operateur demande toujours sudo."""
from __future__ import annotations

import re
from collections.abc import Callable, Mapping
from dataclasses import dataclass

from omega_tail.core.constants import TAILSCALE_COMMAND
from omega_tail.domain.forwarding import Forwarding, enable_script
from omega_tail.domain.preferences import Change, changes, needs_root, problems, set_command
from omega_tail.domain.tailscale import ExitNode, Profile

PROFILE_ID = re.compile(r"^[A-Za-z0-9_-]{1,64}$")


@dataclass(frozen=True)
class SettingsPlan:
    changes: tuple[Change, ...]
    problems: Mapping[str, str]
    command: tuple[str, ...]
    """Vide quand il n'y a rien a appliquer ou qu'une valeur est refusee."""

    @property
    def cuts_session(self) -> tuple[Change, ...]:
        return tuple(change for change in self.changes if change.cuts_session)


@dataclass(frozen=True)
class ConnectionTools:
    profiles: Callable[[], tuple[tuple[Profile, ...], str]]
    exit_nodes: Callable[[], tuple[ExitNode, ...]]
    as_root: bool = False
    forwarding: Callable[[], Forwarding] = Forwarding

    def _command(self, *args: str, operator: bool, root: bool = False) -> tuple[str, ...]:
        command = (TAILSCALE_COMMAND, *args)
        return ("sudo", *command) if not self.as_root and (root or not operator) else command

    def up(self, *, operator: bool) -> tuple[str, ...]:
        return self._command("up", operator=operator)

    def down(self, *, operator: bool) -> tuple[str, ...]:
        return self._command("down", operator=operator)

    def login(self, *, operator: bool) -> tuple[str, ...]:
        """Ajoute un compte (nouveau profil) : Tailscale affiche l'adresse a ouvrir pour s'identifier."""
        return self._command("login", operator=operator)

    def logout(self, *, operator: bool) -> tuple[str, ...]:
        return self._command("logout", operator=operator)

    def switch(self, profile_id: str, *, operator: bool) -> tuple[str, ...]:
        if not PROFILE_ID.match(profile_id):
            raise ValueError("profile id")
        return self._command("switch", profile_id, operator=operator)

    def plan(self, current: Mapping[str, str], wanted: Mapping[str, str], *, operator: bool) -> SettingsPlan:
        refused = problems(wanted)
        found = changes(current, {name: value for name, value in wanted.items() if name not in refused})
        if refused or not found:
            return SettingsPlan(found, refused, ())
        sudo = not self.as_root and (not operator or needs_root(found))
        return SettingsPlan(found, refused, set_command(found, sudo=sudo))

    def enable_forwarding(self) -> tuple[str, ...]:
        """Ecrire dans /etc/sysctl.d demande toujours root."""
        script = enable_script()
        return script if self.as_root else ("sudo", *script)
