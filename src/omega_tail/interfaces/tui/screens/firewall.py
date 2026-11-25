# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Pare-feu Funnel (lot 4, proposition §4.1) : la porte HAProxy qui refuse les connexions abusives avant tout
chiffrement. Etat, activation pas a pas (avec retour arriere automatique), regles appliquees a chaud, listes de
confiance et noire, certificat."""
from __future__ import annotations

from typing import TYPE_CHECKING

from textual.app import ComposeResult
from textual.containers import Container, Horizontal, VerticalScroll
from textual.widgets import Button, Checkbox, Footer, Header, Input, Rule, Select, Static

from omega_tail.application.gate import GateTools
from omega_tail.application.groups import GroupsStatus
from omega_tail.application.survival import Outcome
from omega_tail.domain.gate import MODE_NORMAL, MODE_OBSERVATION
from omega_tail.domain.geo import ATTRIBUTION
from omega_tail.domain.groups import GROUPS_APPLY, GROUPS_OBSERVE, GroupsPolicy, reason_pairs
from omega_tail.domain.snapshot import Snapshot
from omega_tail.interfaces.tui.screens._base import OmegaScreen
from omega_tail.interfaces.tui.widgets.busy import Busy
from omega_tail.interfaces.tui.widgets.status_band import StatusBand
from omega_tail.shared.i18n import N_, _

if TYPE_CHECKING:
    from omega_tail.interfaces.tui.app import OmegaTailApp

NUMBERS = (("ip_per_10s", N_("Connexions par adresse / 10 s")), ("prefix_per_10s", N_("Par préfixe /24 ou /64 / 10 s")),
           ("global_per_s", N_("Budget global (admises / s)")), ("max_connections", N_("Connexions simultanées")),
           ("block_minutes", N_("Durée de blocage (min)")))


GROUP_NUMBERS = (("attack_per_s", N_("Mode attaque au-delà de (entrantes / s)")),
                 ("calm_minutes", N_("Retour au normal après (min de calme)")),
                 ("ja4_per_10s", N_("Empreinte inconnue / 10 s")), ("as_per_10s", N_("AS d'hébergeur / 10 s")),
                 ("country_per_10s", N_("Pays limité / 10 s")))


def groups_text(status: GroupsStatus) -> str:
    if not status.lua:
        return _("HAProxy sans Lua : regroupements indisponibles (la porte du lot 4 protège seule).")
    applied = status.policy.mode == GROUPS_APPLY
    lines = [_("Regroupements : appliqués (refusent en mode attaque)") if applied
             else _("Regroupements : en observation (comptent « aurait refusé », ne refusent rien)")]
    lines.append(_("Mode : ATTAQUE — retour au normal après {seconds} s de calme").format(seconds=status.calm_left_s)
                 if status.attack else _("Mode : normal"))
    if status.learning_days_left:
        lines.append(_("Empreintes : apprentissage, encore {days} jour(s) ; les regroupements restent en "
                       "observation jusqu'à la fin.").format(days=status.learning_days_left))
    elif applied:
        lines.append(_("Empreintes habituelles : {count} (référence prête)").format(count=status.known))
    else:
        lines.append(_("Empreintes habituelles : {count} (référence prête) ; « appliqués » est maintenant "
                       "possible.").format(count=status.known))
    if status.base_days is None:
        lines.append(_("Base AS / pays : absente (« Mettre à jour la base », ou la veille une fois par mois)"))
    else:
        lines.append(_("Base AS / pays : à jour il y a {days} jour(s) ; renouvelée chaque mois par la veille")
                     .format(days=status.base_days))
    if status.reasons:
        text = (_("Connexions refusées (7 j) : {found}") if applied
                else _("Connexions qui auraient été refusées (7 j) : {found}"))
        lines.append(text.format(
            found=", ".join(f"{_(label)} {count}" for label, count in reason_pairs(status.reasons))))
    lines.append(_("Navigateurs courants (Chrome, Edge, Firefox) jamais limités par ces règles."))
    lines.append(ATTRIBUTION)
    return "\n".join(lines)


def refresh_base(gate: GateTools) -> Outcome:
    return gate.refresh_base()


def restart_learning(gate: GateTools) -> Outcome:
    if gate.groups is None:
        return Outcome(False, "Regroupements indisponibles.", {})
    return gate.restart_learning()


class FirewallScreen(OmegaScreen):
    def compose(self) -> ComposeResult:
        app: OmegaTailApp = self.app  # type: ignore[assignment]
        gate = app.gate
        policy = gate.policy() if gate is not None else None
        yield Header()
        yield StatusBand(app.snapshot)
        with VerticalScroll(classes="omega-panel"):
            yield Static(_("PARE-FEU FUNNEL"), classes="omega-title")
            yield Static(_("Une porte (HAProxy) se place entre Funnel et votre site : elle voit l'adresse réelle de "
                           "chaque visiteur et refuse les abus AVANT tout chiffrement (4,6 fois moins de calcul par "
                           "connexion refusée, mesuré). Activation et désactivation avec retour arrière automatique."),
                         classes="omega-hint")
            yield Static("", id="gate-state", classes="tail-box", markup=False)
            with Horizontal(classes="omega-actions"):
                with Container(classes="omega-btn-frame"):
                    yield Button(_("Installer HAProxy"), id="install")
                with Container(classes="omega-btn-frame"):
                    yield Button(_("Activer la protection"), id="activate", variant="primary")
                with Container(classes="omega-btn-frame"):
                    yield Button(_("Désactiver la protection"), id="deactivate", variant="error")
                with Container(classes="omega-btn-frame"):
                    yield Button(_("Renouveler le certificat"), id="renew")

            yield Rule(classes="tail-separator")
            yield Static(_("RÈGLES (appliquées à chaud)"), classes="omega-subtitle")
            with Horizontal(classes="omega-actions"):
                yield Static(_("Mode"), classes="tail-label")
                yield Select([(_("normal : refuse"), MODE_NORMAL),
                              (_("observation : compte sans refuser"), MODE_OBSERVATION)],
                             value=policy.mode if policy else MODE_NORMAL, allow_blank=False, id="mode")
                yield Checkbox(_("Vérifier le nom visé"),
                               value=policy.check_sni if policy else True, id="check_sni")
            for key, label in NUMBERS:
                with Horizontal(classes="omega-actions"):
                    yield Static(_(label), classes="tail-label tail-wide-label")
                    yield Input(str(getattr(policy, key)) if policy else "", id=key, classes="tail-number",
                                placeholder=_("nombre"))
            with Horizontal(classes="omega-actions"), Container(classes="omega-btn-frame"):
                yield Button(_("Appliquer les règles"), id="apply", variant="primary")

            if gate is not None and gate.groups is not None:
                yield from self._compose_groups(gate.groups.policy())

            yield Rule(classes="tail-separator")
            yield Static(_("LISTES"), classes="omega-subtitle")
            yield Static("", id="lists", markup=False)
            with Horizontal(classes="omega-actions"):
                yield Input(placeholder=_("Adresse ou réseau (203.0.113.7, 198.51.100.0/24, 2001:db8::/48)"),
                            id="address")
            with Horizontal(classes="omega-actions"):
                with Container(classes="omega-btn-frame"):
                    yield Button(_("Mettre en confiance"), id="trust")
                with Container(classes="omega-btn-frame"):
                    yield Button(_("Retirer la confiance"), id="untrust")
                with Container(classes="omega-btn-frame"):
                    yield Button(_("Liste noire"), id="blacklist", variant="error")
                with Container(classes="omega-btn-frame"):
                    yield Button(_("Débloquer"), id="unblock")
        with Horizontal(classes="omega-actions omega-fixed-actions"):
            with Container(classes="omega-btn-frame"):
                yield Button(_("Attaques et décisions"), id="attacks")
            with Container(classes="omega-btn-frame"):
                yield Button(_("Retour"), id="back")
        yield Footer()

    def _compose_groups(self, policy: GroupsPolicy) -> ComposeResult:
        yield Rule(classes="tail-separator")
        yield Static(_("REGROUPEMENTS : EMPREINTES, AS, PAYS"), classes="omega-subtitle")
        yield Static(_("Contre les attaques à adresses dispersées : chaque connexion reçoit, avant tout chiffrement, "
                       "son empreinte (JA4), son AS et son pays. Quand les connexions entrantes dépassent le seuil, "
                       "la porte passe seule en MODE ATTAQUE : une empreinte inconnue qui explose, un AS "
                       "d'hébergeur ou un pays choisi qui dépasse son débit est alors refusé. Les navigateurs "
                       "courants ne sont jamais touchés ; les clients connus passent avant le budget. En "
                       "observation, tout est compté (« aurait refusé ») et rien n'est refusé."), classes="omega-hint")
        yield Static("", id="groups-state", classes="tail-box", markup=False)
        with Horizontal(classes="omega-actions"):
            yield Static(_("Regroupements"), classes="tail-label")
            yield Select([(_("observation : comptent sans refuser"), GROUPS_OBSERVE),
                          (_("appliqués : refusent en mode attaque (après l'apprentissage)"), GROUPS_APPLY)],
                         value=policy.mode, allow_blank=False, id="groups-mode")
            yield Checkbox(_("Clients connus avant le budget"), value=policy.known_first, id="g-known_first")
        for key, label in GROUP_NUMBERS:
            with Horizontal(classes="omega-actions"):
                yield Static(_(label), classes="tail-label tail-wide-label")
                yield Input(str(getattr(policy, key)), id=f"g-{key}", classes="tail-number", placeholder=_("nombre"))
        with Horizontal(classes="omega-actions"):
            yield Static(_("Pays limités en mode attaque"), classes="tail-label tail-wide-label")
            yield Input(" ".join(policy.countries), id="g-countries", placeholder=_("ex. CN, RU (vide : aucun)"))
        with Horizontal(classes="omega-actions"):
            yield Static(_("AS d'hébergeurs"), classes="tail-label tail-wide-label")
            yield Input(" ".join(str(number) for number in policy.hosting), id="g-hosting",
                        placeholder=_("ex. 16509 24940 (numéros d'AS)"))
        with Horizontal(classes="omega-actions"):
            with Container(classes="omega-btn-frame"):
                yield Button(_("Appliquer les regroupements"), id="apply-groups", variant="primary")
            with Container(classes="omega-btn-frame"):
                yield Button(_("Mettre à jour la base"), id="refresh-base")
            with Container(classes="omega-btn-frame"):
                yield Button(_("Recommencer l'apprentissage"), id="restart-learning")
        yield Busy(id="base-busy")

    def on_mount(self) -> None:
        self.refresh_state()
        snapshot = getattr(self.app, "snapshot", None)
        if snapshot is not None:
            self.show_snapshot(snapshot)

    def show_snapshot(self, snapshot: Snapshot) -> None:
        self.query_one(StatusBand).show(snapshot)
        self.refresh_state()

    def refresh_state(self) -> None:
        app: OmegaTailApp = self.app  # type: ignore[assignment]
        self.query_one("#gate-state", Static).update(app.gate_state_text())
        gate, snapshot = app.gate, app.snapshot
        installed = gate is not None and bool(gate.machine.haproxy())
        active = gate is not None and gate.state() is not None
        operator = snapshot is not None and snapshot.is_operator
        install = self.query_one("#install", Button)
        if install.parent is not None:  # le cadre du bouton, sinon il reste affiche vide
            install.parent.display = gate is not None and not installed
        self.query_one("#activate", Button).disabled = not installed or active or not operator
        self.query_one("#deactivate", Button).disabled = not active
        if gate is not None and gate.groups is not None:
            status = gate.groups.status()
            self.query_one("#groups-state", Static).update(groups_text(status))
            mode = self.query_one("#groups-mode", Select)
            if mode.value != status.policy.mode:  # mode enregistre (l'apprentissage peut avoir garde l'observation)
                mode.value = status.policy.mode
        if gate is not None:
            trusted, black = gate.lists()
            self.query_one("#lists", Static).update(
                _("Confiance (jamais limitées) : {trusted}\nListe noire (refusées jusqu'à leur retrait) : {black}")
                .format(trusted=", ".join(trusted) or "—", black=", ".join(black) or "—"))

    def on_button_pressed(self, event: Button.Pressed) -> None:
        app: OmegaTailApp = self.app  # type: ignore[assignment]
        button = event.button.id
        address = self.query_one("#address", Input).value
        if button == "install":
            app.install_haproxy()
        elif button == "activate":
            app.activate_gate()
        elif button == "deactivate":
            app.deactivate_gate()
        elif button == "renew":
            app.gate_action(lambda gate: gate.renew_certificate(hot=gate.state() is not None))
        elif button == "apply":
            values = {key: self.query_one(f"#{key}", Input).value for key, _label in NUMBERS}
            values["mode"] = str(self.query_one("#mode", Select).value)
            values["check_sni"] = str(self.query_one("#check_sni", Checkbox).value)
            app.gate_action(lambda gate: gate.apply_policy(values))
        elif button == "apply-groups":
            values = {key: self.query_one(f"#g-{key}", Input).value for key, _label in GROUP_NUMBERS}
            values["mode"] = str(self.query_one("#groups-mode", Select).value)
            values["known_first"] = str(self.query_one("#g-known_first", Checkbox).value)
            values["countries"] = self.query_one("#g-countries", Input).value
            values["hosting"] = self.query_one("#g-hosting", Input).value
            app.gate_action(lambda gate: gate.apply_groups(values), after=self.refresh_state)
        elif button == "refresh-base":
            busy = self.query_one("#base-busy", Busy)
            busy.show(_("Téléchargement et préparation de la base AS / pays (DB-IP Lite) : une à quelques "
                        "minutes, l'écran reste utilisable…"))
            event.button.disabled = True

            def done() -> None:
                busy.hide()
                event.button.disabled = False
                self.refresh_state()

            app.gate_action(refresh_base, after=done)
        elif button == "restart-learning":
            app.gate_action(restart_learning, after=self.refresh_state)
        elif button == "trust":
            app.gate_action(lambda gate: gate.trust(address))
        elif button == "untrust":
            app.gate_action(lambda gate: gate.trust(address, add=False))
        elif button == "blacklist":
            app.gate_action(lambda gate: gate.block(address, forever=True))
        elif button == "unblock":
            app.gate_action(lambda gate: gate.unblock(address))
        elif button == "attacks":
            app.open_key("attacks")
        elif button == "back":
            self.action_back()
