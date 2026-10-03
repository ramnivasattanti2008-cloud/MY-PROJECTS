# Flask Auth Template

Authentication template with login, register, logout, and session management.

## Setup

```bash
cd flask-auth
pip install -r requirements.txt
python app.py
```

## Features

- User registration with password hashing
- Login with session management
- Protected routes
- SQLite database
- Flash messages
- Dashboard for authenticated users

## Routes

- `/` - Home (redirects based on auth status)
- `/register` - User registration
- `/login` - User login
- `/logout` - User logout
- `/dashboard` - Protected user dashboard

## Database

Uses SQLite (`users.db`). Schema auto-created on first run.
