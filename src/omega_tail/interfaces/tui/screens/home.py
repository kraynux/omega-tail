# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Menu principal (deux colonnes de 6, sans bouton Quitter : touche q ou Echap). Entrees lues dans `menu.py`."""
from __future__ import annotations

from collections.abc import Callable
from typing import ClassVar

from textual.app import ComposeResult
from textual.binding import Binding, BindingType
from textual.containers import Center, Container, Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import Button, Footer, Header

from omega_tail.domain.snapshot import Snapshot
from omega_tail.interfaces.tui.menu import COLUMN_TITLES, MENU, Column, entry
from omega_tail.interfaces.tui.screens.quit_confirm import QuitConfirmScreen
from omega_tail.interfaces.tui.widgets.home_wordmark import HomeWordmark
from omega_tail.interfaces.tui.widgets.status_band import StatusBand
from omega_tail.shared.i18n import _

ScreenFactory = Callable[[str], "Screen[None] | None"]


def planned_notice(app: object, key: str) -> None:
    item = entry(key)
    if item is None:
        return
    text = (_("Cet écran arrive dans une prochaine version (lot {lot}).").format(lot=item.planned) if item.planned
            else _("Cet écran n'est pas disponible dans cette session."))
    app.notify(text, title=_(item.label), severity="information")  # type: ignore[attr-defined]


class HomeScreen(Screen[None]):
    BINDINGS: ClassVar[list[BindingType]] = [
        Binding("escape", "back", _("Quitter"), show=False),
        Binding("up", "focus_previous_item", _("Monter"), show=False),
        Binding("down", "focus_next_item", _("Descendre"), show=False),
    ]

    def __init__(self, *, open_screen: ScreenFactory) -> None:
        super().__init__()
        self._open_screen = open_screen

    def compose(self) -> ComposeResult:
        yield Header()
        yield StatusBand(getattr(self.app, "snapshot", None))
        with Vertical(classes="omega-home-root"):
            with Center():
                yield HomeWordmark()
            with Center(), Horizontal(classes="omega-home-columns"):
                for column in Column:
                    with Vertical(classes="omega-home-menu") as box:
                        for item in MENU:
                            if item.column is column:
                                with Container(classes="omega-btn-frame"):
                                    yield Button(_(item.label).upper(), id=f"menu-{item.key}")
                    box.border_title = _(COLUMN_TITLES[column])
        yield Footer()

    def show_snapshot(self, snapshot: Snapshot) -> None:
        self.query_one(StatusBand).show(snapshot)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        key = (event.button.id or "").removeprefix("menu-")
        item = entry(key)
        if item is None:
            return
        screen = None if item.planned else self._open_screen(key)
        if screen is not None:
            self.app.push_screen(screen)
            return
        planned_notice(self.app, key)

    def action_back(self) -> None:
        self.app.push_screen(QuitConfirmScreen(), self._quit_if_confirmed)

    def _quit_if_confirmed(self, confirmed: bool | None) -> None:
        if confirmed:
            self.app.exit()

    def action_focus_previous_item(self) -> None:
        self.focus_previous()

    def action_focus_next_item(self) -> None:
        self.focus_next()
