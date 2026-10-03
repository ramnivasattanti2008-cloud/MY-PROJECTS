# FastAPI Blog API

A complete Blog API built with FastAPI and SQLite, featuring posts, comments, categories, and pagination.

## Features

- Posts with full CRUD operations
- Comments system
- Categories/tags for posts
- Pagination for post listings
- Views counter
- Author filtering
- Auto-generated API documentation at `/docs`

## Installation

```bash
cd fastapi-blog
pip install -r requirements.txt
```

## Running the API

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### Categories

```bash
# Create a category
curl -X POST "http://localhost:8000/categories" \
  -H "Content-Type: application/json" \
  -d '{"name": "Technology", "description": "Tech related posts"}'

# Get all categories
curl http://localhost:8000/categories

# Get single category
curl http://localhost:8000/categories/1

# Delete category
curl -X DELETE "http://localhost:8000/categories/1"
```

### Posts

```bash
# Create a post
curl -X POST "http://localhost:8000/posts" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My First Blog Post",
    "content": "This is the content of my first blog post.",
    "author": "John Doe",
    "category_ids": [1],
    "published": true
  }'

# Get all posts (paginated)
curl "http://localhost:8000/posts"

# Get posts with filters
curl "http://localhost:8000/posts?page=1&per_page=5&author=John"
curl "http://localhost:8000/posts?category_id=1&published_only=true"

# Get single post (increments views)
curl http://localhost:8000/posts/1

# Update post
curl -X PUT "http://localhost:8000/posts/1" \
  -H "Content-Type: application/json" \
  -d '{"title": "Updated Title", "published": true}'

# Delete post
curl -X DELETE "http://localhost:8000/posts/1"
```

### Comments

```bash
# Add comment to post
curl -X POST "http://localhost:8000/posts/1/comments" \
  -H "Content-Type: application/json" \
  -d '{"author": "Jane Smith", "content": "Great post!"}'

# Get comments for a post
curl "http://localhost:8000/posts/1/comments"
curl "http://localhost:8000/posts/1/comments?approved_only=false"
```

## Data Models

### Category
| Field | Type | Description |
|-------|------|-------------|
| id | int | Unique identifier |
| name | string | Category name (unique) |
| slug | string | URL-friendly slug (auto-generated) |
| description | string | Category description |
| created_at | datetime | Creation timestamp |

### Post
| Field | Type | Description |
|-------|------|-------------|
| id | int | Unique identifier |
| title | string | Post title |
| slug | string | URL-friendly slug (auto-generated) |
| content | string | Post content (full text) |
| author | string | Author name |
| published | boolean | Publication status |
| views | int | View counter |
| categories | array | List of categories |
| created_at | datetime | Creation timestamp |
| updated_at | datetime | Last update timestamp |

### Comment
| Field | Type | Description |
|-------|------|-------------|
| id | int | Unique identifier |
| post_id | int | Parent post ID |
| author | string | Comment author |
| content | string | Comment text |
| approved | boolean | Moderation status |
| created_at | datetime | Creation timestamp |

## Pagination Response

```json
{
  "items": [...],
  "total": 42,
  "page": 1,
  "per_page": 10,
  "pages": 5
}
```

## Project Structure

```
fastapi-blog/
├── main.py           # Main application code
├── requirements.txt  # Python dependencies
├── README.md         # This file
└── blog.db           # SQLite database (created on first run)
```

## License

MIT
