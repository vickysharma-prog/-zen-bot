"""Base AI Interface for Zen-Bot."""

from abc import ABC, abstractmethod


class BaseAI(ABC):
    """Abstract base class for AI providers."""
    
    @abstractmethod
    def chat(self, message: str) -> str:
        """Send message and get response."""
        pass
    
    @abstractmethod
    def chat_with_context(self, message: str, history: list) -> str:
        """Chat with conversation history."""
        pass