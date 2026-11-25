# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
from __future__ import annotations

from conftest import SERVE_HPC, SERVE_MPC_RDP, STATUS

from omega_tail.domain.tailscale import BackendState, PublishMode
from omega_tail.infrastructure.system.systemd import parse_show
from omega_tail.infrastructure.tailscale.parsing import parse_preferences, parse_serve, parse_status, short_version


def test_short_version_keeps_only_the_number() -> None:
    assert short_version("1.104.7\n  tailscale commit: fb3b\n") == "1.104.7"
    assert short_version("1.104.4-tfb3b9b2964-g0123") == "1.104.4"
    assert short_version("") == ""


def test_status_is_read_and_daemon_behind_client_is_seen() -> None:
    state = parse_status(STATUS, "1.104.7")
    assert state.daemon_version == "1.104.4" and state.versions_differ
    assert state.backend is BackendState.RUNNING
    assert state.dns_name == "kraynux.tailnet-exemple.ts.net"
    assert state.user == "kraynux@example.org"
    assert (state.peers_total, state.peers_online) == (3, 2)
    assert state.key_expiry is not None and state.key_expiry.year == 2027
    assert state.health == ("a message", "b message")  # sans doublon, ordre stable


def test_status_with_missing_fields_never_fails() -> None:
    state = parse_status({"Self": None, "Peer": [], "Health": None, "BackendState": "Weird"}, "")
    assert state.backend is BackendState.UNKNOWN and state.peers_total == 0 and state.key_expiry is None


def test_preferences_table_with_empty_values() -> None:
    text = "NAME                VALUE\naccept-dns          true\noperator            \nadvertise-routes    192.168.1.0/24\n"
    prefs = parse_preferences(text)
    assert prefs.readable and prefs.operator == "" and prefs.values["advertise-routes"] == "192.168.1.0/24"
    assert parse_preferences("NAME VALUE\noperator kraynux\n").operator == "kraynux"


def test_serve_https_funnel_of_omega_server_is_exposed() -> None:
    (item,) = parse_serve(SERVE_HPC)
    assert (item.port, item.public, item.mode) == (443, True, PublishMode.HTTPS)
    assert item.target == "http://localhost:80" and item.path == "/" and item.exposed


def test_serve_tcp_forward_tailnet_only_is_not_exposed() -> None:
    (item,) = parse_serve(SERVE_MPC_RDP, "kraynux-mpc.ts.net")
    assert (item.port, item.public, item.mode) == (3389, False, PublishMode.TCP)
    assert item.target == "tcp://localhost:3389" and not item.exposed


def test_serve_funnel_tcp_with_proxy_protocol_is_the_protected_form() -> None:
    data = {"TCP": {"443": {"TCPForward": "127.0.0.1:9443", "ProxyProtocol": 2}},
            "AllowFunnel": {"x.ts.net:443": True}}
    (item,) = parse_serve(data)
    assert item.public and item.mode is PublishMode.TCP and item.proxy_protocol == 2 and not item.exposed
    terminated = parse_serve({"TCP": {"8443": {"TCPForward": "127.0.0.1:1", "TerminateTLS": "x.ts.net"}},
                              "AllowFunnel": {"x.ts.net:8443": True}})
    assert terminated[0].mode is PublishMode.TLS_TERMINATED_TCP and terminated[0].exposed


def test_serve_foreground_sessions_and_empty_config() -> None:
    assert parse_serve({}) == ()
    found = parse_serve({"Foreground": {"s1": SERVE_HPC}})
    assert len(found) == 1 and found[0].public


def test_systemctl_show_parsing() -> None:
    text = ("LoadState=loaded\nActiveState=active\nSubState=running\nUnitFileState=enabled\nMainPID=638\n"
            "MemoryCurrent=109000000\nExecStart={ path=/usr/bin/tailscaled ; argv[]=/usr/bin/tailscaled --state=x "
            "; ignore_errors=no }\nDropInPaths=/etc/systemd/system/tailscaled.service.d/override.conf\n"
            "CPUQuotaPerSecUSec=infinity\nCPUWeight=[not set]\nAllowedCPUs=\nNice=0\n")
    state = parse_show(text)
    assert state.known and state.running and state.main_pid == 638 and state.memory_bytes == 109000000
    assert state.exec_start == "/usr/bin/tailscaled --state=x"
    assert state.drop_ins == ("/etc/systemd/system/tailscaled.service.d/override.conf",)
    assert not state.confined
    assert parse_show("LoadState=not-found\n").known is False
    assert parse_show(text.replace("AllowedCPUs=", "AllowedCPUs=0")).confined
    assert parse_show(text.replace("CPUQuotaPerSecUSec=infinity", "CPUQuotaPerSecUSec=500ms")).confined
