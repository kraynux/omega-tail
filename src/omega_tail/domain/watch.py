# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Veille automatique (decision, 2026-11-23) : quand personne n'est devant la machine, la veille coupe
Funnel SEULE (jamais tailscaled), par paliers, et le remet en route seule.

- Un depassement : le seuil du disjoncteur tenu (CPU de tailscaled pendant la duree choisie, ou la temperature).
  Deux depassements comptes sont separes d'au moins cette duree (une meme periode ne compte qu'une fois).
- 3 depassements dans la fenetre (10 min par defaut) : coupure de Funnel, 15 min la premiere fois, 30 min la
  deuxieme, puis 1 h a chaque fois (renouvelable), toujours remise en route automatique, a l'identique.
- Retour au premier palier apres 24 h sans coupure. Apres chaque remise en route, un moment de calme sans mesure.
- Desactivee par defaut ; activee dans Survie (un service sous le compte de l'utilisateur, operateur de Tailscale :
  jamais root)."""
from __future__ import annotations

from dataclasses import dataclass, replace

from omega_tail.domain.init import InitSystem

STEPS_MINUTES = (15, 30, 60)
"""Paliers de coupure ; le dernier se renouvelle."""
STRIKES = 3
DEFAULT_WINDOW_MINUTES = 10
RESET_HOURS = 24
CALM_SECONDS = 120
"""Apres une remise en route : la charge retombe avant de mesurer de nouveau."""
TICK_SECONDS = 5.0
HEARTBEAT_SECONDS = 30.0
ALIVE_SECONDS = 90.0
"""Signe de vie plus vieux : la veille ne tourne plus."""
CUT_PREFIX = "veille-"

WATCH_NAMES: dict[InitSystem, str] = {
    InitSystem.SYSTEMD: "omega-tail-veille.service",
    InitSystem.OPENRC: "omega-tail-veille",
    InitSystem.RUNIT: "omega-tail-veille",
    InitSystem.NONE: "omega-tail-veille",
}


@dataclass(frozen=True)
class WatchState:
    strikes: tuple[float, ...] = ()
    """Instants (secondes epoch) des depassements comptes dans la fenetre."""
    level: int = 0
    """Coupures de la serie en cours (0 : la prochaine sera de 15 min)."""
    last_end: float = 0.0
    """Fin de la derniere coupure (remise en route) : point de depart des 24 h."""
    calm_until: float = 0.0
    heartbeat: float = 0.0
    installed: bool = False
    """Le service a ete active depuis omega-tail (sert a signaler une veille arretee)."""


def cut_minutes(level: int) -> int:
    return STEPS_MINUTES[min(max(level, 0), len(STEPS_MINUTES) - 1)]


def current_level(state: WatchState, now: float) -> int:
    """24 h sans coupure : retour au premier palier."""
    if state.last_end and now - state.last_end >= RESET_HOURS * 3600:
        return 0
    return state.level


def can_strike(state: WatchState, now: float, spacing_s: float) -> bool:
    return not state.strikes or now - state.strikes[-1] >= spacing_s


def on_strike(state: WatchState, now: float, window_minutes: int) -> tuple[WatchState, int | None]:
    """Compte un depassement ; renvoie la duree de coupure (min) quand la fenetre en contient STRIKES."""
    level = current_level(state, now)
    strikes = tuple(at for at in state.strikes if at > now - window_minutes * 60) + (now,)
    if len(strikes) >= STRIKES:
        minutes = cut_minutes(level)
        return replace(state, strikes=(), level=level + 1, last_end=now + minutes * 60), minutes
    return replace(state, strikes=strikes, level=level), None


def after_restore(state: WatchState, now: float) -> WatchState:
    return replace(state, last_end=now, calm_until=now + CALM_SECONDS, strikes=())


@dataclass(frozen=True)
class WatchStatus:
    """Ce que le tableau de bord et Survie montrent de la veille."""
    installed: bool
    alive: bool
    level: int
    strikes: int
    next_minutes: int


def status_of(state: WatchState, now: float, window_minutes: int) -> WatchStatus:
    level = current_level(state, now)
    recent = sum(1 for at in state.strikes if at > now - window_minutes * 60)
    return WatchStatus(state.installed, bool(state.heartbeat) and now - state.heartbeat <= ALIVE_SECONDS, level,
                       recent, cut_minutes(level))


# ---- services (systemd, OpenRC, runit), sous le compte de l'utilisateur ----
def unit_text(*, user: str, python: str) -> str:
    return f"""# omega-tail - veille automatique (Survie). Fichier gere par omega-tail (« Désactiver la veille »).
[Unit]
Description=omega-tail : veille automatique (coupe Funnel seule sous attaque, puis le remet)
After=network-online.target tailscaled.service

[Service]
User={user}
ExecStart={python} -m omega_tail veille lancer
Restart=always
RestartSec=5
NoNewPrivileges=yes
Nice=-5

[Install]
WantedBy=multi-user.target
"""


def openrc_script(*, user: str, python: str, folder: str) -> str:
    return f"""#!/sbin/openrc-run
# omega-tail - veille automatique (Survie). Fichier gere par omega-tail (« Désactiver la veille »).
description="omega-tail : veille automatique"
command="{python}"
command_args="-m omega_tail veille lancer"
command_user="{user}"
supervisor="supervise-daemon"
respawn_delay=5
output_log="{folder}/veille.log"
error_log="{folder}/veille.log"

depend() {{
    need net
    after tailscale tailscaled
}}
"""


def runit_run_script(*, user: str, python: str) -> str:
    return f"""#!/bin/sh
# omega-tail - veille automatique (runit). Fichier gere par omega-tail.
exec 2>&1
exec chpst -u {user} "{python}" -m omega_tail veille lancer
"""


def runit_log_script(*, user: str, folder: str) -> str:
    return f"""#!/bin/sh
# omega-tail - journal de la veille (svlogd).
exec chpst -u {user} svlogd -tt "{folder}/log"
"""
