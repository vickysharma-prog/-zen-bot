"""Gemini AI Adapter for Zen-Bot."""

import google.generativeai as genai
from src.ai.base import BaseAI
from src.core.config import get_config
from src.core.logger import get_logger


class GeminiAI(BaseAI):
    """Google Gemini AI integration."""
    
    def __init__(self):
        self.logger = get_logger()
        self.config = get_config()
        
        # Configure Gemini
        api_key = self.config.gemini_api_key
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in .env")
        
        genai.configure(api_key=api_key)
        
        # Use correct model name
        self.model = genai.GenerativeModel('models/gemini-2.5-flash')
        self.conversation = []
        
        self.logger.debug("Gemini AI initialized")
    
    def chat(self, message: str) -> str:
        """Send message and get response."""
        try:
            response = self.model.generate_content(message)
            return response.text
        except Exception as e:
            self.logger.error(f"Gemini error: {e}")
            return "Sorry, I couldn't process that."
    
    def chat_with_context(self, message: str, history: list) -> str:
        """Chat with conversation history."""
        try:
            # Build context
            context = "You are Zen, a helpful AI voice assistant. Be concise and friendly.\n\n"
            
            for msg in history[-5:]:  # Last 5 messages
                context += f"User: {msg['user']}\nZen: {msg['assistant']}\n"
            
            context += f"User: {message}\nZen:"
            
            response = self.model.generate_content(context)
            return response.text
            
        except Exception as e:
            self.logger.error(f"Gemini error: {e}")
            return "Sorry, I couldn't process that."