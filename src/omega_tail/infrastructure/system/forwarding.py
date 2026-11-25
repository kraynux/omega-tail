# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Lecture du transfert IP dans /proc/sys (aucun droit particulier, aucune commande)."""
from __future__ import annotations

from pathlib import Path

from omega_tail.domain.forwarding import Forwarding

FILES = ("net/ipv4/ip_forward", "net/ipv6/conf/all/forwarding")


def _flag(path: Path) -> bool | None:
    try:
        return path.read_text().strip() == "1"
    except OSError:
        return None


def read_forwarding(root: Path = Path("/proc/sys")) -> Forwarding:
    ipv4, ipv6 = (_flag(root / name) for name in FILES)
    return Forwarding(ipv4, ipv6)
