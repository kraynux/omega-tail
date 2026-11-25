# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Base AS / pays des regroupements (lot 6) : ce que l'application demande a la machine."""
from __future__ import annotations

from collections.abc import Mapping
from datetime import date
from pathlib import Path
from typing import Protocol


class GeoSource(Protocol):
    def refresh(self, folder: Path, today: date) -> tuple[int, int]:
        """Telecharge la base du mois et ecrit geo.bin + noms d'AS dans `folder` ; renvoie (plages pays, plages AS).
        Leve OSError en cas d'echec (l'ancienne base reste alors en place)."""
        ...

    def lookup(self, folder: Path, address: str) -> tuple[str, int]:
        """(pays, AS) d'une adresse ; (« -- », 0) si inconnue."""
        ...

    def names(self, folder: Path) -> Mapping[int, str]:
        ...
