# Sentence Expander

Transform short phrases into compelling full paragraphs using AI.

## Features

- Input short phrases or ideas
- Choose writing tone (Formal, Casual, Persuasive, Academic, Creative)
- Adjust target word count
- Select use case (Essay, Article, Blog Post, Report, Speech)
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

1. Enter your short phrase
2. Select desired tone and use case
3. Adjust word count slider
4. Click "Expand Sentence"
5. Get a fully developed paragraph

## Tech Stack

- Streamlit
- Google Gemini AI
- Python dotenv
