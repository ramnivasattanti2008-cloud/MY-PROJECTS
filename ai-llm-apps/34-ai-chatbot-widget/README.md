# 34 - AI Chatbot Widget Builder

> Build a customizable embeddable chatbot widget — set personality, colors, avatar, and copy the HTML to embed anywhere.

## Quick Start

```bash
cd 34-ai-chatbot-widget
pip install -r requirements.txt
export GEMINI_API_KEY=your_key_here
streamlit run app.py
```

## Features

- **Live Widget Builder** — configure bot name, personality, color, emoji avatar, and welcome message
- **Live Preview** — see the widget as it will appear in real-time
- **Embeddable HTML** — copy the generated HTML and paste it into any website
- **Chat Testing** — test your bot's personality and responses directly in the app
- **Clear Chat** — reset conversation history

## Widget Options

| Option | Description |
|--------|-------------|
| Bot Name | Display name for the chatbot |
| Personality | Friendly / Professional / Casual / Witty / Expert / Supportive |
| Primary Color | Color picker for widget accent color |
| Avatar Emoji | Any emoji as the bot avatar |
| Welcome Message | Initial message shown when chat opens |

## Embedding

Copy the generated HTML and paste it into your website's `<body>`:
```html
<!-- Paste the generated HTML widget here -->
```

## API Key

Get your Gemini API key at https://aistudio.google.com/apikey

```bash
export GEMINI_API_KEY=your_key_here   # Linux/macOS
$env:GEMINI_API_KEY="your_key_here"   # Windows PowerShell
```

## Tech Stack

- Streamlit
- Google Gemini (Generative AI)
