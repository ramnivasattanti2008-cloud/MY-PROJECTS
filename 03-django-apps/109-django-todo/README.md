# Django Todo

A task management application with user authentication.

## Features

- User registration and login
- CRUD operations for todos
- Priority levels (Low, Medium, High)
- Due dates
- Mark todos as complete

## Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Run development server
python manage.py runserver
```

## Usage

1. Register a new account or login
2. Create todos with priority and due dates
3. Mark todos complete when done
4. Filter by status or priority
