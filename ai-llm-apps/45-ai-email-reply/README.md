# AI Email Reply 📧

Get professional email response suggestions for any received email.

## Features

- **Multiple Options** - Choose from 3 different reply styles
- **Tone Control** - Professional, friendly, brief, or enthusiastic
- **Length Options** - Short, medium, or detailed responses
- **Quick Templates** - Common reply templates included

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set your API key:
```bash
export GEMINI_API_KEY="your-api-key"
```

3. Run the app:
```bash
streamlit run app.py
```

## Usage

1. Paste the email you received
2. Select reply tone (Professional, Friendly, Brief, Enthusiastic)
3. Choose length (Short, Medium, Detailed)
4. Optionally add context (meeting times, attachments, etc.)
5. Click "Generate Reply Options"
6. Choose and customize your preferred reply

## Quick Templates Included

- **Acknowledgment** - Quick receipt confirmation
- **Meeting Request** - Schedule follow-up discussions
- **Follow Up** - Nudge on previous conversations
- **Decline** - Professional declination

## Tech Stack

- Streamlit - Web UI
- Google Gemini - AI response generation
- Python - Backend logic
