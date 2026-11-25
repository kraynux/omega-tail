# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Survie (lot 2, proposition §4.2) : confinement de tailscaled et disjoncteur Funnel.

- Confinement : fichier d'ajout systemd SEPARE (`50-omega-tail.conf`), apercu avant, retrait en un bouton ; votre
  propre `override.conf` n'est jamais modifie.
- Disjoncteur : coupure momentanee programmee (remise en route automatique a l'identique) ou coupure totale,
  proposees quand les seuils sont depasses, ou lancees ici a la main ; « Retablir maintenant »."""
from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from textual.app import ComposeResult
from textual.containers import Container, Horizontal, VerticalScroll
from textual.widgets import Button, Checkbox, Footer, Header, Input, Rule, Static

from omega_tail.application.breaker_settings import KEY_CPU, KEY_MINUTES, KEY_SECONDS, KEY_TEMPERATURE, KEY_WINDOW
from omega_tail.domain.confinement import DROP_IN_PATH, drop_in_text, recommended
from omega_tail.domain.snapshot import Snapshot
from omega_tail.domain.watch import RESET_HOURS, STEPS_MINUTES, STRIKES
from omega_tail.interfaces.tui.screens._base import OmegaScreen, set_label
from omega_tail.interfaces.tui.screens.shield import summary as shield_summary
from omega_tail.interfaces.tui.widgets.status_band import StatusBand
from omega_tail.shared.i18n import _

if TYPE_CHECKING:
    from omega_tail.interfaces.tui.app import OmegaTailApp


def _clock(text: str) -> str:
    try:
        return datetime.fromisoformat(text).astimezone().strftime("%H:%M")
    except ValueError:
        return "?"


def confinement_state(snapshot: Snapshot) -> str:
    service = snapshot.service
    if not service.known:
        return _("systemd ne connaît pas tailscaled : confinement impossible ici.")
    if service.init != "systemd":
        state = (_("perdu (tailscaled a redémarré) : « Appliquer le confinement » le remet") if service.confinement_lost
                 else _("actif (groupe de contrôle d'omega-tail)") if service.confined else _("aucun"))
        return "\n".join([_("Confinement actuel : {state}").format(state=state),
                          _("  plafond {quota} · poids {weight} · système d'init {init}").format(
                              quota=service.cpu_quota or "—", weight=service.cpu_weight or "—", init=service.init)])
    ours = DROP_IN_PATH in service.drop_ins
    state = (_("actif, posé par omega-tail") if ours and service.confined else
             _("posé par omega-tail, pas encore appliqué (rechargement ou redémarrage)") if ours else
             _("actif, posé hors d'omega-tail") if service.confined else _("aucun"))
    lines = [_("Confinement actuel : {state}").format(state=state),
             _("  plafond {quota} · poids {weight} · priorité {nice}").format(
                 quota=service.cpu_quota or "—", weight=service.cpu_weight or "—", nice=service.nice or "—")]
    others = [path for path in service.drop_ins if path != DROP_IN_PATH]
    if others:
        lines.append(_("  Vos fichiers d'ajout (jamais modifiés) : {paths}").format(paths=", ".join(others)))
    return "\n".join(lines)


def breaker_state(snapshot: Snapshot) -> str:
    cut = snapshot.cut
    if cut is not None:
        if cut.total:
            return _("Funnel COUPÉ par omega-tail depuis {since} (coupure totale) : « Rétablir maintenant » le "
                     "remet à l'identique.").format(since=_clock(cut.cut_at))
        return _("Funnel COUPÉ par omega-tail depuis {since}, remis en route automatiquement à {until}.").format(
            since=_clock(cut.cut_at), until=_clock(cut.until))
    ports = ", ".join(str(item.port) for item in snapshot.funnel)
    return _("Funnel ouvert : port {ports}.").format(ports=ports) if ports else _(
        "Funnel n'est pas ouvert : rien à couper.")


def watch_state(snapshot: Snapshot, window: int) -> str:
    watch = snapshot.watch
    if watch is None or not watch.installed:
        return _("Désactivée : sous attaque, omega-tail ouvert PROPOSE la coupure (il faut être devant la machine).")
    if not watch.alive:
        return "⚠ " + _("Activée mais arrêtée (aucun signe de vie) : « Activer la veille » la relance.")
    return "\n".join([
        _("En marche, même omega-tail fermé : sous attaque, elle coupe Funnel seule et le remet seule."),
        _("  Dépassements récents : {strikes}/{total} (fenêtre de {window} min) · prochaine coupure : {minutes} "
          "min").format(strikes=watch.strikes, total=STRIKES, window=window, minutes=watch.next_minutes)])


class SurvivalScreen(OmegaScreen):
    def compose(self) -> ComposeResult:
        app: OmegaTailApp = self.app  # type: ignore[assignment]
        policy = app.policy()
        ssh_unit = app.ssh_unit
        cpu_count = app.snapshot.machine.cpu_count if app.snapshot is not None else 4
        plan = recommended(cpu_count)
        yield Header()
        yield StatusBand(app.snapshot)
        with VerticalScroll(classes="omega-panel"):
            yield Static(_("SURVIE"), classes="omega-title")
            yield Static(_("Garder la machine debout sous attaque. Chaque action montre ses commandes avant ; le mot "
                           "de passe sudo se saisit dans le terminal."), classes="omega-hint")

            yield Static(_("CONFINEMENT DE TAILSCALED"), classes="omega-subtitle")
            yield Static("", id="confinement-state", markup=False)
            systemd = app.survival is None or app.survival.init.value == "systemd"
            if systemd:
                yield Static(_("Proposé pour cette machine ({count} fils), dans {path} :").format(
                    count=cpu_count, path=DROP_IN_PATH), classes="omega-hint")
                preview = drop_in_text(plan).rstrip("\n")
            else:
                yield Static(_("Proposé pour cette machine ({count} fils), dans un groupe de contrôle à part :")
                             .format(count=cpu_count), classes="omega-hint")
                preview = (f"/sys/fs/cgroup/omega-tail-tailscaled\n  cpu.max    {plan.quota_percent * 1000} 100000"
                           f"   ({plan.quota_percent} % d'un cœur)\n  cpu.weight {plan.cpu_weight}\n"
                           f"  renice     {plan.nice}")
            yield Static(preview, id="confinement-preview", classes="tail-box", markup=False)
            yield Checkbox(_("Donner la priorité à l'accès SSH ({unit})").format(unit=ssh_unit or "—"),
                           value=bool(ssh_unit), id="ssh-priority", disabled=not ssh_unit)
            yield Checkbox(_("Redémarrer tailscaled tout de suite (la priorité ne s'applique qu'au redémarrage ; "
                             "coupure de quelques secondes)"), value=True, id="restart-now", disabled=not systemd)
            with Horizontal(classes="omega-actions"):
                with Container(classes="omega-btn-frame"):
                    yield Button(_("Appliquer le confinement"), id="confine", variant="primary")
                with Container(classes="omega-btn-frame"):
                    yield Button(_("Retirer le confinement"), id="unconfine")

            yield Rule(classes="tail-separator")
            yield Static(_("VEILLE AUTOMATIQUE"), classes="omega-subtitle")
            yield Static("", id="watch-state", classes="tail-box", markup=False)
            yield Static(_("Pour une machine sans personne devant. Un dépassement : un seuil du disjoncteur tenu "
                           "(plus bas). {strikes} dépassements dans la fenêtre : Funnel coupé {first} min, puis "
                           "{second} min la fois suivante, puis {last} min à chaque fois ; toujours remis en "
                           "route seul, à l'identique. Retour à {first} min après {hours} h sans coupure. Seul "
                           "Funnel est coupé : tailscaled, le tailnet et SSH restent joignables.").format(
                strikes=STRIKES, first=STEPS_MINUTES[0], second=STEPS_MINUTES[1], last=STEPS_MINUTES[-1],
                hours=RESET_HOURS), classes="omega-hint")
            with Horizontal(classes="omega-actions"):
                yield Static(_("Fenêtre (min)"), classes="tail-label")
                yield Input(str(app.watch_window()), id=KEY_WINDOW, classes="tail-number")
                with Container(classes="omega-btn-frame"):
                    yield Button(_("Enregistrer"), id="save-window")
            with Horizontal(classes="omega-actions"):
                with Container(classes="omega-btn-frame"):
                    yield Button(_("Activer la veille"), id="watch-on", variant="primary")
                with Container(classes="omega-btn-frame"):
                    yield Button(_("Désactiver la veille"), id="watch-off")
            yield Static("", id="watch-journal", classes="omega-hint", markup=False)

            yield Rule(classes="tail-separator")
            yield Static(_("BOUCLIER DU PORT WIREGUARD"), classes="omega-subtitle")
            yield Static("", id="shield-summary", markup=False)
            yield Static(_("Protège tailscaled des flots de paquets envoyés sur son port (même sans Funnel)."),
                         classes="omega-hint tail-hint-tight")
            with Horizontal(classes="omega-actions"), Container(classes="omega-btn-frame"):
                yield Button(_("Bouclier du port WireGuard"), id="open-shield", variant="primary")
            yield Rule(classes="tail-separator")

            yield Static(_("DISJONCTEUR FUNNEL"), classes="omega-subtitle")
            yield Static("", id="breaker-state", markup=False)
            yield Static(_("Sans veille, il propose, il ne coupe jamais seul : quand un seuil est dépassé, omega-tail "
                           "ouvert vous propose une coupure momentanée ou totale. Avec la veille automatique "
                           "(ci-dessus), il agit seul."), classes="omega-hint")
            with Horizontal(classes="omega-actions"):
                yield Static(_("CPU tailscaled ≥ (% d'un cœur)"), classes="tail-label")
                yield Input(str(int(policy.cpu_percent)), id=KEY_CPU, classes="tail-number")
                yield Static(_("pendant (s)"), classes="tail-label")
                yield Input(str(policy.seconds), id=KEY_SECONDS, classes="tail-number")
            with Horizontal(classes="omega-actions"):
                yield Static(_("ou température ≥ (°C)"), classes="tail-label")
                yield Input(str(int(policy.temperature_c)), id=KEY_TEMPERATURE, classes="tail-number")
                yield Static(_("coupure momentanée (min)"), classes="tail-label")
                yield Input(str(policy.minutes), id=KEY_MINUTES, classes="tail-number")
            with Horizontal(classes="omega-actions"), Container(classes="omega-btn-frame"):
                yield Button(_("Enregistrer les seuils"), id="save-policy")
            with Horizontal(classes="omega-actions"):
                with Container(classes="omega-btn-frame"):
                    yield Button(_("Couper {minutes} min").format(minutes=policy.minutes), id="cut-minutes",
                                 variant="error")
                with Container(classes="omega-btn-frame"):
                    yield Button(_("Coupure totale"), id="cut-total", variant="error")
                with Container(classes="omega-btn-frame"):
                    yield Button(_("Rétablir maintenant"), id="restore", variant="primary")
            yield Static("", id="operator-hint", classes="omega-hint")

        with Horizontal(classes="omega-actions omega-fixed-actions"), Container(classes="omega-btn-frame"):
            yield Button(_("Retour"), id="back")
        yield Footer()

    def on_mount(self) -> None:
        snapshot = getattr(self.app, "snapshot", None)
        if snapshot is not None:
            self.show_snapshot(snapshot)

    def show_snapshot(self, snapshot: Snapshot) -> None:
        self.query_one(StatusBand).show(snapshot)
        self.query_one("#confinement-state", Static).update(confinement_state(snapshot))
        self.query_one("#breaker-state", Static).update(breaker_state(snapshot))
        self.query_one("#shield-summary", Static).update(shield_summary(snapshot.shield))
        cut, operator = snapshot.cut, snapshot.is_operator
        for button in ("#cut-minutes", "#cut-total"):
            self.query_one(button, Button).disabled = cut is not None or not snapshot.funnel or not operator
        self.query_one("#restore", Button).disabled = cut is None or not operator
        service = snapshot.service
        ours = DROP_IN_PATH in service.drop_ins if service.init == "systemd" else (
            service.confined or service.confinement_lost)
        self.query_one("#unconfine", Button).disabled = not ours
        self.query_one("#confine", Button).disabled = not snapshot.service.known
        app: OmegaTailApp = self.app  # type: ignore[assignment]
        self.query_one("#watch-state", Static).update(watch_state(snapshot, app.watch_window()))
        watch = snapshot.watch
        installed = watch is not None and watch.installed
        self.query_one("#watch-on", Button).parent.display = (  # type: ignore[union-attr]
            app.watch_tools is not None and not (installed and watch is not None and watch.alive))
        self.query_one("#watch-off", Button).parent.display = installed  # type: ignore[union-attr]
        journal = app.watch_tools.journal(6) if app.watch_tools is not None else []
        self.query_one("#watch-journal", Static).update(
            (_("Journal de la veille :") + "\n" + "\n".join(journal)) if journal else "")
        self.query_one("#operator-hint", Static).update("" if operator else _(
            "Le disjoncteur demande d'être opérateur de Tailscale (tableau de bord, « Devenir opérateur ») : la "
            "remise en route programmée tourne sous votre compte, jamais en root."))

    def on_button_pressed(self, event: Button.Pressed) -> None:
        app: OmegaTailApp = self.app  # type: ignore[assignment]
        button = event.button.id
        restart = self.query_one("#restart-now", Checkbox).value
        ssh = app.ssh_unit if self.query_one("#ssh-priority", Checkbox).value else ""
        if button == "confine":
            app.confine(restart=restart, ssh_unit=ssh)
        elif button == "unconfine":
            app.unconfine(restart=restart, ssh_unit=app.ssh_unit)
        elif button == "save-policy":
            values = {key: self.query_one(f"#{key}", Input).value
                      for key in (KEY_CPU, KEY_SECONDS, KEY_TEMPERATURE, KEY_MINUTES)}
            app.save_policy(values)
            set_label(self.query_one("#cut-minutes", Button),
                      _("Couper {minutes} min").format(minutes=app.policy().minutes))
        elif button == "save-window":
            app.save_policy({KEY_WINDOW: self.query_one(f"#{KEY_WINDOW}", Input).value})
        elif button == "watch-on":
            app.set_watch(True)
        elif button == "watch-off":
            app.set_watch(False)
        elif button == "cut-minutes":
            app.ask_cut(app.policy().minutes)
        elif button == "cut-total":
            app.ask_cut(None)
        elif button == "restore":
            app.restore_funnel()
        elif button == "open-shield":
            screen = app.screen_for("shield")
            if screen is not None:
                app.push_screen(screen)
        elif button == "back":
            self.action_back()
