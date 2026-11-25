# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Composition ASCII de l'ecran de demarrage : logo fourni dans ascii.txt,
caracteres non modifies. ascii.txt n'est PAS lu au demarrage : une retouche de ce fichier doit etre reportee ici.

Placement recalcule (les tabulations d'ascii.txt ne donnent pas de colonnes sures) : chaque bloc est centre sur un
axe unique, le milieu du cadre OMEGA-TAIL (77 colonnes, colonne 38). Le schema (SERVE, ecran, FUNNEL, LAN, WEB) est
place depuis ses points de jonction : « ╠═════╣ » colle SERVE a l'ecran, « ╠════╣ » l'ecran a FUNNEL, les « ╦ »
des boites tombent sur les « ╩ » de LAN et de WEB. Bloc de largeur paire : la demi-colonne en trop part a gauche.

Couleurs (regles ecrites en tete d'ascii.txt) :
- cadres (« container ») : clair ($foreground) ;
- texte OMEGA-TAIL : ligne 1 vif ($accent), ligne 2 clair, ligne 3 vif ;
- « LINUX TAILNET CONTROL » vif dans son cadre clair, comme le reste de la suite ; noms des boites du schema vifs ;
- blocs : █ clair, ▓ moins clair, ▒ et ░ chacun une nuance en dessous (transparence du ton clair : suit le theme) ;
- ligne du bas : « | » vifs, mots clairs.
La version (« ░▒▓█V0.1.0█▓▒░ ») vient de pyproject.toml, seule source."""
from __future__ import annotations

from textual.content import Content, Span
from textual.widgets import Static

WIDTH = 77
AXIS = (WIDTH - 1) // 2
CLEAR = "$foreground"
BRIGHT = "$accent"
SHADES = {"█": CLEAR, "▄": CLEAR, "▀": CLEAR, "▓": "$foreground 75%", "▒": "$foreground 55%",
          "░": "$foreground 35%"}

TITLE_BOX = (
    "┌───────────────────────┐",
    "│ LINUX TAILNET CONTROL │",
    "└───────────────────────┘",
)
WORDMARK_BOX = (
    "┌───────────────────────────────────────────────────────────────────────────┐",
    "│ ┌╦═══╦┐ ┌╦═╦═╦┐ ┌╦═══╦┐ ┌╦═══╦┐ ┌╦═══╦┐   ┌═╤╦╤═┐ ┌╦═══╦┐ ┌═╤╦╤═┐ ┌╦      │",
    "│ │║   ║│ │║ ║ ║│ ├╬══    │║  ═╦┐ ├╬═══╬┤ ═   │║│   ├╬═══╬┤   │║│   │║      │",
    "│ └╩═══╩┘ └╩   ╩┘ └╩═══╩┘ └╩═══╩┘ └╩   ╩┘     ╧╩╧   └╩   ╩┘ └═╧╩╧═┘ └╩═══╩┘ │",
    "└───────────────────────────────────────────────────────────────────────────┘",
)
WORDMARK_ROWS = {1: BRIGHT, 2: CLEAR, 3: BRIGHT}

MONITOR_WIDTH = 19
MONITOR = AXIS - MONITOR_WIDTH // 2
"""Colonne du bord gauche de l'ecran du schema ; tout le schema est place depuis elle."""
SCHEMA: tuple[tuple[tuple[int, str], ...], ...] = (
    ((0, "┌▄▄▄▄▄▄▄▄██▄▄▄▄▄▄▄┐"),),
    ((-14, "╔═══════╗"), (0, "│█┌─────────────┐█│"), (23, "╔════════╗")),
    ((-14, "║ SERVE ╠═════╣█│https://░░░░░│█╠════╣ FUNNEL ║"),),
    ((-14, "╚═══╦═══╝"), (0, "│█│name.ts.net░░│█│"), (23, "╚════╦═══╝")),
    ((-10, "║"), (0, "│█└─────────────┘█│"), (28, "║")),
    ((-15, "┌╦═══╩═══╦┐"), (0, "└█████████████████┘"), (23, "┌╦═══╩═══╦┐")),
    ((-15, "│║ L A N ║│"), (6, "███▓███"), (23, "│║ W E B ║│")),
    ((-15, "└╩═══════╩┘"), (2, "╠░░░░░░░░░░░░░╣"), (23, "└╩═══════╩┘")),
)
"""(decalage depuis le bord gauche de l'ecran, texte) pour chaque ligne du schema."""
LABELS = ("SERVE", "FUNNEL", "L A N", "W E B")
TAGLINE = "CONTROL | PROTECTION | TAILSCALE | NETWORK"


def start_on_axis(width: int) -> int:
    return AXIS - width // 2


def on_axis(text: str) -> str:
    return " " * start_on_axis(len(text)) + text


def version_bar(version: str) -> str:
    return on_axis(f"░▒▓█V{version}█▓▒░")


def schema_lines() -> tuple[str, ...]:
    lines = []
    for row in SCHEMA:
        cells: list[str] = []
        for offset, text in row:
            start = MONITOR + offset
            if len(cells) < start:
                cells.extend(" " * (start - len(cells)))
            cells[start:start + len(text)] = text
        lines.append("".join(cells))
    return tuple(lines)


class _Builder:
    def __init__(self) -> None:
        self.text: list[str] = []
        self.spans: list[Span] = []
        self.offset = 0

    def line(self, text: str, style_of: dict[int, str]) -> None:
        start = None
        current = ""
        for index, char in enumerate([*text, "\0"]):
            style = style_of.get(index, "") if char not in (" ", "\0") else ""
            if style != current:
                if current and start is not None:
                    self.spans.append(Span(self.offset + start, self.offset + index, current))
                start, current = index, style
        self.text.append(text)
        self.offset += len(text) + 1

    def content(self) -> Content:
        return Content("\n".join(self.text), self.spans)


def _plain(text: str, color: str = CLEAR) -> dict[int, str]:
    return {index: SHADES.get(char, color) for index, char in enumerate(text)}


def _framed(text: str, inner: str) -> dict[int, str]:
    styles = _plain(text)
    first, last = text.index("│"), text.rindex("│")
    styles.update({index: inner for index in range(first + 1, last) if text[index] not in SHADES})
    return styles


def _schema_row(text: str) -> dict[int, str]:
    styles = _plain(text)
    for label in LABELS:
        position = text.find(label)
        if position >= 0:
            styles.update({position + offset: BRIGHT for offset in range(len(label))})
    return styles


def _tagline(text: str) -> dict[int, str]:
    return {index: BRIGHT if char == "|" else CLEAR for index, char in enumerate(text)}


def splash_content(version: str) -> Content:
    builder = _Builder()
    title = [on_axis(line) for line in TITLE_BOX]
    builder.line(title[0], _plain(title[0]))
    builder.line(title[1], _framed(title[1], BRIGHT))
    builder.line(title[2], _plain(title[2]))
    bar = version_bar(version)
    builder.line(bar, _plain(bar))
    for row, text in enumerate(WORDMARK_BOX):
        builder.line(text, _framed(text, WORDMARK_ROWS[row]) if row in WORDMARK_ROWS else _plain(text))
    for text in schema_lines():
        builder.line(text, _schema_row(text))
    builder.line("", {})
    tagline = on_axis(TAGLINE)
    builder.line(tagline, _tagline(tagline))
    return builder.content()


class SplashHero(Static):
    def __init__(self, version: str) -> None:
        super().__init__(splash_content(version), classes="omega-splash-hero")
