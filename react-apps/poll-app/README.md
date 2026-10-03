# Poll App

A live polling application with real-time result updates. Create polls, vote, and watch results update instantly.

## Features

- Create polls with multiple options
- Vote on polls (one vote per user)
- Real-time result updates via WebSockets
- Close polls
- Vote percentage bars
- Dark-themed UI with live updates

## Tech Stack

- **Backend**: Flask, Flask-SocketIO, Flask-CORS, SQLite
- **Frontend**: React, TypeScript, Socket.IO Client
- **Database**: SQLite (auto-created)

## Setup

### Backend

```bash
cd backend
pip install -r requirements.txt
python app.py
```

The server runs on `http://localhost:5002`

### Frontend

```bash
cd frontend
npm install
npm start
```

The app runs on `http://localhost:3001`

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/polls` | List all polls |
| POST | `/api/polls` | Create a poll |
| GET | `/api/polls/<id>` | Get poll details |
| POST | `/api/polls/<id>/vote` | Vote on a poll |
| POST | `/api/polls/<id>/close` | Close a poll |

## WebSocket Events

- `poll_created` - New poll created
- `poll_updated` - Poll vote count changed
- `poll_closed` - Poll was closed
- `join_poll` - Subscribe to poll updates
- `leave_poll` - Unsubscribe from poll updates
