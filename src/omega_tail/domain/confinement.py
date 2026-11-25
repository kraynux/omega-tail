# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Confinement de tailscaled (proposition §6.1) : un fichier d'ajout systemd SEPARE, a nous
(`tailscaled.service.d/50-omega-tail.conf`), jamais l'`override.conf` deja present sur la machine.
Sous attaque, tailscaled ne prend jamais plus que son plafond : la machine et l'administration restent utilisables.

Pas de coeurs reserves (AllowedCPUs) par defaut : le plafond suffit et laisse tailscaled repartir son travail."""
from __future__ import annotations

from dataclasses import dataclass

DROP_IN_DIR = "/etc/systemd/system/tailscaled.service.d"
DROP_IN_NAME = "50-omega-tail.conf"
DROP_IN_PATH = f"{DROP_IN_DIR}/{DROP_IN_NAME}"
SSH_UNITS = ("sshd.service", "ssh.service")
"""Nom du service SSH selon la distribution (Arch : sshd, Debian / Ubuntu : ssh)."""
SSH_WEIGHT = 200


@dataclass(frozen=True)
class ConfinementPlan:
    quota_percent: int
    """Plafond en % d'UN coeur (100 % = un coeur entier)."""
    cpu_weight: int = 50
    io_weight: int = 50
    nice: int = 5


def recommended(cpu_count: int) -> ConfinementPlan:
    """Un quart des fils de la machine, au moins la moitie d'un coeur : 2 fils -> 50 %, 4 -> 100 %, 8 -> 200 %."""
    return ConfinementPlan(quota_percent=max(50, (max(cpu_count, 1) // 4) * 100))


def drop_in_text(plan: ConfinementPlan) -> str:
    return (
        "# omega-tail - confinement de tailscaled (Survie). Fichier gere par omega-tail :\n"
        "# « Retirer le confinement » le supprime. Votre propre override.conf n'est jamais modifie.\n"
        f"# Sous attaque, tailscaled ne prend jamais plus de {plan.quota_percent} % d'un coeur.\n"
        "[Service]\n"
        f"CPUQuota={plan.quota_percent}%\n"
        f"CPUWeight={plan.cpu_weight}\n"
        f"IOWeight={plan.io_weight}\n"
        f"Nice={plan.nice}\n")


def ssh_drop_in_path(unit: str) -> str:
    return f"/etc/systemd/system/{unit}.d/{DROP_IN_NAME}"


def ssh_drop_in_text() -> str:
    return ("# omega-tail - priorite de l'acces SSH sous attaque (Survie). « Retirer le confinement » le supprime.\n"
            "[Service]\n"
            f"CPUWeight={SSH_WEIGHT}\n")
