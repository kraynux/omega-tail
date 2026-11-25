# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Regroupements et modes (lot 6, decisions du 2026-11-23) : contre les attaques a adresses
dispersees, ou les regles par adresse et par prefixe (lot 4) ne voient chaque adresse qu'une fois.

- Chaque connexion recoit, AVANT tout chiffrement, son empreinte JA4 (domain/ja4.py), son AS et son pays
  (domain/geo.py) ; HAProxy compte le debit de chaque groupe.
- **Mode attaque automatique**, decide par HAProxy lui-meme : quand les connexions entrantes depassent le seuil
  (par seconde), le mode attaque s'enclenche ; il retombe apres le temps de calme sans depassement.
- En mode attaque seulement : une empreinte inconnue (hors reference apprise) qui explose, un AS d'hebergeur ou un
  pays choisi qui depasse son debit -> refus (motif « empreinte », « hebergeur », « pays »). Les navigateurs
  courants (domain/geo.BROWSER_CIPHER_HASHES) ne sont JAMAIS touches par ces regles.
- Clients connus (admis en temps normal dans les dernieres 24 h) : jamais refuses par le budget global.
- Hors attaque, une connexion sur dix seulement est classee (SAMPLE_PERCENT) ; en attaque, toutes.
- **Observation d'abord** (defaut) : tout est compte (« aurait refuse »), rien n'est refuse par ces regles.
- **Reference apprise** : 7 jours d'apprentissage en temps normal avant que la regle des empreintes s'applique ;
  une empreinte vue sur 3 jours, ou sur 2 jours avec au moins 1 % des connexions, est « habituelle »."""
from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field, replace
from datetime import datetime, timedelta
from typing import Any

from omega_tail.domain.geo import HOSTING_ASNS, asn_numbers, countries
from omega_tail.shared.i18n import N_

GROUPS_OBSERVE = "observation"
GROUPS_APPLY = "applique"
TABLE_JA4 = "porte_ja4"
TABLE_AS = "porte_as"
TABLE_COUNTRY = "porte_pays"
TABLE_INCOMING = "porte_entrees"
TABLE_ATTACK = "porte_attaque"
TABLE_REASONS = "porte_groupes"
TABLE_KNOWN = "porte_connus"
KNOWN_JA4_LIST = "ja4-connus.lst"
BROWSER_LIST = "navigateurs.lst"
HOSTING_LIST = "as-hebergeurs.lst"
COUNTRY_LIST = "pays-limites.lst"
GEO_FILE = "geo.bin"
NAMES_FILE = "as-noms.tsv"
JA4_SCRIPT = "omega_ja4.lua"
GEO_SCRIPT = "omega_geo.lua"
LEARNING_DAYS = 7
KNOWN_DAYS = 3
KNOWN_SHARE = 0.01
REASONS = ("empreinte", "hebergeur", "pays")
REASON_LABELS = {"empreinte": N_("empreinte"), "hebergeur": N_("hébergeur"), "pays": N_("pays")}


def reason_pairs(reasons: Mapping[str, int]) -> list[tuple[str, int]]:
    """(libelle lisible, nombre) des motifs comptes, dans l'ordre des motifs."""
    return [(REASON_LABELS[key], reasons[key]) for key in REASONS if key in reasons]


SAMPLE_PERCENT = 10
"""Hors mode attaque, une connexion sur dix est classee (empreinte, AS, pays) : assez pour apprendre et pour les
statistiques, dix fois moins de calcul (mesure du 2026-11-23 : +0,2 a 0,3 ms par connexion classee). En mode
attaque, toutes le sont."""


@dataclass(frozen=True)
class GroupsPolicy:
    mode: str = GROUPS_OBSERVE
    attack_per_s: int = 80
    """Connexions entrantes par seconde qui enclenchent le mode attaque."""
    calm_minutes: int = 5
    ja4_per_10s: int = 50
    as_per_10s: int = 100
    country_per_10s: int = 50
    countries: tuple[str, ...] = ()
    """Pays limites en mode attaque (vide par defaut, decision C)."""
    hosting: tuple[int, ...] = field(default_factory=lambda: tuple(sorted(HOSTING_ASNS)))
    known_first: bool = True


LIMITS = {"attack_per_s": (2, 100_000), "calm_minutes": (1, 240), "ja4_per_10s": (2, 100_000),
          "as_per_10s": (2, 100_000), "country_per_10s": (2, 100_000)}


def groups_from(values: Mapping[str, Any]) -> GroupsPolicy:
    """Politique depuis les reglages ; valeur absente ou hors bornes : valeur par defaut."""
    base = GroupsPolicy()
    numbers = {}
    for key, (low, high) in LIMITS.items():
        try:
            value = int(str(values.get(key, getattr(base, key))).strip())
        except ValueError:
            value = getattr(base, key)
        numbers[key] = value if low <= value <= high else getattr(base, key)
    mode = values.get("mode", base.mode)
    hosting = values.get("hosting")
    return GroupsPolicy(
        mode=mode if mode in (GROUPS_OBSERVE, GROUPS_APPLY) else base.mode,
        countries=countries(str(values.get("countries", ""))),
        hosting=asn_numbers(str(hosting)) if hosting is not None else base.hosting,
        known_first=str(values.get("known_first", base.known_first)).lower() not in ("false", "0", "non"),
        **numbers)


# ---- apprentissage de la reference des empreintes ----
@dataclass(frozen=True)
class Seen:
    days: tuple[str, ...] = ()
    """Jours (AAAA-MM-JJ) ou l'empreinte a ete vue en temps normal."""
    count: int = 0
    last: int = 0
    """Dernier compteur cumule lu dans HAProxy (pour n'ajouter que la difference)."""


@dataclass(frozen=True)
class Learning:
    since: str = ""
    seen: Mapping[str, Seen] = field(default_factory=dict)


def learn(state: Learning, counters: Mapping[str, int], now: datetime, *, attack: bool) -> Learning:
    """Une lecture de la table des empreintes. En mode attaque, seuls les compteurs de reference avancent (le
    trafic de l'attaque n'entre jamais dans la reference)."""
    since = state.since or now.isoformat()
    day = now.date().isoformat()
    seen = dict(state.seen)
    for key, total in counters.items():
        before = seen.get(key, Seen())
        added = total - before.last if total >= before.last else total
        if attack or added <= 0:
            seen[key] = replace(before, last=total)
            continue
        days = before.days if day in before.days else (*before.days, day)[-30:]
        seen[key] = Seen(days, before.count + added, total)
    return Learning(since, seen)


def learning_left(state: Learning, now: datetime) -> int:
    """Jours d'apprentissage restants (0 : la reference compte)."""
    if not state.since:
        return LEARNING_DAYS
    try:
        started = datetime.fromisoformat(state.since)
    except ValueError:
        return LEARNING_DAYS
    left = started + timedelta(days=LEARNING_DAYS) - now
    return max(0, left.days + (1 if left.seconds else 0)) if left.total_seconds() > 0 else 0


def reference(state: Learning) -> tuple[str, ...]:
    total = sum(item.count for item in state.seen.values()) or 1
    return tuple(sorted(key for key, item in state.seen.items()
                        if len(item.days) >= KNOWN_DAYS or (len(item.days) >= 2 and item.count / total >= KNOWN_SHARE)))


# ---- fichier d'HAProxy ----
def global_lines(folder: str) -> str:
    return (f"    tune.stick-counters 10\n    tune.lua.bool-sample-conversion normal\n"
            f"    lua-load {folder}/{JA4_SCRIPT}\n    lua-load {folder}/{GEO_SCRIPT} {folder}/{GEO_FILE}\n")


def tables(policy: GroupsPolicy) -> str:
    peers = "peers omega_tail_pairs"
    return f"""# Regroupements (lot 6) : debit par empreinte JA4, par AS, par pays ; mode attaque ; motifs observes
backend {TABLE_JA4}
    stick-table type string len 40 size 50k expire 8d store conn_cnt,conn_rate(10s) {peers}
backend {TABLE_AS}
    stick-table type string len 12 size 100k expire 1d store conn_cnt,conn_rate(10s) {peers}
backend {TABLE_COUNTRY}
    stick-table type string len 2 size 400 expire 1d store conn_cnt,conn_rate(10s) {peers}
backend {TABLE_INCOMING}
    stick-table type integer size 1 expire 1m store conn_rate(1s)
backend {TABLE_ATTACK}
    stick-table type integer size 1 expire {policy.calm_minutes}m store conn_cnt {peers}
backend {TABLE_REASONS}
    stick-table type string len 16 size 10 expire 7d store conn_cnt,conn_rate(60s) {peers}
backend {TABLE_KNOWN}
    stick-table type ipv6 size 200k expire 24h {peers}
"""


def acl_lines(folder: str) -> str:
    return f"""    acl attaque int(1),in_table({TABLE_ATTACK})
    acl client_connu src,in_table({TABLE_KNOWN})
    acl ja4_connue var(sess.ja4) -m str -f {folder}/{KNOWN_JA4_LIST}
    acl navigateur var(sess.ja4),field(2,_) -m str -f {folder}/{BROWSER_LIST}
    acl hebergeur var(sess.as) -m str -f {folder}/{HOSTING_LIST}
    acl pays_limite var(sess.pays) -m str -f {folder}/{COUNTRY_LIST}
"""


def session_lines(policy: GroupsPolicy) -> str:
    """Juste apres la confiance : toutes les connexions entrantes comptent pour le mode attaque."""
    # Tirage de l'echantillon ici (phase session) : un rand() dans une condition de la phase « content » ferait
    # attendre chaque connexion jusqu'a la fin de l'inspection (2 s), HAProxy le jugeant encore variable.
    return (f"    tcp-request session set-var(sess.tirage) rand(100)\n"
            f"    tcp-request session track-sc6 int(1) table {TABLE_INCOMING}\n"
            f"    tcp-request session track-sc7 int(1) table {TABLE_ATTACK} if {{ sc_conn_rate(6) gt "
            f"{policy.attack_per_s} }}\n")


def budget_exemption(policy: GroupsPolicy, enforce: bool) -> str:
    """Condition ajoutee a la regle du budget global : les clients connus passent (applique seulement)."""
    return " !client_connu" if enforce and policy.known_first else ""


def content_lines(policy: GroupsPolicy, *, enforce: bool, ja4_ready: bool) -> str:
    """Apres le ClientHello complet et les motifs du lot 4 ; jamais pour une connexion deja marquee."""
    clear = "!{ var(sess.motif) -m found } !navigateur"
    rules = [
        "    # ---- regroupements (lot 6) : empreinte, AS, pays ; motifs seulement en mode attaque ----",
        f"    tcp-request content lua.omega_groupes if attaque or {{ var(sess.tirage) -m int lt {SAMPLE_PERCENT} }}",
        f"    tcp-request content track-sc3 var(sess.ja4) table {TABLE_JA4} if {{ var(sess.ja4) -m found }}",
        f"    tcp-request content track-sc4 var(sess.as) table {TABLE_AS}",
        f"    tcp-request content track-sc5 var(sess.pays) table {TABLE_COUNTRY}",
    ]
    if ja4_ready:
        rules.append(f"    tcp-request content set-var(sess.groupe) str(empreinte) if attaque {clear} "
                     f"{{ var(sess.ja4) -m found }} !ja4_connue {{ sc_conn_rate(3) gt {policy.ja4_per_10s} }}")
    rules += [
        f"    tcp-request content set-var(sess.groupe) str(hebergeur) if attaque {clear} "
        f"!{{ var(sess.groupe) -m found }} hebergeur {{ sc_conn_rate(4) gt {policy.as_per_10s} }}",
        f"    tcp-request content set-var(sess.groupe) str(pays) if attaque {clear} "
        f"!{{ var(sess.groupe) -m found }} pays_limite {{ sc_conn_rate(5) gt {policy.country_per_10s} }}",
        f"    tcp-request content track-sc8 var(sess.groupe) table {TABLE_REASONS} if {{ var(sess.groupe) -m found }}",
    ]
    if enforce:
        rules.append("    tcp-request content reject if { var(sess.groupe) -m found }")
    rules.append(f"    tcp-request content track-sc9 src table {TABLE_KNOWN} if !{{ var(sess.motif) -m found }} "
                 "!{ var(sess.groupe) -m found } !attaque")
    return "\n".join(rules) + "\n"


LOG_FORMAT = ("%ci:%cp [%t] %ft %b/%s %Tw/%Tc/%Tt %B %ts %ac/%fc/%bc/%sc/%rc %sq/%bq motif=%[var(sess.motif)] "
              "groupe=%[var(sess.groupe)] ja4=%[var(sess.ja4)] as=%[var(sess.as)] pays=%[var(sess.pays)]")
"""Format tcplog d'HAProxy, suivi des motifs et des groupes (journal de la porte)."""
ERROR_LOG_FORMAT = "%ci:%cp [%t] %ft avant-tls motif=%[var(sess.motif)] groupe=- ja4=- as=- pays=-"
"""Connexions refusees avant l'etage TLS (regles de session du lot 4) : HAProxy les journalise a part ; meme fin de
ligne que LOG_FORMAT pour que le rapport les relise de la meme facon."""
