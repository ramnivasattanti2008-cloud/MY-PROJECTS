# Bug Detector

Find and fix bugs in your Python code using Google Gemini AI.

## Features

- Intelligent bug detection
- Automatic fix suggestions
- Code explanation
- Best practices tips
- Dark themed interface

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
2. Paste your Python code
3. Click "Find Bugs"
4. Review identified issues, fixes, and tips

## What It Detects

- Syntax errors
- Logic bugs
- Runtime exceptions (IndexError, TypeError, etc.)
- Empty list/dict access
- Best practice violations
- Security issues

## Example Bugs It Finds

- Division by zero
- Index out of bounds
- Undefined variables
- Type mismatches
- Missing error handling

## Environment Variables

- `GEMINI_API_KEY` - Your Google Gemini API key (optional)
