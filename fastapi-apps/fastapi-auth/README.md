# FastAPI Authentication API

A complete Authentication API built with FastAPI, featuring JWT tokens, protected routes, and role-based access control.

## Features

- User registration with email validation
- User login with JWT token authentication
- Protected routes requiring authentication
- Role-based access control (user, admin)
- Password hashing with bcrypt
- User profile management
- Protected posts (CRUD)
- Admin-only routes

## Installation

```bash
cd fastapi-auth
pip install -r requirements.txt
```

## Running the API

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Authentication

This API uses OAuth2 with Password flow and JWT Bearer tokens.

1. Register a new user
2. Login to get an access token
3. Include the token in all protected requests:
   ```
   Authorization: Bearer <your-token-here>
   ```

## API Endpoints

### Authentication

```bash
# Register a new user
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "username": "johndoe",
    "password": "secret123",
    "full_name": "John Doe"
  }'

# Login and get access token
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=johndoe&password=secret123"

# Get current user info (requires auth)
curl http://localhost:8000/auth/me \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"

# Update current user profile
curl -X PUT "http://localhost:8000/auth/me" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{"full_name": "John Updated", "bio": "I am a developer"}'
```

### Protected Posts

```bash
# Create a post (requires auth)
curl -X POST "http://localhost:8000/posts" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My First Post",
    "content": "This is the content of my post",
    "published": true
  }'

# Get all posts (requires auth)
curl http://localhost:8000/posts \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"

# Get only your posts (requires auth)
curl "http://localhost:8000/posts?mine=true" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"

# Get single post
curl http://localhost:8000/posts/1 \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"

# Delete a post (owner or admin only)
curl -X DELETE "http://localhost:8000/posts/1" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### Admin Routes

```bash
# Get all users (admin only)
curl http://localhost:8000/admin/users \
  -H "Authorization: Bearer ADMIN_TOKEN_HERE"
```

## Data Models

### User
| Field | Type | Description |
|-------|------|-------------|
| id | int | Unique identifier |
| email | string | User email (unique) |
| username | string | Username (unique) |
| hashed_password | string | Bcrypt hashed password |
| full_name | string | Display name |
| bio | string | User biography |
| is_active | boolean | Account active status |
| is_verified | boolean | Email verified status |
| role | string | Role: user, admin |
| created_at | datetime | Registration timestamp |

### Token Response
| Field | Type | Description |
|-------|------|-------------|
| access_token | string | JWT token |
| token_type | string | Always "bearer" |

### Post
| Field | Type | Description |
|-------|------|-------------|
| id | int | Unique identifier |
| title | string | Post title |
| content | string | Post content |
| user_id | int | Author's user ID |
| published | boolean | Publication status |
| created_at | datetime | Creation timestamp |

## Roles

| Role | Permissions |
|------|-------------|
| user | Create posts, edit/delete own posts |
| admin | All user permissions + view all users |

## Security Notes

- Passwords are hashed using bcrypt
- JWT tokens expire after 30 minutes
- In production, change `SECRET_KEY` to a secure random value
- The database file `auth.db` is created automatically

## Project Structure

```
fastapi-auth/
├── main.py           # Main application code
├── requirements.txt  # Python dependencies
├── README.md         # This file
└── auth.db           # SQLite database (created on first run)
```

## License

MIT
