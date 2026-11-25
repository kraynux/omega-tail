# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Journaux par source logique (« tailscaled », « porte ») : journalctl sous systemd, fichiers sous OpenRC et runit
(Alpine : /var/log/tailscaled.log ; Void : svlogd ou socklog ; sinon le journal general filtre). Sans sudo : un
fichier reserve a root est signale avec ce qu'il faut faire."""
from __future__ import annotations

import re
from collections import deque
from collections.abc import Mapping, Sequence
from datetime import date
from pathlib import Path

from omega_tail.core.constants import JOURNAL_MAX_BYTES, SEARCH_MAX_BYTES, SEARCH_TIMEOUT_SECONDS
from omega_tail.infrastructure.commands import run_quiet
from omega_tail.ports.readers import JournalResult
from omega_tail.shared.i18n import N_

# Raisons affichees (lot 9) : la phrase se traduit, le chemin apres « : » ou entre parentheses reste tel quel
READ_DENIED = N_("lecture refusée")
NO_JOURNAL = N_("aucun journal trouvé")
NO_RIGHTS_HINT = N_("Votre compte ne peut pas lire le journal du système. Ajoutez-le au groupe « systemd-journal » "
                    "(ou « adm » / « wheel » selon la distribution), puis rouvrez votre session.")
FILE_RIGHTS_HINT = N_("Ce journal est réservé à root sur cette machine : ajoutez votre compte au groupe qui peut le "
                      "lire (souvent « adm » ou « wheel »), ou lisez-le avec sudo.")


class Journalctl:
    def __init__(self, units: Mapping[str, str]) -> None:
        self._units = units

    def read(self, source: str, lines: int) -> JournalResult:
        unit = self._units.get(source, source)
        output = run_quiet(["journalctl", "-u", unit, "-n", str(lines), "--no-pager", "-o", "short-iso", "-q"],
                           timeout=20, limit=JOURNAL_MAX_BYTES)
        if output.code == 127:
            return JournalResult((), "journalctl: not found")
        found = tuple(line for line in output.stdout.splitlines() if line.strip())
        blocked = "insufficient permissions" in output.stderr or "not seeing messages" in output.stderr
        if not found and blocked:
            return JournalResult((), output.last_error, NO_RIGHTS_HINT)
        if output.code != 0 and not found:
            return JournalResult((), output.last_error)
        return JournalResult(found)

    def search(self, source: str, since: date, pattern: str) -> JournalResult:
        unit = self._units.get(source, source)
        base = ["journalctl", "-u", unit, "--since", f"{since.isoformat()} 00:00:00", "-r", "--no-pager", "-o", "cat",
                "-q"]
        output = run_quiet([*base, "-g", pattern], timeout=SEARCH_TIMEOUT_SECONDS, limit=SEARCH_MAX_BYTES)
        filtered = False
        if output.code != 0 and "pattern" in output.stderr.lower() and "support" in output.stderr.lower():
            # journalctl compile sans recherche : filtre ici (borne de taille identique)
            output = run_quiet(base, timeout=SEARCH_TIMEOUT_SECONDS, limit=SEARCH_MAX_BYTES)
            filtered = True
        if output.code == 127:
            return JournalResult((), "journalctl: not found")
        blocked = "insufficient permissions" in output.stderr or "not seeing messages" in output.stderr
        expression = re.compile(pattern)
        found = tuple(line for line in output.stdout.splitlines()
                      if line.strip() and (not filtered or expression.search(line)))
        if not found and blocked:
            return JournalResult((), output.last_error, NO_RIGHTS_HINT)
        if not found and not run_quiet(["journalctl", "-u", unit, "-n", "1", "--no-pager", "-o", "cat", "-q"],
                                       timeout=20).stdout.strip():
            # rien du tout pour ce service : sans le groupe du journal, journalctl ne le dit pas toujours
            return JournalResult((), N_("journal vide ou illisible pour ce compte"), NO_RIGHTS_HINT)
        # code 1 : aucune ligne trouvee (journalctl -g), ce n'est pas une erreur
        if output.code not in (0, 1) and not found:
            return JournalResult((), output.last_error)
        return JournalResult(found, truncated=len(output.stdout) >= SEARCH_MAX_BYTES - 1024)


def read_matching(path: Path, pattern: str) -> tuple[tuple[str, ...], bool]:
    """Lignes d'un fichier qui contiennent l'expression, les plus recentes d'abord (borne : SEARCH_MAX_BYTES lus a
    partir de la fin)."""
    expression = re.compile(pattern)
    with open(path, "rb") as handle:
        handle.seek(0, 2)
        size = handle.tell()
        handle.seek(max(0, size - SEARCH_MAX_BYTES))
        data = handle.read().decode("utf-8", errors="replace")
    lines = [line for line in data.splitlines() if expression.search(line)]
    return tuple(reversed(lines)), size > SEARCH_MAX_BYTES


def tail_lines(path: Path, lines: int, keyword: str = "") -> tuple[str, ...]:
    """Dernieres lignes d'un fichier, lu par la fin (borne : JOURNAL_MAX_BYTES)."""
    with open(path, "rb") as handle:
        handle.seek(0, 2)
        size = handle.tell()
        handle.seek(max(0, size - JOURNAL_MAX_BYTES))
        data = handle.read().decode("utf-8", errors="replace")
    kept: deque[str] = deque(maxlen=lines)
    for line in data.splitlines():
        if line.strip() and (not keyword or keyword in line):
            kept.append(line)
    return tuple(kept)


class FileJournal:
    """Sources -> fichiers candidats (chemin, mot a filtrer) ; le premier qui existe est lu."""

    def __init__(self, files: Mapping[str, Sequence[tuple[str, str]]]) -> None:
        self._files = files

    def read(self, source: str, lines: int) -> JournalResult:
        candidates = self._files.get(source, ())
        for path_text, keyword in candidates:
            path = Path(path_text)
            if not path.exists():
                continue
            try:
                return JournalResult(tail_lines(path, lines, keyword))
            except PermissionError:
                return JournalResult((), f"{READ_DENIED} : {path}", FILE_RIGHTS_HINT)
            except OSError as error:
                return JournalResult((), f"{path} : {error}")
        shown = ", ".join(path for path, _keyword in candidates) or "—"
        return JournalResult((), f"{NO_JOURNAL} ({shown})")

    def search(self, source: str, since: date, pattern: str) -> JournalResult:
        """Hors systemd : la date des lignes est relue par l'appelant (celle qu'ecrit HAProxy) ; `since` sert
        seulement sous journald."""
        del since
        for path_text, _keyword in self._files.get(source, ()):
            path = Path(path_text)
            if not path.exists():
                continue
            try:
                lines, truncated = read_matching(path, pattern)
            except PermissionError:
                return JournalResult((), f"{READ_DENIED} : {path}", FILE_RIGHTS_HINT)
            except OSError as error:
                return JournalResult((), f"{path} : {error}")
            return JournalResult(lines, truncated=truncated)
        return JournalResult((), NO_JOURNAL)


def journal_files(folder: str) -> dict[str, list[tuple[str, str]]]:
    """Ou chercher hors systemd. `folder` : dossier de la porte (journal ecrit par son service)."""
    return {
        "tailscaled": [("/var/log/tailscaled.log", ""), ("/var/log/tailscale.log", ""),
                       ("/var/log/tailscaled/current", ""), ("/var/log/socklog/everything/current", "tailscale"),
                       ("/var/log/messages", "tailscale"), ("/var/log/syslog", "tailscale")],
        "porte": [(f"{folder}/porte.log", ""), (f"{folder}/log/current", "")],
    }
