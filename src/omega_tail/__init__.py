# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""omega-tail : pilotage de Tailscale et protection de Funnel. La version est lue dans pyproject.toml, seule source
(procedure de verification, etape B) : splash, barre de titre et « Contact et support » affichent le
meme numero."""
from pathlib import Path

from omega_lib.infrastructure.declaration.app_version import project_version

__version__ = project_version(Path(__file__).resolve().parents[2], "omega-tail")
