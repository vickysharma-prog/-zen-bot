"""Text to Speech for Zen-Bot - Edge TTS (Male Voice, Fast)."""

import os
import asyncio
import tempfile
import edge_tts
import pygame
from src.core.logger import get_logger


class TextToSpeech:
    """Microsoft Edge TTS - Male Voice, Fast."""
    
    def __init__(self):
        self.logger = get_logger()
        pygame.mixer.init(frequency=24000)
        
        # Male voices
        self.voice_en = "en-IN-PrabhatNeural"
        self.voice_hi = "hi-IN-MadhurNeural"
        
        # Reuse event loop
        self.loop = asyncio.new_event_loop()
        
        self.logger.debug("Edge TTS initialized (Male Voice)")
    
    def speak(self, text, lang=None):
        """Speak text fast."""
        if not text:
            return
        
        self.logger.speak(text)
        
        try:
            if lang is None:
                lang = self._detect_language(text)
            
            voice = self.voice_hi if lang == 'hi' else self.voice_en
            
            self.loop.run_until_complete(self._speak_async(text, voice))
            
        except Exception as e:
            self.logger.error(f"TTS error: {e}")
    
    async def _speak_async(self, text, voice):
        """Fast async TTS."""
        temp_path = None
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as f:
                temp_path = f.name
            
            # Faster rate
            communicate = edge_tts.Communicate(text, voice, rate="+20%")
            await communicate.save(temp_path)
            
            pygame.mixer.music.load(temp_path)
            pygame.mixer.music.play()
            
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            
            pygame.mixer.music.unload()
            
        finally:
            if temp_path and os.path.exists(temp_path):
                os.remove(temp_path)
    
    def _detect_language(self, text):
        """Detect Hindi or English."""
        for char in text:
            if '\u0900' <= char <= '\u097F':
                return 'hi'
        return 'en'
    
    def stop(self):
        """Stop speaking."""
        try:
            pygame.mixer.music.stop()
        except:
            pass