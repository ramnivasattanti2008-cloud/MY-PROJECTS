# REST Client CLI

A command-line HTTP client for making API requests with formatted JSON output.

## Features

- Support for GET, POST, PUT, PATCH, DELETE, HEAD methods
- Custom headers via `-H` flag
- JSON body support with `-d` flag
- Read body from file with `@filename`
- Verbose mode for response headers
- Save response to file with `-o` flag
- Color-coded status indicators
- Timing information

## Installation

```bash
# Make executable
chmod +x rest-client.py

# Optional: Add to PATH
sudo ln -s rest-client.py /usr/local/bin/rest
```

## Usage

```bash
# Basic GET request
python rest-client.py GET https://api.example.com/users

# POST with JSON body
python rest-client.py POST https://api.example.com/users \
  -d '{"name": "John", "email": "john@example.com"}'

# PUT with headers
python rest-client.py PUT https://api.example.com/users/1 \
  -H "Authorization: Bearer your-token" \
  -H "Content-Type: application/json" \
  -d '{"name": "Jane"}'

# DELETE request
python rest-client.py DELETE https://api.example.com/users/1

# Read body from file
python rest-client.py POST https://api.example.com/batch \
  -d @request.json

# Save response to file
python rest-client.py GET https://api.example.com/data -o output.json

# Verbose mode (show headers)
python rest-client.py GET https://api.example.com/users -v
```

## Options

| Flag | Description |
|------|-------------|
| `-d, --data` | Request body (JSON string or `@filename`) |
| `-H, --header` | Custom header (can be used multiple times) |
| `-v, --verbose` | Show response headers |
| `-o, --output` | Save response body to file |

## Exit Codes

- `0` - Success (status code < 400)
- `1` - Error (status code >= 400 or connection failure)
