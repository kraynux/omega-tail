# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Interface en 17 langues (lot 9, 2026-11-25) : catalogues complets et sans variable perdue, catalogue de
reference a jour du code, ecrans ouverts dans d'autres langues sans erreur."""
from __future__ import annotations

import ast
import os
import re
import string
from pathlib import Path

import pytest
from funnel_sim import FunnelSim
from test_gate import PRODUCTION
from test_tui import gate_app, settle

from omega_tail.interfaces.tui.menu import MENU
from omega_tail.shared.i18n import LANGUAGE

SRC = Path(__file__).resolve().parents[1] / "src" / "omega_tail"
LOCALE = SRC / "locale"
LANGUAGES = ("en", "es", "pt_BR", "it", "de", "nl", "pl", "ru", "zh_CN", "vi", "id", "ja", "ko", "th", "hi", "ar")
SHARED_POT = Path(__import__("omega_lib").__file__).resolve().parent / "locale" / "omega-lib.pot"
MARKERS = {"_": 0, "N_": 0, "ngettext": 0, "lazy": 0, "Outcome": 1, "_list_outcome": 0, "_apply": 3}


def _unquote(text: str) -> str:
    return ast.literal_eval(text)


def read_po(path: Path) -> dict[str, str]:
    """msgid -> msgstr (lecteur minimal : chaines sur plusieurs lignes, pas de pluriels dans omega-tail)."""
    entries: dict[str, str] = {}
    msgid = msgstr = None
    current = ""
    for line in [*path.read_text(encoding="utf-8").splitlines(), ""]:
        if line.startswith("msgid "):
            if msgid is not None and msgid != "":
                entries[msgid] = msgstr or ""
            msgid, msgstr, current = _unquote(line[6:]), None, "id"
        elif line.startswith("msgstr "):
            msgstr, current = _unquote(line[7:]), "str"
        elif line.startswith('"'):
            if current == "id" and msgid is not None:
                msgid += _unquote(line)
            elif current == "str" and msgstr is not None:
                msgstr += _unquote(line)
        elif not line.strip() and msgid:
            entries[msgid] = msgstr or ""
            msgid = None
    return entries


def fields(text: str) -> tuple[set[str], int, int]:
    names = {name for _lit, name, _spec, _conv in string.Formatter().parse(text) if name is not None}
    return names, text.count("[b]"), text.count("[/b]")


def test_every_language_is_complete_and_keeps_its_variables() -> None:
    reference = read_po(LOCALE / "omega-tail.pot")
    for language in LANGUAGES:
        catalog = read_po(LOCALE / language / "LC_MESSAGES" / "omega-tail.po")
        assert set(catalog) == set(reference), language
        empty = [msgid for msgid, msgstr in catalog.items() if not msgstr.strip()]
        assert not empty, (language, empty[:3])
        broken = [msgid for msgid, msgstr in catalog.items() if fields(msgid) != fields(msgstr)]
        assert not broken, (language, broken[:3])
        assert (LOCALE / language / "LC_MESSAGES" / "omega-tail.mo").exists(), language
        header = (LOCALE / language / "LC_MESSAGES" / "omega-tail.po").read_text(encoding="utf-8")[:4000]
        assert "X-Omega-Status: validated" in header, f"{language} : statut « validé » perdu (2026-11-25)"


def marked_strings() -> set[str]:
    found: set[str] = set()
    for path in SRC.rglob("*.py"):
        for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
            if not isinstance(node, ast.Call):
                continue
            name = getattr(node.func, "id", None) or getattr(node.func, "attr", None)
            if name not in MARKERS or len(node.args) <= MARKERS[name]:
                continue
            argument = node.args[MARKERS[name]]
            if isinstance(argument, ast.Constant) and isinstance(argument.value, str):
                found.add(argument.value)
    return found


def test_reference_catalog_is_up_to_date_with_the_code() -> None:
    """Une phrase ajoutee au code sans relancer l'extraction (tail_catalog.py extract) resterait en francais."""
    known = set(read_po(LOCALE / "omega-tail.pot"))
    if SHARED_POT.exists():
        known |= set(read_po(SHARED_POT))
    missing = sorted(text for text in marked_strings() - known if re.search(r"[A-Za-zÀ-ÿ]", text))
    assert not missing, missing[:5]


@pytest.mark.parametrize("language", ["de", "ja", "ar"])
async def test_every_screen_opens_in_another_language(tmp_path: Path, language: str) -> None:
    LANGUAGE.install(settings_store=None, environ={"OMEGA_TAIL_LANG": language})
    try:
        app = gate_app(tmp_path, FunnelSim(PRODUCTION))
        opened = 0
        async with app.run_test(size=(140, 50)) as pilot:
            await settle(pilot)
            for item in MENU:
                if item.key in ("settings", "help"):
                    continue
                depth = len(app.screen_stack)
                app.open_key(item.key)
                await settle(pilot)
                opened += len(app.screen_stack) > depth
                if len(app.screen_stack) > depth:
                    app.pop_screen()
                    await settle(pilot)
        from omega_tail.shared.i18n import _

        assert _("Tableau de bord") != "Tableau de bord" and opened >= 6
    finally:
        LANGUAGE.install(settings_store=None, environ={"OMEGA_TAIL_LANG": "fr"})
        os.environ.pop("OMEGA_TAIL_LANG", None)
