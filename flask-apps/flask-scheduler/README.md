# Flask Task Scheduler

A simple task scheduling application built with Flask and SQLite.

## Features

- Create, read, update, and delete tasks
- Set due dates and priority levels
- Mark tasks as complete
- Filter tasks by status

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

- `/` - View all tasks
- `/add` - Add a new task
- `/edit/<id>` - Edit a task
- `/delete/<id>` - Delete a task
- `/complete/<id>` - Mark task as complete
