"""Speech to Text for Zen-Bot - Hindi + English."""

import speech_recognition as sr
from src.core.logger import get_logger
from src.core.exceptions import VoiceRecognitionError


class SpeechToText:
    """Converts voice to text - Hindi + English."""
    
    def __init__(self):
        self.logger = get_logger()
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.logger.debug("Speech-to-Text initialized (Hindi + English)")
    
    def listen(self, timeout=5.0):
        """Listen and return text."""
        try:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                self.logger.debug("Listening...")
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=10.0)
            
            # Try English first
            text = self._recognize(audio, 'en-IN')
            
            # If failed, try Hindi
            if not text:
                text = self._recognize(audio, 'hi-IN')
            
            if text:
                self.logger.user(text)
            return text
            
        except sr.WaitTimeoutError:
            return None
        except Exception as e:
            self.logger.error(f"Listen error: {e}")
            return None
    
    def _recognize(self, audio, language):
        """Recognize audio in specific language."""
        try:
            text = self.recognizer.recognize_google(audio, language=language)
            return text.strip()
        except sr.UnknownValueError:
            return None
        except sr.RequestError as e:
            self.logger.error(f"Recognition error: {e}")
            return None