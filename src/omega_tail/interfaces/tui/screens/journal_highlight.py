# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Couleurs des lignes de l'écran Journaux (demande, 2026-11-25 : « des grandes lignes blanches, c'est
assez indigeste » ; même principe que le viewer Simple d'omega-serv, log_line_highlight.py).

Une nuance par information, prises dans les variables du thème courant (`text-primary`, `text-success`…) : les
couleurs suivent le thème choisi, aucun thème à retoucher.
- tailscaled (`journalctl -o short-iso`) : date, machine (grisée), processus, puis la catégorie du message
  (`control:`, `magicsock:`, `dns:`, `wgengine:`…) colorée par famille ; le message garde la couleur du texte,
  rouge s'il signale une erreur, orange un avertissement ; adresses IP en gras.
- porte (format tcplog d'HAProxy, domain/groups.py LOG_FORMAT) : adresse du visiteur, date, entrée et sortie de la
  porte, état de fin, puis motif (refus, en rouge), groupe, empreinte, AS et pays.
La ligne reste du texte brut (Text, jamais du balisage Rich : elle peut contenir ce qu'envoie un visiteur) ; seules
des plages en sont colorées."""
from __future__ import annotations

import re
from collections.abc import Mapping
from dataclasses import dataclass

from rich.style import Style
from rich.text import Text

_ISO_DATE = re.compile(r"^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(?:[.,]\d+)?(?:[+-]\d\d:?\d\d|Z)?")
_SYSLOG_DATE = re.compile(r"^\S{3,5}\s+\d{1,2}\s+\d\d:\d\d:\d\d")
_HEAD = re.compile(r"\s+(?P<host>\S+)\s+(?P<tag>[\w.@/-]+(?:\[\d+\])?):\s")
_CATEGORY_PART = re.compile(r"[A-Za-z][\w.-]{1,30}(?:\([^)]{0,40}\))?: ")
_IPV4 = re.compile(r"(?<![\w.])(?:\d{1,3}\.){3}\d{1,3}(?:/\d{1,2})?(?::\d{1,5})?(?![\w.])")
_IPV6 = re.compile(r"(?<![\w:])\[?(?:[0-9a-fA-F]{1,4}:){2,7}[0-9a-fA-F]{0,4}(?:/\d{1,3})?\]?(?::\d{1,5})?(?![\w:])")
_BRACKETS = re.compile(r"\[[^\]\s]{1,40}\]")
_ERROR = re.compile(r"\b(error|errors|err|failed|failure|fatal|panic|denied|alert|critical|crit|emerg)\b", re.I)
_WARNING = re.compile(r"\b(warn|warning|warnings|timeout|timed out|retry|retrying|unable|unexpected|notice)\b",
                      re.I)
_GATE = re.compile(r"(?P<ip>\S+):(?P<port>\d+) (?P<date>\[[^\]]+\]) (?P<front>\S+) (?:(?P<back>\S+/\S+) "
                   r"(?P<times>\S+) (?P<bytes>\d+) (?P<state>\S{2,4}) |(?P<early>avant-tls) )")
_PAIR = re.compile(r"\b(motif|groupe|ja4|as|pays)=(\S*)")

_FAMILIES: dict[str, tuple[str, ...]] = {
    "control": ("control", "controlclient", "ipnlocal", "ipnserver", "ipn", "auth", "logtail", "health", "policy",
                "localapi", "tsweb", "taildrop", "ssh", "cert", "serve", "funnel", "update", "clientupdate",
                "localbackend"),
    "network": ("magicsock", "derp", "derphttp", "netcheck", "portmapper", "peerapi", "disco", "netmon", "monitor",
                "udprelay", "relayserver", "linkchange"),
    "dns": ("dns", "resolver", "dnsfallback", "forward", "resolv.conf"),
    "engine": ("wgengine", "wg", "router", "netstack", "tstun", "linuxfw", "netfilter", "wireguard", "tun",
               "magicsock-wg", "flowtrack", "conntrack", "accept", "drop", "filter"),
}


@dataclass(frozen=True)
class JournalPalette:
    date: Style
    muted: Style
    process: Style
    ip: Style
    families: Mapping[str, Style]
    other_family: Style
    error: Style
    warning: Style
    error_bold: Style
    warning_bold: Style
    good: Style
    gate: Style
    country: Style
    autonomous: Style


def palette_from_theme(variables: Mapping[str, str]) -> JournalPalette:
    def color(name: str, fallback: str) -> Style:
        value = variables.get(name) or fallback
        try:
            return Style.parse(value)
        except Exception:  # noqa: BLE001 - une valeur du thème illisible par Rich (transparence…) : repli
            return Style.parse(fallback)

    primary, secondary = color("text-primary", "blue"), color("text-secondary", "cyan")
    success, accent = color("text-success", "green"), color("text-accent", "magenta")
    warning, error = color("text-warning", "yellow"), color("text-error", "red")
    bold, italic = Style(bold=True), Style(italic=True)
    return JournalPalette(
        date=secondary, muted=Style(dim=True), process=primary + bold, ip=accent + bold,
        families={"control": primary, "network": success, "dns": secondary + italic, "engine": primary + italic},
        other_family=Style(bold=True), error=error, warning=warning, error_bold=error + bold,
        warning_bold=warning + bold, good=success + bold, gate=primary, country=accent, autonomous=secondary)


def family(category: str) -> str:
    """Famille d'une catégorie de tailscaled (« magicsock », « dns »…), d'après son premier mot."""
    word = category.split(":", 1)[0].split("(", 1)[0].strip().lower()
    return next((name for name, words in _FAMILIES.items() if word in words), "")


def highlight_journal_line(line: str, palette: JournalPalette) -> Text:
    text = Text(line, no_wrap=True)
    date = _ISO_DATE.match(line) or _SYSLOG_DATE.match(line)
    body = 0
    if date is not None:
        text.stylize(palette.date, 0, date.end())
        head = _HEAD.match(line, date.end())
        if head is not None:
            text.stylize(palette.muted, head.start("host"), head.end("host"))
            text.stylize(palette.process, head.start("tag"), head.end("tag") + 1)
            body = head.end()
    gate = _GATE.match(line, body)
    if gate is not None:
        _highlight_gate(text, line, gate, palette)
        return text
    _highlight_message(text, line, body, palette)
    return text


def _highlight_message(text: Text, line: str, start: int, palette: JournalPalette) -> None:
    message = start
    while (part := _CATEGORY_PART.match(line, message)) is not None and not _ERROR.match(part.group(0)) \
            and not _WARNING.match(part.group(0)):
        message = part.end()  # « dns: resolver: forward: » ; s'arrête avant « error: » (gravité, pas catégorie)
    if message > start:
        name = family(line[start:message])
        text.stylize(palette.families.get(name, palette.other_family), start, message - 1)
    if _ERROR.search(line, message):
        text.stylize(palette.error, message, len(line))
    elif _WARNING.search(line, message):
        text.stylize(palette.warning, message, len(line))
    for found in _BRACKETS.finditer(line, message):
        text.stylize(palette.muted, found.start(), found.end())
    _stylize_addresses(text, line, message, palette.ip)
    for found in _ERROR.finditer(line, message):
        text.stylize(palette.error_bold, found.start(), found.end())
    for found in _WARNING.finditer(line, message):
        text.stylize(palette.warning_bold, found.start(), found.end())


def _highlight_gate(text: Text, line: str, match: re.Match[str], palette: JournalPalette) -> None:
    text.stylize(palette.ip, match.start("ip"), match.end("ip"))
    text.stylize(palette.muted, match.start("port") - 1, match.end("port"))
    text.stylize(palette.date, match.start("date"), match.end("date"))
    text.stylize(palette.gate, match.start("front"), match.end("front"))
    if match.group("early") is not None:
        text.stylize(palette.error_bold, match.start("early"), match.end("early"))
    else:
        text.stylize(palette.gate, match.start("back"), match.end("back"))
        text.stylize(palette.muted, match.start("times"), match.end("bytes"))
        state = match.group("state")
        text.stylize(palette.good if state.startswith("--") else palette.warning_bold, match.start("state"),
                     match.end("state"))
        first_pair = _PAIR.search(line, match.end())
        text.stylize(palette.muted, match.end("state"), first_pair.start() if first_pair is not None else len(line))
    for pair in _PAIR.finditer(line, match.end()):
        key, value = pair.group(1), pair.group(2)
        text.stylize(palette.muted, pair.start(1), pair.end(1) + 1)
        if not value or value == "-":
            text.stylize(palette.muted, pair.start(2), pair.end(2))
            continue
        style = {"motif": palette.error_bold, "groupe": palette.warning_bold, "ja4": palette.muted,
                 "as": palette.autonomous, "pays": palette.country}[key]
        text.stylize(style, pair.start(2), pair.end(2))


def _stylize_addresses(text: Text, line: str, start: int, style: Style) -> None:
    for regex in (_IPV4, _IPV6):
        for found in regex.finditer(line, start):
            if regex is _IPV6 and found.group(0).count(":") < 2:
                continue
            text.stylize(style, found.start(), found.end())
