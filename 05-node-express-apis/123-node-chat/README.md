# Real-time Chat

A real-time chat application built with Express.js and Socket.IO.

## Features

- Real-time messaging with Socket.IO
- Multiple chat rooms (general, random, tech)
- User presence (join/leave notifications)
- Typing indicators
- Chat history (last 100 messages per room)
- Online user count
- Clean, responsive UI

## Installation

```bash
npm install
```

## Usage

```bash
npm start
```

The server will start on http://localhost:3003

## Features

### Rooms
- Pre-configured rooms: general, random, tech
- Switch between rooms instantly
- See user count per room

### Real-time Updates
- Instant message delivery
- Typing indicators
- User join/leave notifications
- Online user count

### Chat History
- Messages persist in memory (last 100 per room)
- History loads when joining a room

## API Endpoints

### Get Rooms
```bash
GET /api/rooms
```

### Health Check
```bash
GET /api/health
```

## WebSocket Events

### Client to Server

| Event | Data | Description |
|-------|------|-------------|
| `join` | `{ username, room }` | Join a chat room |
| `chat message` | `{ message, room }` | Send a message |
| `typing` | - | User is typing |
| `stop typing` | - | User stopped typing |
| `switch room` | `room` | Switch to another room |

### Server to Client

| Event | Data | Description |
|-------|------|-------------|
| `chat message` | `{ id, username, message, room, timestamp }` | New message |
| `chat history` | `{ room, messages[] }` | Room history |
| `user joined` | `{ username, room, users }` | User joined |
| `user left` | `{ username, room }` | User left |
| `user typing` | `{ username }` | User typing |
| `user stopped typing` | `{ username }` | User stopped |
| `room list` | `string[]` | All rooms |

## Example Usage

1. Open http://localhost:3003 in two browser tabs
2. Enter different usernames in each tab
3. Start chatting in real-time!
4. Switch between rooms using the sidebar
