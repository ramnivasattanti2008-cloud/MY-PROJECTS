# Text to Speech Converter

A Python script that converts text to speech using Google Text-to-Speech (gTTS) and saves the result as an MP3 file.

## Features

- Convert text to natural-sounding speech
- Support for 18+ languages
- Configurable speech speed (normal/slow)
- Multiple input modes:
  - Direct text input
  - Read from file
  - Clipboard content
  - Interactive mode
- Timestamped output filenames
- Customizable output directory

## Installation

1. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

### Quick Start - Interactive Mode
```bash
python text-to-speech.py
```

### Convert Text Directly
```bash
python text-to-speech.py "Hello, this is a test message"
```

### Convert from File
```bash
python text-to-speech.py --file readme.txt
```

### Specify Language
```bash
python text-to-speech.py "Hola mundo" --lang es
```

### Slow Speech
```bash
python text-to-speech.py "Welcome" --slow
```

### Custom Output File
```bash
python text-to-speech.py "Hello" --output C:\Audio\welcome.mp3
```

## Interactive Mode Commands

When running in interactive mode:
- Enter text directly to convert
- `paste` - Convert clipboard content
- `file <path>` - Convert text from file
- `lang` - List and change language
- `slow` - Toggle slow mode
- `dir <path>` - Change output directory
- `quit` - Exit

## Available Languages

| Code | Language |
|------|----------|
| en | English |
| es | Spanish |
| fr | French |
| de | German |
| it | Italian |
| pt | Portuguese |
| ru | Russian |
| ja | Japanese |
| ko | Korean |
| zh-CN | Chinese (Simplified) |
| hi | Hindi |
| ar | Arabic |
| nl | Dutch |
| pl | Polish |
| tr | Turkish |
| sv | Swedish |
| da | Danish |
| no | Norwegian |
| fi | Finnish |

## Example Output

```
==================================================
TEXT TO SPEECH CONVERTER
Convert text to audio using gTTS
==================================================

Converting text to speech...
  Language: English
  Speed: Normal
  Characters: 45
----------------------------------------

Audio file created successfully!
  File: tts_2024-01-15_14-30-00.mp3
  Location: C:\Users\Username\Documents\Audio\tts_2024-01-15_14-30-00.mp3
  Size: 12.3 KB

File saved: C:\Users\Username\Documents\Audio\tts_2024-01-15_14-30-00.mp3
```

## Requirements

- Python 3.6 or higher
- gTTS library (pip install gtts)
- Internet connection (for Google TTS API)

## Notes

- Requires internet connection to generate speech
- Audio is saved to `~/Documents/Audio/` by default
- Output files use timestamp naming to avoid overwrites
- Character limit depends on Google's limits (usually ~5,000 chars)
