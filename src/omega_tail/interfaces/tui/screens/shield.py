# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Bouclier du port WireGuard (lot 8, ouvert depuis « Survie ») : protege tailscaled des flots de paquets.

Le meme bouclier qu'omega-fire (omega-lib D-018) : pose par omega-fire s'il est relie par omega-connect, sinon
par omega-tail. Chaque action montre ses commandes avant ; le mot de passe sudo se saisit dans le terminal."""
from __future__ import annotations

import contextlib
from typing import TYPE_CHECKING

from omega_lib.shield.models import ShieldMode
from textual.app import ComposeResult
from textual.containers import Container, Horizontal, VerticalScroll
from textual.css.query import NoMatches
from textual.widgets import Button, DataTable, Footer, Header, Static

from omega_tail.application.shield import Action, ShieldView
from omega_tail.domain.init import InitSystem
from omega_tail.domain.shield import FIRE_MIN_VERSION, OMEGA_FIRE, OMEGA_TAIL
from omega_tail.domain.snapshot import Snapshot
from omega_tail.interfaces.shared.presentation import shield_summary as summary
from omega_tail.interfaces.tui.screens._base import OmegaScreen, set_label
from omega_tail.interfaces.tui.widgets.status_band import StatusBand
from omega_tail.shared.i18n import N_, _

if TYPE_CHECKING:
    from omega_tail.interfaces.tui.app import OmegaTailApp

COUNTERS: tuple[tuple[str, str, bool], ...] = (
    ("peer", N_("Pairs connus"), False),
    ("init", N_("Poignées de main"), False),
    ("init_over", N_("Poignées de main en excès (par source)"), True),
    ("unknown", N_("Sources inconnues, paquets bien formés"), False),
    ("unknown_over", N_("Sources inconnues en excès (par source)"), True),
    ("global_over", N_("Excès de l'ensemble des sources inconnues"), True),
    ("other", N_("Paquets qui ne sont pas du WireGuard"), True),
)
BUTTONS: tuple[tuple[Action, str, str], ...] = (
    (Action.POSE, N_("Poser (observation)"), "primary"),
    (Action.MODE, N_("Passer en actif"), "default"),
    (Action.REPOSE, N_("Reposer"), "primary"),
    (Action.HAND_OVER, N_("Confier à omega-fire"), "default"),
    (Action.TAKE_BACK, N_("Reprendre la gestion"), "default"),
    (Action.REMOVE, N_("Retirer"), "error"),
)
TITLES = {
    Action.POSE: N_("POSER LE BOUCLIER DU PORT WIREGUARD ?"),
    Action.MODE: N_("CHANGER LE MODE DU BOUCLIER ?"),
    Action.REPOSE: N_("REPOSER LE BOUCLIER ?"),
    Action.HAND_OVER: N_("CONFIER LE BOUCLIER À OMEGA-FIRE ?"),
    Action.TAKE_BACK: N_("REPRENDRE LA GESTION DU BOUCLIER ?"),
    Action.REMOVE: N_("RETIRER LE BOUCLIER ?"),
}
EXPLANATIONS = {
    Action.POSE: N_("Une table nftables devant tailscaled, en OBSERVATION : rien n'est refusé, les compteurs disent ce "
                    "qui l'aurait été. Un service la remet en place à chaque démarrage."),
    Action.REPOSE: N_("La table enregistrée est remise ; ses compteurs et la liste des pairs repartent de zéro."),
    Action.HAND_OVER: N_("omega-fire gérera le bouclier (remise au démarrage, commandes, liste des règles). La table, "
                         "ses compteurs et les pairs connus ne sont pas touchés."),
    Action.TAKE_BACK: N_("omega-fire n'est plus relié : omega-tail gère de nouveau le bouclier. La table n'est pas "
                         "touchée."),
    Action.REMOVE: N_("La table, ses fichiers et son service sont supprimés : tailscaled ne sera plus protégé "
                      "contre les flots de paquets."),
}
REFUSALS = {
    "port-aleatoire": N_("tailscaled tire son port au hasard (--port 0) : aucun bouclier possible. Fixez un port "
                         "(PORT= dans /etc/default/tailscaled), puis redémarrez tailscaled."),
    "aucune-carte": N_("Aucune carte réseau matérielle trouvée : rien à protéger."),
    "invalide": N_("Port ou nom de carte réseau refusé."),
    "absent": N_("Aucun bouclier enregistré sur cette machine."),
    "redemarrage": N_("Le noyau a été mis à jour sans redémarrage : ses modules ne peuvent plus être chargés et la "
                      "table serait refusée. Redémarrez la machine, puis recommencez."),
}


def view_text(view: ShieldView) -> str:
    facts, lines = view.facts, [summary(view.facts)]
    if facts.installed and facts.settings is not None:
        spec = facts.settings.spec
        lines.append(_("Origine : {tool} (outil qui l'a demandé) · port {port}/udp · cartes réseau : {devices}").format(
            tool=facts.requested_by or "?", port=spec.port, devices=", ".join(spec.devices)))
        if facts.status is not None and facts.status.present:
            lines.append(_("Pairs connus : {count} (jamais limités).").format(count=facts.status.peers))
    else:
        lines.append(_("Détecté : port de tailscaled {port}, cartes réseau {devices}.").format(
            port=view.port or _("au hasard"), devices=", ".join(view.devices) or "—"))
    if not view.egress:
        lines.append(_("Noyau antérieur à 5.16 : sans liste des pairs, seuls le tri des paquets et la limite des "
                       "poignées de main sont posés."))
    fire = view.fire
    if fire.ready:
        lines.append(_("omega-fire {version} relié : il pose et gère le bouclier ; sa liste des règles l'affiche "
                       "avec l'origine omega-tail.").format(version=fire.version))
    elif fire.linked:
        lines.append(_("omega-fire {version} relié, mais trop ancien pour le bouclier (il faut {needed} ou plus "
                       "récent) : omega-tail le gère lui-même. Mettez omega-fire à jour.").format(
            version=fire.version or "?", needed=".".join(str(part) for part in FIRE_MIN_VERSION)))
    else:
        lines.append(_("omega-fire n'est pas relié par omega-connect : omega-tail pose et gère le bouclier lui-même, "
                       "même si ufw ou firewalld sont présents."))
    if facts.manager == OMEGA_FIRE and not fire.ready:
        lines.append(_("Géré par omega-fire, qui n'est plus relié : « Reprendre la gestion » le rend à omega-tail."))
    if not view.modules_ready:
        lines.append(_("Noyau mis à jour sans redémarrage : la table ne peut pas être posée avant un redémarrage."))
    if view.init is InitSystem.NONE:
        lines.append(_("Système d'init inconnu : le bouclier ne sera pas remis en place au redémarrage."))
    return "\n".join(lines)


class ShieldScreen(OmegaScreen):
    def __init__(self) -> None:
        super().__init__()
        self.view: ShieldView | None = None

    def compose(self) -> ComposeResult:
        app: OmegaTailApp = self.app  # type: ignore[assignment]
        yield Header()
        yield StatusBand(app.snapshot)
        with VerticalScroll(classes="omega-panel"):
            yield Static(_("BOUCLIER DU PORT WIREGUARD"), classes="omega-title")
            yield Static(_("Devant tailscaled : poignées de main limitées par source, budget pour les sources qui ne "
                           "sont pas des pairs connus, paquets qui ne sont pas du WireGuard refusés. Mesuré : un flot "
                           "qui prenait un cœur entier à tailscaled n'en prend plus que 1 %. Commencez en "
                           "observation."), classes="omega-hint")
            yield Static("", id="shield-state", classes="tail-box", markup=False)
            yield Static(_("COMPTEURS DEPUIS LA POSE"), classes="omega-subtitle")
            yield DataTable(id="shield-counters", cursor_type="none")
        with Horizontal(classes="omega-actions omega-fixed-actions"):
            for action, label, variant in BUTTONS:
                with Container(classes="omega-btn-frame", id=f"frame-{action.value}"):
                    yield Button(_(label), id=f"shield-{action.value}", variant=variant)  # type: ignore[arg-type]
        with Horizontal(classes="omega-actions omega-fixed-actions"):
            with Container(classes="omega-btn-frame"):
                yield Button(_("Actualiser"), id="refresh")
            with Container(classes="omega-btn-frame"):
                yield Button(_("Retour"), id="back", variant="primary")
        yield Footer()

    def on_mount(self) -> None:
        self.query_one("#shield-counters", DataTable).add_columns(_("Compteur"), _("Paquets"), _("Effet"))
        self.build()

    def show_snapshot(self, snapshot: Snapshot) -> None:
        self.query_one(StatusBand).show(snapshot)
        self.build()

    def build(self) -> None:
        app: OmegaTailApp = self.app  # type: ignore[assignment]
        tools = app.shield
        if tools is None:
            return

        def work() -> None:
            view = tools.view()
            self.app.call_from_thread(self.show, view)

        self.run_worker(work, thread=True, group="shield", exclusive=True)

    def show(self, view: ShieldView) -> None:
        self.view = view
        with contextlib.suppress(NoMatches):
            self.query_one("#shield-state", Static).update(view_text(view))
            table = self.query_one("#shield-counters", DataTable)
            table.clear()
            facts = view.facts
            active = facts.mode is ShieldMode.ACTIVE
            if facts.status is not None and facts.status.present:
                for name, label, refusing in COUNTERS:
                    effect = (_("refusés") if active else _("auraient été refusés")) if refusing else _("admis")
                    table.add_row(_(label), str(getattr(facts.status.counters, name)), effect)
            shown = set(view.actions)
            for action, _label, _variant in BUTTONS:
                self.query_one(f"#frame-{action.value}").display = action in shown
            set_label(self.query_one(f"#shield-{Action.MODE.value}", Button),
                      _("Passer en observation") if active else _("Passer en actif"))

    def on_button_pressed(self, event: Button.Pressed) -> None:
        app: OmegaTailApp = self.app  # type: ignore[assignment]
        button = event.button.id or ""
        if button == "back":
            self.action_back()
        elif button == "refresh":
            self.build()
        elif button.startswith("shield-") and self.view is not None:
            action = Action(button.removeprefix("shield-"))
            mode = None
            if action is Action.MODE:
                mode = ShieldMode.OBSERVE if self.view.facts.mode is ShieldMode.ACTIVE else ShieldMode.ACTIVE
            app.shield_action(action, mode, refused=self.view.facts.refused)


def confirm_text(action: Action, mode: ShieldMode | None, refused: int, via_fire: bool) -> str:
    if action is Action.MODE:
        text = (_("En observation, {count} paquet(s) auraient été refusés : en actif, ils le seront. Les pairs connus "
                  "ne sont jamais limités.").format(count=refused) if mode is ShieldMode.ACTIVE else
                _("Plus rien n'est refusé ; les compteurs continuent de dire ce qui l'aurait été."))
    else:
        text = _(EXPLANATIONS[action])
    if via_fire:
        text += "\n" + _("Par omega-fire (il garde l'origine {tool} et l'inscrit à son journal d'audit).").format(
            tool=OMEGA_TAIL)
    return text
