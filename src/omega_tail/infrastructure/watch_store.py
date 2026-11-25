# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Etat de la veille sous `var/veille/` (etat.json, journal.log, fichiers de service). Ecritures atomiques."""
from __future__ import annotations

import json
from dataclasses import asdict
from datetime import datetime
from pathlib import Path

from omega_tail.domain.watch import WatchState
from omega_tail.infrastructure.survival_store import _write

KEEP_LOG_BYTES = 512 * 1024
"""Journal tourne au-dela (l'ancien est garde une fois, en .1)."""


class FileWatchStore:
    def __init__(self, var: Path) -> None:
        self._folder = var / "veille"

    @property
    def folder(self) -> str:
        return str(self._folder)

    def load(self) -> WatchState:
        try:
            data = json.loads((self._folder / "etat.json").read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return WatchState()
        if not isinstance(data, dict):
            return WatchState()
        try:
            return WatchState(strikes=tuple(float(at) for at in data.get("strikes", ())),
                              level=int(data.get("level", 0)), last_end=float(data.get("last_end", 0.0)),
                              calm_until=float(data.get("calm_until", 0.0)),
                              heartbeat=float(data.get("heartbeat", 0.0)), installed=bool(data.get("installed")))
        except (TypeError, ValueError):
            return WatchState()

    def save(self, state: WatchState) -> None:
        data = asdict(state)
        data["strikes"] = list(state.strikes)
        _write(self._folder / "etat.json", json.dumps(data, indent=2) + "\n")

    def log(self, line: str) -> None:
        self._folder.mkdir(parents=True, exist_ok=True)
        path = self._folder / "journal.log"
        if path.exists() and path.stat().st_size > KEEP_LOG_BYTES:
            path.replace(path.with_suffix(".log.1"))
        with open(path, "a", encoding="utf-8") as handle:
            handle.write(f"{datetime.now().astimezone().isoformat(timespec='seconds')} {line}\n")

    def last_lines(self, count: int) -> list[str]:
        try:
            lines = (self._folder / "journal.log").read_text(encoding="utf-8").splitlines()
        except OSError:
            return []
        return lines[-count:]

    def write_file(self, name: str, text: str) -> str:
        if "/" in name or name.startswith("."):
            raise ValueError("plain file name expected")
        path = self._folder / name
        _write(path, text, 0o644)
        return str(path)
