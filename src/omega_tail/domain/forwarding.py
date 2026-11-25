# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Transfert IP (lot 5) : un noeud de sortie ou un routeur de sous-reseaux ne transmet rien tant que le noyau ne
fait pas suivre les paquets. omega-tail ecrit un fichier sysctl A PART (jamais /etc/sysctl.conf de l'utilisateur),
relu au demarrage par systemd-sysctl, le service sysctl d'OpenRC et les core-services de runit."""
from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

SYSCTL_PATH = "/etc/sysctl.d/99-omega-tail-forwarding.conf"
KEYS = ("net.ipv4.ip_forward", "net.ipv6.conf.all.forwarding")


@dataclass(frozen=True)
class Forwarding:
    """None : valeur illisible (pas d'IPv6, /proc absent)."""
    ipv4: bool | None = None
    ipv6: bool | None = None

    @property
    def missing(self) -> tuple[str, ...]:
        return tuple(key for key, on in zip(KEYS, (self.ipv4, self.ipv6), strict=True) if on is False)


def needs_forwarding(prefs: Mapping[str, str]) -> bool:
    """Vrai quand la machine se propose comme noeud de sortie ou annonce des sous-reseaux."""
    return prefs.get("advertise-exit-node") == "true" or bool(prefs.get("advertise-routes", "").strip())


def enable_script() -> tuple[str, ...]:
    """Texte fixe (aucune valeur de l'utilisateur) : ecrit le fichier puis l'applique tout de suite."""
    lines = " ".join(f"'{key} = 1'" for key in KEYS)
    return ("sh", "-c", f"mkdir -p /etc/sysctl.d && printf '%s\\n' {lines} > {SYSCTL_PATH} "
                        f"&& sysctl -p {SYSCTL_PATH}")
