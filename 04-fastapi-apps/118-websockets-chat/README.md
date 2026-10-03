# WebSockets Chat Server

A simple real-time chat server using FastAPI WebSockets.

## Features

- Real-time messaging with WebSockets
- Multiple chat rooms
- Private messaging
- Message history
- User presence tracking
- Typing indicators
- Built-in HTML chat client

## Installation

```bash
pip install -r requirements.txt
```

## Running the Server

```bash
python server.py
```

The server runs on `http://localhost:8000`

## Testing

### Web Chat Client
Open `http://localhost:8000/client` in your browser for a simple chat interface.

### REST Endpoints

```bash
# Health check
curl http://localhost:8000/

# List active rooms
curl http://localhost:8000/rooms

# Get room history
curl http://localhost:8000/rooms/{room_id}/history
```

## WebSocket Connection

Connect to `ws://localhost:8000/ws?username={username}&room_id={room_id}`

### JavaScript Client Example

```javascript
const username = "Alice";
const roomId = "general";

const ws = new WebSocket(`ws://localhost:8000/ws?username=${encodeURIComponent(username)}&room_id=${encodeURIComponent(roomId)}`);

ws.onopen = () => {
    console.log("Connected to chat server");
};

ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    console.log("Received:", data);

    if (data.type === "message") {
        console.log(`${data.username}: ${data.content}`);
    } else if (data.type === "system") {
        console.log("System:", data.message);
    } else if (data.type === "joined") {
        console.log("Joined room with", data.users);
    }
};

// Send public message
ws.send(JSON.stringify({
    type: "message",
    content: "Hello, everyone!"
}));

// Send private message
ws.send(JSON.stringify({
    type: "private",
    to_user_id: "recipient-user-id",
    content: "Secret message"
}));

// Typing indicator
ws.send(JSON.stringify({
    type: "typing",
    is_typing: true
}));

// Keep-alive ping
ws.send(JSON.stringify({ type: "ping" }));

ws.onclose = () => console.log("Disconnected");
```

## curl WebSocket Testing

Testing WebSockets with curl:

```bash
# Using websocat (install: cargo install websocat)
websocat ws://localhost:8000/ws?username=Alice\&room_id=general

# Send a message from another terminal
websocat ws://localhost:8000/ws?username=Bob\&room_id=general
```

## Message Types

### Incoming Messages (from server)

| Type | Description | Fields |
|------|-------------|--------|
| joined | Confirmation after connecting | room_id, user_id, username, history, users |
| message | Public message | id, user_id, username, content, timestamp |
| system | System notification | message, user_count, timestamp |
| private | Private message | id, from_user_id, from_username, to_user_id, content, timestamp |
| typing | Typing indicator | user_id, username, is_typing |
| pong | Ping response | - |

### Outgoing Messages (to server)

| Type | Description | Fields |
|------|-------------|--------|
| message | Send public message | content |
| private | Send private message | to_user_id, content |
| typing | Send typing indicator | is_typing |
| ping | Keep-alive ping | - |

## Example Workflow

### Terminal 1 - Alice joins
```bash
websocat ws://localhost:8000/ws?username=Alice\&room_id=general
```

### Terminal 2 - Bob joins
```bash
websocat ws://localhost:8000/ws?username=Bob\&room_id=general
```

### Terminal 1 - Send message
```json
{"type": "message", "content": "Hello Bob!"}
```

### Terminal 2 - Receive message
```json
{"type": "message", "id": "uuid", "user_id": "alice-uuid", "username": "Alice", "content": "Hello Bob!", "timestamp": "2024-01-01T00:00:00"}
```

### Check room status
```bash
curl http://localhost:8000/rooms
# {"general": {"user_count": 2, "message_count": 1}}
```

## Features Explained

### Rooms
- Default room: "general"
- Join any room by specifying `room_id` in query params
- Each room maintains its own message history

### Private Messaging
- Send to a specific user by their `user_id`
- Private messages are marked with "PRIVATE" in the client

### Message History
- Last 50 messages sent to new users on join
- Full history available via REST API
- History limited to 100 messages per room

### Keep-Alive
- Server responds to "ping" with "pong"
- Clients should send ping every 30 seconds

## License

MIT
