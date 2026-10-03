# Music Lyrics Generator

Generate original song lyrics with AI based on mood, theme, and genre.

## Features

- Input theme/mood and story topic
- Choose music genre (Pop, Rock, Hip-Hop, R&B, etc.)
- Select song style (Storytelling, Emotional, Upbeat, etc.)
- Generate multiple verses with chorus
- Dark theme with polished UI

## Setup

1. Create a `.env` file with your API key:
```
GEMINI_API_KEY=your_api_key_here
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the app:
```bash
streamlit run app.py
```

## Usage

1. Enter your theme/mood
2. Optionally add a story or topic
3. Select genre and style
4. Choose number of verses
5. Click "Generate Lyrics"
6. Get original song lyrics with verses and chorus

## Tech Stack

- Streamlit
- Google Gemini AI
- Python dotenv
