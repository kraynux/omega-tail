# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Couleurs des lignes des Journaux (2026-11-25, demande) : une nuance par information, couleurs du
theme, jamais de balisage interprete."""
from __future__ import annotations

from rich.style import Style

from omega_tail.interfaces.tui.screens.journal_highlight import family, highlight_journal_line, palette_from_theme

THEME = {"text-primary": "#57A5E2", "text-secondary": "#5684A5", "text-accent": "#FFC473", "text-success": "#8AD4A1",
         "text-warning": "#FFC473", "text-error": "#D17E92"}
PALETTE = palette_from_theme(THEME)


def styled(line: str, piece: str) -> Style:
    """Style compose applique au premier caractere de `piece` dans la ligne coloree."""
    text = highlight_journal_line(line, PALETTE)
    return text.get_style_at_offset(_console(), line.index(piece))


def _console():  # type: ignore[no-untyped-def]
    from rich.console import Console

    return Console()


def test_tailscaled_line_has_one_shade_per_information() -> None:
    line = ("2026-11-25T19:54:03+01:00 serveur tailscaled[918]: magicsock: derp-4 connected via 100.64.12.34:41641 "
            "[abc12]")
    assert styled(line, "2026").color.triplet.hex == "#5684a5"  # date
    assert styled(line, "serveur").dim
    assert styled(line, "tailscaled").bold
    assert styled(line, "magicsock").color.triplet.hex == "#8ad4a1"  # famille reseau
    assert styled(line, "100.64").bold and styled(line, "100.64").color.triplet.hex == "#ffc473"
    assert styled(line, "[abc12]").dim
    assert styled(line, "connected").color is None  # le message garde la couleur du texte


def test_categories_are_grouped_by_family() -> None:
    assert family("control: controlclient direct: ") == "control"
    assert family("dns: resolver: forward: ") == "dns"
    assert family("wgengine: Reconfig: ") == "engine"
    assert family("netcheck: ") == "network"
    assert family("inconnu: ") == ""


def test_error_and_warning_lines_stand_out_and_stop_the_category() -> None:
    error = "2026-11-25T19:54:23+01:00 serveur tailscaled[9]: health(warnable=no-derp-home): error: no DERP home"
    assert styled(error, "error:").bold and styled(error, "error:").color.triplet.hex == "#d17e92"
    assert styled(error, "no DERP").color.triplet.hex == "#d17e92"
    assert styled(error, "health").color.triplet.hex == "#57a5e2"
    warning = "nov. 25 19:52:46 hote tailscaled[9]: netcheck: timeout waiting for STUN"
    assert styled(warning, "waiting").color.triplet.hex == "#ffc473"


def test_gate_line_shows_visitor_reason_and_origin() -> None:
    line = ("2026-11-25T19:54:26+01:00 serveur haproxy[12]: 203.0.113.7:41000 [25/Nov/2026:19:54:26.001] entree "
            "tls/site 0/0/10 0 CD 1/1/0/0/0 0/0 motif=noire groupe=ja4 ja4=t13d as=AS64501 pays=DE")
    assert styled(line, "203.0.113.7").bold
    assert styled(line, "noire").color.triplet.hex == "#d17e92"  # motif de refus
    assert styled(line, "AS64501").color.triplet.hex == "#5684a5"
    assert styled(line, "DE").color.triplet.hex == "#ffc473"
    assert styled(line, "motif=").dim
    early = ("2026-11-25T19:54:25+01:00 serveur haproxy[12]: 198.51.100.9:51000 [25/Nov/2026:19:54:25.001] entree "
             "avant-tls motif=budget groupe=- ja4=- as=- pays=-")
    assert styled(early, "avant-tls").bold and styled(early, "budget").bold


def test_markup_is_never_interpreted_and_unusual_lines_pass() -> None:
    line = "2026-11-25T19:54:26+01:00 h tailscaled[1]: control: [bold red]pas du balisage[/] 999.1.2.3"
    assert highlight_journal_line(line, PALETTE).plain == line
    assert highlight_journal_line("", PALETTE).plain == ""
    assert highlight_journal_line("ligne sans date", PALETTE).plain == "ligne sans date"
    assert palette_from_theme({"text-primary": "#E0E0E099", "text-error": "auto 60%"}).error is not None


def test_group_labels_and_dashboard_alignment_follow_the_language() -> None:
    """Libelles des regroupements traduits (captures 2026-11-25) ; alignement a la largeur d'ecran (japonais…)."""
    import os

    from rich.cells import cell_len

    from omega_tail.application.groups import GroupRow
    from omega_tail.interfaces.shared.messages import group_label
    from omega_tail.interfaces.tui.screens.dashboard import styled
    from omega_tail.shared.i18n import LANGUAGE

    LANGUAGE.install(settings_store=None, environ={"OMEGA_TAIL_LANG": "de"})
    try:
        assert group_label(GroupRow("AS64500", 3, 9, "EXAMPLE-NET", hosting=True)) == "EXAMPLE-NET (Hoster)"
        assert group_label(GroupRow("t13d", 1, 2, "habituelle")) == "üblich"
        assert group_label(GroupRow("FR", 1, 2)) == ""
        lines = [("サービス", "有効", "ok"), ("CPU", "3 %", "ok")]
        rows = styled(lines, {}).plain.splitlines()
        assert cell_len(rows[0].split("有効")[0]) == cell_len(rows[1].split("3 %")[0])
    finally:
        LANGUAGE.install(settings_store=None, environ={"OMEGA_TAIL_LANG": "fr"})
        os.environ.pop("OMEGA_TAIL_LANG", None)
