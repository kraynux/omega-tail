# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Reseau et appareils (lot 7, proposition §3.5) : appareils du tailnet, diagnostic reseau (netcheck), compteurs
internes (metrics). Lecture seule ; rien ici ne change un reglage de Tailscale."""
from __future__ import annotations

import re
from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import datetime

INGRESS_TAG = "tag:ingress"
"""Relais Funnel de Tailscale (« funnel-ingress-node ») : vus comme des appareils, mais ce ne sont pas les votres."""


@dataclass(frozen=True)
class Device:
    name: str
    dns_name: str = ""
    os: str = ""
    online: bool = False
    active: bool = False
    """Echange en cours avec cette machine."""
    direct: str = ""
    """Adresse du chemin direct (vide : relais DERP ou pas de chemin)."""
    relay: str = ""
    """Code du relais DERP de l'appareil (« par »)."""
    last_seen: datetime | None = None
    addresses: tuple[str, ...] = ()
    rx_bytes: int = 0
    tx_bytes: int = 0
    tags: tuple[str, ...] = ()
    exit_node: bool = False
    """Sert de sortie Internet a cette machine en ce moment."""
    exit_option: bool = False

    @property
    def ingress(self) -> bool:
        return INGRESS_TAG in self.tags

    @property
    def address(self) -> str:
        """Adresse IPv4 du tailnet si elle existe (la plus courte a taper), sinon la premiere."""
        return next((item for item in self.addresses if "." in item), self.addresses[0] if self.addresses else "")

    @property
    def path(self) -> str:
        """« direct », « relais » (DERP) ou vide (pas d'echange en cours : chemin inconnu)."""
        if self.direct:
            return "direct"
        return "relais" if self.active else ""


def matches(device: Device, text: str) -> bool:
    """Filtre de l'ecran : nom, nom DNS, systeme, adresse ou etiquette contient le texte (sans casse)."""
    needle = text.strip().lower()
    if not needle:
        return True
    fields = (device.name, device.dns_name, device.os, *device.addresses, *device.tags)
    return any(needle in item.lower() for item in fields)


def sort_devices(devices: list[Device]) -> list[Device]:
    """En ligne d'abord, puis par nom ; les relais Funnel a la fin."""
    return sorted(devices, key=lambda item: (item.ingress, not item.online, item.name.lower()))


@dataclass(frozen=True)
class Latency:
    code: str
    milliseconds: float | None
    city: str


@dataclass(frozen=True)
class Netcheck:
    """Diagnostic reseau de Tailscale (`tailscale netcheck`, sortie texte : la meme depuis des annees)."""
    udp: bool | None = None
    ipv4: str = ""
    """« yes, 1.2.3.4:5678 », « no »… tel que lu."""
    ipv6: str = ""
    varies: bool | None = None
    """MappingVariesByDestIP : vrai = NAT difficile (le port change selon la destination)."""
    port_mapping: str = ""
    nearest: str = ""
    latencies: tuple[Latency, ...] = ()
    raw: str = ""
    error: str = ""


_ITEM = re.compile(r"^\s*\*\s*([^:]+):\s*(.*)$")
_LATENCY = re.compile(r"^\s*-\s*([a-z0-9-]+):\s*([0-9.]+)?(ms|s|µs)?\s*\((.*)\)\s*$")


def _yes(value: str) -> bool | None:
    word = value.strip().split(",", 1)[0].strip().lower()
    if word in ("true", "yes"):
        return True
    if word in ("false", "no"):
        return False
    return None


def parse_netcheck(text: str) -> Netcheck:
    values: dict[str, str] = {}
    latencies: list[Latency] = []
    for line in text.splitlines():
        found = _LATENCY.match(line)
        if found:
            number = None
            if found.group(2):
                number = float(found.group(2)) * {"s": 1000.0, "µs": 0.001}.get(found.group(3) or "ms", 1.0)
            latencies.append(Latency(found.group(1), number, found.group(4).strip()))
            continue
        item = _ITEM.match(line)
        if item:
            values[item.group(1).strip()] = item.group(2).strip()
    return Netcheck(udp=_yes(values.get("UDP", "")), ipv4=values.get("IPv4", ""), ipv6=values.get("IPv6", ""),
                    varies=_yes(values.get("MappingVariesByDestIP", "")),
                    port_mapping=values.get("PortMapping", ""), nearest=values.get("Nearest DERP", ""),
                    latencies=tuple(latencies), raw=text)


@dataclass(frozen=True)
class Metrics:
    """Compteurs internes de tailscaled (`tailscale metrics print`, format Prometheus)."""
    values: Mapping[str, float] = field(default_factory=dict)
    """« nom{etiquettes} » -> valeur."""

    def total(self, name: str, **labels: str) -> float:
        """Somme des series de ce nom dont les etiquettes contiennent `labels`."""
        found = 0.0
        for key, value in self.values.items():
            base, _sep, rest = key.partition("{")
            if base != name:
                continue
            if all(f'{label}="{wanted}"' in rest for label, wanted in labels.items()):
                found += value
        return found

    def by_label(self, name: str, label: str) -> dict[str, float]:
        out: dict[str, float] = {}
        pattern = re.compile(rf'{label}="([^"]*)"')
        for key, value in self.values.items():
            base, _sep, rest = key.partition("{")
            found = pattern.search(rest)
            if base == name and found:
                out[found.group(1)] = out.get(found.group(1), 0.0) + value
        return out


def parse_metrics(text: str) -> Metrics:
    values: dict[str, float] = {}
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        key, _sep, number = line.rpartition(" ")
        try:
            values[key] = float(number)
        except ValueError:
            continue
    return Metrics(values)


_TARGET = re.compile(r"^[A-Za-z0-9][A-Za-z0-9.:_-]{0,252}$")


def valid_target(text: str) -> bool:
    """Nom ou adresse a passer a `tailscale ping` / `whois` : jamais une option (« -… »), ni espace, ni autre
    caractere."""
    return bool(_TARGET.match(text.strip()))
