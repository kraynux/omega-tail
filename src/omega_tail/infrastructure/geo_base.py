# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Base AS / pays de la porte (domain/geo.py) : telechargement de DB-IP Lite (sans compte), construction de
`geo.bin` (plages compactees lues par le Lua de la porte) et des noms d'AS, lecture cote Python."""
from __future__ import annotations

import csv
import gzip
import io
import ipaddress
import os
import struct
import urllib.request
from collections.abc import Iterator
from datetime import date
from pathlib import Path

from omega_tail.domain.geo import MAGIC, UNKNOWN_COUNTRY, Range, compact
from omega_tail.domain.groups import GEO_FILE, GEO_SCRIPT, JA4_SCRIPT, NAMES_FILE
from omega_tail.shared.i18n import N_

URL = "https://download.db-ip.com/free/dbip-{kind}-lite-{month}.csv.gz"

# Raisons affichees (lot 9) : la phrase se traduit, le detail apres « : » garde sa forme
DOWNLOAD_TOO_BIG = N_("fichier trop gros")
DOWNLOAD_FAILED = N_("téléchargement impossible")
USER_AGENT = "omega-tail"
MAX_DOWNLOAD = 64 * 1024 * 1024
MIN_ROWS = 100_000
"""Moins de lignes : fichier tronque ou page d'erreur ; l'ancienne base est gardee."""


def months(today: date) -> tuple[str, str]:
    previous = date(today.year - 1, 12, 1) if today.month == 1 else date(today.year, today.month - 1, 1)
    return today.strftime("%Y-%m"), previous.strftime("%Y-%m")


def download(kind: str, folder: Path, today: date) -> Path:
    """Fichier du mois (ou du mois precedent, publie en debut de mois) ; leve OSError en cas d'echec."""
    error: Exception | None = None
    for month in months(today):
        request = urllib.request.Request(URL.format(kind=kind, month=month), headers={"User-Agent": USER_AGENT})
        try:
            with urllib.request.urlopen(request, timeout=120) as answer:  # noqa: S310 - adresse fixe en https
                data = answer.read(MAX_DOWNLOAD + 1)
        except OSError as failure:
            error = failure
            continue
        if len(data) > MAX_DOWNLOAD:
            raise OSError(f"{DOWNLOAD_TOO_BIG} : {kind}")
        target = folder / f"dbip-{kind}-lite.csv.gz"
        target.write_bytes(data)
        return target
    raise OSError(f"{DOWNLOAD_FAILED} : {kind} ({error})")


def _rows(path: Path) -> Iterator[list[str]]:
    with gzip.open(path, "rt", encoding="utf-8", newline="") as handle:
        yield from csv.reader(handle)


def _ranges(path: Path, value_column: int, names: dict[int, str] | None = None) -> tuple[list[Range], list[Range]]:
    v4: list[Range] = []
    v6: list[Range] = []
    for row in _rows(path):
        if len(row) <= value_column:
            continue
        try:
            first, last = ipaddress.ip_address(row[0]), ipaddress.ip_address(row[1])
        except ValueError:
            continue
        value = row[value_column].strip()
        if names is not None and value.isdigit() and len(row) > value_column + 1:
            names.setdefault(int(value), row[value_column + 1].strip())
        (v4 if first.version == 4 else v6).append(Range(int(first), int(last), value))
    return v4, v6


def _country(value: str) -> str:
    return value if len(value) == 2 and value.isalpha() and value != "ZZ" else UNKNOWN_COUNTRY


def build(country_gz: Path, asn_gz: Path, out: Path, names_out: Path, *, min_rows: int = MIN_ROWS) -> tuple[int, int]:
    """Ecrit geo.bin et les noms d'AS (atomiquement) ; renvoie (plages pays, plages AS) apres compactage."""
    names: dict[int, str] = {}
    c4, c6 = _ranges(country_gz, 2)
    a4, a6 = _ranges(asn_gz, 2, names)
    if len(c4) + len(c6) < min_rows or len(a4) + len(a6) < min_rows:
        raise OSError(N_("base incomplète (trop peu de plages) : ancienne base gardée"))
    sections = []
    counts = [0, 0]
    for index, (ranges, size, kind) in enumerate(((c4, 4, "pays"), (c6, 16, "pays"), (a4, 4, "as"), (a6, 16, "as"))):
        if kind == "pays":
            records = compact((Range(r.start, r.end, _country(r.value)) for r in ranges), UNKNOWN_COUNTRY,
                              2 ** (size * 8) - 1)
            body = b"".join(start.to_bytes(size, "big") + value.encode("ascii") for start, value in records)
        else:
            records = compact((Range(r.start, r.end, r.value if r.value.isdigit() else "0") for r in ranges), "0",
                              2 ** (size * 8) - 1)
            body = b"".join(start.to_bytes(size, "big") + struct.pack(">I", int(value)) for start, value in records)
        counts[index // 2] += len(records)
        sections.append(struct.pack(">I", len(records)) + body)
    temporary = out.with_suffix(".tmp")
    temporary.write_bytes(MAGIC + b"".join(sections))
    os.replace(temporary, out)
    text = io.StringIO()
    for number in sorted(names):
        text.write(f"{number}\t{names[number].replace(chr(9), ' ')}\n")
    temporary_names = names_out.with_suffix(".tmp")
    temporary_names.write_text(text.getvalue(), encoding="utf-8")
    os.replace(temporary_names, names_out)
    return counts[0], counts[1]


class GeoReader:
    """Lecture de geo.bin cote Python (Attaques et decisions) ; meme recherche que le Lua de la porte, directement
    dans les octets du fichier (2026-11-25, MESURES_DEBIT_MEMOIRE.md : 1,35 million de tuples Python prenaient
    ~207 Mo et 20 s de chargement dans la TUI ; les octets prennent la taille du fichier, ~15 Mo, sans attente)."""

    def __init__(self, path: Path) -> None:
        self._data = b""
        self._sections: list[tuple[int, int, int, int]] = []
        """(debut des enregistrements, nombre, taille de la cle, largeur de la valeur) : pays v4, pays v6, AS v4,
        AS v6."""
        try:
            data = path.read_bytes()
        except OSError:
            return
        if not data.startswith(MAGIC):
            return
        at = len(MAGIC)
        sections = []
        for size, width in ((4, 2), (16, 2), (4, 4), (16, 4)):
            if at + 4 > len(data):
                return
            count = struct.unpack_from(">I", data, at)[0]
            at += 4
            end = at + count * (size + width)
            if end > len(data):
                return  # fichier tronque : rien plutot qu'une reponse fausse
            sections.append((at, count, size, width))
            at = end
        self._data, self._sections = data, sections

    def _find(self, section: int, address: int) -> str:
        """Valeur de la derniere plage qui commence avant `address` (meme regle que domain.geo.lookup)."""
        start, count, size, width = self._sections[section]
        step, data = size + width, self._data
        low, high, found = 0, count - 1, -1
        while low <= high:
            middle = (low + high) // 2
            offset = start + middle * step
            if int.from_bytes(data[offset:offset + size], "big") <= address:
                found, low = offset, middle + 1
            else:
                high = middle - 1
        if found < 0:
            return ""
        raw = data[found + size:found + step]
        return raw.decode("ascii") if width == 2 else str(int.from_bytes(raw, "big"))

    @property
    def ready(self) -> bool:
        return len(self._sections) == 4

    def lookup(self, address: str) -> tuple[str, int]:
        """(pays, AS) d'une adresse ; (« -- », 0) si inconnue."""
        if not self.ready:
            return UNKNOWN_COUNTRY, 0
        try:
            ip = ipaddress.ip_address(address)
        except ValueError:
            return UNKNOWN_COUNTRY, 0
        if ip.version == 6 and ip.ipv4_mapped is not None:
            ip = ip.ipv4_mapped
        offset = 0 if ip.version == 4 else 1
        country = self._find(offset, int(ip)) or UNKNOWN_COUNTRY
        asn = self._find(2 + offset, int(ip))
        return country, int(asn) if asn.isdigit() else 0


def read_names(path: Path) -> dict[int, str]:
    names: dict[int, str] = {}
    try:
        for line in path.read_text(encoding="utf-8").splitlines():
            number, _sep, name = line.partition("\t")
            if number.isdigit():
                names[int(number)] = name
    except OSError:
        pass
    return names


class DbIpSource:
    """Port GeoSource : DB-IP Lite telechargee dans le dossier de la porte ; lecture gardee en cache tant que
    geo.bin ne change pas."""

    def __init__(self) -> None:
        self._reader: tuple[float, GeoReader] | None = None
        self._names: tuple[float, dict[int, str]] | None = None

    def refresh(self, folder: Path, today: date) -> tuple[int, int]:
        work = folder / "base-telechargee"
        work.mkdir(parents=True, exist_ok=True)
        try:
            country = download("country", work, today)
            asn = download("asn", work, today)
            return build(country, asn, folder / GEO_FILE, folder / NAMES_FILE)
        finally:
            for path in work.glob("*"):
                path.unlink(missing_ok=True)
            work.rmdir()

    def _current(self, folder: Path) -> GeoReader:
        path = folder / GEO_FILE
        try:
            stamp = path.stat().st_mtime
        except OSError:
            stamp = 0.0
        if self._reader is None or self._reader[0] != stamp:
            self._reader = (stamp, GeoReader(path))
        return self._reader[1]

    def lookup(self, folder: Path, address: str) -> tuple[str, int]:
        return self._current(folder).lookup(address)

    def names(self, folder: Path) -> dict[int, str]:
        path = folder / NAMES_FILE
        try:
            stamp = path.stat().st_mtime
        except OSError:
            return {}
        if self._names is None or self._names[0] != stamp:
            self._names = (stamp, read_names(path))
        return self._names[1]


def lua_scripts() -> dict[str, str]:
    """Scripts Lua de la porte (livres avec omega-tail), copies dans son dossier a chaque preparation."""
    folder = Path(__file__).parent / "lua"
    return {name: (folder / name).read_text(encoding="utf-8") for name in (JA4_SCRIPT, GEO_SCRIPT)}
