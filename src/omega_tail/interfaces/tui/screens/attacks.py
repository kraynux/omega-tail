# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Attaques et decisions (lot 4, proposition §4.3) : compteurs de la porte et adresses les plus actives (lues en
direct dans HAProxy, toutes les 2 s), avec bloquer, liste noire, debloquer, confiance sur la ligne choisie.
Lot 6 : pays et AS de chaque adresse, mode attaque, et trois autres vues (empreintes JA4, AS, pays)."""
from __future__ import annotations

from typing import TYPE_CHECKING

from rich.text import Text
from textual.app import ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Button, DataTable, Footer, Header, Static

from omega_tail.application.gate import BLACK, TRUSTED, TableRow
from omega_tail.application.groups import GroupRow, GroupsStatus
from omega_tail.domain.groups import reason_pairs
from omega_tail.domain.snapshot import Snapshot
from omega_tail.interfaces.shared.messages import group_label
from omega_tail.interfaces.tui.screens._base import OmegaScreen
from omega_tail.interfaces.tui.widgets.status_band import StatusBand
from omega_tail.interfaces.tui.widgets.tables import WideTable
from omega_tail.shared.i18n import N_, _

if TYPE_CHECKING:
    from omega_tail.interfaces.tui.app import OmegaTailApp

REFRESH_SECONDS = 2.0
MAX_ROWS = 200
VIEWS = (("addresses", N_("Adresses")), ("ja4", N_("Empreintes")), ("as", "AS"), ("countries", N_("Pays")))


def groups_line(status: GroupsStatus) -> str:
    """Une ligne : mode (normal / ATTAQUE), regroupements observes ou appliques, motifs comptes."""
    if status.attack:
        mode = _("MODE ATTAQUE (retour au normal après {seconds} s de calme)").format(seconds=status.calm_left_s)
    else:
        mode = _("mode normal")
    applied = status.policy.mode == "applique"
    rules = _("regroupements appliqués") if applied else _("regroupements en observation")
    line = f"{mode} · {rules}"
    if status.reasons:
        # phrases entieres (lot 9) : un morceau de phrase insere ne se traduit pas
        text = _("refusées (7 j) : {reasons}") if applied else _("auraient été refusées (7 j) : {reasons}")
        line += " · " + text.format(
            reasons=", ".join(f"{_(label)} {count}" for label, count in reason_pairs(status.reasons)))
    return line


class AttacksScreen(OmegaScreen):
    def __init__(self) -> None:
        super().__init__()
        self._rows: list[TableRow] = []
        self._view = "addresses"

    def compose(self) -> ComposeResult:
        app: OmegaTailApp = self.app  # type: ignore[assignment]
        yield Header()
        yield StatusBand(app.snapshot)
        with Vertical(classes="tail-journal-panel tail-attacks-panel"):
            yield Static(_("ATTAQUES ET DÉCISIONS"), classes="omega-title")
            yield Static("", id="counters", markup=False)
            if app.gate is not None and app.gate.groups is not None:
                with Horizontal(classes="omega-actions", id="views"):
                    for key, label in VIEWS:
                        with Container(classes="omega-btn-frame"):
                            yield Button(_(label), id=f"view-{key}",
                                         variant="primary" if key == self._view else "default")
            yield WideTable(id="attacks-table", cursor_type="row", zebra_stripes=True)
            yield Static(_("La liste noire d'abord, puis les adresses bloquées, les plus actives, et la confiance. "
                           "Choisissez une ligne puis une action."), classes="omega-hint")
        with Horizontal(classes="omega-actions omega-fixed-actions"):
            for key, label, variant in (("block", _("Bloquer"), "error"), ("blacklist", _("Liste noire"), "error"),
                                        ("unblock", _("Débloquer"), "primary"), ("trust", _("Confiance"), "default")):
                with Container(classes="omega-btn-frame"):
                    yield Button(label, id=key, variant=variant)  # type: ignore[arg-type]
        # Seconde ligne (demande, 2026-11-24) : la liste noire se gere dans son propre ecran
        with Horizontal(classes="omega-actions omega-fixed-actions"):
            with Container(classes="omega-btn-frame"):
                yield Button(_("Gestion de la liste noire"), id="manage-blacklist")
            with Container(classes="omega-btn-frame"):
                yield Button(_("Retour"), id="back")
        yield Footer()

    def on_mount(self) -> None:
        self._columns()
        self.reload()
        self.set_interval(REFRESH_SECONDS, self.reload)

    def show_snapshot(self, snapshot: Snapshot) -> None:
        self.query_one(StatusBand).show(snapshot)

    def _columns(self) -> None:
        table = self.query_one("#attacks-table", WideTable)
        table.clear(columns=True)
        if self._view == "addresses":
            table.add_columns(_("Adresse"), _("Pays"), _("AS"), _("Connexions / 10 s"), _("État"), _("Expire dans"))
        else:
            title = {"ja4": _("Empreinte JA4"), "as": _("AS"), "countries": _("Pays")}[self._view]
            table.add_columns(title, _("Connexions / 10 s"), _("Total"), _("Remarque"))
        for button in ("block", "blacklist", "unblock", "trust"):
            self.query_one(f"#{button}", Button).disabled = self._view != "addresses"

    def reload(self) -> None:
        app: OmegaTailApp = self.app  # type: ignore[assignment]
        gate = app.gate
        if gate is None:
            return
        view, groups = self._view, gate.groups

        def work() -> None:
            counters = gate.counters()
            status = groups.status() if groups is not None and groups.lua() else None
            if groups is not None and status is not None:
                groups.learn()  # au plus une fois par heure (sans veille : l'ecran apprend quand il est ouvert)
            addresses: list[tuple[TableRow, str, int]] = []
            found: list[GroupRow] = []
            if view == "addresses":
                for row in gate.decisions()[:MAX_ROWS]:
                    country, asn = groups.locate(row.address) if groups is not None and "/" not in row.address \
                        else ("", 0)
                    addresses.append((row, country, asn))
            elif groups is not None:
                found = {"ja4": groups.top_fingerprints, "as": groups.top_as,
                         "countries": groups.top_countries}[view](MAX_ROWS)
            self.app.call_from_thread(self._show, view, addresses, found, counters, status)

        self.run_worker(work, thread=True, group="attacks", exclusive=True)

    def _show(self, view: str, addresses: list[tuple[TableRow, str, int]], found: list[GroupRow], counters: object,
              status: GroupsStatus | None) -> None:
        if view != self._view:
            return
        total, current, refused, admitted = (getattr(counters, name) for name in ("total", "current", "refused",
                                                                                   "admitted"))
        text = _("Connexions reçues : {total} · refusées avant chiffrement : {refused} · admises : {admitted} · "
                 "en cours : {current}").format(total=total, refused=refused, admitted=admitted, current=current)
        if status is not None:
            text += "\n" + groups_line(status)
        self.query_one("#counters", Static).update(text)
        table = self.query_one("#attacks-table", WideTable)
        cursor = table.cursor_row
        table.clear()
        styles = self.app.get_css_variables()
        self._rows = [item[0] for item in addresses]
        for row, country, asn in addresses:
            state, expiry = self.state_of(row, styles)
            table.add_row(row.address, country if country and country != "--" else "—",
                          f"AS{asn}" if asn else "—", str(row.rate_10s) if row.seen else "—", state, expiry)
        for group in found:
            table.add_row(group.key, str(group.rate_10s), str(group.count), group_label(group))
        shown = len(addresses) + len(found)
        if shown:
            table.move_cursor(row=min(cursor, shown - 1))
        self._trust_label()

    @staticmethod
    def state_of(row: TableRow, styles: dict[str, str]) -> tuple[Text, str]:
        """État et échéance : la liste où se trouve l'adresse passe avant le blocage temporaire."""
        if row.listed == BLACK:
            return Text(_("liste noire"), style=f"bold {styles.get('error', '')}"), _("jusqu'au retrait")
        if row.listed == TRUSTED:
            return Text(_("confiance"), style=f"bold {styles.get('success', '')}"), "—"
        if row.blocked:
            return Text(_("bloquée"), style=f"bold {styles.get('error', '')}"), f"{row.expires_s // 60} min"
        return Text(_("admise")), "—"

    def _selected_row(self) -> TableRow | None:
        table = self.query_one("#attacks-table", WideTable)
        if not self._rows or not 0 <= table.cursor_row < len(self._rows):
            return None
        return self._rows[table.cursor_row]

    def _trust_label(self) -> None:
        row = self._selected_row()
        trusted = row is not None and row.listed == TRUSTED
        self.query_one("#trust", Button).label = _("Retirer la confiance") if trusted else _("Confiance")

    def on_data_table_row_highlighted(self, _event: DataTable.RowHighlighted) -> None:
        self._trust_label()

    def _selected(self) -> str:
        row = self._selected_row()
        return row.address if row is not None else ""

    def on_button_pressed(self, event: Button.Pressed) -> None:
        app: OmegaTailApp = self.app  # type: ignore[assignment]
        if event.button.id == "back":
            self.action_back()
            return
        if event.button.id == "manage-blacklist":
            from omega_tail.interfaces.tui.screens.blacklist import BlacklistScreen
            self.app.push_screen(BlacklistScreen(), lambda _result: self.reload())
            return
        if (event.button.id or "").startswith("view-"):
            self._view = (event.button.id or "").removeprefix("view-")
            for key, _label in VIEWS:
                self.query_one(f"#view-{key}", Button).variant = "primary" if key == self._view else "default"
            self._columns()
            self.reload()
            return
        address = self._selected()
        row = self._selected_row()
        trusted = row is not None and row.listed == TRUSTED
        if not address:
            self.app.notify(_("Aucune adresse choisie."))
            return
        actions = {"block": lambda gate: gate.block(address),
                   "blacklist": lambda gate: gate.block(address, forever=True),
                   "unblock": lambda gate: gate.unblock(address),
                   "trust": lambda gate: gate.trust(address, add=not trusted)}
        action = actions.get(event.button.id or "")
        if action is not None:
            app.gate_action(action, after=self.reload)
