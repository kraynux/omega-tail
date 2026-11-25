# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Rapport (lot 7, proposition §4.4) : refus des derniers jours, lus dans le journal de la porte. Chaque connexion
y a une ligne (format `domain.groups.LOG_FORMAT`, regroupements appliques ou en observation) : « motif=… » dit
pourquoi la porte l'a refusee (ou l'aurait refusee en observation), « groupe=… » le regroupement qui l'a marquee.
La date est celle qu'HAProxy ecrit lui-meme ([23/Nov/2026:19:23:12.221]) : la meme sous journald et en fichier."""
from __future__ import annotations

import re
from collections import Counter
from collections.abc import Iterable
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta

REPORT_DAYS = 7
"""Periode des attaques du rapport (decision C du lot 7, comme les compteurs des regroupements)."""
TOP_ADDRESSES = 10
GATE_REASONS = ("liste-noire", "bloquee", "budget", "debit-adresse", "debit-prefixe", "pas-tls", "nom")
GROUP_REASONS = ("empreinte", "hebergeur", "pays")
SEARCH_PATTERN = "(motif|groupe)=[a-z]"
"""Lignes a garder (journalctl -g) : une connexion marquee par un motif ou un groupe."""

_MONTHS = {name: number for number, name in enumerate(
    ("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"), start=1)}
_LINE = re.compile(r"(\S+) \[(\d{2})/([A-Z][a-z]{2})/(\d{4}):[\d:.]+\] .*?\bmotif=(\S+) groupe=(\S+)"
                   r"(?: ja4=\S+ as=(\S+) pays=(\S+))?")


@dataclass(frozen=True)
class Marked:
    """Une connexion marquee dans le journal de la porte."""
    day: date
    address: str
    reason: str
    """Motif de la porte (lot 4) ou du regroupement ; vide si aucun."""
    group: str
    asn: str = ""
    country: str = ""


def _address(client: str) -> str:
    """« 1.2.3.4:5678 », « ::ffff:1.2.3.4:5678 », « 2001:db8::1:5678 » -> adresse sans port ni prefixe v4."""
    address = client.rpartition(":")[0] if ":" in client else client
    address = address.strip("[]")
    return address.removeprefix("::ffff:") if "." in address else address


def parse_line(line: str) -> Marked | None:
    found = _LINE.search(line)
    if not found:
        return None
    client, day, month, year, reason, group, asn, country = found.groups()
    if month not in _MONTHS:
        return None
    try:
        when = date(int(year), _MONTHS[month], int(day))
    except ValueError:
        return None
    reason, group = ("" if reason == "-" else reason), ("" if group == "-" else group)
    if not reason and not group:
        return None
    return Marked(when, _address(client), reason, group, "" if asn in (None, "-", "AS0") else asn,
                  "" if country in (None, "-", "--") else country)


@dataclass(frozen=True)
class Refusals:
    """Connexions marquees sur la periode (refusees, ou comptees en observation selon le mode)."""
    days: int = REPORT_DAYS
    by_reason: dict[str, int] = field(default_factory=dict)
    """Motif -> nombre (motifs de la porte, puis regroupements qui ont decide)."""
    by_day: dict[str, int] = field(default_factory=dict)
    """« 2026-11-23 » -> nombre, du plus ancien au plus recent."""
    addresses: tuple[tuple[str, int, str, str], ...] = ()
    """(adresse, nombre, AS, pays) des plus marquees."""
    groups: dict[str, int] = field(default_factory=dict)
    """Regroupement -> nombre (y compris en observation : « aurait refuse »)."""
    total: int = 0
    truncated: bool = False
    """Le journal etait trop gros pour etre lu en entier : les nombres sont des minimums."""
    error: str = ""
    hint: str = ""


def summarize(lines: Iterable[str], today: date, days: int = REPORT_DAYS, *, truncated: bool = False) -> Refusals:
    first = today - timedelta(days=days - 1)
    reasons: Counter[str] = Counter()
    per_day: Counter[str] = Counter()
    per_address: Counter[str] = Counter()
    groups: Counter[str] = Counter()
    where: dict[str, tuple[str, str]] = {}
    total = 0
    for line in lines:
        marked = parse_line(line)
        if marked is None or not first <= marked.day <= today:
            continue
        total += 1
        reason = marked.reason or ""
        if reason:
            reasons[reason] += 1
        if marked.group:
            groups[marked.group] += 1
        per_day[marked.day.isoformat()] += 1
        per_address[marked.address] += 1
        if marked.asn or marked.country:
            where[marked.address] = (marked.asn, marked.country)
    ordered = {key: reasons[key] for key in (*GATE_REASONS, *GROUP_REASONS) if reasons.get(key)}
    ordered.update({key: count for key, count in sorted(reasons.items()) if key not in ordered})
    top = tuple((address, count, *where.get(address, ("", ""))) for address, count in per_address.most_common(
        TOP_ADDRESSES))
    return Refusals(days=days, by_reason=ordered, by_day=dict(sorted(per_day.items())), addresses=top,
                    groups={key: groups[key] for key in GROUP_REASONS if groups.get(key)}, total=total,
                    truncated=truncated)


def report_stamp(moment: datetime) -> str:
    """Partie date du nom de fichier d'un rapport."""
    return moment.strftime("%Y%m%d-%H%M%S")
