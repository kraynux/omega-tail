# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Reseau et appareils (lot 7, proposition §3.5) : appareils du tailnet (filtre, ping Tailscale, whois), diagnostic
reseau (netcheck, a la demande : quelques secondes), DNS, verrou du tailnet et compteurs internes. Lecture seule,
sans droits ; aucun reglage de Tailscale n'est change ici. Taildrop et partages : plus tard (decision A, lot 7)."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import TYPE_CHECKING

from rich.text import Text
from textual.app import ComposeResult
from textual.containers import Container, Horizontal, VerticalScroll
from textual.widgets import Button, Checkbox, DataTable, Footer, Header, Input, Static

from omega_tail.application.network import DeviceList
from omega_tail.domain.network import Device, Metrics, Netcheck, matches, sort_devices
from omega_tail.domain.snapshot import Snapshot
from omega_tail.interfaces.shared.messages import localized
from omega_tail.interfaces.shared.presentation import size
from omega_tail.interfaces.tui.screens._base import OmegaScreen
from omega_tail.interfaces.tui.widgets.status_band import StatusBand
from omega_tail.interfaces.tui.widgets.tables import WideTable
from omega_tail.shared.i18n import _

if TYPE_CHECKING:
    from omega_tail.interfaces.tui.app import OmegaTailApp

LATENCIES_SHOWN = 5


def seen_text(device: Device, now: datetime) -> str:
    """« maintenant » (en ligne), « il y a 3 h », « il y a 2 j » ; « — » si Tailscale ne le dit pas."""
    if device.online:
        return _("maintenant")
    if device.last_seen is None:
        return "—"
    seconds = max(0, int((now - device.last_seen).total_seconds()))
    if seconds < 3600:
        return _("il y a {count} min").format(count=max(1, seconds // 60))
    if seconds < 86400:
        return _("il y a {count} h").format(count=seconds // 3600)
    return _("il y a {count} j").format(count=seconds // 86400)


def path_text(device: Device) -> str:
    if device.path == "direct":
        return _("direct")
    if device.path == "relais":
        return _("relais {code}").format(code=device.relay) if device.relay else _("relais")
    return "—"


def state_text(device: Device) -> str:
    state = _("en ligne") if device.online else _("hors ligne")
    if device.exit_node:
        state += " · " + _("sortie Internet")
    return state


def netcheck_text(report: Netcheck) -> str:
    if report.error:
        return _("Diagnostic impossible : {error}").format(error=localized(report.error))
    if report.udp is None and not report.latencies:
        return report.raw.strip() or _("Tailscale n'a rien répondu.")

    def yes_no(value: str) -> str:
        head, _sep, address = value.partition(",")
        if head.strip().lower() in ("yes", "true"):
            return _("oui, adresse publique {address}").format(address=address.strip()) if address.strip() \
                else _("oui")
        return _("non") if head.strip() else "—"

    lines = [_("UDP : {value}").format(value=_("oui") if report.udp else _(
                 "non — tout passe par les relais de Tailscale (plus lent)") if report.udp is False else "—"),
             _("IPv4 : {value}").format(value=yes_no(report.ipv4)),
             _("IPv6 : {value}").format(value=yes_no(report.ipv6))]
    if report.varies is not None:
        lines.append(_("NAT : {value}").format(value=_(
            "difficile — le port change selon la destination, les relais seront plus fréquents") if report.varies
            else _("simple — les connexions directes se font facilement")))
    lines.append(_("Ouverture de port par la box : {value}").format(value=report.port_mapping or _("aucune")))
    lines.append(_("Relais le plus proche : {value}").format(value=report.nearest or "—"))
    measured = [item for item in report.latencies if item.milliseconds is not None][:LATENCIES_SHOWN]
    if measured:
        lines.append(_("Latence des relais : {values}").format(values=", ".join(
            f"{item.city or item.code} {item.milliseconds:.0f} ms" for item in measured)))
    return "\n".join(lines)


def _paths(values: dict[str, float]) -> dict[str, float]:
    grouped = {"direct": 0.0, "derp": 0.0, "peer": 0.0}
    for path, amount in values.items():
        key = "direct" if path.startswith("direct") else "peer" if path.startswith("peer_relay") else \
            "derp" if path == "derp" else ""
        if key:
            grouped[key] += amount
    return grouped


def metrics_text(metrics: Metrics) -> str:
    if not metrics.values:
        return _("Compteurs internes illisibles (Tailscale trop ancien ?).")
    lines = []
    for title, name in ((_("Reçu"), "tailscaled_inbound_bytes_total"),
                        (_("Envoyé"), "tailscaled_outbound_bytes_total")):
        paths = _paths(metrics.by_label(name, "path"))
        lines.append(_("{title} depuis le démarrage : direct {direct} · relais DERP {derp} · relais d'un pair "
                       "{peer}").format(title=title, direct=size(int(paths["direct"])), derp=size(int(paths["derp"])),
                                        peer=size(int(paths["peer"]))))
    dropped = metrics.by_label("tailscaled_outbound_dropped_packets_total", "reason")
    lines.append(_("Paquets jetés en sortie : {count}").format(count=int(sum(dropped.values()))) + (
        " (" + ", ".join(f"{reason} {int(count)}" for reason, count in sorted(dropped.items())) + ")"
        if dropped else ""))
    lines.append(_("Messages de santé : {count}").format(
        count=int(metrics.total("tailscaled_health_messages"))))
    return "\n".join(lines)


class NetworkScreen(OmegaScreen):
    def __init__(self) -> None:
        super().__init__()
        self._devices: tuple[Device, ...] = ()
        self._shown: list[Device] = []

    def compose(self) -> ComposeResult:
        app: OmegaTailApp = self.app  # type: ignore[assignment]
        yield Header()
        yield StatusBand(app.snapshot)
        with VerticalScroll(classes="omega-panel"):
            yield Static(_("RÉSEAU ET APPAREILS"), classes="omega-title")
            yield Static(_("Ce que voit Tailscale depuis cette machine : les appareils du tailnet, le chemin vers "
                           "chacun (direct ou par un relais), et l'état du réseau. Lecture seule : rien n'est changé "
                           "ici."), classes="omega-hint")
            yield Static(_("APPAREILS"), classes="omega-subtitle")
            with Horizontal(classes="omega-actions"):
                yield Input(placeholder=_("filtrer : nom, système, adresse"), id="device-filter")
                yield Checkbox(_("Relais Funnel de Tailscale"), value=False, id="show-ingress")
            table = WideTable(id="devices-table", cursor_type="row", zebra_stripes=True)
            table.add_columns(_("Nom"), _("Système"), _("État"), _("Chemin"), _("Vu"), _("Adresse"), _("Reçu"),
                              _("Envoyé"))
            yield table
            yield Static("", id="devices-note", classes="omega-hint", markup=False)
            with Horizontal(classes="omega-actions"):
                yield Input(placeholder=_("nom ou adresse (vide : la ligne choisie)"), id="target")
                with Container(classes="omega-btn-frame"):
                    yield Button(_("Ping Tailscale"), id="ping", variant="primary")
                with Container(classes="omega-btn-frame"):
                    yield Button(_("Qui est-ce ?"), id="whois")
            yield Static("", id="probe-result", classes="tail-box", markup=False)

            yield Static(_("DIAGNOSTIC RÉSEAU"), classes="omega-subtitle tail-gap")
            yield Static(_("UDP, IPv4 / IPv6, type de NAT, ouverture de port par la box, relais le plus proche : ce "
                           "qui décide si les connexions sont directes. Prend quelques secondes."),
                         classes="omega-hint")
            with Horizontal(classes="omega-actions"), Container(classes="omega-btn-frame"):
                yield Button(_("Lancer le diagnostic"), id="netcheck", variant="primary")
            yield Static("", id="netcheck-box", classes="tail-box", markup=False)
            with Horizontal(classes="tail-row"):
                yield Static("", id="dns-box", classes="tail-box", markup=False)
                yield Static("", id="lock-box", classes="tail-box", markup=False)
            yield Static("", id="metrics-box", classes="tail-box", markup=False)
        with Horizontal(classes="omega-actions omega-fixed-actions"):
            with Container(classes="omega-btn-frame"):
                yield Button(_("Rafraîchir"), id="refresh")
            with Container(classes="omega-btn-frame"):
                yield Button(_("Retour"), id="back")
        yield Footer()

    def on_mount(self) -> None:
        self.query_one("#probe-result").display = False
        self.query_one("#netcheck-box").display = False
        self.query_one("#netcheck-box").border_title = _("DIAGNOSTIC")
        self.query_one("#dns-box").border_title = "DNS"
        self.query_one("#lock-box").border_title = _("VERROU DU TAILNET")
        self.query_one("#metrics-box").border_title = _("COMPTEURS INTERNES")
        self.reload()

    def show_snapshot(self, snapshot: Snapshot) -> None:
        self.query_one(StatusBand).show(snapshot)

    # ---- lectures ----
    def reload(self) -> None:
        app: OmegaTailApp = self.app  # type: ignore[assignment]
        tools = app.network
        if tools is None:
            return

        def work() -> None:
            devices = tools.devices()
            dns, lock, metrics = tools.dns(), tools.lock(), tools.metrics()
            self.app.call_from_thread(self._show, devices, dns, lock, metrics)

        self.run_worker(work, thread=True, group="network", exclusive=True)

    def _show(self, devices: DeviceList, dns: tuple[str, str], lock: tuple[str, str], metrics: Metrics) -> None:
        self._devices = devices.devices
        self._fill(error=devices.error)
        self.query_one("#dns-box", Static).update(dns[0] or _("Illisible : {error}").format(error=dns[1]))
        self.query_one("#lock-box", Static).update(lock[0] or _("Illisible : {error}").format(error=lock[1]))
        self.query_one("#metrics-box", Static).update(metrics_text(metrics))

    def _fill(self, error: str = "") -> None:
        table = self.query_one("#devices-table", WideTable)
        cursor = table.cursor_row
        table.clear()
        text = self.query_one("#device-filter", Input).value
        ingress = self.query_one("#show-ingress", Checkbox).value
        now = datetime.now(timezone.utc)
        self._shown = [device for device in sort_devices(list(self._devices))
                       if (ingress or not device.ingress) and matches(device, text)]
        for device in self._shown:
            table.add_row(Text(device.name), Text(device.os or "—"), state_text(device), path_text(device),
                          seen_text(device, now), Text(device.address or "—"), size(device.rx_bytes),
                          size(device.tx_bytes))
        if self._shown:
            table.move_cursor(row=min(cursor, len(self._shown) - 1))
        mine = [device for device in self._devices if not device.ingress]
        relays = len(self._devices) - len(mine)
        note = _("{online} en ligne sur {total} appareil(s) ; {relays} relais Funnel de Tailscale (cochez pour les "
                 "voir).").format(online=sum(1 for device in mine if device.online), total=len(mine), relays=relays)
        if error:
            note = _("Appareils illisibles : {error}").format(error=error)
        self.query_one("#devices-note", Static).update(note)

    def on_input_changed(self, event: Input.Changed) -> None:
        if event.input.id == "device-filter":
            self._fill()

    def on_checkbox_changed(self, _event: Checkbox.Changed) -> None:
        self._fill()

    def _target(self) -> str:
        typed = self.query_one("#target", Input).value.strip()
        if typed:
            return typed
        table = self.query_one("#devices-table", WideTable)
        if self._shown and 0 <= table.cursor_row < len(self._shown):
            device = self._shown[table.cursor_row]
            return device.address or device.dns_name
        return ""

    def _probe(self, kind: str) -> None:
        app: OmegaTailApp = self.app  # type: ignore[assignment]
        tools, target = app.network, self._target()
        if tools is None:
            return
        if not target:
            self.app.notify(_("Choisissez un appareil, ou tapez un nom ou une adresse."))
            return
        box = self.query_one("#probe-result", Static)
        box.display = True
        box.border_title = (_("PING {target}") if kind == "ping" else _("QUI EST-CE ? {target}")).format(
            target=target)
        box.update(_("Ping en cours (3 essais au plus)…") if kind == "ping" else _("Lecture…"))

        def work() -> None:
            accepted, text = tools.ping(target) if kind == "ping" else tools.whois(target)
            if not accepted:
                text = _("« {target} » n'est pas un nom ou une adresse valable.").format(target=target)
            self.app.call_from_thread(box.update, text or _("Tailscale n'a rien répondu."))

        self.run_worker(work, thread=True, group="network-probe", exclusive=True)

    def _netcheck(self) -> None:
        app: OmegaTailApp = self.app  # type: ignore[assignment]
        tools = app.network
        if tools is None:
            return
        box = self.query_one("#netcheck-box", Static)
        box.display = True
        box.update(_("Diagnostic en cours (quelques secondes)…"))
        self.query_one("#netcheck", Button).disabled = True

        def work() -> None:
            text = netcheck_text(tools.netcheck())
            self.app.call_from_thread(self._netcheck_done, text)

        self.run_worker(work, thread=True, group="network-netcheck", exclusive=True)

    def _netcheck_done(self, text: str) -> None:
        self.query_one("#netcheck-box", Static).update(text)
        self.query_one("#netcheck", Button).disabled = False

    def on_data_table_row_selected(self, _event: DataTable.RowSelected) -> None:
        self._probe("ping")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        button = event.button.id
        if button in ("ping", "whois"):
            self._probe(button)
        elif button == "netcheck":
            self._netcheck()
        elif button == "refresh":
            self.reload()
        elif button == "back":
            self.action_back()
