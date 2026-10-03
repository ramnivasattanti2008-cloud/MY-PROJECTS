# Quiz App

A Flask-based quiz application with multiple categories, difficulty levels, and leaderboards.

## Features

- 30 pre-loaded questions across 7 categories
- Category filtering (General, Science, History, Geography, Sports, Entertainment, Technology)
- Difficulty levels (Easy, Medium, Hard)
- Real-time answer feedback with explanations
- Leaderboard with player rankings
- Player statistics tracking
- REST API for questions

## Installation

```bash
cd quiz-app
pip install -r requirements.txt
python app.py
```

## Usage

1. Open http://localhost:5003
2. Enter your name
3. Select category and difficulty
4. Answer 10 questions
5. View your results and compare on the leaderboard

## Routes

- `/` - Home page with quiz setup
- `/quiz` - POST to start quiz
- `/quiz/question` - Display current question
- `/quiz/answer` - POST to submit answer
- `/quiz/results` - Show final results
- `/leaderboard` - View rankings
- `/api/questions` - GET quiz questions via API

## Categories

- General Knowledge
- Science
- History
- Geography
- Sports
- Entertainment
- Technology

## Database

Uses SQLite database `quiz_app.db` with tables:
- `questions` - Quiz questions
- `scores` - Game scores
- `leaderboard` - Player rankings
