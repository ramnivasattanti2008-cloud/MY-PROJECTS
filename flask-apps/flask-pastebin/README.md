# Flask Pastebin

A code pastebin with syntax highlighting, expiration options, and password protection.

## Features

- Syntax highlighting for 20+ languages
- Expiration options (1 hour, 24 hours, 7 days, 30 days, never)
- Password protection for private pastes
- View count tracking
- Dark theme UI
- Raw paste viewing

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python app.py
```

The app will start on `http://localhost:5002`

## Supported Languages

Python, JavaScript, Java, C++, C, C#, Go, Rust, Ruby, PHP, Swift, Kotlin, TypeScript, HTML, CSS, SQL, Bash, JSON, XML, YAML, Markdown, and more.

## Routes

- `/` - Create new paste
- `/p/<paste_id>` - View paste
- `/raw/<paste_id>` - View raw paste content

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/create` | Create a new paste |
| GET | `/api/paste/<paste_id>` | Get paste via API |

## Database

SQLite database (`pastebin.db`) is automatically created on first run.
