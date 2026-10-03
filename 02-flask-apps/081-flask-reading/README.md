# Reading List Tracker

A Flask application to track your reading progress across books.

## Features

- Track books in three states: To Read, Currently Reading, Completed
- Add books with title, author, and genre
- Quick status updates with one-click buttons
- Filter by reading status and genre
- Search by title or author
- View reading statistics

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python app.py
```

Open http://127.0.0.1:5000 in your browser.

## How to Use

1. Click "Add Book" to add a book to your list
2. Set the initial status (To Read, Reading, or Completed)
3. Use quick buttons to update status as you progress
4. Filter by status tabs to see specific books
5. Search or filter by genre to find books

## Status Workflow

- **To Read**: Books on your wishlist
- **Reading**: Books you're currently reading (set start date)
- **Completed**: Finished books (set finish date)
