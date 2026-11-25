# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Alertes du tableau de bord : chacune dit ce qui ne va pas et mene a l'ecran qui le corrige (proposition §3.1)."""
from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

from omega_tail.core.constants import (
    KEY_EXPIRY_WARNING_DAYS,
    TAILSCALED_CPU_WARNING_PERCENT,
    TEMPERATURE_CRITICAL_C,
    TEMPERATURE_WARNING_C,
)
from omega_tail.domain.blacklist import BLACKLIST_MAX, BLACKLIST_WARNING
from omega_tail.domain.snapshot import Snapshot
from omega_tail.domain.startup import risky_hooks
from omega_tail.domain.tailscale import BackendState
from omega_tail.shared.i18n import N_


class Level(str, Enum):
    CRITICAL = "critical"
    WARNING = "warning"
    INFO = "info"


class Target(str, Enum):
    """Ecran qui corrige (cle du menu) ; NONE : rien a ouvrir."""
    NONE = ""
    SERVICE = "service"
    CONNECTION = "connection"
    FIREWALL = "firewall"
    SURVIVAL = "survival"
    ATTACKS = "attacks"
    OPERATOR = "operator"
    """Pas un ecran : action « Devenir opérateur » du tableau de bord."""


@dataclass(frozen=True)
class Alert:
    level: Level
    code: str
    text: str
    """Phrase marquee pour la traduction ; `params` la complete (`_(text).format(**params)`)."""
    target: Target = Target.NONE
    params: Mapping[str, object] = field(default_factory=dict)


ORDER = {Level.CRITICAL: 0, Level.WARNING: 1, Level.INFO: 2}


def _time(text: str) -> datetime | None:
    try:
        return datetime.fromisoformat(text) if text else None
    except ValueError:
        return None


def alerts_for(snapshot: Snapshot, now: datetime) -> tuple[Alert, ...]:
    found: list[Alert] = []
    tailscale, service, machine = snapshot.tailscale, snapshot.service, snapshot.machine
    if not tailscale.installed:
        return (Alert(Level.CRITICAL, "not-installed", N_("Tailscale n'est pas installé sur cette machine.")),)
    if (service.known and not service.running) or not tailscale.reachable:
        found.append(Alert(Level.CRITICAL, "daemon-stopped",
                           N_("Le service tailscaled ne répond pas (arrêté ou en échec)."), Target.SERVICE))
    if tailscale.versions_differ:
        found.append(Alert(Level.WARNING, "daemon-outdated", N_(
            "tailscaled n'a pas été redémarré après la mise à jour : {daemon} en marche, {client} installé."),
            Target.SERVICE, {"daemon": tailscale.daemon_version, "client": tailscale.client_version}))
    if tailscale.reachable and tailscale.backend is BackendState.NEEDS_LOGIN:
        found.append(Alert(Level.WARNING, "needs-login", N_("Tailscale attend la connexion d'un compte."),
                           Target.CONNECTION))
    elif tailscale.reachable and tailscale.backend is BackendState.STOPPED:
        found.append(Alert(Level.WARNING, "stopped", N_("Tailscale est déconnecté (« tailscale down »)."),
                           Target.CONNECTION))
    if tailscale.key_expiry is not None:
        days = (tailscale.key_expiry - now).days
        if days < KEY_EXPIRY_WARNING_DAYS:
            found.append(Alert(Level.WARNING if days >= 0 else Level.CRITICAL, "key-expiry",
                               N_("La clé de cette machine expire dans {days} jour(s)."), Target.CONNECTION,
                               {"days": max(days, 0)}))
    gate = snapshot.gate_service
    if snapshot.gated and gate is not None and gate.known and not gate.running:
        found.append(Alert(Level.CRITICAL, "gate-down", N_(
            "Site en panne : Funnel passe par la porte (pare-feu), mais la porte est arrêtée."), Target.FIREWALL))
    if snapshot.gated and snapshot.gate_attack:
        found.append(Alert(Level.WARNING, "gate-attack", N_(
            "La porte est en MODE ATTAQUE : trop de connexions entrantes ; les regroupements (empreintes, AS, pays) "
            "s'appliquent jusqu'au retour au calme."), Target.FIREWALL))
    for publication in snapshot.publications:
        if publication.exposed:
            found.append(Alert(Level.WARNING, "funnel-unprotected", N_(
                "Funnel publié sans protection sur le port {port} : tailscaled fait le TLS de chaque connexion "
                "(une rafale peut saturer la machine)."), Target.FIREWALL, {"port": publication.port}))
    if machine.temperature_c is not None and machine.temperature_c >= TEMPERATURE_WARNING_C:
        critical = machine.temperature_c >= TEMPERATURE_CRITICAL_C
        found.append(Alert(Level.CRITICAL if critical else Level.WARNING, "temperature",
                           N_("Température élevée : {temperature:.0f} °C."), Target.SURVIVAL,
                           {"temperature": machine.temperature_c}))
    cpu = machine.tailscaled_cpu_percent
    if cpu is not None and cpu >= TAILSCALED_CPU_WARNING_PERCENT:
        found.append(Alert(Level.WARNING, "tailscaled-cpu",
                           N_("tailscaled consomme {cpu:.0f} % d'un cœur."), Target.SURVIVAL, {"cpu": cpu}))
    watch = snapshot.watch
    if watch is not None and watch.installed and not watch.alive:
        found.append(Alert(Level.WARNING, "watch-stopped", N_(
            "La veille automatique est activée mais ne tourne plus : Funnel ne sera pas coupé seul sous attaque."),
            Target.SURVIVAL))
    if snapshot.blacklist_count >= BLACKLIST_WARNING:
        found.append(Alert(Level.WARNING, "blacklist-large", N_(
            "Liste noire de la porte : {count} entrées (plafond {max}). Exportez-la puis purgez les plus anciennes : "
            "« Attaques et décisions » → « Gestion de la liste noire »."), Target.ATTACKS,
            {"count": snapshot.blacklist_count, "max": BLACKLIST_MAX}))
    shield = snapshot.shield
    if shield is not None and shield.missing:
        found.append(Alert(Level.WARNING, "shield-missing", N_(
            "Bouclier du port WireGuard ABSENT : un autre outil a effacé sa table (nft flush ruleset, pare-feu "
            "relancé…). Il n'est pas reposé seul : « Survie » → « Bouclier du port WireGuard » → « Reposer »."),
            Target.SURVIVAL))
    elif shield is not None and shield.stale:
        found.append(Alert(Level.WARNING, "shield-stale", N_(
            "Bouclier du port WireGuard : état non mis à jour depuis plus de 3 minutes (service "
            "omega-bouclier-wg arrêté ?)."), Target.SURVIVAL))
    if risky_hooks(service):
        found.append(Alert(Level.WARNING, "startup-up", N_(
            "Le démarrage de tailscaled lance « tailscale up » : si un réglage change (opérateur, nom, routes…), "
            "Tailscale le refusera et tailscaled ne redémarrera plus. « Service » → « Corriger le démarrage »."),
            Target.SERVICE))
    if service.confinement_lost:
        found.append(Alert(Level.WARNING, "confinement-lost", N_(
            "Confinement de tailscaled perdu (le service a redémarré) : « Survie » → « Appliquer le confinement »."),
            Target.SURVIVAL))
    elif snapshot.funnel and service.known and not service.confined:
        found.append(Alert(Level.INFO, "not-confined", N_(
            "tailscaled n'est pas confiné : sous attaque, il peut prendre tous les cœurs."), Target.SURVIVAL))
    if tailscale.reachable and snapshot.preferences.readable and not snapshot.is_operator:
        found.append(Alert(Level.INFO, "not-operator", N_(
            "Vous n'êtes pas opérateur de Tailscale : chaque réglage demandera sudo."), Target.OPERATOR))
    cut = snapshot.cut
    if cut is not None:
        until = _time(cut.until)
        if cut.total:
            found.append(Alert(Level.WARNING, "funnel-cut-total", N_(
                "Funnel coupé par omega-tail (coupure totale) : remise en route manuelle, dans « Survie »."),
                Target.SURVIVAL))
        elif until is not None and until < now:
            found.append(Alert(Level.WARNING, "funnel-restore-overdue", N_(
                "Funnel devait être remis en route à {time} et ne l'est pas : « Rétablir » dans « Survie »."),
                Target.SURVIVAL, {"time": until.astimezone().strftime("%H:%M")}))
        else:
            found.append(Alert(Level.INFO, "funnel-cut", N_(
                "Funnel coupé par omega-tail jusqu'à {time}, puis remis en route automatiquement."),
                Target.SURVIVAL, {"time": until.astimezone().strftime("%H:%M") if until else "?"}))
    for message in tailscale.health:
        target = Target.CONNECTION if "IP forwarding is disabled" in message else Target.NONE
        found.append(Alert(Level.WARNING, "health", N_("Tailscale signale : {message}"), target,
                           {"message": message}))
    return tuple(sorted(found, key=lambda alert: ORDER[alert.level]))
