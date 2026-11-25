# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Racine de composition : cable les lectures reelles (tailscale, systemctl, /proc, journalctl) et les actions."""
from __future__ import annotations

import contextlib
import getpass
import os
import sys
import threading
import time
from collections.abc import Callable, Mapping
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from omega_tail import __version__
from omega_tail.application.actions import ActionTools
from omega_tail.application.connection import ConnectionTools
from omega_tail.application.gate import GateTools
from omega_tail.application.groups import GroupsTools
from omega_tail.application.network import NetworkTools
from omega_tail.application.publication import PublicationTools
from omega_tail.application.report import ReportTools
from omega_tail.application.settings import SettingsTools
from omega_tail.application.shield import ShieldTools
from omega_tail.application.snapshot import SnapshotTools
from omega_tail.application.survival import SurvivalTools
from omega_tail.application.watch import Watcher, WatchTools
from omega_tail.domain.alerts import Alert
from omega_tail.domain.confinement import SSH_UNITS
from omega_tail.domain.gate import BLACK_LIST
from omega_tail.domain.init import GATE_NAMES, TAILSCALED_NAMES, InitSystem
from omega_tail.domain.session import session_through_tailscale
from omega_tail.domain.snapshot import Snapshot
from omega_tail.infrastructure.commands import quiet_command, run_tool, spawn_detached
from omega_tail.infrastructure.exports.writer import FileExportWriter
from omega_tail.infrastructure.gate import GateSystem, HaproxyAdmin
from omega_tail.infrastructure.geo_base import DbIpSource, lua_scripts
from omega_tail.infrastructure.privileged.terminal import run_attached, running_as_root
from omega_tail.infrastructure.settings.directories import clear_directory
from omega_tail.infrastructure.settings.json_store import JsonSettingsStore
from omega_tail.infrastructure.shield import ShieldSystem
from omega_tail.infrastructure.survival_store import FileCutStore
from omega_tail.infrastructure.system.forwarding import read_forwarding
from omega_tail.infrastructure.system.init_detect import detect_init, runit_service_dir
from omega_tail.infrastructure.system.journal import FileJournal, Journalctl, journal_files
from omega_tail.infrastructure.system.machine import ProcMachine
from omega_tail.infrastructure.system.services import service_reader
from omega_tail.infrastructure.system.systemd import first_loaded
from omega_tail.infrastructure.tailscale.cli import TailscaleCli
from omega_tail.infrastructure.tailscale.probe import probe, probe_public
from omega_tail.infrastructure.watch_store import FileWatchStore
from omega_tail.interfaces.cli.main import main_with

HAPROXY_ENV = "OMEGA_TAIL_HAPROXY"
"""Chemin d'HAProxy impose (banc d'essai : binaire compile) ; par defaut, celui du gestionnaire de paquets."""
VAR_DIR_ENV = "OMEGA_TAIL_VAR_DIR"
"""Remplace `<omega-tail>/var` (tests : jamais le vrai var/)."""
DROP_IN_SIZE_LIMIT = 64_000


_INIT: list[InitSystem] = []


def init_system() -> InitSystem:
    """Systeme d'init de la machine (systemd, OpenRC, runit), detecte une fois."""
    if not _INIT:
        _INIT.append(detect_init())
    return _INIT[0]


def project_root() -> Path:
    return Path(__file__).resolve().parents[3]


def count_lines(path: Path) -> int:
    """Lignes non vides d'un fichier (liste noire de la porte) ; 0 s'il manque."""
    try:
        with open(path, "rb") as handle:
            return sum(1 for line in handle if line.strip())
    except OSError:
        return 0


def var_dir(environ: Mapping[str, str] | None = None) -> Path:
    env = os.environ if environ is None else environ
    return Path(env.get(VAR_DIR_ENV) or project_root() / "var")


def current_user(environ: Mapping[str, str] | None = None) -> str:
    env = os.environ if environ is None else environ
    if running_as_root():
        return env.get("SUDO_USER") or "root"
    try:
        return getpass.getuser()
    except (KeyError, OSError):
        return env.get("USER", "")


def build_snapshots(environ: Mapping[str, str] | None = None) -> SnapshotTools:
    env = os.environ if environ is None else environ
    store = FileCutStore(var_dir(env))
    init = init_system()
    return SnapshotTools(tailscale=TailscaleCli(), service=service_reader(init, TAILSCALED_NAMES[init], "tailscaled"),  # type: ignore[arg-type]
                         machine=ProcMachine(),
                         user=lambda: current_user(env),
                         through_tailscale=lambda: session_through_tailscale(env.get("SSH_CONNECTION", "")),
                         now=lambda: datetime.now(timezone.utc), cut=store.current,
                         gate_service=service_reader(init, (GATE_NAMES[init],), "haproxy").state,  # type: ignore[attr-defined]
                         watch=build_watch(env).status,
                         gate_attack=lambda: build_groups(var_dir(env) / "porte", env).attack()[0],
                         shield=build_shield(env).facts,
                         blacklist_count=lambda: count_lines(var_dir(env) / "porte" / BLACK_LIST))


def build_shield(environ: Mapping[str, str] | None = None) -> ShieldTools:
    """Bouclier du port WireGuard (lot 8) : lectures sans droits, commandes par le terminal sudo ou omega-fire."""
    env = os.environ if environ is None else environ
    return ShieldTools(machine=ShieldSystem(var_dir(env) / "bouclier-wg"), clock=time.time, init=init_system(),
                       runit_dir=runit_service_dir(), as_root=running_as_root())


def build_survival(environ: Mapping[str, str] | None = None) -> SurvivalTools:
    env = os.environ if environ is None else environ
    return SurvivalTools(store=FileCutStore(var_dir(env)), serve_config=TailscaleCli().serve_config,
                         quiet=quiet_command, now=lambda: datetime.now(timezone.utc).astimezone(),
                         python=sys.executable, user=lambda: current_user(env), as_root=running_as_root(),
                         init=init_system(), spawn=spawn_detached)


def build_watch(environ: Mapping[str, str] | None = None) -> WatchTools:
    from omega_tail.application.breaker_settings import load_window

    env = os.environ if environ is None else environ
    settings = JsonSettingsStore(var_dir(env) / "settings.json")
    return WatchTools(store=FileWatchStore(var_dir(env)), window=lambda: load_window(settings), clock=time.time,
                      python=sys.executable, user=lambda: current_user(env), init=init_system(),
                      as_root=running_as_root(), runit_dir=runit_service_dir())


def run_watch(environ: Mapping[str, str] | None = None) -> int:  # pragma: no cover - boucle sans fin
    """`omega-tail veille lancer` : la boucle du service (arret propre sur SIGTERM)."""
    import signal

    from omega_tail.application.breaker_settings import load_policy, load_window
    from omega_tail.domain.watch import TICK_SECONDS

    env = os.environ if environ is None else environ
    settings = JsonSettingsStore(var_dir(env) / "settings.json")
    machine, service = ProcMachine(), build_snapshots(env).service

    def measure() -> tuple[float | None, float | None]:
        state = machine.state(service.state().main_pid)
        return state.tailscaled_cpu_percent, state.temperature_c

    watcher = Watcher(store=FileWatchStore(var_dir(env)), survival=build_survival(env), measure=measure,
                      policy=lambda: load_policy(settings), window=lambda: load_window(settings), clock=time.time,
                      shield=build_shield(env).facts)
    stopping: list[bool] = []
    signal.signal(signal.SIGTERM, lambda *_args: stopping.append(True))
    watcher.store.log(f"veille en marche (pid {os.getpid()})")
    gate, chores_at = build_gate(env), 0.0
    chore: threading.Thread | None = None
    while not stopping:
        try:
            watcher.tick()
            if time.time() >= chores_at and (chore is None or not chore.is_alive()):
                chores_at = time.time() + 3600
                chore = threading.Thread(target=group_chores, args=(gate, watcher.store.log), daemon=True)
                chore.start()
        except Exception as error:  # noqa: BLE001 - la veille ne meurt jamais sur une lecture ratee
            watcher.store.log(f"erreur : {error!r}")
        time.sleep(TICK_SECONDS)
    watcher.store.log("veille arrêtée")
    return 0


def group_chores(gate: GateTools, log: Callable[[str], None]) -> None:
    """Toutes les heures, dans la veille (lot 6) : apprentissage des empreintes ; base AS / pays une fois par mois.
    Dans un fil a part : le telechargement et la construction de la base ne retardent jamais la surveillance."""
    groups = gate.groups
    if groups is None or gate.state() is None or not groups.lua():
        return
    try:
        if groups.learn(force=True):
            log("empreintes : référence mise à jour")
        if groups.base_due():
            outcome = groups.refresh_base()
            log("base AS / pays : " + outcome.message.format(**outcome.params))
    except Exception as error:  # noqa: BLE001 - jamais d'arret de la veille
        log(f"regroupements : erreur {error!r}")


def build_gate(environ: Mapping[str, str] | None = None) -> GateTools:
    env = os.environ if environ is None else environ
    var = var_dir(env)
    folder = var / "porte"
    folder.mkdir(parents=True, exist_ok=True)
    os.chmod(folder, 0o700)
    tailscale = TailscaleCli()
    return GateTools(folder=folder, settings=JsonSettingsStore(var / "settings.json"), admin=HaproxyAdmin(folder),
                     machine=GateSystem(env.get(HAPROXY_ENV, "")), store=FileCutStore(var),
                     serve_config=tailscale.serve_config, quiet=quiet_command,
                     dns_name=lambda: tailscale.state().dns_name, user=lambda: current_user(env),
                     python=sys.executable, now=lambda: datetime.now(timezone.utc).astimezone(),
                     as_root=running_as_root(), init=init_system(), runit_dir=runit_service_dir(),
                     groups=build_groups(folder, env), run_tool=run_tool)


def build_groups(folder: Path, environ: Mapping[str, str]) -> GroupsTools:
    system = GateSystem(environ.get(HAPROXY_ENV, ""))
    return GroupsTools(folder=folder, settings=JsonSettingsStore(var_dir(environ) / "settings.json"),
                       admin=HaproxyAdmin(folder), source=DbIpSource(),
                       now=lambda: datetime.now(timezone.utc).astimezone(), lua=system.has_lua, scripts=lua_scripts)


def build_connection() -> ConnectionTools:
    tailscale = TailscaleCli()
    return ConnectionTools(profiles=tailscale.profiles, exit_nodes=tailscale.exit_nodes, as_root=running_as_root(),
                           forwarding=read_forwarding)


def build_publication(gate: GateTools | None = None, environ: Mapping[str, str] | None = None) -> PublicationTools:
    env = os.environ if environ is None else environ
    store = FileCutStore(var_dir(env))

    def gate_port() -> int | None:
        state = gate.state() if gate is not None else None
        return state.gate_port if state is not None else None

    return PublicationTools(store=store, serve_config=TailscaleCli().serve_config, quiet=quiet_command,
                            now=lambda: datetime.now(timezone.utc).astimezone(), gate_port=gate_port,
                            cut_active=lambda: store.current() is not None, probe_public=probe_public,
                            probe_tailnet=probe)


def build_network() -> NetworkTools:
    return NetworkTools(TailscaleCli())


def build_report(*, snapshots: SnapshotTools | None = None, gate: GateTools | None = None,
                 watch: WatchTools | None = None, environ: Mapping[str, str] | None = None) -> ReportTools:
    from omega_tail.application.breaker_settings import load_policy

    settings = JsonSettingsStore(var_dir(environ) / "settings.json")
    return ReportTools(version=__version__, snapshots=snapshots or build_snapshots(environ), journal=build_journal(),
                       breaker=lambda: load_policy(settings), now=lambda: datetime.now(timezone.utc).astimezone(),
                       gate=gate, watch=watch, network=build_network())


def report_setup() -> tuple[ReportTools, FileExportWriter, str]:
    settings = build_settings()
    return (build_report(gate=build_gate(), watch=build_watch()), FileExportWriter(settings.exports_dir),
            settings.export_theme())


def build_settings(environ: Mapping[str, str] | None = None) -> SettingsTools:
    var, root = var_dir(environ), project_root()
    return SettingsTools(JsonSettingsStore(var / "settings.json"), var / "exports", var / "screenshots",
                         lambda directory: clear_directory(directory, root), root)


def read_small_file(path: str) -> str:
    """Fichier d'ajout de systemd (lecture seule, borne) ; illisible : une phrase vide."""
    try:
        with open(path, encoding="utf-8", errors="replace") as handle:
            return handle.read(DROP_IN_SIZE_LIMIT)
    except OSError:
        return ""


def install_language(settings: SettingsTools, terminal_family: object) -> None:
    from omega_lib.i18n.terminal_cell_widths import align_spacing_marks_with_terminal

    from omega_tail.shared.i18n import LANGUAGE

    LANGUAGE.install(settings_store=settings.store, environ=os.environ,
                     terminal_family=terminal_family)  # type: ignore[arg-type]
    align_spacing_marks_with_terminal()


def install_cli_language() -> None:
    """Ligne de commande dans la langue choisie (lot 9). La veille (service) garde le francais de son journal."""
    from omega_lib.infrastructure.terminal.detector import SystemTerminalDetector

    with contextlib.suppress(OSError, ValueError):  # la langue n'empeche jamais une commande : francais
        install_language(build_settings(), SystemTerminalDetector().detect().family)


def run_with_text_direction(app: Any) -> None:
    from omega_lib.i18n.policies import text_direction
    from omega_lib.i18n.terminal_bidi import ENTER_EXPLICIT_MODE, LEAVE_EXPLICIT_MODE, install_visual_reordering

    from omega_tail.shared.i18n import STATE

    if text_direction(STATE.language.code) != "rtl" or not install_visual_reordering():
        app.run()
        return
    sys.stdout.write(ENTER_EXPLICIT_MODE)
    sys.stdout.flush()
    try:
        app.run()
    finally:
        sys.stdout.write(LEAVE_EXPLICIT_MODE)
        sys.stdout.flush()


def restart_for_language(code: str) -> None:  # pragma: no cover - remplace le processus
    from omega_tail.shared.i18n import LANGUAGE

    LANGUAGE.prepare_restart_environment(os.environ, code)
    os.execv(sys.executable, [sys.executable, "-m", "omega_tail", *sys.argv[1:]])


def build_journal() -> Journalctl | FileJournal:
    init = init_system()
    if init is InitSystem.SYSTEMD:
        return Journalctl({"tailscaled": TAILSCALED_NAMES[init][0], "porte": GATE_NAMES[init]})
    return FileJournal(journal_files(str(var_dir() / "porte")))


def dashboard() -> int:
    if not sys.stdin.isatty() or not sys.stdout.isatty():
        from omega_tail.shared.i18n import _

        print(_("omega-tail : pas de terminal interactif ; utilisez « omega-tail etat »."), file=sys.stderr)
        return 2
    from omega_lib.infrastructure.declaration import build_contact_support
    from omega_lib.infrastructure.terminal.detector import SystemTerminalDetector
    from omega_lib.terminal.service import resolve_render_profile

    settings = build_settings()
    detected = SystemTerminalDetector().detect()
    install_language(settings, detected.family)
    from omega_lib.infrastructure.desktop.browser_opener import open_path_in_browser

    from omega_tail.interfaces.tui.app import OmegaTailApp

    def open_folder(path: Path) -> bool:
        return open_path_in_browser(path).ok

    gate, watch, snapshots = build_gate(), build_watch(), build_snapshots()
    app = OmegaTailApp(snapshots=snapshots, actions=ActionTools(run=run_attached, as_root=running_as_root()),
                       journal=build_journal(), version=__version__,
                       render_profile=resolve_render_profile(detected).render_profile, settings=settings,
                       contact=build_contact_support("omega-tail", __version__, var_dir()),
                       writer=FileExportWriter(settings.exports_dir), read_file=read_small_file,
                       survival=build_survival(),
                       ssh_unit=first_loaded(SSH_UNITS) if init_system() is InitSystem.SYSTEMD else "",
                       gate=gate, connection=build_connection(), publication=build_publication(gate),
                       watch=watch, network=build_network(), shield=build_shield(),
                       report=build_report(snapshots=snapshots, gate=gate, watch=watch), open_folder=open_folder)
    run_with_text_direction(app)
    if app.pending_language is not None:  # pragma: no cover - remplace le processus
        restart_for_language(app.pending_language)
    return 0


def state() -> tuple[Snapshot, tuple[Alert, ...]]:
    """Deux lectures a une seconde d'intervalle : la seconde donne le % CPU de tailscaled."""
    tools = build_snapshots()
    tools.collect()
    time.sleep(1)
    snapshot = tools.collect()
    return snapshot, tools.alerts(snapshot)


def main(argv: list[str] | None = None) -> int:
    arguments = sys.argv[1:] if argv is None else argv
    if arguments[:1] == ["synchro"]:
        # Jeton d'installation lu par omega-connect (2026-11-25) : sans interface, sans demarrage de l'etat.
        from omega_tail.app.synchro_runner import run_synchro
        return run_synchro(list(arguments[1:]))
    if arguments and arguments[:2] != ["veille", "lancer"]:
        install_cli_language()
    return main_with(argv, version=__version__, state=state, dashboard=dashboard, survival=build_survival,
                     terminal=run_attached, gate=build_gate, watch_run=run_watch, watch=build_watch,
                     report=report_setup)
