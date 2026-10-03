# 32 - AI Grammar & Style Checker

> Paste any text — get grammar fixes, style improvements, and explanations.

## Quick Start

```bash
cd 32-ai-grammar-check
pip install -r requirements.txt
export GEMINI_API_KEY=your_key_here
streamlit run app.py
```

## Features

- **Full Check** — grammar, spelling, punctuation + style improvements
- **Grammar Only** — pure grammar/spelling/punctuation fixes
- **Style Only** — clarity and engagement improvements without changing meaning
- **Quick Reference** — built-in grammar rule cheat sheet
- Highlights issues with original → corrected explanations

## API Key

Get your Gemini API key at https://aistudio.google.com/apikey

```bash
export GEMINI_API_KEY=your_key_here   # Linux/macOS
$env:GEMINI_API_KEY="your_key_here"   # Windows PowerShell
```

## Tech Stack

- Streamlit
- Google Gemini (Generative AI)
