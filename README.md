<div align="center">

# 🤖 ZEN-BOT

### AI-Powered Voice Assistant

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Gemini](https://img.shields.io/badge/Gemini-AI-8E75B2?style=for-the-badge&logo=google&logoColor=white)](https://deepmind.google/technologies/gemini/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

*A voice-activated assistant that listens, thinks, and responds — in English and Hindi.*

**Video Demo:** https://youtu.be/RWXF9crJTk8

</div>

---

## 🎯 Overview

**Zen-Bot** is a hands-free voice assistant built around a clean, modular
architecture: a **voice layer** (speech-to-text + text-to-speech), a **command
router** that answers common requests locally, and a **Gemini AI** fallback for
open-ended questions. Conversation memory is persisted to **SQLite**, so context
survives restarts.

It is a CS50P final project, written to be readable and extensible.

```
┌──────────────────────────────────────────────────────────┐
│  ░▒▓█ ZEN-BOT █▓▒░                                        │
│  > LOADING VOICE MODULE... OK                             │
│  > CONNECTING AI CORE... OK                               │
│  > ALL SYSTEMS OPERATIONAL                                │
│  [ AWAITING INPUT... ]                                    │
└──────────────────────────────────────────────────────────┘
```

## ✨ Features

### 🎤 Voice
- Speech recognition in **English and Hindi** (auto-fallback between `en-IN` / `hi-IN`)
- Natural **text-to-speech** via Microsoft Edge neural voices (male, English + Hindi)

### 🧠 AI
- Powered by **Google Gemini**, wrapped behind an adapter interface (`BaseAI`)
  so another provider can be dropped in
- **Context-aware** replies using recent conversation history
- History **persisted to SQLite** — memory survives restarts

### ⚡ Built-in skills (answered locally, no AI round-trip)
- **System**: CPU, memory, battery and disk usage (`psutil`)
- **Calculator**: safe arithmetic, spoken or symbolic ("12 times 5 plus 3")
- **Unit conversions**: temperature, length, weight ("convert 10 km to miles")
- **Weather**: current conditions via the key-less wttr.in API
- **Tasks**: add / list / complete a to-do list stored in **SQLite**
- **Time & date**

Anything not matched by a skill falls through to the Gemini AI.

### 🖥️ Interface
- Rich terminal UI

## 🏗️ Architecture

```
Voice in ─► CommandRouter ─► built-in skill?  ── yes ─► spoken answer
                               │
                               └─ no ─► Gemini AI ─► spoken answer
                                          │
                                          └─ turn saved to SQLite history
```

The router keeps intent logic separate from voice and AI, so it is
**unit-testable without a microphone or an API key**.

## 🚀 Installation

```bash
# Clone
git clone https://github.com/vickysharma-prog/-zen-bot.git
cd -zen-bot

# Virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# Dependencies
pip install -r requirements.txt
```

### Configuration

```bash
cp .env.example .env
# then edit .env and set your key
```

```env
GEMINI_API_KEY=your_api_key_here
```

> 💡 Get a free Gemini API key at [Google AI Studio](https://aistudio.google.com/app/apikey).

## 🎮 Usage

```bash
python project.py
```

| Say | Example |
|---|---|
| Greeting | "Hello", "Hey Zen" |
| Time / date | "What time is it?", "What's the date?" |
| System | "What's my CPU usage?", "Battery status" |
| Calculator | "Calculate 12 times 5 plus 3" |
| Convert | "Convert 10 km to miles" |
| Weather | "What's the weather in Delhi?" |
| Tasks | "Add task: buy groceries", "List my tasks" |
| Anything else | "Who is Ada Lovelace?" → answered by AI |
| Exit | "Exit", "Goodbye" |

## 📂 Project structure

```
project.py                     entry point + CS50P functions
src/
  core/       config, logger, exceptions, router, history_store (SQLite)
  voice/      speech_to_text, text_to_speech
  ai/         base (interface), gemini_adapter, ai_manager
  modules/
    system/       monitor (CPU/RAM/battery/disk)
    utilities/    calculator, units, weather
    productivity/ tasks (SQLite to-do)
config/settings.yaml
tests/                         unit tests
```

## 🛡️ Tech stack

| Category | Technology |
|---|---|
| Language | Python 3.11+ |
| AI | Google Gemini |
| Speech-to-text | SpeechRecognition + PyAudio |
| Text-to-speech | Microsoft Edge TTS + pygame |
| System stats | psutil |
| Storage | SQLite |
| Terminal UI | Rich |
| Testing | pytest |

## 🧪 Tests

The skills, parsers and storage are unit-tested and run without a microphone or
an API key (the one live-AI test skips automatically if no key is set):

```bash
pytest -q
# 47 passed, 1 skipped
```

## 🗺️ Roadmap

- Wake-word detection
- Email (Gmail) and calendar integration
- Timers, alarms and reminders

## 📄 License

MIT — see [LICENSE](LICENSE).

## 👨‍💻 Author

**Vicky Sharma** — [github.com/vickysharma-prog](https://github.com/vickysharma-prog)

<div align="center">
Made with Python
</div>
