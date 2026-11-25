# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""La machine : processeur, charge, temperature, consommation de tailscaled."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class MachineState:
    hostname: str = ""
    cpu_count: int = 0
    load: tuple[float, float, float] = (0.0, 0.0, 0.0)
    temperature_c: float | None = None
    """Temperature la plus haute des capteurs lisibles (None : aucun capteur)."""
    cpu_percent: float | None = None
    """CPU de toute la machine, en % de tous ses coeurs, entre deux lectures de /proc/stat (None a la premiere).
    Distinct de celui de tailscaled (retour d'utilisation, 2026-11-24 : la barre ne montrait que tailscaled)."""
    tailscaled_cpu_percent: float | None = None
    """En % d'UN coeur, entre deux lectures (None a la premiere lecture)."""
    tailscaled_rss_bytes: int | None = None
    memory_total_bytes: int | None = None
    memory_available_bytes: int | None = None
    """Memoire disponible sans rien liberer de force (MemAvailable : caches recuperables compris)."""

    @property
    def memory_used_percent(self) -> float | None:
        total, available = self.memory_total_bytes, self.memory_available_bytes
        if not total or available is None:
            return None
        return max(0.0, min(100.0, 100 * (total - available) / total))

    @property
    def load_per_core(self) -> float | None:
        """Charge sur 1 min rapportee au nombre de coeurs (1,0 = tous les coeurs occupes)."""
        return self.load[0] / self.cpu_count if self.cpu_count else None
