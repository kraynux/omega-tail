# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""`omega-tail etat` : l'etat et les alertes en texte (lecture humaine) ou en JSON (scripts, minuteries)."""
from __future__ import annotations

import json
from dataclasses import asdict
from typing import Any

from omega_tail.domain.alerts import Alert
from omega_tail.domain.snapshot import Snapshot
from omega_tail.interfaces.shared.presentation import (
    LEVEL_MARKS,
    alert_text,
    publication_line,
    service_line,
    shield_summary,
    size,
)
from omega_tail.shared.i18n import _


def state_text(snapshot: Snapshot, alerts: tuple[Alert, ...], version: str) -> str:
    tailscale, machine = snapshot.tailscale, snapshot.machine
    lines = [f"OMEGA-TAIL {version} — {machine.hostname} — {snapshot.taken_at:%Y-%m-%d %H:%M:%S}", ""]
    if not tailscale.installed:
        lines.append(_("Tailscale n'est pas installé."))
    else:
        lines += [
            _("Service tailscaled : {state}").format(state=service_line(snapshot.service)),
            _("Version : {daemon} en marche, {client} installée").format(
                daemon=tailscale.daemon_version or "—", client=tailscale.client_version or "—"),
            _("Nom : {name}").format(name=tailscale.dns_name or "—"),
            _("Adresses : {addresses}").format(addresses=", ".join(tailscale.addresses) or "—"),
            _("Opérateur : {operator}").format(operator=snapshot.preferences.operator or "—"),
        ]
    cpu = machine.tailscaled_cpu_percent
    lines += [
        _("tailscaled : {cpu} d'un cœur, {memory}").format(cpu=f"{cpu:.0f} %" if cpu is not None else "—",
                                                         memory=size(machine.tailscaled_rss_bytes)),
        _("Température : {value}").format(
            value=f"{machine.temperature_c:.0f} °C" if machine.temperature_c is not None else "—"),
        shield_summary(snapshot.shield),
        "", _("PUBLICATION")]
    lines += [f"  {publication_line(item)}" for item in snapshot.publications] or [f"  {_('rien de publié')}"]
    lines += ["", _("ALERTES")]
    lines += [f"  {LEVEL_MARKS[alert.level]} {alert_text(alert)}" for alert in alerts] or [f"  {_('aucune')}"]
    return "\n".join(lines) + "\n"


def _plain(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(key): _plain(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_plain(item) for item in value]
    if hasattr(value, "isoformat"):
        return value.isoformat()
    if hasattr(value, "value") and not isinstance(value, (int, float, str, bool)):
        return value.value
    return value


def state_json(snapshot: Snapshot, alerts: tuple[Alert, ...], version: str) -> str:
    data = {"format": "omega-tail-etat", "version": version, "snapshot": _plain(asdict(snapshot)),
            "alerts": [{"level": alert.level.value, "code": alert.code, "text": alert_text(alert),
                        "target": alert.target.value} for alert in alerts]}
    return json.dumps(data, ensure_ascii=False, indent=2) + "\n"
