# Code Paste

A code sharing site with syntax highlighting. Paste code, get a shareable link, and view with beautiful syntax highlighting.

## Features

- Paste code with language auto-detection
- 24+ programming languages supported
- Syntax highlighting via Pygments
- Shareable URLs for each paste
- View count tracking
- Copy code to clipboard
- Recent pastes gallery
- Dark IDE-style theme

## Tech Stack

- **Backend**: Flask, Flask-CORS, Pygments, SQLite
- **Frontend**: React, TypeScript
- **Database**: SQLite (auto-created)
- **Syntax Highlighting**: Pygments (server-side)

## Setup

### Backend

```bash
cd backend
pip install -r requirements.txt
python app.py
```

The server runs on `http://localhost:5004`

### Frontend

```bash
cd frontend
npm install
npm start
```

The app runs on `http://localhost:3003`

## Supported Languages

javascript, typescript, python, java, cpp, c, csharp, go, rust, ruby, php, swift, kotlin, scala, html, css, sql, bash, powershell, json, yaml, xml, markdown, and more.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/languages` | List supported languages |
| POST | `/api/pastes` | Create a new paste |
| GET | `/api/pastes` | List recent pastes |
| GET | `/api/pastes/<id>` | Get paste details |
| GET | `/api/pastes/<id>/raw` | Get raw code |
| GET | `/paste/<id>` | View paste as HTML page |
