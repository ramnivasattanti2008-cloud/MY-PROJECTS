# Simple Proxy API

A Flask API that proxies requests to external APIs, helping you avoid CORS issues when building front-end applications.

## Features

- GitHub API proxy
- Open-Meteo Weather API proxy
- JSONPlaceholder API proxy (for testing)
- Generic URL proxy
- Request/response passthrough

## Installation

```bash
pip install -r requirements.txt
```

## Running the Server

```bash
python app.py
```

The API will be available at `http://localhost:5000`

## Configuration

### Environment Variables (Optional)

- `GITHUB_TOKEN` - GitHub personal access token for authenticated requests
- `UNSPLASH_ACCESS_KEY` - Unsplash API access key

## API Endpoints

### Health Check
```bash
curl http://localhost:5000/health
```

### GitHub API Proxy

```bash
# Get GitHub user info
curl http://localhost:5000/proxy/github/users/octocat

# Get repository info
curl http://localhost:5000/proxy/github/repos/torvalds/linux

# Search repositories
curl "http://localhost:5000/proxy/github/search/repositories?q=python"

# With authentication (set GITHUB_TOKEN env var)
# curl http://localhost:5000/proxy/github/user
```

### Weather API Proxy

```bash
# Get current weather for a location
curl "http://localhost:5000/proxy/weather?latitude=40.7128&longitude=-74.0060"

# Request hourly temperature
curl "http://localhost:5000/proxy/weather?latitude=40.7128&longitude=-74.0060&hourly=temperature_2m"
```

### JSONPlaceholder Proxy (Testing)

```bash
# Get all posts
curl http://localhost:5000/proxy/jsonplaceholder/posts

# Get single post
curl http://localhost:5000/proxy/jsonplaceholder/posts/1

# Get comments for a post
curl http://localhost:5000/proxy/jsonplaceholder/posts/1/comments

# Get all users
curl http://localhost:5000/proxy/jsonplaceholder/users
```

### Generic Proxy

```bash
# Proxy any URL
curl "http://localhost:5000/proxy/https://api.github.com/zen"

# With query parameters
curl "http://localhost:5000/proxy/https://httpbin.org/get?test=123"
```

## Response Format

All responses include metadata about the proxied request:

```json
{
  "success": true,
  "proxied_from": "https://api.github.com",
  "endpoint": "/users/octocat",
  "status_code": 200,
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

## Use Cases

### Frontend Development
When building a front-end app that needs to call APIs that don't support CORS:

```javascript
// Instead of calling the API directly (CORS error)
fetch('https://api.github.com/users/octocat')

// Call through the proxy
fetch('http://localhost:5000/proxy/github/users/octocat')
```

### API Key Protection
Use the proxy to hide API keys from the client:

```bash
# Set your GitHub token
export GITHUB_TOKEN=ghp_your_token_here

# Now authenticated requests work
curl http://localhost:5000/proxy/github/user
```

### Rate Limiting Bypass
Route requests through different instances to bypass rate limits.

## Security Notes

- The generic proxy should be used carefully in production
- Consider adding authentication to the proxy in production
- Rate limiting may be needed for public deployments
