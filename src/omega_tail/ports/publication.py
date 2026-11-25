# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Publication (lot 5) : sauvegardes de `serve status --json` (les memes que celles du disjoncteur et de la porte)."""
from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Protocol


class PublicationStore(Protocol):
    def save_publication(self, cut_id: str, config: Mapping[str, Any]) -> str: ...
    def load_publication(self, path: str) -> dict[str, Any]: ...
    def saves(self) -> list[str]:
        """De la plus ancienne a la plus recente."""
        ...
    def log(self, line: str) -> None: ...
