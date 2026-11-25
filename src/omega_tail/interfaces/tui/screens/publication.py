# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Publication (lot 5, proposition §3.4) : tout ce que Serve (tailnet) et Funnel (Internet) publient, protege par la
porte ou non ; ajouter, retirer, suspendre / retablir Funnel, essai de bout en bout (certificat compris),
sauvegardes et restauration."""
from __future__ import annotations

from typing import TYPE_CHECKING

from textual.app import ComposeResult
from textual.containers import Container, Horizontal, VerticalScroll
from textual.widgets import Button, Footer, Header, Input, Rule, Select, Static

from omega_tail.domain.funnel import Handler
from omega_tail.domain.publication import KINDS, AddRequest, Backup, remove_command
from omega_tail.domain.snapshot import Snapshot
from omega_tail.domain.tailscale import Probe
from omega_tail.interfaces.shared.messages import localized
from omega_tail.interfaces.tui.screens._base import OmegaScreen
from omega_tail.interfaces.tui.screens.confirm import ConfirmScreen
from omega_tail.interfaces.tui.widgets.status_band import StatusBand
from omega_tail.interfaces.tui.widgets.tables import WideTable
from omega_tail.shared.i18n import _

if TYPE_CHECKING:
    from omega_tail.interfaces.tui.app import OmegaTailApp

COLUMNS = ("Port", "Pour", "Mode", "Chemin", "Protection", "Cible")


def protection(handler: Handler) -> str:
    if not handler.public:
        return _("tailnet seul")
    if handler.proxy_protocol == 2 and handler.target.startswith("tcp://127.0.0.1:"):
        return _("par la porte ✔")
    if handler.kind in ("https", "tls-terminated-tcp"):
        return _("non protégé")
    return _("direct")


def probe_text(probe: Probe, handler: Handler) -> str:
    where = _("depuis Internet (relais Funnel {via})") if handler.public else _("par le tailnet ({via})")
    head = ("✔ " if probe.ok else "✖ ") + _("{kind} {port}{path} {where} : {detail}").format(
        kind=handler.kind, port=handler.port, path=handler.path if handler.path not in ("", "/") else "",
        where=where.format(via=probe.via or "?"), detail=localized(probe.detail))
    lines = [head]
    if probe.milliseconds:
        lines.append(_("Temps : {ms:.0f} ms").format(ms=probe.milliseconds))
    certificate = probe.certificate
    if certificate is not None:
        expiry = certificate.not_after.strftime("%Y-%m-%d") if certificate.not_after else "?"
        lines.append(_("Certificat : {subject} · émis par {issuer} · échéance {expiry} · {tls}").format(
            subject=certificate.subject or "?", issuer=certificate.issuer or "?", expiry=expiry,
            tls=certificate.tls_version or "TLS"))
    if not probe.ok and handler.public and probe.detail.startswith("DNS public"):
        lines.append(_("Le nom n'est pas encore publié pour Internet : juste après un ajout, Funnel met parfois une "
                       "minute. Réessayez."))
    if not probe.ok and not handler.public:
        lines.append(_("Un essai par le tailnet depuis la machine elle-même peut échouer selon le système : "
                       "essayez aussi depuis un autre appareil."))
    return "\n".join(lines)


class PublicationScreen(OmegaScreen):
    def __init__(self) -> None:
        super().__init__()
        self._handlers: tuple[Handler, ...] = ()
        self._backups: list[Backup] = []

    def compose(self) -> ComposeResult:
        app: OmegaTailApp = self.app  # type: ignore[assignment]
        yield Header()
        yield StatusBand(app.snapshot)
        with VerticalScroll(classes="omega-panel"):
            yield Static(_("PUBLICATION"), classes="omega-title")
            yield Static(_("Ce que cette machine publie : pour le tailnet seul (Serve) ou pour Internet (Funnel). "
                           "Chaque changement est vérifié, et l'état d'avant est sauvegardé (restaurable en un "
                           "bouton)."), classes="omega-hint")
            table = WideTable(id="pub-table", cursor_type="row", zebra_stripes=True)
            table.add_columns(*(_(column) for column in COLUMNS))
            yield table
            yield Static("", id="pub-note", classes="omega-hint", markup=False)
            with Horizontal(classes="omega-actions"):
                with Container(classes="omega-btn-frame"):
                    yield Button(_("Essai de bout en bout"), id="test", variant="primary")
                with Container(classes="omega-btn-frame"):
                    yield Button(_("Retirer"), id="remove", variant="error")
                with Container(classes="omega-btn-frame"):
                    yield Button(_("Suspendre Funnel"), id="suspend")
                with Container(classes="omega-btn-frame"):
                    yield Button(_("Rétablir Funnel"), id="resume")
            yield Static("", id="test-result", classes="tail-box", markup=False)

            yield Rule(classes="tail-separator")
            yield Static(_("AJOUTER"), classes="omega-subtitle")
            yield Static(_("Pour Internet, le plus sûr : HTTPS sur le port 443, puis « Activer la protection » "
                           "(Pare-feu Funnel) pour que la porte filtre avant tout chiffrement."), classes="omega-hint")
            with Horizontal(classes="omega-actions"):
                yield Static(_("Service local"), classes="tail-label tail-wide-label")
                yield Input(placeholder=_("8080 ou http://127.0.0.1:8080"), id="add-target")
            with Horizontal(classes="omega-actions"):
                yield Static(_("Pour"), classes="tail-label tail-wide-label")
                yield Select([(_("le tailnet seul (Serve)"), "tailnet"), (_("Internet (Funnel)"), "internet")],
                             value="tailnet", allow_blank=False, id="add-who", classes="tail-pref-select")
            with Horizontal(classes="omega-actions"):
                yield Static(_("Mode"), classes="tail-label tail-wide-label")
                yield Select([(kind, kind) for kind in KINDS], value="https", allow_blank=False, id="add-kind",
                             classes="tail-pref-select")
            with Horizontal(classes="omega-actions"):
                yield Static(_("Port (Funnel : 443, 8443, 10000)"), classes="tail-label tail-wide-label")
                yield Input("443", id="add-port", classes="tail-number")
            with Horizontal(classes="omega-actions"):
                yield Static(_("Chemin (HTTPS / HTTP)"), classes="tail-label tail-wide-label")
                yield Input("/", id="add-path", classes="tail-number")
            with Horizontal(classes="omega-actions"), Container(classes="omega-btn-frame"):
                yield Button(_("Publier"), id="add", variant="primary")

            yield Rule(classes="tail-separator")
            yield Static(_("SAUVEGARDES"), classes="omega-subtitle")
            yield Static(_("L'état d'avant chaque changement (publication, pare-feu, disjoncteur) ; les 50 plus "
                           "récentes sont gardées dans var/funnel/sauvegardes/."), classes="omega-hint")
            with Horizontal(classes="omega-actions"):
                yield Select([], prompt=_("Aucune sauvegarde"), id="backup")
                with Container(classes="omega-btn-frame"):
                    yield Button(_("Restaurer"), id="restore")
        with Horizontal(classes="omega-actions omega-fixed-actions"):
            with Container(classes="omega-btn-frame"):
                yield Button(_("Pare-feu Funnel"), id="firewall")
            with Container(classes="omega-btn-frame"):
                yield Button(_("Retour"), id="back")
        yield Footer()

    # ---- lecture ----
    def on_mount(self) -> None:
        self.query_one("#test-result", Static).display = False
        snapshot = getattr(self.app, "snapshot", None)
        if snapshot is not None:
            self.show_snapshot(snapshot)
        self.refresh_state()

    def show_snapshot(self, snapshot: Snapshot) -> None:
        self.query_one(StatusBand).show(snapshot)
        self._show_buttons(snapshot)
        self.refresh_state()

    def refresh_state(self) -> None:
        app: OmegaTailApp = self.app  # type: ignore[assignment]
        tools = app.publication
        if tools is None:
            return

        def work() -> None:
            try:
                handlers, backups = tools.handlers(), tools.backups()
            except (OSError, ValueError) as error:
                self.app.call_from_thread(self._show_error, str(error))
                return
            self.app.call_from_thread(self._show, handlers, backups)

        self.run_worker(work, thread=True, group="publication-read", exclusive=True)

    def _show_error(self, error: str) -> None:
        self.query_one("#pub-note", Static).update(_("Publication illisible : {error}").format(error=error))

    def _show(self, handlers: tuple[Handler, ...], backups: list[Backup]) -> None:
        if handlers != self._handlers or not self.query_one("#pub-table", WideTable).row_count:
            self._handlers = handlers
            table = self.query_one("#pub-table", WideTable)
            row = table.cursor_row
            table.clear()
            for handler in handlers:
                table.add_row(str(handler.port), _("Internet") if handler.public else _("tailnet"), handler.kind,
                              handler.path or "—", protection(handler), handler.target)
            if handlers:
                table.move_cursor(row=min(row, len(handlers) - 1))
        notes = [] if handlers else [_("Rien n'est publié. « Publier » ci-dessous pour commencer.")]
        if not self._operator():
            notes.append(_("Pour changer la publication, devenez opérateur de Tailscale (tableau de bord)."))
        self.query_one("#pub-note", Static).update("\n".join(notes))
        paths = [backup.path for backup in backups]
        if paths != [backup.path for backup in self._backups]:
            self._backups = backups
            select = self.query_one("#backup", Select)
            select.set_options([(f"{item.when} · {_(item.origin)} · {item.summary}", item.path) for item in backups])
        has = bool(handlers)
        self.query_one("#test", Button).disabled = not has
        self.query_one("#remove", Button).disabled = not has or not self._operator()

    def _show_buttons(self, snapshot: Snapshot) -> None:
        operator = snapshot.is_operator
        for name in ("add", "restore"):
            self.query_one(f"#{name}", Button).disabled = not operator
        suspend, resume = self.query_one("#suspend", Button), self.query_one("#resume", Button)
        if suspend.parent is not None:
            suspend.parent.display = snapshot.cut is None
        if resume.parent is not None:
            resume.parent.display = snapshot.cut is not None
        suspend.disabled = not snapshot.funnel or not operator

    def _operator(self) -> bool:
        app: OmegaTailApp = self.app  # type: ignore[assignment]
        return app.snapshot is not None and app.snapshot.is_operator

    def selected(self) -> Handler | None:
        table = self.query_one("#pub-table", WideTable)
        if not self._handlers or table.cursor_row < 0 or table.cursor_row >= len(self._handlers):
            return None
        return self._handlers[table.cursor_row]

    # ---- actions ----
    def on_button_pressed(self, event: Button.Pressed) -> None:
        app: OmegaTailApp = self.app  # type: ignore[assignment]
        button = event.button.id
        if button == "back":
            self.action_back()
        elif button == "firewall":
            app.open_key("firewall")
        elif button == "suspend":
            app.ask_cut(None)
        elif button == "resume":
            app.restore_funnel()
        elif button == "test":
            self.test_selected()
        elif button == "remove":
            self.remove_selected()
        elif button == "add":
            self.add_publication()
        elif button == "restore":
            self.restore_backup()

    def test_selected(self) -> None:
        app: OmegaTailApp = self.app  # type: ignore[assignment]
        tools, handler, snapshot = app.publication, self.selected(), app.snapshot
        if tools is None or handler is None or snapshot is None:
            return
        host = snapshot.tailscale.dns_name
        address = next((item for item in snapshot.tailscale.addresses if "." in item), "")
        result = self.query_one("#test-result", Static)
        result.display = True
        result.update(_("Essai en cours…"))

        def work() -> None:
            probe = tools.test(handler, host, address)
            self.app.call_from_thread(self.query_one("#test-result", Static).update, probe_text(probe, handler))

        self.run_worker(work, thread=True, group="publication-test", exclusive=True)

    def remove_selected(self) -> None:
        app: OmegaTailApp = self.app  # type: ignore[assignment]
        handler = self.selected()
        if handler is None:
            return
        command = " ".join(remove_command(handler, self._handlers))
        text = _("Retire {kind} {port}{path} → {target} ({who}). L'état d'avant est sauvegardé.\n\nCommande : "
                 "{command}").format(kind=handler.kind, port=handler.port,
                                     path=handler.path if handler.path not in ("", "/") else "",
                                     target=handler.target, who=_("Internet") if handler.public else _("tailnet"),
                                     command=command)
        self.app.push_screen(ConfirmScreen(title=_("RETIRER CETTE PUBLICATION ?"), text=text, yes=_("Retirer"),
                                           no=_("Annuler")),
                             lambda confirmed: app.publication_action(lambda tools: tools.remove(handler),
                                                                      self.refresh_state) if confirmed else None)

    def add_publication(self) -> None:
        app: OmegaTailApp = self.app  # type: ignore[assignment]
        port_text = self.query_one("#add-port", Input).value.strip()
        request = AddRequest(kind=str(self.query_one("#add-kind", Select).value),
                             port=int(port_text) if port_text.isdigit() else 0,
                             target=self.query_one("#add-target", Input).value,
                             public=self.query_one("#add-who", Select).value == "internet",
                             path=self.query_one("#add-path", Input).value)
        if request.public:
            text = _("Le service {target} sera joignable depuis Internet (Funnel, port {port}). Pensez ensuite à "
                     "« Activer la protection » (Pare-feu Funnel).").format(target=request.target or "?",
                                                                            port=request.port)
            self.app.push_screen(ConfirmScreen(title=_("PUBLIER SUR INTERNET ?"), text=text, yes=_("Publier"),
                                               no=_("Annuler")),
                                 lambda confirmed: app.publication_action(lambda tools: tools.add(request),
                                                                          self.refresh_state) if confirmed else None)
            return
        app.publication_action(lambda tools: tools.add(request), self.refresh_state)

    def restore_backup(self) -> None:
        app: OmegaTailApp = self.app  # type: ignore[assignment]
        value = self.query_one("#backup", Select).value
        backup = next((item for item in self._backups if item.path == value), None)
        if backup is None:
            self.app.notify(_("Choisissez une sauvegarde."))
            return
        text = _("La publication redevient celle du {when} ({origin}) : {summary}.\nL'état actuel est sauvegardé "
                 "d'abord ; tout est vérifié, et remis comme avant en cas d'échec.").format(
            when=backup.when, origin=_(backup.origin), summary=backup.summary)
        self.app.push_screen(ConfirmScreen(title=_("RESTAURER CETTE SAUVEGARDE ?"), text=text, yes=_("Restaurer"),
                                           no=_("Annuler")),
                             lambda confirmed: app.publication_action(lambda tools: tools.restore(backup.path),
                                                                      self.refresh_state) if confirmed else None)
