from src.modules.system import monitor


def test_reports_are_strings():
    # These call psutil; we assert they return non-empty, speech-friendly text.
    assert isinstance(monitor.cpu_report(), str) and "CPU" in monitor.cpu_report()
    assert "Memory" in monitor.memory_report()
    assert isinstance(monitor.disk_report(), str)


def test_battery_report_handles_absence():
    # On a machine with no battery this still returns a sentence, not an error.
    out = monitor.battery_report()
    assert isinstance(out, str) and len(out) > 0
