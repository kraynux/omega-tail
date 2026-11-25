# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""`omega-tail.sh synchro jeton [--format json]` (compatibilite omega-connect, 2026-11-25) : carte d'identite lue
par omega-connect (Registre, Synchroniser, Reparer, Updater, Installer), sans interface ni banniere, sortie JSON
non traduite. Meme format que les autres outils omega (omega_lib.infrastructure.synchro.install_token, copie de
celui d'omega-stress) : jamais ecrit en root, seul le proprietaire du dossier l'ecrit, `var/omega-jeton.json`,
exclu de l'archive. Pas de fiche d'instance pour l'instant."""
from __future__ import annotations

import sys

TAIL_TOOL = "omega-tail"
USAGE = "usage: omega-tail.sh synchro jeton [--format json]"


def run_synchro(argv: list[str]) -> int:
    from omega_lib.infrastructure.declaration.app_version import project_version
    from omega_lib.infrastructure.synchro.files import dumps
    from omega_lib.infrastructure.synchro.install_token import refresh_install_token
    from omega_lib.synchro.codec import token_to_dict

    from omega_tail.app.main import project_root

    args = list(argv)
    if args[-2:] == ["--format", "json"]:
        args = args[:-2]
    if args != ["jeton"]:
        print(USAGE, file=sys.stderr)
        return 2
    root = project_root()
    refresh = refresh_install_token(root, TAIL_TOOL, project_version(root, TAIL_TOOL))
    if refresh.token is None:
        print(f"omega-tail: installation token not written ({refresh.path}): {refresh.reason}", file=sys.stderr)
        return 1
    print(dumps(token_to_dict(refresh.token)), end="")
    return 0
