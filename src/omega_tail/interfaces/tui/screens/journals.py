# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Journaux (proposition §3.6) : journal de tailscaled (journalctl, sans sudo), nombre de lignes, filtre,
couleurs par information et par categorie (journal_highlight.py, 2026-11-25), export ; source « porte » : journal de
la porte et de ses decisions."""
from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from textual.app import ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Button, Footer, Header, Input, RichLog, Select, Static

from omega_tail.core.constants import JOURNAL_DEFAULT_LINES, JOURNAL_LINES
from omega_tail.domain.snapshot import Snapshot
from omega_tail.interfaces.shared.messages import localized
from omega_tail.interfaces.tui.screens._base import OmegaScreen
from omega_tail.interfaces.tui.screens.exports import view_exports
from omega_tail.interfaces.tui.screens.journal_highlight import highlight_journal_line, palette_from_theme
from omega_tail.interfaces.tui.widgets.status_band import StatusBand
from omega_tail.ports.readers import JournalResult
from omega_tail.shared.i18n import _

if TYPE_CHECKING:
    from omega_tail.interfaces.tui.app import OmegaTailApp

def filtered(lines: tuple[str, ...], text: str) -> list[str]:
    needle = text.strip().lower()
    return [line for line in lines if needle in line.lower()] if needle else list(lines)


class JournalsScreen(OmegaScreen):
    def __init__(self) -> None:
        super().__init__()
        self._result = JournalResult(())
        self._count = 0
        self._unit = "tailscaled"
        """Nombre de lignes de la derniere lecture : la valeur initiale de la liste emet aussi Changed."""

    def compose(self) -> ComposeResult:
        app: OmegaTailApp = self.app  # type: ignore[assignment]
        yield Header()
        yield StatusBand(app.snapshot)
        with Vertical(classes="tail-journal-panel"):
            yield Static(_("JOURNAUX"), classes="omega-title")
            with Horizontal(classes="omega-actions"):
                yield Select([("tailscaled", "tailscaled"), (_("porte (pare-feu)"), "porte")],
                             value="tailscaled", allow_blank=False, id="journal-source")
                yield Select([(_("{count} lignes").format(count=count), count) for count in JOURNAL_LINES],
                             value=JOURNAL_DEFAULT_LINES, allow_blank=False, id="journal-lines")
                yield Input(placeholder=_("Filtrer (texte, adresse…)"), id="journal-filter")
            yield Static("", id="journal-state", classes="omega-hint", markup=False)
            yield RichLog(id="journal-log", wrap=False, highlight=False, markup=False, max_lines=5000)
        with Horizontal(classes="omega-actions omega-fixed-actions"):
            with Container(classes="omega-btn-frame"):
                yield Button(_("Relire"), id="reload", variant="primary")
            with Container(classes="omega-btn-frame"):
                yield Button(_("Exporter"), id="export")
            with Container(classes="omega-btn-frame"):
                yield Button(_("Voir les exports"), id="view-exports")
            with Container(classes="omega-btn-frame"):
                yield Button(_("Retour"), id="back")
        yield Footer()

    def on_mount(self) -> None:
        self._reload()
        # couleurs prises dans le theme : un changement de theme (touche t) recolore les lignes affichees
        self.watch(self.app, "theme", lambda _name: self._show_lines() if self._result.lines else None, init=False)

    def show_snapshot(self, snapshot: Snapshot) -> None:
        self.query_one(StatusBand).show(snapshot)

    def _reload(self) -> None:
        app: OmegaTailApp = self.app  # type: ignore[assignment]
        count = int(str(self.query_one("#journal-lines", Select).value))
        unit = str(self.query_one("#journal-source", Select).value)
        self._count, self._unit = count, unit
        self.query_one("#journal-state", Static).update(_("Lecture du journal…"))

        def work() -> None:
            result = app.journal.read(unit, count)
            self.app.call_from_thread(self._loaded, result)

        self.run_worker(work, thread=True, group="journal", exclusive=True)

    def _loaded(self, result: JournalResult) -> None:
        self._result = result
        self._show_lines()

    def _show_lines(self) -> None:
        log = self.query_one("#journal-log", RichLog)
        log.clear()
        result = self._result
        state = self.query_one("#journal-state", Static)
        if not result.lines:
            message = _("Aucune ligne lue.") + (f" {localized(result.error)}" if result.error else "")
            state.update(message + (f"\n{_(result.hint)}" if result.hint else ""))
            return
        palette = palette_from_theme(self.app.get_css_variables())
        shown = filtered(result.lines, self.query_one("#journal-filter", Input).value)
        for line in shown:
            log.write(highlight_journal_line(line, palette))
        state.update(_("{shown} ligne(s) affichée(s) sur {total} lue(s).").format(shown=len(shown),
                                                                              total=len(result.lines)))

    def on_select_changed(self, event: Select.Changed) -> None:
        lines_changed = event.select.id == "journal-lines" and int(str(event.value)) != self._count
        source_changed = event.select.id == "journal-source" and str(event.value) != self._unit
        if lines_changed or source_changed:
            self._reload()

    def on_input_changed(self, event: Input.Changed) -> None:
        if event.input.id == "journal-filter":
            self._show_lines()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "reload":
            self._reload()
        elif event.button.id == "export":
            self._export()
        elif event.button.id == "view-exports":
            view_exports(self)
        elif event.button.id == "back":
            self.action_back()

    def _export(self) -> None:
        app: OmegaTailApp = self.app  # type: ignore[assignment]
        lines = filtered(self._result.lines, self.query_one("#journal-filter", Input).value)
        if not lines or app.writer is None:
            self.app.notify(_("Rien à exporter."))
            return
        name = f"omega-tail-journal-{self._unit}-{datetime.now():%Y%m%d-%H%M%S}.txt"
        try:
            path = app.writer.save(name, "\n".join(lines) + "\n")
        except (OSError, ValueError) as error:
            self.app.notify(str(error), severity="error")
            return
        self.app.notify(_("Journal exporté : {path}").format(path=path))
