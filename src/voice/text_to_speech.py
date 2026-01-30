"""Text to Speech for Zen-Bot."""

import pyttsx3
from src.core.logger import get_logger
from src.core.config import get_config


class TextToSpeech:
    """Converts text to speech."""
    
    def __init__(self):
        self.logger = get_logger()
        self.config = get_config()
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', self.config.voice.speech_rate)
        self.engine.setProperty('volume', 1.0)
        self.logger.debug("Text-to-Speech initialized")
    
    def speak(self, text):
        """Speak the text."""
        if not text:
            return
        
        self.logger.speak(text)
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            self.logger.error(f"TTS error: {e}")
    
    def stop(self):
        """Stop speaking."""
        try:
            self.engine.stop()
        except:
            pass