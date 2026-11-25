# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Etat du service `tailscaled` par `systemctl show` (lecture, sans droits)."""
from __future__ import annotations

import re

from omega_tail.core.constants import TAILSCALED_UNIT
from omega_tail.domain.service import ServiceState
from omega_tail.infrastructure.commands import run_quiet

PROPERTIES = ("Id", "LoadState", "ActiveState", "SubState", "UnitFileState", "ActiveEnterTimestamp", "MainPID",
              "MemoryCurrent", "ExecStart", "FragmentPath", "DropInPaths", "CPUQuotaPerSecUSec", "CPUWeight",
              "AllowedCPUs", "Nice", "ExecStartPre", "ExecStartPost")
_ARGV = re.compile(r"argv\[\]=([^;]*)")
_ENTRY = re.compile(r"\{([^{}]*)\}")
HOOKS = ("ExecStartPre", "ExecStartPost")


def _failing_hooks(lines: list[str]) -> tuple[str, ...]:
    """Commandes de demarrage dont l'echec arrete le service (ignore_errors=no)."""
    found: list[str] = []
    for line in lines:
        for entry in _ENTRY.findall(line):
            argv = _ARGV.search(entry)
            if argv and "ignore_errors=yes" not in entry:
                found.append(argv.group(1).strip())
    return tuple(found)


def parse_show(text: str) -> ServiceState:
    values: dict[str, str] = {}
    hooks: list[str] = []
    for line in text.splitlines():
        key, sep, value = line.partition("=")
        if sep:
            values[key] = value
            if key in HOOKS:
                hooks.append(value)
    if values.get("LoadState", "not-found") == "not-found":
        return ServiceState(known=False)
    memory = values.get("MemoryCurrent", "")
    argv = _ARGV.search(values.get("ExecStart", ""))
    return ServiceState(
        known=True, active=values.get("ActiveState", ""), sub=values.get("SubState", ""),
        enabled=values.get("UnitFileState", ""), since=values.get("ActiveEnterTimestamp", ""),
        main_pid=int(values["MainPID"]) if values.get("MainPID", "").isdigit() else 0,
        memory_bytes=int(memory) if memory.isdigit() else None,
        exec_start=argv.group(1).strip() if argv else "",
        fragment_path=values.get("FragmentPath", ""),
        drop_ins=tuple(path for path in values.get("DropInPaths", "").split() if path),
        cpu_quota=values.get("CPUQuotaPerSecUSec", ""), cpu_weight=values.get("CPUWeight", ""),
        allowed_cpus=values.get("AllowedCPUs", ""), nice=values.get("Nice", ""), init="systemd",
        name=values.get("Id", ""), start_hooks=_failing_hooks(hooks))


class SystemdService:
    def __init__(self, unit: str = TAILSCALED_UNIT) -> None:
        self._unit = unit

    def state(self) -> ServiceState:
        output = run_quiet(["systemctl", "show", self._unit, "--no-pager", "-p", ",".join(PROPERTIES)])
        if output.code == 127:
            return ServiceState(known=False, error="systemctl: not found")
        if output.code != 0:
            return ServiceState(known=False, error=output.last_error)
        return parse_show(output.stdout)


def first_loaded(units: tuple[str, ...]) -> str:
    """Premier service connu de systemd parmi `units` (service SSH : sshd ou ssh) ; vide si aucun."""
    for unit in units:
        output = run_quiet(["systemctl", "show", unit, "--no-pager", "-p", "LoadState"])
        if output.code == 0 and output.stdout.strip() == "LoadState=loaded":
            return unit
    return ""
