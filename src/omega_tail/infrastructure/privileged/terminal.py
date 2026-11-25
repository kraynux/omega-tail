# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Seul module qui lance une commande sur le VRAI terminal (invite sudo comprise), pendant que l'interface est mise
de cote (`suspended` de l'ecran de base). Jamais de shell, jamais de mot de passe garde."""
from __future__ import annotations

import os
import subprocess
from collections.abc import Sequence


def running_as_root() -> bool:
    return hasattr(os, "geteuid") and os.geteuid() == 0


def run_attached(argv: Sequence[str]) -> int:
    try:
        return subprocess.run(list(argv), check=False).returncode  # noqa: S603 - commande montree avant
    except OSError:
        return 127
