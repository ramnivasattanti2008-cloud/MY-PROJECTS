# Pastebin

A Flask-based pastebin with syntax highlighting, expiration options, and password protection.

## Features

- Syntax highlighting via highlight.js
- Multiple programming languages supported
- Expiration options (1h, 24h, 7d, 30d, never)
- Password protection
- View count tracking
- Raw paste viewing
- RESTful API

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python app.py
```

The app will run on `http://localhost:5002`

## Supported Languages

- Python, JavaScript, TypeScript, Java
- C++, C#, Go, Rust
- HTML, CSS, SQL, JSON, Bash, Markdown
- Plain Text

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/create` | Create a new paste |
| GET | `/p/<paste_id>` | View a paste |
| GET | `/p/<paste_id>/raw` | Get raw paste content |
| POST | `/p/<paste_id>/verify` | Verify password |
| GET | `/api/pastes` | List recent pastes |
| DELETE | `/api/pastes/<paste_id>` | Delete a paste |

## API Examples

```bash
# Create a paste
curl -X POST http://localhost:5002/create \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Hello World",
    "content": "print(\"Hello, World!\")",
    "language": "python",
    "expiration": "24h"
  }'

# Create with password
curl -X POST http://localhost:5002/create \
  -H "Content-Type: application/json" \
  -d '{
    "content": "secret data",
    "password": "mypassword"
  }'

# Verify password
curl -X POST http://localhost:5002/p/<paste_id>/verify \
  -H "Content-Type: application/json" \
  -d '{"password": "mypassword"}'
```

## Database

SQLite database is automatically created on first run. Database file: `pastebin.db`
