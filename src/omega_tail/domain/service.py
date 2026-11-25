# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Le service `tailscaled` vu par systemd."""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


@dataclass(frozen=True)
class ServiceState:
    known: bool
    """systemd connait l'unite (False : pas de systemd, ou Tailscale pas installe comme service)."""
    active: str = ""
    """active, inactive, failed, activating, deactivating..."""
    sub: str = ""
    enabled: str = ""
    """enabled, disabled, static..."""
    since: str = ""
    main_pid: int = 0
    memory_bytes: int | None = None
    exec_start: str = ""
    fragment_path: str = ""
    drop_ins: tuple[str, ...] = ()
    cpu_quota: str = ""
    cpu_weight: str = ""
    allowed_cpus: str = ""
    nice: str = ""
    error: str = ""
    init: str = "systemd"
    """Systeme d'init qui gere le service (systemd, openrc, runit)."""
    name: str = ""
    """Nom du service pour ce systeme d'init (tailscaled.service, tailscale, tailscaled...)."""
    start_hooks: tuple[str, ...] = ()
    """Commandes ExecStartPre / ExecStartPost dont l'echec fait echouer le demarrage (sans « - »)."""
    confinement_lost: bool = False
    """Hors systemd : le groupe de controle d'omega-tail existe, mais tailscaled n'y est plus (redemarre depuis)."""

    @property
    def running(self) -> bool:
        return self.active == "active"

    @property
    def confined(self) -> bool:
        """Une limite CPU est posee (quota, poids ou coeurs autorises)."""
        quota = self.cpu_quota not in ("", "infinity")
        weight = self.cpu_weight not in ("", "[not set]", "100")
        return quota or weight or bool(self.allowed_cpus.strip())


class ServiceAction(str, Enum):
    START = "start"
    STOP = "stop"
    RESTART = "restart"
