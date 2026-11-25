# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Publication (lot 5, proposition §3.4) : ajouter, retirer, restaurer ce que Serve et Funnel publient, et essayer
de bout en bout.

Chaque changement : sauvegarde de l'etat d'avant (var/funnel/sauvegardes/), commande ciblee, puis verification de
la publication obtenue. Si elle n'est pas celle voulue (constat du 2026-11-22 : une autorisation Funnel peut rester
derriere un « --tcp=PORT off »), reconstruction complete ; si elle echoue encore, la publication d'avant est remise.
Les commandes passent sans terminal : il faut etre operateur de Tailscale (comme pour la porte et le disjoncteur)."""
from __future__ import annotations

from collections.abc import Callable, Iterable, Mapping
from dataclasses import dataclass
from datetime import datetime
from typing import Any

from omega_tail.application.survival import Outcome
from omega_tail.domain.funnel import Handler, handlers_of
from omega_tail.domain.publication import (
    AddRequest,
    Backup,
    PublicationError,
    add_command,
    backup_from,
    conflict,
    handler_for,
    is_gate_handler,
    rebuild_commands,
    remove_command,
)
from omega_tail.domain.tailscale import Probe
from omega_tail.ports.publication import PublicationStore
from omega_tail.ports.survival import QuietCommand
from omega_tail.shared.i18n import N_

PublicProbe = Callable[[str, int, str, str], Probe]
"""(nom, port, mode, chemin) -> essai par le chemin public (relais Funnel)."""
TailnetProbe = Callable[[str, int, str, str, str], Probe]
"""(nom, port, adresse, mode, chemin) -> essai par le tailnet."""


def probe_mode(handler: Handler) -> str:
    if handler.kind in ("https", "http"):
        return handler.kind
    if handler.kind == "tls-terminated-tcp":
        return "tls"
    if handler.proxy_protocol == 2 and handler.target.startswith("tcp://127.0.0.1:"):
        return "https"  # la porte du pare-feu fait le TLS puis relaie au site
    return "tcp"


@dataclass(frozen=True)
class PublicationTools:
    store: PublicationStore
    serve_config: Callable[[], dict[str, Any]]
    quiet: QuietCommand
    now: Callable[[], datetime]
    gate_port: Callable[[], int | None] = lambda: None
    """Port local de la porte quand la protection est active (sinon None)."""
    cut_active: Callable[[], bool] = lambda: False
    """Une coupure du disjoncteur est en cours."""
    probe_public: PublicProbe | None = None
    probe_tailnet: TailnetProbe | None = None

    # ---- lecture ----
    def handlers(self) -> tuple[Handler, ...]:
        return handlers_of(self.serve_config())

    def backups(self) -> list[Backup]:
        found = []
        for path in reversed(self.store.saves()):
            try:
                handlers = handlers_of(self.store.load_publication(path))
            except (OSError, ValueError):
                handlers = ()
            backup = backup_from(path, handlers)
            if backup is not None:
                found.append(backup)
        return found

    # ---- changements ----
    def _refused(self) -> Outcome | None:
        if self.cut_active():
            return Outcome(False, "Funnel est coupé par le disjoncteur : rétablissez-le d'abord (Survie).", {})
        return None

    def _save(self, config: Mapping[str, Any]) -> str:
        return self.store.save_publication("publication-" + self.now().strftime("%Y%m%d-%H%M%S"), config)

    def _current(self) -> frozenset[Handler]:
        return frozenset(handlers_of(self.serve_config()))

    def _run(self, commands: Iterable[tuple[str, ...]]) -> str:
        for command in commands:
            code, reason = self.quiet(command)
            if code != 0:
                return reason or f"code {code}"
        return ""

    def _apply(self, config: Mapping[str, Any], desired: frozenset[Handler], commands: Iterable[tuple[str, ...]],
               done: str, params: Mapping[str, object]) -> Outcome:
        before = frozenset(handlers_of(config))
        saved = self._save(config)
        error = self._run(commands)
        now = self._current()
        if now == desired:
            self.store.log(f"publication : {done.format(**params)}")
            return Outcome(True, done, params)
        if error and now == before:
            return Outcome(False, "Refusé par Tailscale ({error}) : rien n'a changé.", {"error": error})
        rebuild_error = self._run(rebuild_commands(desired))
        if self._current() == desired:
            self.store.log(f"publication : {done.format(**params)} (reconstruite)")
            return Outcome(True, done, params)
        self._run(rebuild_commands(before))
        if self._current() == before:
            return Outcome(False, "Changement impossible ({error}) : publication d'avant remise.",
                           {"error": error or rebuild_error or "?"})
        return Outcome(False, "Publication incomplète ({error}) : restaurez la sauvegarde {path}.",
                       {"error": error or rebuild_error or "?", "path": saved})

    def add(self, request: AddRequest) -> Outcome:
        refused = self._refused()
        if refused is not None:
            return refused
        try:
            handler = handler_for(request)
        except PublicationError as error:
            return Outcome(False, "Ajout refusé : {reason}.", {"reason": str(error)})
        config = self.serve_config()
        current = handlers_of(config)
        reason = conflict(handler, current)
        if reason:
            return Outcome(False, "Ajout refusé : {reason}.", {"reason": reason})
        return self._apply(config, frozenset((*current, handler)), [add_command(handler)],
                           "Publié : {kind} {port}{path} → {target} ({who}).",
                           {"kind": handler.kind, "port": handler.port,
                            "path": handler.path if handler.path not in ("", "/") else "",
                            "target": handler.target, "who": "Internet" if handler.public else "tailnet"})

    def remove(self, handler: Handler) -> Outcome:
        refused = self._refused()
        if refused is not None:
            return refused
        gate = self.gate_port()
        if gate is not None and is_gate_handler(handler, gate):
            return Outcome(False, "Ce port passe par la porte : « Désactiver la protection » (Pare-feu Funnel) "
                                  "d'abord.", {})
        config = self.serve_config()
        current = handlers_of(config)
        if handler not in current:
            return Outcome(False, "Ce point n'est plus publié.", {})
        desired = frozenset(item for item in current if item != handler)
        return self._apply(config, desired, [remove_command(handler, current)],
                           "Retiré : {kind} {port}{path}.",
                           {"kind": handler.kind, "port": handler.port,
                            "path": handler.path if handler.path not in ("", "/") else ""})

    def restore(self, path: str) -> Outcome:
        refused = self._refused()
        if refused is not None:
            return refused
        gate = self.gate_port()
        try:
            wanted = frozenset(handlers_of(self.store.load_publication(path)))
        except (OSError, ValueError) as error:
            return Outcome(False, "Sauvegarde illisible ({error}).", {"error": str(error)})
        if gate is not None:
            return Outcome(False, "La protection est active : « Désactiver la protection » (Pare-feu Funnel) "
                                  "d'abord, puis restaurez.", {})
        if any(item.proxy_protocol == 2 and item.target.startswith("tcp://127.0.0.1:") for item in wanted):
            return Outcome(False, "Cette sauvegarde passe par la porte, arrêtée : « Activer la protection » "
                                  "(Pare-feu Funnel) la recrée proprement.", {})
        config = self.serve_config()
        return self._apply(config, wanted, rebuild_commands(wanted), "Sauvegarde du {when} restaurée.",
                           {"when": next((item.when for item in self.backups() if item.path == path), path)})

    # ---- essai de bout en bout ----
    def test(self, handler: Handler, host: str, tailnet_address: str) -> Probe:
        mode, path = probe_mode(handler), handler.path or "/"
        if handler.public:
            if self.probe_public is None:
                return Probe(False, N_("essai public indisponible"))
            return self.probe_public(host, handler.port, mode, path)
        if self.probe_tailnet is None or not tailnet_address:
            return Probe(False, N_("adresse du tailnet inconnue"))
        return self.probe_tailnet(host, handler.port, tailnet_address, mode, path)
