# Proxy API

Express proxy service to bypass CORS restrictions when calling external APIs.

## Quick Start

```bash
npm install
npm start
```

API runs at `http://localhost:3002`

## Convenience Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/github/user/:username | Get GitHub user info |
| GET | /api/weather?lat=&lon= | Get current weather |
| GET | /routes | List all routes |

## Examples

```bash
# Get GitHub user
curl http://localhost:3002/api/github/user/torvalds

# Get weather (latitude, longitude)
curl "http://localhost:3002/api/weather?lat=40.7128&lon=-74.0060"

# List all proxy routes
curl http://localhost:3002/routes
```

## Generic Proxy Endpoints

Proxy any external API request:

### GitHub API
```bash
# Get user repos
curl http://localhost:3002/proxy/github/users/octocat/repos

# Get repo details
curl http://localhost:3002/proxy/github/repos/torvalds/linux
```

### Weather API (Open-Meteo)
```bash
# Forecast
curl "http://localhost:3002/proxy/weather/forecast?latitude=52.52&longitude=13.41"
```

### Nominatim (Geocoding)
```bash
# Search location
curl "http://localhost:3002/proxy/nominatim/search?q=London&format=json"
```

## Response Format

```json
{
  "success": true,
  "data": { ... },
  "status": 200
}
```

## Use Cases

- Bypass CORS in browser applications
- Hide API keys (add them server-side)
- Rate limiting external APIs
- Response caching

## Security

- 30-second timeout on proxied requests
- User-Agent header set to identify requests
- No request body forwarded for GET requests
