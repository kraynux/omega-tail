# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Survie (lot 2) : confinement de tailscaled et disjoncteur Funnel.

Disjoncteur (decision, 2026-11-22) : il PROPOSE ; l'utilisateur choisit une coupure momentanee
programmee (10 min par defaut, puis remise en route automatique a l'identique) ou une coupure totale (remise en
route manuelle). La remise en route programmee est confiee a une minuterie systemd (`systemd-run`) : elle a lieu
meme si omega-tail est ferme ou la session SSH coupee. Elle tourne sous le compte de l'utilisateur, OPERATEUR de
Tailscale (jamais root sur le code de son dossier) ; une minuterie d'une coupure deja levee ne fait rien."""
from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any

from omega_tail.core.constants import TAILSCALED_UNIT
from omega_tail.domain.confinement import (
    DROP_IN_NAME,
    DROP_IN_PATH,
    ConfinementPlan,
    drop_in_text,
    ssh_drop_in_path,
    ssh_drop_in_text,
)
from omega_tail.domain.funnel import (
    Cut,
    cut_commands,
    funnel_allowed,
    public_ports,
    restore_commands,
    same_publication,
    tailnet_only_commands,
)
from omega_tail.domain.init import CGROUP_NAME, CGROUP_ROOT, InitSystem
from omega_tail.domain.service import ServiceState
from omega_tail.domain.startup import fixable, risky_hooks, soften
from omega_tail.ports.survival import CutStore, QuietCommand
from omega_tail.shared.i18n import N_

FUNNEL_STILL_ALLOWED = N_("Funnel encore autorisé sur les ports")
TIMER_PREFIX = "omega-tail-retablir-"
TerminalCommand = Callable[[Sequence[str]], int]


def _sudo(command: Sequence[str], as_root: bool) -> tuple[str, ...]:
    return tuple(command) if as_root else ("sudo", *command)


@dataclass(frozen=True)
class Outcome:
    ok: bool
    message: str
    """Phrase marquee pour la traduction, completee par `params`."""
    params: Mapping[str, object]


@dataclass(frozen=True)
class SurvivalTools:
    store: CutStore
    serve_config: Callable[[], dict[str, Any]]
    quiet: QuietCommand
    now: Callable[[], datetime]
    python: str
    """Interpreteur d'omega-tail, lance par la minuterie de remise en route."""
    user: Callable[[], str]
    as_root: bool = False
    init: InitSystem = InitSystem.SYSTEMD
    spawn: Callable[[Sequence[str]], int] | None = None
    """Hors systemd : lance la remise en route programmee en processus detache, sous le compte de l'utilisateur."""

    # ---- confinement ----
    def confine_commands(self, plan: ConfinementPlan, *, restart: bool, ssh_unit: str = "",
                         pid: int = 0) -> list[tuple[str, ...]]:
        if self.init is not InitSystem.SYSTEMD:
            return self._cgroup_commands(plan, pid)
        return self._systemd_confine(plan, restart=restart, ssh_unit=ssh_unit)

    def _cgroup_commands(self, plan: ConfinementPlan, pid: int) -> list[tuple[str, ...]]:
        """Hors systemd : groupe de controle cgroup v2 a nous (aucun fichier de l'utilisateur modifie). Perdu si
        tailscaled redemarre : omega-tail le signale et propose de le reappliquer. Le texte du shell ne contient que
        des nombres et des chemins fixes."""
        if pid <= 0:
            return []
        folder = f"{CGROUP_ROOT}/{CGROUP_NAME}"
        script = (f"mkdir -p {folder} && (grep -qw cpu {CGROUP_ROOT}/cgroup.subtree_control || "
                  f"echo +cpu > {CGROUP_ROOT}/cgroup.subtree_control) && "
                  f"echo '{plan.quota_percent * 1000} 100000' > {folder}/cpu.max && "
                  f"echo {plan.cpu_weight} > {folder}/cpu.weight && echo {int(pid)} > {folder}/cgroup.procs")
        return [_sudo(("sh", "-c", script), self.as_root),
                _sudo(("renice", "-n", str(plan.nice), "-p", str(int(pid))), self.as_root)]

    def _systemd_confine(self, plan: ConfinementPlan, *, restart: bool, ssh_unit: str) -> list[tuple[str, ...]]:
        source = self.store.write_private(DROP_IN_NAME, drop_in_text(plan))
        commands = [_sudo(("install", "-D", "-m", "0644", source, DROP_IN_PATH), self.as_root)]
        if ssh_unit:
            ssh_source = self.store.write_private(f"ssh-{DROP_IN_NAME}", ssh_drop_in_text())
            commands.append(_sudo(("install", "-D", "-m", "0644", ssh_source, ssh_drop_in_path(ssh_unit)),
                                  self.as_root))
        commands.append(_sudo(("systemctl", "daemon-reload"), self.as_root))
        if restart:
            commands.append(_sudo(("systemctl", "restart", TAILSCALED_UNIT), self.as_root))
        return commands

    def unconfine_commands(self, *, restart: bool, ssh_unit: str = "", pid: int = 0) -> list[tuple[str, ...]]:
        if self.init is not InitSystem.SYSTEMD:
            folder = f"{CGROUP_ROOT}/{CGROUP_NAME}"
            back = f"echo {int(pid)} > {CGROUP_ROOT}/cgroup.procs; " if pid > 0 else ""
            commands = [_sudo(("sh", "-c", f"{back}rmdir {folder} 2>/dev/null; true"), self.as_root)]
            if pid > 0:
                commands.append(_sudo(("renice", "-n", "0", "-p", str(int(pid))), self.as_root))
            return commands
        commands = [_sudo(("rm", "-f", DROP_IN_PATH), self.as_root)]
        if ssh_unit:
            commands.append(_sudo(("rm", "-f", ssh_drop_in_path(ssh_unit)), self.as_root))
        commands.append(_sudo(("systemctl", "daemon-reload"), self.as_root))
        if restart:
            commands.append(_sudo(("systemctl", "restart", TAILSCALED_UNIT), self.as_root))
        return commands

    # ---- demarrage de tailscaled (domain/startup.py) ----
    def startup_fix_commands(self, service: ServiceState, read: Callable[[str], str]) -> list[tuple[str, ...]]:
        """Ajoute « - » devant le `tailscale up` lance au demarrage, dans les fichiers de l'administrateur
        (/etc/systemd) ; l'original est garde dans var/survie. Vide si rien a corriger ou rien de corrigeable."""
        if not risky_hooks(service):
            return []
        stamp = self.now().strftime("%Y%m%d-%H%M%S")
        commands: list[tuple[str, ...]] = []
        for path in (service.fragment_path, *service.drop_ins):
            if not path or not fixable(path):
                continue
            text = read(path)
            fixed = soften(text)
            if not text or fixed == text:
                continue
            name = path.rsplit("/", 1)[-1]
            self.store.write_private(f"demarrage-{name}.avant-{stamp}", text)
            source = self.store.write_private(f"demarrage-{name}", fixed)
            commands.append(_sudo(("install", "-m", "0644", source, path), self.as_root))
        if commands:
            commands.append(_sudo(("systemctl", "daemon-reload"), self.as_root))
        return commands

    # ---- disjoncteur ----
    def open_ports(self) -> tuple[int, ...]:
        return tuple(port for _kind, port in public_ports(self.serve_config()))

    def detached_command(self, cut_id: str, minutes: int) -> tuple[str, ...]:
        """Hors systemd : processus detache sous le compte de l'utilisateur (sans sudo), qui attend puis remet."""
        return (self.python, "-m", "omega_tail", "disjoncteur", "retablir", "--id", cut_id,
                "--attendre", str(minutes * 60))

    def timer_command(self, cut_id: str, minutes: int) -> tuple[str, ...]:
        return _sudo(("systemd-run", f"--on-active={minutes}min", f"--unit={TIMER_PREFIX}{cut_id}", "--collect",
                      f"--uid={self.user()}", "--description=omega-tail : remise en route de Funnel",
                      self.python, "-m", "omega_tail", "disjoncteur", "retablir", "--id", cut_id), self.as_root)

    def new_cut_id(self) -> str:
        return self.now().strftime("%Y%m%d-%H%M%S")

    def cut(self, minutes: int | None, *, schedule: TerminalCommand | None = None,
            cut_id: str = "", watched: bool = False) -> Outcome:
        """Coupe les ports ouverts a Internet. Momentanee : la minuterie est posee AVANT la coupure (si sudo est
        refuse, rien n'est coupe). Si une coupure echoue, ce qui a ete coupe est remis aussitot.
        `watched` : la veille automatique remet elle-meme en route a l'heure (aucune minuterie a poser)."""
        if self.store.current() is not None:
            return Outcome(False, "Funnel est déjà coupé par omega-tail.", {})
        config = self.serve_config()
        commands = cut_commands(config)
        if not commands:
            return Outcome(False, "Rien à couper : aucun port n'est ouvert à Internet.", {})
        cut_id = cut_id or self.new_cut_id()
        saved = self.store.save_publication(cut_id, config)
        until = ""
        if minutes and watched:
            until = (self.now() + timedelta(minutes=minutes)).isoformat()
        elif minutes:
            if self.init is not InitSystem.SYSTEMD and self.spawn is not None:
                code = self.spawn(self.detached_command(cut_id, minutes))
            elif schedule is None:
                return Outcome(False, "Remise en route programmée impossible ici.", {})
            else:
                code = schedule(self.timer_command(cut_id, minutes))
            if code != 0:
                return Outcome(False, "Minuterie de remise en route refusée (code {code}) : rien n'a été coupé.",
                               {"code": code})
            until = (self.now() + timedelta(minutes=minutes)).isoformat()
        for command in commands:
            code, error = self.quiet(command)
            if code != 0:
                for again in restore_commands(config):
                    self.quiet(again)
                self.store.log(f"coupure {cut_id} : ECHEC {' '.join(command)} : {error} ; publication remise")
                return Outcome(False, "Coupure impossible ({error}) : la publication a été remise.",
                               {"error": error or code})
        problem = self._clear_leftover(config)
        if problem:
            for again in (*tailnet_only_commands(config)[:1], *self._rebuild(config)):
                self.quiet(again)
            self.store.log(f"coupure {cut_id} : ECHEC {problem} ; publication remise")
            return Outcome(False, "Coupure impossible ({error}) : la publication a été remise.", {"error": problem})
        ports = tuple(port for _kind, port in public_ports(config))
        self.store.start(Cut(cut_id, self.now().isoformat(), until, saved, ports))
        self.store.log(f"coupure {cut_id} : ports {', '.join(map(str, ports))} ; "
                       + (f"remise en route prevue {until}" if until else "coupure totale"))
        if until:
            return Outcome(True, "Funnel coupé ({ports}) pour {minutes} min, puis remis en route automatiquement.",
                           {"ports": ", ".join(map(str, ports)), "minutes": minutes})
        return Outcome(True, "Funnel coupé ({ports}) jusqu'à votre remise en route.",
                       {"ports": ", ".join(map(str, ports))})

    def _clear_leftover(self, config: dict[str, Any]) -> str:
        """Apres les « off » : si une autorisation Funnel reste (mode TCP), repartir de zero avec les seuls points
        du tailnet, puis verifier que plus rien n'est ouvert a Internet. Renvoie le probleme, vide si tout va bien."""
        if not funnel_allowed(self.serve_config()):
            return ""
        for command in tailnet_only_commands(config):
            code, error = self.quiet(command)
            if code != 0:
                return f"{' '.join(command)} : {error or code}"
        left = funnel_allowed(self.serve_config())
        return f"{FUNNEL_STILL_ALLOWED} : {', '.join(map(str, left))}" if left else ""

    @staticmethod
    def _rebuild(config: dict[str, Any]) -> tuple[tuple[str, ...], ...]:
        """Publication d'origine complete, apres un `serve reset` : tailnet d'abord, puis Funnel."""
        return (*tailnet_only_commands(config)[1:], *restore_commands(config))

    def restore(self, cut_id: str = "") -> Outcome:
        cut = self.store.current()
        if cut is None:
            return Outcome(True, "Rien à rétablir : Funnel n'est pas coupé par omega-tail.", {})
        if cut_id and cut.cut_id != cut_id:
            return Outcome(True, "Minuterie d'une ancienne coupure : rien à faire.", {})
        saved = self.store.load_publication(cut.saved)
        errors = []
        for command in restore_commands(saved):
            code, error = self.quiet(command)
            if code != 0:
                errors.append(error or str(code))
        if not same_publication(saved, self.serve_config()):
            self.store.log(f"remise en route {cut.cut_id} : INCOMPLETE {' ; '.join(errors)}")
            return Outcome(False, "Remise en route incomplète ({errors}) : sauvegarde gardée dans {path}.",
                           {"errors": " ; ".join(errors) or "?", "path": cut.saved})
        self.store.finish()
        self.store.log(f"remise en route {cut.cut_id} : identique a la sauvegarde")
        return Outcome(True, "Funnel remis en route, à l'identique.", {})
