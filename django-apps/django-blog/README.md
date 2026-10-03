# Django Blog

A clean, minimal blog application built with Django.

## Features

- Posts with markdown support
- Categories for organizing posts
- Comments on posts
- Clean, readable URLs

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

1. Visit http://localhost:8000/admin to create categories
2. Create posts with markdown content
3. Readers can comment on posts
