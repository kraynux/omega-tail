# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Rapport de la machine (lot 7, proposition §4.4) : tout ce qu'omega-tail sait, rassemble en une fois pour etre
exporte (TXT, HTML, JSON) ou lu dans l'ecran Rapport. Faits seulement ; lecture seule, sans droits.

Vie privee (decision B du lot 7) : un rapport peut etre envoye a quelqu'un. Sans `include_private`, le compte
Tailscale et les noms / adresses des appareils du tailnet n'y figurent pas (seulement leur nombre) ; les adresses
des attaquants y restent toujours."""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import datetime, timedelta

from omega_tail.application.gate import BLACK, GateCounters, GateState, GateTools, TableRow
from omega_tail.application.groups import GroupRow, GroupsStatus
from omega_tail.application.network import NetworkTools
from omega_tail.application.snapshot import SnapshotTools
from omega_tail.application.watch import WatchTools
from omega_tail.domain.alerts import Alert
from omega_tail.domain.breaker import BreakerPolicy
from omega_tail.domain.gate import GatePolicy
from omega_tail.domain.network import Device, sort_devices
from omega_tail.domain.report import REPORT_DAYS, SEARCH_PATTERN, Refusals, summarize
from omega_tail.domain.snapshot import Snapshot
from omega_tail.domain.watch import WatchStatus
from omega_tail.ports.readers import JournalReader

TOP_GROUPS = 5
JOURNAL_SOURCE = "porte"


@dataclass(frozen=True)
class GateFacts:
    policy: GatePolicy
    state: GateState | None
    counters: GateCounters
    certificate_days: int | None
    trusted: tuple[str, ...]
    black: tuple[str, ...]
    blocked: tuple[TableRow, ...]
    """Adresses bloquees en ce moment (hors liste noire)."""
    busiest: tuple[TableRow, ...]
    groups: GroupsStatus | None = None
    top_fingerprints: tuple[GroupRow, ...] = ()
    top_as: tuple[GroupRow, ...] = ()
    top_countries: tuple[GroupRow, ...] = ()


@dataclass(frozen=True)
class ReportFacts:
    version: str
    generated_at: datetime
    snapshot: Snapshot
    alerts: tuple[Alert, ...]
    include_private: bool
    breaker: BreakerPolicy
    devices: tuple[Device, ...] = ()
    """Seulement avec `include_private`."""
    device_counts: tuple[int, int, int] | None = None
    """(en ligne, total, relais Funnel de Tailscale) ; None si illisible."""
    gate: GateFacts | None = None
    watch: WatchStatus | None = None
    watch_journal: tuple[str, ...] = ()
    refusals: Refusals = field(default_factory=Refusals)


@dataclass
class ReportTools:
    version: str
    snapshots: SnapshotTools
    journal: JournalReader
    breaker: Callable[[], BreakerPolicy]
    now: Callable[[], datetime]
    gate: GateTools | None = None
    watch: WatchTools | None = None
    network: NetworkTools | None = None

    def refusals(self, today: datetime) -> Refusals:
        since = (today - timedelta(days=REPORT_DAYS - 1)).date()
        result = self.journal.search(JOURNAL_SOURCE, since, SEARCH_PATTERN)
        if result.error:
            return Refusals(error=result.error, hint=result.hint)
        return summarize(result.lines, today.date(), REPORT_DAYS, truncated=result.truncated)

    def _gate(self) -> GateFacts | None:
        gate = self.gate
        if gate is None:
            return None
        trusted, black = gate.lists()
        rows = gate.decisions()
        groups = gate.groups
        status = groups.status() if groups is not None and groups.lua() else None
        return GateFacts(
            policy=gate.policy(), state=gate.state(), counters=gate.counters(),
            certificate_days=gate.certificate_days(), trusted=tuple(trusted), black=tuple(black),
            blocked=tuple(row for row in rows if row.blocked and row.listed != BLACK),
            busiest=tuple(sorted((row for row in rows if row.seen), key=lambda row: row.rate_10s, reverse=True)[:10]),
            groups=status,
            top_fingerprints=tuple(groups.top_fingerprints(TOP_GROUPS)) if status is not None and groups else (),
            top_as=tuple(groups.top_as(TOP_GROUPS)) if status is not None and groups else (),
            top_countries=tuple(groups.top_countries(TOP_GROUPS)) if status is not None and groups else ())

    def build(self, *, include_private: bool = False, snapshot: Snapshot | None = None) -> ReportFacts:
        """`snapshot` : la derniere lecture de l'interface (sinon une lecture neuve)."""
        moment = self.now()
        snapshot = snapshot or self.snapshots.collect()
        devices: tuple[Device, ...] = ()
        counts: tuple[int, int, int] | None = None
        if self.network is not None:
            found = self.network.devices()
            mine = tuple(item for item in sort_devices(list(found.devices)) if not item.ingress)
            if not found.error:
                counts = (sum(1 for item in mine if item.online), len(mine), len(found.devices) - len(mine))
            devices = mine if include_private else ()
        return ReportFacts(
            version=self.version, generated_at=moment, snapshot=snapshot, alerts=self.snapshots.alerts(snapshot),
            include_private=include_private, breaker=self.breaker(), devices=devices, device_counts=counts,
            gate=self._gate(),
            watch=self.watch.status() if self.watch is not None else None,
            watch_journal=tuple(self.watch.journal(10)) if self.watch is not None else (),
            refusals=self.refusals(moment) if self.gate is not None else Refusals())
