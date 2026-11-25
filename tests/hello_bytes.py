# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""ClientHello TLS fabriques ou captures pour les tests de JA4 (Python et Lua dans HAProxy)."""
from __future__ import annotations

import contextlib
import socket
import ssl
import struct

CHROME_JA4 = "t13d1516h2_8daaf6152771_e5627efa2ab1"
"""Exemple de reference de la specification JA4 (FoxIO) : Chrome."""


def _ext(kind: int, data: bytes = b"") -> bytes:
    return struct.pack("!HH", kind, len(data)) + data


def _u16s(values: list[int]) -> bytes:
    return b"".join(struct.pack("!H", value) for value in values)


def client_hello(*, ciphers: list[int], extensions: list[bytes], version: int = 0x0303) -> bytes:
    body = struct.pack("!H", version) + bytes(32) + b"\x20" + bytes(32)
    body += struct.pack("!H", len(ciphers) * 2) + _u16s(ciphers) + b"\x01\x00"
    joined = b"".join(extensions)
    body += struct.pack("!H", len(joined)) + joined
    handshake = b"\x01" + len(body).to_bytes(3, "big") + body
    return b"\x16\x03\x01" + struct.pack("!H", len(handshake)) + handshake


def chrome_like() -> bytes:
    """Le Chrome de l'exemple de reference, avec GREASE et un ordre d'extensions melange."""
    name = b"omega.example.ts.net"
    sni = _ext(0x0000, struct.pack("!HBH", len(name) + 3, 0, len(name)) + name)
    protocols = b"\x02h2\x08http/1.1"
    alpn = _ext(0x0010, struct.pack("!H", len(protocols)) + protocols)
    sigalgs = [0x0403, 0x0804, 0x0401, 0x0503, 0x0805, 0x0501, 0x0806, 0x0601]
    signatures = _ext(0x000D, struct.pack("!H", len(sigalgs) * 2) + _u16s(sigalgs))
    versions = _ext(0x002B, bytes([6]) + _u16s([0x7A7A, 0x0304, 0x0303]))
    plain = [_ext(kind, b"\x00") for kind in (0x0005, 0x000A, 0x000B, 0x0012, 0x0015, 0x0017, 0x001B, 0x0023,
                                              0x002D, 0x0033, 0x4469, 0xFF01)]
    extensions = [_ext(0x3A3A), plain[5], sni, plain[0], signatures, plain[9], alpn, versions, *plain[1:5],
                  *plain[6:9], plain[10], plain[11], _ext(0x9A9A, b"\x00")]
    ciphers = [0x1A1A, 0x1301, 0x1302, 0x1303, 0xCCA9, 0xCCA8, 0xC02B, 0xC02F, 0xC02C, 0xC030, 0xC013, 0xC014,
               0x009C, 0x009D, 0x002F, 0x0035]
    return client_hello(ciphers=ciphers, extensions=extensions)


def python_hello(server_name: str = "omega.example.ts.net") -> bytes:
    """Vrai ClientHello envoye par le module ssl de Python (OpenSSL de la machine)."""
    left, right = socket.socketpair()
    left.setblocking(False)
    client = ssl.create_default_context().wrap_socket(left, server_hostname=server_name,
                                                      do_handshake_on_connect=False)
    with client, right:
        with contextlib.suppress(ssl.SSLWantReadError):
            client.do_handshake()
        right.settimeout(2)
        data = b""
        while len(data) < 5 or len(data) < 5 + int.from_bytes(data[3:5], "big"):
            data += right.recv(65536)
        return data
