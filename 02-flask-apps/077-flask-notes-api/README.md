# Flask Notes API

A RESTful notes API built with Flask, featuring full CRUD operations and SQLite storage.

## Features

- Full CRUD operations (Create, Read, Update, Delete)
- SQLite database for persistent storage
- Search functionality
- JSON responses
- CORS enabled

## Installation

```bash
pip install -r requirements.txt
```

## Running the Server

```bash
python app.py
```

The API will be available at `http://localhost:5000`

## API Endpoints

### Health Check
```bash
curl http://localhost:5000/health
```

### Create Note
```bash
# Create a simple note
curl -X POST http://localhost:5000/notes \
  -H "Content-Type: application/json" \
  -d '{"title": "My First Note", "content": "This is the note content"}'

# Create another note
curl -X POST http://localhost:5000/notes \
  -H "Content-Type: application/json" \
  -d '{"title": "Shopping List", "content": "Milk, eggs, bread"}'
```

### Get All Notes
```bash
# Get all notes
curl http://localhost:5000/notes

# Search notes by title or content
curl "http://localhost:5000/notes?search=shopping"
```

### Get Single Note
```bash
curl http://localhost:5000/notes/1
```

### Update Note
```bash
# Update title only
curl -X PUT http://localhost:5000/notes/1 \
  -H "Content-Type: application/json" \
  -d '{"title": "Updated Title"}'

# Update content only
curl -X PUT http://localhost:5000/notes/1 \
  -H "Content-Type: application/json" \
  -d '{"content": "Updated content goes here"}'

# Update both
curl -X PUT http://localhost:5000/notes/1 \
  -H "Content-Type: application/json" \
  -d '{"title": "New Title", "content": "New content"}'
```

### Delete Note
```bash
curl -X DELETE http://localhost:5000/notes/1
```

### Get Notes Count
```bash
curl http://localhost:5000/notes/count
```

## Response Format

### Success Response
```json
{
  "success": true,
  "data": {
    "id": 1,
    "title": "Note Title",
    "content": "Note content",
    "created_at": "2024-01-01T12:00:00.000000",
    "updated_at": "2024-01-01T12:00:00.000000"
  }
}
```

### Error Response
```json
{
  "error": "Error message"
}
```

### List Response
```json
{
  "success": true,
  "count": 2,
  "data": [...]
}
```

## Note Schema

| Field      | Type    | Description                      |
|------------|---------|----------------------------------|
| id         | INTEGER | Primary key, auto-increment      |
| title      | TEXT    | Note title (required)           |
| content    | TEXT    | Note content                     |
| created_at | TEXT    | ISO timestamp of creation        |
| updated_at | TEXT    | ISO timestamp of last update     |

## Database

SQLite database file: `notes.db`

The database is automatically created on first run.
