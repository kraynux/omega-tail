# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Service tailscaled (proposition §3.2) : etat systemd, versions, lancement, fichiers d'ajout (lecture seule :
jamais modifies), confinement ; Demarrer / Arreter / Redemarrer, chaque fois apres avoir montre la commande, avec
le garde-fou « branche sciee » quand la session passe par Tailscale."""
from __future__ import annotations

from typing import TYPE_CHECKING

from textual.app import ComposeResult
from textual.containers import Container, Horizontal, VerticalScroll
from textual.widgets import Button, Footer, Header, Static

from omega_tail.domain.service import ServiceAction
from omega_tail.domain.session import Risk, guard_service_action
from omega_tail.domain.snapshot import Snapshot
from omega_tail.domain.startup import risky_hooks
from omega_tail.interfaces.shared.presentation import service_line, size
from omega_tail.interfaces.tui.screens._base import OmegaScreen
from omega_tail.interfaces.tui.screens.confirm import ConfirmScreen
from omega_tail.interfaces.tui.widgets.status_band import StatusBand
from omega_tail.shared.i18n import N_, _

if TYPE_CHECKING:
    from omega_tail.interfaces.tui.app import OmegaTailApp

ACTION_TITLES = {ServiceAction.START: N_("DÉMARRER TAILSCALED ?"), ServiceAction.STOP: N_("ARRÊTER TAILSCALED ?"),
                 ServiceAction.RESTART: N_("REDÉMARRER TAILSCALED ?")}
ACTION_EFFECTS = {
    ServiceAction.START: N_("Tailscale se reconnecte au tailnet ; les publications (Serve, Funnel) reprennent."),
    ServiceAction.STOP: N_("Tailscale est coupé : plus d'accès par le tailnet, publications (Serve, Funnel) "
                        "interrompues jusqu'au prochain démarrage."),
    ServiceAction.RESTART: N_("Coupure de quelques secondes : le tailnet et les publications (Serve, Funnel) "
                           "reviennent d'eux-mêmes. Applique une mise à jour déjà installée."),
}


def service_text(snapshot: Snapshot, read_file: object) -> str:
    service, tailscale = snapshot.service, snapshot.tailscale
    if not service.known:
        return _("systemd ne connaît pas le service tailscaled sur cette machine.") + (
            f"\n{service.error}" if service.error else "")
    lines = [
        _("État : {state}").format(state=service_line(service)),
        _("Depuis : {since}").format(since=service.since or "—"),
        _("Processus : {pid} · mémoire {memory}").format(pid=service.main_pid or "—",
                                                         memory=size(service.memory_bytes)),
        "",
        _("Version en marche : {version}").format(version=tailscale.daemon_version or "—"),
        _("Version installée : {version}").format(version=tailscale.client_version or "—"),
    ]
    if tailscale.versions_differ:
        lines.append(_("→ La mise à jour est installée mais pas appliquée : « Redémarrer » l'applique."))
    lines += ["", _("Système d'init : {init} · service « {name} »").format(init=service.init, name=service.name or "—"),
              _("Lancement : {command}").format(command=service.exec_start or "—"),
              _("Fichier du service : {path}").format(path=service.fragment_path or "—")]
    if service.drop_ins:
        lines.append(_("Fichiers d'ajout (lus, jamais modifiés par omega-tail) :"))
        for path in service.drop_ins:
            lines.append(f"  {path}")
            content = read_file(path) if callable(read_file) else ""
            lines += [f"    {line}" for line in str(content).splitlines() if line.strip()][:20]
    else:
        lines.append(_("Fichiers d'ajout : aucun."))
    risky = risky_hooks(service)
    if risky:
        lines += ["", _("⚠ Le démarrage lance « tailscale up » : si un réglage change (opérateur, nom, routes…), "
                        "Tailscale le refusera et tailscaled ne redémarrera plus. « Corriger le démarrage » ajoute "
                        "« - » devant la commande (son refus n'arrête plus le service).")]
        lines += [f"  {hook}" for hook in risky]
    lines += ["", _("Confinement : {state}").format(state=_("oui") if service.confined else _("non")),
              _("  plafond CPU {quota} · poids {weight} · cœurs {cpus} · priorité {nice}").format(
                  quota=service.cpu_quota or "—", weight=service.cpu_weight or "—",
                  cpus=service.allowed_cpus or _("tous"), nice=service.nice or "—")]
    if service.confinement_lost:
        lines.append(_("  ⚠ Confinement perdu au redémarrage de tailscaled : « Survie » → « Appliquer le "
                       "confinement »."))
    elif not service.confined:
        lines.append(_("  Le confinement se règle dans « Survie »."))
    if snapshot.through_tailscale:
        lines += ["", _("⚠ Cette session passe par Tailscale : arrêter tailscaled la couperait.")]
    return "\n".join(lines)


class ServiceScreen(OmegaScreen):
    def compose(self) -> ComposeResult:
        app: OmegaTailApp = self.app  # type: ignore[assignment]
        yield Header()
        yield StatusBand(app.snapshot)
        with VerticalScroll(classes="omega-panel"):
            yield Static(_("SERVICE TAILSCALED"), classes="omega-title")
            yield Static(_("Chaque action montre sa commande avant d'être lancée ; le mot de passe sudo se saisit "
                           "dans le terminal."), classes="omega-hint")
            yield Static("", id="service-box", classes="tail-box", markup=False)
        with Horizontal(classes="omega-actions omega-fixed-actions"):
            for action, label in ((ServiceAction.START, _("Démarrer")), (ServiceAction.STOP, _("Arrêter")),
                                  (ServiceAction.RESTART, _("Redémarrer"))):
                with Container(classes="omega-btn-frame"):
                    yield Button(label, id=f"do-{action.value}",
                                 variant="error" if action is ServiceAction.STOP else "primary")
            with Container(classes="omega-btn-frame"):
                yield Button(_("Corriger le démarrage"), id="fix-startup", variant="warning")
            with Container(classes="omega-btn-frame"):
                yield Button(_("Journaux"), id="journals")
            with Container(classes="omega-btn-frame"):
                yield Button(_("Retour"), id="back")
        yield Footer()

    def on_mount(self) -> None:
        self.query_one("#service-box").border_title = "tailscaled"
        snapshot = getattr(self.app, "snapshot", None)
        if snapshot is not None:
            self.show_snapshot(snapshot)

    def show_snapshot(self, snapshot: Snapshot) -> None:
        app: OmegaTailApp = self.app  # type: ignore[assignment]
        self.query_one(StatusBand).show(snapshot)
        self.query_one("#service-box", Static).update(service_text(snapshot, app.read_file))
        running = snapshot.service.running
        self.query_one("#do-start", Button).disabled = running or not snapshot.service.known
        self.query_one("#do-stop", Button).disabled = not running
        self.query_one("#do-restart", Button).disabled = not snapshot.service.known
        fix = self.query_one("#fix-startup", Button)
        if fix.parent is not None:
            fix.parent.display = bool(risky_hooks(snapshot.service))

    def on_button_pressed(self, event: Button.Pressed) -> None:
        button = event.button.id or ""
        app: OmegaTailApp = self.app  # type: ignore[assignment]
        if button.startswith("do-"):
            self._ask(ServiceAction(button.removeprefix("do-")))
        elif button == "fix-startup":
            app.fix_startup()
        elif button == "journals":
            app.open_key("journals")
        elif button == "back":
            self.action_back()

    def _ask(self, action: ServiceAction) -> None:
        app: OmegaTailApp = self.app  # type: ignore[assignment]
        snapshot = app.snapshot
        through = snapshot.through_tailscale if snapshot is not None else False
        guard = guard_service_action(action, through)
        commands, fix = app.service_commands_for(action)
        listing = "\n".join("  " + " ".join(command) for command in commands)
        text = _(ACTION_EFFECTS[action]) + ("\n\n⚠ " + fix if fix else "") + "\n\n" + _("Commandes :") + "\n" + listing
        if guard.risk is not Risk.NONE:
            text += "\n\n⚠ " + _(guard.text)
        self.app.push_screen(ConfirmScreen(title=_(ACTION_TITLES[action]), text=text, yes=_("Lancer"),
                                           no=_("Annuler")),
                             lambda confirmed: self._confirmed(action, guard.risk, confirmed, commands))

    def _confirmed(self, action: ServiceAction, risk: Risk, confirmed: bool | None,
                   commands: list[tuple[str, ...]] | None = None) -> None:
        if not confirmed:
            return
        app: OmegaTailApp = self.app  # type: ignore[assignment]
        if risk is Risk.CUT:
            self.app.push_screen(ConfirmScreen(
                title=_("VOUS ALLEZ PERDRE CETTE SESSION"),
                text=_("Dernière confirmation : tailscaled sera arrêté et cette session coupée. Vous devrez le "
                       "relancer depuis le réseau local ou la machine elle-même."),
                yes=_("Arrêter quand même"), no=_("Annuler")),
                lambda sure: app.run_service_action(action, commands) if sure else None)
            return
        app.run_service_action(action, commands)
