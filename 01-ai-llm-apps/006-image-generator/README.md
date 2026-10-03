# AI Image Generator

Transform your text ideas into detailed image prompts using Google Gemini AI.

## Features

- Text-to-image prompt generation
- Creative and detailed descriptions
- Multiple art style suggestions
- Dark themed UI

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Get Gemini API Key

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Create a new API key
3. Enter it in the app sidebar

### 3. Run the App

```bash
streamlit run app.py
```

## Usage

1. Enter your Gemini API key in the sidebar (or set `GEMINI_API_KEY` environment variable)
2. Type your image idea in the text area
3. Click "Generate Image Prompt"
4. Copy the generated prompt to use with your favorite AI image generator

## Environment Variables

- `GEMINI_API_KEY` - Your Google Gemini API key (optional, can use sidebar input)

## Example Prompts

- "A futuristic city at sunset with flying cars"
- "An enchanted forest with glowing mushrooms"
- "A cozy coffee shop on a rainy day"
