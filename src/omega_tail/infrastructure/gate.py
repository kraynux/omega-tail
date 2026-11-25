# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""La porte cote machine : interface d'administration d'HAProxy (sockets locaux 600), certificat par
`tailscale cert`, verification de la configuration, essais local et public (valides en reel sur le J3455 le
2026-11-22 : adresse reelle par PROXY v2, certificat Let's Encrypt, X25519MLKEM768)."""
from __future__ import annotations

import ipaddress
import os
import random
import shutil
import socket
import ssl
import struct
from datetime import datetime, timezone
from pathlib import Path

from omega_tail.core.constants import TAILSCALE_COMMAND
from omega_tail.infrastructure.commands import run_quiet, run_with_input
from omega_tail.shared.i18n import N_

PROXY_V2_SIGNATURE = b"\r\n\r\n\x00\r\nQUIT\n"
PROBE_SOURCE = "192.0.2.1"
"""Adresse de documentation annoncee par l'essai local (jamais une vraie adresse)."""
PUBLIC_RESOLVER = ("1.1.1.1", 53)
SOCKET_TIMEOUT = 5.0


def _talk(path: Path, line: str) -> str:
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as connection:
        connection.settimeout(SOCKET_TIMEOUT)
        connection.connect(str(path))
        connection.sendall(line.encode() + b"\n")
        chunks = []
        while True:
            data = connection.recv(65536)
            if not data:
                break
            chunks.append(data)
    return b"".join(chunks).decode(errors="replace")


class UnsafeCommand(OSError):
    """Commande refusee avant le socket : elle en enchainerait une autre (« ; » ou fin de ligne)."""


def _single(line: str) -> str:
    """Une seule commande par envoi (scan de securite 2026-11-25, F3). Le CLI d'HAProxy coupe sur « ; » et sur la
    fin de ligne ; seule exception, la charge utile « <<\\n… » (certificat), qui suit la commande."""
    head = line.split(" <<\n", 1)[0]
    if any(char in head for char in ";\n\r"):
        raise UnsafeCommand(f"commande refusée : {head[:80]!r}")
    return line


class HaproxyAdmin:
    def __init__(self, folder: Path) -> None:
        self._folder = folder

    def command(self, line: str) -> str:
        return _talk(self._folder / "admin.sock", _single(line))

    def master(self, line: str) -> str:
        return _talk(self._folder / "master.sock", _single(line))


def proxy_v2_header(source: str, destination: str = "100.64.0.1", source_port: int = 40000,
                    destination_port: int = 443) -> bytes:
    src, dst = ipaddress.ip_address(source), ipaddress.ip_address(destination)
    if src.version == 4 and dst.version == 4:
        body, family = src.packed + dst.packed + struct.pack("!HH", source_port, destination_port), 0x11
    else:
        dst6 = ipaddress.ip_address(f"::ffff:{dst}") if dst.version == 4 else dst
        src6 = ipaddress.ip_address(f"::ffff:{src}") if src.version == 4 else src
        body, family = src6.packed + dst6.packed + struct.pack("!HH", source_port, destination_port), 0x21
    return PROXY_V2_SIGNATURE + bytes([0x21, family]) + struct.pack("!H", len(body)) + body


def _https_get(connection: socket.socket, dns_name: str) -> str:
    context = ssl.create_default_context()
    with context.wrap_socket(connection, server_hostname=dns_name) as tls:
        tls.sendall(f"GET / HTTP/1.1\r\nHost: {dns_name}\r\nUser-Agent: omega-tail-essai\r\n"
                    "Connection: close\r\n\r\n".encode())
        first = tls.recv(4096).decode(errors="replace").split("\r\n", 1)[0]
    return first


def _status_ok(first_line: str) -> bool:
    parts = first_line.split()
    return len(parts) >= 2 and parts[0].startswith("HTTP/") and parts[1].isdigit() and int(parts[1]) < 500


def resolve_public(dns_name: str, resolver: tuple[str, int] = PUBLIC_RESOLVER) -> str:
    """Adresse A publique (relais Funnel), demandee a un resolveur public : le MagicDNS de la machine
    renverrait l'adresse du tailnet et l'essai ne passerait pas par Funnel."""
    ident = random.randrange(65536)
    question = b"".join(bytes([len(label)]) + label.encode() for label in dns_name.split(".")) + b"\x00"
    query = struct.pack("!HHHHHH", ident, 0x0100, 1, 0, 0, 0) + question + struct.pack("!HH", 1, 1)
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp:
        udp.settimeout(SOCKET_TIMEOUT)
        udp.sendto(query, resolver)
        answer, _ = udp.recvfrom(2048)
    if len(answer) < 12 or struct.unpack("!H", answer[:2])[0] != ident:
        raise OSError(N_("réponse DNS invalide"))
    count = struct.unpack("!H", answer[6:8])[0]
    offset = 12 + len(question) + 4
    for _ in range(count):
        if answer[offset] & 0xC0 == 0xC0:
            offset += 2
        else:
            while answer[offset]:
                offset += answer[offset] + 1
            offset += 1
        kind, _cls, _ttl, length = struct.unpack("!HHIH", answer[offset:offset + 10])
        offset += 10
        if kind == 1 and length == 4:
            return socket.inet_ntoa(answer[offset:offset + 4])
        offset += length
    raise OSError(N_("aucune adresse publique pour ce nom"))


class GateSystem:
    def __init__(self, haproxy_override: str = "") -> None:
        self._override = haproxy_override

    def haproxy(self) -> str:
        if self._override:
            return self._override if os.access(self._override, os.X_OK) else ""
        return shutil.which("haproxy") or ""

    def check_config(self, path: str) -> tuple[bool, str]:
        binary = self.haproxy()
        if not binary:
            return False, N_("HAProxy absent")
        output = run_quiet([binary, "-c", "-q", "-f", path], timeout=30)
        error = next((line for line in (output.stdout + output.stderr).splitlines() if "ALERT" in line), "")
        return output.code == 0, error or output.last_error

    def fetch_certificate(self, dns_name: str, cert: str, key: str) -> tuple[bool, str]:
        output = run_quiet([TAILSCALE_COMMAND, "cert", "--cert-file", cert, "--key-file", key, dns_name], timeout=120)
        return output.code == 0, output.last_error

    def certificate_expiry_days(self, pem: str) -> int | None:
        output = run_quiet(["openssl", "x509", "-in", pem, "-noout", "-enddate"])
        text = output.stdout.strip().removeprefix("notAfter=")
        try:
            end = datetime.strptime(text, "%b %d %H:%M:%S %Y %Z").replace(tzinfo=timezone.utc)
        except ValueError:
            return None
        return (end - datetime.now(timezone.utc)).days

    def local_probe(self, gate_port: int, dns_name: str) -> tuple[bool, str]:
        try:
            connection = socket.create_connection(("127.0.0.1", gate_port), timeout=SOCKET_TIMEOUT)
            connection.sendall(proxy_v2_header(PROBE_SOURCE))
            first = _https_get(connection, dns_name)
        except (OSError, ssl.SSLError) as error:
            return False, str(error)
        return _status_ok(first), first

    def public_probe(self, dns_name: str, port: int) -> tuple[bool, str]:
        try:
            address = resolve_public(dns_name)
            connection = socket.create_connection((address, port), timeout=SOCKET_TIMEOUT * 3)
            first = _https_get(connection, dns_name)
        except (OSError, ssl.SSLError) as error:
            return False, str(error)
        return _status_ok(first), f"{first} via {address}"

    def set_cron(self, marker: str, line: str) -> tuple[bool, str]:
        """Crontab de l'utilisateur (aucun droit) : la ligne portant `marker` est remplacee ou retiree, le reste
        de la crontab est garde tel quel (meme regle que le renouvellement des certificats d'omega-serv)."""
        if not shutil.which("crontab"):
            return False, N_("crontab absent (installez cronie ou un autre cron)")
        current = run_quiet(["crontab", "-l"])
        lines = [entry for entry in (current.stdout.splitlines() if current.code == 0 else []) if marker not in entry]
        if line:
            lines.append(line)
        text = "\n".join(lines) + "\n"
        code, error = run_with_input(["crontab", "-"], text.encode())
        return code == 0, error

    def has_lua(self) -> bool:
        """HAProxy compile avec Lua (necessaire aux regroupements du lot 6)."""
        binary = self.haproxy()
        return bool(binary) and "USE_LUA=1" in run_quiet([binary, "-vv"], timeout=10).stdout

    def install_command(self) -> tuple[str, ...]:
        for manager, command in (("pacman", ("pacman", "-S", "--needed", "--noconfirm", "haproxy")),
                                 ("apt-get", ("apt-get", "install", "-y", "haproxy")),
                                 ("dnf", ("dnf", "install", "-y", "haproxy")),
                                 ("zypper", ("zypper", "--non-interactive", "install", "haproxy")),
                                 ("apk", ("apk", "add", "haproxy")),
                                 ("xbps-install", ("xbps-install", "-y", "haproxy")),
                                 ("emerge", ("emerge", "--ask=n", "net-proxy/haproxy"))):
            if shutil.which(manager):
                return ("sudo", *command) if os.geteuid() != 0 else command
        return ()
