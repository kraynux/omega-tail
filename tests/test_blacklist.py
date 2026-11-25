# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Liste noire de la porte (finitions 0.7.0) : dates et origines, plafond, import, purges, export."""
from __future__ import annotations

import json
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path

from funnel_sim import FunnelSim
from test_gate import PRODUCTION, FakeAdmin, gate

from omega_tail.application.gate import in_tailnet
from omega_tail.domain import blacklist
from omega_tail.domain.blacklist import (
    ORIGIN_EXISTING,
    ORIGIN_IMPORT,
    ORIGIN_MANUAL,
    PURGE_ALL,
    PURGE_OLDER,
    PURGE_OLDEST,
    PURGE_ORIGIN,
    PURGE_RANGE,
    BlackEntry,
    PurgeChoice,
    export_text,
    normalize,
    parse_import,
    select_purge,
)

NOW = datetime(2026, 11, 22, 23, 0, tzinfo=timezone.utc)


def test_normalize_and_import_report() -> None:
    assert normalize(" 198.51.100.7/32 ") == "198.51.100.7" and normalize("198.51.100.9/24") == "198.51.100.0/24"
    text = ("# liste d'attaque\n203.0.113.7\n203.0.113.7  # doublon\n198.51.100.0/24\n198.51.100.20\n"
            "100.64.10.47\nnimporte quoi\n2001:db8::1\n\n")
    report = parse_import(text, ["192.0.2.1"], now=NOW, room=100, in_tailnet=in_tailnet)
    assert [entry.address for entry in report.added] == ["203.0.113.7", "198.51.100.0/24", "2001:db8::1"]
    assert all(entry.origin == ORIGIN_IMPORT for entry in report.added)
    assert report.duplicates == 2  # la meme adresse deux fois, et une adresse deja dans un reseau importe
    assert report.tailnet == 1 and report.invalid == ((7, "nimporte quoi"),)
    limited = parse_import("203.0.113.1\n203.0.113.2\n203.0.113.3\n", [], now=NOW, room=2, in_tailnet=in_tailnet)
    assert len(limited.added) == 2 and limited.over_limit == 1


def test_purge_choices() -> None:
    entries = [BlackEntry(f"203.0.113.{day}", NOW - timedelta(days=day), ORIGIN_IMPORT if day % 2 else ORIGIN_MANUAL)
               for day in (30, 20, 10, 1)]
    assert [e.address for e in select_purge(entries, PurgeChoice(PURGE_OLDER, days=15), NOW)] == [
        "203.0.113.30", "203.0.113.20"]
    assert len(select_purge(entries, PurgeChoice(PURGE_OLDEST, count=3), NOW)) == 3
    assert [e.address for e in select_purge(entries, PurgeChoice(PURGE_RANGE, first=3, last=2), NOW)] == [
        "203.0.113.20", "203.0.113.10"]  # plage dans les deux sens, numerotee a partir de 1
    assert [e.address for e in select_purge(entries, PurgeChoice(PURGE_ORIGIN, origin=ORIGIN_IMPORT), NOW)] == [
        "203.0.113.1"]
    assert len(select_purge(entries, PurgeChoice(PURGE_ALL), NOW)) == 4
    exported = export_text(entries)
    again = parse_import(exported, [], now=NOW, room=10, in_tailnet=in_tailnet)
    assert len(again.added) == 4 and not again.invalid  # l'export TXT se reimporte tel quel


def test_old_list_gets_dates_and_files_stay_in_step(tmp_path: Path) -> None:
    tools = gate(tmp_path, FunnelSim(PRODUCTION), admin=FakeAdmin())
    folder = tmp_path / "var" / "porte"
    (folder / "noire.lst").write_text("192.0.2.1\n198.51.100.0/24\n")
    stamp = (NOW - timedelta(days=3)).timestamp()
    os.utime(folder / "noire.lst", (stamp, stamp))
    entries = tools.black_entries()
    assert {(e.address, e.origin) for e in entries} == {("192.0.2.1", ORIGIN_EXISTING),
                                                        ("198.51.100.0/24", ORIGIN_EXISTING)}
    assert all(e.added == NOW - timedelta(days=3) for e in entries)  # date du fichier, pas du jour
    added = tools.add_black("203.0.113.7")
    assert added.ok and added.message == "{address} → liste noire (refusée jusqu'au retrait)."
    data = json.loads((folder / "noire.json").read_text())
    assert [item["adresse"] for item in data] == ["192.0.2.1", "198.51.100.0/24", "203.0.113.7"]
    assert data[-1]["origine"] == ORIGIN_MANUAL
    assert (folder / "noire.lst").read_text() == "192.0.2.1\n198.51.100.0/24\n203.0.113.7\n"
    assert not tools.add_black("198.51.100.9").ok  # deja dans un reseau de la liste
    assert not tools.add_black("100.64.10.47").ok and not tools.add_black("pas une adresse").ok


def test_import_purge_and_limit(tmp_path: Path, monkeypatch: object) -> None:
    admin = FakeAdmin()
    tools = gate(tmp_path, FunnelSim(PRODUCTION), admin=admin)
    outcome, report = tools.import_black("203.0.113.1\n203.0.113.2\n203.0.113.1\n100.64.0.1\nxx\n")
    assert outcome.ok and outcome.params == {"added": 2, "duplicates": 1, "tailnet": 1, "invalid": 1,
                                             "inactive": True}
    assert report.invalid == ((5, "xx"),)
    assert tools.lists()[1] == ["203.0.113.1", "203.0.113.2"]
    preview = tools.purge_preview(PurgeChoice(PURGE_ORIGIN, origin=ORIGIN_IMPORT))
    assert len(preview) == 2
    purged = tools.purge_black(PurgeChoice(PURGE_OLDEST, count=1))
    assert purged.ok and purged.params["count"] == 1 and tools.lists()[1] == ["203.0.113.2"]
    assert not tools.purge_black(PurgeChoice(PURGE_OLDER, days=30)).ok  # rien d'aussi ancien
    assert tools.remove_black(["203.0.113.2"]).params["left"] == 0
    monkeypatch.setattr("omega_tail.application.gate.BLACKLIST_MAX", 2)  # type: ignore[attr-defined]
    tools.import_black("203.0.113.5\n203.0.113.6\n")
    full = tools.add_black("203.0.113.9")
    assert not full.ok and "Liste noire pleine" in full.message
    assert not tools.block("203.0.113.9", forever=True).ok
    assert blacklist.BLACKLIST_MAX == 50_000 and blacklist.BLACKLIST_WARNING == 25_000


def test_one_line_notifications(tmp_path: Path) -> None:
    tools = gate(tmp_path, FunnelSim(PRODUCTION), admin=FakeAdmin())
    assert tools.block("203.0.113.7").message == "{address} → bloquée {minutes} min (blocage temporaire)."
    assert tools.block("203.0.113.7", forever=True).message == "{address} → liste noire (refusée jusqu'au retrait)."
    assert tools.unblock("203.0.113.7").message == "{address} → admise (soumise aux règles), retirée de la liste noire."
    assert tools.trust("203.0.113.8").message == "{address} → confiance (jamais limitée)."
    assert tools.trust("203.0.113.8", add=False).message == "{address} → admise (soumise aux règles)."
    for outcome in (tools.block("203.0.113.9"), tools.trust("203.0.113.9")):
        assert "\n" not in outcome.message


async def test_blacklist_screen_from_attacks(tmp_path: Path) -> None:
    from test_tui import gate_app, settle
    from textual.widgets import Button, Input, Select, Static

    from omega_tail.infrastructure.exports.writer import FileExportWriter
    from omega_tail.interfaces.tui.screens.attacks import AttacksScreen
    from omega_tail.interfaces.tui.screens.blacklist import BlacklistScreen
    from omega_tail.interfaces.tui.screens.confirm import ConfirmScreen
    from omega_tail.interfaces.tui.widgets.tables import WideTable

    app = gate_app(tmp_path, FunnelSim(PRODUCTION))
    app.writer = FileExportWriter(tmp_path / "exports")
    source = tmp_path / "attaque.txt"
    source.write_text("203.0.113.1\n203.0.113.2\n203.0.113.2\n100.64.0.9\nzz\n")
    async with app.run_test(size=(140, 60)) as pilot:
        await settle(pilot)
        app.open_key("attacks")
        await settle(pilot)
        attacks = app.screen
        assert isinstance(attacks, AttacksScreen)
        assert "la notification dit" not in str(attacks.query(Static).last().render())
        attacks.query_one("#manage-blacklist", Button).press()
        await settle(pilot)
        screen = app.screen
        assert isinstance(screen, BlacklistScreen)
        screen.query_one("#import-path", Input).value = str(source)
        screen.query_one("#import", Button).press()
        await settle(pilot)
        await pilot.pause(0.2)
        await settle(pilot)
        table = screen.query_one("#black-table", WideTable)
        assert table.row_count == 2 and str(table.get_row_at(0)[1]) == "203.0.113.1"
        screen.query_one("#new-address", Input).value = "198.51.100.0/24"
        screen.query_one("#add", Button).press()
        await settle(pilot)
        await pilot.pause(0.2)
        await settle(pilot)
        assert table.row_count == 3
        screen.query_one("#filter", Input).value = "198.51"
        await pilot.pause()
        assert table.row_count == 1
        screen.query_one("#filter", Input).value = ""
        screen.query_one("#export-html", Button).press()
        screen.query_one("#export-txt", Button).press()
        await settle(pilot)
        exported = sorted((tmp_path / "exports").iterdir())
        assert [path.suffix for path in exported] == [".html", ".txt"]
        assert "203.0.113.2" in exported[0].read_text() and exported[1].read_text().startswith("# omega-tail")
        screen.query_one("#purge-mode", Select).value = 3  # origine : import
        screen.query_one("#preview", Button).press()
        await pilot.pause()
        assert "2 entrée(s) sur 3 partiraient" in str(screen.query_one("#purge-hint", Static).render())
        screen.query_one("#purge", Button).press()
        await pilot.pause()
        assert isinstance(app.screen, ConfirmScreen)
        app.screen.query_one("#confirm", Button).press()
        await settle(pilot)
        await pilot.pause(0.2)
        await settle(pilot)
        assert app.gate is not None and app.gate.lists()[1] == ["198.51.100.0/24"]
