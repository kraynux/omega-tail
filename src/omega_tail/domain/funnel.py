# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Disjoncteur Funnel (lot 2, decision 2026-11-22) : couper Funnel puis le remettre A L'IDENTIQUE.

Tailscale 1.104 n'a pas de reglage brut de la publication (`serve get-config` ne couvre que les « Tailscale
Services ») : la publication est sauvegardee (`serve status --json`), puis recreee commande par commande.
Constate sur le J3455 le 2026-11-22 : `--https=PORT off` retire tous les chemins du port ; « ProxyProtocol » est la
cle du PROXY protocol. Seuls les ports ouverts a Internet (AllowFunnel) sont coupes ; Serve (tailnet) reste."""
from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

from omega_tail.core.constants import TAILSCALE_COMMAND


@dataclass(frozen=True)
class Handler:
    """Un point de publication, tel que la ligne de commande le recree."""
    kind: str
    """https, http, tcp ou tls-terminated-tcp (nom du drapeau de la ligne de commande)."""
    port: int
    target: str
    path: str = ""
    proxy_protocol: int = 0
    public: bool = False


def _dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _target(handler: Mapping[str, Any]) -> str:
    if "Proxy" in handler:
        return str(handler["Proxy"])
    if "Path" in handler:
        return str(handler["Path"])
    if "Text" in handler:
        return f"text:{handler['Text']}"
    return ""


def handlers_of(config: Mapping[str, Any]) -> tuple[Handler, ...]:
    """Les points publies d'une configuration (`serve status --json`, sans les sessions au premier plan)."""
    funnel = {int(key.rpartition(":")[2]) for key, allowed in _dict(config.get("AllowFunnel")).items()
              if allowed and str(key).rpartition(":")[2].isdigit()}
    web = _dict(config.get("Web"))
    found: list[Handler] = []
    for port_text, raw in sorted(_dict(config.get("TCP")).items(), key=lambda item: int(item[0])
                                 if str(item[0]).isdigit() else 0):
        if not str(port_text).isdigit():
            continue
        port, handler = int(port_text), _dict(raw)
        proxy = handler.get("ProxyProtocol") if isinstance(handler.get("ProxyProtocol"), int) else 0
        if handler.get("HTTPS") or handler.get("HTTP"):
            kind = "https" if handler.get("HTTPS") else "http"
            for key, site in web.items():
                if str(key).rpartition(":")[2] != str(port):
                    continue
                for path, target in sorted(_dict(_dict(site).get("Handlers")).items()):
                    found.append(Handler(kind, port, _target(_dict(target)), path, 0, port in funnel))
        elif handler.get("TCPForward"):
            kind = "tls-terminated-tcp" if handler.get("TerminateTLS") else "tcp"
            found.append(Handler(kind, port, f"tcp://{handler['TCPForward']}", "", int(proxy or 0),
                                 port in funnel))
    return tuple(found)


def public_ports(config: Mapping[str, Any]) -> tuple[tuple[str, int], ...]:
    """(type, port) ouverts a Internet, une fois chacun (un « off » retire tous les chemins du port)."""
    return tuple(dict.fromkeys((handler.kind, handler.port) for handler in handlers_of(config) if handler.public))


def funnel_allowed(config: Mapping[str, Any]) -> tuple[int, ...]:
    """Ports encore autorises a Funnel. `--tcp=PORT off` retire le point mais LAISSE l'autorisation : Tailscale
    annonce toujours « Funnel on » sur ce port et le relais continue d'y envoyer les connexions d'Internet
    (constate en reel sur le J3455, 1.104.5, 2026-11-23)."""
    return tuple(sorted({int(key.rpartition(":")[2]) for key, allowed in _dict(config.get("AllowFunnel")).items()
                         if allowed and str(key).rpartition(":")[2].isdigit()}))


def tailnet_only_commands(config: Mapping[str, Any]) -> tuple[tuple[str, ...], ...]:
    """Repartir d'une publication vide puis recreer les seuls points du tailnet : seule facon de retirer une
    autorisation Funnel restee sans point publie."""
    kept = sorted((handler for handler in handlers_of(config) if not handler.public),
                  key=lambda item: (item.port, item.path not in ("", "/"), item.path))
    commands: list[tuple[str, ...]] = [(TAILSCALE_COMMAND, "serve", "reset")]
    for handler in kept:
        command = [TAILSCALE_COMMAND, "serve", "--bg", "--yes", f"--{handler.kind}={handler.port}"]
        if handler.kind in ("https", "http") and handler.path and handler.path != "/":
            command.append(f"--set-path={handler.path}")
        if handler.proxy_protocol:
            command.append(f"--proxy-protocol={handler.proxy_protocol}")
        command.append(handler.target)
        commands.append(tuple(command))
    return tuple(commands)


def cut_commands(config: Mapping[str, Any]) -> tuple[tuple[str, ...], ...]:
    return tuple((TAILSCALE_COMMAND, "funnel", f"--{kind}={port}", "off") for kind, port in public_ports(config))


def restore_commands(config: Mapping[str, Any]) -> tuple[tuple[str, ...], ...]:
    """Recree les points publics, dans l'ordre (le chemin « / » d'abord)."""
    commands = []
    for handler in handlers_of(config):
        if not handler.public:
            continue
        command = [TAILSCALE_COMMAND, "funnel", "--bg", "--yes", f"--{handler.kind}={handler.port}"]
        if handler.path and handler.path != "/":
            command.append(f"--set-path={handler.path}")
        if handler.proxy_protocol:
            command.append(f"--proxy-protocol={handler.proxy_protocol}")
        command.append(handler.target)
        commands.append(tuple(command))
    return tuple(commands)


def same_publication(saved: Mapping[str, Any], current: Mapping[str, Any]) -> bool:
    """La remise en route a-t-elle redonne exactement les memes points publics ?"""
    def public(config: Mapping[str, Any]) -> set[Handler]:
        return {handler for handler in handlers_of(config) if handler.public}
    return public(saved) == public(current)


@dataclass(frozen=True)
class Cut:
    """Coupure en cours, posee par omega-tail (var/funnel/etat.json)."""
    cut_id: str
    cut_at: str
    """Horodatage ISO de la coupure."""
    until: str = ""
    """Horodatage ISO de la remise en route prevue ; vide : coupure totale (remise en route manuelle)."""
    saved: str = ""
    """Fichier de la publication sauvegardee juste avant la coupure."""
    ports: tuple[int, ...] = ()

    @property
    def total(self) -> bool:
        return not self.until
