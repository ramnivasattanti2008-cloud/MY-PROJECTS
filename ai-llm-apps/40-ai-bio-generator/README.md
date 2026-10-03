# Bio Generator

Create catchy social media bios for any profession using AI.

## Features

- Input profession and personality traits
- Choose platform (Twitter/X, LinkedIn, Instagram)
- Select style (Professional, Casual, Witty, etc.)
- Add interests and hobbies
- Generate multiple unique bio options
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

1. Enter your profession
2. Add personality traits
3. Select platform and style
4. Optionally add interests
5. Choose number of bio options
6. Click "Generate Bios"
7. Get multiple unique bio options to choose from

## Platform Guidelines

- **Twitter/X**: 160 characters max
- **LinkedIn**: 220 characters max
- **Instagram**: 150 characters max

## Tech Stack

- Streamlit
- Google Gemini AI
- Python dotenv
