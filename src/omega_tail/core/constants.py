# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Constantes d'omega-tail (PROPOSITION_MENU_FONCTIONS.md, lot 1)."""
from __future__ import annotations

APP_NAME = "omega-tail"

TAILSCALE_COMMAND = "tailscale"
TAILSCALED_UNIT = "tailscaled.service"
COMMAND_TIMEOUT_SECONDS = 10.0
"""Une commande `tailscale` ou `systemctl` de lecture qui ne repond pas en 10 s est abandonnee (jamais d'attente
sans fin dans l'interface)."""

REFRESH_SECONDS = 5.0
"""Tableau de bord et bande d'etat : relecture toutes les 5 s (lectures legeres : status, serve, systemctl, /proc)."""

JOURNAL_LINES = (100, 300, 1000, 3000)
JOURNAL_DEFAULT_LINES = 300
JOURNAL_MAX_BYTES = 4_000_000
"""Sortie de journalctl lue au plus (3 000 lignes font ~500 Ko) : jamais de lecture sans borne."""

# Alertes (seuils ; omega-server relevee a 76-81 °C le 2026-11-22, MESURES_LOT0.md)
TEMPERATURE_WARNING_C = 75.0
TEMPERATURE_CRITICAL_C = 85.0
TAILSCALED_CPU_WARNING_PERCENT = 50.0
TAILSCALED_CPU_CRITICAL_PERCENT = 90.0
MACHINE_CPU_WARNING_PERCENT = 70.0
MACHINE_CPU_CRITICAL_PERCENT = 90.0
LOAD_WARNING_PER_CORE = 1.0
LOAD_CRITICAL_PER_CORE = 2.0
MEMORY_WARNING_PERCENT = 85.0
MEMORY_CRITICAL_PERCENT = 95.0
"""En % d'un coeur. Au repos : 1,5 a 6 % (relevés du lot 0) ; 120 % a 60 connexions TLS/s sur le J3455."""
KEY_EXPIRY_WARNING_DAYS = 14
CERT_EXPIRY_WARNING_DAYS = 14

# Reseaux de Tailscale (garde-fou « branche sciee »)
TAILSCALE_IPV4_NETWORK = "100.64.0.0/10"
TAILSCALE_IPV6_NETWORK = "fd7a:115c:a1e0::/48"

SEARCH_MAX_BYTES = 32 * 1024 * 1024
"""Recherche dans un journal (rapport : refus des 7 derniers jours) : au-dela, seules les lignes les plus recentes
sont lues et le rapport le dit."""
SEARCH_TIMEOUT_SECONDS = 90
