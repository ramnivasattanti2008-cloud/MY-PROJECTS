# Pastebin Clone

A Flask-based code/text pastebin with syntax highlighting, expiration, and password protection.

## Features

- Syntax highlighting for 20+ languages
- Auto language detection
- Expiration options (10 min, 1 hour, 1 day, 1 week, 1 month)
- Password protection
- Public/unlisted exposure
- View count tracking
- Raw and download modes
- Trending pastes
- REST API

## Installation

```bash
cd pastebin
pip install -r requirements.txt
python app.py
```

## Usage

1. Open http://localhost:5002
2. Paste your code or text
3. Choose language, expiration, and privacy options
4. Click "Create Paste"
5. Share the generated link

## Routes

- `/` - Home page with paste creation form
- `/create` - POST endpoint to create paste
- `/p/<paste_id>` - View a paste
- `/p/<paste_id>/raw` - Raw text view
- `/p/<paste_id>/download` - Download as file
- `/trending` - View trending pastes
- `/api/paste/<paste_id>` - GET paste via API
- `/api/create` - POST to create paste via API

## Supported Languages

Python, JavaScript, Java, C++, C, C#, Go, Rust, Ruby, PHP, Swift, Kotlin, TypeScript, HTML, CSS, SQL, Bash, JSON, XML, YAML, Markdown, Plain Text

## Database

Uses SQLite database `pastebin.db` with table:
- `pastes` - Stores all paste data
