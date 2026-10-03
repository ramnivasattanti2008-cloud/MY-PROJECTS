# Bookmark Manager

A Flask application to save, organize, and search bookmarks with tags and notes.

## Features

- Save bookmarks with title, URL, description, tags, and notes
- Search bookmarks by title, description, or notes
- Filter bookmarks by tags
- Sort by newest, oldest, title, or most visited
- Track visit counts
- Export bookmarks to text file
- Dark theme interface

## Installation

```bash
cd bookmarks-app
pip install -r requirements.txt
python app.py
```

## Usage

1. Open `http://localhost:5000`
2. Add bookmarks with tags for organization
3. Search and filter to find bookmarks quickly
4. Click any bookmark to visit it (counts as a visit)
5. Export your bookmarks anytime

## Database

SQLite database (`bookmarks.db`) created automatically.
Sample bookmarks are added on first run.

## Project Structure

```
bookmarks-app/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── templates/          # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── add_bookmark.html
│   └── edit_bookmark.html
└── README.md
```
