"""Speech to Text for Zen-Bot."""

import speech_recognition as sr
from src.core.logger import get_logger
from src.core.exceptions import VoiceRecognitionError


class SpeechToText:
    """Converts voice to text."""
    
    def __init__(self):
        self.logger = get_logger()
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.logger.debug("Speech-to-Text initialized")
    
    def listen(self, timeout=5.0):
        """Listen and return text."""
        try:
            with self.microphone as source:
                self.logger.debug("Listening...")
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=10.0)
            
            text = self.recognizer.recognize_google(audio)
            self.logger.user(text)
            return text.strip()
            
        except sr.WaitTimeoutError:
            return None
        except sr.UnknownValueError:
            return None
        except Exception as e:
            self.logger.error(f"Listen error: {e}")
            return None