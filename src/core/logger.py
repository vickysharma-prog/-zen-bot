"""Logging system for Zen-Bot."""

import logging
from pathlib import Path
from rich.console import Console
from rich.logging import RichHandler


class ZenLogger:
    """Logger with rich console output."""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if hasattr(self, 'logger'):
            return
            
        self.console = Console()
        self.logger = self._setup_logger()
    
    def _setup_logger(self):
        logger = logging.getLogger("zen-bot")
        logger.setLevel(logging.DEBUG)
        
        if logger.handlers:
            return logger
        
        # Console handler
        console_handler = RichHandler(console=self.console, show_time=True, show_path=False)
        console_handler.setLevel(logging.INFO)
        logger.addHandler(console_handler)
        
        # File handler
        log_dir = Path("data/logs")
        log_dir.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.FileHandler(log_dir / "zen-bot.log", encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_format = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
        file_handler.setFormatter(file_format)
        logger.addHandler(file_handler)
        
        return logger
    
    def debug(self, msg): self.logger.debug(msg)
    def info(self, msg): self.logger.info(msg)
    def warning(self, msg): self.logger.warning(msg)
    def error(self, msg): self.logger.error(msg)
    
    def success(self, msg):
        self.console.print(f"[bold green]✓[/bold green] {msg}")
        self.logger.info(f"SUCCESS: {msg}")
    
    def speak(self, msg):
        self.console.print(f"[bold blue]🔊 Zen:[/bold blue] {msg}")
        self.logger.info(f"SPEAK: {msg}")
    
    def user(self, msg):
        self.console.print(f"[bold yellow]🎤 You:[/bold yellow] {msg}")
        self.logger.info(f"USER: {msg}")


def get_logger():
    """Get logger instance."""
    return ZenLogger()