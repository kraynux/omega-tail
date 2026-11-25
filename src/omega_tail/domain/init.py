# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Systemes d'init pris en charge par la suite omega : systemd, OpenRC, runit (regle de la suite, rappel du
2026-11-23). Noms des services selon le systeme et la distribution."""
from __future__ import annotations

from enum import Enum


class InitSystem(str, Enum):
    SYSTEMD = "systemd"
    OPENRC = "openrc"
    RUNIT = "runit"
    NONE = "none"


TAILSCALED_NAMES: dict[InitSystem, tuple[str, ...]] = {
    InitSystem.SYSTEMD: ("tailscaled.service",),
    InitSystem.OPENRC: ("tailscale", "tailscaled"),   # Alpine : /etc/init.d/tailscale
    InitSystem.RUNIT: ("tailscaled", "tailscale"),    # Void : /etc/sv/tailscaled
    InitSystem.NONE: ("tailscaled",),
}
GATE_NAMES: dict[InitSystem, str] = {
    InitSystem.SYSTEMD: "omega-tail-porte.service",
    InitSystem.OPENRC: "omega-tail-porte",
    InitSystem.RUNIT: "omega-tail-porte",
    InitSystem.NONE: "omega-tail-porte",
}
CGROUP_NAME = "omega-tail-tailscaled"
"""Groupe de controle (cgroup v2) du confinement hors systemd."""
CGROUP_ROOT = "/sys/fs/cgroup"
