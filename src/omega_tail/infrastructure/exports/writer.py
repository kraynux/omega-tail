# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Exports dans le dossier des exports (Reglages ; `var/exports/` par defaut), comme le reste de la suite."""
from __future__ import annotations

from collections.abc import Callable
from pathlib import Path


class FileExportWriter:
    def __init__(self, directory: Path | Callable[[], Path]) -> None:
        self._directory = directory

    def save(self, name: str, content: str) -> str:
        if "/" in name or name.startswith("."):
            raise ValueError("export name must be a plain file name")
        directory = self._directory() if callable(self._directory) else self._directory
        directory.mkdir(parents=True, exist_ok=True)
        path = directory / name
        path.write_text(content, encoding="utf-8")
        return str(path)
