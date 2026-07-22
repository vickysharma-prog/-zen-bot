"""AI Manager for Zen-Bot.

Wraps the AI provider with short-term context and persists every turn to a
SQLite-backed history store, so conversation memory survives restarts.
"""

from src.ai.gemini_adapter import GeminiAI
from src.core.history_store import HistoryStore
from src.core.logger import get_logger


class AIManager:
    """Manages AI interactions, context, and persistent memory."""

    def __init__(self, db_path: str = "data/db/zenbot.db"):
        self.logger = get_logger()
        self.ai = GeminiAI()

        # Persistent memory (SQLite). If it can't be opened, degrade to
        # in-memory only rather than failing to start.
        self.store = None
        try:
            self.store = HistoryStore(db_path)
            self.history = self.store.recent(limit=10)
        except Exception as e:
            self.logger.error(f"History store unavailable, using memory only: {e}")
            self.history = []

        self.logger.debug("AI Manager initialized")

    def get_response(self, user_input: str) -> str:
        """Get AI response with context, and persist the turn."""
        if self.history:
            response = self.ai.chat_with_context(user_input, self.history)
        else:
            response = self.ai.chat(user_input)

        self.history.append({"user": user_input, "assistant": response})
        if len(self.history) > 10:
            self.history = self.history[-10:]

        if self.store is not None:
            try:
                self.store.add(user_input, response)
            except Exception as e:
                self.logger.error(f"Failed to persist history: {e}")

        return response

    def clear_history(self):
        """Clear conversation history (memory and store)."""
        self.history = []
        if self.store is not None:
            try:
                self.store.clear()
            except Exception as e:
                self.logger.error(f"Failed to clear history store: {e}")
        self.logger.debug("History cleared")
