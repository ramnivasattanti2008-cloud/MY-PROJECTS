"""
WebSockets Chat Server
A simple real-time chat server using FastAPI WebSockets.
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Query
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from typing import List, Dict
from uuid import uuid4
import json
import asyncio


app = FastAPI(title="WebSockets Chat Server")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ConnectionManager:
    """Manages WebSocket connections and message broadcasting."""

    def __init__(self):
        # Active connections: {room_id: {user_id: websocket}}
        self.active_connections: Dict[str, Dict[str, WebSocket]] = {}
        # User info: {websocket: {user_id, username, room_id}}
        self.user_info: Dict[WebSocket, dict] = {}
        # Message history: {room_id: [messages]}
        self.message_history: Dict[str, List[dict]] = {}
        # Max messages to store per room
        self.max_history = 100

    async def connect(self, websocket: WebSocket, user_id: str, username: str, room_id: str):
        """Accept and store a new connection."""
        await websocket.accept()

        # Initialize room if needed
        if room_id not in self.active_connections:
            self.active_connections[room_id] = {}
            self.message_history[room_id] = []

        # Store connection
        self.active_connections[room_id][user_id] = websocket
        self.user_info[websocket] = {
            "user_id": user_id,
            "username": username,
            "room_id": room_id
        }

        # Notify room members
        await self.broadcast(
            room_id,
            {
                "type": "system",
                "message": f"{username} joined the chat",
                "user_count": len(self.active_connections[room_id]),
                "timestamp": datetime.utcnow().isoformat()
            },
            exclude_user=user_id
        )

        # Send join confirmation with history
        await websocket.send_json({
            "type": "joined",
            "room_id": room_id,
            "user_id": user_id,
            "username": username,
            "history": self.message_history[room_id][-50:],  # Last 50 messages
            "users": [self.user_info[ws]["username"] for ws in self.active_connections[room_id].values()]
        })

    def disconnect(self, websocket: WebSocket):
        """Remove a connection."""
        if websocket not in self.user_info:
            return

        user_info = self.user_info[websocket]
        room_id = user_info["room_id"]
        user_id = user_info["user_id"]
        username = user_info["username"]

        # Remove from active connections
        if room_id in self.active_connections:
            if user_id in self.active_connections[room_id]:
                del self.active_connections[room_id][user_id]

            # Clean up empty rooms
            if not self.active_connections[room_id]:
                del self.active_connections[room_id]

        # Remove user info
        del self.user_info[websocket]

        return room_id, username, len(self.active_connections.get(room_id, {}))

    async def broadcast(self, room_id: str, message: dict, exclude_user: str = None):
        """Broadcast message to all users in a room."""
        if room_id not in self.active_connections:
            return

        disconnected = []

        for user_id, websocket in list(self.active_connections[room_id].items()):
            if exclude_user and user_id == exclude_user:
                continue

            try:
                await websocket.send_json(message)
            except Exception:
                disconnected.append(user_id)

        # Clean up disconnected clients
        for user_id in disconnected:
            if user_id in self.active_connections[room_id]:
                del self.active_connections[room_id][user_id]

    async def send_personal(self, websocket: WebSocket, message: dict):
        """Send message to a specific user."""
        try:
            await websocket.send_json(message)
        except Exception:
            pass

    async def send_private(self, from_user_id: str, to_user_id: str, message: dict):
        """Send a private message to a specific user."""
        for room_id, connections in self.active_connections.items():
            if to_user_id in connections:
                try:
                    await connections[to_user_id].send_json({
                        **message,
                        "type": "private"
                    })
                    return True
                except Exception:
                    pass
        return False

    def store_message(self, room_id: str, message: dict):
        """Store message in room history."""
        if room_id not in self.message_history:
            self.message_history[room_id] = []

        self.message_history[room_id].append(message)

        # Trim history if needed
        if len(self.message_history[room_id]) > self.max_history:
            self.message_history[room_id] = self.message_history[room_id][-self.max_history:]

    def get_room_users(self, room_id: str) -> List[dict]:
        """Get list of users in a room."""
        if room_id not in self.active_connections:
            return []

        return [
            {"user_id": ws, "username": self.user_info[ws]["username"]}
            for ws, info in self.user_info.items()
            if info["room_id"] == room_id
        ]


# Global manager instance
manager = ConnectionManager()


@app.get("/")
def root():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "WebSockets Chat Server",
        "rooms": list(manager.active_connections.keys()),
        "total_connections": sum(len(r) for r in manager.active_connections.values())
    }


@app.get("/rooms")
def list_rooms():
    """List all active rooms and their user counts."""
    return {
        room_id: {
            "user_count": len(users),
            "message_count": len(manager.message_history.get(room_id, []))
        }
        for room_id, users in manager.active_connections.items()
    }


@app.get("/rooms/{room_id}/history")
def get_history(room_id: str, limit: int = 50):
    """Get message history for a room."""
    if room_id not in manager.message_history:
        return {"messages": []}

    messages = manager.message_history[room_id][-limit:]
    return {"messages": messages}


@app.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    username: str = Query(...),
    room_id: str = Query(default="general")
):
    """WebSocket endpoint for chat communication."""
    user_id = str(uuid4())

    # Connect
    await manager.connect(websocket, user_id, username, room_id)

    try:
        while True:
            # Receive message
            data = await websocket.receive_text()

            try:
                message_data = json.loads(data)
            except json.JSONDecodeError:
                await websocket.send_json({
                    "type": "error",
                    "message": "Invalid JSON format"
                })
                continue

            msg_type = message_data.get("type", "message")

            if msg_type == "message":
                # Public message
                content = message_data.get("content", "").strip()
                if not content:
                    continue

                # Create message object
                message = {
                    "id": str(uuid4()),
                    "user_id": user_id,
                    "username": username,
                    "content": content,
                    "timestamp": datetime.utcnow().isoformat()
                }

                # Store and broadcast
                manager.store_message(room_id, message)
                await manager.broadcast(room_id, {
                    **message,
                    "type": "message"
                })

            elif msg_type == "private":
                # Private message
                to_user_id = message_data.get("to_user_id")
                content = message_data.get("content", "").strip()

                if not to_user_id or not content:
                    await websocket.send_json({
                        "type": "error",
                        "message": "Missing recipient or content"
                    })
                    continue

                message = {
                    "id": str(uuid4()),
                    "from_user_id": user_id,
                    "from_username": username,
                    "to_user_id": to_user_id,
                    "content": content,
                    "timestamp": datetime.utcnow().isoformat()
                }

                sent = await manager.send_private(user_id, to_user_id, message)

                # Confirm to sender
                await websocket.send_json({
                    **message,
                    "type": "private_sent" if sent else "private_failed",
                    "message": "Message sent" if sent else "User not found or offline"
                })

            elif msg_type == "typing":
                # Typing indicator
                await manager.broadcast(
                    room_id,
                    {
                        "type": "typing",
                        "user_id": user_id,
                        "username": username,
                        "is_typing": message_data.get("is_typing", False)
                    },
                    exclude_user=user_id
                )

            elif msg_type == "ping":
                # Keep-alive ping
                await websocket.send_json({"type": "pong"})

    except WebSocketDisconnect:
        # Handle disconnect
        result = manager.disconnect(websocket)
        if result:
            room_id, username, remaining_users = result
            await manager.broadcast(
                room_id,
                {
                    "type": "system",
                    "message": f"{username} left the chat",
                    "user_count": remaining_users,
                    "timestamp": datetime.utcnow().isoformat()
                }
            )
    except Exception as e:
        # Clean up on any error
        result = manager.disconnect(websocket)
        if result:
            room_id, username, _ = result
            await manager.broadcast(
                room_id,
                {
                    "type": "system",
                    "message": f"{username} disconnected unexpectedly",
                    "timestamp": datetime.utcnow().isoformat()
                }
            )


# Simple HTML client for testing
HTML_CLIENT = """
<!DOCTYPE html>
<html>
<head>
    <title>WebSocket Chat</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { font-family: Arial, sans-serif; background: #1a1a2e; color: #eee; height: 100vh; display: flex; }
        .sidebar { width: 250px; background: #16213e; padding: 20px; border-right: 1px solid #0f3460; }
        .sidebar h2 { margin-bottom: 20px; color: #e94560; }
        .room-info { margin-bottom: 20px; padding: 10px; background: #0f3460; border-radius: 8px; }
        .user-list { list-style: none; }
        .user-list li { padding: 8px; margin: 4px 0; background: #0f3460; border-radius: 4px; }
        .chat-area { flex: 1; display: flex; flex-direction: column; }
        .messages { flex: 1; overflow-y: auto; padding: 20px; }
        .message { margin: 10px 0; padding: 12px; background: #16213e; border-radius: 8px; }
        .message.system { background: #0f3460; color: #e94560; font-style: italic; }
        .message.private { border: 1px solid #e94560; }
        .message .meta { font-size: 12px; color: #888; margin-bottom: 4px; }
        .message .content { font-size: 14px; }
        .input-area { padding: 20px; background: #16213e; display: flex; gap: 10px; }
        input { flex: 1; padding: 12px; border: none; border-radius: 8px; background: #0f3460; color: #fff; }
        button { padding: 12px 24px; border: none; border-radius: 8px; background: #e94560; color: #fff; cursor: pointer; }
        button:hover { background: #d63850; }
        .join-form { padding: 20px; background: #16213e; display: flex; gap: 10px; justify-content: center; }
    </style>
</head>
<body>
    <div class="sidebar">
        <h2>Room: <span id="roomId">general</span></h2>
        <div class="room-info">
            <div>Users: <span id="userCount">0</span></div>
        </div>
        <h3>Online Users</h3>
        <ul class="user-list" id="userList"></ul>
    </div>
    <div class="chat-area">
        <div id="messages" class="messages"></div>
        <div class="input-area">
            <input type="text" id="messageInput" placeholder="Type a message..." />
            <button onclick="sendMessage()">Send</button>
        </div>
    </div>

    <script>
        let ws;
        let username = '';
        let roomId = 'general';

        function joinChat() {
            username = document.getElementById('usernameInput').value.trim() || 'Anonymous';
            roomId = document.getElementById('roomInput').value.trim() || 'general';

            document.getElementById('roomId').textContent = roomId;

            ws = new WebSocket(`ws://localhost:8000/ws?username=${encodeURIComponent(username)}&room_id=${encodeURIComponent(roomId)}`);

            ws.onopen = () => addMessage('Connected to chat server', 'system');

            ws.onmessage = (event) => {
                const data = JSON.parse(event.data);

                if (data.type === 'joined') {
                    document.getElementById('userCount').textContent = data.user_count;
                    updateUserList(data.users);
                    data.history.forEach(msg => addMessage(msg));
                }
                else if (data.type === 'message') {
                    addMessage(data, `${data.username} (${data.user_id.slice(0,8)})`);
                }
                else if (data.type === 'system') {
                    addMessage(data.message, 'System');
                    if (data.user_count !== undefined) {
                        document.getElementById('userCount').textContent = data.user_count;
                    }
                }
                else if (data.type === 'private' || data.type === 'private_sent') {
                    addMessage(`[PRIVATE] ${data.from_username}: ${data.content}`, 'Private');
                }
                else if (data.type === 'typing') {
                    // Could show typing indicator
                }
            };

            ws.onclose = () => addMessage('Disconnected from server', 'system');

            document.getElementById('usernameInput').disabled = true;
            document.getElementById('roomInput').disabled = true;
        }

        function updateUserList(users) {
            const list = document.getElementById('userList');
            list.innerHTML = users.map(u => `<li>${u}</li>`).join('');
        }

        function addMessage(data, prefix = '') {
            const messages = document.getElementById('messages');
            const div = document.createElement('div');
            div.className = 'message' + (data.type === 'system' ? ' system' : '');

            if (typeof data === 'string') {
                div.innerHTML = `<div class="content">${data}</div>`;
            } else {
                const time = new Date(data.timestamp).toLocaleTimeString();
                div.innerHTML = `
                    <div class="meta">${prefix || data.username} - ${time}</div>
                    <div class="content">${data.content}</div>
                `;
            }

            messages.appendChild(div);
            messages.scrollTop = messages.scrollHeight;
        }

        function sendMessage() {
            const input = document.getElementById('messageInput');
            const content = input.value.trim();

            if (content && ws && ws.readyState === WebSocket.OPEN) {
                ws.send(JSON.stringify({ type: 'message', content }));
                input.value = '';
            }
        }

        document.getElementById('messageInput').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') sendMessage();
        });

        // Initial join form
        document.write(`
            <div style="flex:1;display:flex;align-items:center;justify-content:center;">
                <div style="background:#16213e;padding:30px;border-radius:12px;text-align:center;">
                    <h2 style="color:#e94560;margin-bottom:20px;">Join Chat</h2>
                    <div class="join-form" style="flex-direction:column;gap:10px;">
                        <input type="text" id="usernameInput" placeholder="Username" style="width:200px;" />
                        <input type="text" id="roomInput" placeholder="Room ID" value="general" style="width:200px;" />
                        <button onclick="joinChat()">Join</button>
                    </div>
                </div>
            </div>
        `);
    </script>
</body>
</html>
"""


@app.get("/client")
def get_client():
    """Serve a simple HTML chat client."""
    from fastapi.responses import HTMLResponse
    return HTMLResponse(HTML_CLIENT)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
