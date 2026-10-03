# Flask Poll App

A simple polling application built with Flask and SQLite.

## Features

- Create polls with multiple options
- Vote on active polls
- View real-time results with percentages
- Delete polls
- Responsive design

## Setup

```bash
cd flask-poll
pip install -r requirements.txt
python app.py
```

## Run

Visit http://localhost:5001

## Routes

- `/` - List all polls
- `/create` - Create a new poll
- `/poll/<id>` - Vote on a poll
- `/poll/<id>/results` - View poll results
- `/poll/<id>/delete` - Delete a poll
