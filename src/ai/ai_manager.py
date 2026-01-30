"""AI Manager for Zen-Bot."""

from src.ai.gemini_adapter import GeminiAI
from src.core.logger import get_logger


class AIManager:
    """Manages AI interactions and context."""
    
    def __init__(self):
        self.logger = get_logger()
        self.ai = GeminiAI()
        self.history = []
        self.logger.debug("AI Manager initialized")
    
    def get_response(self, user_input: str) -> str:
        """Get AI response with context."""
        
        # Get response from AI
        if self.history:
            response = self.ai.chat_with_context(user_input, self.history)
        else:
            response = self.ai.chat(user_input)
        
        # Save to history
        self.history.append({
            "user": user_input,
            "assistant": response
        })
        
        # Keep history limited
        if len(self.history) > 10:
            self.history = self.history[-10:]
        
        return response
    
    def clear_history(self):
        """Clear conversation history."""
        self.history = []
        self.logger.debug("History cleared")