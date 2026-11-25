# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Bandeau OMEGA-TAIL en haut du menu principal (« MENU GENERAL » d'ascii.txt, une seule ligne de texte, 73
colonnes : tient dans un terminal de 80). Couleurs : ligne 1 vif, ligne 2 clair, ligne 3 vif. Le trait d'union de
la ligne 2 est « ═ », comme sur l'ecran de demarrage (« = » dans la variante du menu d'ascii.txt, pris pour une
faute de frappe)."""
from __future__ import annotations

from textual.content import Content, Span
from textual.widgets import Static

LETTERS = (
    "┌╦═══╦┐ ┌╦═╦═╦┐ ┌╦═══╦┐ ┌╦═══╦┐ ┌╦═══╦┐   ┌═╤╦╤═┐ ┌╦═══╦┐ ┌═╤╦╤═┐ ┌╦     ",
    "│║   ║│ │║ ║ ║│ ├╬══    │║  ═╦┐ ├╬═══╬┤ ═   │║│   ├╬═══╬┤   │║│   │║     ",
    "└╩═══╩┘ └╩   ╩┘ └╩═══╩┘ └╩═══╩┘ └╩   ╩┘     ╧╩╧   └╩   ╩┘ └═╧╩╧═┘ └╩═══╩┘",
)
ROW_COLORS = ("$accent", "$foreground", "$accent")


def wordmark_content() -> Content:
    spans, offset = [], 0
    for line, color in zip(LETTERS, ROW_COLORS, strict=True):
        spans.append(Span(offset, offset + len(line), color))
        offset += len(line) + 1
    return Content("\n".join(LETTERS), spans)


class HomeWordmark(Static):
    def __init__(self) -> None:
        super().__init__(wordmark_content(), classes="omega-home-wordmark")
