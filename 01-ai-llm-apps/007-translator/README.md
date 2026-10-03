# AI Translator

Intelligent text translation with automatic language detection using Google Gemini AI.

## Features

- Auto-detect input language
- 22+ supported languages including Indian languages
- Preserve tone and nuance
- Clean dark themed interface

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

## Supported Languages

- English, Spanish, French, German, Italian, Portuguese
- Russian, Japanese, Korean, Chinese
- Arabic, Hindi, Tamil, Telugu, Kannada
- Malayalam, Bengali, Marathi, Gujarati, Punjabi, Urdu

## Usage

1. Enter your Gemini API key in the sidebar
2. Type or paste text in the text area
3. Toggle auto-detect or select source language
4. Choose target language
5. Click Translate

## Environment Variables

- `GEMINI_API_KEY` - Your Google Gemini API key (optional)
