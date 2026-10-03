"""
Mini Twitter Clone - Flask Backend API
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mini-twitter-secret-2026'
CORS(app)

DB_PATH = os.path.join(os.path.dirname(__file__), 'twitter.db')

def init_db():
    """Initialize the SQLite database."""
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                display_name TEXT,
                bio TEXT DEFAULT '',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        c.execute('''
            CREATE TABLE IF NOT EXISTS tweets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                likes INTEGER DEFAULT 0,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        c.execute('''
            CREATE TABLE IF NOT EXISTS follows (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                follower_id INTEGER NOT NULL,
                following_id INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(follower_id, following_id),
                FOREIGN KEY (follower_id) REFERENCES users(id),
                FOREIGN KEY (following_id) REFERENCES users(id)
            )
        ''')
        c.execute('''
            CREATE TABLE IF NOT EXISTS likes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                tweet_id INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(user_id, tweet_id),
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (tweet_id) REFERENCES tweets(id)
            )
        ''')
        # Seed demo users
        demo_users = [
            ('alice', 'Alice Johnson', 'Tech enthusiast and coffee lover'),
            ('bob', 'Bob Smith', 'Software engineer by day, musician by night'),
            ('charlie', 'Charlie Brown', 'Sharing thoughts on life and code'),
        ]
        for username, display_name, bio in demo_users:
            c.execute(
                'INSERT OR IGNORE INTO users (username, display_name, bio) VALUES (?, ?, ?)',
                (username, display_name, bio)
            )
        conn.commit()

init_db()

def row_to_dict(row):
    return dict(row) if row else None

# --- User Routes ---
@app.route('/api/users', methods=['GET'])
def get_users():
    """Get all users."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute('SELECT * FROM users ORDER BY username')
        users = [dict(row) for row in c.fetchall()]
    return jsonify({'success': True, 'data': users})

@app.route('/api/users', methods=['POST'])
def create_user():
    """Register a new user."""
    data = request.get_json()
    username = data.get('username', '').strip().lower()
    display_name = data.get('display_name', username).strip()
    bio = data.get('bio', '').strip()
    if not username or len(username) < 3:
        return jsonify({'success': False, 'error': 'Username must be at least 3 characters'}), 400
    if not all(c.isalnum() or c in '_' for c in username):
        return jsonify({'success': False, 'error': 'Username can only contain letters, numbers, underscore'}), 400
    try:
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute(
                'INSERT INTO users (username, display_name, bio) VALUES (?, ?, ?)',
                (username, display_name, bio)
            )
            conn.commit()
            user_id = c.lastrowid
        return jsonify({'success': True, 'data': {'id': user_id, 'username': username, 'display_name': display_name, 'bio': bio}}), 201
    except sqlite3.IntegrityError:
        return jsonify({'success': False, 'error': 'Username already taken'}), 409

@app.route('/api/users/<username>', methods=['GET'])
def get_user(username):
    """Get user profile with stats."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = c.fetchone()
        if not user:
            return jsonify({'success': False, 'error': 'User not found'}), 404
        user = dict(user)
        c.execute('SELECT COUNT(*) as tweet_count FROM tweets WHERE user_id = ?', (user['id'],))
        user['tweet_count'] = c.fetchone()['tweet_count']
        c.execute('SELECT COUNT(*) as followers FROM follows WHERE following_id = ?', (user['id'],))
        user['followers'] = c.fetchone()['followers']
        c.execute('SELECT COUNT(*) as following FROM follows WHERE follower_id = ?', (user['id'],))
        user['following'] = c.fetchone()['following']
        c.execute('''
            SELECT t.*, u.username, u.display_name,
                   (SELECT COUNT(*) FROM likes WHERE tweet_id = t.id) as likes
            FROM tweets t JOIN users u ON t.user_id = u.id
            WHERE t.user_id = ? ORDER BY t.created_at DESC
        ''', (user['id'],))
        user['tweets'] = [dict(row) for row in c.fetchall()]
    return jsonify({'success': True, 'data': user})

# --- Tweet Routes ---
@app.route('/api/tweets', methods=['GET'])
def get_tweets():
    """Get tweets. Optional: ?user=username or ?feed=username."""
    user_filter = request.args.get('user')
    feed_user = request.args.get('feed')
    limit = request.args.get('limit', 50, type=int)
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        if feed_user:
            c.execute('''
                SELECT t.*, u.username, u.display_name
                FROM tweets t JOIN users u ON t.user_id = u.id
                WHERE t.user_id IN (
                    SELECT following_id FROM follows WHERE follower_id = (
                        SELECT id FROM users WHERE username = ?
                    )
                ) OR t.user_id = (SELECT id FROM users WHERE username = ?)
                ORDER BY t.created_at DESC LIMIT ?
            ''', (feed_user, feed_user, limit))
        elif user_filter:
            c.execute('''
                SELECT t.*, u.username, u.display_name
                FROM tweets t JOIN users u ON t.user_id = u.id
                WHERE u.username = ? ORDER BY t.created_at DESC LIMIT ?
            ''', (user_filter, limit))
        else:
            c.execute('''
                SELECT t.*, u.username, u.display_name
                FROM tweets t JOIN users u ON t.user_id = u.id
                ORDER BY t.created_at DESC LIMIT ?
            ''', (limit,))
        tweets = [dict(row) for row in c.fetchall()]
    return jsonify({'success': True, 'data': tweets})

@app.route('/api/tweets', methods=['POST'])
def create_tweet():
    """Post a new tweet."""
    data = request.get_json()
    username = data.get('username', '').strip()
    content = data.get('content', '').strip()
    if not username:
        return jsonify({'success': False, 'error': 'Username required'}), 400
    if not content or len(content) > 280:
        return jsonify({'success': False, 'error': 'Tweet must be 1-280 characters'}), 400
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('SELECT id FROM users WHERE username = ?', (username,))
        user = c.fetchone()
        if not user:
            return jsonify({'success': False, 'error': 'User not found'}), 404
        user_id = user[0]
        c.execute(
            'INSERT INTO tweets (user_id, content) VALUES (?, ?)',
            (user_id, content)
        )
        conn.commit()
        tweet_id = c.lastrowid
        c.execute('''
            SELECT t.*, u.username, u.display_name
            FROM tweets t JOIN users u ON t.user_id = u.id
            WHERE t.id = ?
        ''', (tweet_id,))
        tweet = dict(c.fetchone())
    return jsonify({'success': True, 'data': tweet}), 201

@app.route('/api/tweets/<int:tweet_id>/like', methods=['POST'])
def like_tweet(tweet_id):
    """Like a tweet."""
    data = request.get_json()
    username = data.get('username', '').strip()
    if not username:
        return jsonify({'success': False, 'error': 'Username required'}), 400
    try:
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute('SELECT id FROM users WHERE username = ?', (username,))
            user = c.fetchone()
            if not user:
                return jsonify({'success': False, 'error': 'User not found'}), 404
            user_id = user[0]
            c.execute('INSERT INTO likes (user_id, tweet_id) VALUES (?, ?)', (user_id, tweet_id))
            c.execute('UPDATE tweets SET likes = likes + 1 WHERE id = ?', (tweet_id,))
            conn.commit()
        return jsonify({'success': True})
    except sqlite3.IntegrityError:
        return jsonify({'success': False, 'error': 'Already liked'}), 409

# --- Follow Routes ---
@app.route('/api/follow', methods=['POST'])
def follow_user():
    """Follow a user."""
    data = request.get_json()
    follower = data.get('follower', '').strip()
    following = data.get('following', '').strip()
    if follower == following:
        return jsonify({'success': False, 'error': 'Cannot follow yourself'}), 400
    try:
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute('SELECT id FROM users WHERE username = ?', (follower,))
            f1 = c.fetchone()
            c.execute('SELECT id FROM users WHERE username = ?', (following,))
            f2 = c.fetchone()
            if not f1 or not f2:
                return jsonify({'success': False, 'error': 'User not found'}), 404
            c.execute('INSERT INTO follows (follower_id, following_id) VALUES (?, ?)', (f1[0], f2[0]))
            conn.commit()
        return jsonify({'success': True})
    except sqlite3.IntegrityError:
        return jsonify({'success': False, 'error': 'Already following'}), 409

@app.route('/api/unfollow', methods=['POST'])
def unfollow_user():
    """Unfollow a user."""
    data = request.get_json()
    follower = data.get('follower', '').strip()
    following = data.get('following', '').strip()
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('SELECT id FROM users WHERE username = ?', (follower,))
        f1 = c.fetchone()
        c.execute('SELECT id FROM users WHERE username = ?', (following,))
        f2 = c.fetchone()
        if not f1 or not f2:
            return jsonify({'success': False, 'error': 'User not found'}), 404
        c.execute('DELETE FROM follows WHERE follower_id = ? AND following_id = ?', (f1[0], f2[0]))
        conn.commit()
    return jsonify({'success': True})

if __name__ == '__main__':
    print('Starting Mini Twitter server on http://localhost:5003')
    app.run(host='0.0.0.0', port=5003, debug=True)
