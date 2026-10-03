# Quiz Game

A Flask quiz game that fetches trivia questions from the Open Trivia Database API.

## Features

- Questions from Open Trivia DB (opentdb.com)
- Multiple categories (Science, History, Geography, etc.)
- Difficulty levels (Easy, Medium, Hard)
- Time-based scoring system
- Score tracking and leaderboard
- Answer review after quiz
- Dark-themed UI

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python app.py
```

The app will run on `http://localhost:5005`

## Categories

- General Knowledge
- Science & Nature
- Computer Science
- Sports
- Geography
- History
- Art
- Animals

## How to Play

1. Enter your name
2. Select a category (optional)
3. Select difficulty (optional)
4. Click "Start Quiz"
5. Answer 10 multiple choice questions
6. Score points based on correctness and speed
7. View your results and compare on the leaderboard

## Scoring

- Base score: 100 points per correct answer
- Time bonus: -5 points per second taken
- Minimum score per question: 10 points

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Home page |
| POST | `/play` | Start a quiz |
| GET | `/question` | Get current question |
| POST | `/answer` | Submit an answer |
| GET | `/results` | View quiz results |
| GET | `/leaderboard` | View leaderboard |
| GET | `/api/scores` | Get scores (JSON) |
| GET | `/api/categories` | Get categories (JSON) |

## API Examples

```bash
# Get leaderboard
curl http://localhost:5005/api/scores

# Get categories
curl http://localhost:5005/api/categories
```

## Database

SQLite database is automatically created on first run. Database file: `quiz.db`

## Requirements

- Internet connection (to fetch questions from Open Trivia DB)
- Python 3.8+
