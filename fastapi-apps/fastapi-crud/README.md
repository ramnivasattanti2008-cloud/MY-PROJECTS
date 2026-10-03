# FastAPI CRUD API

A simple FastAPI CRUD API for managing tasks with SQLite database.

## Features

- Full CRUD operations for tasks
- SQLite persistence
- Pydantic validation
- Pagination and filtering
- Search functionality
- CORS enabled
- Auto-generated API docs

## Installation

```bash
pip install -r requirements.txt
```

## Running the Server

```bash
uvicorn main:app --reload
```

Or:

```bash
python main.py
```

The server runs on `http://localhost:8000`

## API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### Health Check
```bash
curl http://localhost:8000/
```

### Create Task
```bash
curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Complete project documentation",
    "description": "Write comprehensive docs for the API",
    "priority": "high"
  }'
```

### List Tasks (with pagination)
```bash
# Get first page of tasks
curl "http://localhost:8000/tasks?page=1&page_size=10"

# Filter by completed status
curl "http://localhost:8000/tasks?completed=false"

# Filter by priority
curl "http://localhost:8000/tasks?priority=high"

# Search in title/description
curl "http://localhost:8000/tasks?search=documentation"
```

### Get Single Task
```bash
curl http://localhost:8000/tasks/{task_id}
```

### Update Task
```bash
curl -X PUT http://localhost:8000/tasks/{task_id} \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated title",
    "completed": true
  }'
```

### Delete Task
```bash
curl -X DELETE http://localhost:8000/tasks/{task_id}
```

### Get Statistics
```bash
curl http://localhost:8000/stats
```

## Example Workflow

```bash
# Create a task
TASK_ID=$(curl -s -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Test task", "priority": "medium"}' | jq -r '.id')

# Get the task
curl http://localhost:8000/tasks/$TASK_ID

# Update the task
curl -X PUT http://localhost:8000/tasks/$TASK_ID \
  -H "Content-Type: application/json" \
  -d '{"completed": true}'

# Delete the task
curl -X DELETE http://localhost:8000/tasks/$TASK_ID
```

## Data Model

### Task
| Field | Type | Description |
|-------|------|-------------|
| id | string | Unique identifier (UUID) |
| title | string | Task title (required, 1-200 chars) |
| description | string | Task description (optional, max 1000 chars) |
| completed | boolean | Completion status (default: false) |
| priority | string | Priority level: low, medium, high (default: medium) |
| created_at | string | ISO timestamp |
| updated_at | string | ISO timestamp |

## License

MIT
