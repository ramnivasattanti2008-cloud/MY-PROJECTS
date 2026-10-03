# Blog Site

A Flask-based blog with posts, comments, markdown support, and tags.

## Features

- Create and publish blog posts
- Markdown support with syntax highlighting
- Comments system
- Tag-based organization
- Search functionality
- Pagination
- Dark-themed UI

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python app.py
```

The app will run on `http://localhost:5004`

## Routes

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | List all posts |
| GET | `/post/<slug>` | View a post |
| GET | `/create` | Create post form |
| POST | `/create` | Create a new post |
| POST | `/post/<slug>/comment` | Add a comment |
| GET | `/api/posts` | List posts (JSON) |
| GET | `/api/posts/<slug>` | Get post (JSON) |
| DELETE | `/api/posts/<slug>` | Delete a post |
| GET | `/api/tags` | List all tags |

## API Examples

```bash
# Create a post (via form)
curl -X POST http://localhost:5004/create \
  -d "title=My First Post" \
  -d "author=John Doe" \
  -d "content=# Hello World

This is my first blog post with **markdown** support." \
  -d "tags=python, flask, tutorial"

# Add a comment
curl -X POST http://localhost:5004/post/my-first-post/comment \
  -H "Content-Type: application/json" \
  -d '{"author": "Jane", "content": "Great post!"}'

# Get all posts (JSON)
curl http://localhost:5004/api/posts

# Get all tags
curl http://localhost:5004/api/tags

# Delete a post
curl -X DELETE http://localhost:5004/api/posts/my-first-post
```

## Markdown Support

The blog supports Markdown with fenced code blocks and syntax highlighting:

```python
# Python code
def hello():
    print("Hello, World!")
```

```javascript
// JavaScript code
console.log("Hello, World!");
```

## Database

SQLite database is automatically created on first run. Database file: `blog.db`
