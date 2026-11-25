# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Traduction des sorties du client `tailscale` (1.104, releves du 2026-11-22) en objets du domaine. Lecture
prudente : un champ absent ou d'un autre type donne une valeur vide, jamais une erreur."""
from __future__ import annotations

from collections.abc import Mapping
from datetime import datetime
from typing import Any

from omega_tail.domain.network import Device
from omega_tail.domain.tailscale import (
    BackendState,
    ExitNode,
    Preferences,
    Profile,
    Publication,
    PublishMode,
    TailscaleState,
)
from omega_tail.domain.text import without_controls


def short_version(text: str) -> str:
    """« 1.104.4-tfb3b9b2964-g… » ou « 1.104.7\\n  tailscale commit… » -> « 1.104.4 »."""
    first = text.strip().splitlines()[0].strip() if text.strip() else ""
    return first.split("-", 1)[0]


def _dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _time(text: Any) -> datetime | None:
    if not isinstance(text, str) or not text or text.startswith("0001-"):
        return None
    try:
        return datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError:
        return None


def parse_status(data: Mapping[str, Any], client_version: str) -> TailscaleState:
    me = _dict(data.get("Self"))
    users = _dict(data.get("User"))
    user = _dict(users.get(str(me.get("UserID", ""))))
    peers = [_dict(peer) for peer in _dict(data.get("Peer")).values()]
    tailnet = _dict(data.get("CurrentTailnet"))
    health = data.get("Health")
    return TailscaleState(
        installed=True, reachable=True, client_version=client_version,
        daemon_version=short_version(str(data.get("Version", ""))),
        backend=BackendState.parse(str(data.get("BackendState", ""))),
        dns_name=str(me.get("DNSName", "")).rstrip("."), host_name=str(me.get("HostName", "")),
        tailnet=str(tailnet.get("Name", "")), user=str(user.get("LoginName", "")),
        addresses=tuple(str(ip) for ip in me.get("TailscaleIPs") or ()),
        key_expiry=_time(me.get("KeyExpiry")),
        peers_total=len(peers), peers_online=sum(1 for peer in peers if peer.get("Online")),
        tun=data.get("TUN") if isinstance(data.get("TUN"), bool) else None,
        health=tuple(sorted(dict.fromkeys(str(item) for item in health))) if isinstance(health, list) else ())


def parse_preferences(text: str) -> Preferences:
    """Tableau de `tailscale get` : « NAME  VALUE » puis une ligne par preference (valeur vide possible)."""
    values: dict[str, str] = {}
    for line in text.splitlines()[1:]:
        if not line.strip():
            continue
        name, _sep, value = line.strip().partition(" ")
        values[name] = value.strip()
    return Preferences(values=values, readable=bool(values))


def _funnel_ports(config: Mapping[str, Any]) -> dict[int, str]:
    """« hote:port » ouverts a Funnel -> {port: hote}."""
    ports: dict[int, str] = {}
    for key, allowed in _dict(config.get("AllowFunnel")).items():
        host, _sep, port = str(key).rpartition(":")
        if allowed and port.isdigit():
            ports[int(port)] = host
    return ports


def _publications_of(config: Mapping[str, Any], default_host: str) -> list[Publication]:
    funnel = _funnel_ports(config)
    web = _dict(config.get("Web"))
    found: list[Publication] = []
    for port_text, handler_any in _dict(config.get("TCP")).items():
        if not str(port_text).isdigit():
            continue
        port, handler = int(port_text), _dict(handler_any)
        public, host = port in funnel, funnel.get(port, default_host)
        proxy = handler.get("ProxyProtocol")
        proxy_protocol = proxy if isinstance(proxy, int) else 0
        if handler.get("HTTPS") or handler.get("HTTP"):
            mode = PublishMode.HTTPS if handler.get("HTTPS") else PublishMode.HTTP
            routes = [(key, _dict(value)) for key, value in web.items() if str(key).endswith(f":{port}")]
            if not routes:
                found.append(Publication(port, public, mode, host))
            for key, site in routes:
                site_host = str(key).rpartition(":")[0]
                for path, target_any in sorted(_dict(site.get("Handlers")).items()):
                    target = _dict(target_any)
                    shown = target.get("Proxy") or target.get("Path") or ("text" if "Text" in target else "")
                    found.append(Publication(port, public, mode, site_host, str(shown), str(path), proxy_protocol))
        elif handler.get("TCPForward"):
            mode = PublishMode.TLS_TERMINATED_TCP if handler.get("TerminateTLS") else PublishMode.TCP
            found.append(Publication(port, public, mode, host, f"tcp://{handler['TCPForward']}", "",
                                     proxy_protocol))
    return found


def parse_serve(data: Mapping[str, Any], default_host: str = "") -> tuple[Publication, ...]:
    """`tailscale serve status --json` : configuration de fond, plus les sessions au premier plan (« Foreground »)."""
    found = _publications_of(data, default_host)
    for session in _dict(data.get("Foreground")).values():
        found.extend(_publications_of(_dict(session), default_host))
    return tuple(sorted(found, key=lambda item: (not item.public, item.port, item.path)))


def parse_profiles(text: str) -> tuple[Profile, ...]:
    """`tailscale switch --list` : « ID  Tailnet  Account » puis une ligne par compte, « * » sur le compte en
    cours (a la fin du nom du compte)."""
    found = []
    for line in text.splitlines()[1:]:
        parts = line.split()
        if len(parts) < 2:
            continue
        current = parts[-1].endswith("*") or parts[0].endswith("*")
        account = parts[-1].rstrip("*")
        tailnet = " ".join(parts[1:-1]) if len(parts) > 2 else ""
        found.append(Profile(parts[0].rstrip("*"), tailnet, account, current))
    return tuple(found)


def parse_exit_nodes(text: str) -> tuple[ExitNode, ...]:
    """`tailscale exit-node list` : tableau « IP HOSTNAME COUNTRY CITY STATUS » (pays et ville en plusieurs mots
    possibles : seuls l'adresse, le nom et « selected » / « offline » sont lus) ; « no exit nodes found » et les
    commentaires sont ignores."""
    found = []
    for line in text.splitlines():
        parts = line.split()
        if len(parts) < 2 or not (parts[0][0].isdigit() or ":" in parts[0]):
            continue
        status = next((word for word in ("selected", "offline") if word in (part.strip(",") for part in parts)), "")
        found.append(ExitNode(parts[0], parts[1].rstrip("."), status))
    return tuple(found)


def _clean(value: Any) -> str:
    return without_controls(str(value or ""))


def _int(value: Any) -> int:
    return value if isinstance(value, int) and not isinstance(value, bool) else 0


def parse_devices(data: Mapping[str, Any]) -> tuple[Device, ...]:
    """Appareils du tailnet (`status --json`, cle « Peer ») ; la machine elle-meme n'en fait pas partie."""
    devices = []
    for peer in (_dict(item) for item in _dict(data.get("Peer")).values()):
        # Chaque machine declare elle-meme son nom et son systeme : jamais de caractere de controle (F7, 2026-11-25)
        dns = _clean(peer.get("DNSName")).rstrip(".")
        tags = peer.get("Tags")
        devices.append(Device(
            name=_clean(peer.get("HostName")) or dns.split(".", 1)[0] or "?", dns_name=dns,
            os=_clean(peer.get("OS")),
            online=peer.get("Online") is True, active=peer.get("Active") is True,
            direct=_clean(peer.get("CurAddr")), relay=_clean(peer.get("Relay")),
            last_seen=_time(peer.get("LastSeen")),
            addresses=tuple(_clean(ip) for ip in peer.get("TailscaleIPs") or ()),
            rx_bytes=_int(peer.get("RxBytes")), tx_bytes=_int(peer.get("TxBytes")),
            tags=tuple(_clean(tag) for tag in tags) if isinstance(tags, list) else (),
            exit_node=peer.get("ExitNode") is True, exit_option=peer.get("ExitNodeOption") is True))
    return tuple(devices)
