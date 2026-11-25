# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Menu principal (decision, 2026-11-22) : deux colonnes de 6, sans bouton Quitter (touche q).
TAILSCALE — Tableau de bord, Service tailscaled, Connexion et reglages, Publication, Reseau et appareils, Journaux |
PROTECTION — Pare-feu Funnel, Survie, Attaques et decisions, Rapport, Reglages, Aide.
`planned` : version qui construira l'ecran (PROPOSITION_MENU_FONCTIONS.md §7)."""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from omega_tail.shared.i18n import N_


class Column(str, Enum):
    TAILSCALE = "tailscale"
    PROTECTION = "protection"


@dataclass(frozen=True)
class MenuEntry:
    key: str
    label: str
    column: Column
    planned: str = ""
    """Lot qui construira l'ecran (vide : disponible)."""


MENU: tuple[MenuEntry, ...] = (
    MenuEntry("dashboard", N_("Tableau de bord"), Column.TAILSCALE),
    MenuEntry("service", N_("Service tailscaled"), Column.TAILSCALE),
    MenuEntry("connection", N_("Connexion et réglages"), Column.TAILSCALE),
    MenuEntry("publication", N_("Publication"), Column.TAILSCALE),
    MenuEntry("network", N_("Réseau et appareils"), Column.TAILSCALE),
    MenuEntry("journals", N_("Journaux"), Column.TAILSCALE),
    MenuEntry("firewall", N_("Pare-feu Funnel"), Column.PROTECTION),
    MenuEntry("survival", N_("Survie"), Column.PROTECTION),
    MenuEntry("attacks", N_("Attaques et décisions"), Column.PROTECTION),
    MenuEntry("report", N_("Rapport"), Column.PROTECTION),
    MenuEntry("settings", N_("Réglages"), Column.PROTECTION),
    MenuEntry("help", N_("Aide"), Column.PROTECTION),
)
COLUMN_TITLES = {Column.TAILSCALE: N_("TAILSCALE"), Column.PROTECTION: N_("PROTECTION")}


def entry(key: str) -> MenuEntry | None:
    return next((item for item in MENU if item.key == key), None)
