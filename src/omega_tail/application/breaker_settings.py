# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Seuils du disjoncteur, enregistres dans var/settings.json (valeur absente ou invalide : valeur par defaut)."""
from __future__ import annotations

from omega_lib.ports.settings_store import SettingsStore

from omega_tail.domain.breaker import BreakerPolicy
from omega_tail.domain.watch import DEFAULT_WINDOW_MINUTES

KEY_CPU = "breaker_cpu_percent"
KEY_SECONDS = "breaker_seconds"
KEY_TEMPERATURE = "breaker_temperature_c"
KEY_MINUTES = "breaker_minutes"
KEY_WINDOW = "watch_window_minutes"
"""Veille automatique : fenetre ou 3 depassements declenchent la coupure."""
LIMITS = {KEY_CPU: (10.0, 400.0), KEY_SECONDS: (10.0, 3600.0), KEY_TEMPERATURE: (50.0, 110.0),
          KEY_MINUTES: (1.0, 1440.0), KEY_WINDOW: (2.0, 240.0)}
INTEGERS = (KEY_SECONDS, KEY_MINUTES, KEY_WINDOW)


def _number(store: SettingsStore, key: str, default: float) -> float:
    low, high = LIMITS[key]
    try:
        value = float(store.get(key) or "")
    except ValueError:
        return default
    return value if low <= value <= high else default


def load_policy(store: SettingsStore) -> BreakerPolicy:
    base = BreakerPolicy()
    return BreakerPolicy(cpu_percent=_number(store, KEY_CPU, base.cpu_percent),
                         seconds=int(_number(store, KEY_SECONDS, base.seconds)),
                         temperature_c=_number(store, KEY_TEMPERATURE, base.temperature_c),
                         minutes=int(_number(store, KEY_MINUTES, base.minutes)))


def load_window(store: SettingsStore) -> int:
    return int(_number(store, KEY_WINDOW, DEFAULT_WINDOW_MINUTES))


def save_policy(store: SettingsStore, values: dict[str, str]) -> list[str]:
    """Enregistre les valeurs valides ; renvoie les cles refusees (hors bornes ou pas un nombre)."""
    refused = []
    for key, text in values.items():
        low, high = LIMITS[key]
        try:
            value = float(text.replace(",", ".").strip())
        except ValueError:
            refused.append(key)
            continue
        if not low <= value <= high:
            refused.append(key)
            continue
        store.set(key, str(int(value)) if key in INTEGERS else str(value))
    return refused
