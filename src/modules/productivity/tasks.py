"""Task management for Zen-Bot, backed by SQLite.

Stores tasks (with a priority and done flag) in a local SQLite database so they
persist across sessions. All access goes through TaskStore; the assistant calls
the ``handle`` helper to turn spoken requests into actions.
"""

from __future__ import annotations

import re
import sqlite3
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Task:
    id: int
    text: str
    priority: str
    done: bool


class TaskStore:
    """A SQLite-backed to-do list."""

    def __init__(self, db_path: str = "data/db/zenbot.db"):
        self.db_path = db_path
        if db_path != ":memory:":
            Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self._init_schema()

    def _init_schema(self) -> None:
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id       INTEGER PRIMARY KEY AUTOINCREMENT,
                text     TEXT NOT NULL,
                priority TEXT NOT NULL DEFAULT 'normal',
                done     INTEGER NOT NULL DEFAULT 0,
                created  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        self.conn.commit()

    def add(self, text: str, priority: str = "normal") -> Task:
        cur = self.conn.execute(
            "INSERT INTO tasks (text, priority) VALUES (?, ?)", (text.strip(), priority)
        )
        self.conn.commit()
        return Task(id=cur.lastrowid, text=text.strip(), priority=priority, done=False)

    def list(self, include_done: bool = False) -> list[Task]:
        query = "SELECT * FROM tasks"
        if not include_done:
            query += " WHERE done = 0"
        query += " ORDER BY done, id"
        return [
            Task(id=r["id"], text=r["text"], priority=r["priority"], done=bool(r["done"]))
            for r in self.conn.execute(query)
        ]

    def complete(self, task_id: int) -> bool:
        cur = self.conn.execute("UPDATE tasks SET done = 1 WHERE id = ?", (task_id,))
        self.conn.commit()
        return cur.rowcount > 0

    def delete(self, task_id: int) -> bool:
        cur = self.conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        self.conn.commit()
        return cur.rowcount > 0

    def close(self) -> None:
        self.conn.close()


_ADD = re.compile(r"add (?:a )?task[:\s]+(.+)", re.IGNORECASE)
_COMPLETE = re.compile(r"(?:complete|done|finish)\s+task\s+(\d+)", re.IGNORECASE)


def handle(text: str, store: TaskStore) -> str | None:
    """Route a spoken task command to the store. Returns None if not a task
    command so the caller can try other skills."""
    low = text.lower()

    m = _ADD.search(text)
    if m:
        priority = "high" if "urgent" in low or "important" in low else "normal"
        task = store.add(m.group(1), priority)
        return f"Added task {task.id}: {task.text}."

    m = _COMPLETE.search(text)
    if m:
        ok = store.complete(int(m.group(1)))
        return "Marked it done." if ok else "I couldn't find that task."

    if ("list" in low or "show" in low or "what are" in low) and "task" in low:
        tasks = store.list()
        if not tasks:
            return "You have no pending tasks."
        lines = ", ".join(f"{t.id}: {t.text}" for t in tasks)
        return f"You have {len(tasks)} pending tasks. {lines}."

    return None
