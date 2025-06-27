# Voice-to-Text LLM Integration

A Python application that combines voice-to-text functionality with LLM (Large Language Model) integration for recipe suggestions with Indiana flavors.

## Features

- 🎤 **Voice Input**: Convert speech to text using microphone input
- 🤖 **LLM Integration**: Send voice/text prompts to OpenAI's GPT-3.5-turbo
- 🍳 **Recipe Focus**: Specialized for Indiana-inspired recipes
- 📝 **Text Input**: Traditional text-based prompting also available
- 🔧 **Easy Integration**: Modular design for easy app integration

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Audio Setup (macOS)

For PyAudio on macOS, you might need to install portaudio first:

```bash
brew install portaudio
pip install PyAudio
```

### 3. API Key

The application uses an OpenAI API key. Make sure your API key is valid and has sufficient credits.

## Usage

### Quick Start

Run the interactive demo:

```bash
python voice_demo.py
```

### Programmatic Usage

```python
from chatgpt import voice_to_llm, ask_llm

# Voice input
response = voice_to_llm()

# Text input
response = ask_llm("Suggest a recipe using corn and tomatoes")
```

### Direct Script Execution

```bash
python chatgpt.py
```

## Functions

### `voice_input()`
- Captures audio from microphone
- Converts speech to text using Google's speech recognition
- Returns transcribed text or None if failed

### `voice_to_llm()`
- Combines voice input with LLM query
- Returns LLM response based on voice prompt

### `ask_llm(prompt)`
- Sends text prompt to OpenAI's GPT-3.5-turbo
- Returns recipe suggestions with Indiana focus

## Integration

To integrate into your app:

1. Import the functions: `from chatgpt import voice_to_llm, ask_llm`
2. Call `voice_to_llm()` for voice input
3. Call `ask_llm(prompt)` for text input
4. Handle responses as needed

## Error Handling

The voice functionality includes comprehensive error handling for:
- No speech detected
- Unrecognizable audio
- Network/API errors
- Timeout scenarios

## Requirements

- Python 3.7+
- Microphone access
- Internet connection (for speech recognition and LLM API)
- OpenAI API key