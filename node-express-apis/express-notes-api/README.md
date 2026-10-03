# Express.js Notes API

A RESTful notes API built with Express.js, storing notes in a JSON file.

## Features

- Full CRUD operations for notes
- JSON file-based storage
- Search functionality
- Tag support
- CORS enabled

## Installation

```bash
npm install
```

## Running the Server

```bash
npm start
```

Or for development with auto-reload:
```bash
npm run dev
```

The API will be available at `http://localhost:3000`

## API Endpoints

### Health Check
```bash
curl http://localhost:3000/health
```

### Create Note
```bash
# Create a simple note
curl -X POST http://localhost:3000/notes \
  -H "Content-Type: application/json" \
  -d '{"title": "Meeting Notes", "content": "Discuss project timeline"}'

# Create a note with tags
curl -X POST http://localhost:3000/notes \
  -H "Content-Type: application/json" \
  -d '{"title": "Shopping List", "content": "Milk, eggs, bread", "tags": ["personal", " errands"]}'
```

### Get All Notes
```bash
# Get all notes
curl http://localhost:3000/notes

# Search notes
curl "http://localhost:3000/notes?search=meeting"

# Filter by tag
curl "http://localhost:3000/notes?tag=personal"
```

### Get Single Note
```bash
curl http://localhost:3000/notes/{note-id}
```

### Update Note
```bash
curl -X PUT http://localhost:3000/notes/{note-id} \
  -H "Content-Type: application/json" \
  -d '{"title": "Updated Title", "content": "Updated content", "tags": ["updated"]}'
```

### Delete Note
```bash
curl -X DELETE http://localhost:3000/notes/{note-id}
```

### Get All Tags
```bash
curl http://localhost:3000/tags
```

## Response Format

All responses follow this format:
```json
{
  "success": true,
  "data": { ... }
}
```

Error responses:
```json
{
  "success": false,
  "error": "Error message"
}
```

## Note Schema

```json
{
  "id": "uuid-string",
  "title": "Note title",
  "content": "Note content",
  "tags": ["tag1", "tag2"],
  "createdAt": "2024-01-01T00:00:00.000Z",
  "updatedAt": "2024-01-01T00:00:00.000Z"
}
```

## Data Storage

Notes are stored in `notes.json` file in the project directory.
