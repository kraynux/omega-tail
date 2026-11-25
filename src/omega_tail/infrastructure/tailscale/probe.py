# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Essai de bout en bout d'un port publie (lot 5) : une vraie connexion, comme un visiteur. Pour un port public,
l'adresse est demandee a un resolveur public (le relais Funnel, meme chemin qu'au lot 0) ; pour le tailnet seul,
l'adresse Tailscale de la machine. Le certificat presente est lu au passage (echeance, emetteur)."""
from __future__ import annotations

import socket
import ssl
import time
from datetime import datetime, timezone
from typing import Any

from omega_tail.domain.tailscale import Certificate, Probe
from omega_tail.infrastructure.gate import SOCKET_TIMEOUT, resolve_public
from omega_tail.shared.i18n import N_

PUBLIC_DNS = N_("DNS public")
"""Debut du detail d'un echec de resolution (l'ecran Publication le reconnait)."""
MODES = ("https", "http", "tls", "tcp")


def _name(parts: Any, wanted: str) -> str:
    for rdn in parts or ():
        for key, value in rdn:
            if key == wanted:
                return str(value)
    return ""


def certificate_of(tls: ssl.SSLSocket) -> Certificate:
    peer = tls.getpeercert() or {}
    not_after = None
    text = peer.get("notAfter")
    if isinstance(text, str):
        not_after = datetime.fromtimestamp(ssl.cert_time_to_seconds(text), tz=timezone.utc)
    issuer = peer.get("issuer")
    return Certificate(not_after, _name(issuer, "organizationName") or _name(issuer, "commonName"),
                       _name(peer.get("subject"), "commonName"), tls.version() or "")


def _first_line(stream: socket.socket, host: str, path: str) -> str:
    stream.sendall(f"GET {path} HTTP/1.1\r\nHost: {host}\r\nUser-Agent: omega-tail-essai\r\n"
                   "Connection: close\r\n\r\n".encode())
    return stream.recv(4096).decode(errors="replace").split("\r\n", 1)[0]


def _status_ok(line: str) -> bool:
    parts = line.split()
    return len(parts) >= 2 and parts[0].startswith("HTTP/") and parts[1].isdigit() and int(parts[1]) < 500


def probe(host: str, port: int, address: str, mode: str, path: str = "/") -> Probe:
    """`mode` : https (TLS puis GET), http (GET en clair), tls (poignee de main seule), tcp (connexion seule)."""
    if mode not in MODES:
        return Probe(False, f"mode {mode}")
    start = time.monotonic()
    try:
        connection = socket.create_connection((address, port), timeout=SOCKET_TIMEOUT * 3)
    except OSError as error:
        return Probe(False, str(error), via=address)
    certificate = None
    try:
        if mode == "tcp":
            detail, ok = N_("connexion TCP établie"), True
        elif mode == "http":
            detail = _first_line(connection, host, path)
            ok = _status_ok(detail)
        else:
            context = ssl.create_default_context()
            with context.wrap_socket(connection, server_hostname=host) as tls:
                certificate = certificate_of(tls)
                if mode == "tls":
                    detail, ok = f"TLS {certificate.tls_version}", True
                else:
                    detail = _first_line(tls, host, path)
                    ok = _status_ok(detail)
    except (OSError, ssl.SSLError) as error:
        return Probe(False, str(error), (time.monotonic() - start) * 1000, certificate, address)
    finally:
        connection.close()
    return Probe(ok, detail or N_("réponse vide"), (time.monotonic() - start) * 1000, certificate, address)


def probe_public(host: str, port: int, mode: str, path: str = "/") -> Probe:
    try:
        address = resolve_public(host)
    except OSError as error:
        return Probe(False, f"{PUBLIC_DNS} : {error}")
    return probe(host, port, address, mode, path)
