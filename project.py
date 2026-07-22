"""Zen-Bot: AI-Powered Voice Assistant."""

from datetime import datetime


class ZenBot:
    """Main assistant controller.

    The voice, AI and Rich imports are deferred to construction time so the
    pure command-processing functions in this module can be imported (and
    unit-tested) without the audio/AI stack installed.
    """

    def __init__(self):
        from rich.console import Console
        from src.core.logger import get_logger
        from src.core.router import CommandRouter
        from src.modules.productivity.tasks import TaskStore
        from src.voice.speech_to_text import SpeechToText
        from src.voice.text_to_speech import TextToSpeech
        from src.ai.ai_manager import AIManager

        self.console = Console()
        self.logger = get_logger()
        self.stt = SpeechToText()
        self.tts = TextToSpeech()
        self.ai = AIManager()
        self.tasks = TaskStore()
        self.router = CommandRouter(self.tasks)
        self.running = False
    
    def start(self):
        """Start the assistant."""
        self._show_welcome()
        self.running = True
        
        # Time-based greeting with Sir
        now = datetime.now()
        hour = now.hour
        time_str = format_time(now.hour, now.minute)

        if hour < 12:
            greeting = "Good morning"
        elif hour < 17:
            greeting = "Good afternoon"
        else:
            greeting = "Good evening"

        self.tts.speak(f"{greeting} Sir! The time is {time_str}. How may I assist you today?")
        
        while self.running:
            try:
                self.console.print("\n[green]🎤 Listening...[/green]")
                text = self.stt.listen(timeout=5.0)
                
                if text:
                    if is_exit_command(text):
                        self.running = False
                        continue
                    
                    response = self._get_response(text)
                    self.tts.speak(response)
                        
            except KeyboardInterrupt:
                self.running = False
        
        self.tts.speak("Goodbye Sir!")
        self.console.print("\n[bold green]Bye! 👋[/bold green]")
    
    def _get_response(self, command):
        """Route to a built-in skill first, then fall back to the AI."""
        try:
            handled = self.router.route(command)
            if handled is not None:
                return handled
        except Exception as e:  # a skill must never take the whole loop down
            self.logger.error(f"Router error: {e}")

        return self.ai.get_response(command)
    
    def _show_welcome(self):
        """Show welcome screen."""
        self.console.print("\n")
        self.console.print("[green]┌──────────────────────────────────────────────────────────┐[/green]")
        self.console.print("[green]│[/green]  [bold green]░▒▓█ ZEN-BOT █▓▒░[/bold green]                                       [green]│[/green]")
        self.console.print("[green]│[/green]  [dim green]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/dim green]                      [green]│[/green]")
        self.console.print("[green]│[/green]                                                          [green]│[/green]")
        self.console.print("[green]│[/green]  [green]> INITIALIZING SYSTEM...[/green]                                [green]│[/green]")
        self.console.print("[green]│[/green]  [green]> LOADING VOICE MODULE... [bold green]OK[/bold green][/green]                          [green]│[/green]")
        self.console.print("[green]│[/green]  [green]> CONNECTING AI CORE... [bold green]OK[/bold green][/green]                            [green]│[/green]")
        self.console.print("[green]│[/green]  [bold green]> ALL SYSTEMS OPERATIONAL[/bold green]                               [green]│[/green]")
        self.console.print("[green]│[/green]                                                          [green]│[/green]")
        self.console.print("[green]│[/green]  [bold white][ AWAITING INPUT... ][/bold white]                                   [green]│[/green]")
        self.console.print("[green]│[/green]                                                          [green]│[/green]")
        self.console.print("[green]│[/green]  [dim]// Say 'exit' to quit • Ctrl+C to stop[/dim]                [green]│[/green]")
        self.console.print("[green]└──────────────────────────────────────────────────────────┘[/green]")
        self.console.print("\n")


# CS50P Required Functions

def process_command(command):
    """Process a command and return response."""
    cmd = command.lower()
    
    if "hello" in cmd or "hi" in cmd:
        return "Hello! How can I help you?"
    
    elif "time" in cmd:
        now = datetime.now()
        return f"The time is {format_time(now.hour, now.minute)}"
    
    elif "date" in cmd:
        now = datetime.now()
        return f"Today is {now.strftime('%A, %B %d, %Y')}"
    
    elif "your name" in cmd:
        return "I am Zen, your AI assistant."
    
    elif is_exit_command(cmd):
        return "Goodbye!"
    
    else:
        return f"I heard: {command}"


def is_exit_command(command):
    """Check if exit command."""
    exits = ["exit", "quit", "bye", "goodbye", "stop"]
    return any(e in command.lower() for e in exits)


def format_time(hour, minute):
    """Format time in 12-hour format."""
    if not (0 <= hour <= 23):
        raise ValueError("Hour must be 0-23")
    if not (0 <= minute <= 59):
        raise ValueError("Minute must be 0-59")
    
    period = "AM" if hour < 12 else "PM"
    display_hour = hour % 12 or 12
    return f"{display_hour}:{minute:02d} {period}"


def main():
    """Main entry point."""
    bot = ZenBot()
    bot.start()


if __name__ == "__main__":
    main()