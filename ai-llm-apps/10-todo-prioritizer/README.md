# Todo Prioritizer

AI-powered task prioritization that analyzes your tasks and explains the reasoning.

## Features

- Intelligent task analysis
- Priority levels (High/Medium/Low)
- Reasoning for each decision
- Visual task grouping
- Summary metrics

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
2. Enter your tasks (one per line)
3. Click "Prioritize Tasks"
4. Review AI-generated priorities and reasoning
5. Focus on High priority tasks first

## How It Works

The AI considers:
- Urgency and deadlines
- Impact and importance
- Task dependencies
- Effort vs value ratio

## Example Tasks

```
Finish project report (due Friday)
Call dentist for appointment
Buy groceries for dinner
Study for certification exam
Clean the house before guests arrive
```

## Environment Variables

- `GEMINI_API_KEY` - Your Google Gemini API key (optional)
