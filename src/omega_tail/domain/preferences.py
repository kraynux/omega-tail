# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Connexion et reglages (lot 5, proposition §3.3) : les preferences de `tailscale set`, leur verification, la
difference avant / apres et la commande qui les applique.

Noms et valeurs releves avec `tailscale get` / `tailscale set --help` (1.102 et 1.104, 2026-11-23). Chaque valeur
part en argument de la commande (jamais par un shell) ; elle est tout de meme verifiee avant."""
from __future__ import annotations

import ipaddress
import re
from collections.abc import Mapping
from dataclasses import dataclass
from enum import Enum

from omega_tail.core.constants import TAILSCALE_COMMAND
from omega_tail.shared.i18n import N_


class Kind(str, Enum):
    BOOL = "bool"
    TEXT = "text"
    CHOICE = "choice"


class Group(str, Enum):
    IDENTITY = N_("Identité")
    NETWORK = N_("Réseau")
    EXIT = N_("Sortie")
    SERVICES = N_("Services Tailscale")
    OPERATOR = N_("Opérateur")


@dataclass(frozen=True)
class PrefSpec:
    name: str
    """Nom de la preference, tel que `tailscale get` l'affiche et que `tailscale set --NAME=` l'attend."""
    label: str
    group: Group
    kind: Kind
    hint: str
    choices: tuple[str, ...] = ()
    cuts_session: str = ""
    """Valeur qui peut couper une session passant par Tailscale (« * » : tout changement)."""
    example: str = ""
    """Texte attenue montre dans un champ vide (situe le champ, n'est jamais une valeur)."""


PREFS: tuple[PrefSpec, ...] = (
    PrefSpec("hostname", N_("Nom de la machine"), Group.IDENTITY, Kind.TEXT,
             N_("Nom dans le tailnet (vide : celui du système). Change aussi l'adresse *.ts.net : les liens publiés "
                "et le certificat suivent."),
             example=N_("ex. serveur-maison")),
    PrefSpec("nickname", N_("Surnom du compte"), Group.IDENTITY, Kind.TEXT,
             N_("Surnom du compte en cours, pour le reconnaître dans « Changer de compte »."),
             example=N_("ex. maison")),
    PrefSpec("accept-routes", N_("Accepter les routes"), Group.NETWORK, Kind.BOOL,
             N_("Utiliser les sous-réseaux annoncés par les autres machines. À éviter sur une machine du même réseau "
                "local que le routeur qui l'annonce.")),
    PrefSpec("accept-dns", N_("Accepter le DNS du tailnet"), Group.NETWORK, Kind.BOOL,
             N_("MagicDNS : les noms des machines du tailnet se résolvent ici.")),
    PrefSpec("shields-up", N_("Bouclier (refuser les connexions entrantes)"), Group.NETWORK, Kind.BOOL,
             N_("Aucune machine du tailnet ne peut se connecter à celle-ci (SSH et Serve compris). Funnel n'est "
                "pas concerné."), cuts_session="true"),
    PrefSpec("stateful-filtering", N_("Filtrage avec état"), Group.NETWORK, Kind.BOOL,
             N_("Pour un routeur de sous-réseau ou un nœud de sortie : ne laisse revenir que les réponses.")),
    PrefSpec("netfilter-mode", N_("Mode netfilter"), Group.NETWORK, Kind.CHOICE,
             N_("on : Tailscale gère ses règles de pare-feu ; nodivert : ses chaînes sans les brancher ; off : "
                "aucune règle (à vos risques)."), choices=("on", "nodivert", "off"), cuts_session="*"),
    PrefSpec("exit-node", N_("Nœud de sortie utilisé"), Group.EXIT, Kind.CHOICE,
             N_("Faire passer le trafic Internet de cette machine par une autre machine du tailnet (vide : "
                "aucun)."), cuts_session="*"),
    PrefSpec("exit-node-allow-lan-access", N_("Garder l'accès au réseau local"), Group.EXIT, Kind.BOOL,
             N_("Avec un nœud de sortie : le réseau local reste joignable directement.")),
    PrefSpec("advertise-exit-node", N_("Proposer cette machine comme nœud de sortie"), Group.EXIT, Kind.BOOL,
             N_("Les autres machines pourront sortir sur Internet par celle-ci (à approuver dans la console "
                "d'administration).")),
    PrefSpec("advertise-routes", N_("Sous-réseaux annoncés"), Group.EXIT, Kind.TEXT,
             N_("Réseaux locaux rendus joignables au tailnet, séparés par des virgules (192.168.1.0/24) ; vide : "
                "aucun."),
             example=N_("ex. 192.168.1.0/24, 10.0.0.0/8")),
    PrefSpec("ssh", N_("SSH Tailscale"), Group.SERVICES, Kind.BOOL,
             N_("Serveur SSH de Tailscale, selon les règles du tailnet. Votre SSH habituel n'est pas touché."),
             cuts_session="false"),
    PrefSpec("webclient", N_("Interface web (port 5252)"), Group.SERVICES, Kind.BOOL,
             N_("Page de gestion de cette machine, joignable par le tailnet seulement.")),
    PrefSpec("auto-update", N_("Mises à jour automatiques"), Group.SERVICES, Kind.BOOL,
             N_("Tailscale se met à jour seul quand sa distribution le permet. Sinon : gestionnaire de paquets.")),
    PrefSpec("update-check", N_("Signaler les mises à jour"), Group.SERVICES, Kind.BOOL,
             N_("Tailscale prévient quand une version plus récente existe.")),
    PrefSpec("relay-server-port", N_("Port du relais pair (UDP)"), Group.SERVICES, Kind.TEXT,
             N_("Cette machine relaie les connexions d'autres machines du tailnet sur ce port UDP ; vide : non."),
             example=N_("ex. 40000")),
    PrefSpec("operator", N_("Opérateur"), Group.OPERATOR, Kind.TEXT,
             N_("Nom du compte Linux qui pilote Tailscale sans sudo (« Mon compte » le remplit) ; vide : root "
                "seul. Changer l'opérateur demande sudo une fois."),
             example=N_("ex. votre compte Linux")),
)
SPECS = {spec.name: spec for spec in PREFS}

HOSTNAME = re.compile(r"^[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?$")
UNIX_USER = re.compile(r"^[a-z_][a-z0-9_.-]{0,31}\$?$")
EXIT_NODE = re.compile(r"^[A-Za-z0-9.:_-]{1,253}$")


def normalize(spec: PrefSpec, value: str) -> str:
    text = value.strip()
    if spec.kind is Kind.BOOL:
        return "true" if text.lower() in ("true", "1", "yes", "on") else "false"
    if spec.name == "advertise-routes":
        return ",".join(part.strip() for part in text.split(",") if part.strip())
    return text


def problem(name: str, value: str) -> str:
    """Pourquoi la valeur est refusee (phrase marquee pour la traduction), vide si elle convient."""
    spec = SPECS.get(name)
    if spec is None:
        return N_("réglage inconnu")
    text = normalize(spec, value)
    if any(ord(char) < 32 or ord(char) == 127 for char in value):
        return N_("caractère de contrôle")
    if spec.kind is Kind.CHOICE and spec.choices and text not in spec.choices:
        return N_("valeur hors liste")
    if not text:
        return ""
    if name == "hostname" and not HOSTNAME.match(text):
        return N_("lettres, chiffres et tirets seulement (63 au plus)")
    if name == "nickname" and len(text) > 64:
        return N_("64 caractères au plus")
    if name == "operator" and not UNIX_USER.match(text):
        return N_("nom de compte Unix attendu")
    if name == "exit-node" and not EXIT_NODE.match(text):
        return N_("adresse ou nom de machine attendu")
    if name == "relay-server-port" and not (text.isdigit() and int(text) <= 65535):
        return N_("port de 0 à 65535")
    if name == "advertise-routes":
        for part in text.split(","):
            try:
                ipaddress.ip_network(part, strict=True)
            except ValueError:
                return N_("réseau invalide : {value}")
    return ""


@dataclass(frozen=True)
class Change:
    name: str
    before: str
    after: str

    @property
    def spec(self) -> PrefSpec:
        return SPECS[self.name]

    @property
    def cuts_session(self) -> bool:
        marker = self.spec.cuts_session
        return marker == "*" or (bool(marker) and self.after == marker)


def changes(current: Mapping[str, str], wanted: Mapping[str, str]) -> tuple[Change, ...]:
    """Reglages a changer, dans l'ordre de l'ecran. Un reglage absent de `wanted` n'est pas touche."""
    found = []
    for spec in PREFS:
        if spec.name not in wanted:
            continue
        before, after = normalize(spec, current.get(spec.name, "")), normalize(spec, wanted[spec.name])
        if before != after:
            found.append(Change(spec.name, before, after))
    return tuple(found)


def problems(wanted: Mapping[str, str]) -> dict[str, str]:
    return {name: reason for name, value in wanted.items() if (reason := problem(name, value))}


def needs_root(found: tuple[Change, ...]) -> bool:
    """Changer l'operateur demande root (un operateur ne se remplace pas lui-meme)."""
    return any(change.name == "operator" for change in found)


def set_command(found: tuple[Change, ...], *, sudo: bool) -> tuple[str, ...]:
    """Une seule commande `tailscale set` : tout ou rien, comme le fait Tailscale."""
    command = (TAILSCALE_COMMAND, "set", *(f"--{change.name}={change.after}" for change in found))
    return ("sudo", *command) if sudo else command
