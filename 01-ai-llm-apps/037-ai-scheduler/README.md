# AI Scheduler 📅

Let AI create optimal daily schedules based on your tasks, available time, and energy levels.

## Features

- **Smart Scheduling** - AI optimizes your day for maximum productivity
- **Energy-Aware** - Schedules demanding tasks during peak hours
- **Flexible Input** - Works with any number of tasks
- **Break Integration** - Includes natural break times

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set your API key:
```bash
export GEMINI_API_KEY="your-api-key"
```

3. Run the app:
```bash
streamlit run app.py
```

## Usage

1. Set your available time (start and end)
2. Enter your tasks (one per line)
3. Select focus areas and energy level
4. Click "Generate Schedule"
5. Get an optimized daily plan

## Example Tasks

```
Complete project report
Team meeting
Code review
Lunch break
Email responses
Gym workout
Read documentation
```

## Tech Stack

- Streamlit - Web UI
- Google Gemini - AI scheduling optimization
- Python - Backend logic
