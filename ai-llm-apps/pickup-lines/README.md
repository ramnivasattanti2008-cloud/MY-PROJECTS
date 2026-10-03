# 💬 AI Pickup Line Generator

A fun, creative tool powered by Google Gemini that generates witty, charming, and sometimes cheesy pickup lines for any situation.

## Features

- **10 Situations**: Casual, Online Dating, Workplace, Party, Coffee Shop, Travel, Art, Concert, Sports, Any
- **6 Styles**: Witty, Cheesy, Romantic, Geeky, Dark Humor, Self-Deprecating
- **Customizable Count**: Generate 3-10 lines at once
- **Explanations**: Learn why each line works
- **Effectiveness Ratings**: See which lines are most likely to succeed
- **Target Description**: Get personalized lines based on interests

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

1. Select your situation (where you're meeting someone)
2. Choose your preferred style of humor
3. Pick how many lines to generate
4. Optionally describe your target's interests
5. Toggle explanations and ratings
6. Click "Generate Pickup Lines"

## Style Guide

| Style | Best For | Vibe |
|-------|----------|------|
| Witty & Clever | Smart audiences | Intellectual wordplay |
| Cheesy & Fun | Breaking the ice | Light-hearted puns |
| Smooth & Romantic | Nighttime场合 | Classic charm |
| Geeky/Nerdy | Tech/SCI-FI fans | Reference-based humor |
| Dark Humor | Edgy crowds | Bold and unexpected |
| Self-Deprecating | Building rapport | Humble and relatable |

## Example Situations

- **Coffee Shop**: "Are you a double espresso? Because you're keeping me awake all night."
- **Online Dating**: "I'm not a photographer, but I can definitely picture us together."
- **Concert**: "Are you the opening act? Because you've got my attention."

## Tech Stack

- Streamlit - Web UI framework
- Google Gemini - AI line generation

## Disclaimer

Use responsibly and always respect personal boundaries. Humor is subjective - read the room before delivering any line!
