# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
from __future__ import annotations

from datetime import timedelta

from conftest import FUNNEL_HTTPS, NOW, service_state, snapshot, tailscale_state

from omega_tail.application.actions import ActionTools, operator_command, service_command
from omega_tail.domain.alerts import Level, Target, alerts_for
from omega_tail.domain.machine import MachineState
from omega_tail.domain.service import ServiceAction
from omega_tail.domain.session import Risk, guard_service_action, is_tailscale_address, session_through_tailscale
from omega_tail.domain.tailscale import BackendState, Preferences, Publication, PublishMode, TailscaleState


def codes(shot) -> list[str]:  # type: ignore[no-untyped-def]
    return [alert.code for alert in alerts_for(shot, NOW)]


def test_healthy_machine_has_no_alert() -> None:
    assert codes(snapshot()) == []


def test_not_installed_is_the_only_alert() -> None:
    assert codes(snapshot(tailscale=TailscaleState(installed=False, reachable=False))) == ["not-installed"]


def test_case_of_web_server_and_omega_server() -> None:
    """Releves du 2026-11-22 : demon pas redemarre, Funnel HTTPS, non confine, 76-81 °C."""
    shot = snapshot(tailscale=tailscale_state(daemon_version="1.104.4"), publications=(FUNNEL_HTTPS,),
                    machine=MachineState(temperature_c=81.0, tailscaled_cpu_percent=6.2))
    found = alerts_for(shot, NOW)
    assert [alert.code for alert in found] == ["daemon-outdated", "funnel-unprotected", "temperature",
                                               "not-confined"]
    assert found[0].target is Target.SERVICE and found[0].params == {"daemon": "1.104.4", "client": "1.104.7"}
    assert found[1].target is Target.FIREWALL and found[1].params == {"port": 443}
    assert found[2].level is Level.WARNING
    assert found[3].level is Level.INFO and found[3].target is Target.SURVIVAL


def test_critical_alerts_come_first() -> None:
    shot = snapshot(service=service_state(active="failed"), tailscale=tailscale_state(reachable=False),
                    preferences=Preferences({"operator": ""}, readable=True),
                    machine=MachineState(temperature_c=90.0))
    found = alerts_for(shot, NOW)
    assert [alert.level for alert in found][:2] == [Level.CRITICAL, Level.CRITICAL]
    assert "not-operator" not in [alert.code for alert in found]  # demon injoignable : pas de conseil d'operateur


def test_login_key_expiry_cpu_operator_and_health() -> None:
    shot = snapshot(tailscale=tailscale_state(backend=BackendState.NEEDS_LOGIN, key_expiry=NOW + timedelta(days=3),
                                              health=("dns broken",)),
                    preferences=Preferences({"operator": ""}, readable=True),
                    machine=MachineState(tailscaled_cpu_percent=120.0))
    assert codes(shot) == ["needs-login", "key-expiry", "tailscaled-cpu", "health", "not-operator"]
    assert codes(snapshot(user="root", preferences=Preferences({"operator": ""}, readable=True))) == []


def test_tailnet_only_or_protected_publication_is_not_an_alert() -> None:
    tcp = Publication(443, True, PublishMode.TCP, "x", "tcp://127.0.0.1:9443", "", 2)
    rdp = Publication(3389, False, PublishMode.TCP, "x", "tcp://localhost:3389")
    assert "funnel-unprotected" not in codes(snapshot(publications=(tcp, rdp)))


def test_tailscale_addresses_and_ssh_connection() -> None:
    assert is_tailscale_address("100.64.0.72") and is_tailscale_address("fd7a:115c:a1e0::1")
    assert not is_tailscale_address("192.168.1.60") and not is_tailscale_address("nonsense")
    assert session_through_tailscale("100.64.10.47 51234 100.64.0.72 22")
    assert not session_through_tailscale("192.168.1.60 51234 192.168.1.50 22")
    assert not session_through_tailscale("")


def test_guard_against_cutting_the_branch() -> None:
    assert guard_service_action(ServiceAction.STOP, True).risk is Risk.CUT
    assert guard_service_action(ServiceAction.RESTART, True).risk is Risk.INTERRUPTION
    assert guard_service_action(ServiceAction.START, True).risk is Risk.NONE
    assert guard_service_action(ServiceAction.STOP, False).risk is Risk.NONE


def test_commands_are_shown_complete_and_sudo_only_when_needed() -> None:
    assert service_command(ServiceAction.RESTART) == ("sudo", "systemctl", "restart", "tailscaled.service")
    assert service_command(ServiceAction.STOP, as_root=True) == ("systemctl", "stop", "tailscaled.service")
    assert operator_command("kraynux") == ("sudo", "tailscale", "set", "--operator=kraynux")
    ran: list[tuple[str, ...]] = []
    tools = ActionTools(run=lambda argv: ran.append(tuple(argv)) or 0)
    assert tools.service(ServiceAction.START)[1] == 0 and ran == [("sudo", "systemctl", "start",
                                                                   "tailscaled.service")]
