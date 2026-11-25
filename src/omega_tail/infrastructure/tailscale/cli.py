# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Lectures par le client `tailscale` (status, get, serve status, version, exit-node list, netcheck, dns status,
lock status, metrics, ping, whois : sans droits ; switch --list : operateur)."""
from __future__ import annotations

import json
import shutil
from typing import Any

from omega_tail.core.constants import TAILSCALE_COMMAND
from omega_tail.domain.network import Device, Metrics, Netcheck, parse_metrics, parse_netcheck
from omega_tail.domain.tailscale import ExitNode, Preferences, Profile, Publication, TailscaleState
from omega_tail.infrastructure.commands import run_quiet
from omega_tail.infrastructure.tailscale.parsing import (
    parse_devices,
    parse_exit_nodes,
    parse_preferences,
    parse_profiles,
    parse_serve,
    parse_status,
    short_version,
)

NETCHECK_TIMEOUT_SECONDS = 40
TEXT_LIMIT_BYTES = 256 * 1024


class TailscaleCli:
    def __init__(self, command: str = TAILSCALE_COMMAND) -> None:
        self._command = command
        self._dns_name = ""

    def installed(self) -> bool:
        return shutil.which(self._command) is not None

    def state(self) -> TailscaleState:
        if not self.installed():
            return TailscaleState(installed=False, reachable=False)
        version = run_quiet([self._command, "version"])
        client = short_version(version.stdout) if version.code == 0 else ""
        status = run_quiet([self._command, "status", "--json"])
        if status.code != 0:
            return TailscaleState(installed=True, reachable=False, client_version=client,
                                  error=status.last_error)
        try:
            data = json.loads(status.stdout)
        except ValueError:
            return TailscaleState(installed=True, reachable=False, client_version=client,
                                  error="tailscale status: invalid JSON")
        state = parse_status(data if isinstance(data, dict) else {}, client)
        self._dns_name = state.dns_name
        return state

    def preferences(self) -> Preferences:
        if not self.installed():
            return Preferences()
        output = run_quiet([self._command, "get"])
        return parse_preferences(output.stdout) if output.code == 0 else Preferences()

    def serve_config(self) -> dict[str, Any]:
        """Publication brute (`serve status --json`) : sauvegardee avant une coupure de Funnel."""
        output = run_quiet([self._command, "serve", "status", "--json"])
        if output.code != 0:
            raise OSError(output.last_error or "tailscale serve status")
        data = json.loads(output.stdout or "{}")
        return data if isinstance(data, dict) else {}

    def publications(self) -> tuple[Publication, ...]:
        if not self.installed():
            return ()
        output = run_quiet([self._command, "serve", "status", "--json"])
        if output.code != 0:
            return ()
        try:
            data = json.loads(output.stdout or "{}")
        except ValueError:
            return ()
        return parse_serve(data if isinstance(data, dict) else {}, self._dns_name)

    def profiles(self) -> tuple[tuple[Profile, ...], str]:
        """Comptes connus ; sinon (aucun, phrase d'erreur de Tailscale : « Access denied » sans operateur)."""
        output = run_quiet([self._command, "switch", "--list"])
        if output.code != 0:
            return (), output.stderr.strip().splitlines()[0] if output.stderr.strip() else "tailscale switch"
        return parse_profiles(output.stdout), ""

    def exit_nodes(self) -> tuple[ExitNode, ...]:
        output = run_quiet([self._command, "exit-node", "list"])
        return parse_exit_nodes(output.stdout) if output.code == 0 else ()

    # ---- reseau et appareils (lot 7) ----
    def devices(self) -> tuple[Device, ...]:
        output = run_quiet([self._command, "status", "--json"])
        if output.code != 0:
            raise OSError(output.last_error or "tailscale status")
        try:
            data = json.loads(output.stdout or "{}")
        except ValueError as error:
            raise OSError("tailscale status: invalid JSON") from error
        return parse_devices(data if isinstance(data, dict) else {})

    def netcheck(self) -> Netcheck:
        output = run_quiet([self._command, "netcheck"], timeout=NETCHECK_TIMEOUT_SECONDS)
        if output.code != 0 and not output.stdout.strip():
            return Netcheck(error=output.last_error or "tailscale netcheck")
        return parse_netcheck(output.stdout)

    def text(self, *arguments: str) -> tuple[str, str]:
        """Sortie texte d'une lecture (`dns status`, `lock status`) ; (texte, erreur)."""
        output = run_quiet([self._command, *arguments], limit=TEXT_LIMIT_BYTES)
        if output.code != 0 and not output.stdout.strip():
            return "", output.last_error or f"tailscale {' '.join(arguments)}"
        return output.stdout.strip(), ""

    def metrics(self) -> Metrics:
        output = run_quiet([self._command, "metrics", "print"], limit=TEXT_LIMIT_BYTES)
        return parse_metrics(output.stdout) if output.code == 0 else Metrics()

    def ping(self, target: str) -> str:
        """Trois essais au plus (5 s chacun) ; `target` deja verifie (domain.network.valid_target)."""
        output = run_quiet([self._command, "ping", "--c", "3", "--timeout", "5s", "--", target], timeout=25,
                           limit=TEXT_LIMIT_BYTES)
        return (output.stdout + output.stderr).strip()

    def whois(self, target: str) -> str:
        output = run_quiet([self._command, "whois", "--", target], limit=TEXT_LIMIT_BYTES)
        return (output.stdout + output.stderr).strip()
