"""Persistent conversation memory for Zen-Bot, backed by SQLite.

The assistant keeps short-term context in memory for the AI prompt, but this
store persists every turn to SQLite so context survives restarts and can be
inspected later.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path


class HistoryStore:
    """A SQLite-backed conversation log."""

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
            CREATE TABLE IF NOT EXISTS history (
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                user      TEXT NOT NULL,
                assistant TEXT NOT NULL,
                created   TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        self.conn.commit()

    def add(self, user: str, assistant: str) -> None:
        self.conn.execute(
            "INSERT INTO history (user, assistant) VALUES (?, ?)", (user, assistant)
        )
        self.conn.commit()

    def recent(self, limit: int = 5) -> list[dict]:
        """Return the last ``limit`` turns in chronological order."""
        rows = self.conn.execute(
            "SELECT user, assistant FROM history ORDER BY id DESC LIMIT ?", (limit,)
        ).fetchall()
        return [{"user": r["user"], "assistant": r["assistant"]} for r in reversed(rows)]

    def clear(self) -> None:
        self.conn.execute("DELETE FROM history")
        self.conn.commit()

    def close(self) -> None:
        self.conn.close()
