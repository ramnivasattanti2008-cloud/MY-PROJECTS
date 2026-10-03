# Todo API

A RESTful Todo API with JWT authentication built with Express.js and SQLite.

## Features

- User registration and login with JWT
- CRUD operations for todos
- Priority levels (low, medium, high)
- Mark todos as complete/incomplete
- Filter todos by status and priority

## Installation

```bash
npm install
```

## Usage

```bash
npm start
```

The server will start on http://localhost:3002

## API Endpoints

### Authentication

#### Register
```bash
POST /api/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}
```

#### Login
```bash
POST /api/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}
```

### Todos (requires JWT token)

Add the header: `Authorization: Bearer <your-token>`

#### Create Todo
```bash
POST /api/todos
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "Complete project",
  "description": "Finish the API documentation",
  "priority": "high"
}
```

#### Get All Todos
```bash
GET /api/todos
Authorization: Bearer <token>

# Filter by status
GET /api/todos?completed=true
GET /api/todos?completed=false

# Filter by priority
GET /api/todos?priority=high
```

#### Get Single Todo
```bash
GET /api/todos/:id
Authorization: Bearer <token>
```

#### Update Todo
```bash
PUT /api/todos/:id
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "Updated title",
  "completed": true,
  "priority": "low"
}
```

#### Delete Todo
```bash
DELETE /api/todos/:id
Authorization: Bearer <token>
```

#### Toggle Completion
```bash
PATCH /api/todos/:id/toggle
Authorization: Bearer <token>
```

## Example with cURL

```bash
# Register
curl -X POST http://localhost:3002/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "secret123"}'

# Login
curl -X POST http://localhost:3002/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "secret123"}'

# Create todo (use token from login response)
curl -X POST http://localhost:3002/api/todos \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <your-token>" \
  -d '{"title": "Learn Node.js", "priority": "high"}'

# Get all todos
curl http://localhost:3002/api/todos \
  -H "Authorization: Bearer <your-token>"
```

## Environment Variables

- `JWT_SECRET` - Secret key for JWT signing (default: your-secret-key-change-in-production)
- `PORT` - Server port (default: 3002)
