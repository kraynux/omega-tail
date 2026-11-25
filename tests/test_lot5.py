# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Lot 5 : Connexion et reglages (preferences de `tailscale set`, comptes) et Publication (ajout, retrait,
reconstruction, sauvegardes, essai). Jamais le vrai Tailscale : simulateur de serve/funnel et faux lecteurs."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest
from conftest import SERVE_HPC, FakeService, FakeTailscale, service_state, tailscale_state, tools
from funnel_sim import FunnelSim
from omega_lib.terminal.models import RenderProfile
from textual.widgets import Button, Checkbox, Input, Select, Static

from omega_tail.application.actions import ActionTools
from omega_tail.application.connection import ConnectionTools
from omega_tail.application.publication import PublicationTools, probe_mode
from omega_tail.application.settings import SettingsTools
from omega_tail.domain.funnel import Handler, handlers_of
from omega_tail.domain.preferences import Change, changes, needs_root, problem, set_command
from omega_tail.domain.publication import (
    AddRequest,
    PublicationError,
    add_command,
    backup_from,
    conflict,
    handler_for,
    rebuild_commands,
    remove_command,
)
from omega_tail.domain.tailscale import ExitNode, Preferences, Probe, Profile
from omega_tail.infrastructure.exports.writer import FileExportWriter
from omega_tail.infrastructure.settings.directories import clear_directory
from omega_tail.infrastructure.settings.json_store import JsonSettingsStore
from omega_tail.infrastructure.survival_store import FileCutStore
from omega_tail.infrastructure.tailscale.parsing import parse_exit_nodes, parse_profiles
from omega_tail.interfaces.tui.app import OmegaTailApp
from omega_tail.interfaces.tui.screens.confirm import ConfirmScreen
from omega_tail.interfaces.tui.screens.connection import ConnectionScreen
from omega_tail.interfaces.tui.screens.publication import PublicationScreen
from omega_tail.interfaces.tui.screens.typed_confirm import TypedConfirmScreen

# `tailscale get` (1.102.5, pc-107, 2026-11-23)
GET = {"accept-dns": "true", "accept-routes": "false", "advertise-exit-node": "false",
       "advertise-routes": "192.168.1.0/24", "auto-update": "false", "exit-node": "",
       "exit-node-allow-lan-access": "false", "hostname": "", "netfilter-mode": "on", "nickname": "",
       "operator": "kraynux", "relay-server-port": "", "shields-up": "false", "ssh": "false",
       "stateful-filtering": "false", "update-check": "true", "webclient": "false"}

SWITCH_LIST = """ID    Tailnet               Account
a1b2  kraynux@example.org   kraynux@example.org*
c3d4  travail.example       moi@travail.example
"""
EXIT_LIST = """
 IP                  HOSTNAME                          COUNTRY            CITY                   STATUS
 100.101.102.103     sortie.tailnet-exemple.ts.net.     United States      New York               -
 100.101.102.104     autre.tailnet-exemple.ts.net.      -                  -                      offline

# To view the complete list of exit nodes, including those in locations, run 'tailscale exit-node list'.
"""


# ---- preferences ----
def test_changes_are_normalized_and_in_screen_order() -> None:
    found = changes(GET, {**GET, "ssh": "True", "hostname": " vitrine ", "advertise-routes": "192.168.1.0/24, "})
    assert found == (Change("hostname", "", "vitrine"), Change("ssh", "false", "true"))
    assert set_command(found, sudo=False) == ("tailscale", "set", "--hostname=vitrine", "--ssh=true")


def test_values_are_checked_before_anything_runs() -> None:
    assert problem("hostname", "nom avec espace")
    assert problem("hostname", "a" * 64)
    assert not problem("hostname", "omega-server")
    assert problem("advertise-routes", "192.168.1.1/24")  # bits d'hote : refuse
    assert not problem("advertise-routes", "192.168.1.0/24,10.0.0.0/8")
    assert problem("netfilter-mode", "tout")
    assert problem("operator", "root; rm -rf /")
    assert problem("relay-server-port", "70000")
    assert problem("nickname", "a\nb")
    assert problem("inconnu", "x")


def test_session_cutting_changes_are_flagged() -> None:
    assert Change("shields-up", "false", "true").cuts_session
    assert not Change("shields-up", "true", "false").cuts_session
    assert Change("ssh", "true", "false").cuts_session
    assert Change("exit-node", "", "100.101.102.103").cuts_session
    assert not Change("accept-dns", "true", "false").cuts_session


def test_operator_never_needs_sudo_except_to_change_the_operator() -> None:
    connection = ConnectionTools(profiles=lambda: ((), ""), exit_nodes=lambda: ())
    plan = connection.plan(GET, {**GET, "accept-routes": "true"}, operator=True)
    assert plan.command == ("tailscale", "set", "--accept-routes=true")
    assert connection.plan(GET, {**GET, "accept-routes": "true"}, operator=False).command[0] == "sudo"
    plan = connection.plan(GET, {**GET, "operator": "autre"}, operator=True)
    assert plan.command == ("sudo", "tailscale", "set", "--operator=autre") and needs_root(plan.changes)
    refused = connection.plan(GET, {**GET, "hostname": "mauvais nom", "ssh": "true"}, operator=True)
    assert "hostname" in refused.problems and refused.command == ()
    assert connection.plan(GET, dict(GET), operator=True).command == ()
    assert connection.switch("c3d4", operator=True) == ("tailscale", "switch", "c3d4")
    assert connection.logout(operator=False) == ("sudo", "tailscale", "logout")
    with pytest.raises(ValueError):
        connection.switch("c3d4; reboot", operator=True)


def test_profiles_and_exit_nodes_are_parsed() -> None:
    assert parse_profiles(SWITCH_LIST) == (Profile("a1b2", "kraynux@example.org", "kraynux@example.org", True),
                                           Profile("c3d4", "travail.example", "moi@travail.example", False))
    assert parse_exit_nodes(EXIT_LIST) == (ExitNode("100.101.102.103", "sortie.tailnet-exemple.ts.net"),
                                           ExitNode("100.101.102.104", "autre.tailnet-exemple.ts.net", "offline"))
    assert parse_exit_nodes("no exit nodes found\n") == ()


# ---- publication : domaine ----
def test_requests_are_checked() -> None:
    assert handler_for(AddRequest("https", 443, "8080", True)) == Handler("https", 443, "http://127.0.0.1:8080", "/",
                                                                          0, True)
    assert handler_for(AddRequest("tcp", 2222, "22", False)).target == "tcp://127.0.0.1:22"
    for bad in (AddRequest("https", 8080, "8080", True),            # Funnel : 443, 8443, 10000 seulement
                AddRequest("https", 443, "http://192.168.1.5:80", False),  # service local seulement
                AddRequest("https", 443, "8080", False, "/a b"),
                AddRequest("tcp", 443, "http://127.0.0.1:80", False),
                AddRequest("ftp", 21, "21", False),
                AddRequest("https", 0, "80", False)):
        with pytest.raises(PublicationError):
            handler_for(bad)


def test_commands_and_conflicts() -> None:
    root = Handler("https", 443, "http://127.0.0.1:80", "/", 0, True)
    api = Handler("https", 443, "http://127.0.0.1:8080", "/api", 0, True)
    assert add_command(api) == ("tailscale", "funnel", "--bg", "--yes", "--https=443", "--set-path=/api",
                                "http://127.0.0.1:8080")
    assert remove_command(root, [root]) == ("tailscale", "funnel", "--https=443", "off")
    assert remove_command(api, [root, api]) == ("tailscale", "funnel", "--https=443", "--set-path=/api", "off")
    assert rebuild_commands([api, root])[0] == ("tailscale", "serve", "reset")
    assert rebuild_commands([api, root])[1][-1] == "http://127.0.0.1:80"  # « / » d'abord
    assert conflict(Handler("https", 443, "http://127.0.0.1:81", "/", 0, False), [root])
    assert conflict(Handler("https", 443, "http://127.0.0.1:81", "/", 0, True), [root])
    assert not conflict(api, [root])
    assert probe_mode(Handler("tcp", 443, "tcp://127.0.0.1:9443", "", 2, True)) == "https"
    assert probe_mode(Handler("tcp", 3389, "tcp://localhost:3389")) == "tcp"


def test_backup_names_tell_who_made_them() -> None:
    assert backup_from("/x/funnel-porte-20261123-101500.json", ()).origin == "pare-feu"  # type: ignore[union-attr]
    assert backup_from("/x/funnel-20261123-101500.json", ()).when == "2026-11-23 10:15:00"  # type: ignore[union-attr]
    assert backup_from("/x/autre.json", ()) is None


# ---- publication : application ----
class Clock:
    def __init__(self) -> None:
        self.now = datetime(2026, 11, 23, 10, 0, tzinfo=timezone.utc)

    def __call__(self) -> datetime:
        self.now += timedelta(seconds=1)
        return self.now


def publication(sim: FunnelSim, tmp_path: Path, *, gate: int | None = None, cut: bool = False) -> PublicationTools:
    return PublicationTools(store=FileCutStore(tmp_path / "var"), serve_config=sim.serve_config, quiet=sim.quiet,
                            now=Clock(), gate_port=lambda: gate, cut_active=lambda: cut,
                            probe_public=lambda host, port, mode, path: Probe(True, f"{mode} {host}:{port}{path}"))


def test_add_saves_then_verifies(tmp_path: Path) -> None:
    sim = FunnelSim(SERVE_HPC)
    tools_ = publication(sim, tmp_path)
    outcome = tools_.add(AddRequest("tcp", 2222, "22", False))
    assert outcome.ok, outcome
    assert Handler("tcp", 2222, "tcp://127.0.0.1:22", "", 0, False) in handlers_of(sim.config)
    assert len(tools_.backups()) == 1 and tools_.backups()[0].origin == "publication"
    assert not tools_.add(AddRequest("https", 443, "8080", False)).ok  # port deja publie pour Internet


def test_leftover_funnel_permission_is_cleaned_by_a_rebuild(tmp_path: Path) -> None:
    """Constat du 2026-11-22 : « --tcp=PORT off » laisse l'autorisation Funnel ; un Serve ajoute ensuite sur ce port
    serait public. La verification le voit et reconstruit."""
    sim = FunnelSim({"TCP": {"10000": {"TCPForward": "127.0.0.1:22"}},
                     "AllowFunnel": {"kraynux.tailnet-exemple.ts.net:10000": True}})
    tools_ = publication(sim, tmp_path)
    assert tools_.remove(Handler("tcp", 10000, "tcp://127.0.0.1:22", "", 0, True)).ok
    assert sim.config.get("AllowFunnel")  # reste derriere, sans effet tant que rien n'y est servi
    outcome = tools_.add(AddRequest("tcp", 10000, "2222", False))
    assert outcome.ok
    assert ("tailscale", "serve", "reset") in sim.calls
    assert handlers_of(sim.config) == (Handler("tcp", 10000, "tcp://127.0.0.1:2222", "", 0, False),)


def test_remove_one_path_keeps_the_others(tmp_path: Path) -> None:
    sim = FunnelSim(SERVE_HPC)
    tools_ = publication(sim, tmp_path)
    assert tools_.add(AddRequest("https", 443, "8080", True, "/api")).ok
    assert len(handlers_of(sim.config)) == 2
    assert tools_.remove(Handler("https", 443, "http://127.0.0.1:8080", "/api", 0, True)).ok
    assert handlers_of(sim.config) == handlers_of(SERVE_HPC)


def test_restore_gives_back_a_saved_publication(tmp_path: Path) -> None:
    sim = FunnelSim(SERVE_HPC)
    tools_ = publication(sim, tmp_path)
    assert tools_.add(AddRequest("tcp", 2222, "22", False)).ok
    first = tools_.backups()[-1]
    outcome = tools_.restore(first.path)
    assert outcome.ok, outcome
    assert set(handlers_of(sim.config)) == set(handlers_of(SERVE_HPC))
    assert len(tools_.backups()) == 2  # l'etat d'avant la restauration est garde aussi


def test_refusals(tmp_path: Path) -> None:
    gated = {"TCP": {"443": {"TCPForward": "127.0.0.1:9443", "ProxyProtocol": 2}},
             "AllowFunnel": {"kraynux.tailnet-exemple.ts.net:443": True}}
    sim = FunnelSim(gated)
    gate_handler = handlers_of(gated)[0]
    assert not publication(sim, tmp_path, gate=9443).remove(gate_handler).ok
    assert not publication(sim, tmp_path, gate=9443).restore("/nulle/part.json").ok
    assert not publication(sim, tmp_path, cut=True).add(AddRequest("tcp", 2222, "22", False)).ok
    assert sim.calls == []


def test_tailscale_refusal_changes_nothing(tmp_path: Path) -> None:
    sim = FunnelSim(SERVE_HPC, fail_on="--tcp=8443")
    outcome = publication(sim, tmp_path).add(AddRequest("tcp", 8443, "22", True))
    assert not outcome.ok and "rien n'a changé" in outcome.message
    assert sim.config == SERVE_HPC and ("tailscale", "serve", "reset") not in sim.calls


def test_end_to_end_probe_goes_through_the_public_path(tmp_path: Path) -> None:
    sim = FunnelSim(SERVE_HPC)
    probe = publication(sim, tmp_path).test(handlers_of(SERVE_HPC)[0], "kraynux.tailnet-exemple.ts.net", "100.1.2.3")
    assert probe.ok and probe.detail == "https kraynux.tailnet-exemple.ts.net:443/"


# ---- interface ----
class PrefsTailscale(FakeTailscale):
    def preferences(self) -> Preferences:
        return Preferences(dict(GET), readable=True)


def make_app(tmp_path: Path, ran: list[tuple[str, ...]], sim: FunnelSim | None = None,
             through: bool = False) -> OmegaTailApp:
    settings = SettingsTools(JsonSettingsStore(tmp_path / "settings.json"), tmp_path / "exports",
                             tmp_path / "shots", lambda d: clear_directory(d, tmp_path), tmp_path)
    connection = ConnectionTools(profiles=lambda: (parse_profiles(SWITCH_LIST), ""),
                                 exit_nodes=lambda: parse_exit_nodes(EXIT_LIST))
    return OmegaTailApp(snapshots=tools(PrefsTailscale(tailscale_state()), FakeService(service_state()), through),
                        journal=None,  # type: ignore[arg-type]
                        actions=ActionTools(run=lambda argv: ran.append(tuple(argv)) or 0), version="0.4.0",
                        render_profile=RenderProfile.STANDARD, settings=settings, splash=False,
                        writer=FileExportWriter(settings.exports_dir), refresh_seconds=0, connection=connection,
                        publication=publication(sim or FunnelSim(SERVE_HPC), tmp_path))


async def settle(pilot) -> None:  # type: ignore[no-untyped-def]
    await pilot.app.workers.wait_for_complete()
    await pilot.pause()


async def test_connection_screen_shows_and_applies_settings(tmp_path: Path) -> None:
    ran: list[tuple[str, ...]] = []
    app = make_app(tmp_path, ran)
    async with app.run_test(size=(120, 50)) as pilot:
        await settle(pilot)
        app.screen.query_one("#menu-connection", Button).press()
        await settle(pilot)
        screen = app.screen
        assert isinstance(screen, ConnectionScreen)
        assert screen.query_one("#pref-accept-dns", Checkbox).value
        assert screen.query_one("#pref-advertise-routes", Input).value == "192.168.1.0/24"
        assert screen.query_one("#pref-exit-node", Select).value == "__aucun__"
        await settle(pilot)
        assert not screen.query_one("#exit-note", Static).display  # des nœuds existent
        assert not screen.query_one("#switch", Button).disabled  # deux comptes
        assert "connecté" in str(screen.query_one("#conn-state", Static).render())
        assert not screen.query_one("#changes-frame").display  # rien en attente : pas de boîte vide
        screen.query_one("#pref-ssh", Checkbox).value = True
        await pilot.pause()
        assert screen.query_one("#changes-frame").display  # affiché pendant la saisie
        text = str(screen.query_one("#changes", Static).render())
        assert "tailscale set --ssh=true" in text and "sudo" not in text
        screen.query_one("#apply", Button).press()
        await pilot.pause()
        assert isinstance(app.screen, ConfirmScreen)
        app.screen.query_one("#confirm", Button).press()
        await settle(pilot)
        assert ran == [("tailscale", "set", "--ssh=true")]
        await settle(pilot)
        result = str(screen.query_one("#changes", Static).render())
        # le résultat reste écrit, vérifié sur les valeurs relues (le faux Tailscale n'a rien changé)
        assert screen.query_one("#changes-frame").display and "Dernière application" in result
        assert "✖" in result and "false lu" in result
        assert not screen.query_one("#pref-ssh", Checkbox).value


async def test_my_account_fills_the_operator_field(tmp_path: Path) -> None:
    ran: list[tuple[str, ...]] = []
    app = make_app(tmp_path, ran)
    async with app.run_test(size=(120, 50)) as pilot:
        await settle(pilot)
        app.open_key("connection")
        await settle(pilot)
        screen = app.screen
        field = screen.query_one("#pref-operator", Input)
        assert field.placeholder == "ex. kraynux"
        assert screen.query_one("#pref-advertise-routes", Input).placeholder.startswith("ex. 192.168")
        screen._loaded = {**screen._loaded, "operator": ""}
        field.value = ""
        screen.query_one("#operator-me", Button).press()
        await pilot.pause()
        assert field.value == "kraynux"
        assert "sudo tailscale set --operator=kraynux" in str(screen.query_one("#changes", Static).render())


async def test_no_exit_node_explains_how_to_get_one(tmp_path: Path) -> None:
    app = make_app(tmp_path, [])
    app.connection = ConnectionTools(profiles=lambda: ((), ""), exit_nodes=lambda: ())
    async with app.run_test(size=(120, 50)) as pilot:
        await settle(pilot)
        app.open_key("connection")
        await settle(pilot)
        note = app.screen.query_one("#exit-note", Static)
        assert note.display and "Proposer cette machine" in str(note.render())


def test_forwarding_is_read_and_enabled_in_a_separate_file(tmp_path: Path) -> None:
    from omega_tail.domain.forwarding import SYSCTL_PATH, Forwarding, needs_forwarding
    from omega_tail.infrastructure.system.forwarding import read_forwarding
    (tmp_path / "net/ipv4").mkdir(parents=True)
    (tmp_path / "net/ipv4/ip_forward").write_text("0\n")
    found = read_forwarding(tmp_path)
    assert found == Forwarding(False, None) and found.missing == ("net.ipv4.ip_forward",)
    assert needs_forwarding({"advertise-routes": "10.0.0.0/8"}) and needs_forwarding({"advertise-exit-node": "true"})
    assert not needs_forwarding({"advertise-exit-node": "false", "advertise-routes": ""})
    command = ConnectionTools(profiles=lambda: ((), ""), exit_nodes=lambda: ()).enable_forwarding()
    assert command[:3] == ("sudo", "sh", "-c") and SYSCTL_PATH in command[3] and "sysctl -p" in command[3]
    assert ConnectionTools(profiles=lambda: ((), ""), exit_nodes=lambda: (), as_root=True).enable_forwarding()[0] == "sh"


async def test_forwarding_warning_and_button(tmp_path: Path) -> None:
    from omega_tail.domain.forwarding import Forwarding
    ran: list[tuple[str, ...]] = []
    app = make_app(tmp_path, ran)
    app.connection = ConnectionTools(profiles=lambda: ((), ""), exit_nodes=lambda: (),
                                     forwarding=lambda: Forwarding(False, False))
    async with app.run_test(size=(120, 50)) as pilot:
        await settle(pilot)
        app.open_key("connection")
        await settle(pilot)
        screen = app.screen
        note = screen.query_one("#forward-note", Static)
        assert note.display and "ip_forward" in str(note.render())  # GET annonce 192.168.1.0/24
        screen.query_one("#pref-advertise-routes", Input).value = ""
        await pilot.pause()
        assert not note.display
        screen.query_one("#pref-advertise-exit-node", Checkbox).value = True
        await pilot.pause()
        assert note.display
        await pilot.pause()
        assert "Activer le transfert IP" in str(screen.query_one("#changes", Static).render())
        screen.query_one("#forward-on", Button).press()
        await pilot.pause()
        assert isinstance(app.screen, ConfirmScreen)
        app.screen.query_one("#confirm", Button).press()
        await settle(pilot)
        assert ran and ran[0][:3] == ("sudo", "sh", "-c")


async def test_logout_needs_the_machine_name(tmp_path: Path) -> None:
    ran: list[tuple[str, ...]] = []
    app = make_app(tmp_path, ran, through=True)
    async with app.run_test(size=(120, 50)) as pilot:
        await settle(pilot)
        app.open_key("connection")
        await settle(pilot)
        app.screen.query_one("#logout", Button).press()
        await pilot.pause()
        confirm = app.screen
        assert isinstance(confirm, TypedConfirmScreen)
        assert "COUPÉE" in str(confirm.query_one("#confirm-text", Static).render())
        assert confirm.query_one("#confirm", Button).disabled
        confirm.query_one("#typed", Input).value = "omega-server"
        await pilot.pause()
        confirm.query_one("#confirm", Button).press()
        await settle(pilot)
        assert ran == [("tailscale", "logout")]


async def test_publication_screen_lists_adds_and_removes(tmp_path: Path) -> None:
    ran: list[tuple[str, ...]] = []
    sim = FunnelSim(SERVE_HPC)
    app = make_app(tmp_path, ran, sim)
    async with app.run_test(size=(120, 50)) as pilot:
        await settle(pilot)
        app.open_key("publication")
        await settle(pilot)
        screen = app.screen
        assert isinstance(screen, PublicationScreen)
        table = screen.query_one("#pub-table")
        assert table.row_count == 1  # type: ignore[attr-defined]
        assert "non protégé" in str(table.get_row_at(0))  # type: ignore[attr-defined]
        screen.query_one("#add-target", Input).value = "22"
        screen.query_one("#add-kind", Select).value = "tcp"
        screen.query_one("#add-port", Input).value = "2222"
        screen.query_one("#add", Button).press()
        await settle(pilot)
        await settle(pilot)
        assert table.row_count == 2  # type: ignore[attr-defined]
        assert ran == []  # sans terminal : l'operateur n'a pas besoin de sudo
        table.move_cursor(row=1)  # type: ignore[attr-defined]
        screen.query_one("#remove", Button).press()
        await pilot.pause()
        assert isinstance(app.screen, ConfirmScreen)
        app.screen.query_one("#confirm", Button).press()
        await settle(pilot)
        await settle(pilot)
        assert set(handlers_of(sim.config)) == set(handlers_of(SERVE_HPC))
        assert [backup.origin for backup in screen._backups] == ["publication", "publication"]
