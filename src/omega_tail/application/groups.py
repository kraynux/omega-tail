# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Regroupements et modes (lot 6, domain/groups.py) : fichiers de la porte (scripts Lua, listes), apprentissage
de la reference des empreintes, base AS / pays (mise a jour mensuelle), etat pour les ecrans.

Qui fait quoi :
- HAProxy decide seul, connexion par connexion (mode attaque, regles des groupes) ;
- la veille (si elle est activee) apprend toutes les heures et met la base a jour une fois par mois ; sinon
  l'ecran Attaques et decisions apprend quand il est ouvert, et la base se met a jour par son bouton."""
from __future__ import annotations

import contextlib
import json
from collections.abc import Callable, Mapping
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path

from omega_lib.ports.settings_store import SettingsStore

from omega_tail.application.survival import Outcome
from omega_tail.domain.geo import BROWSER_CIPHER_HASHES, HOSTING_ASNS, REFRESH_DAYS
from omega_tail.domain.groups import (
    BROWSER_LIST,
    COUNTRY_LIST,
    GEO_FILE,
    HOSTING_LIST,
    KNOWN_JA4_LIST,
    LEARNING_DAYS,
    REASONS,
    TABLE_AS,
    TABLE_ATTACK,
    TABLE_COUNTRY,
    TABLE_JA4,
    TABLE_REASONS,
    GroupsPolicy,
    Learning,
    Seen,
    groups_from,
    learn,
    learning_left,
    reference,
)
from omega_tail.ports.gate import GateAdmin
from omega_tail.ports.geo import GeoSource
from omega_tail.shared.i18n import N_

SETTING_PREFIX = "groupes_"
POLICY_KEYS = ("mode", "attack_per_s", "calm_minutes", "ja4_per_10s", "as_per_10s", "country_per_10s",
               "countries", "hosting", "known_first")
STATE_FILE = "groupes.json"
LEARN_SECONDS = 3600


@dataclass(frozen=True)
class GroupRow:
    key: str
    rate_10s: int
    count: int
    label: str = ""
    """Nom lisible : navigateur, nom de l'AS, « habituelle »... (phrase du catalogue ou nom propre)"""
    hosting: bool = False
    """AS d'hebergeur ou de nuage (affiche « (hebergeur) » apres le nom, traduit par l'interface)."""


def parse_rows(text: str) -> list[GroupRow]:
    """`show table` d'une table a cle texte : « 0x..: key=AS16509 use=0 exp=86399 conn_cnt=12 conn_rate(10000)=3 »."""
    rows = []
    for line in text.splitlines():
        if "key=" not in line:
            continue
        fields = dict(part.split("=", 1) for part in line.split()[1:] if "=" in part)
        rate = next((value for key, value in fields.items() if key.startswith("conn_rate")), "0")
        count = fields.get("conn_cnt", "0")
        rows.append(GroupRow(fields.get("key", ""), int(rate) if rate.isdigit() else 0,
                             int(count) if count.isdigit() else 0))
    return sorted(rows, key=lambda row: (-row.rate_10s, -row.count, row.key))


@dataclass(frozen=True)
class GroupsStatus:
    lua: bool
    policy: GroupsPolicy
    attack: bool = False
    calm_left_s: int = 0
    learning_days_left: int = 0
    known: int = 0
    base_updated: str = ""
    base_days: int | None = None
    reasons: Mapping[str, int] = field(default_factory=dict)
    """Connexions marquees par motif (7 derniers jours) : refusees si applique, « aurait refuse » sinon."""


@dataclass
class GroupsTools:
    folder: Path
    settings: SettingsStore
    admin: GateAdmin
    source: GeoSource
    now: Callable[[], datetime]
    lua: Callable[[], bool]
    """HAProxy compile avec Lua (sinon : pas de regroupements, porte du lot 4 seule)."""
    scripts: Callable[[], Mapping[str, str]]
    """Scripts Lua de la porte (nom -> texte), copies dans le dossier de la porte."""
    _last_learn: float = 0.0

    # ---- reglages ----
    def policy(self) -> GroupsPolicy:
        values = {key: self.settings.get(SETTING_PREFIX + key) for key in POLICY_KEYS
                  if self.settings.get(SETTING_PREFIX + key) is not None}
        return groups_from(values)

    def save_policy(self, values: Mapping[str, str]) -> GroupsPolicy:
        current = self.policy()
        merged: dict[str, object] = {key: getattr(current, key) for key in POLICY_KEYS}
        merged["countries"] = " ".join(current.countries)
        merged["hosting"] = " ".join(str(number) for number in current.hosting)
        merged.update(values)
        policy = groups_from(merged)
        for key in POLICY_KEYS:
            value = getattr(policy, key)
            if key == "countries":
                value = " ".join(policy.countries)
            elif key == "hosting":
                value = " ".join(str(number) for number in policy.hosting)
            self.settings.set(SETTING_PREFIX + key, str(value))
        return policy

    # ---- etat appris ----
    def _load(self) -> tuple[Learning, dict[str, object]]:
        try:
            data = json.loads((self.folder / STATE_FILE).read_text(encoding="utf-8"))
        except (OSError, ValueError):
            data = {}
        if not isinstance(data, dict):
            data = {}
        seen = {}
        for key, item in dict(data.get("seen") or {}).items():
            if isinstance(item, dict):
                seen[str(key)] = Seen(tuple(item.get("days", ())), int(item.get("count", 0)), int(item.get("last", 0)))
        base = data.get("base") if isinstance(data.get("base"), dict) else {}
        return Learning(str(data.get("since", "")), seen), dict(base or {})

    def _save(self, learning: Learning, base: Mapping[str, object]) -> None:
        data = {"since": learning.since, "seen": {key: asdict(item) for key, item in learning.seen.items()},
                "base": dict(base)}
        temporary = self.folder / f".{STATE_FILE}.tmp"
        temporary.write_text(json.dumps(data, indent=1) + "\n", encoding="utf-8")
        temporary.replace(self.folder / STATE_FILE)

    def learning_days(self) -> int:
        """Jours d'apprentissage restants (0 : la reference compte)."""
        learning, _base = self._load()
        return learning_left(learning, self.now()) if learning.since else LEARNING_DAYS

    def ready(self) -> bool:
        """La reference des empreintes compte (apprentissage termine)."""
        learning, _base = self._load()
        return bool(learning.since) and learning_left(learning, self.now()) == 0

    # ---- fichiers de la porte ----
    def render_args(self) -> dict[str, object]:
        """Ecrit scripts et listes, puis renvoie les arguments de render_config (sans Lua : porte du lot 4)."""
        if not self.lua():
            return {"groups": None, "ja4_ready": False}
        self.folder.mkdir(parents=True, exist_ok=True)
        for name, text in self.scripts().items():
            (self.folder / name).write_text(text, encoding="utf-8")
        policy = self.policy()
        learning, _base = self._load()
        ready = bool(learning.since) and learning_left(learning, self.now()) == 0
        self._write_list(BROWSER_LIST, sorted(BROWSER_CIPHER_HASHES))
        self._write_list(HOSTING_LIST, [f"AS{number}" for number in policy.hosting])
        self._write_list(COUNTRY_LIST, list(policy.countries))
        self._write_list(KNOWN_JA4_LIST, list(reference(learning)) if ready else [])
        return {"groups": policy, "ja4_ready": ready}

    def _write_list(self, name: str, entries: list[str]) -> bool:
        path = self.folder / name
        text = "".join(f"{entry}\n" for entry in entries)
        try:
            if path.read_text(encoding="utf-8") == text:
                return False
        except OSError:
            pass
        path.write_text(text, encoding="utf-8")
        return True

    # ---- apprentissage ----
    def _table(self, name: str) -> list[GroupRow]:
        try:
            return parse_rows(self.admin.command(f"show table {name}"))
        except OSError:
            return []

    def attack(self) -> tuple[bool, int]:
        """(mode attaque, secondes de calme restantes avant le retour au mode normal)."""
        try:
            text = self.admin.command(f"show table {TABLE_ATTACK}")
        except OSError:
            return False, 0
        for line in text.splitlines():
            if "key=" in line:
                fields = dict(part.split("=", 1) for part in line.split()[1:] if "=" in part)
                expires = fields.get("exp", "0")
                return True, int(expires) // 1000 if expires.isdigit() else 0
        return False, 0

    def learn(self, *, force: bool = False) -> bool:
        """Une lecture des empreintes (au plus une par heure sauf `force`). Vrai si la reference a change."""
        moment = self.now()
        if not force and moment.timestamp() - self._last_learn < LEARN_SECONDS:
            return False
        rows = self._table(TABLE_JA4)
        if not rows and not (self.folder / STATE_FILE).exists():
            return False
        self._last_learn = moment.timestamp()
        learning, base = self._load()
        before = reference(learning) if learning_left(learning, moment) == 0 and learning.since else ()
        learning = learn(learning, {row.key: row.count for row in rows}, moment, attack=self.attack()[0])
        self._save(learning, base)
        if learning_left(learning, moment) != 0:
            return False
        after = reference(learning)
        if self._write_list(KNOWN_JA4_LIST, list(after)):
            for entry in sorted(set(after) - set(before)):
                try:
                    self.admin.command(f"add acl {self.folder / KNOWN_JA4_LIST} {entry}")
                except OSError:
                    break
            return True
        return False

    def restart_learning(self) -> Outcome:
        _learning, base = self._load()
        self._save(Learning(self.now().isoformat(), {}), base)
        self._write_list(KNOWN_JA4_LIST, [])
        with contextlib.suppress(OSError):
            self.admin.command(f"clear acl {self.folder / KNOWN_JA4_LIST}")
        return Outcome(True, "Apprentissage recommencé : {days} jours avant que la référence compte.",
                       {"days": 7})

    # ---- base AS / pays ----
    def base_due(self) -> bool:
        _learning, base = self._load()
        if not (self.folder / GEO_FILE).exists():
            return True
        try:
            updated = datetime.fromisoformat(str(base.get("updated", "")))
        except ValueError:
            return True
        return (self.now() - updated).days >= REFRESH_DAYS

    def refresh_base(self, *, reload: bool = True) -> Outcome:
        try:
            countries, asns = self.source.refresh(self.folder, self.now().date())
        except OSError as error:
            return Outcome(False, "Base AS / pays non mise à jour ({error}) : l'ancienne reste en place.",
                           {"error": str(error)})
        learning, base = self._load()
        base = {"updated": self.now().isoformat(), "countries": countries, "asns": asns}
        self._save(learning, base)
        if reload:
            with contextlib.suppress(OSError):  # porte arretee : la base sera lue a son demarrage
                self.admin.master("reload")
        return Outcome(True, "Base AS / pays à jour ({countries} plages pays, {asns} plages AS).",
                       {"countries": countries, "asns": asns})

    # ---- etat pour les ecrans ----
    def status(self) -> GroupsStatus:
        learning, base = self._load()
        moment = self.now()
        attack, left = self.attack()
        days: int | None = None
        try:
            days = (moment - datetime.fromisoformat(str(base.get("updated", "")))).days
        except ValueError:
            days = None
        reasons = {row.key: row.count for row in self._table(TABLE_REASONS) if row.key in REASONS}
        return GroupsStatus(lua=self.lua(), policy=self.policy(), attack=attack, calm_left_s=left,
                            learning_days_left=learning_left(learning, moment) if learning.since else 7,
                            known=len(reference(learning)) if learning.since else 0,
                            base_updated=str(base.get("updated", "")), base_days=days, reasons=reasons)

    def top_fingerprints(self, count: int = 10) -> list[GroupRow]:
        learning, _base = self._load()
        known = set(reference(learning))
        rows = []
        for row in self._table(TABLE_JA4)[:count]:
            parts = row.key.split("_")
            label = BROWSER_CIPHER_HASHES.get(parts[1], "") if len(parts) == 3 else ""
            if not label and row.key in known:
                label = N_("habituelle")
            rows.append(GroupRow(row.key, row.rate_10s, row.count, label))
        return rows

    def top_as(self, count: int = 10) -> list[GroupRow]:
        names = self.source.names(self.folder)
        rows = []
        for row in self._table(TABLE_AS)[:count]:
            number = int(row.key.removeprefix("AS")) if row.key.removeprefix("AS").isdigit() else 0
            label = names.get(number, "") or HOSTING_ASNS.get(number, "")
            rows.append(GroupRow(row.key, row.rate_10s, row.count, label, hosting=number in self.policy().hosting))
        return rows

    def top_countries(self, count: int = 10) -> list[GroupRow]:
        limited = set(self.policy().countries)
        return [GroupRow(row.key, row.rate_10s, row.count, N_("limité en attaque") if row.key in limited else "")
                for row in self._table(TABLE_COUNTRY)[:count]]

    def locate(self, address: str) -> tuple[str, int]:
        return self.source.lookup(self.folder, address)
