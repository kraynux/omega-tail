# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Etat de Tailscale sur cette machine, tel que le client `tailscale` le donne (status, get, serve status).
Aucune lecture ici : les formats de Tailscale sont traduits par infrastructure/tailscale/parsing.py."""
from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class BackendState(str, Enum):
    RUNNING = "Running"
    STOPPED = "Stopped"
    NEEDS_LOGIN = "NeedsLogin"
    NEEDS_MACHINE_AUTH = "NeedsMachineAuth"
    STARTING = "Starting"
    NO_STATE = "NoState"
    UNKNOWN = "Unknown"

    @classmethod
    def parse(cls, text: str) -> BackendState:
        return next((state for state in cls if state.value == text), cls.UNKNOWN)


@dataclass(frozen=True)
class TailscaleState:
    installed: bool
    """Le client `tailscale` est present."""
    reachable: bool
    """Le service `tailscaled` a repondu."""
    client_version: str = ""
    daemon_version: str = ""
    backend: BackendState = BackendState.UNKNOWN
    dns_name: str = ""
    host_name: str = ""
    tailnet: str = ""
    user: str = ""
    addresses: tuple[str, ...] = ()
    key_expiry: datetime | None = None
    peers_total: int = 0
    peers_online: int = 0
    tun: bool | None = None
    health: tuple[str, ...] = ()
    error: str = ""
    """Derniere ligne d'erreur de `tailscale status` quand le service n'a pas repondu."""

    @property
    def versions_differ(self) -> bool:
        """Client mis a jour mais service pas redemarre (cas releve sur deux machines en production, 2026-11-22)."""
        return bool(self.client_version and self.daemon_version and self.client_version != self.daemon_version)


@dataclass(frozen=True)
class Preferences:
    """Preferences de `tailscale get` (nom -> valeur, telles qu'affichees)."""
    values: Mapping[str, str] = field(default_factory=dict)
    readable: bool = False

    @property
    def operator(self) -> str:
        return self.values.get("operator", "")


class PublishMode(str, Enum):
    HTTPS = "https"
    HTTP = "http"
    TCP = "tcp"
    TLS_TERMINATED_TCP = "tls-terminated-tcp"


@dataclass(frozen=True)
class Publication:
    """Un port publie par Serve (tailnet seul) ou Funnel (Internet)."""
    port: int
    public: bool
    mode: PublishMode
    host: str = ""
    target: str = ""
    path: str = ""
    proxy_protocol: int = 0

    @property
    def tls_by_tailscaled(self) -> bool:
        """tailscaled fait la poignee de main TLS de chaque connexion (cout mesure : ~80 % du CPU par connexion,
        MESURES_LOT0.md §8)."""
        return self.mode in (PublishMode.HTTPS, PublishMode.TLS_TERMINATED_TCP)

    @property
    def exposed(self) -> bool:
        """Public ET TLS fait par tailscaled : la configuration que la porte d'omega-tail doit proteger."""
        return self.public and self.tls_by_tailscaled


@dataclass(frozen=True)
class Profile:
    """Un compte connu de cette machine (`tailscale switch --list`)."""
    profile_id: str
    tailnet: str
    account: str
    current: bool = False


@dataclass(frozen=True)
class ExitNode:
    """Un noeud de sortie propose dans le tailnet (`tailscale exit-node list`)."""
    address: str
    name: str
    status: str = ""


@dataclass(frozen=True)
class Certificate:
    """Certificat presente par un port publie (lu par une vraie connexion TLS)."""
    not_after: datetime | None
    issuer: str = ""
    subject: str = ""
    tls_version: str = ""


@dataclass(frozen=True)
class Probe:
    """Essai de bout en bout d'un port publie."""
    ok: bool
    detail: str
    milliseconds: float = 0.0
    certificate: Certificate | None = None
    via: str = ""
    """Adresse jointe (relais Funnel pour un essai public, adresse du tailnet sinon)."""
