# ZEN-BOT
#### Video Demo: https://youtu.be/RWXF9crJTk8

<div align="center">

# 🤖 ZEN-BOT

### AI-Powered Voice Assistant

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Gemini](https://img.shields.io/badge/Gemini-AI-8E75B2?style=for-the-badge&logo=google&logoColor=white)](https://deepmind.google/technologies/gemini/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

*A powerful voice-activated assistant that listens, thinks, and responds naturally.*

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Tech Stack](#-tech-stack) • [Contributing](#-contributing)

---

</div>

## 🎯 Overview

**Zen-Bot** is an intelligent voice assistant that combines speech recognition, natural language processing, and AI to create a seamless hands-free experience. Built with modularity and extensibility in mind.
<div align="center">
```
┌──────────────────────────────────────────────────────────┐
│  ░▒▓█ ZEN-BOT █▓▒░                                       │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━                      │
│                                                          │
│  > INITIALIZING SYSTEM...                                │
│  > LOADING VOICE MODULE... OK                            │
│  > CONNECTING AI CORE... OK                              │
│  > ALL SYSTEMS OPERATIONAL                               │
│                                                          │
│  [ AWAITING INPUT... ]                                   │
└──────────────────────────────────────────────────────────┘
```
</div>

## ✨ Features

### 🎤 Voice Interaction
- Real-time speech recognition
- Natural text-to-speech responses
- Multi-language support
- Wake word detection

### 🧠 AI Intelligence
- Powered by Google Gemini AI
- Context-aware conversations
- Memory of previous interactions
- Natural language understanding

### 🖥️ System Control
- Launch applications
- System monitoring (CPU, RAM, Battery)
- Screenshot capture
- Volume control
- File operations

### 📧 Productivity
- Email integration (Gmail)
- Calendar management
- Task management with priorities
- Notes and reminders

### ☁️ Utilities
- Weather forecasts
- Timers and alarms
- Calculator
- Web search
- Unit conversions

---

## 🚀 Installation

### Prerequisites

- Python 3.11 or higher
- Working microphone
- Internet connection (for AI features)

### Quick Start

```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/zen-bot.git
cd zen-bot

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt


Configuration
Create a .env file in the root directory:

env

GEMINI_API_KEY=your_api_key_here
DEFAULT_LANGUAGE=en
VOICE_ENABLED=true
💡 Get your free Gemini API key at Google AI Studio

🎮 Usage
Starting Zen-Bot
Bash

python project.py
Voice Commands
Command	Example
Greetings	"Hello", "Hey Zen"
Time/Date	"What time is it?", "What's today's date?"
Questions	"Who is Elon Musk?", "Explain quantum physics"
System	"Open Chrome", "What's my CPU usage?"
Tasks	"Add task: Buy groceries", "Show my tasks"
Exit	"Exit", "Goodbye", "Quit"
Example Conversation
text

You: "Hello Zen"
Zen: "Hello! How can I help you today?"

You: "What's the weather like?"
Zen: "Currently it's 28°C and sunny in your area..."

You: "Set a reminder for 5 PM"
Zen: "Reminder set for 5:00 PM. I'll notify you then."

You: "Goodbye"
Zen: "Goodbye! Have a great day!"
📂 Project Structure
text

zen-bot/
├── src/
│   ├── core/               # Configuration, logging, exceptions
│   │   ├── config.py
│   │   ├── logger.py
│   │   └── exceptions.py
│   ├── voice/              # Speech recognition & synthesis
│   │   ├── speech_to_text.py
│   │   └── text_to_speech.py
│   ├── ai/                 # AI integrations
│   │   ├── base.py
│   │   ├── gemini_adapter.py
│   │   └── ai_manager.py
│   ├── modules/            # Feature modules
│   │   ├── system/
│   │   ├── productivity/
│   │   └── utilities/
│   └── ui/                 # Terminal interface
├── data/                   # Runtime data
│   ├── db/
│   ├── logs/
│   └── notes/
├── tests/                  # Test suite
├── config/                 # Configuration files
├── project.py              # Entry point
├── requirements.txt
└── README.md
🛡️ Tech Stack
Category	Technology
Language	Python 3.11+
AI Engine	Google Gemini AI
Speech Recognition	SpeechRecognition, PyAudio
Text-to-Speech	pyttsx3
Terminal UI	Rich
Database	SQLite3
Testing	pytest
Configuration	python-dotenv, PyYAML
🧪 Testing
Bash

# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src
🤝 Contributing
Contributions are welcome! Please follow these steps:

Fork the repository
Create a feature branch (git checkout -b feature/amazing-feature)
Commit changes (git commit -m 'Add amazing feature')
Push to branch (git push origin feature/amazing-feature)
Open a Pull Request
📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

👨‍💻 Author
Vicky - GitHub

<div align="center">
⭐ Star this repository if you found it helpful!

Made with ❤️ and Python

</div> ```
