# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Faux lecteurs (jamais le vrai Tailscale, systemd ou journal) et donnees relevees le 2026-11-22."""
from __future__ import annotations

from dataclasses import replace
from datetime import datetime, timezone

import pytest

from omega_tail.application.snapshot import SnapshotTools
from omega_tail.domain.machine import MachineState
from omega_tail.domain.service import ServiceState
from omega_tail.domain.snapshot import Snapshot
from omega_tail.domain.tailscale import BackendState, Preferences, Publication, PublishMode, TailscaleState
from omega_tail.ports.readers import JournalResult

NOW = datetime(2026, 11, 22, 19, 0, tzinfo=timezone.utc)

# `tailscale serve status --json` sur deux machines reelles le 2026-11-22
SERVE_HPC = {"TCP": {"443": {"HTTPS": True}},
             "Web": {"kraynux.tailnet-exemple.ts.net:443": {"Handlers": {"/": {"Proxy": "http://localhost:80"}}}},
             "AllowFunnel": {"kraynux.tailnet-exemple.ts.net:443": True}}
SERVE_MPC_RDP = {"TCP": {"3389": {"TCPForward": "localhost:3389"}}}

STATUS = {
    "Version": "1.104.4-tfb3b9b2964-g0123", "BackendState": "Running", "TUN": True,
    "Self": {"HostName": "omega-server", "DNSName": "kraynux.tailnet-exemple.ts.net.", "UserID": 42,
             "TailscaleIPs": ["100.64.0.72", "fd7a:115c:a1e0::cb32:5e69"], "KeyExpiry": "2027-01-20T19:37:28Z"},
    "User": {"42": {"LoginName": "kraynux@example.org"}},
    "CurrentTailnet": {"Name": "kraynux@example.org"},
    "Peer": {"a": {"Online": True}, "b": {"Online": False}, "c": {"Online": True}},
    "Health": ["b message", "a message", "a message"],
}


def tailscale_state(**changes: object) -> TailscaleState:
    base = TailscaleState(installed=True, reachable=True, client_version="1.104.7", daemon_version="1.104.7",
                          backend=BackendState.RUNNING, dns_name="kraynux.tailnet-exemple.ts.net",
                          host_name="omega-server", addresses=("100.64.0.72",), peers_total=3, peers_online=2)
    return replace(base, **changes)  # type: ignore[arg-type]


def service_state(**changes: object) -> ServiceState:
    base = ServiceState(known=True, active="active", sub="running", enabled="enabled", main_pid=418645,
                        cpu_quota="infinity", cpu_weight="[not set]")
    return replace(base, **changes)  # type: ignore[arg-type]


FUNNEL_HTTPS = Publication(443, True, PublishMode.HTTPS, "kraynux.tailnet-exemple.ts.net", "http://localhost:80", "/")


def snapshot(**changes: object) -> Snapshot:
    base = Snapshot(taken_at=NOW, tailscale=tailscale_state(),
                    preferences=Preferences({"operator": "kraynux"}, readable=True), publications=(),
                    service=service_state(), machine=MachineState(hostname="omega-server", cpu_count=4,
                                                                  temperature_c=50.0, tailscaled_cpu_percent=2.0),
                    user="kraynux", through_tailscale=False)
    return replace(base, **changes)  # type: ignore[arg-type]


class FakeTailscale:
    def __init__(self, state: TailscaleState | None = None, publications: tuple[Publication, ...] = (),
                 operator: str = "kraynux") -> None:
        self._state = state or tailscale_state()
        self._publications = publications
        self._operator = operator

    def state(self) -> TailscaleState:
        return self._state

    def preferences(self) -> Preferences:
        return Preferences({"operator": self._operator}, readable=True)

    def publications(self) -> tuple[Publication, ...]:
        return self._publications


class FakeService:
    def __init__(self, state: ServiceState | None = None) -> None:
        self._state = state or service_state()

    def state(self) -> ServiceState:
        return self._state


class FakeMachine:
    def state(self, tailscaled_pid: int) -> MachineState:
        return MachineState(hostname="omega-server", cpu_count=4, temperature_c=78.0, tailscaled_cpu_percent=6.0)


class FakeJournal:
    def __init__(self, lines: tuple[str, ...] = ("ligne ok", "magicsock: error sending", "warn: retry")) -> None:
        self.lines = lines
        self.calls: list[tuple[str, int]] = []

    def read(self, unit: str, lines: int) -> JournalResult:
        self.calls.append((unit, lines))
        return JournalResult(self.lines)

    def search(self, source: str, since: object, pattern: str) -> JournalResult:
        self.calls.append((source, 0))
        return JournalResult(tuple(line for line in self.lines if "motif=" in line or "groupe=" in line))


def tools(tailscale: FakeTailscale | None = None, service: FakeService | None = None,
          through: bool = False, user: str = "kraynux") -> SnapshotTools:
    return SnapshotTools(tailscale=tailscale or FakeTailscale(), service=service or FakeService(),
                         machine=FakeMachine(), user=lambda: user, through_tailscale=lambda: through,
                         now=lambda: NOW)


@pytest.fixture(autouse=True)
def _isolated_var(tmp_path, monkeypatch):  # type: ignore[no-untyped-def]
    monkeypatch.setenv("OMEGA_TAIL_VAR_DIR", str(tmp_path / "var"))
