# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Texte venu d'ailleurs (noms et systemes declares par les machines du tailnet) : sans caracteres de controle avant
d'arriver dans un terminal (scan de securite 2026-11-25, F7 : un nom d'hote avec des sequences ANSI / OSC pouvait
changer le titre de la fenetre, ecrire dans le presse-papiers ou masquer une partie du rapport texte)."""
from __future__ import annotations

import unicodedata

BIDI_CONTROLS = frozenset("‪‫‬‭‮⁦⁧⁨⁩")
"""Inversions de sens d'ecriture : elles peuvent faire lire un nom a l'envers."""


def without_controls(text: str, *, keep: str = "") -> str:
    """Retire les caracteres de controle C0 / C1 (ESC compris), DEL et les inversions de sens. `keep` : ceux a
    garder (ex. "\\n\\t" pour un rapport en plusieurs lignes)."""
    return "".join(char for char in text
                   if char in keep or (unicodedata.category(char) != "Cc" and char not in BIDI_CONTROLS))
