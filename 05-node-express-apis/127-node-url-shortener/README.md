# URL Shortener

A simple Express.js URL shortener with SQLite database.

## Features

- Create short URLs with auto-generated IDs
- Track click counts
- View URL statistics
- Delete URLs
- List all shortened URLs

## Installation

```bash
npm install
```

## Usage

```bash
npm start
```

The server will start on http://localhost:3000

## API Endpoints

### Create Short URL
```bash
POST /api/shorten
Content-Type: application/json

{ "url": "https://example.com" }
```

### Redirect
```
GET /:id
```
Opens the original URL and increments click count.

### Get URL Stats
```bash
GET /api/urls/:id
```

### List All URLs
```bash
GET /api/urls
```

### Delete URL
```bash
DELETE /api/urls/:id
```

## Example

```bash
# Create a short URL
curl -X POST http://localhost:3000/api/shorten \
  -H "Content-Type: application/json" \
  -d '{"url": "https://github.com"}'

# Response
{
  "id": "abc12345",
  "short_url": "http://localhost:3000/abc12345",
  "original_url": "https://github.com"
}

# Visit the short URL
curl http://localhost:3000/abc12345
```
