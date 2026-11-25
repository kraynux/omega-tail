# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Processeur, charge, temperature, memoire et consommation de tailscaled, lus dans /proc et /sys (sans droits)."""
from __future__ import annotations

import os
import socket
import time
from pathlib import Path

from omega_tail.domain.machine import MachineState

CLOCK_TICKS = os.sysconf("SC_CLK_TCK") if hasattr(os, "sysconf") else 100


def _read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def process_ticks(stat_text: str) -> int | None:
    """utime + stime de /proc/<pid>/stat (le nom du processus peut contenir des espaces : lu apres « ) »)."""
    _head, sep, rest = stat_text.rpartition(")")
    fields = rest.split()
    if not sep or len(fields) < 13:
        return None
    try:
        return int(fields[11]) + int(fields[12])
    except ValueError:
        return None


def max_temperature(sys_root: Path = Path("/sys")) -> float | None:
    values: list[float] = []
    for pattern in ("class/hwmon/hwmon*/temp*_input", "class/thermal/thermal_zone*/temp"):
        for path in sys_root.glob(pattern):
            text = _read(path).strip()
            if text.lstrip("-").isdigit():
                celsius = int(text) / 1000
                if 0 < celsius < 150:
                    values.append(celsius)
    return max(values) if values else None


def memory(meminfo_text: str) -> tuple[int | None, int | None]:
    """(MemTotal, MemAvailable) de /proc/meminfo, en octets."""
    values: dict[str, int] = {}
    for line in meminfo_text.splitlines():
        key, _sep, rest = line.partition(":")
        fields = rest.split()
        if fields and fields[0].isdigit():
            values[key] = int(fields[0]) * 1024
    return values.get("MemTotal"), values.get("MemAvailable")


def cpu_times(stat_text: str) -> tuple[int, int] | None:
    """(total, inactif) de la ligne « cpu » de /proc/stat ; inactif = idle + iowait."""
    for line in stat_text.splitlines():
        if line.startswith("cpu "):
            try:
                values = [int(value) for value in line.split()[1:]]
            except ValueError:
                return None
            if len(values) < 4:
                return None
            idle = values[3] + (values[4] if len(values) > 4 else 0)
            return sum(values[:8]), idle
    return None


def find_pid(name: str = "tailscaled", proc: Path = Path("/proc")) -> int:
    for entry in proc.iterdir():
        if entry.name.isdigit() and _read(entry / "comm").strip() == name:
            return int(entry.name)
    return 0


class ProcMachine:
    """Garde la lecture precedente pour calculer le % CPU de la machine et de tailscaled entre deux lectures."""

    def __init__(self, proc: Path = Path("/proc"), sys_root: Path = Path("/sys")) -> None:
        self._proc, self._sys = proc, sys_root
        self._last: tuple[int, float, int] | None = None
        self._last_cpu: tuple[int, int] | None = None

    def state(self, tailscaled_pid: int) -> MachineState:
        pid = tailscaled_pid or find_pid(proc=self._proc)
        cpu, rss = None, None
        if pid:
            ticks = process_ticks(_read(self._proc / str(pid) / "stat"))
            now = time.monotonic()
            if ticks is not None:
                if self._last is not None and self._last[0] == pid and now > self._last[1]:
                    cpu = max(0.0, 100 * (ticks - self._last[2]) / CLOCK_TICKS / (now - self._last[1]))
                self._last = (pid, now, ticks)
            for line in _read(self._proc / str(pid) / "status").splitlines():
                if line.startswith("VmRSS:") and line.split()[1].isdigit():
                    rss = int(line.split()[1]) * 1024
        machine_cpu = None
        times = cpu_times(_read(self._proc / "stat"))
        if times is not None:
            if self._last_cpu is not None and times[0] > self._last_cpu[0]:
                spent = times[0] - self._last_cpu[0]
                machine_cpu = max(0.0, min(100.0, 100 * (spent - (times[1] - self._last_cpu[1])) / spent))
            self._last_cpu = times
        load_fields = _read(self._proc / "loadavg").split()
        try:
            load = (float(load_fields[0]), float(load_fields[1]), float(load_fields[2]))
        except (IndexError, ValueError):
            load = (0.0, 0.0, 0.0)
        total, available = memory(_read(self._proc / "meminfo"))
        return MachineState(hostname=(socket.gethostname() or "").split(".")[0], cpu_count=os.cpu_count() or 0,
                            load=load, temperature_c=max_temperature(self._sys), cpu_percent=machine_cpu,
                            tailscaled_cpu_percent=cpu,
                            tailscaled_rss_bytes=rss, memory_total_bytes=total,
                            memory_available_bytes=available)
