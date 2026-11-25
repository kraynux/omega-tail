# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Rapport (lot 7, proposition §4.4) : tout ce qu'omega-tail sait de la machine, en faits ; apercu ici, export TXT /
HTML / JSON dans le dossier des exports, et « Voir les exports » (methode commune de la suite : le dossier dans le
navigateur par omega-lib ; sans session graphique, liste et lecture ici meme).

Le compte Tailscale et les appareils du tailnet ne sont inclus que si la case est cochee (decision B du lot 7) :
un rapport peut etre envoye a quelqu'un."""
from __future__ import annotations

import contextlib
from typing import TYPE_CHECKING

from omega_lib.theme.policies import DEFAULT_EXPORT_THEME, EXPORT_PALETTES
from rich.text import Text
from textual.app import ComposeResult
from textual.containers import Container, Horizontal, VerticalScroll
from textual.css.query import NoMatches
from textual.widgets import Button, Checkbox, Footer, Header, Select, Static

from omega_tail.application.report import ReportFacts
from omega_tail.domain.snapshot import Snapshot
from omega_tail.interfaces.shared.report_view import export_name, render, render_text
from omega_tail.interfaces.tui.screens._base import OmegaScreen
from omega_tail.interfaces.tui.screens.exports import view_exports
from omega_tail.interfaces.tui.widgets.status_band import StatusBand
from omega_tail.shared.i18n import _

if TYPE_CHECKING:
    from omega_tail.interfaces.tui.app import OmegaTailApp

EXPORT_BUTTONS = {"export-txt": "txt", "export-html": "html", "export-json": "json"}


class ReportScreen(OmegaScreen):
    def __init__(self) -> None:
        super().__init__()
        self.facts: ReportFacts | None = None

    def compose(self) -> ComposeResult:
        app: OmegaTailApp = self.app  # type: ignore[assignment]
        yield Header()
        yield StatusBand(app.snapshot)
        with VerticalScroll(classes="omega-panel"):
            yield Static(_("RAPPORT"), classes="omega-title")
            yield Static(_("Tout ce qu'omega-tail sait de cette machine, en faits : Tailscale, publication, machine, "
                           "pare-feu, survie, alertes, et les attaques des 7 derniers jours (journal de la porte). "
                           "Enregistré dans le dossier des exports ; « Voir les exports » les ouvre pour les lire."),
                         classes="omega-hint")
            yield Checkbox(_("Inclure le compte Tailscale et les appareils du tailnet (noms, adresses)"), value=False,
                           id="include-private")
            yield Static(_("Sans cette case, seul leur nombre figure : le rapport peut être envoyé à quelqu'un sans "
                           "dévoiler votre tailnet. Les adresses des attaquants y restent toujours."),
                         classes="omega-hint")
            yield Static(_("THÈME DE LA PAGE HTML"), classes="omega-subtitle")
            settings = app.settings
            theme = settings.export_theme() if settings is not None else DEFAULT_EXPORT_THEME
            yield Select([(name, name) for name in EXPORT_PALETTES], value=theme, allow_blank=False,
                         id="export-theme")
            yield Static("", id="status", classes="omega-hint", markup=False)
            yield Static(_("APERÇU"), classes="omega-subtitle")
            yield Static("", id="report-preview", markup=False)
        # Deux barres (disposition d'omega-connect, voulue) : exporter et voir ; actualiser et retour
        with Horizontal(classes="omega-actions omega-fixed-actions"):
            for button_id, label in (("export-txt", _("Exporter TXT")), ("export-html", _("Exporter HTML")),
                                     ("export-json", _("Exporter JSON"))):
                with Container(classes="omega-btn-frame"):
                    yield Button(label, id=button_id, disabled=True)
            with Container(classes="omega-btn-frame"):
                yield Button(_("Voir les exports"), id="view-exports")
        with Horizontal(classes="omega-actions omega-fixed-actions"):
            with Container(classes="omega-btn-frame"):
                yield Button(_("Actualiser"), id="refresh", disabled=True)
            with Container(classes="omega-btn-frame"):
                yield Button(_("Retour"), id="back", variant="primary")
        yield Footer()

    def on_mount(self) -> None:
        self.build()

    def show_snapshot(self, snapshot: Snapshot) -> None:
        self.query_one(StatusBand).show(snapshot)

    def _set_ready(self, ready: bool) -> None:
        with contextlib.suppress(NoMatches):
            for button_id in (*EXPORT_BUTTONS, "refresh"):
                self.query_one(f"#{button_id}", Button).disabled = not ready

    def build(self) -> None:
        app: OmegaTailApp = self.app  # type: ignore[assignment]
        tools = app.report
        if tools is None:
            return
        private = self.query_one("#include-private", Checkbox).value
        snapshot = app.snapshot
        self._set_ready(False)
        self.query_one("#status", Static).update(_("Rapport en préparation (journal de la porte des 7 derniers "
                                                   "jours compris)…"))

        def work() -> None:
            try:
                facts = tools.build(include_private=private, snapshot=snapshot)
            except Exception as error:  # noqa: BLE001 - jamais planter l'interface pour un rapport
                self.app.call_from_thread(self._error, str(error) or type(error).__name__)
                return
            self.app.call_from_thread(self._show, facts)

        self.run_worker(work, thread=True, group="report", exclusive=True)

    def _error(self, message: str) -> None:
        with contextlib.suppress(NoMatches):
            self.query_one("#status", Static).update(_("Erreur : {message}").format(message=message))
            self.query_one("#refresh", Button).disabled = False

    def _show(self, facts: ReportFacts) -> None:
        self.facts = facts
        with contextlib.suppress(NoMatches):
            self.query_one("#report-preview", Static).update(Text(render_text(facts)))
            self.query_one("#status", Static).update(_("Rapport prêt ({time}).").format(
                time=facts.generated_at.strftime("%H:%M:%S")))
            self._set_ready(True)

    def on_checkbox_changed(self, event: Checkbox.Changed) -> None:
        if event.checkbox.id == "include-private":
            self.build()

    def _export(self, file_format: str) -> None:
        app: OmegaTailApp = self.app  # type: ignore[assignment]
        if self.facts is None or app.writer is None:
            return
        theme = str(self.query_one("#export-theme", Select).value)
        with app.exporting():
            content, extension = render(self.facts, file_format, theme)
        try:
            path = app.writer.save(export_name(self.facts, extension), content)
        except (OSError, ValueError) as error:
            self.app.notify(_("Export impossible : {error}").format(error=error), severity="error")
            return
        self.query_one("#status", Static).update(_("Rapport enregistré : {path}").format(path=path))
        self.app.notify(_("Rapport enregistré : {path}").format(path=path))

    def on_button_pressed(self, event: Button.Pressed) -> None:
        button = event.button.id or ""
        if button in EXPORT_BUTTONS:
            self._export(EXPORT_BUTTONS[button])
        elif button == "view-exports":
            view_exports(self)
        elif button == "refresh":
            self.build()
        elif button == "back":
            self.action_back()
