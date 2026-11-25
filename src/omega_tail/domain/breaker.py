# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Quand proposer la coupure de Funnel (decision, 2026-11-22 : le disjoncteur PROPOSE, il ne coupe
jamais seul). Proposition si tailscaled reste au-dessus du seuil CPU pendant toute la duree choisie, ou si la
temperature atteint son seuil."""
from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

from omega_tail.shared.i18n import N_

DEFAULT_CPU_PERCENT = 80.0
"""En % d'un coeur. Au repos 1,5 a 6 % ; 120 % a 60 nouvelles connexions TLS/s sur le J3455 (lot 0)."""
DEFAULT_SECONDS = 60
DEFAULT_TEMPERATURE_C = 85.0
DEFAULT_MINUTES = 10
"""Coupure momentanee par defaut (exemple : « couper 10 min »)."""
SAMPLE_SLACK_SECONDS = 6.0
"""Marge d'une mesure (rafraichissement de 5 s + retard) pour juger qu'une duree est couverte."""
SNOOZE_MINUTES = 15
"""« Pas maintenant » : plus de proposition pendant 15 min."""


@dataclass(frozen=True)
class BreakerPolicy:
    cpu_percent: float = DEFAULT_CPU_PERCENT
    seconds: int = DEFAULT_SECONDS
    temperature_c: float = DEFAULT_TEMPERATURE_C
    minutes: int = DEFAULT_MINUTES


@dataclass(frozen=True)
class Sample:
    at: float
    """Secondes (horloge monotone)."""
    cpu: float | None
    temperature: float | None


@dataclass(frozen=True)
class Trigger:
    reason: str
    """Phrase marquee pour la traduction, completee par `params`."""
    params: dict[str, float]


def assess(samples: Sequence[Sample], policy: BreakerPolicy) -> Trigger | None:
    if not samples:
        return None
    last = samples[-1]
    if last.temperature is not None and last.temperature >= policy.temperature_c:
        return Trigger(N_("Température de {temperature:.0f} °C (seuil {threshold:.0f} °C)."),
                       {"temperature": last.temperature, "threshold": policy.temperature_c})
    # Les mesures ne tombent jamais pile (une toutes les ~5 s, avec du retard) : la fenetre garde une mesure de
    # marge, sinon une duree courte (10 s) n'etait jamais « couverte » (constate en reel sur le J3455, 2026-11-23).
    window = [sample for sample in samples if sample.at >= last.at - policy.seconds - SAMPLE_SLACK_SECONDS]
    covered = last.at - window[0].at >= policy.seconds * 0.9 if window else False
    values = [sample.cpu for sample in window]
    if covered and values and all(value is not None and value >= policy.cpu_percent for value in values):
        average = sum(value for value in values if value is not None) / len(values)
        return Trigger(N_("tailscaled au-dessus de {threshold:.0f} % d'un cœur depuis {seconds} s "
                          "(moyenne {average:.0f} %)."),
                       {"threshold": policy.cpu_percent, "seconds": policy.seconds, "average": average})
    return None
