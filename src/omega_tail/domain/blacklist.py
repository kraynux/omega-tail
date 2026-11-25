# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Liste noire de la porte (finitions 0.7.0, decisions 2026-11-24) : chaque entree garde sa date d'ajout
et son origine (`noire.json`), le fichier lu par HAProxy (`noire.lst`) n'en est que la liste des adresses.

Plafond 50 000 entrees (alerte a 25 000) : HAProxy en tiendrait bien plus, c'est omega-tail qui ralentirait (fichier
reecrit, liste relue par l'ecran). Import : une adresse ou un reseau par ligne, `#` = commentaire, doublons et
adresses du tailnet ecartes et comptes. Purges comme pour les journaux : par anciennete, les N plus anciennes, une
plage de lignes, une origine, ou tout."""
from __future__ import annotations

import ipaddress
import re
from collections.abc import Callable, Iterable
from dataclasses import dataclass
from datetime import datetime, timedelta

from omega_tail.shared.i18n import N_

BLACKLIST_MAX = 50_000
BLACKLIST_WARNING = 25_000

ORIGIN_SCREEN = "ecran"
ORIGIN_MANUAL = "manuel"
ORIGIN_IMPORT = "import"
ORIGIN_EXISTING = "existant"
ORIGIN_LABELS = {ORIGIN_SCREEN: N_("écran Attaques"), ORIGIN_MANUAL: N_("ajout manuel"), ORIGIN_IMPORT: N_("import"),
                 ORIGIN_EXISTING: N_("avant les dates")}

PURGE_OLDER = "anciennes"
PURGE_OLDEST = "premieres"
PURGE_RANGE = "plage"
PURGE_ORIGIN = "origine"
PURGE_ALL = "tout"

_CANONICAL = re.compile(r"[0-9a-f.:]+(/[0-9]{1,3})?")


@dataclass(frozen=True)
class BlackEntry:
    address: str
    added: datetime
    origin: str = ORIGIN_SCREEN


@dataclass(frozen=True)
class ImportReport:
    added: tuple[BlackEntry, ...] = ()
    duplicates: int = 0
    tailnet: int = 0
    over_limit: int = 0
    invalid: tuple[tuple[int, str], ...] = ()
    """(numero de ligne, texte) des lignes ecartees."""


@dataclass(frozen=True)
class PurgeChoice:
    mode: str
    days: int = 0
    count: int = 0
    first: int = 0
    last: int = 0
    origin: str = ""


def normalize(text: str) -> str:
    """Adresse ou reseau sous forme canonique (192.0.2.0/24, 2001:db8::/32) ; ValueError sinon. Une adresse seule
    reste sans /32 ou /128, comme HAProxy l'ecrit."""
    text = text.strip()
    if "/" in text:
        network = ipaddress.ip_network(text, strict=False)
        result = str(network.network_address) if network.prefixlen == network.max_prefixlen else str(network)
    else:
        result = str(ipaddress.ip_address(text))
    if not is_canonical(result):
        raise ValueError(f"adresse refusee : {text!r}")
    return result


def is_canonical(entry: str) -> bool:
    """Chiffres, points, deux-points et un prefixe, rien d'autre : seule forme qui part vers HAProxy (fichiers et
    socket d'administration). Scan de securite 2026-11-25, F3 : Python accepte un identifiant de zone IPv6
    (« fe80::1%x;shutdown frontend porte ») et le rend tel quel ; le « ; » enchainait une seconde commande."""
    return _CANONICAL.fullmatch(entry) is not None


def covered(address: str, entries: Iterable[str]) -> bool:
    """Deja dans la liste, ou contenue dans un reseau de la liste."""
    try:
        target = ipaddress.ip_network(address, strict=False)
    except ValueError:
        return False
    for entry in entries:
        try:
            network = ipaddress.ip_network(entry, strict=False)
        except ValueError:
            continue
        if network.version == target.version and target.subnet_of(network):  # type: ignore[arg-type]
            return True
    return False


def parse_import(text: str, existing: Iterable[str], *, now: datetime, room: int,
                 in_tailnet: Callable[[str], bool]) -> ImportReport:
    """Fichier TXT -> entrees nouvelles. `room` : places restantes sous le plafond. `in_tailnet` : fonction
    adresse -> bool (passee par l'application, pour ne pas dupliquer la liste des reseaux)."""
    known = set(existing)
    networks = [entry for entry in known if "/" in entry]
    added: list[BlackEntry] = []
    invalid: list[tuple[int, str]] = []
    duplicates = tailnet = over = 0
    for number, raw in enumerate(text.splitlines(), start=1):
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        try:
            address = normalize(line)
        except ValueError:
            invalid.append((number, raw.strip()[:80]))
            continue
        if in_tailnet(address):
            tailnet += 1
            continue
        if address in known or covered(address, networks):
            duplicates += 1
            continue
        if len(added) >= room:
            over += 1
            continue
        known.add(address)
        if "/" in address:
            networks.append(address)
        added.append(BlackEntry(address, now, ORIGIN_IMPORT))
    return ImportReport(tuple(added), duplicates, tailnet, over, tuple(invalid))


def ordered(entries: Iterable[BlackEntry]) -> list[BlackEntry]:
    """Ordre d'affichage et des plages : la plus ancienne d'abord."""
    return sorted(entries, key=lambda entry: (entry.added, entry.address))


def select_purge(entries: list[BlackEntry], choice: PurgeChoice, now: datetime) -> list[BlackEntry]:
    """Entrees que la purge retirerait (apercu, puis purge). `entries` dans l'ordre de `ordered`."""
    if choice.mode == PURGE_ALL:
        return list(entries)
    if choice.mode == PURGE_OLDER:
        limit = now - timedelta(days=max(0, choice.days))
        return [entry for entry in entries if entry.added < limit]
    if choice.mode == PURGE_OLDEST:
        return list(entries[:max(0, choice.count)])
    if choice.mode == PURGE_RANGE:
        first, last = sorted((max(1, choice.first), max(1, choice.last)))
        return list(entries[first - 1:last])
    if choice.mode == PURGE_ORIGIN:
        return [entry for entry in entries if entry.origin == choice.origin]
    return []


def export_text(entries: Iterable[BlackEntry]) -> str:
    """Reimportable tel quel : la date et l'origine en commentaire."""
    lines = ["# omega-tail : liste noire de la porte (une adresse ou un réseau par ligne, # = commentaire)"]
    lines += [f"{entry.address}  # {entry.added.strftime('%Y-%m-%d %H:%M')} {entry.origin}" for entry in entries]
    return "\n".join(lines) + "\n"
