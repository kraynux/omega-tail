# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Bande d'etat (une ligne, sous l'en-tete de chaque ecran), par ordre d'importance (un terminal etroit coupe la
fin) : service tailscaled, CPU de la machine, CPU de tailscaled, temperature, memoire, Funnel, pare-feu (porte),
veille automatique, connexion. Vert / orange / rouge selon le theme actif ; attenue : desactive par choix."""
from __future__ import annotations

from rich.cells import cell_len
from textual.content import Content, Span
from textual.widgets import Static

from omega_tail.core.constants import (
    MACHINE_CPU_CRITICAL_PERCENT,
    MACHINE_CPU_WARNING_PERCENT,
    MEMORY_CRITICAL_PERCENT,
    MEMORY_WARNING_PERCENT,
    TAILSCALED_CPU_CRITICAL_PERCENT,
    TAILSCALED_CPU_WARNING_PERCENT,
    TEMPERATURE_CRITICAL_C,
    TEMPERATURE_WARNING_C,
)
from omega_tail.domain.machine import MachineState
from omega_tail.domain.snapshot import Snapshot
from omega_tail.domain.tailscale import BackendState
from omega_tail.interfaces.shared.presentation import BACKEND_LABELS
from omega_tail.shared.i18n import _

OK, WARN, BAD, OFF = "$success", "$warning", "$error", "$text-muted"


def level(value: float, warning: float, critical: float) -> str:
    return BAD if value >= critical else WARN if value >= warning else OK


def machine_cpu_color(machine: MachineState) -> str:
    return level(machine.cpu_percent or 0.0, MACHINE_CPU_WARNING_PERCENT, MACHINE_CPU_CRITICAL_PERCENT)


def tailscaled_cpu_color(cpu: float) -> str:
    return level(cpu, TAILSCALED_CPU_WARNING_PERCENT, TAILSCALED_CPU_CRITICAL_PERCENT)


def band_parts(snapshot: Snapshot) -> list[tuple[str, str]]:
    """(texte, couleur) ; la couleur s'applique au voyant « ● » qui precede le texte."""
    tailscale, service, machine = snapshot.tailscale, snapshot.service, snapshot.machine
    if not tailscale.installed:
        return [(_("Tailscale absent"), BAD)]
    parts: list[tuple[str, str]] = []
    if service.known:
        running = service.running
        version = f" {tailscale.daemon_version}" if tailscale.daemon_version else ""
        parts.append((f"tailscaled {_('actif') if running else _('arrêté')}{version}",
                      (WARN if tailscale.versions_differ else OK) if running else BAD))
    if machine.cpu_percent is not None:
        parts.append((_("CPU machine {cpu:.0f} %").format(cpu=machine.cpu_percent), machine_cpu_color(machine)))
    cpu = machine.tailscaled_cpu_percent
    if cpu is not None:
        parts.append((_("CPU tailscaled {cpu:.0f} %").format(cpu=cpu), tailscaled_cpu_color(cpu)))
    if machine.temperature_c is not None:
        temperature = machine.temperature_c
        parts.append((f"{temperature:.0f} °C", BAD if temperature >= TEMPERATURE_CRITICAL_C
                      else WARN if temperature >= TEMPERATURE_WARNING_C else OK))
    used = machine.memory_used_percent
    if used is not None:
        parts.append((_("RAM {used:.0f} %").format(used=used), BAD if used >= MEMORY_CRITICAL_PERCENT
                      else WARN if used >= MEMORY_WARNING_PERCENT else OK))
    funnel = snapshot.funnel
    if snapshot.cut is not None:
        parts.append((_("Funnel coupé"), WARN))
    elif funnel:
        ports = ", ".join(str(item.port) for item in funnel)
        exposed = any(item.exposed for item in funnel)
        parts.append((f"Funnel {ports}" + (f" {_('sans porte')}" if exposed else ""), WARN if exposed else OK))
    else:
        parts.append((_("Funnel fermé"), OK))
    gate = snapshot.gate_service
    if snapshot.gated:
        running = gate is None or not gate.known or gate.running
        if running and snapshot.gate_attack:
            parts.append((_("Pare-feu actif · attaque"), WARN))
        else:
            parts.append((_("Pare-feu actif") if running else _("Pare-feu arrêté"), OK if running else BAD))
    else:
        parts.append((_("Pare-feu inactif"), WARN if funnel and snapshot.cut is None else OFF))
    watch = snapshot.watch
    if watch is not None:
        if watch.installed:
            parts.append((_("Veille active") if watch.alive else _("Veille arrêtée"), OK if watch.alive else BAD))
        else:
            parts.append((_("Veille inactive"), OFF))
    backend = tailscale.backend
    parts.append((_(BACKEND_LABELS[backend]) if tailscale.reachable else _("Tailscale injoignable"),
                  OK if backend is BackendState.RUNNING else BAD if not tailscale.reachable else WARN))
    return parts


def band_content(snapshot: Snapshot | None, width: int = 0) -> Content:
    """Une ligne ; si `width` est donnee et trop courte, retour a la ligne ENTRE deux voyants (jamais au milieu)."""
    if snapshot is None:
        return Content(_("Lecture de l'état…"))
    text, spans, line = "", [], 0
    for index, (label, color) in enumerate(band_parts(snapshot)):
        item = f"● {label}"
        if index:
            if width and line + 3 + cell_len(item) > width:
                text += "\n"
                line = 0
            else:
                text += " │ "
                line += 3
        spans.append(Span(len(text), len(text) + 1, color))
        text += item
        line += cell_len(item)
    return Content(text, spans)


class StatusBand(Static):
    def __init__(self, snapshot: Snapshot | None = None) -> None:
        super().__init__(band_content(snapshot), classes="omega-status-band")
        self.border_title = _("État")
        self._snapshot = snapshot

    def show(self, snapshot: Snapshot) -> None:
        self._snapshot = snapshot
        self.update(band_content(snapshot, self.content_size.width))

    def on_resize(self) -> None:
        self.update(band_content(self._snapshot, self.content_size.width))
