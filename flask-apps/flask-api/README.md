# Flask REST API

REST API template with CRUD operations and JWT authentication ready.

## Setup

```bash
cd flask-api
pip install -r requirements.txt
python app.py
```

## Authentication

### Login
```bash
POST /api/auth/login
Content-Type: application/json

{"username": "admin", "password": "password"}
```

Response:
```json
{"token": "eyJhbGciOiJIUzI1..."}
```

## API Endpoints

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | / | No | API info |
| POST | /api/auth/login | No | Get JWT token |
| GET | /api/items | Yes | List all items |
| GET | /api/items/:id | Yes | Get item |
| POST | /api/items | Yes | Create item |
| PUT | /api/items/:id | Yes | Update item |
| DELETE | /api/items/:id | Yes | Delete item |

## Usage

Include JWT token in Authorization header:
```
Authorization: Bearer <token>
```

## Response Format

```json
{"success": true, "message": "Success", "data": {...}}
```
