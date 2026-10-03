# Notes API

A RESTful API for managing notes with CRUD operations, search, and categories.

## Quick Start

```bash
npm install
npm start
```

API runs at `http://localhost:3000`

## Endpoints

### Notes

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /notes | List all notes |
| GET | /notes/:id | Get single note |
| POST | /notes | Create note |
| PUT | /notes/:id | Update note |
| DELETE | /notes/:id | Delete note |
| GET | /categories | List categories |

### Query Parameters

- `search` - Search in title/content
- `category` - Filter by category
- `sort` - `newest` (default) or `oldest`

## Examples

```bash
# Create a note
curl -X POST http://localhost:3000/notes \
  -H "Content-Type: application/json" \
  -d '{"title": "Meeting Notes", "content": "Discuss Q4 goals", "category": "work"}'

# List all notes
curl http://localhost:3000/notes

# Search notes
curl "http://localhost:3000/notes?search=meeting"

# Filter by category
curl "http://localhost:3000/notes?category=work"

# Get single note
curl http://localhost:3000/notes/<id>

# Update note
curl -X PUT http://localhost:3000/notes/<id> \
  -H "Content-Type: application/json" \
  -d '{"title": "Updated Title", "content": "Updated content"}'

# Delete note
curl -X DELETE http://localhost:3000/notes/<id>

# List categories
curl http://localhost:3000/categories
```

## Response Format

```json
{
  "success": true,
  "data": [...],
  "count": 10
}
```

## Data Storage

Notes are stored in `notes.json` in the project directory.
