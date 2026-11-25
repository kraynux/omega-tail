# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Detection du systeme d'init, reprise d'omega-serv (infrastructure/services/detector.py, lui-meme porte depuis
omega-fire) : /proc/1/comm, puis binaires, puis dossiers."""
from __future__ import annotations

import shutil
from pathlib import Path

from omega_tail.domain.init import InitSystem


def detect_init(proc_root: Path = Path("/proc"), root: Path = Path("/")) -> InitSystem:
    try:
        name = (proc_root / "1" / "comm").read_text(encoding="utf-8").strip()
    except OSError:
        name = ""
    by_name = {"systemd": InitSystem.SYSTEMD, "openrc-init": InitSystem.OPENRC, "openrc": InitSystem.OPENRC,
               "runit": InitSystem.RUNIT, "runsvdir": InitSystem.RUNIT}
    if name in by_name:
        return by_name[name]
    if (root / "run" / "systemd" / "system").exists():
        return InitSystem.SYSTEMD
    if shutil.which("rc-service") is not None or (root / "run" / "openrc").exists():
        return InitSystem.OPENRC
    if shutil.which("sv") is not None and ((root / "etc" / "sv").exists() or (root / "etc" / "runit").exists()):
        return InitSystem.RUNIT
    if shutil.which("systemctl") is not None:
        return InitSystem.SYSTEMD
    return InitSystem.NONE


def runit_service_dir(root: Path = Path("/")) -> str:
    """Dossier des services actifs de runit selon la distribution (Void : /var/service ; Artix : /run/runit/service ;
    autres : /etc/service, /service)."""
    for candidate in ("var/service", "run/runit/service", "etc/service", "service"):
        if (root / candidate).is_dir():
            return "/" + candidate
    return "/var/service"
