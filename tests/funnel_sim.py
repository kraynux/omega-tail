# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Simulateur de `tailscale funnel` / `serve status --json`, fidele a ce qui a ete constate sur le J3455
(Tailscale 1.104.5, 2026-11-22) : « --https=PORT off » retire tous les chemins du port et son autorisation
Funnel ; « --tcp=PORT off » retire le port mais laisse l'autorisation (sans effet : rien n'est servi)."""
from __future__ import annotations

import copy
from collections.abc import Sequence
from typing import Any

HOST = "kraynux.tailnet-exemple.ts.net"


class FunnelSim:
    def __init__(self, config: dict[str, Any], *, fail_on: str = "") -> None:
        self.config = copy.deepcopy(config)
        self.fail_on = fail_on
        self.calls: list[tuple[str, ...]] = []

    def serve_config(self) -> dict[str, Any]:
        return copy.deepcopy(self.config)

    def quiet(self, argv: Sequence[str]) -> tuple[int, str]:
        command = tuple(argv)
        self.calls.append(command)
        if self.fail_on and self.fail_on in " ".join(command):
            return 1, "Access denied: serve config denied"
        if command[1:] == ("serve", "reset"):
            self.config = {}
            return 0, ""
        public = command[1] == "funnel"
        flags = {part.split("=", 1)[0][2:]: part.split("=", 1)[1] for part in command if part.startswith("--")
                 and "=" in part}
        kind = next(key for key in ("https", "http", "tcp", "tls-terminated-tcp") if key in flags)
        port = flags[kind]
        tcp = self.config.setdefault("TCP", {})
        web = self.config.setdefault("Web", {})
        allow = self.config.setdefault("AllowFunnel", {})
        if command[-1] == "off" and "set-path" in flags:  # un seul chemin du port
            for key in [key for key in web if key.endswith(f":{port}")]:
                web[key].get("Handlers", {}).pop(flags["set-path"], None)
                if not web[key].get("Handlers"):
                    web.pop(key)
            if not any(key.endswith(f":{port}") for key in web):
                tcp.pop(port, None)
        elif command[-1] == "off":
            tcp.pop(port, None)
            for key in [key for key in web if key.endswith(f":{port}")]:
                web.pop(key)
            if kind in ("https", "http"):  # constate 2026-11-22 : « --tcp=PORT off » laisse AllowFunnel
                for key in [key for key in allow if key.endswith(f":{port}")]:
                    allow.pop(key)
        else:
            target = command[-1]
            if kind in ("https", "http"):
                tcp[port] = {"HTTPS": True} if kind == "https" else {"HTTP": True}
                handlers = web.setdefault(f"{HOST}:{port}", {}).setdefault("Handlers", {})
                handlers[flags.get("set-path", "/")] = {"Proxy": target}
            else:
                entry: dict[str, Any] = {"TCPForward": target.removeprefix("tcp://")}
                if kind == "tls-terminated-tcp":
                    entry["TerminateTLS"] = HOST
                if "proxy-protocol" in flags:
                    entry["ProxyProtocol"] = int(flags["proxy-protocol"])
                tcp[port] = entry
            if public:  # « serve » ne touche pas l'autorisation Funnel (une ancienne peut rester)
                allow[f"{HOST}:{port}"] = True
        for key in ("TCP", "Web", "AllowFunnel"):
            if not self.config.get(key):
                self.config.pop(key, None)
        return 0, ""
