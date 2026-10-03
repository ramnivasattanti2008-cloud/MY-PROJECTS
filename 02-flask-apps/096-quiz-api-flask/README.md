# Quiz API Flask Application

A trivia quiz application that fetches questions from the Open Trivia Database API.

## Features

- Fetch random trivia questions from Open Trivia DB
- Multiple difficulty levels (easy, medium, hard)
- Configurable number of questions (1-50)
- Score tracking and statistics
- High scores leaderboard
- Detailed results review
- Modern dark theme UI

## Installation

```bash
pip install -r requirements.txt
```

## Running the Application

```bash
python app.py
```

The application will run at `http://localhost:5004`

## How to Play

1. Enter your name
2. Select number of questions
3. Choose difficulty (optional)
4. Answer each question
5. View your final score and review answers

## API Integration

Uses the Open Trivia Database API:
- https://opentdb.com/api.php

Questions cover various categories including:
- Science, History, Geography
- Entertainment, Sports, Art
- And many more!

## Routes

| Route | Method | Description |
|-------|--------|-------------|
| `/` | GET | Home page with quiz setup |
| `/start` | POST | Start a new quiz session |
| `/quiz` | GET | Display current question |
| `/answer` | POST | Submit answer |
| `/result` | GET | Show quiz results |
| `/quit` | GET | Quit current quiz |

## Project Structure

```
quiz-api-flask/
├── app.py              # Main Flask application
├── templates/
│   ├── index.html      # Quiz setup and questions
│   └── result.html    # Quiz results
├── requirements.txt
└── README.md
```

## Database

SQLite database (`quiz.db`) stores:
- Quiz sessions
- Individual question results
- Player scores

## License

MIT License
