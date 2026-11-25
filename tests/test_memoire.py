# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Memoire (2026-11-25, MESURES_DEBIT_MEMOIRE.md) : base AS / pays lue dans les octets du fichier, tables de la porte
bornees."""
from __future__ import annotations

import tracemalloc
from pathlib import Path

from test_groups import write_base

from omega_tail.domain.gate import (
    TABLE_IP_SIZE,
    TABLE_PREFIX_SIZE,
    Backend,
    GatePolicy,
    GateTarget,
    render_config,
)
from omega_tail.infrastructure.geo_base import GeoReader


def test_geo_reader_keeps_the_file_bytes_only(tmp_path: Path) -> None:
    path = write_base(tmp_path)
    tracemalloc.start()
    reader = GeoReader(path)
    used = tracemalloc.get_traced_memory()[0]
    tracemalloc.stop()
    assert reader.ready and used < path.stat().st_size + 4096  # les octets, pas un objet par plage
    assert reader.lookup("3.1.2.3") == ("US", 16509) and reader.lookup("90.1.1.1") == ("FR", 3215)


def test_geo_reader_refuses_a_truncated_file(tmp_path: Path) -> None:
    path = write_base(tmp_path)
    data = path.read_bytes()
    (tmp_path / "court.bin").write_bytes(data[:-3])
    truncated = GeoReader(tmp_path / "court.bin")
    assert not truncated.ready and truncated.lookup("3.1.2.3") == ("--", 0)
    assert not GeoReader(tmp_path / "absent.bin").ready


def test_gate_tables_are_bounded() -> None:
    text = render_config(GatePolicy(), GateTarget(443, "x.ts.net", Backend("127.0.0.1:8080")), gate_port=9443,
                         folder="/v/porte")
    assert f"stick-table type ipv6 size {TABLE_IP_SIZE} expire" in text and TABLE_IP_SIZE == "200k"
    assert f"stick-table type ipv6 size {TABLE_PREFIX_SIZE} expire 10m" in text and TABLE_PREFIX_SIZE == "100k"
    assert "size 1m" not in text
