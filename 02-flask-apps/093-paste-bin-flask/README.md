# Code Pastebin Flask Application

A code/text pastebin with syntax highlighting powered by Highlight.js.

## Features

- Create and share code snippets
- 23 programming languages supported
- Syntax highlighting via Highlight.js
- View raw text content
- Clone existing pastes
- Expiration options (1, 7, 30, 90 days)
- View count tracking
- REST API for programmatic access

## Installation

```bash
pip install -r requirements.txt
```

## Running the Application

```bash
python app.py
```

The application will run at `http://localhost:5001`

## Supported Languages

- Python, JavaScript, TypeScript
- Java, C, C++, C#
- Go, Rust, Ruby, PHP, Swift, Kotlin
- HTML, CSS, SQL, Bash
- JSON, XML, YAML, Markdown
- Plain Text

## API Endpoints

### List Recent Pastes
```
GET /api/pastes
```

### Get Specific Paste
```
GET /api/pastes/<paste_id>
```

### Raw Content
```
GET /raw/<paste_id>
```

## Project Structure

```
paste-bin-flask/
├── app.py              # Main Flask application
├── templates/
│   ├── index.html      # Paste creation form
│   └── view.html       # Paste viewer with highlighting
├── requirements.txt
└── README.md
```

## Database

SQLite database (`pastebin.db`) is automatically created on first run.

## License

MIT License
