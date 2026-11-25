# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""systemd, OpenRC, runit (regle de la suite, rappel le 2026-11-23). Pas de machine OpenRC ni runit
dans le parc : sorties de rc-service et de sv simulees, arborescences factices."""
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import pytest
from conftest import NOW, service_state, snapshot
from funnel_sim import FunnelSim
from test_gate import PRODUCTION, FakeMachine
from test_gate import gate as make_gate

from omega_tail.application.actions import service_command
from omega_tail.application.survival import SurvivalTools
from omega_tail.domain.alerts import alerts_for
from omega_tail.domain.confinement import recommended
from omega_tail.domain.gate import CRON_MARKER, cron_line, openrc_script, runit_run_script
from omega_tail.domain.init import InitSystem
from omega_tail.domain.service import ServiceAction
from omega_tail.infrastructure import commands
from omega_tail.infrastructure.survival_store import FileCutStore
from omega_tail.infrastructure.system import init_detect, services
from omega_tail.infrastructure.system.journal import FileJournal, journal_files


def test_detection_order(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    proc = tmp_path / "proc"
    (proc / "1").mkdir(parents=True)
    monkeypatch.setattr(init_detect.shutil, "which", lambda name: None)
    for comm, expected in (("systemd", InitSystem.SYSTEMD), ("openrc-init", InitSystem.OPENRC),
                           ("runit", InitSystem.RUNIT)):
        (proc / "1" / "comm").write_text(comm + "\n")
        assert init_detect.detect_init(proc, tmp_path) is expected
    (proc / "1" / "comm").write_text("init\n")  # sysvinit + openrc (Gentoo, Alpine) : dossier /run/openrc
    (tmp_path / "run" / "openrc").mkdir(parents=True)
    assert init_detect.detect_init(proc, tmp_path) is InitSystem.OPENRC
    (tmp_path / "var" / "service").mkdir(parents=True)
    assert init_detect.runit_service_dir(tmp_path) == "/var/service"


def test_service_commands_per_init() -> None:
    assert service_command(ServiceAction.RESTART) == ("sudo", "systemctl", "restart", "tailscaled.service")
    assert service_command(ServiceAction.RESTART, init=InitSystem.OPENRC, name="tailscale") == (
        "sudo", "rc-service", "tailscale", "restart")
    assert service_command(ServiceAction.STOP, init=InitSystem.RUNIT, name="tailscaled", as_root=True) == (
        "sv", "down", "tailscaled")
    assert service_command(ServiceAction.START, init=InitSystem.RUNIT)[-2:] == ("up", "tailscaled")


def fake_quiet(outputs: dict[str, tuple[int, str]]):  # type: ignore[no-untyped-def]
    def run(argv, **_kwargs):  # type: ignore[no-untyped-def]
        code, text = outputs.get(argv[0], (127, ""))
        return commands.Output(code, text, "")
    return run


def test_openrc_state(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    (tmp_path / "etc" / "init.d").mkdir(parents=True)
    (tmp_path / "etc" / "init.d" / "tailscale").write_text("#!/sbin/openrc-run\n")
    (tmp_path / "etc" / "runlevels" / "default").mkdir(parents=True)
    (tmp_path / "etc" / "runlevels" / "default" / "tailscale").symlink_to("/etc/init.d/tailscale")
    monkeypatch.setattr(services, "run_quiet", fake_quiet({"rc-service": (0, " * status: started\n")}))
    monkeypatch.setattr(services, "find_pid", lambda name: 4242)
    monkeypatch.setattr(services, "cgroup_confinement", lambda pid: ("infinity", "", False))
    state = services.OpenrcService(("tailscale", "tailscaled"), root=tmp_path).state()
    assert (state.known, state.running, state.enabled, state.name, state.init) == (True, True, "enabled",
                                                                                   "tailscale", "openrc")
    monkeypatch.setattr(services, "run_quiet", fake_quiet({"rc-service": (3, " * status: stopped\n")}))
    assert not services.OpenrcService(("tailscale",), root=tmp_path).state().running


def test_runit_state(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    (tmp_path / "etc" / "sv" / "tailscaled").mkdir(parents=True)
    (tmp_path / "var" / "service").mkdir(parents=True)
    (tmp_path / "var" / "service" / "tailscaled").symlink_to(tmp_path / "etc" / "sv" / "tailscaled")
    monkeypatch.setattr(services, "find_pid", lambda name: 77)
    monkeypatch.setattr(services, "cgroup_confinement", lambda pid: ("100%", "50", False))
    monkeypatch.setattr(services, "run_quiet", fake_quiet(
        {"sv": (0, "run: tailscaled: (pid 77) 3600s; run: log: (pid 70) 3600s\n")}))
    state = services.RunitService(("tailscaled",), root=tmp_path).state()
    assert state.running and state.enabled == "enabled" and state.confined
    monkeypatch.setattr(services, "run_quiet", fake_quiet({"sv": (1, "warning: tailscaled: unable to open "
                                                                        "supervise/ok: access denied\n")}))
    assert services.RunitService(("tailscaled",), root=tmp_path).state().running  # le processus fait foi


def test_cgroup_reading(tmp_path: Path) -> None:
    proc, root = tmp_path / "proc", tmp_path / "cg"
    (proc / "5").mkdir(parents=True)
    (root / "omega-tail-tailscaled").mkdir(parents=True)
    (root / "omega-tail-tailscaled" / "cpu.max").write_text("100000 100000\n")
    (root / "omega-tail-tailscaled" / "cpu.weight").write_text("50\n")
    (proc / "5" / "cgroup").write_text("0::/omega-tail-tailscaled\n")
    assert services.cgroup_confinement(5, proc, root) == ("100%", "50", False)
    (proc / "5" / "cgroup").write_text("0::/openrc.tailscale\n")  # tailscaled redemarre : sorti du groupe
    assert services.cgroup_confinement(5, proc, root) == ("infinity", "", True)


def survival(tmp_path: Path, init: InitSystem, spawned: list[tuple[str, ...]]) -> SurvivalTools:
    sim = FunnelSim(PRODUCTION)
    return SurvivalTools(store=FileCutStore(tmp_path / "var"), serve_config=sim.serve_config, quiet=sim.quiet,
                         now=lambda: NOW, python="/opt/ot/python", user=lambda: "kraynux", init=init,
                         spawn=lambda argv: spawned.append(tuple(argv)) or 0)


def test_confinement_without_systemd_is_a_cgroup(tmp_path: Path) -> None:
    tools = survival(tmp_path, InitSystem.OPENRC, [])
    commands_ = tools.confine_commands(recommended(4), restart=True, ssh_unit="sshd.service", pid=4242)
    script = commands_[0][-1]
    assert commands_[0][:3] == ("sudo", "sh", "-c") and "echo '100000 100000' > /sys/fs/cgroup/omega-tail-tailscaled" \
        "/cpu.max" in script and "echo 4242 > /sys/fs/cgroup/omega-tail-tailscaled/cgroup.procs" in script
    assert commands_[1] == ("sudo", "renice", "-n", "5", "-p", "4242")
    assert not any("/etc/" in part for command in commands_ for part in command)  # aucun fichier de l'utilisateur
    assert tools.confine_commands(recommended(4), restart=False, pid=0) == []
    undo = tools.unconfine_commands(restart=False, pid=4242)
    assert "echo 4242 > /sys/fs/cgroup/cgroup.procs" in undo[0][-1] and undo[1][-1] == "4242"


def test_timed_cut_without_systemd_is_a_detached_user_process(tmp_path: Path) -> None:
    spawned: list[tuple[str, ...]] = []
    tools = survival(tmp_path, InitSystem.RUNIT, spawned)
    outcome = tools.cut(10, schedule=lambda command: pytest.fail("pas de sudo hors systemd"), cut_id="c1")
    assert outcome.ok and spawned == [("/opt/ot/python", "-m", "omega_tail", "disjoncteur", "retablir", "--id",
                                       "c1", "--attendre", "600")]


class CronMachine(FakeMachine):
    def __init__(self) -> None:
        super().__init__()
        self.crontab: dict[str, str] = {}

    def set_cron(self, marker: str, line: str) -> tuple[bool, str]:
        if line:
            self.crontab[marker] = line
        else:
            self.crontab.pop(marker, None)
        return True, ""


def test_gate_services_per_init(tmp_path: Path) -> None:
    for init in (InitSystem.OPENRC, InitSystem.RUNIT):
        machine = CronMachine()
        tools = make_gate(tmp_path / init.value, FunnelSim(PRODUCTION), machine=machine)
        tools.init = init
        assert tools.prepare().ok
        assert machine.crontab[CRON_MARKER].endswith(f"porte certificat --si-besoin >/dev/null 2>&1 {CRON_MARKER}")
        steps = tools.service_commands()
        if init is InitSystem.OPENRC:
            assert steps[0][-1] == "/etc/init.d/omega-tail-porte" and steps[1][1:] == ("rc-update", "add",
                                                                                         "omega-tail-porte", "default")
            assert "command_user=\"kraynux\"" in (tools.folder / "omega-tail-porte.openrc").read_text()
        else:
            assert steps[0][-1] == "/etc/sv/omega-tail-porte/run" and steps[2][1:] == (
                "ln", "-sfn", "/etc/sv/omega-tail-porte", "/var/service/omega-tail-porte")
            assert (tools.folder / "log").is_dir()
        tools.stop_commands()
        assert CRON_MARKER not in machine.crontab


def test_scripts_run_as_the_user_in_foreground() -> None:
    script = openrc_script(user="kraynux", haproxy="/usr/sbin/haproxy", folder="/home/k/ot/var/porte")
    assert script.startswith("#!/sbin/openrc-run") and 'supervisor="supervise-daemon"' in script
    assert "-W -db -f /home/k/ot/var/porte/haproxy.cfg" in script
    run = runit_run_script(user="kraynux", haproxy="/usr/bin/haproxy", folder="/v/porte")
    assert "exec chpst -u kraynux" in run and "-W -db" in run
    assert cron_line("/p/python").startswith("17 4 * * * /p/python -m omega_tail porte certificat --si-besoin")


def test_file_journal(tmp_path: Path) -> None:
    log = tmp_path / "messages"
    log.write_text("a tailscaled: ok\nb other: x\nc tailscaled: error\n")
    journal = FileJournal({"tailscaled": [(str(tmp_path / "absent"), ""), (str(log), "tailscale")]})
    assert journal.read("tailscaled", 10).lines == ("a tailscaled: ok", "c tailscaled: error")
    assert journal.read("tailscaled", 1).lines == ("c tailscaled: error",)
    assert "aucun journal" in FileJournal({"porte": [("/n/a", "")]}).read("porte", 5).error
    assert journal_files("/v/porte")["porte"][0] == ("/v/porte/porte.log", "")


def test_confinement_lost_alert() -> None:
    lost = snapshot(service=service_state(init="openrc", name="tailscale", confinement_lost=True))
    codes = [alert.code for alert in alerts_for(lost, datetime(2026, 11, 23, tzinfo=timezone.utc))]
    assert "confinement-lost" in codes and "not-confined" not in codes


def test_install_command_knows_more_package_managers(monkeypatch: pytest.MonkeyPatch) -> None:
    from omega_tail.infrastructure import gate as gate_infra

    for manager, expected in (("apk", ("apk", "add", "haproxy")), ("xbps-install", ("xbps-install", "-y", "haproxy")),
                              ("emerge", ("emerge", "--ask=n", "net-proxy/haproxy"))):
        monkeypatch.setattr(gate_infra.shutil, "which", lambda name, wanted=manager: f"/x/{name}" if name == wanted
                            else None)
        monkeypatch.setattr(gate_infra.os, "geteuid", lambda: 1000)
        assert gate_infra.GateSystem().install_command() == ("sudo", *expected)
