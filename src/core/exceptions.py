"""Custom exceptions for Zen-Bot."""


class ZenBotException(Exception):
    """Base exception."""
    pass


class ConfigurationError(ZenBotException):
    """Configuration invalid."""
    pass


class APIKeyMissingError(ConfigurationError):
    """API key missing."""
    def __init__(self, key_name: str):
        super().__init__(f"API key '{key_name}' missing. Add to .env file.")


class VoiceRecognitionError(ZenBotException):
    """Voice recognition failed."""
    pass


class SpeechSynthesisError(ZenBotException):
    """Text-to-speech failed."""
    pass


class AIProviderError(ZenBotException):
    """AI provider failed."""
    pass