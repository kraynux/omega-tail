# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Seul endroit (avec infrastructure.privileged) ou omega-tail lance une commande (contrat import-linter).
Commandes de LECTURE lancees pendant que l'interface tourne : sans terminal (nouvelle session, entree fermee),
jamais d'invite sudo par-dessus l'interface (correctif de la suite, ~/DEV/OMEGA_A_FAIRE_SUDO_TUI.md), duree bornee."""
from __future__ import annotations

import os
import subprocess
from collections.abc import Sequence
from dataclasses import dataclass

from omega_tail.core.constants import COMMAND_TIMEOUT_SECONDS


@dataclass(frozen=True)
class Output:
    code: int
    stdout: str
    stderr: str

    @property
    def last_error(self) -> str:
        lines = [line.strip() for line in self.stderr.splitlines() if line.strip()]
        return lines[-1] if lines else ""


def run_quiet(argv: Sequence[str], *, timeout: float = COMMAND_TIMEOUT_SECONDS, limit: int = 0) -> Output:
    """Code 127 : commande absente ; 124 : trop longue. `limit` borne la sortie lue (octets, 0 : sans borne)."""
    env = dict(os.environ, LC_ALL="C", LANG="C")
    try:
        done = subprocess.run(list(argv), capture_output=True, stdin=subprocess.DEVNULL,  # noqa: S603
                              start_new_session=True, timeout=timeout, check=False, env=env)
    except FileNotFoundError:
        return Output(127, "", f"{argv[0]}: not found")
    except subprocess.TimeoutExpired:
        return Output(124, "", f"{argv[0]}: timeout")
    except OSError as error:
        return Output(126, "", str(error))
    stdout = done.stdout[:limit] if limit else done.stdout
    return Output(done.returncode, stdout.decode("utf-8", errors="replace"),
                  done.stderr.decode("utf-8", errors="replace"))


def quiet_command(argv: Sequence[str]) -> tuple[int, str]:
    """Port QuietCommand : code et derniere ligne d'erreur."""
    output = run_quiet(argv)
    return output.code, output.last_error


def run_with_input(argv: Sequence[str], data: bytes, *, timeout: float = 10) -> tuple[int, str]:
    """Commande qui lit `data` sur son entree (ex. `crontab -`) ; (code, erreur). Code 124 : trop longue."""
    try:
        done = subprocess.run(list(argv), input=data, capture_output=True, timeout=timeout,  # noqa: S603
                              check=False, start_new_session=True)
    except subprocess.TimeoutExpired:
        return 124, f"{argv[0]}: timeout"
    except OSError as error:
        return 126, str(error)
    return done.returncode, done.stderr.decode(errors="replace").strip()


def spawn_detached(argv: Sequence[str]) -> int:
    """Processus detache sous le compte de l'utilisateur (remise en route programmee hors systemd)."""
    try:
        subprocess.Popen(list(argv), stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,  # noqa: S603
                         stderr=subprocess.DEVNULL, start_new_session=True)
    except OSError:
        return 127
    return 0


def run_tool(argv: Sequence[str], *, timeout: float = 900) -> tuple[int, str]:
    """Commande longue d'omega-tail lui-meme dans un processus a part (mise a jour de la base AS / pays) : l'ecran
    reste fluide pendant le calcul. (code, derniere ligne ecrite). Code 124 : trop longue."""
    try:
        done = subprocess.run(list(argv), capture_output=True, stdin=subprocess.DEVNULL,  # noqa: S603
                              start_new_session=True, timeout=timeout, check=False)
    except subprocess.TimeoutExpired:
        return 124, f"{argv[0]}: timeout"
    except OSError as error:
        return 126, str(error)
    text = (done.stdout or done.stderr).decode("utf-8", errors="replace")
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return done.returncode, lines[-1] if lines else ""
