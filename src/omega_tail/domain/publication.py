# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Publication (lot 5, proposition §3.4) : ajouter, retirer, reconstruire ce que Serve (tailnet) et Funnel
(Internet) publient, et nommer les sauvegardes.

Constats (J3455, Tailscale 1.104.5, 2026-11-22) : « --https=PORT off » retire tous les chemins du port et son
autorisation Funnel ; « --tcp=PORT off » laisse l'autorisation Funnel du port (sans effet tant que rien n'y est
servi, mais un Serve ajoute plus tard sur ce port deviendrait public). D'ou la verification apres chaque changement
et, si le resultat n'est pas celui voulu, la reconstruction complete (`serve reset` puis chaque point, une
commande par point), qui repart d'une configuration propre."""
from __future__ import annotations

import re
from collections.abc import Iterable
from dataclasses import dataclass

from omega_tail.core.constants import TAILSCALE_COMMAND
from omega_tail.domain.funnel import Handler
from omega_tail.shared.i18n import N_

FUNNEL_PORTS = (443, 8443, 10000)
"""Seuls ports que Funnel ouvre a Internet."""
KINDS = ("https", "http", "tcp", "tls-terminated-tcp")
WEB_KINDS = ("https", "http")
LOCAL_HOSTS = ("127.0.0.1", "localhost", "[::1]")
PATH = re.compile(r"^/[A-Za-z0-9._~/-]{0,200}$")
LOCAL_URL = re.compile(r"^(https?|https\+insecure)://(127\.0\.0\.1|localhost|\[::1\]):(\d{1,5})(/[A-Za-z0-9._~/-]*)?$")
LOCAL_TCP = re.compile(r"^tcp://(127\.0\.0\.1|localhost|\[::1\]):(\d{1,5})$")


class PublicationError(ValueError):
    """Demande refusee ; le message est une phrase marquee pour la traduction."""


@dataclass(frozen=True)
class AddRequest:
    kind: str
    port: int
    target: str
    """Port local (« 8080 ») ou adresse locale (http://127.0.0.1:8080, tcp://127.0.0.1:22)."""
    public: bool
    path: str = "/"


def _port(text: str | int) -> int:
    value = int(text) if str(text).isdigit() else -1
    if not 1 <= value <= 65535:
        raise PublicationError(N_("port de 1 à 65535 attendu"))
    return value


def local_target(kind: str, text: str) -> str:
    """Cible locale, ecrite comme Tailscale l'attend. Un service local seulement (jamais une autre machine)."""
    value = text.strip()
    if value.isdigit():
        port = _port(value)
        return f"http://127.0.0.1:{port}" if kind in WEB_KINDS else f"tcp://127.0.0.1:{port}"
    if kind in WEB_KINDS:
        found = LOCAL_URL.match(value)
        if found is None:
            raise PublicationError(N_("cible locale attendue : un port, ou http://127.0.0.1:PORT"))
        _port(found.group(3))
        return value
    found = LOCAL_TCP.match(value)
    if found is None:
        raise PublicationError(N_("cible locale attendue : un port, ou tcp://127.0.0.1:PORT"))
    _port(found.group(2))
    return value


def handler_for(request: AddRequest) -> Handler:
    if request.kind not in KINDS:
        raise PublicationError(N_("mode inconnu"))
    port = _port(request.port)
    if request.public and port not in FUNNEL_PORTS:
        raise PublicationError(N_("Funnel n'ouvre que les ports 443, 8443 et 10000"))
    path = ""
    if request.kind in WEB_KINDS:
        path = request.path.strip() or "/"
        if not PATH.match(path):
            raise PublicationError(N_("chemin attendu : /, /site, /api/v1…"))
    return Handler(request.kind, port, local_target(request.kind, request.target), path, 0, request.public)


def conflict(handler: Handler, current: Iterable[Handler]) -> str:
    """Pourquoi l'ajout heurte l'existant (phrase marquee), vide sinon."""
    for other in current:
        if other.port != handler.port:
            continue
        if other.public != handler.public:
            return N_("ce port est déjà publié pour un autre public (tailnet / Internet)")
        if handler.kind not in WEB_KINDS or other.kind not in WEB_KINDS:
            return N_("ce port est déjà publié")
        if other.kind != handler.kind:
            return N_("ce port est déjà publié dans un autre mode")
        if other.path == handler.path:
            return N_("ce chemin est déjà publié sur ce port")
    return ""


def _verb(handler: Handler) -> str:
    return "funnel" if handler.public else "serve"


def add_command(handler: Handler) -> tuple[str, ...]:
    command = [TAILSCALE_COMMAND, _verb(handler), "--bg", "--yes", f"--{handler.kind}={handler.port}"]
    if handler.kind in WEB_KINDS and handler.path and handler.path != "/":
        command.append(f"--set-path={handler.path}")
    if handler.proxy_protocol:
        command.append(f"--proxy-protocol={handler.proxy_protocol}")
    command.append(handler.target)
    return tuple(command)


def remove_command(handler: Handler, current: Iterable[Handler]) -> tuple[str, ...]:
    """Un chemin seul quand le port en publie d'autres ; sinon le port entier."""
    command = [TAILSCALE_COMMAND, _verb(handler), f"--{handler.kind}={handler.port}"]
    shared = any(other.port == handler.port and other != handler for other in current)
    if handler.kind in WEB_KINDS and shared:
        command.append(f"--set-path={handler.path or '/'}")
    command.append("off")
    return tuple(command)


def rebuild_commands(handlers: Iterable[Handler]) -> tuple[tuple[str, ...], ...]:
    """Repartir d'une publication vide, puis recreer chaque point (« / » d'abord sur chaque port)."""
    ordered = sorted(handlers, key=lambda item: (item.port, item.path != "/", item.path))
    return ((TAILSCALE_COMMAND, "serve", "reset"), *(add_command(handler) for handler in ordered))


def is_gate_handler(handler: Handler, gate_port: int) -> bool:
    return (handler.public and handler.kind == "tcp" and handler.proxy_protocol == 2
            and handler.target == f"tcp://127.0.0.1:{gate_port}")


BACKUP_NAME = re.compile(r"^funnel-(?:(?P<kind>[a-z]+)-)?(?P<day>\d{8})-(?P<time>\d{6})\.json$")
BACKUP_KINDS = {"porte": N_("pare-feu"), "publication": N_("publication"), "veille": N_("veille automatique"),
                "": N_("disjoncteur")}


@dataclass(frozen=True)
class Backup:
    path: str
    when: str
    """« 2026-11-23 10:15:00 »."""
    origin: str
    """Qui l'a faite (phrase marquee : pare-feu, publication, disjoncteur)."""
    handlers: tuple[Handler, ...] = ()

    @property
    def summary(self) -> str:
        if not self.handlers:
            return "∅"
        return ", ".join(sorted({f"{item.kind} {item.port}{' (Funnel)' if item.public else ''}"
                                 for item in self.handlers}))


def backup_from(path: str, handlers: tuple[Handler, ...]) -> Backup | None:
    name = path.rsplit("/", 1)[-1]
    found = BACKUP_NAME.match(name)
    if found is None:
        return None
    day, time = found.group("day"), found.group("time")
    when = f"{day[:4]}-{day[4:6]}-{day[6:]} {time[:2]}:{time[2:4]}:{time[4:]}"
    origin = BACKUP_KINDS.get(found.group("kind") or "", BACKUP_KINDS[""])
    return Backup(path, when, origin, handlers)
