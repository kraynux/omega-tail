# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Connexion et reglages (lot 5, proposition §3.3) : connexion, compte, et les preferences de `tailscale set`
presentees en cases et champs, chacune avec sa phrase d'explication. Les changements en attente s'affichent pendant
la saisie (avant -> apres et commande), au-dessus de « Appliquer » ; apres application, le resultat reste ecrit, verifie
sur les valeurs relues.

Les valeurs sont lues une fois a l'ouverture (puis apres chaque application) : la relecture toutes les 5 s ne
remplace jamais ce que l'utilisateur est en train de modifier."""
from __future__ import annotations

from collections.abc import Mapping
from datetime import datetime
from typing import TYPE_CHECKING

from textual.app import ComposeResult
from textual.containers import Container, Horizontal, VerticalScroll
from textual.widgets import Button, Checkbox, Footer, Header, Input, Rule, Select, Static

from omega_tail.domain.forwarding import SYSCTL_PATH as FORWARD_PATH
from omega_tail.domain.forwarding import Forwarding, needs_forwarding
from omega_tail.domain.preferences import PREFS, Group, Kind, PrefSpec
from omega_tail.domain.snapshot import Snapshot
from omega_tail.domain.tailscale import BackendState, ExitNode, Profile
from omega_tail.interfaces.tui.screens._base import OmegaScreen
from omega_tail.interfaces.tui.screens.confirm import ConfirmScreen
from omega_tail.interfaces.tui.screens.typed_confirm import TypedConfirmScreen
from omega_tail.interfaces.tui.widgets.status_band import StatusBand
from omega_tail.shared.i18n import N_, _

if TYPE_CHECKING:
    from omega_tail.application.connection import SettingsPlan
    from omega_tail.interfaces.tui.app import OmegaTailApp

NO_EXIT_NODE = "__aucun__"
STATES = {BackendState.RUNNING: N_("connecté"), BackendState.STOPPED: N_("déconnecté (tailscale down)"),
          BackendState.NEEDS_LOGIN: N_("compte à connecter"),
          BackendState.NEEDS_MACHINE_AUTH: N_("machine à approuver"), BackendState.STARTING: N_("démarrage")}


def widget_id(spec: PrefSpec) -> str:
    return f"pref-{spec.name}"


class ConnectionScreen(OmegaScreen):
    def __init__(self) -> None:
        super().__init__()
        self._loaded: dict[str, str] = {}
        self._lists_read = False
        self._reload = True
        self._profiles: tuple[Profile, ...] = ()
        self._exit_nodes: tuple[ExitNode, ...] = ()
        self._applied: SettingsPlan | None = None
        self._applied_code = 0
        self._applied_at = ""

    def compose(self) -> ComposeResult:
        app: OmegaTailApp = self.app  # type: ignore[assignment]
        yield Header()
        yield StatusBand(app.snapshot)
        with VerticalScroll(classes="omega-panel"):
            yield Static(_("CONNEXION ET RÉGLAGES"), classes="omega-title")
            yield Static(_("La connexion de cette machine au tailnet, son compte, et les réglages de Tailscale. "
                           "Chaque commande s'affiche avant d'être lancée, dans le terminal (sans sudo si vous êtes "
                           "opérateur)."), classes="omega-hint")
            yield Static("", id="conn-state", classes="tail-box", markup=False)
            with Horizontal(classes="omega-actions"):
                with Container(classes="omega-btn-frame"):
                    yield Button(_("Se connecter"), id="up", variant="primary")
                with Container(classes="omega-btn-frame"):
                    yield Button(_("Se déconnecter"), id="down")
                with Container(classes="omega-btn-frame"):
                    yield Button(_("Ajouter un compte"), id="login")
                with Container(classes="omega-btn-frame"):
                    yield Button(_("Déconnexion définitive"), id="logout", variant="error")

            yield Rule(classes="tail-separator")
            yield Static(_("COMPTE"), classes="omega-subtitle")
            with Horizontal(classes="omega-actions"):
                yield Select([], prompt=_("Comptes de cette machine (lecture…)"), id="profile")
                with Container(classes="omega-btn-frame"):
                    yield Button(_("Changer de compte"), id="switch", disabled=True)
            yield Static("", id="profile-note", classes="omega-hint", markup=False)

            for group in Group:
                yield Static(_(group.value).upper(), classes="omega-subtitle tail-gap")
                for spec in (item for item in PREFS if item.group is group):
                    yield from self._control(spec)
        with VerticalScroll(id="changes-frame"):
            yield Static("", id="changes", markup=False)
        with Horizontal(classes="omega-actions omega-fixed-actions"):
            with Container(classes="omega-btn-frame"):
                yield Button(_("Appliquer"), id="apply", variant="primary")
            with Container(classes="omega-btn-frame"):
                yield Button(_("Relire"), id="reload")
            with Container(classes="omega-btn-frame"):
                yield Button(_("Retour"), id="back")
        yield Footer()

    def _control(self, spec: PrefSpec) -> ComposeResult:
        if spec.kind is Kind.BOOL:
            yield Checkbox(_(spec.label), id=widget_id(spec))
        else:
            with Horizontal(classes="omega-actions"):
                yield Static(_(spec.label), classes="tail-label tail-wide-label")
                if spec.kind is Kind.CHOICE:
                    options = [(choice, choice) for choice in spec.choices] or [(_("aucun"), NO_EXIT_NODE)]
                    yield Select(options, allow_blank=False, id=widget_id(spec), classes="tail-pref-select")
                else:
                    yield Input(id=widget_id(spec), classes="tail-pref-input",
                                placeholder=_(spec.example) if spec.example else "")
                    if spec.name == "operator":
                        yield Button(_("Mon compte"), id="operator-me")
        yield Static(_(spec.hint), classes="omega-hint tail-pref-hint", markup=False)
        if spec.name == "exit-node":
            yield Static("", id="exit-note", classes="omega-hint tail-pref-hint", markup=False)
        if spec.name == "advertise-routes":
            yield Static("", id="forward-note", classes="tail-box", markup=False)
            with Horizontal(classes="omega-actions", id="forward-row"), Container(classes="omega-btn-frame"):
                yield Button(_("Activer le transfert IP"), id="forward-on")

    # ---- lecture ----
    def on_mount(self) -> None:
        snapshot = getattr(self.app, "snapshot", None)
        if snapshot is not None:
            self.show_snapshot(snapshot)
        self.load_lists()

    def load_lists(self) -> None:
        app: OmegaTailApp = self.app  # type: ignore[assignment]
        tools = app.connection
        if tools is None:
            return

        def work() -> None:
            profiles, error = tools.profiles()
            nodes = tools.exit_nodes()
            self.app.call_from_thread(self._show_lists, profiles, error, nodes)

        self.run_worker(work, thread=True, group="connection-lists", exclusive=True)

    def _show_lists(self, profiles: tuple[Profile, ...], error: str, nodes: tuple[ExitNode, ...]) -> None:
        self._profiles, self._exit_nodes, self._lists_read = profiles, nodes, True
        select = self.query_one("#profile", Select)
        select.set_options([(f"{item.account} · {item.tailnet}" + (_(" (en cours)") if item.current else ""),
                             item.profile_id) for item in profiles])
        current = next((item.profile_id for item in profiles if item.current), None)
        if current is not None:
            select.value = current
        self.query_one("#switch", Button).disabled = len(profiles) < 2
        note = ""
        if error:
            note = _("Comptes illisibles ({error}) : devenez opérateur (tableau de bord).").format(error=error)
        elif len(profiles) < 2:
            note = _("Un seul compte sur cette machine : « Ajouter un compte » pour en connecter un autre.")
        self.query_one("#profile-note", Static).update(note)
        self._fill_exit_nodes(self._loaded.get("exit-node", ""))

    def _fill_exit_nodes(self, current: str) -> None:
        select = self.query_one("#pref-exit-node", Select)
        options = [(_("aucun"), NO_EXIT_NODE)]
        options += [(f"{node.name} ({node.address})" + (f" · {node.status}" if node.status else ""), node.address)
                    for node in self._exit_nodes]
        if current and all(value != current for _label, value in options):
            options.append((current, current))
        select.set_options(options)
        select.value = current or NO_EXIT_NODE
        note = self.query_one("#exit-note", Static)
        empty = self._lists_read and not self._exit_nodes
        note.update("" if not empty else _(
            "Aucune machine du tailnet ne se propose comme nœud de sortie. Sur la machine voulue : cocher « Proposer "
            "cette machine comme nœud de sortie », appliquer, puis l'approuver dans la console d'administration de "
            "Tailscale (Machines → Edit route settings)."))
        note.display = empty

    def show_snapshot(self, snapshot: Snapshot) -> None:
        self.query_one(StatusBand).show(snapshot)
        self._show_state(snapshot)
        if snapshot.user and snapshot.user != "root":
            self.query_one("#pref-operator", Input).placeholder = _("ex. {user}").format(user=snapshot.user)
        self.show_forwarding()
        if self._reload and snapshot.preferences.readable:
            self._reload = False
            self._fill(snapshot.preferences.values)

    def _show_state(self, snapshot: Snapshot) -> None:
        state = snapshot.tailscale
        expiry = state.key_expiry.strftime("%Y-%m-%d") if state.key_expiry else _("aucune")
        lines = [
            _("État : {state}").format(state=_(STATES.get(state.backend, state.backend.value))
                                       if state.reachable else _("tailscaled ne répond pas")),
            _("Compte : {user} · tailnet : {tailnet}").format(user=state.user or "—", tailnet=state.tailnet or "—"),
            _("Machine : {name} · {addresses}").format(name=state.dns_name or state.host_name or "—",
                                                       addresses=", ".join(state.addresses) or "—"),
            _("Expiration de la clé : {expiry} · opérateur : {operator}").format(
                expiry=expiry, operator=snapshot.preferences.operator or _("aucun (sudo)")),
        ]
        if snapshot.through_tailscale:
            lines.append("⚠ " + _("Votre session passe par Tailscale : se déconnecter vous couperait."))
        self.query_one("#conn-state", Static).update("\n".join(lines))
        running = state.backend is BackendState.RUNNING
        self.query_one("#up", Button).disabled = not state.reachable or running
        self.query_one("#down", Button).disabled = not running
        self.query_one("#logout", Button).disabled = not state.reachable or state.backend is BackendState.NEEDS_LOGIN

    def _forwarding(self) -> Forwarding:
        app: OmegaTailApp = self.app  # type: ignore[assignment]
        return app.connection.forwarding() if app.connection is not None else Forwarding()

    def _forwarding_needed(self) -> bool:
        return bool(self._loaded) and needs_forwarding(self.wanted_settings())

    def show_forwarding(self) -> None:
        """Avertit quand la machine se propose comme noeud de sortie ou routeur sans transfert IP du noyau."""
        missing = self._forwarding().missing
        shown = bool(missing) and self._forwarding_needed()
        self.query_one("#forward-note", Static).update(("⚠ " + _(
            "Transfert IP désactivé ({keys}) : le nœud de sortie et les sous-réseaux annoncés ne transmettront rien. "
            "« Activer le transfert IP » écrit un fichier à part ({path}), gardé au redémarrage.").format(
            keys=", ".join(missing), path=FORWARD_PATH)) if shown else "")
        self.query_one("#forward-note", Static).display = shown
        self.query_one("#forward-row", Horizontal).display = shown

    def on_checkbox_changed(self, event: Checkbox.Changed) -> None:
        if (event.checkbox.id or "").startswith("pref-"):
            self.show_forwarding()
            self.show_changes()

    def on_input_changed(self, event: Input.Changed) -> None:
        if (event.input.id or "").startswith("pref-"):
            self.show_forwarding()
            self.show_changes()

    def on_select_changed(self, event: Select.Changed) -> None:
        if (event.select.id or "").startswith("pref-"):
            self.show_changes()

    def fill_operator(self) -> None:
        """Met le compte qui a lance omega-tail (celui d'avant sudo) dans le champ Operateur."""
        snapshot = getattr(self.app, "snapshot", None)
        user = snapshot.user if snapshot is not None else ""
        if not user or user == "root":
            self.app.notify(_("Compte inconnu ou root : tapez le nom du compte Linux à rendre opérateur."))
            return
        self.query_one("#pref-operator", Input).value = user
        self.preview_settings()

    def _fill(self, values: Mapping[str, str]) -> None:
        current = dict(values)
        self._loaded = current
        for spec in PREFS:
            known = spec.name in current
            value = current.get(spec.name, "")
            if spec.kind is Kind.BOOL:
                box = self.query_one(f"#{widget_id(spec)}", Checkbox)
                box.value, box.disabled = value == "true", not known
            elif spec.name == "exit-node":
                self._fill_exit_nodes(value)
                self.query_one(f"#{widget_id(spec)}", Select).disabled = not known
            elif spec.kind is Kind.CHOICE:
                select = self.query_one(f"#{widget_id(spec)}", Select)
                if value in spec.choices:
                    select.value = value
                select.disabled = not known
            else:
                field = self.query_one(f"#{widget_id(spec)}", Input)
                field.value, field.disabled = value, not known
        self.show_forwarding()
        self.show_changes()

    def wanted_settings(self) -> dict[str, str]:
        found: dict[str, str] = {}
        for spec in PREFS:
            if spec.name not in self._loaded:
                continue
            if spec.kind is Kind.BOOL:
                found[spec.name] = "true" if self.query_one(f"#{widget_id(spec)}", Checkbox).value else "false"
            elif spec.kind is Kind.CHOICE:
                value = str(self.query_one(f"#{widget_id(spec)}", Select).value)
                found[spec.name] = "" if value == NO_EXIT_NODE else value
            else:
                found[spec.name] = self.query_one(f"#{widget_id(spec)}", Input).value
        return found

    # ---- changements ----
    def plan_settings(self) -> SettingsPlan | None:
        app: OmegaTailApp = self.app  # type: ignore[assignment]
        if app.connection is None:
            return None
        operator = app.snapshot is not None and app.snapshot.is_operator
        return app.connection.plan(self._loaded, self.wanted_settings(), operator=operator)

    def describe_plan(self, plan: SettingsPlan) -> str:
        app: OmegaTailApp = self.app  # type: ignore[assignment]
        lines = []
        for name, reason in plan.problems.items():
            lines.append("✖ " + _("{name} : {reason}").format(name=name, reason=_(reason).format(
                value=self.wanted_settings().get(name, ""))))
        for change in plan.changes:
            lines.append(_("{label} : {before} → {after}").format(label=_(change.spec.label),
                                                                   before=change.before or "∅",
                                                                   after=change.after or "∅"))
        if not lines:
            return _("Aucun changement.")
        if plan.command:
            lines += ["", _("Commande :"), "  " + " ".join(plan.command)]
        missing = self._forwarding().missing
        if missing and needs_forwarding({change.name: change.after for change in plan.changes}):
            lines += ["", "⚠ " + _("Transfert IP désactivé ({keys}) : « Activer le transfert IP » aussi.").format(
                keys=", ".join(missing))]
        through = app.snapshot is not None and app.snapshot.through_tailscale
        if through and plan.cuts_session:
            lines += ["", "⚠ " + _("Votre session passe par Tailscale ; ces changements peuvent la couper : {names}.")
                      .format(names=", ".join(_(change.spec.label) for change in plan.cuts_session))]
        return "\n".join(lines)

    def describe_result(self) -> str:
        """Resultat de la derniere application, verifie sur les valeurs relues (pas sur la commande seule)."""
        plan = self._applied
        if plan is None:
            return ""
        if self._applied_code != 0:
            head = "✖ " + _("Dernière application ({time}) : la commande a échoué (code {code}).").format(
                time=self._applied_at, code=self._applied_code)
        else:
            head = _("Dernière application ({time}) :").format(time=self._applied_at)
        lines = [head]
        for change in plan.changes:
            now = self._loaded.get(change.name)
            if now == change.after:
                lines.append("✔ " + _("{label} : {after}").format(label=_(change.spec.label),
                                                                  after=change.after or "∅"))
            else:
                lines.append("✖ " + _("{label} : {after} demandé, {now} lu").format(
                    label=_(change.spec.label), after=change.after or "∅", now=now or "∅"))
        return "\n".join(lines)

    def show_changes(self) -> None:
        """Changements en attente pendant la saisie ; sinon le resultat de la derniere application ; sinon rien."""
        plan = self.plan_settings() if self._loaded else None
        if plan is not None and (plan.changes or plan.problems):
            text = _("À appliquer :") + "\n" + self.describe_plan(plan)
        else:
            text = self.describe_result()
        self.query_one("#changes", Static).update(text)
        self.query_one("#changes-frame", VerticalScroll).display = bool(text)

    def preview_settings(self) -> None:
        self.show_changes()

    def apply_settings(self) -> None:
        plan = self.plan_settings()
        if plan is None:
            return
        text = self.describe_plan(plan)
        self.show_changes()
        if plan.problems:
            self.app.notify(_("Valeur refusée : corrigez la ligne marquée ✖."), severity="error")
            return
        if not plan.command:
            self.app.notify(_("Aucun changement."))
            return
        self.app.push_screen(ConfirmScreen(title=_("APPLIQUER LES RÉGLAGES ?"), text=text, yes=_("Appliquer"),
                                           no=_("Annuler")),
                             lambda confirmed: self._apply(plan) if confirmed else None)

    def _apply(self, plan: SettingsPlan) -> None:
        self._applied, self._applied_at = plan, datetime.now().strftime("%H:%M")
        self._applied_code = self._run([plan.command])

    def _run(self, commands: list[tuple[str, ...]]) -> int:
        app: OmegaTailApp = self.app  # type: ignore[assignment]
        code = app.run_in_terminal(commands)
        self._reload = True
        app.request_refresh()
        self.load_lists()
        return code

    # ---- connexion ----
    def _operator(self) -> bool:
        app: OmegaTailApp = self.app  # type: ignore[assignment]
        return app.snapshot is not None and app.snapshot.is_operator

    def _cut_warning(self) -> str:
        app: OmegaTailApp = self.app  # type: ignore[assignment]
        snapshot = app.snapshot
        notes = []
        if snapshot is not None and snapshot.through_tailscale:
            notes.append("⚠ " + _("Votre session passe par Tailscale : elle sera COUPÉE et ne reviendra pas. Il "
                                  "faudra un accès local (ou un autre chemin) pour vous reconnecter."))
        if snapshot is not None and snapshot.publications:
            notes.append("⚠ " + _("Ce qui est publié (Serve et Funnel) ne sera plus joignable."))
        return ("\n\n" + "\n".join(notes)) if notes else ""

    def on_button_pressed(self, event: Button.Pressed) -> None:
        app: OmegaTailApp = self.app  # type: ignore[assignment]
        tools, button, operator = app.connection, event.button.id, self._operator()
        if button == "back":
            self.action_back()
        elif button == "apply":
            self.apply_settings()
        elif button == "forward-on" and tools is not None:
            app.confirm_commands(_("ACTIVER LE TRANSFERT IP ?"), _(
                "Le noyau fera suivre les paquets (IPv4 et IPv6) : nécessaire pour un nœud de sortie ou des "
                "sous-réseaux annoncés. Fichier à part {path}, relu au démarrage (systemd, OpenRC, runit) ; pour "
                "annuler : supprimer ce fichier puis redémarrer.").format(path=FORWARD_PATH),
                [tools.enable_forwarding()])
        elif button == "operator-me":
            self.fill_operator()
        elif button == "reload":
            self._reload = True
            app.request_refresh()
            self.load_lists()
        elif tools is None:
            return
        elif button == "up":
            app.confirm_commands(_("SE CONNECTER ?"), _(
                "Remet cette machine dans le tailnet. Si un compte doit s'identifier, Tailscale affiche dans le "
                "terminal l'adresse à ouvrir dans un navigateur."), [tools.up(operator=operator)])
        elif button == "down":
            app.confirm_commands(_("SE DÉCONNECTER ?"), _(
                "La machine quitte le tailnet (le compte reste enregistré : « Se connecter » la remet).")
                + self._cut_warning(), [tools.down(operator=operator)])
        elif button == "login":
            app.confirm_commands(_("AJOUTER UN COMPTE ?"), _(
                "Connecte un autre compte (ou un autre tailnet) sur cette machine ; il devient le compte en cours. "
                "Tailscale affiche l'adresse à ouvrir pour vous identifier. L'ancien compte reste dans « Changer de "
                "compte »."), [tools.login(operator=operator)])
        elif button == "switch":
            self._switch(operator)
        elif button == "logout":
            self._logout(operator)

    def _switch(self, operator: bool) -> None:
        app: OmegaTailApp = self.app  # type: ignore[assignment]
        tools = app.connection
        value = self.query_one("#profile", Select).value
        chosen = next((item for item in self._profiles if item.profile_id == value), None)
        if tools is None or chosen is None or chosen.current:
            self.app.notify(_("Choisissez un autre compte que le compte en cours."))
            return
        app.confirm_commands(_("CHANGER DE COMPTE ?"), _(
            "La machine passe sur le compte {account} (tailnet {tailnet}). Son adresse et ce qu'elle voit du "
            "tailnet changent.").format(account=chosen.account, tailnet=chosen.tailnet or "—")
            + self._cut_warning(), [tools.switch(chosen.profile_id, operator=operator)])

    def _logout(self, operator: bool) -> None:
        app: OmegaTailApp = self.app  # type: ignore[assignment]
        tools, snapshot = app.connection, app.snapshot
        if tools is None:
            return
        word = (snapshot.tailscale.host_name if snapshot is not None else "") or "logout"
        command = tools.logout(operator=operator)
        text = _("La machine est retirée du compte : sa clé est révoquée, il faudra s'identifier à nouveau (et "
                 "peut-être la réapprouver) pour la remettre dans le tailnet.\n\nCommande : {command}").format(
            command=" ".join(command)) + self._cut_warning() + "\n\n" + _(
            "Pour confirmer, tapez le nom de la machine : {word}").format(word=word)
        self.app.push_screen(TypedConfirmScreen(title=_("DÉCONNEXION DÉFINITIVE ?"), text=text, word=word,
                                                yes=_("Déconnecter"), no=_("Annuler")),
                             lambda confirmed: None if not confirmed else self._run_quiet([command]))

    def _run_quiet(self, commands: list[tuple[str, ...]]) -> None:
        self._run(commands)
