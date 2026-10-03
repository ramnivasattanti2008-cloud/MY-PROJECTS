"""
Live Polling App - Flask Backend with SocketIO
"""
from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import sqlite3
import os
import uuid
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'poll-app-secret-key-2026'
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

DB_PATH = os.path.join(os.path.dirname(__file__), 'polls.db')

def init_db():
    """Initialize the SQLite database."""
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS polls (
                id TEXT PRIMARY KEY,
                question TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_active INTEGER DEFAULT 1,
                total_votes INTEGER DEFAULT 0
            )
        ''')
        c.execute('''
            CREATE TABLE IF NOT EXISTS options (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                poll_id TEXT NOT NULL,
                text TEXT NOT NULL,
                votes INTEGER DEFAULT 0,
                FOREIGN KEY (poll_id) REFERENCES polls(id)
            )
        ''')
        c.execute('''
            CREATE TABLE IF NOT EXISTS votes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                poll_id TEXT NOT NULL,
                option_id INTEGER NOT NULL,
                voter_id TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(poll_id, voter_id)
            )
        ''')
        conn.commit()

init_db()

def get_poll_with_options(poll_id):
    """Get a poll with its options."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute('SELECT * FROM polls WHERE id = ?', (poll_id,))
        poll = c.fetchone()
        if not poll:
            return None
        c.execute('SELECT * FROM options WHERE poll_id = ? ORDER BY id', (poll_id,))
        options = [dict(row) for row in c.fetchall()]
    result = dict(poll)
    result['options'] = options
    return result

def generate_short_id():
    """Generate a short readable poll ID."""
    return str(uuid.uuid4())[:8]

# API Routes
@app.route('/api/polls', methods=['GET'])
def get_polls():
    """Get all polls."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute('SELECT * FROM polls ORDER BY created_at DESC')
        polls = [dict(row) for row in c.fetchall()]
    return jsonify({'success': True, 'data': polls})

@app.route('/api/polls', methods=['POST'])
def create_poll():
    """Create a new poll."""
    data = request.get_json()
    question = data.get('question', '').strip()
    options = data.get('options', [])
    if not question:
        return jsonify({'success': False, 'error': 'Question required'}), 400
    if len(options) < 2:
        return jsonify({'success': False, 'error': 'At least 2 options required'}), 400
    options = [opt.strip() for opt in options if opt.strip()]
    if len(options) < 2:
        return jsonify({'success': False, 'error': 'At least 2 non-empty options required'}), 400
    poll_id = generate_short_id()
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('INSERT INTO polls (id, question) VALUES (?, ?)', (poll_id, question))
        for opt in options:
            c.execute('INSERT INTO options (poll_id, text) VALUES (?, ?)', (poll_id, opt))
        conn.commit()
    poll = get_poll_with_options(poll_id)
    socketio.emit('poll_created', poll)
    return jsonify({'success': True, 'data': poll}), 201

@app.route('/api/polls/<poll_id>', methods=['GET'])
def get_poll(poll_id):
    """Get a specific poll with results."""
    poll = get_poll_with_options(poll_id)
    if not poll:
        return jsonify({'success': False, 'error': 'Poll not found'}), 404
    return jsonify({'success': True, 'data': poll})

@app.route('/api/polls/<poll_id>/vote', methods=['POST'])
def vote_poll(poll_id):
    """Vote on a poll."""
    data = request.get_json()
    option_id = data.get('option_id')
    voter_id = data.get('voter_id', request.remote_addr)
    if option_id is None:
        return jsonify({'success': False, 'error': 'Option ID required'}), 400
    poll = get_poll_with_options(poll_id)
    if not poll:
        return jsonify({'success': False, 'error': 'Poll not found'}), 404
    if not poll['is_active']:
        return jsonify({'success': False, 'error': 'Poll is closed'}), 400
    valid_option_ids = [opt['id'] for opt in poll['options']]
    if option_id not in valid_option_ids:
        return jsonify({'success': False, 'error': 'Invalid option'}), 400
    try:
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute(
                'INSERT INTO votes (poll_id, option_id, voter_id) VALUES (?, ?, ?)',
                (poll_id, option_id, voter_id)
            )
            c.execute('UPDATE options SET votes = votes + 1 WHERE id = ?', (option_id,))
            c.execute('UPDATE polls SET total_votes = total_votes + 1 WHERE id = ?', (poll_id,))
            conn.commit()
        poll = get_poll_with_options(poll_id)
        socketio.emit('poll_updated', poll, room=poll_id)
        return jsonify({'success': True, 'data': poll})
    except sqlite3.IntegrityError:
        return jsonify({'success': False, 'error': 'Already voted'}), 409

@app.route('/api/polls/<poll_id>/close', methods=['POST'])
def close_poll(poll_id):
    """Close a poll."""
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('UPDATE polls SET is_active = 0 WHERE id = ?', (poll_id,))
        conn.commit()
    poll = get_poll_with_options(poll_id)
    if poll:
        socketio.emit('poll_closed', poll, room=poll_id)
    return jsonify({'success': True})

@socketio.on('join_poll')
def handle_join_poll(data):
    """Subscribe to poll updates."""
    poll_id = data.get('poll_id')
    if poll_id:
        from flask_socketio import join_room
        join_room(poll_id)

@socketio.on('leave_poll')
def handle_leave_poll(data):
    """Unsubscribe from poll updates."""
    poll_id = data.get('poll_id')
    if poll_id:
        from flask_socketio import leave_room
        leave_room(poll_id)

@socketio.on('connect')
def handle_connect():
    print(f'Client connected: {request.sid}')

@socketio.on('disconnect')
def handle_disconnect():
    print(f'Client disconnected: {request.sid}')

if __name__ == '__main__':
    print('Starting Poll App server on http://localhost:5002')
    socketio.run(app, host='0.0.0.0', port=5002, debug=True)
