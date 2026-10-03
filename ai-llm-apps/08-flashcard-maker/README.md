# Flashcard Maker

Create study flashcards from any topic using Google Gemini AI.

## Features

- Generate Q&A flashcards from topics/notes
- Adjustable number of cards (3-15)
- Download as text file
- Dark themed UI

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Get Gemini API Key

1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Create a new API key
3. Enter it in the app sidebar

### 3. Run the App

```bash
streamlit run app.py
```

## Usage

1. Enter your Gemini API key in the sidebar
2. Type your topic or paste study notes
3. Adjust number of flashcards with slider
4. Click "Generate Flashcards"
5. Download cards as text file

## Example Topics

- "Python list comprehensions"
- "World War II key events"
- "Cell biology basics"
- "Math formulas"

## Environment Variables

- `GEMINI_API_KEY` - Your Google Gemini API key (optional)
