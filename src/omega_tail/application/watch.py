# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Veille automatique (domain/watch.py) : la boucle qui mesure, compte, coupe Funnel et le remet en route, et
l'installation de son service (systemd, OpenRC, runit) sous le compte de l'utilisateur.

La veille remet elle-meme Funnel en route a l'heure prevue (pas de minuterie sudo : elle tourne deja en
permanence) ; si elle s'arrete pendant une coupure, son service la relance et elle remet aussitot ce qui est du."""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field, replace
from datetime import datetime

from omega_tail.application.survival import Outcome, SurvivalTools
from omega_tail.domain.breaker import BreakerPolicy, Sample, assess
from omega_tail.domain.init import InitSystem
from omega_tail.domain.shield import ShieldFacts
from omega_tail.domain.watch import (
    CUT_PREFIX,
    HEARTBEAT_SECONDS,
    STRIKES,
    WATCH_NAMES,
    WatchState,
    WatchStatus,
    after_restore,
    can_strike,
    on_strike,
    openrc_script,
    runit_log_script,
    runit_run_script,
    status_of,
    unit_text,
)
from omega_tail.ports.watch import WatchStore

SYSTEMD_DIR = "/etc/systemd/system"
RETRY_LOG_SECONDS = 300.0


def _epoch(text: str) -> float | None:
    try:
        return datetime.fromisoformat(text).timestamp() if text else None
    except ValueError:
        return None


@dataclass
class Watcher:
    """Une veille en marche : garde les mesures recentes entre deux tours."""
    store: WatchStore
    survival: SurvivalTools
    measure: Callable[[], tuple[float | None, float | None]]
    """(CPU de tailscaled en % d'un coeur, temperature) ; None si illisible."""
    policy: Callable[[], BreakerPolicy]
    window: Callable[[], int]
    clock: Callable[[], float]
    shield: Callable[[], ShieldFacts | None] = lambda: None
    """Bouclier du port WireGuard (lot 8, decision C) : sa disparition est notee, jamais reposee ici."""
    samples: list[Sample] = field(default_factory=list)
    _last_beat: float = 0.0
    _last_error: float = 0.0
    _shield_missing: bool = False

    def tick(self) -> None:
        now = self.clock()
        self._check_shield()
        loaded = self.store.load()
        state = self._watch(self._restore_due(loaded, now), now)
        if now - self._last_beat >= HEARTBEAT_SECONDS or state != loaded:
            self._last_beat = now
            self.store.save(replace(state, heartbeat=now))

    def _check_shield(self) -> None:
        facts = self.shield()
        missing = facts is not None and facts.missing
        if missing and not self._shield_missing:
            self.store.log("bouclier du port WireGuard ABSENT : table effacée par un autre outil ; "
                           "« Survie » → « Reposer » (jamais reposé par la veille)")
        elif self._shield_missing and not missing and facts is not None and facts.present:
            self.store.log("bouclier du port WireGuard de nouveau en place")
        self._shield_missing = missing

    def _restore_due(self, state: WatchState, now: float) -> WatchState:
        cut = self.survival.store.current()
        if cut is None or not cut.until:
            return state
        until = _epoch(cut.until)
        if until is None or now < until:
            return state
        outcome = self.survival.restore(cut.cut_id)
        if not outcome.ok:
            if now - self._last_error >= RETRY_LOG_SECONDS:
                self._last_error = now
                self.store.log(f"remise en route {cut.cut_id} : ECHEC ({outcome.params}) ; nouvel essai")
            return state
        self.store.log(f"Funnel remis en route ({cut.cut_id}), à l'identique")
        self.samples.clear()
        return after_restore(state, now)

    def _watch(self, state: WatchState, now: float) -> WatchState:
        cpu, temperature = self.measure()
        self.samples.append(Sample(now, cpu, temperature))
        policy = self.policy()
        horizon = now - max(policy.seconds * 2, 120)
        self.samples[:] = [sample for sample in self.samples if sample.at >= horizon]
        if now < state.calm_until or self.survival.store.current() is not None:
            return state
        trigger = assess(tuple(self.samples), policy)
        if trigger is None or not can_strike(state, now, policy.seconds):
            return state
        self.samples.clear()  # une meme periode ne compte qu'une fois
        reason = trigger.reason.format(**trigger.params)
        before = state
        state, minutes = on_strike(state, now, self.window())
        if minutes is None:
            self.store.log(f"dépassement {len(state.strikes)}/{STRIKES} : {reason}")
            return state
        self.store.log(f"dépassement {STRIKES}/{STRIKES} : {reason}")
        outcome = self._cut(minutes)
        if outcome.ok:
            self.store.log(f"Funnel coupé {minutes} min (palier {state.level}) ; remise en route automatique")
            return state
        self.store.log(f"coupure impossible : {outcome.message.format(**outcome.params)}")
        return replace(before, strikes=())  # palier inchange : la prochaine coupure reessaiera le meme

    def _cut(self, minutes: int) -> Outcome:
        if not self.survival.open_ports():
            return Outcome(False, "Rien à couper : aucun port n'est ouvert à Internet.", {})
        cut_id = CUT_PREFIX + self.survival.new_cut_id()
        return self.survival.cut(minutes, cut_id=cut_id, watched=True)


@dataclass(frozen=True)
class WatchTools:
    store: WatchStore
    window: Callable[[], int]
    clock: Callable[[], float]
    python: str
    user: Callable[[], str]
    init: InitSystem = InitSystem.SYSTEMD
    as_root: bool = False
    runit_dir: str = "/var/service"

    def status(self) -> WatchStatus:
        return status_of(self.store.load(), self.clock(), self.window())

    def journal(self, count: int = 8) -> list[str]:
        return self.store.last_lines(count)

    def mark_installed(self, installed: bool) -> None:
        self.store.save(replace(self.store.load(), installed=installed))
        self.store.log("veille activée" if installed else "veille désactivée")

    def _sudo(self, *command: str) -> tuple[str, ...]:
        return command if self.as_root else ("sudo", *command)

    @property
    def name(self) -> str:
        return WATCH_NAMES[self.init]

    def start_commands(self) -> list[tuple[str, ...]]:
        """Ecrit les fichiers du service (sans droits) puis renvoie les commandes sudo qui l'installent."""
        user, folder = self.user(), self.store.folder
        if self.init is InitSystem.OPENRC:
            script = self.store.write_file("omega-tail-veille.openrc",
                                           openrc_script(user=user, python=self.python, folder=folder))
            return [self._sudo("install", "-m", "0755", script, f"/etc/init.d/{self.name}"),
                    self._sudo("rc-update", "add", self.name, "default"),
                    self._sudo("rc-service", self.name, "restart")]
        if self.init is InitSystem.RUNIT:
            run = self.store.write_file("sv-run", runit_run_script(user=user, python=self.python))
            log = self.store.write_file("sv-log-run", runit_log_script(user=user, folder=folder))
            service = f"/etc/sv/{self.name}"
            return [self._sudo("install", "-D", "-m", "0755", run, f"{service}/run"),
                    self._sudo("install", "-D", "-m", "0755", log, f"{service}/log/run"),
                    self._sudo("install", "-d", "-o", user, f"{folder}/log"),
                    self._sudo("ln", "-sfn", service, f"{self.runit_dir}/{self.name}")]
        unit = self.store.write_file(self.name, unit_text(user=user, python=self.python))
        return [self._sudo("install", "-m", "0644", unit, f"{SYSTEMD_DIR}/{self.name}"),
                self._sudo("systemctl", "daemon-reload"),
                self._sudo("systemctl", "enable", "--now", self.name),
                self._sudo("systemctl", "restart", self.name)]

    def stop_commands(self) -> list[tuple[str, ...]]:
        if self.init is InitSystem.OPENRC:
            return [self._sudo("rc-service", self.name, "stop"), self._sudo("rc-update", "del", self.name, "default")]
        if self.init is InitSystem.RUNIT:
            return [self._sudo("sv", "down", f"{self.runit_dir}/{self.name}"),
                    self._sudo("rm", "-f", f"{self.runit_dir}/{self.name}")]
        return [self._sudo("systemctl", "disable", "--now", self.name)]
