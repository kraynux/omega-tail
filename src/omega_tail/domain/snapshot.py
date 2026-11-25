# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Une lecture complete de la machine (tableau de bord, bande d'etat, `omega-tail etat`)."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from omega_tail.domain.funnel import Cut
from omega_tail.domain.machine import MachineState
from omega_tail.domain.service import ServiceState
from omega_tail.domain.shield import ShieldFacts
from omega_tail.domain.tailscale import Preferences, Publication, TailscaleState
from omega_tail.domain.watch import WatchStatus


@dataclass(frozen=True)
class Snapshot:
    taken_at: datetime
    tailscale: TailscaleState
    preferences: Preferences
    publications: tuple[Publication, ...]
    service: ServiceState
    machine: MachineState
    user: str
    """Compte qui lance omega-tail."""
    through_tailscale: bool
    """La session en cours passe par Tailscale (garde-fou « branche sciee »)."""
    cut: Cut | None = None
    """Coupure de Funnel posee par omega-tail (disjoncteur), s'il y en a une."""
    gate_service: ServiceState | None = None
    """Service de la porte (pare-feu Funnel), s'il est connu de systemd."""
    watch: WatchStatus | None = None
    """Veille automatique (Survie) : activee, en marche, palier."""
    gate_attack: bool = False
    """La porte est en mode attaque (regroupements, lot 6)."""
    shield: ShieldFacts | None = None
    """Bouclier du port WireGuard (lot 8)."""
    blacklist_count: int = 0
    """Entrees de la liste noire de la porte (alerte a 25 000, plafond 50 000)."""

    @property
    def gated(self) -> tuple[Publication, ...]:
        """Ports publics passant par une porte locale (TCP + PROXY v2 vers 127.0.0.1)."""
        return tuple(item for item in self.funnel if item.proxy_protocol == 2
                     and item.target.startswith("tcp://127.0.0.1:"))

    @property
    def funnel(self) -> tuple[Publication, ...]:
        return tuple(item for item in self.publications if item.public)

    @property
    def is_operator(self) -> bool:
        return self.user == "root" or (bool(self.user) and self.preferences.operator == self.user)
