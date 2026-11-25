# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Pare-feu Funnel (lot 4, plan B) : la porte avant TLS, faite par HAProxy et pilotee par omega-tail.

Montage (etude §5, mesure lot 0 : refus avant TLS = 4,6 fois moins de CPU, admis = 2 fois moins) :
  Internet -> relais Funnel -> tailscaled (`funnel --tcp=443 --proxy-protocol=2`, TLS NON termine)
  -> 127.0.0.1:<port de la porte> (HAProxy : adresse reelle par PROXY v2, regles AVANT toute cryptographie,
  lecture du ClientHello) -> second etage interne (TLS des seules connexions admises) -> service d'origine (HTTP,
  X-Forwarded-For REMPLACE par l'adresse reelle).

Regles dans l'ordre : confiance et tailnet (jamais limites) ; liste noire permanente ; bloquee pour la duree choisie ;
budget global de nouvelles connexions par seconde ; debit par adresse puis par prefixe (/24, /64) sur 10 s - un
depassement bloque l'adresse pour la duree choisie ; ClientHello absent ou nom visé different de celui de la machine.
Mode observation : tout est compte et marque, rien n'est refuse (pour regler les seuils sans risque).

Les nombres viennent toujours de la configuration validee (bornes ci-dessous) : aucun texte libre n'entre dans le
fichier d'HAProxy, sauf le nom de la machine et la cible, verifies par motif."""
from __future__ import annotations

import ipaddress
import re
import shlex
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any
from urllib.parse import urlsplit

from omega_tail.core.constants import TAILSCALE_COMMAND
from omega_tail.domain.funnel import handlers_of
from omega_tail.domain.groups import (
    ERROR_LOG_FORMAT,
    GROUPS_APPLY,
    LOG_FORMAT,
    GroupsPolicy,
    acl_lines,
    budget_exemption,
    content_lines,
    global_lines,
    session_lines,
    tables,
)
from omega_tail.shared.i18n import N_

MODE_NORMAL = "normal"
MODE_OBSERVATION = "observation"
DEFAULT_GATE_PORT = 9443
TABLE_IP = "porte_ip"
TABLE_PREFIX = "porte_prefixe"
TABLE_GLOBAL = "porte_budget"
TABLE_IP_SIZE = "200k"
TABLE_PREFIX_SIZE = "100k"
"""Places des tables par adresse et par prefixe (2026-11-25, MESURES_DEBIT_MEMOIRE.md) : ~214 octets par adresse,
1 million de places pouvaient porter HAProxy a ~256 Mo sous une attaque tres distribuee. Pleine, une table evince
ses entrees les plus anciennes (verifie sur HAProxy 3.4) : une adresse qui attaque encore reste suivie. Pire cas
borne a ~45 + ~20 Mo ; un petit site n'approche jamais 200 000 adresses en une heure."""
FRONTEND = "porte"
TRUST_LIST = "confiance.lst"
TAILNET_NETWORKS = ("100.64.0.0/10", "fd7a:115c:a1e0::/48")
"""Adresses du tailnet (IPv4 et IPv6 de Tailscale), toujours admises par la porte, avant toute regle (decision du
2026-11-24) : omega-tail protege Funnel d'Internet mais laisse les machines du tailnet tranquilles. Un
visiteur de Funnel arrive avec son adresse publique (en-tete PROXY), jamais avec une adresse de ces reseaux."""
BLACK_LIST = "noire.lst"
BLACK_JSON = "noire.json"
"""Dates et origines des entrees de la liste noire (noire.lst en est genere)."""
SERVICE_UNIT = "omega-tail-porte.service"
_DNS_NAME = re.compile(r"^[a-z0-9]([a-z0-9-]*[a-z0-9])?(\.[a-z0-9]([a-z0-9-]*[a-z0-9])?)+$")
_HOST = re.compile(r"^(\[[0-9a-fA-F:]+\]|[A-Za-z0-9.-]+)$")


@dataclass(frozen=True)
class GatePolicy:
    """Valeurs par defaut prudentes pour un petit site (un navigateur ouvre quelques connexions et les garde)."""
    mode: str = MODE_NORMAL
    ip_per_10s: int = 40
    prefix_per_10s: int = 200
    global_per_s: int = 100
    max_connections: int = 500
    block_minutes: int = 60
    check_sni: bool = True


LIMITS = {"ip_per_10s": (2, 10_000), "prefix_per_10s": (2, 100_000), "global_per_s": (1, 100_000),
          "max_connections": (10, 100_000), "block_minutes": (1, 10_080)}


def policy_from(values: Mapping[str, Any]) -> GatePolicy:
    """Politique depuis les reglages ; une valeur absente ou hors bornes reprend sa valeur par defaut."""
    base = GatePolicy()
    numbers = {}
    for key, (low, high) in LIMITS.items():
        try:
            value = int(str(values.get(key, getattr(base, key))).strip())
        except ValueError:
            value = getattr(base, key)
        numbers[key] = value if low <= value <= high else getattr(base, key)
    mode = values.get("mode", base.mode)
    check = str(values.get("check_sni", base.check_sni)).lower() not in ("false", "0", "non")
    return GatePolicy(mode=mode if mode in (MODE_NORMAL, MODE_OBSERVATION) else base.mode, check_sni=check,
                      **numbers)


@dataclass(frozen=True)
class Backend:
    address: str
    """hote:port du service d'origine."""
    tls: bool = False
    verify: bool = False
    """`https://` : tailscaled verifie le certificat du service, la porte aussi (seul `https+insecure://` s'en passe ;
    scan de securite 2026-11-25, F5)."""
    name: str = ""
    """Nom d'hote tel qu'ecrit dans la cible (SNI et verification du nom ; vide si c'est une adresse IP)."""


@dataclass(frozen=True)
class GateTarget:
    """Ce que la porte remplace : un port public servi en HTTPS par tailscaled, un seul chemin « / »."""
    public_port: int
    dns_name: str
    backend: Backend


class UnsupportedPublication(ValueError):
    """La publication actuelle n'entre pas dans ce que la porte sait proteger (version 1)."""


# Raisons affichees (lot 9) : la phrase se traduit, le detail apres « : » garde sa forme (interfaces.shared.messages)
TARGET_UNSUPPORTED = N_("cible non prise en charge")
UNEXPECTED_NAME = N_("nom de machine inattendu")


def backend_of(target: str) -> Backend:
    parts = urlsplit(target if "://" in target else f"http://{target}")
    if parts.scheme not in ("http", "https", "https+insecure") or not parts.hostname:
        raise UnsupportedPublication(f"{TARGET_UNSUPPORTED} : {target}")
    host = parts.hostname
    if host == "localhost":
        host = "127.0.0.1"
    shown = f"[{host}]" if ":" in host else host
    if not _HOST.match(shown) or (parts.path not in ("", "/")):
        raise UnsupportedPublication(f"{TARGET_UNSUPPORTED} : {target}")
    port = parts.port or (443 if parts.scheme.startswith("https") else 80)
    verify = parts.scheme == "https"
    return Backend(f"{shown}:{port}", tls=parts.scheme.startswith("https"), verify=verify,
                   name=parts.hostname if verify and not _is_ip(parts.hostname) else "")


def _is_ip(host: str) -> bool:
    try:
        ipaddress.ip_address(host)
    except ValueError:
        return False
    return True


def backend_tls_options(backend: Backend) -> str:
    """Options de la ligne `server origine`. `https+insecure://` : sans verification, comme tailscaled. `https://` :
    certificat verifie par les autorites du systeme, et le nom quand la cible en donne un (F5, 2026-11-25 : la porte
    ecrivait toujours `verify none` et retirait sans le dire la verification choisie)."""
    if not backend.tls:
        return ""
    if not backend.verify:
        return " ssl verify none"
    options = " ssl verify required ca-file @system-ca"
    if backend.name:
        options += f" sni str({backend.name}) verifyhost {backend.name}"
    return options


def gate_target(config: Mapping[str, Any], dns_name: str) -> GateTarget:
    """Version 1 : exactement un port public, en HTTPS par tailscaled, avec le seul chemin « / »."""
    public = [handler for handler in handlers_of(config) if handler.public]
    ports = {handler.port for handler in public}
    if not public:
        raise UnsupportedPublication(N_("aucun port n'est ouvert à Internet (Funnel)"))
    if len(ports) != 1:
        raise UnsupportedPublication(N_("plusieurs ports Funnel : la porte n'en protège qu'un pour l'instant"))
    handler = public[0]
    if handler.kind == "tcp" and handler.proxy_protocol == 2:
        raise UnsupportedPublication(N_("Funnel passe déjà par une porte (TCP + PROXY v2)"))
    if handler.kind != "https" or len(public) != 1 or handler.path not in ("", "/"):
        raise UnsupportedPublication(N_("seule une publication HTTPS avec le chemin « / » est prise en charge"))
    if not _DNS_NAME.match(dns_name):
        raise UnsupportedPublication(f"{UNEXPECTED_NAME} : {dns_name}")
    return GateTarget(handler.port, dns_name, backend_of(handler.target))


def switch_commands(target: GateTarget, gate_port: int) -> tuple[tuple[str, ...], ...]:
    """HTTPS par tailscaled -> TCP brut + PROXY v2 vers la porte (tailscaled ne fait plus le TLS)."""
    return ((TAILSCALE_COMMAND, "funnel", f"--https={target.public_port}", "off"),
            (TAILSCALE_COMMAND, "funnel", "--bg", "--yes", f"--tcp={target.public_port}", "--proxy-protocol=2",
             f"tcp://127.0.0.1:{gate_port}"))


def unswitch_commands(public_port: int) -> tuple[tuple[str, ...], ...]:
    return ((TAILSCALE_COMMAND, "funnel", f"--tcp={public_port}", "off"),)


def is_gate_publication(config: Mapping[str, Any], gate_port: int) -> bool:
    return any(handler.public and handler.kind == "tcp" and handler.proxy_protocol == 2
               and handler.target == f"tcp://127.0.0.1:{gate_port}" for handler in handlers_of(config))


def render_config(policy: GatePolicy, target: GateTarget, *, gate_port: int, folder: str,
                  groups: GroupsPolicy | None = None, ja4_ready: bool = False) -> str:
    """Fichier d'HAProxy (3.x). `folder` : dossier de la porte (var/porte, chemin absolu). `groups` : regroupements
    du lot 6 (HAProxy avec Lua seulement ; None : porte du lot 4 seule)."""
    observe = policy.mode == MODE_OBSERVATION
    enforce = groups is not None and groups.mode == GROUPS_APPLY and not observe
    lua_global = global_lines(folder) if groups is not None else ""
    group_tables = tables(groups) if groups is not None else ""
    group_acls = acl_lines(folder) if groups is not None else ""
    group_session = session_lines(groups) if groups is not None else ""
    group_content = content_lines(groups, enforce=enforce, ja4_ready=ja4_ready) if groups is not None else ""
    exemption = budget_exemption(groups, enforce) if groups is not None else ""
    log_format = f'    log-format "{LOG_FORMAT}"\n' if groups is not None else ""
    # Connexions refusees des la session (liste noire, budget, debit) : HAProxy les journalise comme « erreurs de
    # connexion », sans le format ci-dessus ; avec ce format-ci, leur motif est dans le journal (rapport, lot 7).
    log_format += f'    error-log-format "{ERROR_LOG_FORMAT}"\n'
    reject = "" if observe else "    tcp-request session reject if { var(sess.motif) -m found }\n"
    content_reject = "" if observe else "    tcp-request content reject if { var(sess.motif) -m found }\n"
    sni = (f"    tcp-request content set-var(sess.motif) str(nom) if !{{ var(sess.motif) -m found }} "
           f"!{{ req.ssl_sni -i {target.dns_name} }}\n") if policy.check_sni else ""
    backend_tls = backend_tls_options(target.backend)
    block = f"{policy.block_minutes}m"
    return f"""# omega-tail - porte avant TLS de Funnel (pare-feu). Fichier genere : ne pas modifier a la main,
# il est reecrit par omega-tail a chaque changement de reglage. Mode : {policy.mode}.
global
    maxconn {policy.max_connections + 100}
    stats socket {folder}/admin.sock mode 600 level admin expose-fd listeners
    stats timeout 10s
    ssl-default-bind-curves X25519MLKEM768:X25519:P-256
    ssl-default-bind-ciphersuites TLS_CHACHA20_POLY1305_SHA256:TLS_AES_128_GCM_SHA256:TLS_AES_256_GCM_SHA384
    ssl-default-bind-options ssl-min-ver TLSv1.2
    log stdout format short local0 info
    localpeer omega-tail
{lua_global}
defaults
    log global
    timeout connect 5s
    timeout client 30s
    timeout server 60s
    timeout http-request 10s

# Tables transmises au nouveau processus lors d'un rechargement (regles changees a chaud) : une adresse bloquee
# le reste. Le pair ecoute sur un socket du dossier de la porte (700) : aucun autre compte de la machine ne peut
# y pousser de mise a jour (scan de securite 2026-11-25, F4 : avant, un port TCP local sans authentification).
peers omega_tail_pairs
    peer omega-tail unix@{folder}/pairs.sock

# Compteurs par adresse (debit sur 10 s, drapeau « bloquee » gpc0) et par prefixe /24 ou /64
backend {TABLE_IP}
    stick-table type ipv6 size {TABLE_IP_SIZE} expire {block} store conn_rate(10s),gpc0 peers omega_tail_pairs
backend {TABLE_PREFIX}
    stick-table type ipv6 size {TABLE_PREFIX_SIZE} expire 10m store conn_rate(10s) peers omega_tail_pairs
# Budget global : connexions ADMISES par seconde (cle unique 1)
backend {TABLE_GLOBAL}
    stick-table type integer size 1 expire 1m store conn_rate(1s)
{group_tables}
frontend {FRONTEND}
    mode tcp
    bind 127.0.0.1:{gate_port} accept-proxy
    maxconn {policy.max_connections}
    option tcplog
{log_format}    tcp-request inspect-delay 2s
    acl confiance src -f {folder}/{TRUST_LIST}
    acl noire src -f {folder}/{BLACK_LIST}
    acl tailnet src {" ".join(TAILNET_NETWORKS)}
{group_acls}    # « session » et non « connection » : evaluees APRES la lecture de l'en-tete PROXY (adresse reelle),
    # toujours avant toute cryptographie (le TLS est au second etage).
    tcp-request session accept if confiance or tailnet
{group_session}    tcp-request session track-sc0 src table {TABLE_IP}
    tcp-request session track-sc1 src,ipmask(24,64) table {TABLE_PREFIX}
    tcp-request session set-var(sess.motif) str(liste-noire) if noire
    tcp-request session set-var(sess.motif) str(bloquee) if !{{ var(sess.motif) -m found }} {{ sc0_get_gpc0 gt 0 }}
    tcp-request session set-var(sess.motif) str(budget) if !{{ var(sess.motif) -m found }} {{ int(1),table_conn_rate({TABLE_GLOBAL}) gt {policy.global_per_s} }}{exemption}
    tcp-request session sc-inc-gpc0(0) if !{{ var(sess.motif) -m found }} {{ sc0_conn_rate gt {policy.ip_per_10s} }}
    tcp-request session set-var(sess.motif) str(debit-adresse) if !{{ var(sess.motif) -m found }} {{ sc0_conn_rate gt {policy.ip_per_10s} }}
    tcp-request session set-var(sess.motif) str(debit-prefixe) if !{{ var(sess.motif) -m found }} {{ sc1_conn_rate gt {policy.prefix_per_10s} }}
{reject}    tcp-request content set-var(sess.motif) str(pas-tls) if !{{ var(sess.motif) -m found }} !{{ req.ssl_hello_type 1 }}
{sni}{content_reject}{group_content}    tcp-request content track-sc2 int(1) table {TABLE_GLOBAL} if !{{ var(sess.motif) -m found }}
    tcp-request content accept
    default_backend porte_vers_tls

backend porte_vers_tls
    mode tcp
    server tls abns@omega-tail-tls-{gate_port} send-proxy-v2

frontend porte_tls
    mode http
    bind abns@omega-tail-tls-{gate_port} accept-proxy ssl crt {folder}/certificat.pem alpn h2,http/1.1
    option httplog
    http-request set-header X-Forwarded-For %[src]
    http-request set-header X-Forwarded-Proto https
    default_backend service

backend service
    mode http
    server origine {target.backend.address}{backend_tls}
"""


def unit_text(*, user: str, haproxy: str, folder: str) -> str:
    """Service systemd de la porte : sous le compte de l'utilisateur (jamais root), ecoute locale seulement."""
    config = f"{folder}/haproxy.cfg"
    return f"""# omega-tail - porte avant TLS de Funnel. Fichier gere par omega-tail (« Desactiver la porte » l'arrete).
[Unit]
Description=omega-tail : porte avant TLS de Funnel (HAProxy)
After=network-online.target tailscaled.service

[Service]
User={user}
ExecStartPre={haproxy} -c -q -f {config}
ExecStart={haproxy} -Ws -f {config} -S {folder}/master.sock
ExecReload={haproxy} -c -q -f {config}
ExecReload=/bin/kill -USR2 $MAINPID
Restart=on-failure
RestartSec=2
NoNewPrivileges=yes
PrivateTmp=yes
ProtectSystem=strict
ReadWritePaths={folder}

[Install]
WantedBy=multi-user.target
"""


def openrc_script(*, user: str, haproxy: str, folder: str) -> str:
    """Service OpenRC de la porte (supervise-daemon), sous le compte de l'utilisateur, journal dans le dossier."""
    config = f"{folder}/haproxy.cfg"
    return f"""#!/sbin/openrc-run
# omega-tail - porte avant TLS de Funnel. Fichier gere par omega-tail (« Desactiver la protection » l'arrete).
description="omega-tail : porte avant TLS de Funnel (HAProxy)"
command="{haproxy}"
command_args="-W -db -f {config} -S {folder}/master.sock"
command_user="{user}"
supervisor="supervise-daemon"
output_log="{folder}/porte.log"
error_log="{folder}/porte.log"

depend() {{
    need net
    after tailscale tailscaled
}}

# Verification sous le compte de l'utilisateur, jamais en root : la configuration et les scripts Lua qu'elle charge
# sont dans son dossier (scan de securite 2026-11-25, F2).
start_pre() {{
    su -s /bin/sh -c {shlex.quote(f"{shlex.quote(haproxy)} -c -q -f {shlex.quote(config)}")} {shlex.quote(user)}
}}
"""


def runit_run_script(*, user: str, haproxy: str, folder: str) -> str:
    config = f"{folder}/haproxy.cfg"
    return f"""#!/bin/sh
# omega-tail - porte avant TLS de Funnel (runit). Fichier gere par omega-tail.
exec 2>&1
# Verification sous le compte de l'utilisateur, jamais en root (scan de securite 2026-11-25, F1)
chpst -u {user} "{haproxy}" -c -q -f "{config}" || exit 1
exec chpst -u {user} "{haproxy}" -W -db -f "{config}" -S "{folder}/master.sock"
"""


def runit_log_script(*, user: str, folder: str) -> str:
    return f"""#!/bin/sh
# omega-tail - journal de la porte (svlogd), dans le dossier de la porte.
exec chpst -u {user} svlogd -tt "{folder}/log"
"""


CRON_MARKER = "# omega-tail-porte-certificat"


def cron_line(python: str) -> str:
    """Hors systemd : verification quotidienne du certificat, dans la crontab de l'utilisateur (ligne marquee)."""
    return f"17 4 * * * {python} -m omega_tail porte certificat --si-besoin >/dev/null 2>&1 {CRON_MARKER}"
