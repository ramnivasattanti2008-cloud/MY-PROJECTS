# URL Shortener

A Flask-based URL shortener with SQLite database, click tracking, and analytics.

## Features

- Create short URLs with custom codes
- Click tracking and statistics
- Analytics dashboard
- RESTful API
- Dark-themed UI

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python app.py
```

The app will run on `http://localhost:5001`

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/shorten` | Create a short URL |
| GET | `/<short_code>` | Redirect to original URL |
| GET | `/api/urls` | List all URLs |
| GET | `/api/urls/<short_code>` | Get URL details |
| DELETE | `/api/urls/<short_code>` | Delete a URL |
| GET | `/analytics` | View analytics dashboard |

## API Examples

```bash
# Create short URL
curl -X POST http://localhost:5001/shorten \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com/very/long/path"}'

# Create with custom code
curl -X POST http://localhost:5001/shorten \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com", "custom_code": "my-link"}'

# List all URLs
curl http://localhost:5001/api/urls

# Delete URL
curl -X DELETE http://localhost:5001/api/urls/abc123
```

## Database

SQLite database is automatically created on first run. Database file: `urlshortener.db`
