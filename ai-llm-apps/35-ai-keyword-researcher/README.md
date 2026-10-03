# 35 - AI Keyword Researcher

> Input a topic and get SEO keywords, long-tail phrases, questions, and content ideas.

## Quick Start

```bash
cd 35-ai-keyword-researcher
pip install -r requirements.txt
export GEMINI_API_KEY=your_key_here
streamlit run app.py
```

## Features

- **Primary Keywords** — high-volume, competitive head terms
- **Secondary Keywords** — medium-volume, moderate competition
- **Long-tail Keywords** — low competition, high purchase intent
- **Question Keywords** — FAQ-style for featured snippets
- **Content Ideas** — 3 SEO-friendly blog post titles
- **Difficulty Tips** — color-coded guidance for each keyword tier
- **Manual Tracker** — save keywords you're actively tracking
- **Configurable Output** — choose number of keywords, include/exclude question and long-tail keywords

## Settings

| Setting | Description |
|---------|-------------|
| Topic / Niche | Your main subject area |
| Target Audience | Who you're writing for |
| Content Type | Blog, SEO Article, YouTube, Social, Product Page |
| Number of Keywords | 5–30 keywords |
| Question Keywords | Include "how", "why", "what" queries |
| Long-tail Keywords | 3-5 word phrases |

## API Key

Get your Gemini API key at https://aistudio.google.com/apikey

```bash
export GEMINI_API_KEY=your_key_here   # Linux/macOS
$env:GEMINI_API_KEY="your_key_here"   # Windows PowerShell
```

## Tech Stack

- Streamlit
- Google Gemini (Generative AI)
