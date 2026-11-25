# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Piege du demarrage (trouve en production, 2026-11-23) : un fichier d'ajout de l'utilisateur lance
`tailscale up ...` apres le demarrage (ExecStartPost). Des qu'un reglage change ensuite par `tailscale set`
(operateur, nom, routes...), Tailscale refuse ce `up` qui ne les redonne pas tous ; systemd voit la commande
echouer, arrete tailscaled, reessaie, puis abandonne : la machine sort du tailnet au premier redemarrage.

Correction proposee (montree, confirmee, sauvegardee) : le prefixe « - » de systemd devant cette commande (son echec
n'arrete plus le service). Les reglages, eux, sont deja gardes par Tailscale d'un demarrage a l'autre."""
from __future__ import annotations

import re

from omega_tail.domain.service import ServiceState

_LINE = re.compile(r"^(\s*ExecStart(?:Pre|Post)\s*=\s*)(\S.*?)(\s*)$")
_PREFIXES = "@-:+!"
FIXABLE_ROOT = "/etc/systemd/"
"""Seuls les fichiers de l'administrateur sont corriges, jamais ceux du paquet (/usr/lib : ecrases a la mise a jour)."""


def is_risky_up(command: str) -> bool:
    """`tailscale up` sans `--reset` : refuse des qu'un reglage non repris a change."""
    words = command.lstrip(_PREFIXES).split()
    if not words or words[0].rsplit("/", 1)[-1] != "tailscale":
        return False
    return "up" in words[1:] and "--reset" not in words


def risky_hooks(service: ServiceState) -> tuple[str, ...]:
    return tuple(hook for hook in service.start_hooks if is_risky_up(hook))


def soften(text: str) -> str:
    """Ajoute « - » devant chaque ExecStartPre / ExecStartPost qui lance un `tailscale up` risque ; rien d'autre."""
    out: list[str] = []
    for line in text.splitlines(keepends=True):
        body = line.rstrip("\r\n")
        match = _LINE.match(body)
        if match:
            command = match.group(2)
            leading = command[:len(command) - len(command.lstrip(_PREFIXES))]
            if "-" not in leading and is_risky_up(command):
                line = match.group(1) + "-" + command + match.group(3) + line[len(body):]
        out.append(line)
    return "".join(out)


def fixable(path: str) -> bool:
    return path.startswith(FIXABLE_ROOT) and ".." not in path
