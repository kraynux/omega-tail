# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Etat d'un service sous OpenRC et runit (systemd : systemd.py), sans droits. Le confinement hors systemd est un
groupe de controle cgroup v2 (`/sys/fs/cgroup/omega-tail-tailscaled`) : il est lu dans /proc/<pid>/cgroup."""
from __future__ import annotations

from pathlib import Path

from omega_tail.domain.init import CGROUP_NAME, CGROUP_ROOT, InitSystem
from omega_tail.domain.service import ServiceState
from omega_tail.infrastructure.commands import run_quiet
from omega_tail.infrastructure.system.init_detect import runit_service_dir
from omega_tail.infrastructure.system.machine import find_pid


def _read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def cgroup_of(pid: int, proc: Path = Path("/proc")) -> str:
    """Chemin cgroup v2 du processus (« 0::/omega-tail-tailscaled » -> « /omega-tail-tailscaled »)."""
    for line in _read(proc / str(pid) / "cgroup").splitlines():
        if line.startswith("0::"):
            return line[3:].strip()
    return ""


def cgroup_confinement(pid: int, proc: Path = Path("/proc"), root: Path = Path(CGROUP_ROOT)) -> tuple[str, str, bool]:
    """(plafond cpu.max, poids, perdu) du confinement d'omega-tail hors systemd."""
    ours = root / CGROUP_NAME
    if pid and cgroup_of(pid, proc) == f"/{CGROUP_NAME}":
        quota, period = (_read(ours / "cpu.max").split() + ["", ""])[:2]
        shown = "infinity" if quota in ("", "max") else f"{int(quota) * 100 // max(int(period or 100000), 1)}%"
        return shown, _read(ours / "cpu.weight").strip(), False
    return "infinity", "", ours.is_dir()


def _first_existing(names: tuple[str, ...], folder: Path) -> str:
    return next((name for name in names if (folder / name).exists()), names[0])


class OpenrcService:
    def __init__(self, names: tuple[str, ...], root: Path = Path("/"), process: str = "tailscaled") -> None:
        self._name = _first_existing(names, root / "etc" / "init.d")
        self._root, self._process = root, process

    def state(self) -> ServiceState:
        name, root = self._name, self._root
        if not (root / "etc" / "init.d" / name).exists():
            return ServiceState(known=False, init=InitSystem.OPENRC.value, name=name)
        output = run_quiet(["rc-service", name, "status"])
        text = (output.stdout + output.stderr).lower()
        active = "active" if "started" in text else "failed" if "crashed" in text else "inactive"
        enabled = "enabled" if any((runlevel / name).is_symlink() or (runlevel / name).exists()
                                   for runlevel in (root / "etc" / "runlevels").glob("*")) else "disabled"
        pid = find_pid(self._process)
        quota, weight, lost = cgroup_confinement(pid)
        return ServiceState(known=True, active=active, sub=active, enabled=enabled, main_pid=pid,
                            exec_start=f"/etc/init.d/{name}", fragment_path=f"/etc/init.d/{name}",
                            cpu_quota=quota, cpu_weight=weight, init=InitSystem.OPENRC.value, name=name,
                            confinement_lost=lost)


class RunitService:
    def __init__(self, names: tuple[str, ...], root: Path = Path("/"), process: str = "tailscaled") -> None:
        self._name = _first_existing(names, root / "etc" / "sv")
        self._root, self._process = root, process

    def state(self) -> ServiceState:
        name, root = self._name, self._root
        definition = root / "etc" / "sv" / name
        if not definition.exists():
            return ServiceState(known=False, init=InitSystem.RUNIT.value, name=name)
        link = root / runit_service_dir(root).lstrip("/") / name
        enabled = link.is_symlink() or link.exists()
        pid = find_pid(self._process)
        output = run_quiet(["sv", "status", name])
        text = output.stdout.strip()
        if text.startswith("run:"):
            active = "active"
        elif text.startswith(("down:", "fail:")):
            active = "inactive"
        else:  # statut reserve a root sur certaines distributions : le processus fait foi
            active = "active" if pid else "inactive"
        quota, weight, lost = cgroup_confinement(pid)
        return ServiceState(known=True, active=active, sub=active, enabled="enabled" if enabled else "disabled",
                            main_pid=pid, exec_start=str(definition / "run"), fragment_path=str(definition),
                            cpu_quota=quota, cpu_weight=weight, init=InitSystem.RUNIT.value, name=name,
                            confinement_lost=lost)


def service_reader(init: InitSystem, names: tuple[str, ...], process: str) -> object:
    """Lecteur d'etat du service selon le systeme d'init (port ServiceReader)."""
    from omega_tail.infrastructure.system.systemd import SystemdService

    if init is InitSystem.OPENRC:
        return OpenrcService(names, process=process)
    if init is InitSystem.RUNIT:
        return RunitService(names, process=process)
    return SystemdService(names[0])
