# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Compatibilite omega-connect (2026-11-25) : `omega-tail.sh synchro jeton` ecrit et affiche la carte d'identite."""
from __future__ import annotations

import json
import shutil
from pathlib import Path

import pytest

from omega_tail.app import main as app_main
from omega_tail.app.synchro_runner import run_synchro

ROOT = Path(__file__).resolve().parents[1]


def test_token_written_under_var_and_printed(tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
                                             capsys: pytest.CaptureFixture[str]) -> None:
    root = tmp_path / "omega-tail"
    root.mkdir()
    shutil.copy(ROOT / "pyproject.toml", root / "pyproject.toml")
    monkeypatch.setattr(app_main, "project_root", lambda: root)
    assert app_main.main(["synchro", "jeton", "--format", "json"]) == 0
    printed = json.loads(capsys.readouterr().out)
    saved = json.loads((root / "var" / "omega-jeton.json").read_text())
    assert printed == saved and saved["tool"] == "omega-tail" and saved["root"] == str(root)
    assert saved["version"] == app_main.__version__
    assert (root / "var" / "omega-jeton.json").stat().st_mode & 0o777 == 0o644


def test_unknown_synchro_command_is_refused(capsys: pytest.CaptureFixture[str]) -> None:
    assert run_synchro(["fiche"]) == 2 and "synchro jeton" in capsys.readouterr().err


def test_omega_lib_knows_omega_tail() -> None:
    from omega_lib.declaration.models import SOFTWARES
    from omega_lib.synchro.constants import TOOL_LAUNCHERS
    assert TOOL_LAUNCHERS["omega-tail"] == "omega-tail.sh" and "omega-tail" in SOFTWARES
    assert (ROOT / TOOL_LAUNCHERS["omega-tail"]).is_file()
