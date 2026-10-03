# Flask Bookmarks App

A bookmark manager with tags and search functionality.

## Features

- Save bookmarks with URL, title, and description
- Tag-based organization
- Search by title, description, or URL
- Filter by tag
- Edit and delete bookmarks
- Auto-favicon fetching

## Setup

```bash
cd flask-bookmarks
pip install -r requirements.txt
python app.py
```

## Run

Visit http://localhost:5002

## Routes

- `/` - List all bookmarks (supports `?search=` and `?tag=` filters)
- `/add` - Add a new bookmark
- `/edit/<id>` - Edit a bookmark
- `/delete/<id>` - Delete a bookmark
