# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Tableau de bord (proposition §3.1) : Tailscale, machine, publication, puis les alertes ; « Corriger » ouvre
l'ecran qui corrige l'alerte choisie. Rafraichi par l'application toutes les 5 s (lectures sans droits)."""
from __future__ import annotations

from typing import TYPE_CHECKING

from rich.cells import cell_len
from rich.text import Text
from textual.app import ComposeResult
from textual.containers import Container, Horizontal, VerticalScroll
from textual.widgets import Button, Footer, Header, Static

from omega_tail.core.constants import (
    LOAD_CRITICAL_PER_CORE,
    LOAD_WARNING_PER_CORE,
    MACHINE_CPU_CRITICAL_PERCENT,
    MACHINE_CPU_WARNING_PERCENT,
    MEMORY_CRITICAL_PERCENT,
    MEMORY_WARNING_PERCENT,
    TAILSCALED_CPU_CRITICAL_PERCENT,
    TAILSCALED_CPU_WARNING_PERCENT,
    TEMPERATURE_CRITICAL_C,
    TEMPERATURE_WARNING_C,
)
from omega_tail.domain.alerts import Alert, Target
from omega_tail.domain.blacklist import BLACKLIST_MAX, BLACKLIST_WARNING
from omega_tail.domain.snapshot import Snapshot
from omega_tail.domain.tailscale import BackendState
from omega_tail.interfaces.shared.presentation import (
    BACKEND_LABELS,
    LEVEL_MARKS,
    LEVEL_STYLES,
    alert_text,
    publication_line,
    service_line,
    size,
)
from omega_tail.interfaces.tui.menu import entry
from omega_tail.interfaces.tui.screens._base import OmegaScreen
from omega_tail.interfaces.tui.widgets.status_band import StatusBand
from omega_tail.interfaces.tui.widgets.tables import WideTable
from omega_tail.shared.i18n import _

if TYPE_CHECKING:
    from omega_tail.interfaces.tui.app import OmegaTailApp


def target_label(target: Target) -> str:
    if target is Target.NONE:
        return "—"
    if target is Target.OPERATOR:
        return _("bouton « Devenir opérateur »")
    item = entry(target.value)
    if item is None:
        return "—"
    return _(item.label) + (f" ({_('lot {lot}').format(lot=item.planned)})" if item.planned else "")


Line = tuple[str, str, str]
"""(libelle, valeur, niveau) ; niveau : ok, warn, bad, off ou vide (valeur neutre)."""
LEVEL_VARIABLES = {"ok": "success", "warn": "warning", "bad": "error"}


def _yes_no(flag: bool) -> str:
    return _("oui") if flag else _("non")


def tailscale_lines(snapshot: Snapshot) -> list[Line]:
    tailscale = snapshot.tailscale
    if not tailscale.installed:
        return [(_("Tailscale"), _("n'est pas installé"), "bad")]
    service = snapshot.service
    lines: list[Line] = [(_("Service"), service_line(service),
                          "" if not service.known else "ok" if service.running else "bad")]
    if not tailscale.reachable:
        lines.append((_("tailscaled"), _("ne répond pas : {error}").format(error=tailscale.error or "—"), "bad"))
        lines.append((_("Client installé"), tailscale.client_version or "—", ""))
        return lines
    running = tailscale.backend is BackendState.RUNNING
    versions = tailscale.daemon_version if not tailscale.versions_differ else _(
        "{daemon} en marche, {client} installé").format(daemon=tailscale.daemon_version,
                                                       client=tailscale.client_version)
    values = snapshot.preferences.values
    exit_used = values.get("exit-node", "")
    routes = values.get("advertise-routes", "").strip()
    lines += [
        (_("État"), _(BACKEND_LABELS[tailscale.backend]), "ok" if running else "warn"),
        (_("Version"), versions, "warn" if tailscale.versions_differ else ""),
        (_("Nom"), tailscale.dns_name or tailscale.host_name or "—", ""),
        (_("Adresses"), ", ".join(tailscale.addresses) or "—", ""),
        (_("Compte"), tailscale.user or "—", ""),
        (_("Appareils du tailnet"), _("{online} en ligne sur {total}").format(online=tailscale.peers_online,
                                                                             total=tailscale.peers_total), ""),
        (_("Clé de la machine"), tailscale.key_expiry.strftime("%Y-%m-%d") if tailscale.key_expiry
         else _("sans expiration"), ""),
        (_("Opérateur"), snapshot.preferences.operator or _("aucun (sudo requis)"),
         "ok" if snapshot.is_operator else "warn"),
        (_("Nœud de sortie proposé"), _yes_no(values.get("advertise-exit-node") == "true"), ""),
        (_("Nœud de sortie utilisé"), exit_used or _("aucun"), ""),
        (_("Sous-réseaux annoncés"), routes or _("aucun"), ""),
    ]
    return lines


def machine_lines(snapshot: Snapshot) -> list[Line]:
    machine = snapshot.machine
    cpu, per_core = machine.tailscaled_cpu_percent, machine.load_per_core
    lines: list[Line] = [
        (_("Machine"), _("{name} ({count} fils)").format(name=machine.hostname or "—", count=machine.cpu_count), ""),
        (_("CPU machine"), f"{machine.cpu_percent:.0f} %" if machine.cpu_percent is not None else "…",
         _level(machine.cpu_percent, MACHINE_CPU_WARNING_PERCENT, MACHINE_CPU_CRITICAL_PERCENT)),
        (_("Charge"), f"{machine.load[0]:.2f} {machine.load[1]:.2f} {machine.load[2]:.2f}",
         _level(per_core, LOAD_WARNING_PER_CORE, LOAD_CRITICAL_PER_CORE)),
        (_("Température"), f"{machine.temperature_c:.0f} °C" if machine.temperature_c is not None
         else _("pas de capteur"), _level(machine.temperature_c, TEMPERATURE_WARNING_C, TEMPERATURE_CRITICAL_C)),
        (_("Mémoire"), _("{used} utilisés sur {total}").format(
            used=f"{machine.memory_used_percent:.0f} %" if machine.memory_used_percent is not None else "—",
            total=size(machine.memory_total_bytes)),
         _level(machine.memory_used_percent, MEMORY_WARNING_PERCENT, MEMORY_CRITICAL_PERCENT)),
        (_("CPU tailscaled"), _("{cpu} d'un cœur, {memory}").format(
            cpu=f"{cpu:.0f} %" if cpu is not None else "…", memory=size(machine.tailscaled_rss_bytes)),
         _level(cpu, TAILSCALED_CPU_WARNING_PERCENT, TAILSCALED_CPU_CRITICAL_PERCENT)),
        (_("Confinement"), _yes_no(snapshot.service.confined) if snapshot.service.known else "—",
         "ok" if snapshot.service.confined else ""),
    ]
    return lines + protection_lines(snapshot)


def protection_lines(snapshot: Snapshot) -> list[Line]:
    """Ce que dit la barre d'etat, en detail : Funnel, porte, veille, bouclier, disjoncteur, liste noire."""
    lines: list[Line] = []
    funnel = snapshot.funnel
    if snapshot.cut is not None:
        lines.append((_("Funnel"), _("coupé par le disjoncteur"), "warn"))
    elif funnel:
        exposed = any(item.exposed for item in funnel)
        lines.append((_("Funnel"), _("ouvert sur {ports}").format(ports=", ".join(str(item.port) for item in funnel))
                      + (f" {_('sans porte')}" if exposed else ""), "warn" if exposed else "ok"))
    else:
        lines.append((_("Funnel"), _("fermé"), "ok"))
    gate = snapshot.gate_service
    if snapshot.gated:
        running = gate is None or not gate.known or gate.running
        value = (_("actif · MODE ATTAQUE") if snapshot.gate_attack else _("actif")) if running else _("arrêté")
        lines.append((_("Pare-feu (porte)"), value, ("warn" if snapshot.gate_attack else "ok") if running else "bad"))
    else:
        lines.append((_("Pare-feu (porte)"), _("inactif"), "warn" if funnel and snapshot.cut is None else "off"))
    lines.append((_("Liste noire"), _("{count} entrée(s)").format(count=snapshot.blacklist_count),
                  _level(float(snapshot.blacklist_count), BLACKLIST_WARNING, BLACKLIST_MAX)))
    watch = snapshot.watch
    if watch is not None:
        if not watch.installed:
            lines.append((_("Veille"), _("inactive"), "off"))
        elif not watch.alive:
            lines.append((_("Veille"), _("arrêtée"), "bad"))
        else:
            lines.append((_("Veille"), _("active, palier {level}").format(level=watch.level),
                          "warn" if watch.level else "ok"))
    shield = snapshot.shield
    if shield is not None:
        if not shield.installed:
            lines.append((_("Bouclier WireGuard"), _("non posé"), "off"))
        elif shield.missing:
            lines.append((_("Bouclier WireGuard"), _("ABSENT (table effacée)"), "bad"))
        elif shield.stale:
            lines.append((_("Bouclier WireGuard"), _("état non mis à jour"), "warn"))
        else:
            mode = shield.status.mode.value if shield.status is not None and shield.status.mode is not None else "—"
            lines.append((_("Bouclier WireGuard"), _("posé, mode {mode}").format(mode=_(mode)), "ok"))
    return lines


def _level(value: float | None, warning: float, critical: float) -> str:
    if value is None:
        return ""
    return "bad" if value >= critical else "warn" if value >= warning else "ok"


def _color(styles: dict[str, str], name: str) -> str:
    """Couleur du theme utilisable par Rich (les variables du type « auto 60% » ne le sont pas)."""
    value = styles.get(name, "")
    return value if value.startswith("#") else ""


def styled(lines: list[Line], styles: dict[str, str]) -> Text:
    """Libelles dans la couleur d'accent du theme, valeurs en couleur de niveau (vert, orange, rouge) ou neutres."""
    width = max((cell_len(label) for label, _value, _level in lines), default=0)
    text = Text()
    for index, (label, value, level) in enumerate(lines):
        if index:
            text.append("\n")
        # largeur a l'ecran, pas en caracteres : japonais, chinois, coreen, thai, hindi (captures 2026-11-25)
        text.append(label + " " * (width - cell_len(label) + 2), style=_color(styles, "accent"))
        if level == "off":
            text.append(value, style="dim")
        else:
            variable = LEVEL_VARIABLES.get(level, "")
            text.append(value, style=f"bold {_color(styles, variable)}".strip() if variable else "")
    return text


def publication_text(snapshot: Snapshot) -> str:
    if not snapshot.publications:
        return _("Rien n'est publié (ni Serve, ni Funnel).")
    return "\n".join(publication_line(item) for item in snapshot.publications)


class DashboardScreen(OmegaScreen):
    def compose(self) -> ComposeResult:
        app: OmegaTailApp = self.app  # type: ignore[assignment]
        yield Header()
        yield StatusBand(app.snapshot)
        with VerticalScroll(classes="omega-panel"):
            yield Static(_("TABLEAU DE BORD"), classes="omega-title")
            yield Static("", id="taken-at", classes="omega-hint")
            yield Static(_("ALERTES"), classes="omega-subtitle")
            yield WideTable(id="alerts-table", cursor_type="row", zebra_stripes=True)
            yield Static("", id="alerts-hint", classes="omega-hint")
            with Horizontal(classes="tail-row"):
                yield Static("", id="tailscale-box", classes="tail-box", markup=False)
                yield Static("", id="machine-box", classes="tail-box", markup=False)
            yield Static("", id="publication-box", classes="tail-box", markup=False)
        with Horizontal(classes="omega-actions omega-fixed-actions"):
            with Container(classes="omega-btn-frame"):
                yield Button(_("Corriger"), id="fix", variant="primary")
            with Container(classes="omega-btn-frame"):
                yield Button(_("Devenir opérateur"), id="operator")
            with Container(classes="omega-btn-frame"):
                yield Button(_("Rafraîchir"), id="refresh")
            with Container(classes="omega-btn-frame"):
                yield Button(_("Retour"), id="back")
        yield Footer()

    def on_mount(self) -> None:
        self.query_one("#tailscale-box").border_title = "TAILSCALE"
        self.query_one("#machine-box").border_title = _("MACHINE")
        self.query_one("#publication-box").border_title = _("PUBLICATION")
        table = self.query_one("#alerts-table", WideTable)
        table.add_columns("", _("Où corriger"), _("Alerte"))
        snapshot = getattr(self.app, "snapshot", None)
        if snapshot is not None:
            self.show_snapshot(snapshot)

    def _alerts(self) -> tuple[Alert, ...]:
        return tuple(getattr(self.app, "alerts", ()))

    def show_snapshot(self, snapshot: Snapshot) -> None:
        self.query_one(StatusBand).show(snapshot)
        self.query_one("#taken-at", Static).update(_("Lu à {time} · relu toutes les 5 s").format(
            time=snapshot.taken_at.strftime("%H:%M:%S")))
        styles = self.app.get_css_variables()
        self.query_one("#tailscale-box", Static).update(styled(tailscale_lines(snapshot), styles))
        self.query_one("#machine-box", Static).update(styled(machine_lines(snapshot), styles))
        self.query_one("#publication-box", Static).update(publication_text(snapshot))
        # le cadre du bouton avec lui : sinon un petit cadre vide reste dans la barre (retour d'utilisation 2026-11-23)
        self.query_one("#operator", Button).parent.display = (  # type: ignore[union-attr]
            not snapshot.is_operator and snapshot.tailscale.reachable)
        table = self.query_one("#alerts-table", WideTable)
        row = table.cursor_row
        table.clear()
        alerts = self._alerts()
        for alert in alerts:
            style = styles.get(LEVEL_STYLES[alert.level], "")
            table.add_row(Text(LEVEL_MARKS[alert.level], style=f"bold {style}"), Text(target_label(alert.target)),
                          Text(alert_text(alert)))
        if alerts:
            table.move_cursor(row=min(row, len(alerts) - 1))
        self.query_one("#alerts-hint", Static).update(
            _("Aucune alerte.") if not alerts else _("Choisissez une alerte puis « Corriger » (ou Entrée)."))

    def on_data_table_row_selected(self) -> None:
        self._fix()

    def _fix(self) -> None:
        alerts = self._alerts()
        table = self.query_one("#alerts-table", WideTable)
        if not alerts or not 0 <= table.cursor_row < len(alerts):
            self.app.notify(_("Aucune alerte choisie."))
            return
        app: OmegaTailApp = self.app  # type: ignore[assignment]
        target = alerts[table.cursor_row].target
        if target is Target.OPERATOR:
            app.become_operator()
        elif target is Target.NONE:
            self.app.notify(_("Rien à ouvrir pour cette alerte : elle vient de Tailscale lui-même."))
        else:
            app.open_key(target.value)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        app: OmegaTailApp = self.app  # type: ignore[assignment]
        if event.button.id == "fix":
            self._fix()
        elif event.button.id == "operator":
            app.become_operator()
        elif event.button.id == "refresh":
            app.request_refresh()
        elif event.button.id == "back":
            self.action_back()
