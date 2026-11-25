# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Application Textual d'omega-tail : ecran de demarrage, menu (TAILSCALE | PROTECTION, 6 + 6), bande d'etat et
tableau de bord rafraichis toutes les 5 s, actions lancees dans le vrai terminal. Meme cadre que le reste de la
suite (themes d'omega-lib, feuilles de style par profil de rendu, confirmation de sortie, touches t r a s q).

Le composition root (app/main.py) passe les outils deja cables : l'interface n'importe jamais l'infrastructure."""
from __future__ import annotations

import contextlib
import shutil
import sys
import time
from collections import deque
from collections.abc import Callable, Iterable, Sequence
from contextlib import AbstractContextManager
from pathlib import Path
from typing import TYPE_CHECKING, ClassVar, Literal, cast

from omega_lib.ports.declaration import ContactSupportServices
from omega_lib.shield.models import ShieldMode
from omega_lib.terminal.models import RenderProfile
from omega_lib.theme.policies import DEFAULT_TUI_THEME, TUI_THEMES
from textual.app import App, SystemCommand
from textual.binding import Binding, BindingType

from omega_tail.application.actions import ActionTools, operator_command, service_command
from omega_tail.application.breaker_settings import load_policy, load_window, save_policy
from omega_tail.application.connection import ConnectionTools
from omega_tail.application.gate import GateTools
from omega_tail.application.network import NetworkTools
from omega_tail.application.publication import PublicationTools
from omega_tail.application.report import ReportTools
from omega_tail.application.settings import KEY_THEME, SettingsTools
from omega_tail.application.shield import Action as ShieldAction
from omega_tail.application.shield import ShieldTools
from omega_tail.application.snapshot import SnapshotTools
from omega_tail.application.survival import Outcome, SurvivalTools
from omega_tail.application.watch import WatchTools
from omega_tail.core.constants import REFRESH_SECONDS
from omega_tail.domain.alerts import Alert
from omega_tail.domain.breaker import SNOOZE_MINUTES, BreakerPolicy, Sample, assess
from omega_tail.domain.confinement import DROP_IN_PATH
from omega_tail.domain.init import InitSystem
from omega_tail.domain.service import ServiceAction
from omega_tail.domain.snapshot import Snapshot
from omega_tail.domain.watch import DEFAULT_WINDOW_MINUTES
from omega_tail.interfaces.shared.messages import outcome_text
from omega_tail.interfaces.tui.language_setting import notify_language_at_startup
from omega_tail.interfaces.tui.menu import entry
from omega_tail.interfaces.tui.rendering.stylesheet_loader import load_paths_for
from omega_tail.interfaces.tui.rendering.textual_theme_builder import build_all_textual_themes
from omega_tail.interfaces.tui.screens._base import suspended
from omega_tail.interfaces.tui.screens.attacks import AttacksScreen
from omega_tail.interfaces.tui.screens.breaker_proposal import BreakerProposalScreen
from omega_tail.interfaces.tui.screens.confirm import ConfirmScreen
from omega_tail.interfaces.tui.screens.connection import ConnectionScreen
from omega_tail.interfaces.tui.screens.contact_support import contact_support_screen
from omega_tail.interfaces.tui.screens.dashboard import DashboardScreen
from omega_tail.interfaces.tui.screens.firewall import FirewallScreen
from omega_tail.interfaces.tui.screens.help import HelpScreen
from omega_tail.interfaces.tui.screens.home import HomeScreen, planned_notice
from omega_tail.interfaces.tui.screens.journals import JournalsScreen
from omega_tail.interfaces.tui.screens.network import NetworkScreen
from omega_tail.interfaces.tui.screens.publication import PublicationScreen
from omega_tail.interfaces.tui.screens.quit_confirm import QuitConfirmScreen
from omega_tail.interfaces.tui.screens.report import ReportScreen
from omega_tail.interfaces.tui.screens.service import ServiceScreen
from omega_tail.interfaces.tui.screens.settings import SettingsScreen
from omega_tail.interfaces.tui.screens.shield import REFUSALS, TITLES, ShieldScreen, confirm_text
from omega_tail.interfaces.tui.screens.splash import SplashScreen
from omega_tail.interfaces.tui.screens.survival import SurvivalScreen
from omega_tail.ports.export import ExportWriter
from omega_tail.ports.readers import JournalReader
from omega_tail.shared.i18n import N_, _, exporting

if TYPE_CHECKING:
    from pathlib import PurePath

    from textual.screen import Screen

TITLE = "OMEGA-TAIL"
STARTUP_FIX_TEXT = N_(
    "Le démarrage de tailscaled lance « tailscale up » (votre fichier d'ajout). Depuis qu'un réglage a changé "
    "(opérateur, nom, routes…), Tailscale refuse ce « up » incomplet : systemd arrête alors tailscaled et abandonne "
    "après cinq essais (la machine sort du tailnet). omega-tail ajoute « - » devant cette commande : son refus "
    "n'arrête plus le service, et vos réglages restent gardés par Tailscale. Rien d'autre ne change ; l'original "
    "est gardé dans var/survie.")


class OmegaTailApp(App[None]):
    TITLE = TITLE
    BINDINGS: ClassVar[list[BindingType]] = [
        Binding("q", "quit", _("Quitter"), show=True),
        Binding("ctrl+q", "quit", _("Quitter"), show=False),
        Binding("t", "cycle_theme", _("Thème suivant"), show=True),
        Binding("r", "refresh_terminal", _("Rafraîchir"), show=True),
        Binding("a", "help", _("Aide"), show=True),
        Binding("s", "open_settings", _("Réglages"), show=True),
    ]

    def __init__(self, *, snapshots: SnapshotTools, actions: ActionTools, journal: JournalReader, version: str,
                 render_profile: RenderProfile, settings: SettingsTools | None = None,
                 contact: ContactSupportServices | None = None, writer: ExportWriter | None = None,
                 read_file: Callable[[str], str] | None = None, splash: bool = True,
                 refresh_seconds: float = REFRESH_SECONDS, survival: SurvivalTools | None = None,
                 ssh_unit: str = "", clock: Callable[[], float] = time.monotonic,
                 gate: GateTools | None = None, connection: ConnectionTools | None = None,
                 publication: PublicationTools | None = None, watch: WatchTools | None = None,
                 network: NetworkTools | None = None, report: ReportTools | None = None,
                 open_folder: Callable[[Path], bool] | None = None, shield: ShieldTools | None = None) -> None:
        super().__init__(css_path=cast("list[str | PurePath]", load_paths_for(render_profile)))
        for theme in build_all_textual_themes():
            self.register_theme(theme)
        self.theme = settings.theme() if settings is not None else DEFAULT_TUI_THEME
        self.title = f"{TITLE} {version}"
        self._snapshots = snapshots
        self._actions = actions
        self.journal = journal
        self._version = version
        self.settings = settings
        self._contact = contact
        self.writer = writer
        self.read_file = read_file or (lambda _path: "")
        self._splash = splash
        self._refresh_seconds = refresh_seconds
        self.snapshot: Snapshot | None = None
        self.alerts: tuple[Alert, ...] = ()
        self.pending_language: str | None = None
        """Langue choisie dans les Reglages : app/main.py relance l'interface apres sa fermeture."""
        self.survival = survival
        self.gate = gate
        """Pare-feu Funnel (porte HAProxy), lot 4."""
        self.connection = connection
        """Connexion et reglages, lot 5."""
        self.publication = publication
        self.watch_tools = watch
        """Pas `self.watch` : nom deja pris par Textual (DOMNode.watch)."""
        """Publication (Serve et Funnel), lot 5."""
        self.network = network
        """Reseau et appareils, lot 7."""
        self.report = report
        """Rapport, lot 7."""
        self.open_folder = open_folder
        self.shield = shield
        """Bouclier du port WireGuard, lot 8."""
        """« Voir les exports » : le dossier dans le navigateur (omega-lib) ; faux sans session graphique."""
        self.ssh_unit = ssh_unit
        """Service SSH de la machine (sshd ou ssh ; vide : aucun) : priorite sous attaque (Survie)."""
        self._clock = clock
        self._samples: deque[Sample] = deque(maxlen=720)
        self._snooze_until = 0.0
        self._proposing = False

    @property
    def as_root(self) -> bool:
        return self._actions.as_root

    def on_mount(self) -> None:
        self._update_sub_title()
        notify_language_at_startup(self)
        self.push_screen(HomeScreen(open_screen=self.screen_for))
        if self._splash:
            self.push_screen(SplashScreen(version=self._version))
        self.request_refresh()
        if self._refresh_seconds > 0:
            self.set_interval(self._refresh_seconds, self.request_refresh)

    # ---- lecture de l'etat ----
    def request_refresh(self) -> None:
        self.run_worker(self._collect, thread=True, group="snapshot", exclusive=True)

    def _collect(self) -> None:
        try:
            snapshot = self._snapshots.collect()
            alerts = self._snapshots.alerts(snapshot)
        except Exception as error:  # noqa: BLE001 - une lecture ratee ne ferme jamais l'interface
            self.call_from_thread(self.notify, str(error), title=_("Lecture de l'état"), severity="error")
            return
        self.call_from_thread(self._publish, snapshot, alerts)

    def _publish(self, snapshot: Snapshot, alerts: tuple[Alert, ...]) -> None:
        self.snapshot, self.alerts = snapshot, alerts
        for screen in self.screen_stack:
            show = getattr(screen, "show_snapshot", None)
            if callable(show):
                with contextlib.suppress(Exception):  # ecran en cours de construction
                    show(snapshot)
        self._watch_breaker(snapshot)

    # ---- disjoncteur : il propose, il ne coupe jamais seul ----
    def policy(self) -> BreakerPolicy:
        return load_policy(self.settings.store) if self.settings is not None else BreakerPolicy()

    def watch_window(self) -> int:
        return load_window(self.settings.store) if self.settings is not None else DEFAULT_WINDOW_MINUTES

    def save_policy(self, values: dict[str, str]) -> None:
        if self.settings is None:
            return
        refused = save_policy(self.settings.store, values)
        if refused:
            self.notify(_("Valeurs refusées (nombre hors limites) : {keys}").format(keys=", ".join(refused)),
                        severity="error")
        else:
            self.notify(_("Seuils enregistrés."))

    def _watch_breaker(self, snapshot: Snapshot) -> None:
        machine = snapshot.machine
        now = self._clock()
        self._samples.append(Sample(now, machine.tailscaled_cpu_percent, machine.temperature_c))
        watching = snapshot.watch is not None and snapshot.watch.alive
        if (self.survival is None or self._proposing or now < self._snooze_until or snapshot.cut is not None
                or not snapshot.funnel or not snapshot.is_operator or watching):  # la veille agit seule
            return
        policy = self.policy()
        trigger = assess(tuple(self._samples), policy)
        if trigger is None:
            return
        self._proposing = True
        ports = ", ".join(str(item.port) for item in snapshot.funnel)
        self.push_screen(BreakerProposalScreen(reason=_(trigger.reason).format(**trigger.params),
                                               minutes=policy.minutes, ports=ports), self._proposal_answered)

    def _proposal_answered(self, choice: str | None) -> None:
        self._proposing = False
        if choice == "minutes":
            self.cut_funnel(self.policy().minutes)
        elif choice == "total":
            self.cut_funnel(None)
        else:
            self._snooze_until = self._clock() + SNOOZE_MINUTES * 60
            self.notify(_("Pas de nouvelle proposition pendant {minutes} min.").format(minutes=SNOOZE_MINUTES))

    def ask_cut(self, minutes: int | None) -> None:
        text = (_("Funnel sera coupé {minutes} min puis remis en route automatiquement, à l'identique (minuterie "
                  "systemd : sudo une fois, dans le terminal).").format(minutes=minutes) if minutes else
                _("Funnel sera coupé jusqu'à ce que vous le rétablissiez (« Rétablir maintenant »)."))
        self.push_screen(ConfirmScreen(title=_("COUPER FUNNEL ?"), text=text + "\n\n" + _(
            "Les connexions venues d'Internet s'arrêtent aussitôt ; le tailnet (Serve, SSH) n'est pas touché."),
            yes=_("Couper"), no=_("Annuler")), lambda confirmed: self.cut_funnel(minutes) if confirmed else None)

    def exporting(self) -> AbstractContextManager[None]:
        """Langue des exports le temps d'un export (lot 9)."""
        return exporting(self.settings.store if self.settings is not None else None)

    def _outcome(self, outcome: Outcome) -> None:
        self.notify(outcome_text(outcome), title=_("Disjoncteur"),
                    severity="information" if outcome.ok else "error", timeout=10)
        self.request_refresh()

    def cut_funnel(self, minutes: int | None) -> None:
        if self.survival is None:
            return
        survival = self.survival

        def schedule(command: Sequence[str]) -> int:
            return self.run_in_terminal([tuple(command)])

        try:
            outcome = survival.cut(minutes, schedule=schedule)
        except (OSError, ValueError) as error:
            self.notify(str(error), title=_("Disjoncteur"), severity="error")
            return
        self._outcome(outcome)

    def restore_funnel(self) -> None:
        if self.survival is None:
            return
        survival = self.survival

        def work() -> None:
            try:
                outcome = survival.restore()
            except (OSError, ValueError) as error:
                self.call_from_thread(self.notify, str(error), title=_("Disjoncteur"), severity="error")
                return
            self.call_from_thread(self._outcome, outcome)

        self.run_worker(work, thread=True, group="restore", exclusive=True)

    # ---- pare-feu Funnel (porte HAProxy) ----
    def gate_state_text(self) -> str:
        gate = self.gate
        if gate is None:
            return _("Pare-feu indisponible.")
        haproxy = gate.machine.haproxy()
        state = gate.state()
        service = self.snapshot.gate_service if self.snapshot is not None else None
        lines = [_("HAProxy : {path}").format(path=haproxy or _("non installé (« Installer HAProxy »)"))]
        if service is not None and service.known:
            lines.append(_("Service de la porte : {state}").format(
                state=_("actif") if service.running else _("arrêté")))
        if state is not None:
            lines.append(_("Protection ACTIVE depuis {since} : Funnel {port} → porte 127.0.0.1:{gate} → {backend}")
                         .format(since=state.since[:16].replace("T", " "), port=state.public_port,
                                 gate=state.gate_port, backend=state.backend))
            counters = gate.counters()
            lines.append(_("Connexions : {total} reçues · {refused} refusées avant chiffrement · {current} en cours")
                         .format(total=counters.total, refused=counters.refused, current=counters.current))
        else:
            try:
                target = gate.target()
                lines.append(_("Protection inactive. Funnel {port} (HTTPS par tailscaled) → {backend} : pris en "
                               "charge.").format(port=target.public_port, backend=target.backend.address))
            except (ValueError, OSError) as error:
                lines.append(_("Protection inactive : {reason}.").format(reason=error))
        days = gate.certificate_days()
        if days is not None:
            lines.append(_("Certificat : encore {days} jour(s) (renouvelé chaque jour si besoin)").format(days=days))
        policy = gate.policy()
        lines.append(_("Mode : {mode} · {ip} connexions / 10 s par adresse · budget {budget} / s · blocage {block} min")
                     .format(mode=_(policy.mode), ip=policy.ip_per_10s, budget=policy.global_per_s,
                             block=policy.block_minutes))
        if self.snapshot is not None and not self.snapshot.is_operator:
            lines.append(_("⚠ Devenez opérateur de Tailscale (tableau de bord) : la porte en a besoin."))
        return "\n".join(lines)

    def _refresh_gate_screens(self) -> None:
        for screen in self.screen_stack:
            refresh = getattr(screen, "refresh_state", None)
            if callable(refresh):
                with contextlib.suppress(Exception):
                    refresh()

    def gate_action(self, action: Callable[[GateTools], Outcome], after: Callable[[], None] | None = None) -> None:
        gate = self.gate
        if gate is None:
            return

        def work() -> None:
            try:
                outcome = action(gate)
            except (OSError, ValueError) as error:
                self.call_from_thread(self.notify, str(error), title=_("Pare-feu"), severity="error")
                return
            self.call_from_thread(self._gate_outcome, outcome, after)

        self.run_worker(work, thread=True, group="gate", exclusive=True)

    def _gate_outcome(self, outcome: Outcome, after: Callable[[], None] | None = None) -> None:
        text = outcome_text(outcome)
        if outcome.ok and outcome.params.get("inactive"):
            text += "\n" + _("La porte n'est pas active : les listes s'appliqueront à son activation.")
        severity: Literal["information", "warning", "error"] = (
            "error" if not outcome.ok else "warning" if outcome.params.get("warning") else "information")
        self.notify(text, title=_("Pare-feu"), severity=severity, timeout=12)
        self._refresh_gate_screens()
        if after is not None:
            after()
        self.request_refresh()

    @property
    def version(self) -> str:
        return self._version

    # ---- publication (Serve et Funnel) ----
    def publication_action(self, action: Callable[[PublicationTools], Outcome],
                           after: Callable[[], None] | None = None) -> None:
        tools = self.publication
        if tools is None:
            return

        def work() -> None:
            try:
                outcome = action(tools)
            except (OSError, ValueError) as error:
                self.call_from_thread(self.notify, str(error), title=_("Publication"), severity="error")
                return
            self.call_from_thread(self._publication_outcome, outcome, after)

        self.notify(_("Changement en cours, puis vérification…"), title=_("Publication"))
        self.run_worker(work, thread=True, group="publication", exclusive=True)

    def _publication_outcome(self, outcome: Outcome, after: Callable[[], None] | None) -> None:
        self.notify(outcome_text(outcome), title=_("Publication"),
                    severity="information" if outcome.ok else "error", timeout=12)
        if after is not None:
            after()
        self.request_refresh()

    def install_haproxy(self) -> None:
        if self.gate is None:
            return
        command = self.gate.install_command()
        if not command:
            self.notify(_("Gestionnaire de paquets inconnu : installez HAProxy avec celui de votre système."),
                        severity="error")
            return
        self._confirm_commands(_("INSTALLER HAPROXY ?"), _(
            "HAProxy est installé par le gestionnaire de paquets de la distribution (mises à jour de sécurité "
            "comprises)."), [command])

    def activate_gate(self) -> None:
        if self.gate is None:
            return
        self.push_screen(ConfirmScreen(title=_("ACTIVER LA PROTECTION ?"), text=_(
            "1. Préparation (certificat *.ts.net, listes, configuration vérifiée).\n"
            "2. Services de la porte et de son certificat (sudo, dans le terminal ; la porte tourne sous votre "
            "compte, jamais en root).\n"
            "3. Bascule de Funnel vers la porte, puis essai depuis Internet. En cas d'échec, la publication "
            "d'origine est remise aussitôt.\n\nCoupure du site : quelques secondes pendant la bascule."),
            yes=_("Activer"), no=_("Annuler")), lambda confirmed: self._activate_prepare() if confirmed else None)

    def _activate_prepare(self) -> None:
        gate = self.gate
        if gate is None:
            return

        def work() -> None:
            outcome = gate.prepare()
            self.call_from_thread(self._activate_services, outcome)

        self.notify(_("Préparation de la porte…"), title=_("Pare-feu"))
        self.run_worker(work, thread=True, group="gate", exclusive=True)

    def _activate_services(self, outcome: Outcome) -> None:
        gate = self.gate
        if gate is None or not outcome.ok:
            self._gate_outcome(outcome)
            return
        if self.run_in_terminal(gate.service_commands()) != 0:
            return
        self.notify(_("Porte lancée ; bascule de Funnel et essai depuis Internet…"), title=_("Pare-feu"))
        self.gate_action(lambda tools: tools.switch(wait=time.sleep))

    def deactivate_gate(self) -> None:
        if self.gate is None:
            return
        self.push_screen(ConfirmScreen(title=_("DÉSACTIVER LA PROTECTION ?"), text=_(
            "Funnel est remis exactement comme avant (HTTPS par tailscaled), vérifié, puis la porte est arrêtée "
            "(sudo, dans le terminal). Vos réglages et vos listes sont gardés."),
            yes=_("Désactiver"), no=_("Annuler")), lambda confirmed: self._deactivate() if confirmed else None)

    def _deactivate(self) -> None:
        gate = self.gate
        if gate is None:
            return

        def work() -> None:
            outcome = gate.unswitch()
            self.call_from_thread(self._deactivate_services, outcome)

        self.run_worker(work, thread=True, group="gate", exclusive=True)

    def _deactivate_services(self, outcome: Outcome) -> None:
        self._gate_outcome(outcome)
        if outcome.ok and self.gate is not None:
            self.run_in_terminal(self.gate.stop_commands())

    # ---- confinement ----
    def confine(self, *, restart: bool, ssh_unit: str) -> None:
        if self.survival is None or self.snapshot is None:
            return
        from omega_tail.domain.confinement import recommended

        commands = self.survival.confine_commands(recommended(self.snapshot.machine.cpu_count), restart=restart,
                                                  ssh_unit=ssh_unit, pid=self.snapshot.service.main_pid)
        if not commands:
            self.notify(_("tailscaled ne tourne pas : rien à confiner."), severity="warning")
            return
        if self.survival.init is InitSystem.SYSTEMD:
            text = _("Pose le fichier d'ajout {path} (votre propre override.conf n'est pas modifié), recharge "
                     "systemd{restart}.").format(path=DROP_IN_PATH,
                                                 restart=_(", puis redémarre tailscaled") if restart else "")
            if restart:
                commands, text = self._fix_first(commands, text)
        else:
            text = _("Place tailscaled dans un groupe de contrôle à part (cgroup v2), avec son plafond et sa priorité. "
                     "Aucun de vos fichiers n'est modifié. Perdu si tailscaled redémarre : omega-tail le signalera.")
        self._confirm_commands(_("CONFINER TAILSCALED ?"), text, commands)

    def unconfine(self, *, restart: bool, ssh_unit: str) -> None:
        if self.survival is None:
            return
        pid = self.snapshot.service.main_pid if self.snapshot is not None else 0
        commands = self.survival.unconfine_commands(restart=restart, ssh_unit=ssh_unit, pid=pid)
        text = _("Supprime les fichiers d'ajout posés par omega-tail, puis recharge systemd.")
        if restart:
            commands, text = self._fix_first(commands, text)
        self._confirm_commands(_("RETIRER LE CONFINEMENT ?"), text, commands)

    # ---- demarrage de tailscaled (piege du « tailscale up », domain/startup.py) ----
    def startup_fix(self) -> list[tuple[str, ...]]:
        if self.survival is None or self.snapshot is None:
            return []
        return self.survival.startup_fix_commands(self.snapshot.service, self.read_file)

    def _fix_first(self, commands: list[tuple[str, ...]], text: str) -> tuple[list[tuple[str, ...]], str]:
        """Avant un redemarrage de tailscaled : corrige d'abord le demarrage s'il echouerait."""
        fix = self.startup_fix()
        if not fix:
            return commands, text
        return fix + commands, text + "\n\n⚠ " + _(STARTUP_FIX_TEXT)

    def fix_startup(self) -> None:
        commands = self.startup_fix()
        if not commands:
            self.notify(_("Rien à corriger ici : la commande n'est pas dans un fichier de /etc/systemd (à corriger "
                          "à la main, avec « - » devant la commande)."), severity="warning", timeout=10)
            return
        self._confirm_commands(_("CORRIGER LE DÉMARRAGE DE TAILSCALED ?"), _(STARTUP_FIX_TEXT), commands)

    def confirm_commands(self, title: str, text: str, commands: list[tuple[str, ...]]) -> None:
        """Montre les commandes, demande confirmation, puis les lance dans le vrai terminal."""
        self._confirm_commands(title, text, commands)

    def _confirm_commands(self, title: str, text: str, commands: list[tuple[str, ...]]) -> None:
        listing = "\n".join("  " + " ".join(command) for command in commands)
        guard = ""
        if self.snapshot is not None and self.snapshot.through_tailscale and any(
                "restart" in command for command in commands):
            guard = "\n\n⚠ " + _("Cette session passe par Tailscale : elle se figera quelques secondes pendant le "
                                  "redémarrage, puis reviendra en général.")
        self.push_screen(ConfirmScreen(title=title, text=text + "\n\n" + _("Commandes :") + "\n" + listing + guard,
                                       yes=_("Lancer"), no=_("Annuler")),
                         lambda confirmed: self._after_commands(self.run_in_terminal(commands)) if confirmed
                         else None)

    def _after_commands(self, code: int) -> None:
        self.request_refresh()

    # ---- veille automatique ----
    def set_watch(self, on: bool) -> None:
        """Active ou desactive le service de la veille (sudo dans le terminal, commandes montrees avant)."""
        watch = self.watch_tools
        if watch is None:
            return
        if on and (self.snapshot is None or not self.snapshot.is_operator):
            self.notify(_("La veille coupe et remet Funnel sous votre compte : devenez d'abord opérateur de "
                          "Tailscale (tableau de bord)."), severity="error", timeout=10)
            return
        commands = watch.start_commands() if on else watch.stop_commands()
        listing = "\n".join("  " + " ".join(command) for command in commands)
        text = (_("La veille tournera en permanence, sous votre compte (jamais root), même omega-tail fermé. Sous "
                  "attaque, elle coupe Funnel seule par paliers (15 min, 30 min, puis 1 h renouvelable) et le "
                  "remet en route seule.") if on else
                _("La veille s'arrête : sous attaque, omega-tail ouvert vous proposera de nouveau la coupure."))
        self.push_screen(ConfirmScreen(
            title=_("ACTIVER LA VEILLE AUTOMATIQUE ?") if on else _("DÉSACTIVER LA VEILLE AUTOMATIQUE ?"),
            text=text + "\n\n" + _("Commandes :") + "\n" + listing, yes=_("Lancer"), no=_("Annuler")),
            lambda confirmed: self._watch_done(on, self.run_in_terminal(commands)) if confirmed else None)

    def _watch_done(self, on: bool, code: int) -> None:
        if self.watch_tools is not None and code == 0:
            self.watch_tools.mark_installed(on)
            self.notify(_("Veille automatique activée.") if on else _("Veille automatique désactivée."))
        elif code != 0:
            self.notify(_("Commande refusée (code {code}) : rien n'a changé.").format(code=code), severity="error")
        self.request_refresh()

    def shield_action(self, action: ShieldAction, mode: ShieldMode | None = None, *, refused: int = 0) -> None:
        """Bouclier du port WireGuard : commandes montrees avant, lancees dans le terminal (sudo)."""
        tools = self.shield
        if tools is None:
            return
        plan = tools.plan(action, mode)
        if plan.refusal:
            self.notify(_(REFUSALS.get(plan.refusal, plan.refusal)), severity="error", timeout=12)
            return
        listing = "\n".join("  " + " ".join(command) for command in plan.commands)
        text = confirm_text(action, mode, refused, plan.via_fire) + "\n\n" + _("Commandes :") + "\n" + listing
        self.push_screen(ConfirmScreen(title=_(TITLES[action]), text=text, yes=_("Lancer"), no=_("Annuler")),
                         lambda confirmed: self._shield_done(action, self.run_in_terminal(plan.commands))
                         if confirmed else None)

    def _shield_done(self, action: ShieldAction, code: int) -> None:
        if self.shield is not None:
            self.shield.finished(action, code == 0)
        if isinstance(self.screen, ShieldScreen):
            self.screen.build()

    # ---- navigation ----
    def screen_for(self, key: str) -> Screen[None] | None:
        if key == "dashboard":
            return DashboardScreen()
        if key == "service":
            return ServiceScreen()
        if key == "journals":
            return JournalsScreen()
        if key == "connection" and self.connection is not None:
            return ConnectionScreen()
        if key == "publication" and self.publication is not None:
            return PublicationScreen()
        if key == "survival":
            return SurvivalScreen()
        if key == "shield" and self.shield is not None:
            return ShieldScreen()
        if key == "firewall" and self.gate is not None:
            return FirewallScreen()
        if key == "attacks" and self.gate is not None:
            return AttacksScreen()
        if key == "network" and self.network is not None:
            return NetworkScreen()
        if key == "report" and self.report is not None:
            return ReportScreen()
        if key == "settings" and self.settings is not None:
            return SettingsScreen(tools=self.settings)
        if key == "help":
            contact = self._contact
            return HelpScreen(version=self._version, writer=self.writer,
                              contact=(lambda: contact_support_screen(contact)) if contact is not None else None)
        return None

    def open_key(self, key: str) -> None:
        item = entry(key)
        screen = None if item is None or item.planned else self.screen_for(key)
        if screen is not None:
            self.push_screen(screen)
        else:
            planned_notice(self, key)

    # ---- actions dans le vrai terminal ----
    def run_in_terminal(self, commands: Sequence[Sequence[str]]) -> int:
        """Lance les commandes une a une dans le vrai terminal (invite sudo comprise), s'arrete a la premiere qui
        echoue ; renvoie le code de la derniere lancee."""
        code = 0
        shown = [" ".join(command) for command in commands]
        with suspended(self, _("omega-tail — commandes lancées une à une :") + "\n" + "\n".join(
                f"  {line}" for line in shown) + "\n" + _("Le mot de passe sudo ne s'affiche pas pendant la saisie.")):
            stream = sys.__stdout__
            for command, line in zip(commands, shown, strict=True):
                if stream is not None:
                    with contextlib.suppress(OSError):
                        stream.write(f"\n$ {line}\n")
                        stream.flush()
                code = self._actions.run(command)
                if code != 0:
                    break
            if stream is not None:
                with contextlib.suppress(OSError):
                    stream.write("\n" + (_("✔ Terminé.") if code == 0 else _("✖ Échec (code {code}).").format(
                        code=code)) + "\n")
                    stream.flush()
            with contextlib.suppress(EOFError, OSError):
                input(_("Entrée pour revenir à omega-tail… "))
        if code == 0:
            self.notify(_("Fait : {command}").format(command=shown[-1] if shown else ""))
        else:
            self.notify(_("Échec (code {code}) : {command}").format(code=code, command=" ; ".join(shown)),
                        severity="error")
        self.request_refresh()
        return code

    def service_command_for(self, action: ServiceAction) -> tuple[str, ...]:
        """Commande du service tailscaled selon le systeme d'init de la machine."""
        service = self.snapshot.service if self.snapshot is not None else None
        init = InitSystem(service.init) if service is not None and service.init in InitSystem._value2member_map_ \
            else InitSystem.SYSTEMD
        return service_command(action, as_root=self.as_root, init=init, name=service.name if service else "")

    def service_commands_for(self, action: ServiceAction) -> tuple[list[tuple[str, ...]], str]:
        """Commandes d'une action sur le service ; avant un (re)demarrage, la correction du demarrage s'il le faut,
        avec sa phrase d'explication (vide sinon)."""
        commands = [self.service_command_for(action)]
        if action is ServiceAction.STOP:
            return commands, ""
        fixed, text = self._fix_first(commands, "")
        return fixed, text.strip().removeprefix("⚠ ")

    def run_service_action(self, action: ServiceAction, commands: list[tuple[str, ...]] | None = None) -> None:
        self.run_in_terminal(commands or [self.service_command_for(action)])

    def become_operator(self) -> None:
        snapshot = self.snapshot
        user = snapshot.user if snapshot is not None else ""
        if not user or user == "root":
            self.notify(_("Compte inconnu ou root : rien à faire."))
            return
        commands, text = self._fix_first([operator_command(user, as_root=self.as_root)], _(
            "Le compte « {user} » pourra régler Tailscale (connexion, publication, préférences) sans sudo. "
            "Une seule fois ; annulable ensuite avec « sudo tailscale set --operator= ».").format(user=user))
        listing = "\n".join("  " + " ".join(command) for command in commands)
        self.push_screen(ConfirmScreen(
            title=_("DEVENIR OPÉRATEUR DE TAILSCALE ?"),
            text=text + "\n\n" + _("Commandes :") + "\n" + listing,
            yes=_("Lancer"), no=_("Annuler")),
            lambda confirmed: self._after_commands(self.run_in_terminal(commands)) if confirmed else None)

    # ---- cadre commun de la suite ----
    def _update_sub_title(self) -> None:
        """« theme | colonnes x lignes », comme les autres outils de la suite ; « r » la relit."""
        columns, rows = self.size.width, self.size.height
        if not columns:  # pas encore monte : taille du terminal
            columns, rows = shutil.get_terminal_size()
        self.sub_title = f"{self.theme} | {columns}x{rows}"

    def watch_theme(self, _theme_name: str) -> None:
        self._update_sub_title()
        settings = getattr(self, "settings", None)
        if settings is not None and settings.store.get(KEY_THEME) != self.theme:
            with contextlib.suppress(OSError):
                settings.store.set(KEY_THEME, self.theme)

    async def action_quit(self) -> None:
        self.push_screen(QuitConfirmScreen(), self._quit_if_confirmed)

    def _quit_if_confirmed(self, confirmed: bool | None) -> None:
        if confirmed:
            self.exit()

    def action_refresh_terminal(self) -> None:
        self.refresh(layout=True)
        self._update_sub_title()
        self.notify(f"{self.size.width}x{self.size.height}", title=_("Terminal rafraîchi"))
        self.request_refresh()

    def action_help(self) -> None:
        screen = self.screen_for("help")
        if screen is not None:
            self.push_screen(screen)

    def action_open_settings(self) -> None:
        screen = self.screen_for("settings")
        if screen is not None:
            self.push_screen(screen)

    def action_cycle_theme(self) -> None:
        names = list(TUI_THEMES)
        index = names.index(self.theme) if self.theme in names else 0
        self.theme = names[(index + 1) % len(names)]

    def get_system_commands(self, screen: Screen) -> Iterable[SystemCommand]:
        yield SystemCommand(_("Thème"), _("Changer le thème actif"), self.action_change_theme)
        yield SystemCommand(_("Quitter"), _("Quitter l'application (avec confirmation)"), self.action_quit)
        yield SystemCommand(_("Capture d'écran"), _("Enregistrer une capture SVG de l'écran courant"),
                            self.save_screen_capture)

    def save_screen_capture(self) -> None:
        directory = self.settings.screenshots_dir() if self.settings is not None else None
        if directory is None:
            self.notify(_("Dossier des captures non configuré."), severity="warning")
            return
        try:
            directory.mkdir(parents=True, exist_ok=True)
        except OSError as error:
            self.notify(str(error), severity="error")
            return
        self.deliver_screenshot(path=str(directory))
