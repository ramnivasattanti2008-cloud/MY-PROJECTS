"""
Flask URL Shortener with custom short codes, click tracking, and analytics dashboard.
"""
import string
import random
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
import sqlite3
from contextlib import contextmanager

app = Flask(__name__)
app.config['DATABASE'] = 'urlshortener.db'


def get_db():
    """Get database connection."""
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


@contextmanager
def get_db_conn():
    """Context manager for database connections."""
    conn = get_db()
    try:
        yield conn
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()


def init_db():
    """Initialize the database with required tables."""
    with get_db_conn() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS urls (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                original_url TEXT NOT NULL,
                short_code TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                click_count INTEGER DEFAULT 0,
                is_active BOOLEAN DEFAULT 1
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS clicks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url_id INTEGER NOT NULL,
                clicked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                ip_address TEXT,
                user_agent TEXT,
                referer TEXT,
                FOREIGN KEY (url_id) REFERENCES urls(id)
            )
        ''')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_short_code ON urls(short_code)')


def generate_short_code(length=6):
    """Generate a random short code."""
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))


def is_valid_url(url):
    """Basic URL validation."""
    return url and (url.startswith('http://') or url.startswith('https://'))


@app.route('/')
def index():
    """Home page with URL shortener form."""
    return render_template('index.html')


@app.route('/dashboard')
def dashboard():
    """Analytics dashboard showing all URLs and stats."""
    with get_db_conn() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, original_url, short_code, created_at, click_count
            FROM urls WHERE is_active = 1
            ORDER BY created_at DESC
            LIMIT 100
        ''')
        urls = cursor.fetchall()

        cursor.execute('SELECT COUNT(*) as total, SUM(click_count) as clicks FROM urls')
        stats = cursor.fetchone()

    return render_template('dashboard.html', urls=urls, stats=stats)


@app.route('/create', methods=['POST'])
def create_short_url():
    """Create a new shortened URL."""
    original_url = request.form.get('url', '').strip()
    custom_code = request.form.get('custom_code', '').strip()

    if not is_valid_url(original_url):
        return jsonify({'error': 'Please enter a valid URL starting with http:// or https://'}), 400

    if custom_code:
        if len(custom_code) < 3 or len(custom_code) > 20:
            return jsonify({'error': 'Custom code must be between 3 and 20 characters'}), 400
        if not all(c.isalnum() or c in '-_' for c in custom_code):
            return jsonify({'error': 'Custom code can only contain letters, numbers, hyphens, and underscores'}), 400
        short_code = custom_code
    else:
        short_code = generate_short_code()

    try:
        with get_db_conn() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id FROM urls WHERE short_code = ?', (short_code,))
            if cursor.fetchone():
                return jsonify({'error': 'This short code already exists. Please choose another.'}), 409

            cursor.execute(
                'INSERT INTO urls (original_url, short_code) VALUES (?, ?)',
                (original_url, short_code)
            )
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    short_url = request.host_url + short_code
    return jsonify({
        'success': True,
        'short_url': short_url,
        'short_code': short_code
    })


@app.route('/<short_code>')
def redirect_to_url(short_code):
    """Redirect to the original URL and track the click."""
    with get_db_conn() as conn:
        cursor = conn.cursor()
        cursor.execute(
            'SELECT id, original_url FROM urls WHERE short_code = ? AND is_active = 1',
            (short_code,)
        )
        url = cursor.fetchone()

        if not url:
            abort(404)

        cursor.execute(
            'INSERT INTO clicks (url_id, ip_address, user_agent, referer) VALUES (?, ?, ?, ?)',
            (url['id'], request.remote_addr, request.user_agent.string, request.referrer)
        )
        cursor.execute(
            'UPDATE urls SET click_count = click_count + 1 WHERE id = ?',
            (url['id'],)
        )

    return redirect(url['original_url'])


@app.route('/stats/<short_code>')
def url_stats(short_code):
    """Get detailed stats for a specific URL."""
    with get_db_conn() as conn:
        cursor = conn.cursor()
        cursor.execute(
            'SELECT id, original_url, short_code, created_at, click_count FROM urls WHERE short_code = ?',
            (short_code,)
        )
        url = cursor.fetchone()

        if not url:
            abort(404)

        cursor.execute('''
            SELECT clicked_at, ip_address, referer
            FROM clicks WHERE url_id = ?
            ORDER BY clicked_at DESC LIMIT 50
        ''', (url['id'],))
        clicks = cursor.fetchall()

    return render_template('stats.html', url=url, clicks=clicks)


@app.route('/api/urls')
def api_list_urls():
    """API endpoint to list all URLs."""
    with get_db_conn() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT short_code, original_url, created_at, click_count
            FROM urls WHERE is_active = 1 ORDER BY created_at DESC
        ''')
        urls = [dict(row) for row in cursor.fetchall()]

    return jsonify({'urls': urls, 'count': len(urls)})


@app.route('/api/urls/<short_code>', methods=['DELETE'])
def api_delete_url(short_code):
    """Soft delete a URL."""
    with get_db_conn() as conn:
        cursor = conn.cursor()
        cursor.execute('UPDATE urls SET is_active = 0 WHERE short_code = ?', (short_code,))
        if cursor.rowcount == 0:
            return jsonify({'error': 'URL not found'}), 404

    return jsonify({'success': True})


@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors."""
    return render_template('error.html', error='Page not found', message='The requested URL does not exist.'), 404


if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5001)
