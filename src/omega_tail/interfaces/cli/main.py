# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Ligne de commande : sans argument, l'interface ; `etat` (texte ou JSON), `rapport`, `aide`, `--version`."""
from __future__ import annotations

import argparse
import sys
import time
from collections.abc import Callable, Sequence

from omega_tail.application.gate import GateTools, certificate_needs_renewal
from omega_tail.application.report import ReportTools
from omega_tail.application.survival import Outcome, SurvivalTools
from omega_tail.application.watch import WatchTools
from omega_tail.domain.alerts import Alert
from omega_tail.domain.groups import reason_pairs
from omega_tail.domain.snapshot import Snapshot
from omega_tail.domain.text import without_controls
from omega_tail.interfaces.cli.state_view import state_json, state_text
from omega_tail.interfaces.shared.help_view import help_text
from omega_tail.interfaces.shared.messages import group_label, outcome_text
from omega_tail.interfaces.shared.report_view import FORMATS, export_name, render
from omega_tail.ports.export import ExportWriter
from omega_tail.shared.i18n import _

StateFunction = Callable[[], tuple[Snapshot, tuple[Alert, ...]]]
DashboardFunction = Callable[[], int]
TerminalCommand = Callable[[Sequence[str]], int]
ReportSetup = Callable[[], tuple[ReportTools, ExportWriter, str]]
"""Outils du rapport, dossier des exports, theme d'export."""


def parser(version: str) -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(prog="omega-tail", description=_("Pilotage de Tailscale et protection de Funnel."))
    root.add_argument("--version", action="version", version=f"omega-tail {version}")
    commands = root.add_subparsers(dest="command")
    state = commands.add_parser("etat", help=_("état de Tailscale, de la machine et alertes"))
    state.add_argument("--format", choices=("texte", "json"), default="texte")
    commands.add_parser("aide", help=_("aide complète en texte"))
    report = commands.add_parser("rapport", help=_("rapport de la machine (faits seulement)"))
    report.add_argument("--format", choices=FORMATS, default="txt")
    report.add_argument("--exporter", action="store_true",
                        help=_("enregistrer dans le dossier des exports (sinon : affiché)"))
    report.add_argument("--prive", action="store_true",
                        help=_("inclure le compte Tailscale et les noms / adresses des appareils du tailnet"))
    breaker = commands.add_parser("disjoncteur", help=_("couper ou remettre Funnel (Survie)"))
    actions = breaker.add_subparsers(dest="action", required=True)
    actions.add_parser("etat", help=_("coupure en cours"))
    cut = actions.add_parser("couper", help=_("couper Funnel"))
    how = cut.add_mutually_exclusive_group(required=True)
    how.add_argument("--minutes", type=int, help=_("coupure momentanée, remise en route automatique (minuterie)"))
    how.add_argument("--totale", action="store_true", help=_("coupure jusqu'à « retablir »"))
    restore = actions.add_parser("retablir", help=_("remettre Funnel à l'identique"))
    restore.add_argument("--id", default="", help=_("coupure visée (minuterie) ; une autre coupure est ignorée"))
    restore.add_argument("--attendre", type=int, default=0, help=_("secondes d'attente avant (hors systemd)"))
    watch = commands.add_parser("veille", help=_("veille automatique (coupe Funnel seule sous attaque)"))
    watch_actions = watch.add_subparsers(dest="action", required=True)
    watch_actions.add_parser("lancer", help=_("tourner en continu (lancé par le service de la veille)"))
    watch_actions.add_parser("etat", help=_("état de la veille et dernières lignes du journal"))
    gate = commands.add_parser("porte", help=_("pare-feu Funnel (porte HAProxy)"))
    gate_actions = gate.add_subparsers(dest="action", required=True)
    gate_actions.add_parser("etat", help=_("état de la porte et compteurs"))
    certificate = gate_actions.add_parser("certificat", help=_("renouveler le certificat *.ts.net de la porte"))
    certificate.add_argument("--si-besoin", action="store_true", help=_("seulement s'il expire dans moins de 30 jours"))
    gate_actions.add_parser("groupes", help=_("regroupements : mode attaque, empreintes, AS, pays (lot 6)"))
    gate_actions.add_parser("base", help=_("mettre à jour la base AS / pays (DB-IP Lite)"))
    block = gate_actions.add_parser("bloquer", help=_("bloquer une adresse (durée de blocage) ou un réseau"))
    block.add_argument("adresse")
    block.add_argument("--toujours", action="store_true", help=_("liste noire, jusqu'à « debloquer »"))
    for name, text in (("debloquer", _("débloquer une adresse ou un réseau")),
                       ("confiance", _("mettre en confiance (jamais limitée)"))):
        gate_actions.add_parser(name, help=text).add_argument("adresse")
    return root


def report_command(arguments: argparse.Namespace, setup: ReportSetup) -> int:
    tools, writer, theme = setup()
    tools.snapshots.collect()  # deux lectures a une seconde : la seconde donne le % CPU de tailscaled
    time.sleep(1)
    facts = tools.build(include_private=arguments.prive, snapshot=tools.snapshots.collect())
    content, extension = render(facts, arguments.format, theme)
    if not arguments.exporter:
        # Vers le terminal : aucun caractere de controle (noms declares par les machines du tailnet, F7)
        sys.stdout.write(without_controls(content, keep="\n\t"))
        return 0
    try:
        path = writer.save(export_name(facts, extension), content)
    except (OSError, ValueError) as error:
        sys.stderr.write(_("Export impossible : {error}").format(error=error) + "\n")
        return 1
    sys.stdout.write(_("Rapport enregistré : {path}").format(path=path) + "\n")
    return 0


def breaker(arguments: argparse.Namespace, survival: SurvivalTools, terminal: TerminalCommand | None) -> int:

    if arguments.action == "etat":
        cut = survival.store.current()
        if cut is None:
            sys.stdout.write(_("Funnel n'est pas coupé par omega-tail.") + "\n")
        else:
            until = (_("remise en route prévue {when}").format(when=cut.until) if cut.until
                     else _("coupure totale"))
            sys.stdout.write(_("Funnel coupé depuis {since} ({until}), ports {ports} ; sauvegarde {saved}").format(
                since=cut.cut_at, until=until, ports=", ".join(map(str, cut.ports)), saved=cut.saved) + "\n")
        return 0
    if arguments.action == "couper":
        if arguments.minutes is not None and arguments.minutes < 1:
            sys.stderr.write(_("--minutes : 1 au moins.") + "\n")
            return 2
        outcome = survival.cut(None if arguments.totale else arguments.minutes, schedule=terminal)
    else:
        if arguments.attendre > 0:
            import time

            time.sleep(min(arguments.attendre, 7 * 24 * 3600))
        outcome = survival.restore(arguments.id)
    stream = sys.stdout if outcome.ok else sys.stderr
    stream.write(outcome_text(outcome) + "\n")
    return 0 if outcome.ok else 1


def _say(outcome: Outcome) -> int:
    stream = sys.stdout if outcome.ok else sys.stderr
    stream.write(outcome_text(outcome) + "\n")
    if outcome.ok and outcome.params.get("inactive"):
        stream.write(_("La porte n'est pas active : les listes s'appliqueront à son activation.") + "\n")
    return 0 if outcome.ok else 1


def watch_state(tools: WatchTools) -> int:
    status = tools.status()
    if not status.installed:
        sys.stdout.write(_("Veille automatique : désactivée.") + "\n")
    else:
        alive = _("en marche") if status.alive else _("ARRÊTÉE (signe de vie trop vieux)")
        sys.stdout.write(_("Veille automatique : {state} ; dépassements récents {strikes}/3 ; prochaine coupure "
                           "{minutes} min").format(state=alive, strikes=status.strikes,
                                                   minutes=status.next_minutes) + "\n")
    for line in tools.journal(10):
        sys.stdout.write(f"  {line}\n")
    return 0 if status.alive or not status.installed else 1


def gate_command(arguments: argparse.Namespace, gate: GateTools) -> int:
    if arguments.action == "etat":
        state, counters, days = gate.state(), gate.counters(), gate.certificate_days()
        if state is None:
            sys.stdout.write(_("Porte inactive : Funnel ne passe pas par elle.") + "\n")
        else:
            sys.stdout.write(_("Porte active depuis {since} : Funnel {port} -> 127.0.0.1:{gate} -> {backend}").format(
                since=state.since, port=state.public_port, gate=state.gate_port, backend=state.backend) + "\n")
            sys.stdout.write(_("Connexions : {total} reçues, {refused} refusées avant chiffrement, {current} en "
                               "cours").format(total=counters.total, refused=counters.refused,
                                               current=counters.current) + "\n")
        left = "—" if days is None else _("{days} jour(s) restants").format(days=days)
        sys.stdout.write(_("Certificat : {left}").format(left=left) + "\n")
        return 0
    if arguments.action == "certificat":
        days = gate.certificate_days()
        if arguments.si_besoin and not certificate_needs_renewal(days):
            sys.stdout.write(_("Certificat valable encore {days} jour(s) : rien à faire.").format(days=days) + "\n")
            return 0
        return _say(gate.renew_certificate(hot=gate.state() is not None))
    if arguments.action in ("groupes", "base"):
        return groups_command(arguments.action, gate)
    if arguments.action == "bloquer":
        return _say(gate.block(arguments.adresse, forever=arguments.toujours))
    if arguments.action == "debloquer":
        return _say(gate.unblock(arguments.adresse))
    return _say(gate.trust(arguments.adresse))


def groups_command(action: str, gate: GateTools) -> int:
    groups = gate.groups
    if groups is None:
        sys.stdout.write(_("Regroupements indisponibles.") + "\n")
        return 2
    if action == "base":
        return _say(groups.refresh_base(reload=gate.state() is not None))
    status = groups.status()
    if not status.lua:
        sys.stdout.write(_("HAProxy sans Lua : regroupements (JA4, AS, pays) indisponibles, porte du lot 4 "
                           "seule.") + "\n")
        return 1
    policy = status.policy
    mode = _("appliqués") if policy.mode == "applique" else _("observation (rien n'est refusé par ces règles)")
    attack = (_("ATTAQUE (retour au normal dans {seconds} s sans dépassement)").format(seconds=status.calm_left_s)
              if status.attack else _("normal"))
    sys.stdout.write(_("Regroupements : {mode} ; mode {attack}").format(mode=mode, attack=attack) + "\n")
    sys.stdout.write(_("Mode attaque au-delà de {rate} connexions entrantes / s ; calme {minutes} min").format(
        rate=policy.attack_per_s, minutes=policy.calm_minutes) + "\n")
    learning = (_("référence prête") if status.learning_days_left == 0
                else _("apprentissage : encore {days} jour(s)").format(days=status.learning_days_left))
    sys.stdout.write(_("Empreintes habituelles : {known} ({learning})").format(known=status.known,
                                                                             learning=learning) + "\n")
    base = (_("mise à jour il y a {days} jour(s)").format(days=status.base_days) if status.base_days is not None
            else _("absente (« omega-tail porte base »)"))
    sys.stdout.write(_("Base AS / pays : {base}").format(base=base) + "\n")
    if status.reasons:
        found = ", ".join(f"{_(label)} {count}" for label, count in reason_pairs(status.reasons))
        line = (_("Connexions refusées (7 j) : {found}") if policy.mode == "applique"
                else _("Connexions qui auraient été refusées (7 j) : {found}"))
        sys.stdout.write(line.format(found=found) + "\n")
    for title, rows in ((_("Empreintes les plus actives (connexions / 10 s, total) :"), groups.top_fingerprints(5)),
                        (_("AS les plus actifs (connexions / 10 s, total) :"), groups.top_as(5)),
                        (_("Pays les plus actifs (connexions / 10 s, total) :"), groups.top_countries(5))):
        if rows:
            sys.stdout.write(title + "\n")
            for row in rows:
                sys.stdout.write(f"  {row.key}  {row.rate_10s}  {row.count}  {group_label(row)}\n")
    return 0


def main_with(argv: list[str] | None, *, version: str, state: StateFunction, dashboard: DashboardFunction,
              survival: Callable[[], SurvivalTools] | None = None, terminal: TerminalCommand | None = None,
              gate: Callable[[], GateTools] | None = None, watch_run: Callable[[], int] | None = None,
              watch: Callable[[], WatchTools] | None = None, report: ReportSetup | None = None) -> int:
    arguments = parser(version).parse_args(argv)
    if arguments.command == "rapport":
        return report_command(arguments, report) if report is not None else 2
    if arguments.command == "veille":
        if arguments.action == "lancer":
            return watch_run() if watch_run is not None else 2
        return watch_state(watch()) if watch is not None else 2
    if arguments.command == "porte":
        return gate_command(arguments, gate()) if gate is not None else 2
    if arguments.command == "disjoncteur":
        if survival is None:
            return 2
        return breaker(arguments, survival(), terminal)
    if arguments.command == "etat":
        snapshot, alerts = state()
        render = state_json if arguments.format == "json" else state_text
        sys.stdout.write(render(snapshot, alerts, version))
        return 1 if any(alert.level.value == "critical" for alert in alerts) else 0
    if arguments.command == "aide":
        sys.stdout.write(help_text())
        return 0
    return dashboard()
