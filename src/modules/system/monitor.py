"""System monitoring for Zen-Bot.

Reports CPU, memory, disk and battery using psutil, and returns short,
speech-friendly strings the assistant can read aloud.
"""

from __future__ import annotations

import shutil

try:
    import psutil
except ImportError:  # pragma: no cover - psutil is a declared dependency
    psutil = None


def _pct(value: float) -> str:
    return f"{value:.0f}%"


def cpu_report() -> str:
    """One-line CPU usage summary."""
    if psutil is None:
        return "System monitoring is unavailable (psutil not installed)."
    usage = psutil.cpu_percent(interval=0.3)
    cores = psutil.cpu_count(logical=True)
    return f"CPU usage is {_pct(usage)} across {cores} cores."


def memory_report() -> str:
    """One-line RAM usage summary."""
    if psutil is None:
        return "System monitoring is unavailable (psutil not installed)."
    vm = psutil.virtual_memory()
    used_gb = (vm.total - vm.available) / 1024**3
    total_gb = vm.total / 1024**3
    return f"Memory usage is {_pct(vm.percent)}, {used_gb:.1f} of {total_gb:.1f} gigabytes used."


def disk_report(path: str = "/") -> str:
    """One-line disk usage summary for a mount point."""
    total, used, free = shutil.disk_usage(path)
    pct = 100 * used / total if total else 0
    return f"Disk usage is {_pct(pct)}, {free / 1024**3:.0f} gigabytes free."


def battery_report() -> str:
    """One-line battery summary, or a note if there is no battery."""
    if psutil is None:
        return "System monitoring is unavailable (psutil not installed)."
    battery = getattr(psutil, "sensors_battery", lambda: None)()
    if battery is None:
        return "No battery detected (this looks like a desktop or server)."
    state = "charging" if battery.power_plugged else "on battery"
    return f"Battery is at {_pct(battery.percent)} and {state}."


def full_report() -> str:
    """Combined system summary."""
    return " ".join([cpu_report(), memory_report(), battery_report()])
