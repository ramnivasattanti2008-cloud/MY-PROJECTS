# Python HTTP Web Server

A simple HTTP web server built entirely with Python's built-in `http.server` module. No external dependencies required!

## Features

- Static file serving from `/static` directory
- JSON REST API endpoints
- GET and POST request handling
- CORS support for API endpoints
- Interactive web interface for testing

## Running the Server

```bash
# Run with default port (8000)
python server.py

# Run on custom port
python server.py --port 3000
```

## API Endpoints

### Health Check
```bash
curl http://localhost:8000/api/health
```

### Users API
```bash
# List all users
curl http://localhost:8000/api/users

# Get user by ID
curl http://localhost:8000/api/users/1

# Create new user
curl -X POST http://localhost:8000/api/users \
  -H "Content-Type: application/json" \
  -d '{"name": "John", "email": "john@example.com"}'
```

### Posts API
```bash
# List all posts
curl http://localhost:8000/api/posts

# Get post by ID
curl http://localhost:8000/api/posts/1

# Create new post
curl -X POST http://localhost:8000/api/posts \
  -H "Content-Type: application/json" \
  -d '{"title": "My Post", "author": "John", "content": "Hello world!"}'
```

### Server Info
```bash
curl http://localhost:8000/api/info
```

## Static Files

Place any static files (HTML, CSS, JS, images) in the `static/` directory. They will be served at:
- `/` or `/index.html` - Main HTML page
- `/static/<filename>` - Other static files

## Project Structure

```
web-server/
├── server.py          # Main server with routing
├── static/
│   └── index.html     # Interactive demo page
├── requirements.txt   # No external dependencies
└── README.md
```

## Requirements

- Python 3.6+
- No external packages needed (uses built-in modules only)
