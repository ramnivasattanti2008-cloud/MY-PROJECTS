# ✒️ AI Poem Generator

A creative poetry app powered by Google Gemini that transforms emotions and themes into beautiful, original poems.

## Features

- **7 Poetry Styles**: Haiku, Sonnet, Free Verse, Limerick, Ode, Ballad, Acrostic
- **12 Mood Options**: Love, Nature, Melancholy, Joy, Mystery, Adventure, and more
- **Custom Themes**: Enter your own theme or keyword
- **Emotional Keywords**: Add specific feelings to incorporate
- **Interpretation**: Optional deeper meaning analysis
- **Quick Prompts**: One-click mood selection

## Installation

```bash
pip install -r requirements.txt
```

## Setup

1. Get a Google Gemini API key from [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Set the environment variable:
   ```bash
   export GEMINI_API_KEY="your-api-key"  # Linux/Mac
   set GEMINI_API_KEY="your-api-key"     # Windows
   ```

## Usage

```bash
streamlit run app.py
```

## Poetry Styles Explained

| Style | Description | Best For |
|-------|-------------|----------|
| Haiku | 3 lines, 5-7-5 syllables | Nature, brief moments |
| Sonnet | 14 lines, rhyme scheme | Love, deep emotions |
| Free Verse | No structure | Modern expression |
| Limerick | 5 lines, AABBA | Humor, playfulness |
| Ode | Celebratory, formal | Honoring subjects |
| Ballad | Narrative with repetition | Storytelling |
| Acrostic | Hidden message in letters | Personal messages |

## Examples

```python
# Set your API key
export GEMINI_API_KEY="..."

# Run the app
streamlit run app.py
```

## Tech Stack

- Streamlit - Web UI framework
- Google Gemini - AI poetry generation
