# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Regroupements par AS et par pays (lot 6, decisions du 2026-11-23).

Base : DB-IP Lite (pays et AS, licence CC BY 4.0 - « IP Geolocation by DB-IP », a citer), telechargee une fois
par mois. HAProxy ne charge PAS des plages CIDR (mesure du 2026-11-23 : 1,4 million de plages pays + 0,7 million
d'AS = +630 Mo de memoire) : omega-tail compacte la base en plages triees (debut, valeur) dans un fichier binaire
d'une quinzaine de Mo, ou le script Lua de la porte cherche par dichotomie.

Format de `geo.bin` (gros-boutiste) : MAGIC, puis 4 sections (pays IPv4, pays IPv6, AS IPv4, AS IPv6), chacune
« nombre (u32) » puis les enregistrements « debut (4 ou 16 octets) + valeur » ; valeur pays = 2 lettres
(« -- » : inconnu), valeur AS = u32 (0 : inconnu). Une adresse prend la valeur de la derniere plage qui commence
avant elle ; les trous de la base sont des plages « inconnu »."""
from __future__ import annotations

import re
from collections.abc import Iterable
from dataclasses import dataclass

from omega_tail.shared.i18n import N_

MAGIC = b"OMGEO001"
UNKNOWN_COUNTRY = "--"
ATTRIBUTION = "IP Geolocation by DB-IP (https://db-ip.com), CC BY 4.0"
REFRESH_DAYS = 30
_COUNTRY = re.compile(r"^[A-Z]{2}$")

HOSTING_ASNS: dict[int, str] = {
    16509: "Amazon AWS", 14618: "Amazon AWS", 8987: "Amazon AWS", 396982: "Google Cloud", 15169: "Google",
    19527: "Google", 8075: "Microsoft Azure", 8068: "Microsoft", 31898: "Oracle Cloud", 45102: "Alibaba Cloud",
    37963: "Alibaba Cloud", 132203: "Tencent Cloud", 45090: "Tencent Cloud", 16276: "OVHcloud", 24940: "Hetzner",
    213230: "Hetzner", 14061: "DigitalOcean", 63949: "Akamai Linode", 20473: "Vultr (Choopa)",
    51167: "Contabo", 12876: "Scaleway", 60781: "Leaseweb", 16265: "Leaseweb", 28753: "Leaseweb",
    9009: "M247", 36352: "ColoCrossing", 53667: "FranTech (BuyVM)", 46606: "Unified Layer", 26496: "GoDaddy",
    197540: "netcup", 62240: "Clouvider", 211252: "Delis", 40021: "Contabo US", 55286: "B2 Net Solutions",
    35916: "MultaCom", 49505: "Selectel", 50673: "Serverius", 202425: "IP Volume", 211298: "Driftnet",
    210644: "AEZA", 44477: "Stark Industries", 136907: "Huawei Cloud", 55990: "Huawei Cloud",
}
"""AS d'hebergeurs et de nuages connus (limites seulement en mode attaque, decision D). Liste modifiable dans le
Pare-feu ; les navigateurs des visiteurs passent par des fournisseurs d'acces, pas par ces AS."""

BROWSER_CIPHER_HASHES: dict[str, str] = {
    "8daaf6152771": N_("Chrome, Edge, Firefox récent"),
    "5b57614c22b0": N_("Firefox (ancien)"),
}
"""Partie b du JA4 (suites triees) des navigateurs courants, verifiee le 2026-11-23 (Chromium et Firefox reels a
travers la porte, exemple de reference de FoxIO) : jamais limites (decision D)."""


@dataclass(frozen=True)
class Range:
    start: int
    end: int
    value: str


def compact(ranges: Iterable[Range], gap: str, maximum: int = 2**128 - 1) -> list[tuple[int, str]]:
    """Plages triees -> debuts (debut, valeur) ; plages voisines de meme valeur fusionnees, trous en `gap`.
    `maximum` : derniere adresse de la famille (pas de plage « inconnu » au-dela)."""
    out: list[tuple[int, str]] = []
    expected = 0
    for item in sorted(ranges, key=lambda entry: entry.start):
        if item.end < item.start or item.end < expected:
            continue
        start = max(item.start, expected)
        if start > expected and (not out or out[-1][1] != gap):
            out.append((expected, gap))
        if not out or out[-1][1] != item.value:
            out.append((start, item.value))
        expected = item.end + 1
    if expected <= maximum and (not out or out[-1][1] != gap):
        out.append((expected, gap))
    return out


def lookup(records: list[tuple[int, str]], address: int) -> str:
    """Valeur de la derniere plage qui commence avant `address` (reference des tests du Lua)."""
    low, high = 0, len(records) - 1
    found = ""
    while low <= high:
        middle = (low + high) // 2
        if records[middle][0] <= address:
            found = records[middle][1]
            low = middle + 1
        else:
            high = middle - 1
    return found


def countries(text: str) -> tuple[str, ...]:
    """« fr, CN ru » -> (CN, FR, RU) ; tout ce qui n'est pas un code a 2 lettres est ignore."""
    found = {part.upper() for part in re.split(r"[\s,;]+", text) if part}
    return tuple(sorted(code for code in found if _COUNTRY.match(code) and code != UNKNOWN_COUNTRY))


def asn_numbers(text: str) -> tuple[int, ...]:
    """« AS16509, 24940 » -> (16509, 24940)."""
    found = set()
    for part in re.split(r"[\s,;]+", text):
        digits = part.upper().removeprefix("AS")
        if digits.isdigit() and 0 < int(digits) < 2**32:
            found.add(int(digits))
    return tuple(sorted(found))
