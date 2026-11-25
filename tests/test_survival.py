# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from pathlib import Path

from conftest import NOW, snapshot
from funnel_sim import HOST, FunnelSim

from omega_tail.application.breaker_settings import KEY_CPU, KEY_MINUTES, load_policy, save_policy
from omega_tail.application.survival import SurvivalTools
from omega_tail.domain.alerts import Level, Target, alerts_for
from omega_tail.domain.breaker import BreakerPolicy, Sample, assess
from omega_tail.domain.confinement import DROP_IN_PATH, ConfinementPlan, drop_in_text, recommended
from omega_tail.domain.funnel import Cut, cut_commands, handlers_of, restore_commands, same_publication
from omega_tail.infrastructure.settings.json_store import JsonSettingsStore
from omega_tail.infrastructure.survival_store import FileCutStore

# Configuration mixte : Funnel HTTPS a deux chemins + Funnel TCP PROXY v2 + Serve RDP (tailnet seul)
MIXED = {
    "TCP": {"443": {"HTTPS": True}, "8443": {"TCPForward": "127.0.0.1:9443", "ProxyProtocol": 2},
            "3389": {"TCPForward": "localhost:3389"}},
    "Web": {f"{HOST}:443": {"Handlers": {"/": {"Proxy": "http://localhost:80"},
                                         "/b": {"Proxy": "http://127.0.0.1:8080/b"}}}},
    "AllowFunnel": {f"{HOST}:443": True, f"{HOST}:8443": True},
}


def test_only_internet_ports_are_cut_once_each_and_restored_in_order() -> None:
    assert cut_commands(MIXED) == (("tailscale", "funnel", "--https=443", "off"),
                                   ("tailscale", "funnel", "--tcp=8443", "off"))
    assert restore_commands(MIXED) == (
        ("tailscale", "funnel", "--bg", "--yes", "--https=443", "http://localhost:80"),
        ("tailscale", "funnel", "--bg", "--yes", "--https=443", "--set-path=/b", "http://127.0.0.1:8080/b"),
        ("tailscale", "funnel", "--bg", "--yes", "--tcp=8443", "--proxy-protocol=2", "tcp://127.0.0.1:9443"))
    assert {handler.port for handler in handlers_of(MIXED) if not handler.public} == {3389}


def test_simulated_round_trip_gives_back_the_same_json() -> None:
    sim = FunnelSim(MIXED)
    for command in cut_commands(MIXED):
        sim.quiet(command)
    assert sim.config["TCP"] == {"3389": {"TCPForward": "localhost:3389"}}  # le tailnet reste
    assert not any(handler.public for handler in handlers_of(sim.config))  # plus rien de servi a Internet
    for command in restore_commands(MIXED):
        sim.quiet(command)
    assert same_publication(MIXED, sim.config) and sim.config == MIXED


def tools(tmp_path: Path, sim: FunnelSim) -> SurvivalTools:
    return SurvivalTools(store=FileCutStore(tmp_path / "var"), serve_config=sim.serve_config, quiet=sim.quiet,
                         now=lambda: NOW, python="/opt/omega-tail/.venv/bin/python", user=lambda: "kraynux")


def test_total_cut_then_restore(tmp_path: Path) -> None:
    sim = FunnelSim(MIXED)
    survival = tools(tmp_path, sim)
    outcome = survival.cut(None)
    assert outcome.ok and survival.store.current() is not None and survival.store.current().total
    assert not any(handler.public for handler in handlers_of(sim.config))
    saved = Path(survival.store.current().saved)
    assert saved.stat().st_mode & 0o777 == 0o600
    assert not survival.cut(None).ok  # deja coupe
    assert survival.restore().ok and sim.config == MIXED and survival.store.current() is None
    journal = (tmp_path / "var" / "funnel" / "journal.log").read_text()
    assert "coupure totale" in journal and "identique a la sauvegarde" in journal


def test_cut_leaves_no_funnel_permission_behind(tmp_path: Path) -> None:
    """« --tcp=PORT off » laisse l'autorisation Funnel (Tailscale annonce toujours « Funnel on ») : la coupure
    repart de zero avec les seuls points du tailnet, puis la remise en route rend la publication a l'identique."""
    from omega_tail.domain.funnel import funnel_allowed

    sim = FunnelSim(MIXED)
    survival = tools(tmp_path, sim)
    assert survival.cut(None).ok
    assert funnel_allowed(sim.config) == () and sim.config["TCP"] == {"3389": {"TCPForward": "localhost:3389"}}
    assert survival.restore().ok and sim.config == MIXED


def test_timed_cut_schedules_first_under_the_operator_account(tmp_path: Path) -> None:
    sim = FunnelSim(MIXED)
    survival = tools(tmp_path, sim)
    scheduled: list[tuple[str, ...]] = []
    outcome = survival.cut(10, schedule=lambda command: scheduled.append(tuple(command)) or 0,
                           cut_id="20261122-190000")
    assert outcome.ok and outcome.params["minutes"] == 10
    (timer,) = scheduled
    assert timer[:3] == ("sudo", "systemd-run", "--on-active=10min")
    assert "--uid=kraynux" in timer and "--unit=omega-tail-retablir-20261122-190000" in timer
    assert timer[-6:] == ("-m", "omega_tail", "disjoncteur", "retablir", "--id", "20261122-190000")
    cut = survival.store.current()
    assert cut is not None and cut.until == (NOW + timedelta(minutes=10)).isoformat() and cut.ports == (443, 8443)
    assert survival.restore("ancienne-coupure").message.startswith("Minuterie d'une ancienne")
    assert survival.store.current() is not None
    assert survival.restore("20261122-190000").ok and sim.config == MIXED


def test_refused_sudo_for_the_timer_cuts_nothing(tmp_path: Path) -> None:
    sim = FunnelSim(MIXED)
    survival = tools(tmp_path, sim)
    outcome = survival.cut(10, schedule=lambda command: 1)
    assert not outcome.ok and sim.calls == [] and survival.store.current() is None and sim.config == MIXED


def test_failed_cut_puts_the_publication_back(tmp_path: Path) -> None:
    sim = FunnelSim(MIXED, fail_on="--tcp=8443 off")
    survival = tools(tmp_path, sim)
    outcome = survival.cut(None)
    assert not outcome.ok and survival.store.current() is None and same_publication(MIXED, sim.config)


def test_nothing_public_nothing_to_cut_and_incomplete_restore_keeps_the_save(tmp_path: Path) -> None:
    rdp = {"TCP": {"3389": {"TCPForward": "localhost:3389"}}}
    assert not tools(tmp_path, FunnelSim(rdp)).cut(None).ok
    sim = FunnelSim(MIXED)
    survival = tools(tmp_path / "b", sim)
    assert survival.cut(None).ok
    sim.fail_on = "--tcp=8443"
    outcome = survival.restore()
    assert not outcome.ok and survival.store.current() is not None


def test_breaker_proposes_only_after_the_whole_window() -> None:
    policy = BreakerPolicy(cpu_percent=80, seconds=60, temperature_c=85)
    rising = [Sample(float(t), 120.0, 60.0) for t in range(0, 61, 5)]
    trigger = assess(rising, policy)
    assert trigger is not None and trigger.params["average"] == 120.0
    assert assess(rising[:6], policy) is None  # 25 s seulement
    dip = [*rising[:-2], Sample(55.0, 20.0, 60.0), rising[-1]]
    assert assess(dip, policy) is None  # une baisse dans la fenetre : pas d'attaque soutenue
    hot = assess([Sample(0.0, 2.0, 86.0)], policy)
    assert hot is not None and "Température" in hot.reason
    assert assess([], policy) is None


def test_policy_settings_are_bounded(tmp_path: Path) -> None:
    store = JsonSettingsStore(tmp_path / "settings.json")
    assert load_policy(store) == BreakerPolicy()
    assert save_policy(store, {KEY_CPU: "150", KEY_MINUTES: "0"}) == [KEY_MINUTES]
    assert load_policy(store).cpu_percent == 150.0 and load_policy(store).minutes == 10
    store.set(KEY_CPU, "9999")
    assert load_policy(store).cpu_percent == 80.0


def test_confinement_plan_and_file() -> None:
    assert [recommended(n).quota_percent for n in (1, 2, 4, 8)] == [50, 50, 100, 200]
    text = drop_in_text(ConfinementPlan(100))
    assert "[Service]\nCPUQuota=100%\nCPUWeight=50\nIOWeight=50\nNice=5\n" in text
    assert DROP_IN_PATH == "/etc/systemd/system/tailscaled.service.d/50-omega-tail.conf"


def test_confinement_commands_install_our_own_file_only(tmp_path: Path) -> None:
    survival = tools(tmp_path, FunnelSim(MIXED))
    commands = survival.confine_commands(recommended(4), restart=True, ssh_unit="sshd.service")
    source = str(tmp_path / "var" / "survie" / "50-omega-tail.conf")
    assert commands[0] == ("sudo", "install", "-D", "-m", "0644", source, DROP_IN_PATH)
    assert commands[1][-1] == "/etc/systemd/system/sshd.service.d/50-omega-tail.conf"
    assert commands[2:] == [("sudo", "systemctl", "daemon-reload"),
                            ("sudo", "systemctl", "restart", "tailscaled.service")]
    assert "CPUQuota=100%" in Path(source).read_text()
    assert all("override.conf" not in " ".join(command) for command in commands)
    undo = survival.unconfine_commands(restart=False, ssh_unit="")
    assert undo == [("sudo", "rm", "-f", DROP_IN_PATH), ("sudo", "systemctl", "daemon-reload")]


def test_cut_alerts() -> None:
    later = (NOW + timedelta(minutes=10)).isoformat()
    timed = alerts_for(snapshot(cut=Cut("x", NOW.isoformat(), later)), NOW)
    assert [(a.code, a.level, a.target) for a in timed] == [("funnel-cut", Level.INFO, Target.SURVIVAL)]
    overdue = alerts_for(snapshot(cut=Cut("x", NOW.isoformat(), later)), NOW + timedelta(minutes=30))
    assert overdue[0].code == "funnel-restore-overdue" and overdue[0].level is Level.WARNING
    total = alerts_for(snapshot(cut=Cut("x", NOW.isoformat())), datetime(2026, 11, 23, tzinfo=timezone.utc))
    assert total[0].code == "funnel-cut-total"
