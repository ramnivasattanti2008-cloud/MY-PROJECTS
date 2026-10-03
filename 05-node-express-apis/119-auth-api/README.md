# Auth API

A secure authentication API with JWT tokens and bcrypt password hashing.

## Quick Start

```bash
npm install
npm start
```

API runs at `http://localhost:3001`

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /auth/register | Register new user |
| POST | /auth/login | Login user |
| POST | /auth/logout | Logout user |
| GET | /auth/me | Get current user |
| GET | /health | Health check |

## Examples

```bash
# Register new user
curl -X POST http://localhost:3001/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "secret123", "name": "John"}'

# Login
curl -X POST http://localhost:3001/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "secret123"}'

# Get current user (requires token)
curl http://localhost:3001/auth/me \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"

# Logout
curl -X POST http://localhost:3001/auth/logout \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## Authentication

Protected endpoints require a JWT token in the Authorization header:

```
Authorization: Bearer <token>
```

Token expires after 7 days.

## Response Format

```json
{
  "success": true,
  "message": "Login successful",
  "data": {
    "token": "eyJhbGci...",
    "user": { "id": 1, "email": "user@example.com", "name": "John" }
  }
}
```

## Security Features

- Passwords hashed with bcrypt (10 salt rounds)
- JWT tokens with 7-day expiration
- Session tracking in SQLite
- Automatic cleanup of expired sessions

## Data Storage

User data stored in `auth.db` (SQLite).
