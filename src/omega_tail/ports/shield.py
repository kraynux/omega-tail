# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""La machine vue par le bouclier du port WireGuard (lectures sans droits ; les commandes root passent par le
terminal sudo de l'interface)."""
from __future__ import annotations

from typing import Protocol

from omega_lib.shield.models import ShieldSettings, ShieldStatus

from omega_tail.domain.shield import FireLink


class ShieldMachine(Protocol):
    def settings(self) -> ShieldSettings | None: ...

    def status(self) -> ShieldStatus | None: ...

    def tailscaled_port(self) -> int: ...

    def devices(self) -> tuple[str, ...]: ...

    def kernel_release(self) -> str: ...

    def modules_ready(self) -> bool:
        """Faux : noyau mis a jour sans redemarrage, `nft_limit` ne peut plus etre charge."""
        ...

    def fire(self) -> FireLink: ...

    def stage(self, files: dict[str, str]) -> str:
        """Ecrit les fichiers prepares (var/bouclier-wg, 0700) ; rend le dossier."""
        ...

    def requested(self) -> bool: ...

    def set_requested(self, requested: bool) -> None: ...
