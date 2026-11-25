# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
from __future__ import annotations

import json

import pytest
from conftest import FUNNEL_HTTPS, NOW, snapshot, tailscale_state

from omega_tail import __version__
from omega_tail.domain.alerts import alerts_for
from omega_tail.interfaces.cli.main import main_with
from omega_tail.interfaces.shared.help_view import help_text, render_help_html
from omega_tail.interfaces.tui.menu import MENU


def state():  # type: ignore[no-untyped-def]
    shot = snapshot(tailscale=tailscale_state(daemon_version="1.104.4"), publications=(FUNNEL_HTTPS,))
    return shot, alerts_for(shot, NOW)


def test_version_comes_from_pyproject() -> None:
    assert __version__ == "0.7.0"


def test_etat_text(capsys: pytest.CaptureFixture[str]) -> None:
    assert main_with(["etat"], version="0.1.0", state=state, dashboard=lambda: 9) == 0
    out = capsys.readouterr().out
    assert "1.104.4 en marche, 1.104.7 installée" in out
    assert "Funnel publié sans protection sur le port 443" in out
    assert "kraynux.tailnet-exemple.ts.net:443 · Internet (Funnel)" in out


def test_etat_json_is_parseable(capsys: pytest.CaptureFixture[str]) -> None:
    main_with(["etat", "--format", "json"], version="0.1.0", state=state, dashboard=lambda: 9)
    data = json.loads(capsys.readouterr().out)
    assert data["format"] == "omega-tail-etat" and data["snapshot"]["tailscale"]["backend"] == "Running"
    assert [alert["code"] for alert in data["alerts"]][:2] == ["daemon-outdated", "funnel-unprotected"]


def test_no_argument_opens_the_interface() -> None:
    assert main_with([], version="0.1.0", state=state, dashboard=lambda: 9) == 9


def test_help_covers_every_available_menu_and_exports(capsys: pytest.CaptureFixture[str]) -> None:
    text = help_text()
    for label in ("Tableau de bord", "Service tailscaled", "Journaux", "Survie", "Pare-feu Funnel", "Attaques et décisions", "Réglages", "Devenir opérateur"):
        assert label.upper() in text
    page = render_help_html("0.1.0")
    assert "<h1>Aide d’omega-tail" in page and "OMEGA-TAIL 0.1.0" in page
    assert main_with(["aide"], version="0.1.0", state=state, dashboard=lambda: 9) == 0
    assert "DÉMARRAGE RAPIDE" in capsys.readouterr().out


def test_menu_is_two_columns_of_six_without_quit() -> None:
    assert len(MENU) == 12 and all(entry.key != "quit" for entry in MENU)
    assert [entry.column.value for entry in MENU].count("tailscale") == 6
    assert not [entry.key for entry in MENU if entry.planned]  # lot 7 : les 12 ecrans existent
