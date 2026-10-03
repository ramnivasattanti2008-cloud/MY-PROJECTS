# Flask Simple Forum

A simple forum application with threads, replies, and categories.

## Features

- Multiple categories for organizing discussions
- Create new discussion threads
- Reply to threads
- View thread with all replies
- Clean, readable interface

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python app.py
```

Open http://localhost:5000 in your browser.

## Routes

- `/` - Home page with categories and recent threads
- `/category/<id>` - View threads in a category
- `/thread/<id>` - View thread with replies
- `/new-thread` - Create a new thread
- `/reply/<id>` - Post a reply to a thread
- `/delete-thread/<id>` - Delete a thread

## Default Categories

The forum comes with 4 default categories:
- General - General discussion topics
- Help - Get help with any topic
- Ideas - Share your ideas and suggestions
- Announcements - Official announcements
