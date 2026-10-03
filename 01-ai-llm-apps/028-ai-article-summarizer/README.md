# 33 - AI Article Summarizer

> Paste an article URL or text — get a clear, structured summary with key takeaways.

## Quick Start

```bash
cd 33-ai-article-summarizer
pip install -r requirements.txt
export GEMINI_API_KEY=your_key_here
streamlit run app.py
```

## Features

- **URL Mode** — paste any article URL and it auto-fetches the content
- **Text Mode** — paste raw text directly
- **Adjustable Length** — Short (3 bullets), Medium (5 bullets), Long (8 bullets)
- **Customizable Output** — choose to include: Key Takeaways, Main Arguments, Supporting Evidence, TL;DR
- Clean markdown-formatted output

## API Key

Get your Gemini API key at https://aistudio.google.com/apikey

```bash
export GEMINI_API_KEY=your_key_here   # Linux/macOS
$env:GEMINI_API_KEY="your_key_here"   # Windows PowerShell
```

## Tech Stack

- Streamlit
- Google Gemini (Generative AI)
- BeautifulSoup4 (web scraping)
