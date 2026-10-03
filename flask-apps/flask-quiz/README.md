# Flask Quiz App

An interactive quiz application using the Open Trivia Database API with score tracking and leaderboards.

## Features

- Questions from Open Trivia Database (thousands of questions)
- Multiple categories (General Knowledge, Science, History, etc.)
- Three difficulty levels (Easy, Medium, Hard)
- Configurable number of questions (5-50)
- Score tracking and statistics
- Global leaderboard
- Dark theme UI

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python app.py
```

The app will start on `http://localhost:5005`

## Categories

- General Knowledge
- Entertainment: Books
- Entertainment: Film
- Entertainment: Music
- Entertainment: Television
- Entertainment: Video Games
- Science & Nature
- Science: Computers
- Science: Mathematics
- Sports
- Geography
- History
- Animals

## Routes

| Route | Description |
|-------|-------------|
| `/` | Home page with quiz setup |
| `/quiz` | Take the quiz |
| `/results` | View quiz results |
| `/leaderboard` | View top scores |

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/categories` | List available categories |
| GET | `/api/stats` | Get quiz statistics |

## Database

SQLite database (`quiz.db`) is automatically created on first run.

## How to Play

1. Enter your name
2. Select number of questions (5-50)
3. Choose difficulty level
4. Select a category (or any)
5. Answer all questions
6. View your results and compare with others on the leaderboard
