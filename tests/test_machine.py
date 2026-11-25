# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
from __future__ import annotations

from pathlib import Path

from omega_tail.infrastructure.system.machine import ProcMachine, find_pid, max_temperature, process_ticks


def test_process_ticks_with_spaces_in_the_name() -> None:
    fields = " ".join(["S"] + ["0"] * 10 + ["120", "30"] + ["0"] * 30)
    assert process_ticks(f"638 (tail scaled) {fields}") == 150
    assert process_ticks("garbage") is None


def test_max_temperature_ignores_absurd_values(tmp_path: Path) -> None:
    hwmon = tmp_path / "class" / "hwmon" / "hwmon0"
    hwmon.mkdir(parents=True)
    (hwmon / "temp1_input").write_text("76000\n")
    (hwmon / "temp2_input").write_text("200000\n")
    zone = tmp_path / "class" / "thermal" / "thermal_zone0"
    zone.mkdir(parents=True)
    (zone / "temp").write_text("81000\n")
    assert max_temperature(tmp_path) == 81.0
    assert max_temperature(tmp_path / "nothing") is None


def test_cpu_percent_between_two_reads(tmp_path: Path, monkeypatch) -> None:  # type: ignore[no-untyped-def]
    proc = tmp_path / "proc"
    (proc / "77").mkdir(parents=True)
    (proc / "77" / "comm").write_text("tailscaled\n")
    (proc / "loadavg").write_text("1.00 0.50 0.25 1/100 7\n")
    (proc / "77" / "status").write_text("Name: tailscaled\nVmRSS:\t  1024 kB\n")

    def stat(ticks: int) -> None:
        (proc / "77" / "stat").write_text("77 (tailscaled) " + " ".join(["S"] + ["0"] * 10 + [str(ticks), "0"]
                                                                         + ["0"] * 30))

    clock = iter([100.0, 102.0])
    monkeypatch.setattr("omega_tail.infrastructure.system.machine.time.monotonic", lambda: next(clock))
    monkeypatch.setattr("omega_tail.infrastructure.system.machine.CLOCK_TICKS", 100)
    machine = ProcMachine(proc=proc, sys_root=tmp_path / "sys")
    assert find_pid(proc=proc) == 77
    stat(1000)
    first = machine.state(0)
    assert first.tailscaled_cpu_percent is None and first.tailscaled_rss_bytes == 1024 * 1024
    stat(1100)  # 100 ticks = 1 s de CPU en 2 s -> 50 % d'un coeur
    second = machine.state(77)
    assert second.tailscaled_cpu_percent == 50.0 and second.load == (1.0, 0.5, 0.25)
