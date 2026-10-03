# Task Manager

A Flask app to track tasks with priorities and due dates.

## Setup

```bash
cd flask-tasks
pip install -r requirements.txt
python app.py
```

Open http://localhost:5003

## Features

- Create, edit, delete tasks
- Set priority (Low, Medium, High)
- Set due dates with overdue detection
- Mark tasks as complete/incomplete
- Filter by status (All, Active, Completed)

## Database

SQLite (tasks.db) - auto-created on first run.
