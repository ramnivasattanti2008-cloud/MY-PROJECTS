# Code Explainer AI 🤖

An AI-powered tool that explains any code snippet line by line using Google's Gemini API.

## Features

- Paste any programming code (Python, JavaScript, Java, C++, Go, Rust, etc.)
- Get detailed, beginner-friendly explanations
- Auto-detect or specify the programming language
- Clean, dark-themed interface

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Get a Gemini API key from [Google AI Studio](https://aistudio.google.com/)

3. Run the app:
   ```bash
   streamlit run app.py
   ```

4. Enter your API key in the sidebar

## Usage

1. Paste your code in the text area
2. Select the programming language (or leave as "auto")
3. Click "Explain Code" to get line-by-line explanations

## Environment Variables

- `GEMINI_API_KEY` - Your Gemini API key (optional, can also enter in UI)
