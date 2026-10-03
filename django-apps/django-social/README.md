# Django Social

A social networking application with user profiles and follow system.

## Features

- User registration and profiles
- Profile pictures
- Create and view posts
- Follow/unfollow users
- User timeline and feed

## Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

## Usage

1. Register and login
2. Edit your profile
3. Create posts
4. Follow other users
5. View your feed with posts from people you follow
