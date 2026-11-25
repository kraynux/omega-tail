# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Pare-feu Funnel (lot 4, plan B) : preparer, activer, regler et desactiver la porte HAProxy.

Ordre d'activation (chaque etape s'arrete au premier echec, rien n'est laisse a moitie) :
1. preparer, sans droits : publication prise en charge ? certificat `*.ts.net` (`tailscale cert`, operateur),
   listes, configuration ecrite puis verifiee (`haproxy -c`), fichiers des services systemd ;
2. services (sudo, dans le terminal) : porte sous le compte de l'utilisateur + minuterie de renouvellement ;
3. basculer, sans droits : essai local de la porte, sauvegarde de la publication, Funnel en TCP + PROXY v2 vers
   la porte, essai PUBLIC par le relais ; en cas d'echec, la publication d'origine est remise aussitot.
Desactiver : publication d'origine remise et verifiee, puis arret des services (sudo)."""
from __future__ import annotations

import contextlib
import ipaddress
import json
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

from omega_lib.ports.settings_store import SettingsStore

from omega_tail.application.groups import GroupsTools
from omega_tail.application.survival import Outcome
from omega_tail.domain.blacklist import (
    BLACKLIST_MAX,
    ORIGIN_EXISTING,
    ORIGIN_MANUAL,
    ORIGIN_SCREEN,
    BlackEntry,
    ImportReport,
    PurgeChoice,
    covered,
    is_canonical,
    normalize,
    ordered,
    parse_import,
    select_purge,
)
from omega_tail.domain.funnel import restore_commands, same_publication
from omega_tail.domain.gate import (
    BLACK_JSON,
    BLACK_LIST,
    CRON_MARKER,
    DEFAULT_GATE_PORT,
    SERVICE_UNIT,
    TABLE_IP,
    TAILNET_NETWORKS,
    TRUST_LIST,
    GatePolicy,
    GateTarget,
    UnsupportedPublication,
    cron_line,
    gate_target,
    openrc_script,
    policy_from,
    render_config,
    runit_log_script,
    runit_run_script,
    switch_commands,
    unit_text,
    unswitch_commands,
)
from omega_tail.domain.groups import GROUPS_APPLY, GROUPS_OBSERVE
from omega_tail.domain.init import GATE_NAMES, InitSystem
from omega_tail.ports.gate import GateAdmin, GateMachine
from omega_tail.ports.survival import CutStore, QuietCommand
from omega_tail.shared.i18n import N_

POLICY_KEYS = ("mode", "ip_per_10s", "prefix_per_10s", "global_per_s", "max_connections", "block_minutes",
               "check_sni")
SETTING_PREFIX = "porte_"
TIMER_UNIT = "omega-tail-porte-certificat.timer"
TIMER_SERVICE = "omega-tail-porte-certificat.service"
SYSTEMD_DIR = "/etc/systemd/system"
CERT_RENEW_DAYS = 30


TRUSTED, BLACK = "confiance", "liste-noire"


@dataclass(frozen=True)
class TableRow:
    address: str
    rate_10s: int
    blocked: bool
    expires_s: int
    listed: str = ""
    """TRUSTED, BLACK ou vide : la liste ou se trouve l'adresse (ou le reseau qui la contient)."""
    seen: bool = True
    """Faux : adresse des listes, sans connexion recente (pas dans la table de HAProxy)."""


def classifier(trusted: list[str], black: list[str]) -> Callable[[str], str]:
    """Place d'une adresse (TRUSTED, BLACK ou vide), listes analysees UNE fois : l'ecran Attaques classe chaque
    ligne toutes les 2 s, et la liste noire peut compter 50 000 entrees (adresses seules : recherche directe ;
    reseaux : parcourus, ils sont peu nombreux). La confiance et le tailnet passent avant (accept en premier)."""
    def split(entries: list[str]) -> tuple[set[str], list[ipaddress.IPv4Network | ipaddress.IPv6Network]]:
        singles: set[str] = set()
        networks: list[ipaddress.IPv4Network | ipaddress.IPv6Network] = []
        for entry in entries:
            if "/" not in entry:  # deja ecrite sous forme canonique par omega-tail : pas d'analyse (50 000 lignes)
                singles.add(entry)
                continue
            try:
                network = ipaddress.ip_network(entry, strict=False)
            except ValueError:
                continue
            if network.num_addresses == 1:
                singles.add(str(network.network_address))
            else:
                networks.append(network)
        return singles, networks

    trusted_singles, trusted_networks = split([*trusted, *TAILNET_NETWORKS])
    black_singles, black_networks = split(black)

    def inside(ip: ipaddress.IPv4Address | ipaddress.IPv6Address, singles: set[str],
               networks: list[ipaddress.IPv4Network | ipaddress.IPv6Network]) -> bool:
        return str(ip) in singles or any(ip.version == network.version and ip in network for network in networks)

    def classify(address: str) -> str:
        try:
            ip = ipaddress.ip_address(address)
        except ValueError:
            return ""
        if isinstance(ip, ipaddress.IPv6Address) and ip.ipv4_mapped is not None:
            ip = ip.ipv4_mapped
        if inside(ip, trusted_singles, trusted_networks):
            return TRUSTED
        return BLACK if inside(ip, black_singles, black_networks) else ""

    return classify


def place(address: str, trusted: list[str], black: list[str]) -> str:
    """Liste qui contient l'adresse (adresse ou reseau). La confiance passe avant (accept en premier dans HAProxy)."""
    return classifier(trusted, black)(address)


def in_tailnet(entry: str) -> bool:
    """Adresse ou reseau entierement dans le tailnet : la porte l'admet toujours, la bloquer n'aurait aucun effet
    (un reseau plus large, ex. 100.0.0.0/8, reste blocable : seule sa part publique sera refusee)."""
    try:
        network = ipaddress.ip_network(entry, strict=False)
    except ValueError:
        return False
    return any(network.version == tailnet.version and network.subnet_of(tailnet)  # type: ignore[arg-type]
               for tailnet in map(ipaddress.ip_network, TAILNET_NETWORKS))


def decision_rows(rows: list[TableRow], trusted: list[str], black: list[str]) -> list[TableRow]:
    """Table de HAProxy completee par les listes : chaque adresse dit ou elle se trouve ; les entrees des listes
    sans connexion recente sont ajoutees. Ordre : liste noire, bloquees, plus actives, confiance."""
    classify = classifier(trusted, black)
    found = [TableRow(row.address, row.rate_10s, row.blocked, row.expires_s, classify(row.address)) for row in rows]
    known = {row.address for row in found}
    found += [TableRow(entry, 0, False, 0, BLACK, seen=False) for entry in black if entry not in known]
    found += [TableRow(entry, 0, False, 0, TRUSTED, seen=False) for entry in trusted if entry not in known]
    order = {BLACK: 0, "": 1, TRUSTED: 2}
    return sorted(found, key=lambda row: (order[row.listed], not row.blocked, -row.rate_10s))


@dataclass(frozen=True)
class GateCounters:
    total: int = 0
    current: int = 0
    refused: int = 0
    admitted: int = 0


@dataclass(frozen=True)
class GateState:
    """Bascule en cours (var/porte/etat.json)."""
    public_port: int
    gate_port: int
    saved: str
    since: str
    dns_name: str = ""
    backend: str = ""


def parse_table(text: str) -> list[TableRow]:
    """`show table porte_ip` : « 0x..: key=::ffff:1.2.3.4 use=0 exp=3599 shard=0 gpc0=1 conn_rate(10000)=57 »."""
    rows = []
    for line in text.splitlines():
        if "key=" not in line:
            continue
        fields = dict(part.split("=", 1) for part in line.split()[1:] if "=" in part)
        address = fields.get("key", "").removeprefix("::ffff:")
        rate = next((value for key, value in fields.items() if key.startswith("conn_rate")), "0")
        rows.append(TableRow(address, int(rate) if rate.isdigit() else 0, fields.get("gpc0", "0") not in ("0", ""),
                             int(fields.get("exp", "0")) // 1000 if fields.get("exp", "0").isdigit() else 0))
    return sorted(rows, key=lambda row: (not row.blocked, -row.rate_10s))


def parse_counters(stat_csv: str) -> GateCounters:
    lines = stat_csv.strip().splitlines()
    if not lines:
        return GateCounters()
    header = lines[0].lstrip("# ").split(",")
    values: dict[str, dict[str, str]] = {}
    for line in lines[1:]:
        row = dict(zip(header, line.split(","), strict=False))
        if row.get("svname") == "FRONTEND":
            values[row.get("pxname", "")] = row

    def number(proxy: str, key: str) -> int:
        text = values.get(proxy, {}).get(key, "")
        return int(text) if text.isdigit() else 0

    refused = number("porte", "dcon") + number("porte", "dses") + number("porte", "dreq")
    return GateCounters(total=number("porte", "stot"), current=number("porte", "scur"), refused=refused,
                        admitted=number("porte_tls", "stot"))


def _address(text: str) -> str:
    """Adresse ou reseau valide, ecrit sous forme canonique ; leve ValueError sinon (aucun texte libre ne part, ni
    identifiant de zone IPv6 : scan de securite 2026-11-25, F3)."""
    return normalize(text)


@dataclass
class GateTools:
    folder: Path
    settings: SettingsStore
    admin: GateAdmin
    machine: GateMachine
    store: CutStore
    serve_config: Callable[[], dict[str, Any]]
    quiet: QuietCommand
    dns_name: Callable[[], str]
    user: Callable[[], str]
    python: str
    now: Callable[[], datetime]
    as_root: bool = False
    gate_port: int = DEFAULT_GATE_PORT
    init: InitSystem = InitSystem.SYSTEMD
    runit_dir: str = "/var/service"
    """Dossier des services actifs de runit (Void : /var/service)."""
    groups: GroupsTools | None = None
    """Regroupements du lot 6 (AS, pays, JA4, modes) ; None : porte du lot 4 seule."""
    run_tool: Callable[[Sequence[str]], tuple[int, str]] | None = None
    """Commande longue d'omega-tail dans un processus a part (None : dans ce processus, comme les essais)."""
    _last_target: GateTarget | None = field(default=None, repr=False)

    # ---- chemins ----
    def path(self, name: str) -> Path:
        return self.folder / name

    @property
    def config_path(self) -> Path:
        return self.path("haproxy.cfg")

    @property
    def pem_path(self) -> Path:
        return self.path("certificat.pem")

    def _sudo(self, *command: str) -> tuple[str, ...]:
        return command if self.as_root else ("sudo", *command)

    # ---- reglages ----
    def policy(self) -> GatePolicy:
        return policy_from({key: self.settings.get(SETTING_PREFIX + key) or "" for key in POLICY_KEYS
                            if self.settings.get(SETTING_PREFIX + key)})

    def save_policy(self, values: Mapping[str, str]) -> GatePolicy:
        merged = {**{key: getattr(self.policy(), key) for key in POLICY_KEYS}, **values}
        policy = policy_from(merged)
        for key in POLICY_KEYS:
            self.settings.set(SETTING_PREFIX + key, str(getattr(policy, key)))
        return policy

    def _group_args(self) -> dict[str, Any]:
        return self.groups.render_args() if self.groups is not None else {}

    # ---- etat ----
    def state(self) -> GateState | None:
        try:
            data = json.loads(self.path("etat.json").read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return None
        if not isinstance(data, dict) or not data.get("saved"):
            return None
        return GateState(int(data.get("public_port", 443)), int(data.get("gate_port", self.gate_port)),
                         str(data["saved"]), str(data.get("since", "")), str(data.get("dns_name", "")),
                         str(data.get("backend", "")))

    def _write_state(self, state: GateState | None) -> None:
        path = self.path("etat.json")
        if state is None:
            path.unlink(missing_ok=True)
            return
        path.write_text(json.dumps(state.__dict__, indent=2) + "\n", encoding="utf-8")

    def counters(self) -> GateCounters:
        try:
            return parse_counters(self.admin.command("show stat"))
        except OSError:
            return GateCounters()

    def top(self) -> list[TableRow]:
        try:
            return parse_table(self.admin.command(f"show table {TABLE_IP}"))
        except OSError:
            return []

    def decisions(self) -> list[TableRow]:
        trusted, black = self.lists()
        return decision_rows(self.top(), trusted, black)

    def _list_outcome(self, message: str, params: dict[str, object]) -> Outcome:
        """Precise si la porte est arretee : les listes ne s'appliqueront qu'a son activation."""
        return Outcome(True, message, {**params, "inactive": self.state() is None})

    def certificate_days(self) -> int | None:
        return self.machine.certificate_expiry_days(str(self.pem_path)) if self.pem_path.exists() else None

    def lists(self) -> tuple[list[str], list[str]]:
        def read(name: str) -> list[str]:
            try:
                return [line.strip() for line in self.path(name).read_text().splitlines() if line.strip()]
            except OSError:
                return []
        return read(TRUST_LIST), read(BLACK_LIST)

    # ---- activation ----
    def install_command(self) -> tuple[str, ...]:
        return self.machine.install_command()

    def target(self) -> GateTarget:
        """Publication actuelle prise en charge ? Leve UnsupportedPublication avec la raison."""
        return gate_target(self.serve_config(), self.dns_name())

    def renew_certificate(self, *, hot: bool = False) -> Outcome:
        dns = self.dns_name()
        if not dns:
            return Outcome(False, "Nom de la machine inconnu : Tailscale est-il connecté ?", {})
        self.folder.mkdir(parents=True, exist_ok=True)
        cert, key = self.path("certificat.crt"), self.path("certificat.key")
        ok, reason = self.machine.fetch_certificate(dns, str(cert), str(key))
        if not ok:
            return Outcome(False, "Certificat refusé ({error}). Êtes-vous opérateur de Tailscale ?", {"error": reason})
        pem = cert.read_text() + key.read_text()
        temporary = self.path(".certificat.pem.tmp")
        temporary.touch(mode=0o600)
        temporary.write_text(pem)
        temporary.replace(self.pem_path)
        if hot:
            try:
                self.admin.command(f"set ssl cert {self.pem_path} <<\n{pem}\n")
                self.admin.command(f"commit ssl cert {self.pem_path}")
            except OSError as error:
                return Outcome(False, "Certificat renouvelé, mais la porte ne l'a pas repris ({error}).",
                               {"error": str(error)})
        return Outcome(True, "Certificat de {name} à jour.", {"name": dns})

    def prepare(self) -> Outcome:
        try:
            target = self.target()
        except UnsupportedPublication as error:
            return Outcome(False, "Publication non prise en charge : {reason}.", {"reason": str(error)})
        except OSError as error:
            return Outcome(False, "Publication illisible ({error}).", {"error": str(error)})
        haproxy = self.machine.haproxy()
        if not haproxy:
            return Outcome(False, "HAProxy n'est pas installé : « Installer HAProxy » d'abord.", {})
        outcome = self.renew_certificate()
        if not outcome.ok:
            return outcome
        for name in (TRUST_LIST, BLACK_LIST):
            self.path(name).touch(exist_ok=True)
        self.config_path.write_text(render_config(self.policy(), target, gate_port=self.gate_port,
                                                  folder=str(self.folder), **self._group_args()),
                                    encoding="utf-8")
        ok, reason = self.machine.check_config(str(self.config_path))
        if not ok:
            return Outcome(False, "Configuration de la porte refusée par HAProxy : {error}", {"error": reason})
        self._write_service_files(haproxy)
        if self.init is not InitSystem.SYSTEMD:
            ok, reason = self.machine.set_cron(CRON_MARKER, cron_line(self.python))
            if not ok:
                return Outcome(False, "Renouvellement du certificat non programmé (crontab : {error}).",
                               {"error": reason})
        self._last_target = target
        return Outcome(True, "Porte prête : certificat, listes et configuration vérifiés.", {})

    def _write_service_files(self, haproxy: str) -> None:
        user, folder = self.user(), str(self.folder)
        if self.init is InitSystem.OPENRC:
            self.path("omega-tail-porte.openrc").write_text(openrc_script(user=user, haproxy=haproxy, folder=folder))
        elif self.init is InitSystem.RUNIT:
            self.path("log").mkdir(exist_ok=True)
            self.path("sv-run").write_text(runit_run_script(user=user, haproxy=haproxy, folder=folder))
            self.path("sv-log-run").write_text(runit_log_script(user=user, folder=folder))
        else:
            self.path(SERVICE_UNIT).write_text(unit_text(user=user, haproxy=haproxy, folder=folder))
            self.path(TIMER_SERVICE).write_text(self._timer_service_text())
            self.path(TIMER_UNIT).write_text(self._timer_text())

    def _timer_service_text(self) -> str:
        return ("# omega-tail - renouvellement du certificat de la porte (sous le compte de l'utilisateur).\n"
                "[Unit]\nDescription=omega-tail : renouvellement du certificat de la porte\n\n"
                f"[Service]\nType=oneshot\nUser={self.user()}\n"
                f"ExecStart={self.python} -m omega_tail porte certificat --si-besoin\n")

    @staticmethod
    def _timer_text() -> str:
        return ("# omega-tail - verification quotidienne du certificat de la porte.\n"
                "[Unit]\nDescription=omega-tail : certificat de la porte\n\n"
                "[Timer]\nOnCalendar=daily\nPersistent=true\nRandomizedDelaySec=1h\n\n"
                "[Install]\nWantedBy=timers.target\n")

    def service_commands(self) -> list[tuple[str, ...]]:
        name = GATE_NAMES[self.init]
        if self.init is InitSystem.OPENRC:
            script = str(self.path("omega-tail-porte.openrc"))
            return [self._sudo("install", "-m", "0755", script, f"/etc/init.d/{name}"),
                    self._sudo("rc-update", "add", name, "default"),
                    self._sudo("rc-service", name, "restart")]
        if self.init is InitSystem.RUNIT:
            folder = f"/etc/sv/{name}"
            return [self._sudo("install", "-D", "-m", "0755", str(self.path("sv-run")), f"{folder}/run"),
                    self._sudo("install", "-D", "-m", "0755", str(self.path("sv-log-run")), f"{folder}/log/run"),
                    self._sudo("ln", "-sfn", folder, f"{self.runit_dir}/{name}"),
                    self._sudo("sh", "-c", f"sleep 6; sv restart {self.runit_dir}/{name} || true")]
        commands = [self._sudo("install", "-m", "0644", str(self.path(unit)), f"{SYSTEMD_DIR}/{unit}")
                    for unit in (SERVICE_UNIT, TIMER_SERVICE, TIMER_UNIT)]
        commands.append(self._sudo("systemctl", "daemon-reload"))
        commands.append(self._sudo("systemctl", "enable", "--now", SERVICE_UNIT, TIMER_UNIT))
        commands.append(self._sudo("systemctl", "restart", SERVICE_UNIT))
        return commands

    def stop_commands(self) -> list[tuple[str, ...]]:
        name = GATE_NAMES[self.init]
        if self.init is not InitSystem.SYSTEMD:
            self.machine.set_cron(CRON_MARKER, "")
        if self.init is InitSystem.OPENRC:
            return [self._sudo("rc-service", name, "stop"), self._sudo("rc-update", "del", name, "default")]
        if self.init is InitSystem.RUNIT:
            return [self._sudo("sv", "down", f"{self.runit_dir}/{name}"),
                    self._sudo("rm", "-f", f"{self.runit_dir}/{name}")]
        return [self._sudo("systemctl", "disable", "--now", SERVICE_UNIT, TIMER_UNIT)]

    def switch(self, *, wait: Callable[[float], None] | None = None) -> Outcome:
        """Funnel -> porte. Essai local d'abord ; essai public ensuite, sinon retour arriere immediat."""
        if self.state() is not None:
            return Outcome(False, "La porte protège déjà Funnel.", {})
        try:
            config = self.serve_config()
            target = gate_target(config, self.dns_name())
        except (UnsupportedPublication, OSError) as error:
            return Outcome(False, "Publication non prise en charge : {reason}.", {"reason": str(error)})
        ok, detail = self.machine.local_probe(self.gate_port, target.dns_name)
        if not ok:
            return Outcome(False, "La porte ne répond pas en local ({detail}) : rien n'a été basculé.",
                           {"detail": detail})
        cut_id = "porte-" + self.now().strftime("%Y%m%d-%H%M%S")
        saved = self.store.save_publication(cut_id, config)
        self._write_state(GateState(target.public_port, self.gate_port, saved, self.now().isoformat(),
                                    target.dns_name, target.backend.address))
        for command in switch_commands(target, self.gate_port):
            code, reason = self.quiet(command)
            if code != 0:
                self._rollback(target.public_port, config)
                return Outcome(False, "Bascule refusée ({error}) : publication d'origine remise.",
                               {"error": reason or code})
        detail = ""
        for _attempt in range(5):
            if wait is not None:
                wait(3.0)
            ok, detail = self.machine.public_probe(target.dns_name, target.public_port)
            if ok:
                self.store.log(f"porte {cut_id} : Funnel {target.public_port} -> 127.0.0.1:{self.gate_port}")
                return Outcome(True, "Funnel passe par la porte : essai public réussi ({detail}).", {"detail": detail})
        self._rollback(target.public_port, config)
        return Outcome(False, "Essai public échoué ({detail}) : publication d'origine remise.", {"detail": detail})

    def _rollback(self, public_port: int, config: Mapping[str, Any]) -> None:
        for command in (*unswitch_commands(public_port), *restore_commands(config)):
            self.quiet(command)
        self._write_state(None)
        self.store.log(f"porte : retour arriere vers la publication d'origine (port {public_port})")

    def unswitch(self) -> Outcome:
        state = self.state()
        if state is None:
            return Outcome(True, "La porte ne protège pas Funnel : rien à remettre.", {})
        saved = self.store.load_publication(state.saved)
        errors = []
        for command in (*unswitch_commands(state.public_port), *restore_commands(saved)):
            code, error = self.quiet(command)
            if code != 0:
                errors.append(error or str(code))
        if not same_publication(saved, self.serve_config()):
            return Outcome(False, "Publication d'origine incomplète ({errors}) : sauvegarde gardée dans {path}.",
                           {"errors": " ; ".join(errors) or "?", "path": state.saved})
        self._write_state(None)
        self.store.log(f"porte : publication d'origine remise (port {state.public_port})")
        return Outcome(True, "Publication d'origine remise, à l'identique.", {})

    # ---- reglages a chaud ----
    def apply_policy(self, values: Mapping[str, str]) -> Outcome:
        policy = self.save_policy(values)
        state = self.state()
        if state is None or not self.config_path.exists():
            return Outcome(True, "Règles enregistrées ; elles s'appliqueront à l'activation.", {})
        try:
            target = gate_target(self.store.load_publication(state.saved), state.dns_name)
        except (UnsupportedPublication, OSError) as error:
            return Outcome(False, "Règles enregistrées, configuration non régénérée ({error}).", {"error": str(error)})
        previous = self.config_path.read_text(encoding="utf-8")
        self.config_path.write_text(render_config(policy, target, gate_port=state.gate_port, folder=str(self.folder),
                                                  **self._group_args()))
        ok, reason = self.machine.check_config(str(self.config_path))
        if not ok:
            self.config_path.write_text(previous)
            return Outcome(False, "Règles refusées par HAProxy ({error}) : ancienne configuration gardée.",
                           {"error": reason})
        try:
            self.admin.master("reload")
        except OSError as error:
            return Outcome(False, "Règles écrites, rechargement impossible ({error}).", {"error": str(error)})
        return Outcome(True, "Règles appliquées à chaud (mode {mode}).", {"mode": policy.mode})

    def apply_groups(self, values: Mapping[str, str]) -> Outcome:
        """Regroupements (lot 6) enregistres puis appliques a chaud (meme chemin que les regles)."""
        if self.groups is None:
            return Outcome(False, "Regroupements indisponibles.", {})
        policy = self.groups.save_policy(values)
        held = 0
        if policy.mode == GROUPS_APPLY and not self.groups.ready():
            # Lien apprentissage -> observation : sans reference, « appliques » refuserait des clients legitimes
            # qui ne sont pas des navigateurs (incident en production du 2026-11-23, mode choisi pendant l'essai).
            held = self.groups.learning_days()
            policy = self.groups.save_policy({"mode": GROUPS_OBSERVE})
        outcome = self.apply_policy({})
        if not outcome.ok:
            return outcome
        if held:
            return Outcome(True, "Apprentissage des empreintes en cours (encore {days} jour(s)) : les regroupements "
                                 "restent en observation jusqu'à la fin ; « appliqués » sera possible ensuite.",
                           {"days": held, "warning": True})
        if self.state() is not None:
            mode = N_("appliqués") if policy.mode == GROUPS_APPLY else N_("en observation")
            return Outcome(True, "Regroupements appliqués à chaud ({mode}).", {"mode": mode})
        return outcome

    def restart_learning(self) -> Outcome:
        """Recommencer l'apprentissage remet aussi les regroupements en observation (meme lien qu'a l'application)."""
        if self.groups is None:
            return Outcome(False, "Regroupements indisponibles.", {})
        outcome = self.groups.restart_learning()
        if self.groups.policy().mode != GROUPS_APPLY:
            return outcome
        self.groups.save_policy({"mode": GROUPS_OBSERVE})
        applied = self.apply_policy({})
        if not applied.ok:
            return applied
        return Outcome(True, "Apprentissage recommencé : regroupements repassés en observation pour les {days} "
                             "jours d'apprentissage.", {"days": self.groups.learning_days()})

    def _list_change(self, name: str, address: str, add: bool) -> None:
        if name == BLACK_LIST:
            entries = [entry for entry in self.black_entries() if entry.address != address]
            if add:
                entries.append(BlackEntry(address, self.now(), ORIGIN_SCREEN))
            self._save_black(entries)
        else:
            kept = [entry for entry in self.lists()[0] if entry != address]
            self.path(name).write_text("".join(f"{entry}\n" for entry in [*kept, *([address] if add else [])]))
        with contextlib.suppress(OSError):  # porte arretee : la liste sera lue au prochain demarrage
            self.admin.command(f"{'add' if add else 'del'} acl {self.path(name)} {address}")

    def refresh_base(self) -> Outcome:
        """Base AS / pays : telechargee et preparee dans un processus a part quand c'est possible (le calcul en
        Python figeait l'ecran, meme lance dans un fil ; retour d'utilisation 2026-11-24)."""
        if self.groups is None:
            return Outcome(False, "Regroupements indisponibles.", {})
        if self.run_tool is None:
            return self.groups.refresh_base(reload=self.state() is not None)
        code, text = self.run_tool((self.python, "-m", "omega_tail", "porte", "base"))
        if code == 124:
            return Outcome(False, "Base AS / pays : trop longue (plus de 15 minutes), abandonnée ; l'ancienne reste "
                                  "en place.", {})
        return Outcome(code == 0, "{text}", {"text": text or "?"})

    # ---- liste noire : dates, origines, plafond (finitions 0.7.0) ----
    def black_entries(self) -> list[BlackEntry]:
        """`noire.json` (dates, origines) complete par `noire.lst` : une adresse ajoutee a la main dans le fichier
        d'HAProxy, ou une liste d'avant les dates, recoit la date du fichier et l'origine « existant »."""
        dated: dict[str, BlackEntry] = {}
        with contextlib.suppress(OSError, ValueError, KeyError, TypeError):
            for item in json.loads(self.path(BLACK_JSON).read_text(encoding="utf-8")):
                added = datetime.fromisoformat(str(item["ajout"]))
                entry = BlackEntry(str(item["adresse"]), added if added.tzinfo else added.astimezone(),
                                   str(item.get("origine", ORIGIN_SCREEN)))
                dated[entry.address] = entry
        listed = self.lists()[1]
        if listed:
            try:
                since = datetime.fromtimestamp(self.path(BLACK_LIST).stat().st_mtime).astimezone()
            except OSError:
                since = self.now()
            for address in listed:
                if address not in dated:
                    dated[address] = BlackEntry(address, since, ORIGIN_EXISTING)
        listed_set = set(listed)
        # Une ligne qui n'est pas une adresse canonique (fichier modifie a la main, ou import d'avant le correctif F3
        # du 2026-11-25) est ecartee : elle disparait des deux fichiers a la prochaine ecriture.
        return ordered(entry for entry in dated.values()
                       if (entry.address in listed_set or not listed) and is_canonical(entry.address))

    def _save_black(self, entries: list[BlackEntry]) -> None:
        """Les deux fichiers, chacun remplace d'un coup (jamais a moitie ecrit)."""
        self.folder.mkdir(parents=True, exist_ok=True)
        entries = ordered(entries)
        data = [{"adresse": entry.address, "ajout": entry.added.isoformat(timespec="seconds"),
                 "origine": entry.origin} for entry in entries]
        for name, content in ((BLACK_JSON, json.dumps(data, indent=1, ensure_ascii=False) + "\n"),
                              (BLACK_LIST, "".join(f"{entry.address}\n" for entry in entries))):
            temporary = self.path(f".{name}.tmp")
            temporary.write_text(content, encoding="utf-8")
            temporary.replace(self.path(name))

    def _reload_lists(self) -> bool:
        """Changement en nombre (import, purge) : HAProxy relit ses listes, les tables restent (pairs)."""
        if self.state() is None:
            return False
        with contextlib.suppress(OSError):
            self.admin.master("reload")
            return True
        return False

    def _full(self, count: int) -> Outcome | None:
        if count >= BLACKLIST_MAX:
            return Outcome(False, "Liste noire pleine ({max} entrées) : purgez ou exportez-la dans « Gestion de la "
                                  "liste noire » avant d'en ajouter.", {"max": BLACKLIST_MAX})
        return None

    def add_black(self, text: str, origin: str = ORIGIN_MANUAL) -> Outcome:
        """Ajout manuel (en prevision) d'une adresse ou d'un reseau."""
        try:
            address = normalize(_address(text))
        except ValueError:
            return Outcome(False, "Adresse ou réseau invalide : {text}", {"text": text})
        if in_tailnet(address):
            return Outcome(False, "{address} fait partie du tailnet : la porte admet toujours les machines Tailscale, "
                                  "elle ne peut pas être bloquée.", {"address": address})
        entries = self.black_entries()
        if covered(address, [entry.address for entry in entries]):
            return Outcome(False, "{address} est déjà dans la liste noire (ou dans un de ses réseaux).",
                           {"address": address})
        full = self._full(len(entries))
        if full is not None:
            return full
        if address in self.lists()[0]:
            self._list_change(TRUST_LIST, address, False)
        self._save_black([*entries, BlackEntry(address, self.now(), origin)])
        with contextlib.suppress(OSError):
            self.admin.command(f"add acl {self.path(BLACK_LIST)} {address}")
        return self._list_outcome("{address} → liste noire (refusée jusqu'au retrait).", {"address": address})

    def remove_black(self, addresses: list[str]) -> Outcome:
        wanted = set(addresses)
        entries = self.black_entries()
        kept = [entry for entry in entries if entry.address not in wanted]
        removed = len(entries) - len(kept)
        self._save_black(kept)
        if removed <= 20:
            for address in filter(is_canonical, wanted):  # jamais de texte libre vers le socket (F3)
                with contextlib.suppress(OSError):
                    self.admin.command(f"del acl {self.path(BLACK_LIST)} {address}")
        else:
            self._reload_lists()
        return self._list_outcome("{count} entrée(s) retirée(s) de la liste noire ; il en reste {left}.",
                                  {"count": removed, "left": len(kept)})

    def import_black(self, text: str) -> tuple[Outcome, ImportReport]:
        entries = self.black_entries()
        report = parse_import(text, [entry.address for entry in entries], now=self.now(),
                              room=max(0, BLACKLIST_MAX - len(entries)), in_tailnet=in_tailnet)
        if report.added:
            trusted = self.lists()[0]
            added = {entry.address for entry in report.added}
            if any(entry in added for entry in trusted):
                self.path(TRUST_LIST).write_text("".join(f"{entry}\n" for entry in trusted if entry not in added))
            self._save_black([*entries, *report.added])
            self._reload_lists()
        message = N_("Import : {added} ajoutée(s), {duplicates} doublon(s), {tailnet} du tailnet écartée(s), "
                     "{invalid} ligne(s) invalide(s).")
        params: dict[str, object] = {"added": len(report.added), "duplicates": report.duplicates,
                                     "tailnet": report.tailnet, "invalid": len(report.invalid)}
        if report.over_limit:  # deux phrases entieres : une phrase en morceaux ne se traduit pas (lot 9)
            message = N_("Import : {added} ajoutée(s), {duplicates} doublon(s), {tailnet} du tailnet écartée(s), "
                         "{invalid} ligne(s) invalide(s), {over} au-delà du plafond de {max}.")
            params.update(over=report.over_limit, max=BLACKLIST_MAX)
        return self._list_outcome(message, params), report

    def purge_preview(self, choice: PurgeChoice) -> list[BlackEntry]:
        return select_purge(self.black_entries(), choice, self.now())

    def purge_black(self, choice: PurgeChoice) -> Outcome:
        entries = self.black_entries()
        gone = {entry.address for entry in select_purge(entries, choice, self.now())}
        if not gone:
            return Outcome(False, "Aucune entrée ne correspond : rien n'a été retiré.", {})
        kept = [entry for entry in entries if entry.address not in gone]
        self._save_black(kept)
        self._reload_lists()
        return self._list_outcome("Purge : {count} entrée(s) retirée(s) de la liste noire ; il en reste {left}.",
                                  {"count": len(gone), "left": len(kept)})

    # ---- actions sur une adresse (ecran Attaques) : une ligne, l'action et la place finale ----
    def block(self, text: str, *, forever: bool = False) -> Outcome:
        """Liste noire : retire aussi de la confiance (sinon la confiance passerait avant et rien ne changerait)."""
        try:
            address = _address(text)
        except ValueError:
            return Outcome(False, "Adresse invalide : {text}", {"text": text})
        if in_tailnet(address):
            return Outcome(False, "{address} fait partie du tailnet : la porte admet toujours les machines Tailscale, "
                                  "elle ne peut pas être bloquée.", {"address": address})
        trusted = address in self.lists()[0]
        if forever or "/" in address:
            full = self._full(len(self.lists()[1])) if address not in self.lists()[1] else None
            if full is not None:
                return full
            if trusted:
                self._list_change(TRUST_LIST, address, False)
            self._list_change(BLACK_LIST, address, True)
            message = (N_("{address} → liste noire (refusée jusqu'au retrait), retirée de la confiance.") if trusted
                       else N_("{address} → liste noire (refusée jusqu'au retrait)."))
            return self._list_outcome(message, {"address": address})
        if place(address, *self.lists()) == TRUSTED:
            return Outcome(False, "{address} est en confiance (jamais limitée) : la confiance passe avant le "
                                  "blocage. Retirez-la de la confiance d'abord.", {"address": address})
        try:
            self.admin.command(f"set table {TABLE_IP} key {address} data.gpc0 1")
        except OSError as error:
            return Outcome(False, "Porte injoignable ({error}) : blocage temporaire impossible porte arrêtée.",
                           {"error": str(error)})
        minutes = self.policy().block_minutes
        return Outcome(True, "{address} → bloquée {minutes} min (blocage temporaire).",
                       {"address": address, "minutes": minutes})

    def unblock(self, text: str) -> Outcome:
        try:
            address = _address(text)
        except ValueError:
            return Outcome(False, "Adresse invalide : {text}", {"text": text})
        black = address in self.lists()[1]
        if black:
            self._list_change(BLACK_LIST, address, False)
        if "/" not in address:
            with contextlib.suppress(OSError):
                self.admin.command(f"set table {TABLE_IP} key {address} data.gpc0 0")
        if place(address, *self.lists()) == BLACK:
            message = N_("{address} → toujours refusée : elle fait partie d'un réseau en liste noire.")
        elif black:
            message = N_("{address} → admise (soumise aux règles), retirée de la liste noire.")
        else:
            message = N_("{address} → admise (soumise aux règles), blocage temporaire levé.")
        return self._list_outcome(message, {"address": address})

    def trust(self, text: str, *, add: bool = True) -> Outcome:
        try:
            address = _address(text)
        except ValueError:
            return Outcome(False, "Adresse invalide : {text}", {"text": text})
        black = address in self.lists()[1]
        if add and black:
            self._list_change(BLACK_LIST, address, False)
        self._list_change(TRUST_LIST, address, add)
        if add:
            message = (N_("{address} → confiance (jamais limitée), retirée de la liste noire.") if black
                       else N_("{address} → confiance (jamais limitée)."))
        elif in_tailnet(address):
            message = N_("{address} → toujours admise : elle fait partie du tailnet.")
        elif place(address, *self.lists()) == BLACK:
            message = N_("{address} → liste noire (refusée jusqu'au retrait).")
        else:
            message = N_("{address} → admise (soumise aux règles).")
        return self._list_outcome(message, {"address": address})


def certificate_needs_renewal(days: int | None) -> bool:
    return days is None or days < CERT_RENEW_DAYS

