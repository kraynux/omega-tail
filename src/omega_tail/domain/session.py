# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Garde-fou « branche sciee » (PROPOSITION_MENU_FONCTIONS.md §1) : si la session passe par Tailscale, une action
qui coupe Tailscale couperait aussi cette session."""
from __future__ import annotations

import ipaddress
from dataclasses import dataclass
from enum import Enum

from omega_tail.core.constants import TAILSCALE_IPV4_NETWORK, TAILSCALE_IPV6_NETWORK
from omega_tail.domain.service import ServiceAction
from omega_tail.shared.i18n import N_

_NETWORKS = (ipaddress.ip_network(TAILSCALE_IPV4_NETWORK), ipaddress.ip_network(TAILSCALE_IPV6_NETWORK))


def is_tailscale_address(text: str) -> bool:
    try:
        address = ipaddress.ip_address(text.split("%", 1)[0])
    except ValueError:
        return False
    return any(address.version == network.version and address in network for network in _NETWORKS)


def session_through_tailscale(ssh_connection: str) -> bool:
    """`SSH_CONNECTION` = « ip_client port_client ip_serveur port_serveur ». Vrai si l'une des deux adresses est
    une adresse Tailscale (session SSH ouverte par le tailnet)."""
    parts = ssh_connection.split()
    return len(parts) >= 3 and (is_tailscale_address(parts[0]) or is_tailscale_address(parts[2]))


class Risk(str, Enum):
    NONE = "none"
    INTERRUPTION = "interruption"
    """Coupure de quelques secondes : la session se fige puis revient en general."""
    CUT = "cut"
    """La session est perdue et ne peut pas relancer Tailscale elle-meme."""


@dataclass(frozen=True)
class Guard:
    risk: Risk
    text: str = ""
    """Phrase a afficher (marquee pour la traduction)."""


def guard_service_action(action: ServiceAction, through_tailscale: bool) -> Guard:
    if not through_tailscale or action is ServiceAction.START:
        return Guard(Risk.NONE)
    if action is ServiceAction.STOP:
        return Guard(Risk.CUT, N_(
            "Cette session passe par Tailscale : arrêter tailscaled la coupera, et vous ne pourrez pas le relancer "
            "d'ici. Accès de secours : le réseau local ou la machine elle-même."))
    return Guard(Risk.INTERRUPTION, N_(
        "Cette session passe par Tailscale : pendant le redémarrage elle se figera quelques secondes, puis "
        "reviendra en général d'elle-même."))
