# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Lectures de la machine (toutes sans droits particuliers)."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Protocol

from omega_tail.domain.machine import MachineState
from omega_tail.domain.network import Device, Metrics, Netcheck
from omega_tail.domain.service import ServiceState
from omega_tail.domain.tailscale import Preferences, Publication, TailscaleState


class TailscaleReader(Protocol):
    def state(self) -> TailscaleState: ...
    def preferences(self) -> Preferences: ...
    def publications(self) -> tuple[Publication, ...]: ...


class ServiceReader(Protocol):
    def state(self) -> ServiceState: ...


class MachineReader(Protocol):
    def state(self, tailscaled_pid: int) -> MachineState: ...


@dataclass(frozen=True)
class JournalResult:
    lines: tuple[str, ...]
    error: str = ""
    """Pourquoi rien n'a ete lu (droits, journalctl absent...)."""
    hint: str = ""
    """Ce que l'utilisateur peut faire (marque pour la traduction)."""
    truncated: bool = False
    """Trop de lignes : seules les plus recentes ont ete lues."""


class JournalReader(Protocol):
    def read(self, source: str, lines: int) -> JournalResult:
        """`source` : « tailscaled » ou « porte » (le lecteur sait ou les trouver selon le systeme d'init)."""
        ...

    def search(self, source: str, since: date, pattern: str) -> JournalResult:
        """Lignes depuis le jour `since` (inclus) qui contiennent l'expression `pattern`, les plus recentes d'abord,
        bornees en taille (`truncated`)."""
        ...


class NetworkReader(Protocol):
    """Reseau et appareils (lot 7) : lectures seules du client `tailscale`."""
    def devices(self) -> tuple[Device, ...]:
        """Leve OSError si tailscaled ne repond pas."""
        ...
    def netcheck(self) -> Netcheck: ...
    def text(self, *arguments: str) -> tuple[str, str]: ...
    def metrics(self) -> Metrics: ...
    def ping(self, target: str) -> str: ...
    def whois(self, target: str) -> str: ...
