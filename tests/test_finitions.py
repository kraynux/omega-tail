# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Finitions 0.7.0 (retours d'utilisation, 2026-11-24) : CPU de la machine distinct de tailscaled, tableau de bord
complet et colore, alerte de liste noire, base AS / pays mise a jour dans un processus a part."""
from __future__ import annotations

from dataclasses import replace
from pathlib import Path

from conftest import snapshot
from funnel_sim import FunnelSim
from test_gate import PRODUCTION, FakeAdmin, gate

from omega_tail.domain.alerts import Target, alerts_for
from omega_tail.domain.machine import MachineState
from omega_tail.infrastructure.system.machine import ProcMachine, cpu_times
from omega_tail.interfaces.tui.screens.dashboard import machine_lines, styled, tailscale_lines
from omega_tail.interfaces.tui.widgets.status_band import band_parts


def test_machine_cpu_from_proc_stat(tmp_path: Path) -> None:
    assert cpu_times("cpu  100 0 100 700 100 0 0 0 0 0\ncpu0 1 2 3 4\n") == (1000, 800)
    assert cpu_times("rien\n") is None
    proc = tmp_path / "proc"
    proc.mkdir()
    (proc / "loadavg").write_text("0.5 0.4 0.3 1/100 42\n")
    (proc / "stat").write_text("cpu  100 0 100 700 100 0 0 0 0 0\n")
    reader = ProcMachine(proc=proc, sys_root=tmp_path)
    assert reader.state(0).cpu_percent is None  # premiere lecture : pas encore d'ecart
    (proc / "stat").write_text("cpu  250 0 250 800 100 0 0 0 0 0\n")  # 300 occupes sur 400
    assert reader.state(0).cpu_percent == 75.0


def test_band_separates_machine_and_tailscaled_cpu() -> None:
    base = snapshot()
    shot = replace(base, machine=replace(base.machine, cpu_percent=92.0, tailscaled_cpu_percent=4.0))
    labels = [label for label, _color in band_parts(shot)]
    assert "CPU machine 92 %" in labels and "CPU tailscaled 4 %" in labels
    colors = dict(band_parts(shot))
    assert colors["CPU machine 92 %"] == "$error" and colors["CPU tailscaled 4 %"] == "$success"


def test_dashboard_lines_are_complete_and_leveled() -> None:
    base = snapshot()
    machine = MachineState(hostname="serveur-web", cpu_count=4, load=(9.0, 1.0, 1.0), cpu_percent=12.0,
                           temperature_c=80.0, memory_total_bytes=1000, memory_available_bytes=900)
    shot = replace(base, machine=machine, blacklist_count=30_000)
    lines = {label: (value, level) for label, value, level in machine_lines(shot)}
    assert lines["CPU machine"] == ("12 %", "ok") and lines["Charge"][1] == "bad"  # 9 / 4 coeurs >= 2
    assert lines["Température"][1] == "warn" and lines["Liste noire"] == ("30000 entrée(s)", "warn")
    assert {"Funnel", "Pare-feu (porte)"} <= set(lines)
    tailscale = {label for label, _value, _level in tailscale_lines(shot)}
    assert {"Nœud de sortie proposé", "Nœud de sortie utilisé", "Sous-réseaux annoncés"} <= tailscale
    text = styled(machine_lines(shot), {"accent": "#00D4FF", "success": "#00FF00", "text-muted": "auto 60%"})
    assert "CPU machine" in text.plain and any("#00D4FF" in str(span.style) for span in text.spans)


def test_large_blacklist_alert() -> None:
    base = snapshot()
    assert not [a for a in alerts_for(replace(base, blacklist_count=24_999), base.taken_at)
                if a.code == "blacklist-large"]
    found = [a for a in alerts_for(replace(base, blacklist_count=25_000), base.taken_at) if a.code == "blacklist-large"]
    assert found and found[0].target is Target.ATTACKS


def test_base_refresh_runs_apart(tmp_path: Path) -> None:
    calls: list[tuple[str, ...]] = []

    def runner(argv: object) -> tuple[int, str]:
        calls.append(tuple(argv))  # type: ignore[arg-type]
        return 0, "Base AS / pays à jour (10 plages pays, 20 plages AS)."

    tools = gate(tmp_path, FunnelSim(PRODUCTION), admin=FakeAdmin())
    assert not tools.refresh_base().ok  # sans regroupements
    from test_groups import groups_tools
    tools.groups = groups_tools(tmp_path / "var", FakeAdmin(), [snapshot().taken_at])  # type: ignore[arg-type]
    tools.run_tool = runner
    outcome = tools.refresh_base()
    assert outcome.ok and outcome.params["text"].startswith("Base AS / pays à jour")
    assert calls == [("/x/python", "-m", "omega_tail", "porte", "base")]
    tools.run_tool = lambda _argv: (124, "")
    assert "trop longue" in tools.refresh_base().message
