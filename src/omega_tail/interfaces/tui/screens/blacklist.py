# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Gestion de la liste noire de la porte (finitions 0.7.0, demande 2026-11-24) : voir, filtrer, ajouter
en prevision, supprimer, importer un fichier TXT (doublons ecartes), purger finement (anciennete, les N plus
anciennes, plage de lignes, origine, tout) avec apercu, exporter TXT / HTML / JSON. Ouvert depuis « Attaques et
decisions ». Toute modification est appliquee a chaud dans HAProxy."""
from __future__ import annotations

import contextlib
from collections.abc import Callable
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING

from omega_lib.theme.policies import DEFAULT_EXPORT_THEME, EXPORT_PALETTES
from textual.app import ComposeResult
from textual.containers import Container, Horizontal, VerticalScroll
from textual.css.query import NoMatches
from textual.widgets import Button, Footer, Header, Input, Select, Static

from omega_tail.application.survival import Outcome
from omega_tail.domain.blacklist import (
    BLACKLIST_MAX,
    BLACKLIST_WARNING,
    ORIGIN_EXISTING,
    ORIGIN_IMPORT,
    ORIGIN_MANUAL,
    ORIGIN_SCREEN,
    PURGE_ALL,
    PURGE_OLDER,
    PURGE_OLDEST,
    PURGE_ORIGIN,
    PURGE_RANGE,
    BlackEntry,
    PurgeChoice,
)
from omega_tail.domain.snapshot import Snapshot
from omega_tail.interfaces.shared.blacklist_view import origin_label, render
from omega_tail.interfaces.shared.messages import outcome_text
from omega_tail.interfaces.tui.screens._base import OmegaScreen
from omega_tail.interfaces.tui.screens.confirm import ConfirmScreen
from omega_tail.interfaces.tui.screens.exports import view_exports
from omega_tail.interfaces.tui.screens.typed_confirm import TypedConfirmScreen
from omega_tail.interfaces.tui.widgets.busy import Busy
from omega_tail.interfaces.tui.widgets.status_band import StatusBand
from omega_tail.interfaces.tui.widgets.tables import WideTable
from omega_tail.shared.i18n import N_, _

if TYPE_CHECKING:
    from omega_tail.application.gate import GateTools
    from omega_tail.interfaces.tui.app import OmegaTailApp

SHOWN_MAX = 500
IMPORT_MAX_BYTES = 8 * 1024 * 1024
PURGES = (
    (PURGE_OLDER, "", N_("Plus anciennes que N jours")),
    (PURGE_OLDEST, "", N_("Les N plus anciennes")),
    (PURGE_RANGE, "", N_("De la ligne A à la ligne B")),
    (PURGE_ORIGIN, ORIGIN_IMPORT, N_("Origine : import")),
    (PURGE_ORIGIN, ORIGIN_SCREEN, N_("Origine : écran Attaques")),
    (PURGE_ORIGIN, ORIGIN_MANUAL, N_("Origine : ajout manuel")),
    (PURGE_ORIGIN, ORIGIN_EXISTING, N_("Origine : avant les dates")),
    (PURGE_ALL, "", N_("Toute la liste")),
)
EXPORT_BUTTONS = {"export-txt": "txt", "export-html": "html", "export-json": "json"}


def _thousands(value: int) -> str:
    return f"{value:,}".replace(",", "\u202f")


def _number(text: str) -> int:
    text = text.strip()
    return int(text) if text.isdigit() else 0


class BlacklistScreen(OmegaScreen):
    def __init__(self) -> None:
        super().__init__()
        self._entries: list[BlackEntry] = []
        self._shown: list[BlackEntry] = []

    def compose(self) -> ComposeResult:
        app: OmegaTailApp = self.app  # type: ignore[assignment]
        yield Header()
        yield StatusBand(app.snapshot)
        with VerticalScroll(classes="omega-panel"):
            yield Static(_("GESTION DE LA LISTE NOIRE"), classes="omega-title")
            yield Static("", id="summary", classes="omega-hint", markup=False)
            yield Static(_("AJOUTER OU IMPORTER"), classes="omega-subtitle")
            with Horizontal(classes="omega-actions tail-black-row"):
                yield Input(placeholder=_("adresse ou réseau (ex. 203.0.113.7 ou 198.51.100.0/24)"),
                            id="new-address", classes="tail-black-input")
                with Container(classes="omega-btn-frame"):
                    yield Button(_("Ajouter"), id="add")
            with Horizontal(classes="omega-actions tail-black-row"):
                yield Input(placeholder=_("fichier TXT : une adresse ou un réseau par ligne, # = commentaire"),
                            id="import-path", classes="tail-black-input")
                with Container(classes="omega-btn-frame"):
                    yield Button(_("Importer"), id="import")
            yield Static(_("Les doublons, les adresses déjà couvertes par un réseau de la liste et celles du tailnet "
                           "sont écartés et comptés. Un export TXT se réimporte tel quel (récidive)."),
                         classes="omega-hint")
            yield Static(_("LISTE"), classes="omega-subtitle")
            yield Input(placeholder=_("filtrer : début d'adresse, réseau, date (2026-11), origine"), id="filter",
                        classes="tail-black-input")
            yield WideTable(id="black-table", cursor_type="row", zebra_stripes=True)
            yield Static("", id="shown", classes="omega-hint", markup=False)
            yield Static(_("PURGER"), classes="omega-subtitle")
            with Horizontal(classes="omega-actions tail-black-row"):
                yield Select([(_(label), index) for index, (_mode, _origin, label) in enumerate(PURGES)], value=0,
                             allow_blank=False, id="purge-mode", classes="tail-purge-mode")
                yield Input(placeholder=_("N ou A"), id="purge-a", classes="tail-number")
                yield Input(placeholder="B", id="purge-b", classes="tail-number")
                with Container(classes="omega-btn-frame"):
                    yield Button(_("Aperçu"), id="preview")
                with Container(classes="omega-btn-frame"):
                    yield Button(_("Purger"), id="purge", variant="error")
            yield Static(_("Les lignes sont numérotées de la plus ancienne à la plus récente, comme dans le tableau "
                           "sans filtre. L'aperçu dit combien d'entrées partiraient ; rien n'est retiré sans "
                           "confirmation."), id="purge-hint", classes="omega-hint", markup=False)
            yield Static(_("THÈME DE LA PAGE HTML"), classes="omega-subtitle")
            settings = app.settings
            theme = settings.export_theme() if settings is not None else DEFAULT_EXPORT_THEME
            yield Select([(name, name) for name in EXPORT_PALETTES], value=theme, allow_blank=False,
                         id="export-theme", classes="tail-purge-mode")
            yield Busy(id="busy")
        with Horizontal(classes="omega-actions omega-fixed-actions"):
            with Container(classes="omega-btn-frame"):
                yield Button(_("Supprimer"), id="remove", variant="primary")
            for button_id, label in (("export-txt", _("Exporter TXT")), ("export-html", _("Exporter HTML")),
                                     ("export-json", _("Exporter JSON"))):
                with Container(classes="omega-btn-frame"):
                    yield Button(label, id=button_id)
            with Container(classes="omega-btn-frame"):
                yield Button(_("Voir les exports"), id="view-exports")
            with Container(classes="omega-btn-frame"):
                yield Button(_("Retour"), id="back")
        yield Footer()

    def on_mount(self) -> None:
        table = self.query_one("#black-table", WideTable)
        table.add_columns("N°", _("Adresse ou réseau"), _("Ajoutée le"), _("Origine"))
        self.reload()

    def show_snapshot(self, snapshot: Snapshot) -> None:
        self.query_one(StatusBand).show(snapshot)

    # ---- lecture ----
    def reload(self) -> None:
        app: OmegaTailApp = self.app  # type: ignore[assignment]
        gate = app.gate
        if gate is None:
            return

        def work() -> None:
            entries = gate.black_entries()
            self.app.call_from_thread(self._loaded, entries)

        self.run_worker(work, thread=True, group="blacklist-read", exclusive=True)

    def _loaded(self, entries: list[BlackEntry]) -> None:
        self._entries = entries
        count = len(entries)
        summary = _("{count} entrée(s) sur {max} au plus. Refusées par la porte avant tout chiffrement, jusqu'à "
                    "leur retrait.").format(count=_thousands(count), max=_thousands(BLACKLIST_MAX))
        if count >= BLACKLIST_WARNING:
            summary += " " + _("La liste grossit : exportez-la puis purgez les plus anciennes.")
        with contextlib.suppress(NoMatches):
            self.query_one("#summary", Static).update(summary)
        self._fill()

    def _fill(self) -> None:
        needle = self.query_one("#filter", Input).value.strip().lower()
        numbered = list(enumerate(self._entries, start=1))
        if needle:
            numbered = [(number, entry) for number, entry in numbered
                        if needle in entry.address or needle in entry.added.strftime("%Y-%m-%d %H:%M")
                        or needle in origin_label(entry.origin).lower()]
        table = self.query_one("#black-table", WideTable)
        cursor = table.cursor_row
        table.clear()
        visible = numbered[:SHOWN_MAX]
        self._shown = [entry for _number, entry in visible]
        for number, entry in visible:
            table.add_row(str(number), entry.address, entry.added.strftime("%Y-%m-%d %H:%M"),
                          origin_label(entry.origin))
        if visible:
            table.move_cursor(row=min(cursor, len(visible) - 1))
        if len(numbered) > SHOWN_MAX:
            text = _("{shown} premières lignes affichées sur {total} : affinez le filtre, ou exportez pour tout "
                     "voir.").format(shown=SHOWN_MAX, total=len(numbered))
        elif needle:
            text = _("{count} entrée(s) correspondent au filtre.").format(count=len(numbered))
        else:
            text = "" if numbered else _("La liste noire est vide.")
        self.query_one("#shown", Static).update(text)

    def on_input_changed(self, event: Input.Changed) -> None:
        if event.input.id == "filter":
            self._fill()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        if event.input.id == "new-address":
            self._add()
        elif event.input.id == "import-path":
            self._import()

    # ---- actions ----
    def _run(self, action: Callable[[GateTools], Outcome], busy: str = "") -> None:
        """Action de GateTools dans un fil ; la notification dit le resultat, puis la liste est relue."""
        app: OmegaTailApp = self.app  # type: ignore[assignment]
        gate = app.gate
        if gate is None:
            return
        if busy:
            self.query_one("#busy", Busy).show(busy)

        def work() -> None:
            try:
                outcome = action(gate)
            except (OSError, ValueError) as error:
                outcome = Outcome(False, "{error}", {"error": str(error)})
            self.app.call_from_thread(self._done, outcome)

        self.run_worker(work, thread=True, group="blacklist", exclusive=True)

    def _done(self, outcome: Outcome) -> None:
        with contextlib.suppress(NoMatches):
            self.query_one("#busy", Busy).hide()
        text = outcome_text(outcome)
        if outcome.params.get("invalid_lines"):
            text += "\n" + _("Lignes invalides : {lines}").format(lines=outcome.params["invalid_lines"])
        if outcome.ok and outcome.params.get("inactive"):
            text += "\n" + _("La porte n'est pas active : les listes s'appliqueront à son activation.")
        self.app.notify(text, title=_("Liste noire"), severity="information" if outcome.ok else "error", timeout=12)
        self.reload()

    def _add(self) -> None:
        field = self.query_one("#new-address", Input)
        text = field.value.strip()
        if not text:
            self.app.notify(_("Tapez une adresse ou un réseau."))
            return
        field.value = ""
        self._run(lambda gate: gate.add_black(text))

    def _import(self) -> None:
        raw = self.query_one("#import-path", Input).value.strip()
        if not raw:
            self.app.notify(_("Indiquez le chemin du fichier TXT à importer."))
            return
        path = Path(raw).expanduser()

        def action(gate: GateTools) -> Outcome:
            if not path.is_file():
                return Outcome(False, "Fichier introuvable : {path}", {"path": str(path)})
            if path.stat().st_size > IMPORT_MAX_BYTES:
                return Outcome(False, "Fichier trop gros (plus de {size} Mo) : découpez-le.",
                               {"size": IMPORT_MAX_BYTES // (1024 * 1024)})
            outcome, report = gate.import_black(path.read_text(encoding="utf-8", errors="replace"))
            if report.invalid:
                lines = ", ".join(str(number) for number, _text in report.invalid[:10])
                return Outcome(outcome.ok, outcome.message,
                               {**outcome.params, "invalid_lines": lines + ("…" if len(report.invalid) > 10 else "")})
            return outcome

        self._run(action, _("Import en cours…"))

    def _remove(self) -> None:
        table = self.query_one("#black-table", WideTable)
        if not self._shown or not 0 <= table.cursor_row < len(self._shown):
            self.app.notify(_("Aucune entrée choisie."))
            return
        address = self._shown[table.cursor_row].address
        self._run(lambda gate: gate.remove_black([address]))

    def _choice(self) -> PurgeChoice:
        mode, origin, _label = PURGES[int(self.query_one("#purge-mode", Select).value)]  # type: ignore[arg-type]
        a, b = _number(self.query_one("#purge-a", Input).value), _number(self.query_one("#purge-b", Input).value)
        return PurgeChoice(mode, days=a, count=a, first=a, last=b or a, origin=origin)

    def _check(self, choice: PurgeChoice) -> str:
        if choice.mode in (PURGE_OLDER, PURGE_OLDEST) and choice.days <= 0:
            return _("Tapez N (un nombre entier) dans le premier champ.")
        if choice.mode == PURGE_RANGE and choice.first <= 0:
            return _("Tapez A et B (numéros de ligne) dans les deux champs.")
        return ""

    def _preview(self) -> None:
        app: OmegaTailApp = self.app  # type: ignore[assignment]
        choice = self._choice()
        problem = self._check(choice)
        if problem or app.gate is None:
            self.app.notify(problem or _("Pare-feu indisponible."), severity="warning")
            return
        gone = app.gate.purge_preview(choice)
        self.query_one("#purge-hint", Static).update(
            _("Aperçu : {count} entrée(s) sur {total} partiraient.").format(count=len(gone), total=len(self._entries))
            + ("" if not gone else " " + _("De {first} à {last}.").format(first=gone[0].address,
                                                                          last=gone[-1].address)))

    def _purge(self) -> None:
        app: OmegaTailApp = self.app  # type: ignore[assignment]
        choice = self._choice()
        problem = self._check(choice)
        if problem or app.gate is None:
            self.app.notify(problem or _("Pare-feu indisponible."), severity="warning")
            return
        count = len(app.gate.purge_preview(choice))
        if not count:
            self.app.notify(_("Aucune entrée ne correspond : rien à purger."))
            return
        text = _("{count} entrée(s) vont quitter la liste noire : ces adresses seront de nouveau admises (soumises "
                 "aux règles). Exportez la liste avant si vous voulez pouvoir les réinjecter.").format(count=count)

        def answer(yes: bool | None) -> None:
            if yes:
                self._run(lambda gate: gate.purge_black(choice), _("Purge en cours…"))

        if choice.mode == PURGE_ALL:
            self.app.push_screen(TypedConfirmScreen(title=_("VIDER LA LISTE NOIRE ?"), text=text, word=_("VIDER"),
                                                    yes=_("Vider"), no=_("Annuler")), answer)
        else:
            self.app.push_screen(ConfirmScreen(title=_("PURGER LA LISTE NOIRE ?"), text=text, yes=_("Purger"),
                                               no=_("Annuler")), answer)

    def _export(self, file_format: str) -> None:
        app: OmegaTailApp = self.app  # type: ignore[assignment]
        if app.writer is None:
            return
        snapshot = app.snapshot
        machine = (snapshot.machine.hostname or snapshot.tailscale.host_name) if snapshot is not None else ""
        theme = str(self.query_one("#export-theme", Select).value)
        with app.exporting():
            content, name = render(self._entries, file_format, version=app.version, machine=machine or "?",
                                   when=datetime.now().astimezone(), theme=theme)
        try:
            path = app.writer.save(name, content)
        except (OSError, ValueError) as error:
            self.app.notify(_("Export impossible : {error}").format(error=error), severity="error")
            return
        self.app.notify(_("Liste noire enregistrée ({count} entrée(s)) : {path}").format(count=len(self._entries),
                                                                                          path=path))

    def on_button_pressed(self, event: Button.Pressed) -> None:
        button = event.button.id or ""
        if button == "add":
            self._add()
        elif button == "import":
            self._import()
        elif button == "remove":
            self._remove()
        elif button == "preview":
            self._preview()
        elif button == "purge":
            self._purge()
        elif button in EXPORT_BUTTONS:
            self._export(EXPORT_BUTTONS[button])
        elif button == "view-exports":
            view_exports(self)
        elif button == "back":
            self.action_back()
