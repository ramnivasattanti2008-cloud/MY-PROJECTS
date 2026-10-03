# Chat Room

A real-time multi-room chat application built with Flask-SocketIO and React.

## Features

- Multiple chat rooms (general, tech, random, help)
- Real-time messaging via WebSockets
- User join/leave notifications
- Create custom rooms
- Message history persistence
- Dark theme UI

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

The server runs on `http://localhost:5001`

### Frontend

```bash
cd frontend
npm install
npm start
```

The app runs on `http://localhost:3000`

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/rooms` | List all rooms |
| POST | `/api/rooms` | Create a new room |
| GET | `/api/messages/<room>` | Get messages for a room |
| WS | `message` | Send/receive chat messages |
| WS | `join` | Join a room |
| WS | `leave` | Leave a room |

## WebSocket Events

- `connect` - Client connects
- `disconnect` - Client disconnects
- `join` - Join a room with `{ username, room }`
- `leave` - Leave a room with `{ username, room }`
- `message` - Send/receive message `{ username, content, room }`
