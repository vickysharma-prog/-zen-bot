"""Configuration manager for Zen-Bot."""

import os
from dataclasses import dataclass
from pathlib import Path
from dotenv import load_dotenv
from src.core.logger import get_logger


@dataclass
class VoiceConfig:
    enabled: bool = True
    wake_word: str = "zen"
    language: str = "en"
    speech_rate: int = 175


@dataclass
class AIConfig:
    provider: str = "gemini"
    temperature: float = 0.7
    max_tokens: int = 1024


@dataclass
class Config:
    voice: VoiceConfig
    ai: AIConfig
    gemini_api_key: str = ""
    openai_api_key: str = ""


class ConfigManager:
    _instance = None
    _config = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if ConfigManager._config is not None:
            return
        
        self.logger = get_logger()
        load_dotenv()
        
        ConfigManager._config = Config(
            voice=VoiceConfig(),
            ai=AIConfig(),
            gemini_api_key=os.getenv("GEMINI_API_KEY", ""),
            openai_api_key=os.getenv("OPENAI_API_KEY", "")
        )
        
        self.logger.debug("Config loaded")
    
    @property
    def config(self):
        return ConfigManager._config


def get_config():
    """Get config instance."""
    return ConfigManager().config