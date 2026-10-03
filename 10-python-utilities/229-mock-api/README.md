# Mock API Server

A Python Flask-based mock API server. Define endpoints in YAML and serve realistic mock responses. Perfect for frontend development and testing without a real backend.

## Features

- **YAML Configuration**: Define all endpoints in a single YAML file
- **Dynamic Responses**: Generate random data, UUIDs, emails, dates
- **Response Templates**: Use template syntax for dynamic values
- **Configurable Delays**: Simulate network latency
- **Custom Status Codes**: Return error responses for testing
- **CORS Support**: Built-in CORS headers
- **No External Dependencies**: Uses Python's built-in HTTP server

## Installation

```bash
# Install optional YAML support
pip install pyyaml

# Or use requirements.txt
pip install -r requirements.txt
```

## Quick Start

```bash
# Create a sample configuration
python mock-api.py --init

# Run the server
python mock-api.py -c mock-config.yaml

# Or use defaults (built-in sample config)
python mock-api.py
```

## Configuration Format

Create a `mock-config.yaml` file:

```yaml
name: My Mock API
port: 8080
host: localhost
base_path: /api/v1

variables:
  api_version: "1.0.0"

routes:
  # GET endpoint
  - path: /users
    method: GET
    description: List all users
    response:
      users:
        - id: 1
          name: John Doe
          email: john@example.com
        - id: 2
          name: Jane Smith
          email: jane@example.com
      total: 2

  # Dynamic response with template syntax
  - path: /users/{id}
    method: GET
    description: Get user by ID
    response:
      id: "{{increment}}"
      name: "{{name}}"
      email: "{{email}}"
      created_at: "{{datetime}}"

  # POST endpoint with delay
  - path: /users
    method: POST
    description: Create user
    status: 201
    delay: 500  # ms
    response:
      id: 3
      message: User created successfully

  # Error response
  - path: /protected
    method: GET
    status: 401
    response:
      error: Unauthorized
      message: Please log in to access this resource
```

## Dynamic Values

Use `{{type}}` syntax in your responses:

| Type | Description | Example |
|------|-------------|---------|
| `{{uuid}}` | Random UUID | `a1b2c3d4-e5f6-7890-abcd-ef1234567890` |
| `{{increment}}` | Auto-increment number | `1`, `2`, `3` |
| `{{random}}` | Random integer | `42` |
| `{{random_float}}` | Random float | `3.14` |
| `{{boolean}}` | Random boolean | `true` |
| `{{name}}` | Random full name | `John Smith` |
| `{{email}}` | Random email | `user123@example.com` |
| `{{lorem words=5}}` | Lorem ipsum text | `lorem ipsum dolor sit amet` |
| `{{date}}` | Current date | `2024-01-15` |
| `{{datetime}}` | Current datetime | `2024-01-15T10:30:00` |
| `{{datetime offset_days=-7}}` | Date with offset | `2024-01-08T10:30:00` |
| `{{url}}` | Random URL | `https://api.example.com/posts/42` |
| `{{image_url}}` | Random image URL | `https://picsum.photos/640/480` |
| `{{choice:cat,dog,bird}}` | Random choice | `cat` |

## Usage

```bash
# Run with config file
python mock-api.py -c my-config.yaml

# Custom port
python mock-api.py -c my-config.yaml -p 3000

# Custom host
python mock-api.py -c my-config.yaml --host 0.0.0.0

# List endpoints
python mock-api.py -c my-config.yaml -l

# Use built-in sample config
python mock-api.py

# Generate sample config
python mock-api.py --init
```

## API Endpoints

### Request

```
GET /api/v1/users
POST /api/v1/users
GET /api/v1/users/{id}
PUT /api/v1/users/{id}
DELETE /api/v1/users/{id}
```

### Response Headers

All responses include:
```
Content-Type: application/json
X-Powered-By: MockAPI
Access-Control-Allow-Origin: *
```

### Status Codes

Configure custom status codes per endpoint:
- `200` - OK (default)
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `500` - Internal Server Error

## Testing with curl

```bash
# Get all users
curl http://localhost:8080/api/v1/users

# Get single user
curl http://localhost:8080/api/v1/users/1

# Create user
curl -X POST http://localhost:8080/api/v1/users \
  -H "Content-Type: application/json" \
  -d '{"name": "New User", "email": "new@example.com"}'

# Update user
curl -X PUT http://localhost:8080/api/v1/users/1 \
  -H "Content-Type: application/json" \
  -d '{"name": "Updated Name"}'

# Delete user
curl -X DELETE http://localhost:8080/api/v1/users/1
```

## Options

| Flag | Description |
|------|-------------|
| `-c, --config` | YAML configuration file |
| `-p, --port` | Server port (overrides config) |
| `--host` | Server host (overrides config) |
| `--init` | Create sample config file |
| `-l, --list` | List available endpoints |
