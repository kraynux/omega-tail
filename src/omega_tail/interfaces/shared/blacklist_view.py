# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Export de la liste noire de la porte (finitions 0.7.0) : TXT reimportable tel quel, HTML au theme d'export
d'omega-lib (meme cadre que le rapport et l'aide), JSON."""
from __future__ import annotations

import html
import json
from collections.abc import Sequence
from datetime import datetime

from omega_lib.theme.policies import DEFAULT_EXPORT_THEME, EXPORT_PALETTES

from omega_tail.domain.blacklist import ORIGIN_LABELS, BlackEntry, export_text
from omega_tail.domain.report import report_stamp
from omega_tail.interfaces.shared.help_view import _style
from omega_tail.shared.i18n import TRANSLATOR, _


def origin_label(origin: str) -> str:
    return _(ORIGIN_LABELS.get(origin, origin))


def render_html(entries: Sequence[BlackEntry], *, version: str, machine: str, when: datetime,
                theme: str = DEFAULT_EXPORT_THEME) -> str:
    theme = theme if theme in EXPORT_PALETTES else DEFAULT_EXPORT_THEME
    title = _("OMEGA-TAIL {version} — LISTE NOIRE DE LA PORTE ({machine})").format(version=version, machine=machine)
    note = _("Établie le {date} : {count} entrée(s), la plus ancienne d'abord. L'export TXT se réimporte "
             "tel quel.").format(date=when.strftime("%Y-%m-%d %H:%M"), count=len(entries))
    head = "".join(f"<th>{html.escape(column)}</th>" for column in ("N°", _("Adresse ou réseau"), _("Ajoutée le"),
                                                                    _("Origine")))
    rows = "".join(f"<tr><td>{number}</td><td>{html.escape(entry.address)}</td>"
                   f"<td>{entry.added.strftime('%Y-%m-%d %H:%M')}</td><td>{html.escape(origin_label(entry.origin))}"
                   "</td></tr>" for number, entry in enumerate(entries, start=1))
    css = _style(f"palette_{theme}.css") + "\n" + _style("base.css")
    return (f'<!DOCTYPE html>\n<html lang="{TRANSLATOR.html_lang()}" dir="{TRANSLATOR.html_dir()}">\n'
            '<head>\n<meta charset="UTF-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
            f"<title>{html.escape(_('Liste noire - Omega-Tail'))}</title>\n<style>\n{css}\n</style>\n</head>\n<body>\n"
            '<div class="container"><div class="terminal-header"><div class="terminal-dots">'
            '<span class="dot dot-close"></span><span class="dot dot-min"></span><span class="dot dot-max"></span>'
            '</div><span class="terminal-title">omega-tail -- liste noire</span></div>\n<div class="terminal-body">\n'
            f'<h1>{html.escape(title)}<span class="cursor"></span></h1>\n'
            f'<div class="note-historique"><span class="note-prefix">[OMEGA-TAIL {html.escape(version)}]</span> '
            f"{html.escape(note)}</div>\n"
            f'<div class="table-wrapper"><table><thead><tr>{head}</tr></thead><tbody>{rows}</tbody></table></div>\n'
            "</div></div>\n</body>\n</html>\n")


def render_json(entries: Sequence[BlackEntry], *, version: str, machine: str, when: datetime) -> str:
    data = {"outil": "omega-tail", "version": version, "date": when.isoformat(timespec="seconds"),
            "machine": machine, "liste_noire": [{"adresse": entry.address,
                                                 "ajout": entry.added.isoformat(timespec="seconds"),
                                                 "origine": entry.origin} for entry in entries]}
    return json.dumps(data, indent=2, ensure_ascii=False) + "\n"


def render(entries: Sequence[BlackEntry], file_format: str, *, version: str, machine: str, when: datetime,
           theme: str = DEFAULT_EXPORT_THEME) -> tuple[str, str]:
    """(contenu, nom du fichier)."""
    name = f"omega-tail-liste-noire-{report_stamp(when)}"
    if file_format == "html":
        return render_html(entries, version=version, machine=machine, when=when, theme=theme), f"{name}.html"
    if file_format == "json":
        return render_json(entries, version=version, machine=machine, when=when), f"{name}.json"
    return export_text(entries), f"{name}.txt"
