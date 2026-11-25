# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Texte d'un resultat d'action, traduit (lot 9, 2026-11-25) : la phrase marquee et ses parametres.

Un parametre peut etre lui-meme une phrase du catalogue (une raison : « HAProxy absent ») ou une phrase suivie d'un
detail (« cible non prise en charge : http://… », « aucun journal trouvé (…) ») : la phrase est traduite, le detail
garde sa forme. Adresses, nombres, noms de fichiers passent tels quels (absents du catalogue)."""
from __future__ import annotations

from typing import TYPE_CHECKING

from omega_tail.shared.i18n import _

if TYPE_CHECKING:
    from omega_tail.application.groups import GroupRow
    from omega_tail.application.survival import Outcome

_DETAIL_SEPARATORS = (" : ", " (")


def localized(value: object) -> object:
    if not isinstance(value, str) or not value:
        return value
    translated = _(value)
    if translated != value:
        return translated
    for separator in _DETAIL_SEPARATORS:
        head, found, tail = value.partition(separator)
        if found and head:
            head_translated = _(head)
            if head_translated != head:
                return f"{head_translated}{found}{tail}"
    return value


def group_label(row: GroupRow) -> str:
    """Nom d'un groupe (empreinte, AS, pays) dans la langue : phrase du catalogue (« habituelle », navigateurs) ou nom
    propre (AS), suivi de « (hébergeur) » pour un AS d'hébergeur (2026-11-25 : ces libellés restaient en français)."""
    name = str(localized(row.label)) if row.label else ""
    if row.hosting:
        return _("{name} (hébergeur)").format(name=name) if name else _("hébergeur")
    return name


def outcome_text(outcome: Outcome) -> str:
    return _(outcome.message).format(**{key: localized(value) for key, value in outcome.params.items()})
