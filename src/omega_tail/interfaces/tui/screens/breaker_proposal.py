# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Proposition du disjoncteur (decision : il propose, il ne coupe jamais seul). Renvoie « minutes »
(coupure momentanee programmee), « total » (coupure totale) ou None (pas maintenant)."""
from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Center, Container, Horizontal, Middle, Vertical
from textual.screen import Screen
from textual.widgets import Button, Static

from omega_tail.shared.i18n import _


class BreakerProposalScreen(Screen[str | None]):
    def __init__(self, *, reason: str, minutes: int, ports: str) -> None:
        super().__init__()
        self._reason, self._minutes, self._ports = reason, minutes, ports

    def compose(self) -> ComposeResult:
        with Middle(), Center(), Vertical(classes="omega-confirm-box omega-trust-box"):
            yield Static(_("ATTAQUE PROBABLE — COUPER FUNNEL ?"), classes="omega-confirm-title")
            yield Static(_(
                "{reason}\n\nCouper Funnel (port {ports}) arrête aussitôt les connexions venues d'Internet : la "
                "machine respire. Le tailnet (Serve, SSH) n'est pas touché.\n\n"
                "• Coupure de {minutes} min : Funnel est remis en route tout seul, à l'identique, même si "
                "omega-tail est fermé.\n• Coupure totale : Funnel reste coupé jusqu'à ce que vous le rétablissiez "
                "(menu Survie).").format(reason=self._reason, ports=self._ports, minutes=self._minutes),
                id="proposal-text", markup=False)
            with Horizontal(classes="omega-confirm-buttons"):
                with Container(classes="omega-btn-frame"):
                    yield Button(_("Couper {minutes} min").format(minutes=self._minutes), id="minutes",
                                 variant="error")
                with Container(classes="omega-btn-frame"):
                    yield Button(_("Coupure totale"), id="total", variant="error")
                with Container(classes="omega-btn-frame"):
                    yield Button(_("Pas maintenant"), id="later", variant="primary")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.dismiss(event.button.id if event.button.id in ("minutes", "total") else None)
