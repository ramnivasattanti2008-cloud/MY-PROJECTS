# URL Shortener API

Express API for creating short URLs and tracking visits.

## Quick Start

```bash
npm install
npm start
```

API runs at `http://localhost:3004`

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /urls | Create short URL |
| GET | /urls | List all URLs |
| GET | /urls/:shortCode | Get URL info |
| DELETE | /urls/:shortCode | Delete URL |
| GET | /urls/:shortCode/clicks | Get click statistics |
| GET | /:shortCode | Redirect to original URL |

## Examples

```bash
# Create short URL (auto-generated code)
curl -X POST http://localhost:3004/urls \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.example.com/very/long/path"}'

# Create short URL (custom code)
curl -X POST http://localhost:3004/urls \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.example.com", "customCode": "mylink"}'

# Create with title
curl -X POST http://localhost:3004/urls \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.example.com", "title": "Example Site"}'

# List all URLs
curl http://localhost:3004/urls

# Get URL info with recent visits
curl http://localhost:3004/urls/abc123

# Get click statistics
curl http://localhost:3004/urls/abc123/clicks

# Delete URL
curl -X DELETE http://localhost:3004/urls/abc123

# Redirect (returns 302)
curl -v http://localhost:3004/abc123
```

## Response Format

```json
{
  "success": true,
  "data": {
    "id": 1,
    "shortCode": "abc123",
    "shortUrl": "http://localhost:3004/abc123",
    "originalUrl": "https://www.example.com",
    "title": "Example Site",
    "visitCount": 42
  }
}
```

## Click Statistics

```json
{
  "success": true,
  "data": {
    "totalClicks": 100,
    "clicksByDay": [
      { "date": "2024-01-15", "clicks": 12 }
    ],
    "topReferers": [
      { "referer": "https://twitter.com", "count": 45 }
    ],
    "lastVisited": "2024-01-15T10:30:00Z"
  }
}
```

## Features

- Auto-generated short codes (6 characters)
- Custom short codes supported
- Visit tracking with referrer, user agent, timestamp
- Click statistics by day
- Top referrers

## Data Storage

Data stored in `urls.db` (SQLite).
