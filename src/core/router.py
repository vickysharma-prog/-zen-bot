"""Command router for Zen-Bot.

Turns a spoken command into an action by matching it against the built-in skills
(system, calculator, units, weather, tasks, time/date). If nothing matches it
returns None, and the caller falls back to the Gemini AI for a free-form answer.

Keeping routing here - separate from voice and AI - makes the intent logic
unit-testable without a microphone or an API key.
"""

from __future__ import annotations

import re
from datetime import datetime

from src.modules.system import monitor
from src.modules.utilities import calculator, units, weather
from src.modules.productivity.tasks import TaskStore, handle as handle_task


def _format_time(now: datetime) -> str:
    period = "AM" if now.hour < 12 else "PM"
    hour = now.hour % 12 or 12
    return f"{hour}:{now.minute:02d} {period}"


class CommandRouter:
    """Dispatches a command string to a built-in skill, or None for the AI."""

    def __init__(self, task_store: TaskStore | None = None, enable_network: bool = True):
        self.tasks = task_store
        self.enable_network = enable_network

    def route(self, text: str) -> str | None:
        cmd = text.lower().strip()
        if not cmd:
            return None

        # Greetings / identity
        if re.search(r"\b(hello|hi|hey)\b", cmd):
            return "Hello! How can I help you?"
        if "your name" in cmd or "who are you" in cmd:
            return "I am Zen, your voice assistant."
        if cmd in ("help", "what can you do", "what can you do?"):
            return self.help_text()

        # Time / date (word-boundary so "6 times 7" is not read as "time")
        if re.search(r"\btime\b", cmd):
            return f"The time is {_format_time(datetime.now())}."
        if re.search(r"\bdate\b", cmd) or "day is it" in cmd:
            return f"Today is {datetime.now().strftime('%A, %B %d, %Y')}."

        # System
        if "cpu" in cmd or "processor" in cmd:
            return monitor.cpu_report()
        if "memory" in cmd or "ram" in cmd:
            return monitor.memory_report()
        if "battery" in cmd:
            return monitor.battery_report()
        if "disk" in cmd or "storage" in cmd:
            return monitor.disk_report()

        # Tasks (needs a store)
        if self.tasks is not None and "task" in cmd:
            handled = handle_task(text, self.tasks)
            if handled is not None:
                return handled

        # Unit conversion ("convert X unit to unit")
        if re.search(r"\bconvert\b", cmd) or re.search(r"\d+\s*[a-z]+\s+(to|in|into)\s+[a-z]+", cmd):
            return units.answer(text)

        # Calculator ("calculate ...", "what is 2 + 2")
        if "calculate" in cmd or re.search(r"\d\s*[-+*/x]\s*\d", cmd) or "what is" in cmd:
            expr = re.sub(r".*?(calculate|what is|what's)\s*", "", text, flags=re.IGNORECASE)
            if re.search(r"\d", expr):
                return calculator.answer(expr)

        # Weather ("weather in London", "what's the weather")
        if "weather" in cmd:
            if not self.enable_network:
                return "Weather lookups need network access."
            m = re.search(r"weather (?:in|at|for)\s+(.+)", cmd)
            location = m.group(1).strip(" ?.") if m else ""
            return weather.current(location)

        return None

    @staticmethod
    def help_text() -> str:
        return (
            "I can tell the time and date, report CPU, memory, battery and disk, "
            "do calculations and unit conversions, check the weather, manage your "
            "tasks, and answer general questions with AI."
        )
