# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Rapport de la machine (lot 7) en sections traduites, puis en texte, HTML (theme d'export d'omega-lib, meme cadre
que l'aide) ou JSON. Faits seulement, sans jargon de ligne de commande. Utilise par `omega-tail rapport` et par
l'ecran Rapport."""
from __future__ import annotations

import html
import json
from dataclasses import dataclass, field

from omega_lib.theme.policies import DEFAULT_EXPORT_THEME, EXPORT_PALETTES

from omega_tail.application.gate import BLACK, TRUSTED, TableRow
from omega_tail.application.groups import GroupRow
from omega_tail.application.report import GateFacts, ReportFacts
from omega_tail.domain.gate import MODE_OBSERVATION
from omega_tail.domain.groups import GROUPS_APPLY, reason_pairs
from omega_tail.domain.report import Refusals, report_stamp
from omega_tail.interfaces.shared.help_view import STYLES, _style
from omega_tail.interfaces.shared.messages import group_label, localized
from omega_tail.interfaces.shared.presentation import (
    BACKEND_LABELS,
    alert_text,
    publication_line,
    service_line,
    shield_summary,
    size,
)
from omega_tail.shared.i18n import N_, TRANSLATOR, _

GATE_REASON_LABELS = {
    "liste-noire": N_("liste noire"), "bloquee": N_("adresse bloquée"), "budget": N_("budget global dépassé"),
    "debit-adresse": N_("trop de connexions d'une adresse"), "debit-prefixe": N_("trop de connexions d'un réseau"),
    "pas-tls": N_("pas une connexion TLS"), "nom": N_("mauvais nom de site (SNI)"),
    "empreinte": N_("empreinte inconnue en rafale"), "hebergeur": N_("AS d'hébergeur en rafale"),
    "pays": N_("pays limité en rafale"),
}
FORMATS = ("txt", "html", "json")


@dataclass(frozen=True)
class Section:
    key: str
    title: str
    lines: tuple[str, ...] = ()
    columns: tuple[str, ...] = ()
    rows: tuple[tuple[str, ...], ...] = ()
    data: dict[str, object] = field(default_factory=dict)
    """Faits bruts pour le JSON."""


def _reason(key: str) -> str:
    return _(GATE_REASON_LABELS[key]) if key in GATE_REASON_LABELS else key


def _tailscale(facts: ReportFacts) -> Section:
    snapshot = facts.snapshot
    tailscale = snapshot.tailscale
    lines = [_("Service tailscaled : {state}").format(state=service_line(snapshot.service))]
    if not tailscale.installed:
        lines.append(_("Tailscale n'est pas installé."))
        return Section("tailscale", "TAILSCALE", tuple(lines))
    if not tailscale.reachable:
        lines.append(_("tailscaled ne répond pas : {error}").format(error=tailscale.error or "—"))
        return Section("tailscale", "TAILSCALE", tuple(lines))
    lines += [
        _("État : {state}").format(state=_(BACKEND_LABELS[tailscale.backend])),
        _("Version : {daemon} en marche, {client} installé").format(daemon=tailscale.daemon_version or "—",
                                                                    client=tailscale.client_version or "—"),
        _("Nom de la machine : {name}").format(name=tailscale.dns_name or tailscale.host_name or "—"),
        _("Compte : {user}").format(user=tailscale.user or "—") if facts.include_private
        else _("Compte : masqué (non inclus dans ce rapport)"),
    ]
    if facts.device_counts is not None:
        online, total, relays = facts.device_counts
        lines.append(_("Appareils du tailnet : {online} en ligne sur {total} (plus {relays} relais Funnel de "
                       "Tailscale)").format(online=online, total=total, relays=relays))
    else:
        lines.append(_("Appareils du tailnet : {online} en ligne sur {total}").format(
            online=tailscale.peers_online, total=tailscale.peers_total))
    lines.append(_("Clé de la machine : {expiry}").format(
        expiry=tailscale.key_expiry.strftime("%Y-%m-%d") if tailscale.key_expiry else _("sans expiration")))
    lines.append(_("Opérateur : {operator}").format(operator=snapshot.preferences.operator or _("aucun")))
    rows = tuple((name, value) for name, value in sorted(snapshot.preferences.values.items()))
    return Section("tailscale", "TAILSCALE", tuple(lines), (_("Préférence"), _("Valeur")), rows,
                   {"version": tailscale.daemon_version, "etat": tailscale.backend.value,
                    "preferences": dict(snapshot.preferences.values)})


def _publication(facts: ReportFacts) -> Section:
    items = facts.snapshot.publications
    lines = tuple(publication_line(item) for item in items) or (_("Rien n'est publié (ni Serve, ni Funnel)."),)
    return Section("publication", _("PUBLICATION"), lines)


def _machine(facts: ReportFacts) -> Section:
    snapshot = facts.snapshot
    machine = snapshot.machine
    cpu = machine.tailscaled_cpu_percent
    memory = machine.memory_used_percent
    lines = (
        _("Machine : {name} ({count} fils)").format(name=machine.hostname or "—", count=machine.cpu_count),
        _("Charge : {a:.2f} {b:.2f} {c:.2f}").format(a=machine.load[0], b=machine.load[1], c=machine.load[2]),
        _("Température : {value}").format(
            value=f"{machine.temperature_c:.0f} °C" if machine.temperature_c is not None else _("pas de capteur")),
        _("Mémoire vive utilisée : {value}").format(value=f"{memory:.0f} %" if memory is not None else "—"),
        _("tailscaled : {cpu} d'un cœur, {memory}").format(
            cpu=f"{cpu:.0f} %" if cpu is not None else "—", memory=size(machine.tailscaled_rss_bytes)),
    )
    return Section("machine", _("MACHINE"), lines)


def _group_rows(rows: tuple[GroupRow, ...]) -> str:
    return ", ".join(f"{row.key}{' (' + group_label(row) + ')' if row.label or row.hosting else ''} {row.count}"
                     for row in rows)


def _gate(facts: ReportFacts) -> Section:
    gate: GateFacts | None = facts.gate
    if gate is None:
        return Section("porte", _("PARE-FEU FUNNEL"), (_("Pare-feu indisponible sur cette machine."),))
    service = facts.snapshot.gate_service
    lines = []
    if service is not None and service.known:
        lines.append(_("Service de la porte : {state}").format(state=service_line(service)))
    if gate.state is not None:
        lines.append(_("Protection active depuis {since} : Funnel {port} → porte → {backend}").format(
            since=gate.state.since[:16].replace("T", " "), port=gate.state.public_port, backend=gate.state.backend))
        lines.append(_("Connexions depuis le démarrage de la porte : {total} reçues · {refused} refusées avant "
                       "chiffrement · {admitted} admises · {current} en cours").format(
            total=gate.counters.total, refused=gate.counters.refused, admitted=gate.counters.admitted,
            current=gate.counters.current))
    else:
        lines.append(_("Protection inactive : Funnel ne passe pas par la porte."))
    policy = gate.policy
    lines.append(_("Mode : {mode}").format(mode=_("observation (rien n'est refusé)") if policy.mode == MODE_OBSERVATION
                                           else _("normal (les règles refusent)")))
    lines.append(_("Règles : {ip} connexions / 10 s par adresse · {prefix} / 10 s par réseau · budget global {budget} "
                   "/ s · {maximum} connexions au plus · blocage {block} min · nom du site {sni}").format(
        ip=policy.ip_per_10s, prefix=policy.prefix_per_10s, budget=policy.global_per_s,
        maximum=policy.max_connections, block=policy.block_minutes,
        sni=_("vérifié") if policy.check_sni else _("non vérifié")))
    if gate.certificate_days is not None:
        lines.append(_("Certificat : encore {days} jour(s)").format(days=gate.certificate_days))
    lines.append(_("Confiance : {count} adresse(s) ou réseau(x)").format(count=len(gate.trusted)))
    lines.append(_("Liste noire : {entries}").format(entries=", ".join(gate.black) or _("vide")))
    if gate.blocked:
        lines.append(_("Bloquées en ce moment : {entries}").format(entries=", ".join(
            f"{row.address} ({row.expires_s // 60} min)" for row in gate.blocked)))
    else:
        lines.append(_("Bloquées en ce moment : aucune"))
    status = gate.groups
    if status is not None:
        applied = status.policy.mode == GROUPS_APPLY
        lines.append(_("Regroupements : {mode} · {attack}").format(
            mode=_("appliqués") if applied else _("en observation"),
            attack=_("MODE ATTAQUE en cours") if status.attack else _("mode normal")))
        lines.append(_("Empreintes : apprentissage, encore {days} jour(s)").format(days=status.learning_days_left)
                     if status.learning_days_left else
                     _("Empreintes habituelles : {count} (référence prête)").format(count=status.known))
        lines.append(_("Base AS / pays : à jour il y a {days} jour(s)").format(days=status.base_days)
                     if status.base_days is not None else _("Base AS / pays : absente"))
        for title, found in ((_("Empreintes les plus actives"), gate.top_fingerprints),
                             (_("AS les plus actifs"), gate.top_as), (_("Pays les plus actifs"), gate.top_countries)):
            if found:
                lines.append(f"{title} : {_group_rows(found)}")
    rows = tuple((row.address, str(row.rate_10s), _state(row)) for row in gate.busiest)
    return Section("porte", _("PARE-FEU FUNNEL"), tuple(lines),
                   (_("Adresse la plus active"), _("Connexions / 10 s"), _("État")) if rows else (), rows,
                   {"actif": gate.state is not None, "mode": policy.mode, "recues": gate.counters.total,
                    "refusees": gate.counters.refused, "admises": gate.counters.admitted,
                    "liste_noire": list(gate.black), "bloquees": [row.address for row in gate.blocked],
                    "regroupements": status.policy.mode if status is not None else None})


def _state(row: TableRow) -> str:
    if row.listed == BLACK:
        return _("liste noire")
    if row.listed == TRUSTED:
        return _("confiance")
    return _("bloquée") if row.blocked else _("admise")


def _survival(facts: ReportFacts) -> Section:
    snapshot = facts.snapshot
    lines = [_("Confinement de tailscaled : {state}").format(
        state=_("oui") if snapshot.service.confined else _("non") if snapshot.service.known else "—")]
    watch = facts.watch
    if watch is None or not watch.installed:
        lines.append(_("Veille automatique : désactivée"))
    elif not watch.alive:
        lines.append(_("Veille automatique : activée mais arrêtée (aucun signe de vie)"))
    else:
        lines.append(_("Veille automatique : active · {strikes} dépassement(s) récent(s) · prochaine coupure "
                       "{minutes} min").format(strikes=watch.strikes, minutes=watch.next_minutes))
    breaker = facts.breaker
    lines.append(_("Disjoncteur : tailscaled au-delà de {cpu:.0f} % d'un cœur pendant {seconds} s, ou machine au-delà "
                   "de {temperature:.0f} °C ; coupure proposée de {minutes} min").format(
        cpu=breaker.cpu_percent, seconds=breaker.seconds, temperature=breaker.temperature_c,
        minutes=breaker.minutes))
    cut = snapshot.cut
    if cut is not None:
        lines.append(_("Funnel coupé depuis {since} ; remise en route {until}").format(
            since=cut.cut_at[:16].replace("T", " "),
            until=cut.until[:16].replace("T", " ") if cut.until else _("manuelle")))
    else:
        lines.append(_("Aucune coupure de Funnel en cours."))
    lines.append(shield_summary(snapshot.shield))
    shield = snapshot.shield
    if shield is not None and shield.installed:
        lines.append(_("  origine : {tool} · géré par {manager} · pairs connus : {peers}").format(
            tool=shield.requested_by or "?", manager=shield.manager or "?",
            peers=shield.status.peers if shield.status is not None else 0))
    if facts.watch_journal:
        lines.append(_("Journal de la veille (derniers événements) :"))
        lines += [f"  {line}" for line in facts.watch_journal]
    return Section("survie", _("SURVIE"), tuple(lines))


def _alerts(facts: ReportFacts) -> Section:
    lines = tuple(alert_text(alert) for alert in facts.alerts) or (_("Aucune alerte."),)
    return Section("alertes", _("ALERTES"), lines, data={"alertes": [alert.code for alert in facts.alerts]})


def _attacks(facts: ReportFacts) -> Section:
    found: Refusals = facts.refusals
    title = _("ATTAQUES DES {days} DERNIERS JOURS").format(days=found.days)
    if facts.gate is None:
        return Section("attaques", title, (_("Pare-feu indisponible : rien à compter."),))
    if found.error:
        lines = [_("Journal de la porte illisible : {error}").format(error=localized(found.error))]
        if found.hint:
            lines.append(_(found.hint))
        return Section("attaques", title, tuple(lines))
    gate_observing = facts.gate.policy.mode == MODE_OBSERVATION
    groups = facts.gate.groups
    groups_applied = groups is not None and groups.policy.mode == GROUPS_APPLY
    lines = [_("Lu dans le journal de la porte : chaque connexion marquée par une règle (refusée, ou seulement "
               "comptée en observation, selon le mode du moment).")]
    if not found.total:
        lines.append(_("Aucune connexion marquée sur la période."))
    else:
        lines.append(_("Connexions marquées : {count}{floor}").format(
            count=found.total, floor=_(" (au moins : journal trop long, seules les plus récentes ont été lues)")
            if found.truncated else ""))
        if found.by_reason:
            text = (_("Règles de la porte, connexions qui auraient été refusées (observation) : {reasons}")
                    if gate_observing else _("Règles de la porte, connexions refusées : {reasons}"))
            lines.append(text.format(reasons=", ".join(
                f"{_reason(key)} {count}" for key, count in found.by_reason.items())))
        if found.groups:
            text = (_("Regroupements, connexions refusées : {reasons}") if groups_applied
                    else _("Regroupements, connexions qui auraient été refusées (observation) : {reasons}"))
            lines.append(text.format(reasons=", ".join(
                f"{_(label)} {count}" for label, count in reason_pairs(found.groups))))
        lines.append(_("Par jour : {days}").format(days=", ".join(
            f"{day} {count}" for day, count in found.by_day.items())))
    rows = tuple((address, str(count), asn or "—", country or "—")
                 for address, count, asn, country in found.addresses)
    return Section("attaques", title, tuple(lines),
                   (_("Adresse"), _("Connexions marquées"), _("AS"), _("Pays")) if rows else (), rows,
                   {"jours": found.days, "total": found.total, "motifs": dict(found.by_reason),
                    "regroupements": dict(found.groups), "par_jour": dict(found.by_day),
                    "incomplet": found.truncated})


def _devices(facts: ReportFacts) -> Section:
    rows = tuple((device.name, device.os or "—", _("en ligne") if device.online else _("hors ligne"),
                  device.address or "—") for device in facts.devices)
    return Section("appareils", _("APPAREILS DU TAILNET"),
                   () if rows else (_("Aucun appareil lu."),), (_("Nom"), _("Système"), _("État"), _("Adresse")),
                   rows)


def sections(facts: ReportFacts) -> list[Section]:
    found = [_tailscale(facts), _publication(facts), _machine(facts), _gate(facts), _survival(facts),
             _alerts(facts), _attacks(facts)]
    if facts.include_private:
        found.append(_devices(facts))
    return found


def _header(facts: ReportFacts) -> list[str]:
    machine = facts.snapshot.machine.hostname or facts.snapshot.tailscale.host_name or "?"
    privacy = _("Compte et appareils du tailnet inclus.") if facts.include_private else _(
        "Compte et appareils du tailnet non inclus (seulement leur nombre) ; les adresses des attaquants restent.")
    return [_("OMEGA-TAIL {version} — RAPPORT DE LA MACHINE {machine}").format(version=facts.version,
                                                                             machine=machine),
            _("Établi le {date} (lecture seule, sans droits).").format(
                date=facts.generated_at.strftime("%Y-%m-%d %H:%M")), privacy]


def _table_text(section: Section) -> list[str]:
    if not section.rows:
        return []
    widths = [max(len(str(cell)) for cell in column) for column in zip(section.columns, *section.rows, strict=False)]
    lines = ["  " + "  ".join(str(cell).ljust(width) for cell, width in zip(section.columns, widths, strict=False))]
    lines += ["  " + "  ".join(str(cell).ljust(width) for cell, width in zip(row, widths, strict=False)).rstrip()
              for row in section.rows]
    return lines


def render_text(facts: ReportFacts) -> str:
    rule = "=" * 78
    lines = [rule, *_header(facts), rule]
    for section in sections(facts):
        lines += ["", section.title]
        lines += [f"  {line}" for line in section.lines]
        lines += _table_text(section)
    return "\n".join(lines) + "\n"


def render_html(facts: ReportFacts, theme: str = DEFAULT_EXPORT_THEME) -> str:
    theme = theme if theme in EXPORT_PALETTES else DEFAULT_EXPORT_THEME
    header = _header(facts)
    body = [f'<h1>{html.escape(header[0])}<span class="cursor"></span></h1>',
            f'<div class="note-historique"><span class="note-prefix">[OMEGA-TAIL {html.escape(facts.version)}]'
            f"</span> {html.escape(header[1])} {html.escape(header[2])}</div>"]
    for section in sections(facts):
        body.append(f"<h2>{html.escape(section.title)}</h2>")
        if section.lines:
            body.append('<ul class="note-list">' + "".join(f"<li>{html.escape(line)}</li>" for line in section.lines)
                        + "</ul>")
        if section.rows:
            head = "".join(f"<th>{html.escape(column)}</th>" for column in section.columns)
            rows = "".join("<tr>" + "".join(f"<td>{html.escape(str(cell))}</td>" for cell in row) + "</tr>"
                           for row in section.rows)
            body.append(f'<div class="table-wrapper"><table><thead><tr>{head}</tr></thead><tbody>{rows}</tbody>'
                        "</table></div>")
    footer = _("OMEGA-TAIL {version} — rapport.").format(version=facts.version)
    body.append(f'<div class="footer-note">{html.escape(footer)}</div>')
    css = _style(f"palette_{theme}.css") + "\n" + _style("base.css")
    return (f'<!DOCTYPE html>\n<html lang="{TRANSLATOR.html_lang()}" dir="{TRANSLATOR.html_dir()}">\n'
            '<head>\n<meta charset="UTF-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
            f"<title>{html.escape(_('Rapport - Omega-Tail'))}</title>\n<style>\n{css}\nh2 {{ margin-top: 1.6rem; }}\n"
            "</style>\n</head>\n<body>\n"
            '<div class="container"><div class="terminal-header"><div class="terminal-dots">'
            '<span class="dot dot-close"></span><span class="dot dot-min"></span><span class="dot dot-max"></span>'
            '</div><span class="terminal-title">omega-tail -- rapport</span></div>\n'
            '<div class="terminal-body">\n' + "\n".join(body) + "\n</div></div>\n</body>\n</html>\n")


def render_json(facts: ReportFacts) -> str:
    data = {"outil": "omega-tail", "version": facts.version, "date": facts.generated_at.isoformat(),
            "machine": facts.snapshot.machine.hostname, "prive_inclus": facts.include_private,
            "sections": [{"cle": section.key, "titre": section.title, "lignes": list(section.lines),
                          "colonnes": list(section.columns), "tableau": [list(row) for row in section.rows],
                          "faits": section.data} for section in sections(facts)]}
    return json.dumps(data, indent=2, ensure_ascii=False) + "\n"


def render(facts: ReportFacts, file_format: str, theme: str = DEFAULT_EXPORT_THEME) -> tuple[str, str]:
    """(contenu, extension)."""
    if file_format == "json":
        return render_json(facts), "json"
    if file_format == "html":
        return render_html(facts, theme), "html"
    return render_text(facts), "txt"


def export_name(facts: ReportFacts, extension: str) -> str:
    return f"omega-tail-rapport-{report_stamp(facts.generated_at)}.{extension}"


__all__ = ["FORMATS", "STYLES", "Section", "export_name", "render", "render_html", "render_json", "render_text",
           "sections"]
