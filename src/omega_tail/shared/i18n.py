# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Traduction de l'interface - seul point d'acces aux phrases traduites d'omega-tail (meme interface
que omega_stress/shared/i18n.py).

    from omega_tail.shared.i18n import _, N_, ngettext

Le francais est la langue de reference ; les 16 autres langues arrivent au lot 9
(PROPOSITION_MENU_FONCTIONS.md §7). Catalogues : locale/<langue>/LC_MESSAGES/omega-tail.mo, chaines au catalogue
partage omega-lib."""
from __future__ import annotations

from contextlib import AbstractContextManager
from pathlib import Path
from typing import Any

from omega_lib.i18n.service import mark
from omega_lib.i18n.translator import ToolTranslator
from omega_lib.infrastructure.i18n.tool_language import ToolLanguage

DOMAIN = "omega-tail"
TRANSLATOR = ToolTranslator(DOMAIN)
STATE = TRANSLATOR.state
LANGUAGE = ToolLanguage(TRANSLATOR, Path(__file__).resolve().parents[1] / "locale", "OMEGA_TAIL_LANG")

N_ = mark
lazy = TRANSLATOR.lazy


def _(message: str) -> str:
    return TRANSLATOR.gettext(message)


def ngettext(singular: str, plural: str, n: int) -> str:
    return TRANSLATOR.ngettext(singular, plural, n)


def exporting(settings_store: Any) -> AbstractContextManager[None]:
    """Le temps du bloc, `_()` repond dans la langue des exports (reglage « Langue des exports » ; « Comme
    l'interface » par defaut). Lot 9, 2026-11-25."""
    return TRANSLATOR.translating_as(LANGUAGE.export_state(settings_store))
