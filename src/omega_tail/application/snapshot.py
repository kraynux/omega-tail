# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Lecture complete de la machine (tableau de bord, bande d'etat, `omega-tail etat`)."""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime

from omega_tail.domain.alerts import Alert, alerts_for
from omega_tail.domain.funnel import Cut
from omega_tail.domain.service import ServiceState
from omega_tail.domain.shield import ShieldFacts
from omega_tail.domain.snapshot import Snapshot
from omega_tail.domain.watch import WatchStatus
from omega_tail.ports.readers import MachineReader, ServiceReader, TailscaleReader


@dataclass(frozen=True)
class SnapshotTools:
    tailscale: TailscaleReader
    service: ServiceReader
    machine: MachineReader
    user: Callable[[], str]
    through_tailscale: Callable[[], bool]
    now: Callable[[], datetime]
    cut: Callable[[], Cut | None] = lambda: None
    """Coupure de Funnel en cours (disjoncteur)."""
    gate_service: Callable[[], ServiceState] = lambda: ServiceState(known=False)
    """Service de la porte (pare-feu Funnel)."""
    watch: Callable[[], WatchStatus | None] = lambda: None
    """Veille automatique (Survie)."""
    gate_attack: Callable[[], bool] = lambda: False
    """La porte est en mode attaque (lot 6)."""
    shield: Callable[[], ShieldFacts | None] = lambda: None
    """Bouclier du port WireGuard (lot 8)."""
    blacklist_count: Callable[[], int] = lambda: 0
    """Entrees de la liste noire de la porte."""

    def collect(self) -> Snapshot:
        service = self.service.state()
        return Snapshot(
            taken_at=self.now(), tailscale=self.tailscale.state(), preferences=self.tailscale.preferences(),
            publications=self.tailscale.publications(), service=service,
            machine=self.machine.state(service.main_pid), user=self.user(),
            through_tailscale=self.through_tailscale(), cut=self.cut(),
            gate_service=self.gate_service(), watch=self.watch(), gate_attack=self.gate_attack(),
            shield=self.shield(), blacklist_count=self.blacklist_count())

    def alerts(self, snapshot: Snapshot) -> tuple[Alert, ...]:
        return alerts_for(snapshot, self.now())
