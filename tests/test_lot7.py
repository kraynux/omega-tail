# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Lot 7 : Reseau et appareils, Rapport, Voir les exports. Sorties de Tailscale relevees sur la machine de dev
(1.102.5, 2026-11-23) ; jamais le vrai Tailscale ni le vrai journal."""
from __future__ import annotations

import json
from datetime import date, datetime, timezone
from pathlib import Path

from conftest import FUNNEL_HTTPS, NOW, FakeJournal, FakeTailscale, tools
from omega_lib.terminal.models import RenderProfile
from textual.widgets import Button, Checkbox, Input, Static

from omega_tail.application.actions import ActionTools
from omega_tail.application.network import NetworkTools
from omega_tail.application.report import ReportTools
from omega_tail.application.settings import SettingsTools
from omega_tail.domain.breaker import BreakerPolicy
from omega_tail.domain.network import Device, Metrics, Netcheck, matches, parse_metrics, parse_netcheck, valid_target
from omega_tail.domain.report import parse_line, summarize
from omega_tail.infrastructure.exports.writer import FileExportWriter
from omega_tail.infrastructure.settings.directories import clear_directory
from omega_tail.infrastructure.settings.json_store import JsonSettingsStore
from omega_tail.infrastructure.system.journal import FileJournal
from omega_tail.infrastructure.tailscale.parsing import parse_devices
from omega_tail.interfaces.cli.main import main_with
from omega_tail.interfaces.shared.report_view import render_html, render_json, render_text
from omega_tail.interfaces.tui.app import OmegaTailApp

NETCHECK = """
Report:
\t* Time: 2026-11-23 19:31:46.000567144+01:00
\t* UDP: true
\t* IPv4: yes, 37.67.116.15:50711
\t* IPv6: no, but OS has support
\t* MappingVariesByDestIP: false
\t* PortMapping: UPnP
\t* Nearest DERP: Paris
\t* DERP latency:
\t\t- par: 17.6ms  (Paris)
\t\t- lhr: 17.7ms  (London)
\t\t- waw: 37ms    (Warsaw)
\t\t- syd:         (Sydney)
"""
METRICS = """# TYPE tailscaled_inbound_bytes_total counter
tailscaled_health_messages{type="warning"} 2
tailscaled_inbound_bytes_total{path="derp"} 1024
tailscaled_inbound_bytes_total{path="direct_ipv4"} 2048
tailscaled_inbound_bytes_total{path="direct_ipv6"} 2048
tailscaled_outbound_bytes_total{path="peer_relay_ipv4"} 10
tailscaled_outbound_dropped_packets_total{reason="error"} 1
tailscaled_outbound_dropped_packets_total{reason="unknown_protocol"} 6
"""
STATUS = {"Peer": {
    "a": {"HostName": "funnel-ingress-node", "OS": "", "Online": True, "Tags": ["tag:ingress"],
          "TailscaleIPs": ["fd7a:115c:a1e0::a801:26ab"], "LastSeen": "0001-01-01T00:00:00Z"},
    "b": {"HostName": "serveur-web", "DNSName": "serveur-web.tailnet-exemple.ts.net.", "OS": "linux", "Online": True,
          "Active": True, "CurAddr": "192.168.1.103:41641", "Relay": "par",
          "TailscaleIPs": ["100.64.12.34", "fd7a:115c:a1e0::1"], "RxBytes": 2048, "TxBytes": 10},
    "c": {"HostName": "Telephone Android", "DNSName": "telephone.tailnet-exemple.ts.net.", "OS": "android",
          "Online": False, "Relay": "par", "TailscaleIPs": ["100.64.24.15"], "LastSeen": "2026-11-21T15:22:33.1Z",
          "Tags": None},
    "d": {"HostName": "<script>alert(1)</script>", "OS": "linux", "Online": True, "Active": True, "Relay": "fra",
          "TailscaleIPs": ["100.64.0.9"]}}}


# ---- reseau ----
def test_netcheck_is_read_from_its_text_report() -> None:
    from omega_tail.interfaces.tui.screens.network import netcheck_text

    found = parse_netcheck(NETCHECK)
    assert found.udp is True and found.varies is False and found.port_mapping == "UPnP" and found.nearest == "Paris"
    assert [(item.code, item.milliseconds) for item in found.latencies] == [("par", 17.6), ("lhr", 17.7),
                                                                             ("waw", 37.0), ("syd", None)]
    text = netcheck_text(found)
    assert "UDP : oui" in text and "adresse publique 37.67.116.15:50711" in text and "IPv6 : non" in text
    assert "NAT : simple" in text and "Paris 18 ms" in text and "Sydney" not in text
    assert "Diagnostic impossible : boom" in netcheck_text(Netcheck(error="boom"))
    assert netcheck_text(parse_netcheck("autre chose")) == "autre chose"  # format inconnu : tel quel


def test_metrics_summary_groups_paths() -> None:
    from omega_tail.interfaces.tui.screens.network import metrics_text

    metrics = parse_metrics(METRICS)
    assert metrics.total("tailscaled_inbound_bytes_total") == 5120
    assert metrics.by_label("tailscaled_outbound_dropped_packets_total", "reason") == {"error": 1,
                                                                                      "unknown_protocol": 6}
    text = metrics_text(metrics)
    assert "Reçu depuis le démarrage : direct 4.0 Ko · relais DERP 1.0 Ko · relais d'un pair 0 o" in text
    assert "Paquets jetés en sortie : 7 (error 1, unknown_protocol 6)" in text and "Messages de santé : 2" in text
    assert "illisibles" in metrics_text(Metrics())


def test_devices_paths_filters_and_funnel_relays() -> None:
    from omega_tail.interfaces.tui.screens.network import path_text, seen_text

    devices = {device.name: device for device in parse_devices(STATUS)}
    assert devices["funnel-ingress-node"].ingress and not devices["serveur-web"].ingress
    server, phone = devices["serveur-web"], devices["Telephone Android"]
    assert server.path == "direct" and server.address == "100.64.12.34" and path_text(server) == "direct"
    assert phone.path == "" and path_text(phone) == "—" and phone.dns_name == "telephone.tailnet-exemple.ts.net"
    assert path_text(devices["<script>alert(1)</script>"]) == "relais fra"
    assert seen_text(phone, datetime(2026, 11, 23, 15, 22, 34, tzinfo=timezone.utc)) == "il y a 2 j"
    assert seen_text(phone, datetime(2026, 11, 21, 18, 0, tzinfo=timezone.utc)) == "il y a 2 h"
    assert seen_text(server, NOW) == "maintenant"
    assert matches(phone, "ANDROID") and matches(phone, "100.64.24") and not matches(phone, "linux")
    assert devices["funnel-ingress-node"].last_seen is None


def test_ping_and_whois_targets_are_checked() -> None:
    assert valid_target("serveur-web") and valid_target("100.64.12.34") and valid_target("fd7a:115c:a1e0::1")
    for bad in ("-c", "--help", "a b", "x;rm -rf /", "", "nom$(id)", "a" * 300):
        assert not valid_target(bad), bad

    class Reader:
        def __init__(self) -> None:
            self.asked: list[str] = []

        def ping(self, target: str) -> str:
            self.asked.append(target)
            return "pong"

    reader = Reader()
    network = NetworkTools(reader)  # type: ignore[arg-type]
    assert network.ping("--help") == (False, "--help") and reader.asked == []
    assert network.ping(" serveur-web ") == (True, "pong") and reader.asked == ["serveur-web"]


# ---- journal de la porte ----
LOG_LINES = (
    "3.5.0.9:40000 [23/Nov/2026:19:40:10.680] porte porte_vers_tls/tls 1/0/1 1823 CD 2/1/0/0/0 0/0 motif=- "
    "groupe=empreinte ja4=t13d_x_y as=AS16509 pays=US",
    "6.6.6.6:40000 [23/Nov/2026:19:40:10.680] porte avant-tls motif=liste-noire groupe=- ja4=- as=- pays=-",
    "6.6.6.6:40001 [22/Nov/2026:08:00:00.000] porte avant-tls motif=liste-noire groupe=- ja4=- as=- pays=-",
    "2001:db8::7:5555 [21/Nov/2026:08:00:00.000] porte avant-tls motif=debit-adresse groupe=- ja4=- as=- pays=-",
    "::ffff:9.9.9.9:12 [21/Nov/2026:08:00:00.000] porte avant-tls motif=budget groupe=- ja4=- as=- pays=-",
    "90.1.1.4:40000 [23/Nov/2026:19:40:02.436] porte porte_vers_tls/tls 1/0/0 7 CD 1/1/0/0/0 0/0 motif=- "
    "groupe=- ja4=t13d1516h2_8daaf6152771_e5627efa2ab1 as=AS3215 pays=FR",
    "1.1.1.1:1 [01/Nov/2026:08:00:00.000] porte avant-tls motif=budget groupe=- ja4=- as=- pays=-",
    "Started omega-tail : porte avant TLS de Funnel (HAProxy).",
)


def test_refusals_are_summed_from_the_gate_journal() -> None:
    assert parse_line(LOG_LINES[5]) is None and parse_line(LOG_LINES[7]) is None
    assert parse_line(LOG_LINES[3]).address == "2001:db8::7"  # type: ignore[union-attr]
    assert parse_line(LOG_LINES[4]).address == "9.9.9.9"  # type: ignore[union-attr]
    found = summarize(LOG_LINES, date(2026, 11, 23))
    assert found.total == 5  # le 1er novembre est hors de la periode
    assert found.by_reason == {"liste-noire": 2, "budget": 1, "debit-adresse": 1}
    assert found.groups == {"empreinte": 1}
    assert found.by_day == {"2026-11-21": 2, "2026-11-22": 1, "2026-11-23": 2}
    assert found.addresses[0] == ("6.6.6.6", 2, "", "")
    assert ("3.5.0.9", 1, "AS16509", "US") in found.addresses


def test_file_journal_search_reads_from_the_end(tmp_path: Path) -> None:
    log = tmp_path / "porte.log"
    log.write_text("\n".join(LOG_LINES) + "\n")
    result = FileJournal({"porte": [(str(log), "")]}).search("porte", date(2026, 11, 17), "(motif|groupe)=[a-z]")
    assert result.lines[0].startswith("1.1.1.1") and len(result.lines) == 6 and not result.truncated
    assert FileJournal({"porte": []}).search("porte", date(2026, 11, 17), "x").error


# ---- rapport ----
class FakeNetworkReader:
    def __init__(self) -> None:
        self.pinged: list[str] = []

    def devices(self) -> tuple[Device, ...]:
        return parse_devices(STATUS)

    def netcheck(self) -> Netcheck:
        return parse_netcheck(NETCHECK)

    def text(self, *arguments: str) -> tuple[str, str]:
        return ("MagicDNS: enabled", "") if arguments[0] == "dns" else ("", "lock: access denied")

    def metrics(self) -> Metrics:
        return parse_metrics(METRICS)

    def ping(self, target: str) -> str:
        self.pinged.append(target)
        return f"pong from {target} via 192.168.1.103:41641 in 1ms"

    def whois(self, target: str) -> str:
        return "Machine:\n  Name: serveur-web"


def report_tools(tmp_path: Path, *, gate: object | None = None) -> ReportTools:
    state = FakeTailscale()
    snapshot_tools = tools(FakeTailscale(state.state(), (FUNNEL_HTTPS,)))
    return ReportTools(version="0.6.0", snapshots=snapshot_tools, journal=FakeJournal(LOG_LINES),
                       breaker=BreakerPolicy, now=lambda: datetime(2026, 11, 23, 20, 0, tzinfo=timezone.utc),
                       gate=gate, network=NetworkTools(FakeNetworkReader()))  # type: ignore[arg-type]


def _gate(tmp_path: Path) -> object:
    from funnel_sim import FunnelSim
    from test_gate import PRODUCTION, FakeAdmin
    from test_gate import gate as make_gate

    return make_gate(tmp_path, FunnelSim(PRODUCTION), admin=FakeAdmin())


def test_report_hides_the_tailnet_unless_asked(tmp_path: Path) -> None:
    tools_ = report_tools(tmp_path, gate=_gate(tmp_path))
    facts = tools_.build()
    text = render_text(facts)
    for title in ("TAILSCALE", "PUBLICATION", "MACHINE", "PARE-FEU FUNNEL", "SURVIE", "ALERTES",
                  "ATTAQUES DES 7 DERNIERS JOURS"):
        assert f"\n{title}\n" in text, title
    assert "Compte : masqué" in text and "serveur-web" not in text and "Telephone" not in text
    assert "Appareils du tailnet : 2 en ligne sur 3 (plus 1 relais Funnel de Tailscale)" in text
    assert "liste noire 2" in text and "6.6.6.6" in text  # les attaquants restent
    assert "Règles de la porte, connexions refusées" in text and "empreinte inconnue en rafale" not in text
    private = render_text(tools_.build(include_private=True))
    assert "APPAREILS DU TAILNET" in private and "serveur-web" in private and "Compte : masqué" not in private
    page = render_html(tools_.build(include_private=True))
    assert "<script>alert(1)</script>" not in page and "&lt;script&gt;alert(1)&lt;/script&gt;" in page
    data = json.loads(render_json(facts))
    attacks = next(section for section in data["sections"] if section["cle"] == "attaques")
    assert attacks["faits"]["motifs"] == {"liste-noire": 2, "budget": 1, "debit-adresse": 1}
    assert data["prive_inclus"] is False


def test_report_without_gate_or_journal(tmp_path: Path) -> None:
    text = render_text(report_tools(tmp_path).build())
    assert "Pare-feu indisponible" in text

    class Closed(FakeJournal):
        def search(self, source: str, since: object, pattern: str):  # type: ignore[no-untyped-def]
            from omega_tail.ports.readers import JournalResult

            return JournalResult((), "journal vide ou illisible pour ce compte", "Ajoutez-le au groupe")

    tools_ = report_tools(tmp_path, gate=_gate(tmp_path))
    tools_.journal = Closed()
    text = render_text(tools_.build())
    assert "Journal de la porte illisible : journal vide ou illisible pour ce compte" in text


def test_cli_report_prints_or_exports(tmp_path: Path, capsys) -> None:  # type: ignore[no-untyped-def]
    tools_ = report_tools(tmp_path, gate=_gate(tmp_path))
    writer = FileExportWriter(tmp_path / "exports")

    def setup():  # type: ignore[no-untyped-def]
        return tools_, writer, "omega-base"

    def unused() -> int:
        raise AssertionError

    assert main_with(["rapport"], version="0.6.0", state=unused, dashboard=unused, report=setup) == 0  # type: ignore[arg-type]
    assert "RAPPORT DE LA MACHINE" in capsys.readouterr().out
    assert main_with(["rapport", "--format", "json", "--exporter"], version="0.6.0", state=unused,  # type: ignore[arg-type]
                     dashboard=unused, report=setup) == 0
    saved = list((tmp_path / "exports").glob("omega-tail-rapport-*.json"))
    assert len(saved) == 1 and json.loads(saved[0].read_text())["outil"] == "omega-tail"


# ---- ecrans ----
def lot7_app(tmp_path: Path, *, opener: object = None) -> tuple[OmegaTailApp, FakeNetworkReader]:
    settings = SettingsTools(JsonSettingsStore(tmp_path / "settings.json"), tmp_path / "exports",
                             tmp_path / "shots", lambda d: clear_directory(d, tmp_path), tmp_path)
    reader = FakeNetworkReader()
    network = NetworkTools(reader)  # type: ignore[arg-type]
    report = report_tools(tmp_path, gate=_gate(tmp_path))
    report.network = network
    app = OmegaTailApp(snapshots=tools(), journal=FakeJournal(), actions=ActionTools(run=lambda argv: 0),
                       version="0.6.0", render_profile=RenderProfile.STANDARD, settings=settings, splash=False,
                       writer=FileExportWriter(settings.exports_dir), refresh_seconds=0, network=network,
                       report=report, open_folder=opener)  # type: ignore[arg-type]
    return app, reader


async def test_network_screen_lists_devices_and_pings(tmp_path: Path) -> None:
    from test_tui import settle

    from omega_tail.interfaces.tui.screens.network import NetworkScreen
    from omega_tail.interfaces.tui.widgets.tables import WideTable

    app, reader = lot7_app(tmp_path)
    async with app.run_test(size=(130, 50)) as pilot:
        await settle(pilot)
        app.open_key("network")
        await settle(pilot)
        screen = app.screen
        assert isinstance(screen, NetworkScreen)
        table = screen.query_one("#devices-table", WideTable)
        assert table.row_count == 3 and str(table.get_row_at(0)[0]) == "<script>alert(1)</script>"
        assert "2 en ligne sur 3 appareil(s) ; 1 relais Funnel" in str(screen.query_one("#devices-note").render())
        screen.query_one("#show-ingress", Checkbox).value = True
        await settle(pilot)
        assert table.row_count == 4
        screen.query_one("#device-filter", Input).value = "serveur"
        await settle(pilot)
        assert table.row_count == 1
        screen.query_one("#ping", Button).press()
        await settle(pilot)
        assert reader.pinged == ["100.64.12.34"]
        assert "pong from 100.64.12.34" in str(screen.query_one("#probe-result", Static).render())
        screen.query_one("#target", Input).value = "--help"
        screen.query_one("#ping", Button).press()
        await settle(pilot)
        assert reader.pinged == ["100.64.12.34"]
        assert "n'est pas un nom ou une adresse valable" in str(screen.query_one("#probe-result", Static).render())
        screen.query_one("#netcheck", Button).press()
        await settle(pilot)
        assert "Relais le plus proche : Paris" in str(screen.query_one("#netcheck-box", Static).render())
        assert "MagicDNS: enabled" in str(screen.query_one("#dns-box", Static).render())
        assert "lock: access denied" in str(screen.query_one("#lock-box", Static).render())


async def test_report_screen_exports_and_falls_back_without_browser(tmp_path: Path) -> None:
    from test_tui import settle

    from omega_tail.interfaces.tui.screens.exports import ExportsScreen
    from omega_tail.interfaces.tui.screens.report import ReportScreen

    opened: list[Path] = []
    app, _reader = lot7_app(tmp_path, opener=lambda path: opened.append(path) or False)
    async with app.run_test(size=(130, 50)) as pilot:
        await settle(pilot)
        app.open_key("report")
        await settle(pilot)
        screen = app.screen
        assert isinstance(screen, ReportScreen)
        preview = str(screen.query_one("#report-preview", Static).render())
        assert "RAPPORT DE LA MACHINE" in preview and "Compte : masqué" in preview
        screen.query_one("#include-private", Checkbox).value = True
        await settle(pilot)
        assert "APPAREILS DU TAILNET" in str(screen.query_one("#report-preview", Static).render())
        for button in ("#export-txt", "#export-html"):
            screen.query_one(button, Button).press()
            await settle(pilot)
        names = sorted(path.suffix for path in (tmp_path / "exports").iterdir())
        assert names == [".html", ".txt"]
        screen.query_one("#view-exports", Button).press()
        await settle(pilot)
        await pilot.pause(0.2)
        assert opened == [tmp_path / "exports"]
        assert isinstance(app.screen, ExportsScreen)  # pas de navigateur : liste et lecture ici
