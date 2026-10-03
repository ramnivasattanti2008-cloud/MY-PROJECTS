# Todo REST API Flask Application

A RESTful API for managing a todo list with full CRUD operations.

## Features

- Full CRUD operations for todos
- Filtering by completion status and priority
- Search in title and description
- Statistics endpoint
- Bulk operations (complete all, clear completed)
- Proper error handling and validation
- JSON responses with consistent structure

## Installation

```bash
pip install -r requirements.txt
```

## Running the Application

```bash
python app.py
```

The API will run at `http://localhost:5002`

## API Endpoints

### List Todos
```
GET /api/todos
```
Query params: `completed`, `priority`, `search`

### Get Single Todo
```
GET /api/todos/<id>
```

### Create Todo
```
POST /api/todos
Content-Type: application/json

{
    "title": "My todo",
    "description": "Optional description",
    "priority": "medium"  // low, medium, high
}
```

### Update Todo
```
PUT /api/todos/<id>
Content-Type: application/json

{
    "title": "Updated title",
    "completed": true,
    "priority": "high"
}
```

### Delete Todo
```
DELETE /api/todos/<id>
```

### Get Statistics
```
GET /api/todos/stats
```

### Complete All Todos
```
POST /api/todos/complete-all
```

### Clear Completed Todos
```
DELETE /api/todos/clear-completed
```

## Response Format

All responses follow this structure:

```json
{
    "success": true,
    "data": { ... },
    "message": "optional message"
}
```

On error:
```json
{
    "success": false,
    "error": "Error message"
}
```

## Todo Fields

| Field | Type | Description |
|-------|------|-------------|
| id | integer | Unique identifier |
| title | string | Todo title (required) |
| description | string | Optional description |
| completed | boolean | Completion status |
| priority | string | low, medium, or high |
| created_at | timestamp | Creation time |
| updated_at | timestamp | Last update time |

## Example Usage with cURL

```bash
# Create a todo
curl -X POST http://localhost:5002/api/todos \
  -H "Content-Type: application/json" \
  -d '{"title": "Learn Flask", "priority": "high"}'

# Get all todos
curl http://localhost:5002/api/todos

# Mark as completed
curl -X PUT http://localhost:5002/api/todos/1 \
  -H "Content-Type: application/json" \
  -d '{"completed": true}'

# Delete a todo
curl -X DELETE http://localhost:5002/api/todos/1

# Get stats
curl http://localhost:5002/api/todos/stats
```

## Database

SQLite database (`todos.db`) is automatically created on first run.

## License

MIT License
