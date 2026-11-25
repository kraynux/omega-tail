# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Scan de securite claude-security du 2026-11-25 (CLAUDE-SECURITY-20261125-075456) : un test par faille corrigee."""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

import pytest
from funnel_sim import FunnelSim
from test_gate import PRODUCTION, FakeAdmin, gate

from omega_tail.domain.blacklist import is_canonical, normalize, parse_import
from omega_tail.domain.gate import (
    GatePolicy,
    GateTarget,
    backend_of,
    backend_tls_options,
    openrc_script,
    render_config,
    runit_run_script,
)
from omega_tail.domain.text import without_controls
from omega_tail.infrastructure.gate import UnsafeCommand, _single
from omega_tail.infrastructure.tailscale.parsing import parse_devices

FOLDER = "/home/u/omega-tail/var/porte"
ZONE = "fe80::1%x;shutdown frontend porte"


def test_f1_runit_checks_config_as_the_user() -> None:
    lines = runit_run_script(user="u", haproxy="/usr/sbin/haproxy", folder=FOLDER).splitlines()
    commands = [line for line in lines if line and not line.startswith("#") and line != "exec 2>&1"]
    assert commands and all(line.removeprefix("exec ").startswith("chpst -u u ") for line in commands)  # rien en root


def test_f2_openrc_checks_config_as_the_user() -> None:
    script = openrc_script(user="u", haproxy="/usr/sbin/haproxy", folder=FOLDER)
    start_pre = script.split("start_pre() {", 1)[1].split("}", 1)[0].strip()
    assert start_pre == f"su -s /bin/sh -c '/usr/sbin/haproxy -c -q -f {FOLDER}/haproxy.cfg' u"


def test_f3_zone_ids_never_reach_haproxy(tmp_path: Path) -> None:
    with pytest.raises(ValueError):
        normalize(ZONE)
    with pytest.raises(ValueError):
        normalize("fe80::1%eth0")
    assert is_canonical("2001:db8::/32") and is_canonical("::ffff:192.0.2.1") and not is_canonical("1.2.3.4 x")
    report = parse_import(f"{ZONE}\n203.0.113.1\n", [], now=datetime.now(), room=10,
                          in_tailnet=lambda _address: False)
    assert [entry.address for entry in report.added] == ["203.0.113.1"] and len(report.invalid) == 1
    admin = FakeAdmin()
    tools = gate(tmp_path, FunnelSim(PRODUCTION), admin=admin)
    assert not tools.block(ZONE).ok and not tools.add_black(ZONE).ok
    # Entree piegee deja sur le disque (import d'avant le correctif) : ecartee, jamais envoyee au socket
    folder = tmp_path / "var" / "porte"
    (folder / "noire.lst").write_text(f"{ZONE}\n198.51.100.7\n")
    (folder / "noire.json").write_text(json.dumps([{"adresse": ZONE, "ajout": "2026-11-25T08:00:00+00:00"}]))
    assert [entry.address for entry in tools.black_entries()] == ["198.51.100.7"]
    tools.remove_black([ZONE, "198.51.100.7"])
    assert admin.lines and not any(";" in line for line in admin.lines)
    assert (folder / "noire.lst").read_text() == ""
    with pytest.raises(UnsafeCommand):
        _single(f"del acl /x/noire.lst {ZONE}")
    with pytest.raises(UnsafeCommand):
        _single("show stat\nshutdown frontend porte")
    assert _single("set ssl cert /x/c.pem <<\n-----BEGIN-----\nAA\n").startswith("set ssl cert")


def test_f4_peers_listen_on_a_private_socket() -> None:
    text = render_config(GatePolicy(), GateTarget(443, "x.ts.net", backend_of("http://127.0.0.1:8080")),
                         gate_port=9443, folder=FOLDER)
    assert f"peer omega-tail unix@{FOLDER}/pairs.sock" in text and "127.0.0.1:9444" not in text


def test_f5_verified_backend_stays_verified() -> None:
    assert backend_tls_options(backend_of("http://127.0.0.1:8080")) == ""
    assert backend_tls_options(backend_of("https+insecure://localhost:8443")) == " ssl verify none"
    assert backend_tls_options(backend_of("https://127.0.0.1:8443")) == " ssl verify required ca-file @system-ca"
    assert backend_tls_options(backend_of("https://localhost:8443")) == (
        " ssl verify required ca-file @system-ca sni str(localhost) verifyhost localhost")


def test_f6_install_uses_mktemp() -> None:
    script = (Path(__file__).resolve().parent.parent / "install.sh").read_text()
    assert "/tmp/omega-tail" not in script and 'VENV_ERR="$(mktemp)"' in script


def test_f7_tailnet_names_lose_control_characters() -> None:
    hostile = "pc\x1b]52;c;ZWNobyBwd24=\x07\x1b[2J‮evil\x9b"
    devices = parse_devices({"Peer": {"k": {"HostName": hostile, "OS": "linux\x1b[31m", "Tags": ["tag:\x1bx"]}}})
    assert devices[0].name == "pc]52;c;ZWNobyBwd24=[2Jevil" and devices[0].os == "linux[31m"
    assert devices[0].tags == ("tag:x",)
    assert without_controls("a\tb\nc\x1b", keep="\n\t") == "a\tb\nc"
