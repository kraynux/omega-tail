# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Bouclier du port WireGuard cote machine (ports/shield.py) : lectures d'omega-lib (sans droits), omega-fire
trouve par le registre d'omega-connect (meme methode qu'omega-stress), fichiers prepares dans var/bouclier-wg."""
from __future__ import annotations

import os
import re
from pathlib import Path

from omega_lib.infrastructure.shield.machine import (
    kernel_modules_ready,
    kernel_release,
    physical_devices,
    read_settings,
    read_status,
    tailscaled_port,
)
from omega_lib.shield.models import ShieldSettings, ShieldStatus

from omega_tail.domain.shield import OMEGA_FIRE, FireLink

REQUESTED_NAME = "demande"
_VERSION = re.compile(r'^version\s*=\s*"([^"]+)"', re.MULTILINE)


def omega_fire_link() -> FireLink:
    """omega-fire relie par omega-connect (espace partage actif) : lanceur et version (pyproject.toml, seule
    source). Jamais d'exception : registre illisible ou omega-lib ancien = pas d'omega-fire."""
    try:
        from omega_lib.infrastructure.synchro.files import read_contract, zone_dir
        from omega_lib.synchro.constants import TOOL_LAUNCHERS, ZONE_REGISTRY
        from omega_lib.synchro.registry import ZoneState, registry_from_dict

        registry = read_contract(zone_dir() / ZONE_REGISTRY, registry_from_dict).value
        if registry is None or registry.state is not ZoneState.ACTIVE:
            return FireLink()
        fire = next((entry for entry in registry.installations if entry.tool == OMEGA_FIRE), None)
        if fire is None:
            return FireLink()
        launcher = Path(fire.root) / TOOL_LAUNCHERS[OMEGA_FIRE]
        if not launcher.is_file() or launcher.is_symlink():
            return FireLink()
        try:
            found = _VERSION.search((Path(fire.root) / "pyproject.toml").read_text(encoding="utf-8"))
        except OSError:
            found = None
        return FireLink(str(launcher), found.group(1) if found else "")
    except Exception:  # noqa: BLE001 - registre illisible : pas d'omega-fire
        return FireLink()


class ShieldSystem:
    def __init__(self, folder: Path) -> None:
        self._folder = folder

    def settings(self) -> ShieldSettings | None:
        return read_settings()

    def status(self) -> ShieldStatus | None:
        return read_status()

    def tailscaled_port(self) -> int:
        return tailscaled_port()

    def devices(self) -> tuple[str, ...]:
        return physical_devices()

    def kernel_release(self) -> str:
        return kernel_release()

    def modules_ready(self) -> bool:
        return kernel_modules_ready()

    def fire(self) -> FireLink:
        return omega_fire_link()

    def _ready(self) -> Path:
        self._folder.mkdir(parents=True, exist_ok=True)
        os.chmod(self._folder, 0o700)
        return self._folder

    def stage(self, files: dict[str, str]) -> str:
        folder = self._ready()
        for name, content in files.items():
            temporary = folder / f".{name}.tmp"
            temporary.write_text(content, encoding="utf-8")
            temporary.replace(folder / name)
        return str(folder)

    def requested(self) -> bool:
        return (self._folder / REQUESTED_NAME).is_file()

    def set_requested(self, requested: bool) -> None:
        path = self._ready() / REQUESTED_NAME
        if requested:
            path.write_text("omega-tail a demande le bouclier du port WireGuard\n", encoding="utf-8")
        else:
            path.unlink(missing_ok=True)
