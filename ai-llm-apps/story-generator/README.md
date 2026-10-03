# 📖 AI Story Generator

An interactive storytelling app powered by Google Gemini AI that crafts unique short stories based on your creative prompts.

## Features

- **Multiple Genres**: Fantasy, Sci-Fi, Mystery, Romance, Horror, Adventure, Comedy, Drama
- **Customizable Tone**: Dark, Light, Humorous, Suspenseful, Heartwarming
- **Adjustable Length**: 300-700 words
- **Character & Setting Input**: Define your story's elements
- **Structured Output**: Title, characters, plot points, and full narrative

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

## How It Works

1. Select your preferred genre and tone
2. Choose your story length
3. Enter a story starter prompt (be creative!)
4. Optionally define a main character and setting
5. Click "Generate Story" and let the AI weave your tale

## Demo Mode

Without an API key, the app runs in demo mode showing the story structure template.

## Tech Stack

- Streamlit - Web UI framework
- Google Gemini - AI story generation
