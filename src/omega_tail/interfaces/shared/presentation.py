# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Mise en forme commune (bande d'etat, tableau de bord, ligne de commande) : textes traduits, tailles lisibles."""
from __future__ import annotations

from omega_lib.shield.models import ShieldMode

from omega_tail.domain.alerts import Alert, Level
from omega_tail.domain.service import ServiceState
from omega_tail.domain.shield import ShieldFacts
from omega_tail.domain.tailscale import BackendState, Publication, PublishMode
from omega_tail.shared.i18n import N_, _

BACKEND_LABELS = {
    BackendState.RUNNING: N_("connecté"), BackendState.STOPPED: N_("déconnecté"),
    BackendState.NEEDS_LOGIN: N_("connexion du compte attendue"),
    BackendState.NEEDS_MACHINE_AUTH: N_("machine à approuver dans la console"),
    BackendState.STARTING: N_("démarrage"), BackendState.NO_STATE: N_("sans état"),
    BackendState.UNKNOWN: N_("inconnu"),
}
MODE_LABELS = {
    PublishMode.HTTPS: N_("HTTPS (TLS par tailscaled)"), PublishMode.HTTP: N_("HTTP"),
    PublishMode.TCP: N_("TCP (TLS transmis tel quel)"),
    PublishMode.TLS_TERMINATED_TCP: N_("TCP, TLS par tailscaled"),
}
LEVEL_MARKS = {Level.CRITICAL: "✖", Level.WARNING: "▲", Level.INFO: "●"}
LEVEL_STYLES = {Level.CRITICAL: "error", Level.WARNING: "warning", Level.INFO: "secondary"}


def size(value: int | None) -> str:
    if value is None:
        return "—"
    amount = float(value)
    for unit in (N_("o"), N_("Ko"), N_("Mo"), N_("Go")):
        if amount < 1024 or unit == "Go":
            return f"{amount:.0f} {_(unit)}" if unit == "o" else f"{amount:.1f} {_(unit)}"
        amount /= 1024
    return f"{amount:.1f} {_('Go')}"


def alert_text(alert: Alert) -> str:
    return _(alert.text).format(**alert.params)


def publication_line(item: Publication) -> str:
    where = _("Internet (Funnel)") if item.public else _("tailnet seul (Serve)")
    url = f"{item.host}:{item.port}{item.path if item.path not in ('', '/') else ''}" if item.host else str(item.port)
    target = f" → {item.target}" if item.target else ""
    proxy = f" · PROXY v{item.proxy_protocol}" if item.proxy_protocol else ""
    return f"{url} · {where} · {_(MODE_LABELS[item.mode])}{proxy}{target}"


def service_line(service: ServiceState) -> str:
    if not service.known:
        return _("inconnu de systemd")
    state = {"active": _("actif"), "inactive": _("arrêté"), "failed": _("en échec"),
             "activating": _("démarrage"), "deactivating": _("arrêt en cours")}.get(service.active, service.active)
    enabled = {"enabled": _("lancé au démarrage"), "disabled": _("pas lancé au démarrage")}.get(
        service.enabled, service.enabled)
    return f"{state} · {enabled}"


def shield_mode_label(facts: ShieldFacts) -> str:
    return _("actif") if facts.mode is ShieldMode.ACTIVE else _("observation")


def shield_summary(facts: ShieldFacts | None) -> str:
    """Une ligne pour « Survie », le tableau de bord et le rapport."""
    if facts is None:
        return _("Bouclier du port WireGuard : état illisible.")
    if facts.removed_elsewhere:
        return _("Bouclier du port WireGuard : retiré depuis omega-fire (ou à la main).")
    if not facts.installed and not facts.present:
        return _("Bouclier du port WireGuard : aucun. Sans lui, tailscaled dépense environ un cœur pour 100 000 "
                 "paquets par seconde, même invalides.")
    if facts.missing:
        return "⚠ " + _("Bouclier du port WireGuard ABSENT : un autre outil a effacé sa table ; « Reposer » la remet.")
    if facts.stale:
        return "⚠ " + _("Bouclier du port WireGuard : état non mis à jour (service omega-bouclier-wg arrêté ?).")
    text = _("Bouclier du port WireGuard : {mode}, géré par {manager} ; {count} paquet(s) refusé(s)").format(
        mode=shield_mode_label(facts), manager=facts.manager or "?", count=facts.refused)
    if facts.mode is not ShieldMode.ACTIVE:
        text = _("Bouclier du port WireGuard : {mode}, géré par {manager} ; {count} paquet(s) auraient été "
                 "refusés").format(mode=shield_mode_label(facts), manager=facts.manager or "?", count=facts.refused)
    return text + "."
