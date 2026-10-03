"""
URL Shortener Flask Application
Shorten URLs, track clicks, and view analytics
"""
import os
import sqlite3
import string
import random
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
DATABASE = os.path.join(os.path.dirname(__file__), 'urlshortener.db')


def get_db():
    """Get database connection with row factory"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize the database schema"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            short_code VARCHAR(10) UNIQUE NOT NULL,
            original_url TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            click_count INTEGER DEFAULT 0
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clicks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url_id INTEGER NOT NULL,
            clicked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            user_agent TEXT,
            ip_address TEXT,
            FOREIGN KEY (url_id) REFERENCES urls(id)
        )
    ''')
    conn.commit()
    conn.close()


def generate_short_code(length=6):
    """Generate a random short code"""
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))


@app.route('/')
def index():
    """Home page with URL submission form"""
    return render_template('index.html')


@app.route('/shorten', methods=['POST'])
def shorten_url():
    """Create a shortened URL"""
    original_url = request.form.get('url', '').strip()

    if not original_url:
        flash('Please provide a URL to shorten', 'error')
        return redirect(url_for('index'))

    # Add https if no scheme provided
    if not original_url.startswith(('http://', 'https://')):
        original_url = 'https://' + original_url

    conn = get_db()
    cursor = conn.cursor()

    # Generate unique short code
    short_code = generate_short_code()
    while cursor.execute('SELECT 1 FROM urls WHERE short_code = ?', (short_code,)).fetchone():
        short_code = generate_short_code()

    try:
        cursor.execute(
            'INSERT INTO urls (short_code, original_url) VALUES (?, ?)',
            (short_code, original_url)
        )
        conn.commit()
        short_url = request.host_url + short_code
        flash(f'Successfully shortened! Your URL: {short_url}', 'success')
    except Exception as e:
        flash(f'Error creating short URL: {str(e)}', 'error')
    finally:
        conn.close()

    return redirect(url_for('index'))


@app.route('/<short_code>')
def redirect_to_url(short_code):
    """Redirect to original URL and track click"""
    conn = get_db()
    cursor = conn.cursor()

    result = cursor.execute(
        'SELECT id, original_url FROM urls WHERE short_code = ?',
        (short_code,)
    ).fetchone()

    if not result:
        conn.close()
        flash('Short URL not found', 'error')
        return redirect(url_for('index'))

    # Track the click
    cursor.execute(
        'INSERT INTO clicks (url_id, user_agent, ip_address) VALUES (?, ?, ?)',
        (result['id'], request.user_agent.string, request.remote_addr)
    )
    cursor.execute(
        'UPDATE urls SET click_count = click_count + 1 WHERE id = ?',
        (result['id'],)
    )
    conn.commit()
    conn.close()

    return redirect(result['original_url'])


@app.route('/stats')
def stats():
    """Analytics dashboard showing all URLs and their statistics"""
    conn = get_db()
    cursor = conn.cursor()

    urls = cursor.execute('''
        SELECT
            id, short_code, original_url, created_at, click_count,
            (SELECT COUNT(*) FROM clicks WHERE url_id = urls.id) as total_clicks
        FROM urls
        ORDER BY created_at DESC
    ''').fetchall()

    # Calculate statistics
    total_urls = len(urls)
    total_clicks = sum(url['click_count'] for url in urls)

    # Get recent clicks
    recent_clicks = cursor.execute('''
        SELECT c.clicked_at, c.user_agent, c.ip_address, u.short_code, u.original_url
        FROM clicks c
        JOIN urls u ON c.url_id = u.id
        ORDER BY c.clicked_at DESC
        LIMIT 20
    ''').fetchall()

    conn.close()

    return render_template('stats.html',
                         urls=urls,
                         total_urls=total_urls,
                         total_clicks=total_clicks,
                         recent_clicks=recent_clicks)


@app.route('/api/shorten', methods=['POST'])
def api_shorten():
    """API endpoint to create short URL"""
    data = request.get_json()

    if not data or 'url' not in data:
        return jsonify({'error': 'URL is required'}), 400

    original_url = data['url'].strip()

    if not original_url.startswith(('http://', 'https://')):
        original_url = 'https://' + original_url

    conn = get_db()
    cursor = conn.cursor()

    short_code = generate_short_code()
    while cursor.execute('SELECT 1 FROM urls WHERE short_code = ?', (short_code,)).fetchone():
        short_code = generate_short_code()

    try:
        cursor.execute(
            'INSERT INTO urls (short_code, original_url) VALUES (?, ?)',
            (short_code, original_url)
        )
        conn.commit()
        short_url = request.host_url + short_code
        conn.close()
        return jsonify({
            'short_url': short_url,
            'short_code': short_code,
            'original_url': original_url
        }), 201
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 500


@app.route('/api/stats/<short_code>')
def api_stats(short_code):
    """API endpoint to get stats for a specific URL"""
    conn = get_db()
    cursor = conn.cursor()

    url = cursor.execute(
        'SELECT * FROM urls WHERE short_code = ?',
        (short_code,)
    ).fetchone()

    if not url:
        conn.close()
        return jsonify({'error': 'URL not found'}), 404

    clicks = cursor.execute(
        'SELECT * FROM clicks WHERE url_id = ? ORDER BY clicked_at DESC',
        (url['id'],)
    ).fetchall()

    conn.close()

    return jsonify({
        'short_code': url['short_code'],
        'original_url': url['original_url'],
        'created_at': url['created_at'],
        'click_count': url['click_count'],
        'clicks': [dict(click) for click in clicks]
    })


if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
