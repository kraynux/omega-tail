# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Confirmation renforcee (lot 5 : deconnexion definitive) : le bouton ne s'active qu'une fois le mot demande
tape a l'identique."""
from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Center, Container, Horizontal, Middle, Vertical
from textual.screen import Screen
from textual.widgets import Button, Input, Static


class TypedConfirmScreen(Screen[bool]):
    def __init__(self, *, title: str, text: str, word: str, yes: str, no: str) -> None:
        super().__init__()
        self._title, self._text, self._word, self._yes, self._no = title, text, word, yes, no

    def compose(self) -> ComposeResult:
        with Middle(), Center(), Vertical(classes="omega-confirm-box omega-trust-box"):
            yield Static(self._title, classes="omega-confirm-title")
            yield Static(self._text, id="confirm-text", markup=False)
            yield Input(placeholder=self._word, id="typed")
            with Horizontal(classes="omega-confirm-buttons"):
                with Container(classes="omega-btn-frame"):
                    yield Button(self._yes, id="confirm", variant="error", disabled=True)
                with Container(classes="omega-btn-frame"):
                    yield Button(self._no, id="cancel", variant="primary")

    def on_mount(self) -> None:
        self.query_one("#typed", Input).focus()

    def on_input_changed(self, event: Input.Changed) -> None:
        self.query_one("#confirm", Button).disabled = event.value.strip() != self._word

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.dismiss(event.button.id == "confirm")
