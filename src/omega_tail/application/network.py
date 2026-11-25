# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Reseau et appareils (lot 7, proposition §3.5) : lectures seules, sans droits. Le nom ou l'adresse tape pour un
ping ou un whois est verifie avant d'etre passe a `tailscale` (jamais une option)."""
from __future__ import annotations

from dataclasses import dataclass

from omega_tail.domain.network import Device, Metrics, Netcheck, valid_target
from omega_tail.ports.readers import NetworkReader


@dataclass(frozen=True)
class DeviceList:
    devices: tuple[Device, ...] = ()
    error: str = ""


@dataclass(frozen=True)
class NetworkTools:
    reader: NetworkReader

    def devices(self) -> DeviceList:
        try:
            return DeviceList(self.reader.devices())
        except OSError as error:
            return DeviceList(error=str(error))

    def netcheck(self) -> Netcheck:
        return self.reader.netcheck()

    def dns(self) -> tuple[str, str]:
        return self.reader.text("dns", "status")

    def lock(self) -> tuple[str, str]:
        return self.reader.text("lock", "status")

    def metrics(self) -> Metrics:
        return self.reader.metrics()

    def ping(self, target: str) -> tuple[bool, str]:
        """(accepte, texte) : refus si le nom ou l'adresse n'est pas valable."""
        target = target.strip()
        if not valid_target(target):
            return False, target
        return True, self.reader.ping(target)

    def whois(self, target: str) -> tuple[bool, str]:
        target = target.strip()
        if not valid_target(target):
            return False, target
        return True, self.reader.whois(target)
