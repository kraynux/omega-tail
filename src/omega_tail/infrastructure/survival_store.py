# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Etat du disjoncteur sous `var/funnel/` (etat.json, sauvegardes/, journal.log) et fichiers d'ajout a installer
sous `var/survie/`. Ecritures atomiques ; rien n'est jamais supprime sauf l'etat de la coupure levee. Les sauvegardes
de publication les plus anciennes sont gardees (au plus 50, les plus vieilles partent)."""
from __future__ import annotations

import json
import os
import tempfile
from collections.abc import Mapping
from datetime import datetime
from pathlib import Path
from typing import Any

from omega_tail.domain.funnel import Cut

KEEP_SAVES = 50


def _write(path: Path, text: str, mode: int = 0o644) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(dir=path.parent, prefix=".tmp-")
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            handle.write(text)
        os.chmod(temporary, mode)
        os.replace(temporary, path)
    except OSError:
        Path(temporary).unlink(missing_ok=True)
        raise


class FileCutStore:
    def __init__(self, var: Path) -> None:
        self._funnel = var / "funnel"
        self._survival = var / "survie"

    @property
    def state_file(self) -> Path:
        return self._funnel / "etat.json"

    def current(self) -> Cut | None:
        try:
            data = json.loads(self.state_file.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return None
        if not isinstance(data, dict) or not data.get("cut_id"):
            return None
        ports = tuple(int(port) for port in data.get("ports", ()) if str(port).isdigit())
        return Cut(str(data["cut_id"]), str(data.get("cut_at", "")), str(data.get("until", "")),
                   str(data.get("saved", "")), ports)

    def save_publication(self, cut_id: str, config: Mapping[str, Any]) -> str:
        folder = self._funnel / "sauvegardes"
        path = folder / f"funnel-{cut_id}.json"
        _write(path, json.dumps(config, indent=2, ensure_ascii=False) + "\n", 0o600)
        saves = sorted(folder.glob("funnel-*.json"))
        for old in saves[:-KEEP_SAVES]:
            old.unlink(missing_ok=True)
        return str(path)

    def saves(self) -> list[str]:
        """Sauvegardes de la publication, de la plus ancienne a la plus recente."""
        folder = self._funnel / "sauvegardes"
        return [str(path) for path in sorted(folder.glob("funnel-*.json"), key=lambda item: item.stat().st_mtime)]

    def load_publication(self, path: str) -> dict[str, Any]:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}

    def start(self, cut: Cut) -> None:
        _write(self.state_file, json.dumps({"cut_id": cut.cut_id, "cut_at": cut.cut_at, "until": cut.until,
                                            "saved": cut.saved, "ports": list(cut.ports)}, indent=2) + "\n")

    def finish(self) -> None:
        self.state_file.unlink(missing_ok=True)

    def log(self, line: str) -> None:
        self._funnel.mkdir(parents=True, exist_ok=True)
        with open(self._funnel / "journal.log", "a", encoding="utf-8") as handle:
            handle.write(f"{datetime.now().astimezone().isoformat(timespec='seconds')} {line}\n")

    def write_private(self, name: str, text: str) -> str:
        if "/" in name or name.startswith("."):
            raise ValueError("plain file name expected")
        path = self._survival / name
        _write(path, text, 0o644)
        return str(path)
