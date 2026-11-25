# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Empreinte JA4 d'un ClientHello TLS (lot 6). Ecrite d'apres la specification publique de FoxIO (JA4, licence
BSD 3-Clause ; JA4+ hors perimetre). Cette version Python est la reference des tests ; la porte calcule la meme
dans HAProxy (infrastructure/gate_lua/ja4.lua), AVANT tout chiffrement.

JA4 = a_b_c
  a : protocole (t = TCP) + version TLS la plus haute (supported_versions, sinon celle du ClientHello) + d/i (nom
      SNI present ou non) + nombre de suites (2 chiffres) + nombre d'extensions (2 chiffres) + premier et dernier
      caractere du premier ALPN (« 00 » sans ALPN) ;
  b : 12 premiers caracteres du SHA-256 des suites triees (hexadecimal, separees par des virgules) ;
  c : idem pour les extensions triees sans SNI ni ALPN, suivies de « _ » et des algorithmes de signature dans
      l'ordre d'origine.
Les valeurs GREASE (0x?a?a) sont ignorees partout : Chrome en tire de nouvelles a chaque connexion."""
from __future__ import annotations

import hashlib
from dataclasses import dataclass

EMPTY_HASH = "000000000000"
_VERSIONS = {0x0304: "13", 0x0303: "12", 0x0302: "11", 0x0301: "10", 0x0300: "s3", 0x0002: "s2",
             0xFEFF: "d1", 0xFEFD: "d2", 0xFEFC: "d3"}
EXT_SNI, EXT_ALPN, EXT_SIGALGS, EXT_VERSIONS = 0x0000, 0x0010, 0x000D, 0x002B


def is_grease(value: int) -> bool:
    return (value & 0x0F0F) == 0x0A0A and (value >> 8) == (value & 0xFF)


@dataclass(frozen=True)
class ClientHello:
    version: int
    ciphers: tuple[int, ...]
    extensions: tuple[int, ...]
    sigalgs: tuple[int, ...] = ()
    versions: tuple[int, ...] = ()
    alpn: tuple[bytes, ...] = ()


class NotClientHello(ValueError):
    """Donnees incompletes ou qui ne sont pas un ClientHello TLS."""


def _u16(data: bytes, at: int) -> int:
    if at + 2 > len(data):
        raise NotClientHello("tronque")
    return int.from_bytes(data[at:at + 2], "big")


def _u16_list(data: bytes) -> tuple[int, ...]:
    return tuple(int.from_bytes(data[i:i + 2], "big") for i in range(0, len(data) - 1, 2))


def parse(record: bytes) -> ClientHello:
    """Premier enregistrement TLS (en-tete de 5 octets compris) contenant un ClientHello complet."""
    if len(record) < 9 or record[0] != 0x16 or record[5] != 0x01:
        raise NotClientHello("pas un ClientHello")
    length = int.from_bytes(record[6:9], "big")
    body = record[9:9 + length]
    if len(body) < length or length < 38:
        raise NotClientHello("incomplet")
    version, at = _u16(body, 0), 34
    at += 1 + body[at]  # session
    count = _u16(body, at)
    ciphers = _u16_list(body[at + 2:at + 2 + count])
    at += 2 + count
    at += 1 + body[at]  # compression
    extensions: list[int] = []
    sigalgs: tuple[int, ...] = ()
    versions: tuple[int, ...] = ()
    alpn: list[bytes] = []
    if at + 2 <= len(body):
        end = min(len(body), at + 2 + _u16(body, at))
        at += 2
        while at + 4 <= end:
            kind, size = _u16(body, at), _u16(body, at + 2)
            data = body[at + 4:at + 4 + size]
            at += 4 + size
            extensions.append(kind)
            if kind == EXT_SIGALGS and len(data) >= 2:
                sigalgs = _u16_list(data[2:2 + _u16(data, 0)])
            elif kind == EXT_VERSIONS and data:
                versions = _u16_list(data[1:1 + data[0]])
            elif kind == EXT_ALPN and len(data) >= 2:
                index, stop = 2, 2 + _u16(data, 0)
                while index < min(stop, len(data)):
                    size_name = data[index]
                    alpn.append(data[index + 1:index + 1 + size_name])
                    index += 1 + size_name
    return ClientHello(version, ciphers, tuple(extensions), sigalgs, versions, tuple(alpn))


def _hash(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()[:12] if text else EMPTY_HASH


def _alnum(byte: int) -> bool:
    return 0x30 <= byte <= 0x39 or 0x41 <= byte <= 0x5A or 0x61 <= byte <= 0x7A


def _alpn_code(alpn: tuple[bytes, ...]) -> str:
    if not alpn or not alpn[0]:
        return "00"
    first = alpn[0]
    if _alnum(first[0]) and _alnum(first[-1]):
        return chr(first[0]) + chr(first[-1])
    text = first.hex()
    return text[0] + text[-1]


def ja4(hello: ClientHello, protocol: str = "t") -> str:
    ciphers = [value for value in hello.ciphers if not is_grease(value)]
    extensions = [value for value in hello.extensions if not is_grease(value)]
    versions = [value for value in hello.versions if not is_grease(value)]
    version = _VERSIONS.get(max(versions) if versions else hello.version, "00")
    sni = "d" if EXT_SNI in extensions else "i"
    part_a = f"{protocol}{version}{sni}{min(len(ciphers), 99):02d}{min(len(extensions), 99):02d}" \
             f"{_alpn_code(hello.alpn)}"
    part_b = _hash(",".join(f"{value:04x}" for value in sorted(ciphers)))
    kept = ",".join(f"{value:04x}" for value in sorted(extensions) if value not in (EXT_SNI, EXT_ALPN))
    sigalgs = ",".join(f"{value:04x}" for value in hello.sigalgs if not is_grease(value))
    part_c = _hash(f"{kept}_{sigalgs}" if sigalgs else kept) if kept else EMPTY_HASH
    return f"{part_a}_{part_b}_{part_c}"


def ja4_of(record: bytes) -> str:
    return ja4(parse(record))
