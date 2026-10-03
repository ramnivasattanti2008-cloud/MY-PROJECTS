"""
Link Collector - Flask Backend API
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os
import re
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'link-collector-secret-2026'
CORS(app)

DB_PATH = os.path.join(os.path.dirname(__file__), 'links.db')

def init_db():
    """Initialize the SQLite database."""
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS links (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT NOT NULL,
                title TEXT DEFAULT '',
                description TEXT DEFAULT '',
                tags TEXT DEFAULT '',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                visit_count INTEGER DEFAULT 0,
                is_favorite INTEGER DEFAULT 0
            )
        ''')
        c.execute('''
            CREATE TABLE IF NOT EXISTS tags (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                color TEXT DEFAULT '#6366f1',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        # Seed demo links
        demo_links = [
            ('https://github.com', 'GitHub', 'Code hosting and collaboration', 'code,tools', 0),
            ('https://stackoverflow.com', 'Stack Overflow', 'Programming Q&A', 'code,community', 0),
            ('https://developer.mozilla.org', 'MDN Web Docs', 'Web development reference', 'web,docs', 0),
            ('https://flask.palletsprojects.com', 'Flask', 'Python web framework', 'python,web', 0),
            ('https://react.dev', 'React', 'JavaScript library for UI', 'javascript,frontend', 0),
        ]
        for url, title, desc, tags, fav in demo_links:
            c.execute(
                'INSERT OR IGNORE INTO links (url, title, description, tags) VALUES (?, ?, ?, ?)',
                (url, title, desc, tags)
            )
        conn.commit()

init_db()

def row_to_dict(row):
    return dict(row) if row else None

def validate_url(url):
    """Basic URL validation."""
    pattern = re.compile(
        r'^https?://'
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'
        r'localhost|'
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
        r'(?::\d+)?'
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return bool(pattern.match(url))

# --- Link Routes ---
@app.route('/api/links', methods=['GET'])
def get_links():
    """Get all links with optional filtering."""
    tag_filter = request.args.get('tag')
    search = request.args.get('search', '').strip()
    favorites_only = request.args.get('favorites', '').strip().lower() == 'true'
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        query = 'SELECT * FROM links WHERE 1=1'
        params = []
        if tag_filter:
            query += ' AND tags LIKE ?'
            params.append(f'%{tag_filter}%')
        if search:
            query += ' AND (title LIKE ? OR description LIKE ? OR url LIKE ? OR tags LIKE ?)'
            s = f'%{search}%'
            params.extend([s, s, s, s])
        if favorites_only:
            query += ' AND is_favorite = 1'
        query += ' ORDER BY created_at DESC'
        c.execute(query, params)
        links = [dict(row) for row in c.fetchall()]
    return jsonify({'success': True, 'data': links})

@app.route('/api/links', methods=['POST'])
def create_link():
    """Add a new link."""
    data = request.get_json()
    url = data.get('url', '').strip()
    title = data.get('title', url).strip()[:200]
    description = data.get('description', '').strip()[:500]
    tags = data.get('tags', '')
    if isinstance(tags, list):
        tags = ','.join(t.strip() for t in tags if t.strip())
    if not url:
        return jsonify({'success': False, 'error': 'URL is required'}), 400
    if not validate_url(url):
        return jsonify({'success': False, 'error': 'Invalid URL format'}), 400
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute(
            'INSERT INTO links (url, title, description, tags) VALUES (?, ?, ?, ?)',
            (url, title, description, tags)
        )
        conn.commit()
        link_id = c.lastrowid
        c.execute('SELECT * FROM links WHERE id = ?', (link_id,))
        link = dict(c.fetchone())
    return jsonify({'success': True, 'data': link}), 201

@app.route('/api/links/<int:link_id>', methods=['GET'])
def get_link(link_id):
    """Get a specific link."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute('SELECT * FROM links WHERE id = ?', (link_id,))
        link = c.fetchone()
        if not link:
            return jsonify({'success': False, 'error': 'Link not found'}), 404
    return jsonify({'success': True, 'data': dict(link)})

@app.route('/api/links/<int:link_id>', methods=['PUT'])
def update_link(link_id):
    """Update a link."""
    data = request.get_json()
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM links WHERE id = ?', (link_id,))
        if not c.fetchone():
            return jsonify({'success': False, 'error': 'Link not found'}), 404
        updates = []
        params = []
        for field in ['title', 'description', 'tags', 'is_favorite']:
            if field in data:
                updates.append(f'{field} = ?')
                params.append(data[field])
        if updates:
            params.append(link_id)
            c.execute(f'UPDATE links SET {", ".join(updates)} WHERE id = ?', params)
            conn.commit()
        c.execute('SELECT * FROM links WHERE id = ?', (link_id,))
        link = dict(c.fetchone())
    return jsonify({'success': True, 'data': link})

@app.route('/api/links/<int:link_id>', methods=['DELETE'])
def delete_link(link_id):
    """Delete a link."""
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('SELECT id FROM links WHERE id = ?', (link_id,))
        if not c.fetchone():
            return jsonify({'success': False, 'error': 'Link not found'}), 404
        c.execute('DELETE FROM links WHERE id = ?', (link_id,))
        conn.commit()
    return jsonify({'success': True})

@app.route('/api/links/<int:link_id>/visit', methods=['POST'])
def visit_link(link_id):
    """Track a link visit."""
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('UPDATE links SET visit_count = visit_count + 1 WHERE id = ?', (link_id,))
        conn.commit()
    return jsonify({'success': True})

@app.route('/api/links/<int:link_id>/favorite', methods=['POST'])
def toggle_favorite(link_id):
    """Toggle favorite status."""
    data = request.get_json() or {}
    favorite = data.get('favorite')
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        if favorite is not None:
            c.execute('UPDATE links SET is_favorite = ? WHERE id = ?', (1 if favorite else 0, link_id))
        else:
            c.execute('UPDATE links SET is_favorite = NOT is_favorite WHERE id = ?', (link_id,))
        conn.commit()
        c.execute('SELECT * FROM links WHERE id = ?', (link_id,))
        link = c.fetchone()
        if not link:
            return jsonify({'success': False, 'error': 'Link not found'}), 404
    return jsonify({'success': True, 'data': dict(link)})

# --- Tag Routes ---
@app.route('/api/tags', methods=['GET'])
def get_tags():
    """Get all unique tags with counts."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute('''
            SELECT DISTINCT value as name, COUNT(*) as count
            FROM links, json_each(REPLACE(links.tags, ',', '","'))
            GROUP BY value
            ORDER BY count DESC
        ''')
        # Simpler approach: parse tags from links table
        c.execute('SELECT tags FROM links WHERE tags != ""')
        all_tags = {}
        for row in c.fetchall():
            for tag in row['tags'].split(','):
                tag = tag.strip()
                if tag:
                    all_tags[tag] = all_tags.get(tag, 0) + 1
        tags = [{'name': t, 'count': c} for t, c in sorted(all_tags.items(), key=lambda x: -x[1])]
    return jsonify({'success': True, 'data': tags})

# --- Stats ---
@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get collection statistics."""
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('SELECT COUNT(*) as total FROM links')
        total = c.fetchone()[0]
        c.execute('SELECT COUNT(*) as favorites FROM links WHERE is_favorite = 1')
        favorites = c.fetchone()[0]
        c.execute('SELECT SUM(visit_count) as visits FROM links')
        visits = c.fetchone()[0] or 0
        c.execute('SELECT COUNT(DISTINCT tags) FROM links WHERE tags != ""')
        unique_tags = c.fetchone()[0]
    return jsonify({
        'success': True,
        'data': {
            'total': total,
            'favorites': favorites,
            'total_visits': visits,
            'tag_count': unique_tags
        }
    })

if __name__ == '__main__':
    print('Starting Link Collector server on http://localhost:5005')
    app.run(host='0.0.0.0', port=5005, debug=True)
