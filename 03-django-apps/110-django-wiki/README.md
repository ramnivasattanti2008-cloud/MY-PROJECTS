# Django Wiki

A collaborative wiki application with markdown support and version history.

## Features

- Create and edit wiki pages
- Markdown content with preview
- Version history for all pages
- Restore previous versions
- Search pages by title
- Table of contents from headings

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

1. Create pages through the admin or via the create page link
2. Edit pages using markdown
3. View version history on any page
4. Restore previous versions if needed
5. Search for pages using the search feature
