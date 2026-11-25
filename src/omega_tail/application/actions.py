# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Actions qui changent la machine (lot 1 : service tailscaled, droit d'operateur). Chacune est une commande
complete, montree avant d'etre lancee, et lancee dans le vrai terminal (mot de passe sudo saisi par l'utilisateur,
jamais garde)."""
from __future__ import annotations

from collections.abc import Callable, Sequence
from dataclasses import dataclass

from omega_tail.core.constants import TAILSCALE_COMMAND, TAILSCALED_UNIT
from omega_tail.domain.init import InitSystem
from omega_tail.domain.service import ServiceAction

TerminalCommand = Callable[[Sequence[str]], int]
"""Lance une commande sur le vrai terminal (invite sudo comprise) ; renvoie son code de sortie."""


def service_command(action: ServiceAction, *, as_root: bool = False, init: InitSystem = InitSystem.SYSTEMD,
                    name: str = "") -> tuple[str, ...]:
    """systemd : systemctl ; OpenRC : rc-service ; runit : sv (meme regle que les gestionnaires d'omega-serv)."""
    if init is InitSystem.OPENRC:
        command: tuple[str, ...] = ("rc-service", name or "tailscale", action.value)
    elif init is InitSystem.RUNIT:
        verb = {ServiceAction.START: "up", ServiceAction.STOP: "down", ServiceAction.RESTART: "restart"}[action]
        command = ("sv", verb, name or "tailscaled")
    else:
        command = ("systemctl", action.value, name or TAILSCALED_UNIT)
    return command if as_root else ("sudo", *command)


def operator_command(user: str, *, as_root: bool = False) -> tuple[str, ...]:
    command = (TAILSCALE_COMMAND, "set", f"--operator={user}")
    return command if as_root else ("sudo", *command)


@dataclass(frozen=True)
class ActionTools:
    run: TerminalCommand
    as_root: bool = False

    def service(self, action: ServiceAction, *, init: InitSystem = InitSystem.SYSTEMD,
                name: str = "") -> tuple[tuple[str, ...], int]:
        command = service_command(action, as_root=self.as_root, init=init, name=name)
        return command, self.run(command)

    def become_operator(self, user: str) -> tuple[tuple[str, ...], int]:
        command = operator_command(user, as_root=self.as_root)
        return command, self.run(command)
