# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Bouclier du port WireGuard (lot 8, omega-lib D-018) : ce qu'omega-tail en sait et qui le pilote.

Decisions (2026-11-23) : la regle va dans omega-fire s'il est relie par omega-connect (il en voit
l'origine et la pilote depuis sa liste des regles) ; sinon omega-tail pose LA MEME table lui-meme, meme si ufw ou
firewalld sont la ; observation d'abord ; reprise par un bouton des deux cotes ; retrait possible depuis
omega-fire ; table effacee par un autre outil : alerte, jamais reposee seule."""
from __future__ import annotations

import re
from dataclasses import dataclass

from omega_lib.shield.models import ShieldMode, ShieldSettings, ShieldStatus

OMEGA_TAIL = "omega-tail"
OMEGA_FIRE = "omega-fire"
FIRE_MIN_VERSION = (3, 7, 0)
"""Premier omega-fire qui connait le bouclier (plus ancien : il le prendrait pour la table d'un autre outil)."""


def version_tuple(text: str) -> tuple[int, ...]:
    found = re.match(r"^\s*(\d+)\.(\d+)(?:\.(\d+))?", text or "")
    if found is None:
        return ()
    return tuple(int(part or 0) for part in found.groups())


@dataclass(frozen=True)
class FireLink:
    """omega-fire relie par omega-connect (registre de l'espace partage actif), comme pour omega-stress."""
    launcher: str = ""
    version: str = ""

    @property
    def linked(self) -> bool:
        return bool(self.launcher)

    @property
    def ready(self) -> bool:
        return self.linked and version_tuple(self.version) >= FIRE_MIN_VERSION


@dataclass(frozen=True)
class ShieldFacts:
    """Etat du bouclier pour la bande d'etat, les alertes, la veille et le rapport."""
    settings: ShieldSettings | None
    status: ShieldStatus | None
    now: float
    requested: bool = False
    """omega-tail a pose (ou fait poser) un bouclier et ne l'a pas retire lui-meme."""

    @property
    def installed(self) -> bool:
        return self.settings is not None

    @property
    def present(self) -> bool:
        return self.status is not None and self.status.present

    @property
    def stale(self) -> bool:
        return self.installed and (self.status is None or self.status.stale(self.now))

    @property
    def missing(self) -> bool:
        """Enregistre mais plus dans le noyau : un autre outil a efface la table."""
        return self.installed and self.status is not None and not self.status.present

    @property
    def removed_elsewhere(self) -> bool:
        """Demande par omega-tail, retire ailleurs (omega-fire ou a la main) : decision B du lot 8."""
        return self.requested and not self.installed and not self.present

    @property
    def mode(self) -> ShieldMode | None:
        if self.status is not None and self.status.present and self.status.mode is not None:
            return self.status.mode
        return self.settings.spec.mode if self.settings is not None else None

    @property
    def requested_by(self) -> str:
        if self.settings is not None:
            return self.settings.spec.requested_by
        return self.status.requested_by if self.status is not None else ""

    @property
    def manager(self) -> str:
        return self.settings.manager if self.settings is not None else ""

    @property
    def refused(self) -> int:
        return self.status.counters.refused if self.status is not None and self.status.present else 0
