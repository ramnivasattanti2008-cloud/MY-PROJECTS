"""
Real-time Chat Room - Flask Backend with SocketIO
"""
from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask_cors import CORS
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'chat-room-secret-key-2026'
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

DB_PATH = os.path.join(os.path.dirname(__file__), 'chat.db')

def init_db():
    """Initialize the SQLite database."""
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS rooms (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        c.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                room TEXT NOT NULL,
                username TEXT NOT NULL,
                content TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        # Seed default rooms
        default_rooms = ['general', 'tech', 'random', 'help']
        for room in default_rooms:
            c.execute('INSERT OR IGNORE INTO rooms (name) VALUES (?)', (room,))
        conn.commit()

init_db()

# REST API endpoints
@app.route('/api/rooms', methods=['GET'])
def get_rooms():
    """Get all available chat rooms."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute('SELECT * FROM rooms ORDER BY name')
        rooms = [dict(row) for row in c.fetchall()]
    return jsonify({'success': True, 'data': rooms})

@app.route('/api/messages/<room>', methods=['GET'])
def get_messages(room):
    """Get last 50 messages from a room."""
    limit = request.args.get('limit', 50, type=int)
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute(
            'SELECT * FROM messages WHERE room = ? ORDER BY id DESC LIMIT ?',
            (room, limit)
        )
        messages = [dict(row) for row in c.fetchall()]
    messages.reverse()
    return jsonify({'success': True, 'data': messages})

@app.route('/api/rooms', methods=['POST'])
def create_room():
    """Create a new chat room."""
    data = request.get_json()
    name = data.get('name', '').strip().lower()
    if not name:
        return jsonify({'success': False, 'error': 'Room name required'}), 400
    if not all(c.isalnum() or c in '-_' for c in name):
        return jsonify({'success': False, 'error': 'Invalid room name'}), 400
    try:
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute('INSERT INTO rooms (name) VALUES (?)', (name,))
            conn.commit()
            room_id = c.lastrowid
        return jsonify({'success': True, 'data': {'id': room_id, 'name': name}}), 201
    except sqlite3.IntegrityError:
        return jsonify({'success': False, 'error': 'Room already exists'}), 409

# SocketIO event handlers
@socketio.on('connect')
def handle_connect():
    """Handle client connection."""
    print(f'Client connected: {request.sid}')

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection."""
    print(f'Client disconnected: {request.sid}')

@socketio.on('join')
def handle_join(data):
    """Handle user joining a room."""
    username = data.get('username', 'Anonymous').strip()
    room = data.get('room', 'general').strip()
    join_room(room)
    # Save join message
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute(
            'INSERT INTO messages (room, username, content) VALUES (?, ?, ?)',
            (room, username, f'{username} joined the room')
        )
        conn.commit()
    emit('message', {
        'username': 'System',
        'content': f'{username} joined {room}',
        'timestamp': datetime.now().isoformat(),
        'system': True
    }, to=room)
    print(f'{username} joined room: {room}')

@socketio.on('leave')
def handle_leave(data):
    """Handle user leaving a room."""
    username = data.get('username', 'Anonymous')
    room = data.get('room', 'general')
    leave_room(room)
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute(
            'INSERT INTO messages (room, username, content) VALUES (?, ?, ?)',
            (room, username, f'{username} left the room')
        )
        conn.commit()
    emit('message', {
        'username': 'System',
        'content': f'{username} left {room}',
        'timestamp': datetime.now().isoformat(),
        'system': True
    }, to=room)
    print(f'{username} left room: {room}')

@socketio.on('message')
def handle_message(data):
    """Handle incoming chat messages."""
    username = data.get('username', 'Anonymous').strip()
    content = data.get('content', '').strip()
    room = data.get('room', 'general').strip()
    if not content:
        return
    timestamp = datetime.now().isoformat()
    # Save to database
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute(
            'INSERT INTO messages (room, username, content) VALUES (?, ?, ?)',
            (room, username, content)
        )
        conn.commit()
        msg_id = c.lastrowid
    msg_data = {
        'id': msg_id,
        'username': username,
        'content': content,
        'room': room,
        'timestamp': timestamp,
        'system': False
    }
    emit('message', msg_data, to=room)
    print(f'Message in {room} from {username}: {content[:50]}')

if __name__ == '__main__':
    print('Starting Chat Room server on http://localhost:5001')
    socketio.run(app, host='0.0.0.0', port=5001, debug=True)
