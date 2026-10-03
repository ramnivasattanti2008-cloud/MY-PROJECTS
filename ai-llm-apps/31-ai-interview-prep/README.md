# 31 - AI Interview Prep Coach

> Input a job role, get likely interview questions, sample answers, and tips.

## Quick Start

```bash
cd 31-ai-interview-prep
pip install -r requirements.txt
export GEMINI_API_KEY=your_key_here
streamlit run app.py
```

## Features

- **Question Generator** — generates 8-10 realistic questions based on job role, experience level, and focus areas
- **Practice Mode** — paste any question and get a strong answer outline + tips
- **Focus Areas** — Technical, Behavioral, Situational, HR/Round 1
- **Experience Levels** — Fresher, Mid-Level, Senior, Lead/Manager

## API Key

Get your Gemini API key at https://aistudio.google.com/apikey

Set it as an environment variable:
```bash
export GEMINI_API_KEY=your_key_here   # Linux/macOS
set GEMINI_API_KEY=your_key_here       # Windows CMD
$env:GEMINI_API_KEY="your_key_here"   # Windows PowerShell
```

## Tech Stack

- Streamlit
- Google Gemini (Generative AI)
