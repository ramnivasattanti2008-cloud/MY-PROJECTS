# Express.js REST API

A simple Express.js REST API for managing posts with middleware examples, error handling, and pagination.

## Features

- Full CRUD operations for posts
- Middleware examples (logging, validation, CORS, helmet, morgan)
- Pagination and filtering
- Search functionality
- Tag management
- Statistics endpoint
- Comprehensive error handling

## Installation

```bash
npm install
```

## Running the Server

```bash
npm start
# or
node server.js

# Development mode with auto-reload
npm run dev
```

The server runs on `http://localhost:3000`

## API Endpoints

### Health Check
```bash
curl http://localhost:3000/
```

### Create Post
```bash
curl -X POST http://localhost:3000/api/posts \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My First Post",
    "content": "This is the content of my first blog post.",
    "author": "John Doe",
    "tags": ["javascript", "nodejs"]
  }'
```

### List Posts (with pagination)
```bash
# Get first page of posts
curl "http://localhost:3000/api/posts?page=1&pageSize=10"

# Filter by author
curl "http://localhost:3000/api/posts?author=John"

# Filter by tag
curl "http://localhost:3000/api/posts?tag=javascript"

# Search in title and content
curl "http://localhost:3000/api/posts?search=nodejs"
```

### Get Single Post
```bash
curl http://localhost:3000/api/posts/{post_id}
```

### Update Post (full update)
```bash
curl -X PUT http://localhost:3000/api/posts/{post_id} \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated Title",
    "content": "Updated content for the post.",
    "author": "Jane Doe",
    "tags": ["updated", "api"]
  }'
```

### Partial Update Post
```bash
curl -X PATCH http://localhost:3000/api/posts/{post_id} \
  -H "Content-Type: application/json" \
  -d '{"title": "Only updating the title"}'
```

### Delete Post
```bash
curl -X DELETE http://localhost:3000/api/posts/{post_id}
```

### Get All Tags
```bash
curl http://localhost:3000/api/tags
```

### Get Statistics
```bash
curl http://localhost:3000/api/stats
```

## Example Workflow

```bash
# Create a post
POST_RESPONSE=$(curl -s -X POST http://localhost:3000/api/posts \
  -H "Content-Type: application/json" \
  -d '{"title": "Test Post", "content": "Test content"}')

POST_ID=$(echo $POST_RESPONSE | jq -r '.id')

# Get the post
curl http://localhost:3000/api/posts/$POST_ID

# Update the post
curl -X PATCH http://localhost:3000/api/posts/$POST_ID \
  -H "Content-Type: application/json" \
  -d '{"title": "Updated Test Post"}'

# Delete the post
curl -X DELETE http://localhost:3000/api/posts/$POST_ID
```

## Middleware Stack

| Middleware | Purpose |
|------------|---------|
| helmet | Security headers |
| cors | Cross-origin resource sharing |
| morgan | HTTP request logging |
| express.json | JSON body parsing |

## Custom Middleware

- **Request Logger**: Logs method, path, and timestamp
- **validatePost**: Validates title and content fields
- **validateUUID**: Validates ID parameter format
- **errorHandler**: Centralized error handling

## Data Model

### Post
| Field | Type | Description |
|-------|------|-------------|
| id | string | UUID |
| title | string | Post title (required, max 200 chars) |
| content | string | Post content (required, max 10000 chars) |
| author | string | Author name (default: "anonymous") |
| tags | string[] | Array of tags (lowercase) |
| createdAt | string | ISO timestamp |
| updatedAt | string | ISO timestamp |

## Error Responses

```json
{
  "error": "Error message"
}
```

| Status | Meaning |
|--------|---------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request |
| 404 | Not Found |
| 500 | Server Error |

## License

MIT
