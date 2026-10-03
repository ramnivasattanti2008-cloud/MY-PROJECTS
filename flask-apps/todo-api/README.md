# Todo API

A Flask REST API for managing todos with filtering, search, and bulk operations.

## Features

- Full CRUD operations
- Filtering by completion status and priority
- Search by title and description
- Tag support
- Due date support
- Bulk operations
- Statistics endpoint

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python app.py
```

The API will run on `http://localhost:5003`

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API info |
| GET | `/api/todos` | List all todos |
| POST | `/api/todos` | Create a todo |
| GET | `/api/todos/<id>` | Get a todo |
| PUT | `/api/todos/<id>` | Update a todo |
| DELETE | `/api/todos/<id>` | Delete a todo |
| GET | `/api/todos/stats` | Get statistics |
| POST | `/api/todos/bulk` | Bulk operations |

## Query Parameters

| Parameter | Description |
|-----------|-------------|
| `completed` | Filter by completion (true/false) |
| `priority` | Filter by priority (low/medium/high) |
| `tag` | Filter by tag |
| `search` | Search in title and description |

## API Examples

```bash
# Create a todo
curl -X POST http://localhost:5003/api/todos \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Learn Flask",
    "description": "Build a REST API with Flask",
    "priority": "high",
    "tags": "python, flask, api",
    "due_date": "2026-09-30T12:00:00"
  }'

# List all todos
curl http://localhost:5003/api/todos

# Filter completed todos
curl "http://localhost:5003/api/todos?completed=true"

# Search todos
curl "http://localhost:5003/api/todos?search=flask"

# Filter by priority
curl "http://localhost:5003/api/todos?priority=high"

# Update a todo
curl -X PUT http://localhost:5003/api/todos/1 \
  -H "Content-Type: application/json" \
  -d '{"completed": true}'

# Bulk complete
curl -X POST http://localhost:5003/api/todos/bulk \
  -H "Content-Type: application/json" \
  -d '{"action": "complete", "ids": [1, 2, 3]}'

# Get statistics
curl http://localhost:5003/api/todos/stats
```

## Response Format

```json
{
  "id": 1,
  "title": "Learn Flask",
  "description": "Build a REST API with Flask",
  "completed": false,
  "priority": "high",
  "tags": ["python", "flask", "api"],
  "created_at": "2026-09-06T10:00:00",
  "updated_at": "2026-09-06T10:00:00",
  "due_date": "2026-09-30T12:00:00"
}
```

## Database

SQLite database is automatically created on first run. Database file: `todos.db`
