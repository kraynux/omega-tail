# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""JA4 (lot 6) : exemple de reference de la specification, GREASE ignore, ClientHello reel de Python."""
from __future__ import annotations

import contextlib
import re

import pytest
from hello_bytes import CHROME_JA4, chrome_like, client_hello, python_hello

from omega_tail.domain.ja4 import NotClientHello, is_grease, ja4_of

FORMAT = re.compile(r"^t(13|12|11|10)[di]\d{4}[0-9a-z]{2}_[0-9a-f]{12}_[0-9a-f]{12}$")


def test_reference_example_with_grease_and_shuffled_extensions() -> None:
    assert ja4_of(chrome_like()) == CHROME_JA4
    assert is_grease(0x1A1A) and is_grease(0xFAFA) and not is_grease(0x1301) and not is_grease(0x0A0B)


def test_no_extensions_no_alpn_no_sni() -> None:
    bare = client_hello(ciphers=[0x002F], extensions=[], version=0x0301)
    assert ja4_of(bare) == "t10i010000_" + ja4_of(bare).split("_")[1] + "_000000000000"


def test_real_python_client_hello() -> None:
    record = python_hello()
    found = ja4_of(record)
    assert FORMAT.match(found), found
    assert found[3] == "d"  # nom SNI envoye
    assert ja4_of(python_hello()) == found  # stable d'une connexion a l'autre


def test_garbage_is_refused() -> None:
    for data in (b"", b"GET / HTTP/1.1\r\n", chrome_like()[:40]):
        with pytest.raises(NotClientHello):
            ja4_of(data)


def _free_port() -> int:
    import socket

    with socket.socket() as probe:
        probe.bind(("127.0.0.1", 0))
        return int(probe.getsockname()[1])


def test_haproxy_lua_gives_the_same_ja4(tmp_path) -> None:  # type: ignore[no-untyped-def]
    """Le script Lua de la porte, execute par le vrai HAProxy, donne exactement le JA4 de reference."""
    import shutil
    import socket
    import subprocess
    import time
    from pathlib import Path

    haproxy = shutil.which("haproxy")
    if not haproxy or "USE_LUA=1" not in subprocess.run([haproxy, "-vv"], capture_output=True, text=True).stdout:
        pytest.skip("HAProxy avec Lua absent")
    script = Path(__file__).parents[1] / "src/omega_tail/infrastructure/lua/omega_ja4.lua"
    port = _free_port()
    config = tmp_path / "h.cfg"
    config.write_text(f"""global
    tune.lua.bool-sample-conversion normal
    lua-load {script}
    log stdout format raw local0
defaults
    mode tcp
    log global
    timeout client 3s
    timeout connect 2s
    timeout server 2s
frontend f
    bind 127.0.0.1:{port}
    tcp-request inspect-delay 2s
    tcp-request content reject unless {{ req.ssl_hello_type 1 }}
    tcp-request content lua.omega_ja4
    tcp-request content reject
    log-format "JA4=%[var(sess.ja4)]"
""")
    process = subprocess.Popen([haproxy, "-db", "-f", str(config)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                               text=True)
    records = [chrome_like(), python_hello(), python_hello("autre.example"), b"\x16\x03\x01\x00\x05garbage"]
    try:
        for _ in range(50):
            try:
                socket.create_connection(("127.0.0.1", port), timeout=1).close()
                break
            except OSError:
                time.sleep(0.1)
        for record in records:
            with socket.create_connection(("127.0.0.1", port), timeout=3) as connection:
                connection.sendall(record)
                with contextlib.suppress(OSError):
                    connection.recv(10)
        time.sleep(0.5)
    finally:
        process.terminate()
        output = process.communicate(timeout=10)[0]
    found = [line.split("JA4=", 1)[1].strip() for line in output.splitlines() if "JA4=" in line]
    expected = [ja4_of(record) for record in records[:3]] + ["-"]
    assert found[-4:] == expected, output
