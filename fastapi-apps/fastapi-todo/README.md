# FastAPI Todo API

A simple and elegant Todo API built with FastAPI and SQLite.

## Features

- Full CRUD operations for todos
- Filter by completion status and priority
- Pagination support
- Priority levels (low, medium, high)
- Auto-generated API documentation at `/docs`

## Installation

```bash
cd fastapi-todo
pip install -r requirements.txt
```

## Running the API

```bash
uvicorn main:app --reload
```

Or run directly:

```bash
python main.py
```

The API will be available at `http://localhost:8000`

## API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### Health Check
```bash
curl http://localhost:8000/health
```

### Create Todo
```bash
# Create a todo with all fields
curl -X POST "http://localhost:8000/todos" \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy groceries", "description": "Milk, bread, eggs", "priority": "high"}'

# Create a minimal todo
curl -X POST "http://localhost:8000/todos" \
  -H "Content-Type: application/json" \
  -d '{"title": "Read a book"}'
```

### Get All Todos
```bash
# Get all todos
curl http://localhost:8000/todos

# Get only completed todos
curl "http://localhost:8000/todos?completed=true"

# Get only high priority todos
curl "http://localhost:8000/todos?priority=high"

# Get todos with pagination
curl "http://localhost:8000/todos?skip=0&limit=10"
```

### Get Single Todo
```bash
curl http://localhost:8000/todos/1
```

### Update Todo
```bash
# Update title and priority
curl -X PUT "http://localhost:8000/todos/1" \
  -H "Content-Type: application/json" \
  -d '{"title": "Updated title", "priority": "low"}'

# Mark as completed
curl -X PUT "http://localhost:8000/todos/1" \
  -H "Content-Type: application/json" \
  -d '{"completed": true}'
```

### Delete Todo
```bash
curl -X DELETE "http://localhost:8000/todos/1"
```

### Clear Completed Todos
```bash
curl -X DELETE "http://localhost:8000/todos/completed/clear"
```

## Data Model

### Todo
| Field | Type | Description |
|-------|------|-------------|
| id | int | Unique identifier (auto-generated) |
| title | string | Todo title (required, max 255 chars) |
| description | string | Todo description (optional, max 1000 chars) |
| completed | boolean | Completion status (default: false) |
| priority | string | Priority level: low, medium, high (default: medium) |
| created_at | datetime | Creation timestamp |
| updated_at | datetime | Last update timestamp |

## Project Structure

```
fastapi-todo/
├── main.py           # Main application code
├── requirements.txt # Python dependencies
├── README.md        # This file
└── todo.db          # SQLite database (created on first run)
```

## License

MIT
