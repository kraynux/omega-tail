# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Le logo reprend ascii.txt caractere pour caractere ; seules les colonnes sont recalculees."""
from __future__ import annotations

from pathlib import Path

import pytest

from omega_tail.interfaces.tui.widgets.home_wordmark import LETTERS
from omega_tail.interfaces.tui.widgets.splash_hero import AXIS, WORDMARK_BOX, schema_lines, splash_content

# ascii.txt (dessin du logo) : a la racine du depot, ou dans le dossier de travail au-dessus (deplace le
# 2026-11-25) ; absent de l'archive publiee : le test est alors saute.
_SOURCES = [Path(__file__).resolve().parents[index] / "ascii.txt" for index in (1, 2)]
_FOUND = next((path for path in _SOURCES if path.exists()), None)
if _FOUND is None:
    pytest.skip("ascii.txt absent (archive publiée)", allow_module_level=True)
ASCII = _FOUND.read_text(encoding="utf-8")


def test_every_logo_line_is_in_ascii_txt() -> None:
    for line in WORDMARK_BOX:
        assert line in ASCII
    for line in LETTERS[0], LETTERS[2]:
        assert line.rstrip() in ASCII
    stripped = [line.replace("\t", " ").strip() for line in ASCII.splitlines()]
    for line in schema_lines():
        pieces = [piece for piece in line.split("  ") if piece.strip()]
        for piece in pieces:
            assert any(piece.strip() in source for source in stripped), piece


def test_schema_junctions_line_up() -> None:
    lines = schema_lines()
    serve_line = lines[2]
    monitor_left = lines[0].index("┌")
    assert serve_line.index("╣") == monitor_left  # SERVE ═════╣ colle au bord gauche de l'ecran
    assert serve_line.index("╠════╣") == lines[0].index("┐")  # bord droit de l'ecran vers FUNNEL
    assert lines[3].index("╦") == lines[4].index("║") == lines[5].index("╩")  # SERVE -> LAN
    assert lines[3].rindex("╦") == lines[4].rindex("║") == lines[5].rindex("╩")  # FUNNEL -> WEB
    assert monitor_left + 9 == AXIS


def test_every_block_is_centered_on_the_wordmark_axis() -> None:
    text = splash_content("0.1.0").plain.split("\n")
    for line in (text[1], text[3], text[-1]):
        body = line.strip()
        start = line.index(body)
        assert start + (len(body) - 1) // 2 in (AXIS, AXIS - 1)
    assert "░▒▓█V0.1.0█▓▒░" in text[3]
    assert max(len(line) for line in text) == 77
