from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from datetime import datetime, timedelta
import sqlite3
import secrets
import hashlib
import random

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-in-production'
DATABASE = 'api_dashboard.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as db:
        db.execute('''
            CREATE TABLE IF NOT EXISTS api_keys (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key_id VARCHAR(32) UNIQUE NOT NULL,
                key_secret_hash VARCHAR(64) NOT NULL,
                name VARCHAR(100) NOT NULL,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                expires_at TIMESTAMP,
                is_active BOOLEAN DEFAULT 1,
                rate_limit INTEGER DEFAULT 100,
                last_used TIMESTAMP,
                usage_count INTEGER DEFAULT 0
            )
        ''')

        db.execute('''
            CREATE TABLE IF NOT EXISTS api_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key_id VARCHAR(32) NOT NULL,
                endpoint VARCHAR(255) NOT NULL,
                method VARCHAR(10) NOT NULL,
                status_code INTEGER,
                response_time_ms INTEGER,
                ip_address VARCHAR(45),
                user_agent TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (key_id) REFERENCES api_keys(key_id)
            )
        ''')

        db.execute('''
            CREATE TABLE IF NOT EXISTS endpoints (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                path VARCHAR(255) UNIQUE NOT NULL,
                method VARCHAR(10) NOT NULL,
                description TEXT,
                response_format VARCHAR(20) DEFAULT 'json',
                requires_auth BOOLEAN DEFAULT 1
            )
        ''')

        existing = db.execute('SELECT COUNT(*) as count FROM api_keys').fetchone()['count']
        if existing == 0:
            seed_demo_data(db)

        db.commit()

def seed_demo_data(db):
    demo_keys = [
        ('demo_key_001', 'Demo API Key', 'For testing purposes', 7),
        ('prod_key_002', 'Production Key', 'Main production API key', 365),
    ]

    for key_id, name, desc, days_valid in demo_keys:
        secret = secrets.token_hex(16)
        secret_hash = hashlib.sha256(secret.encode()).hexdigest()
        expires = (datetime.now() + timedelta(days=days_valid)).isoformat()

        db.execute('''
            INSERT INTO api_keys (key_id, key_secret_hash, name, description, expires_at, usage_count)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (key_id, secret_hash, name, desc, expires, random.randint(100, 5000)))

        for i in range(random.randint(10, 50)):
            endpoint = random.choice(['/api/users', '/api/products', '/api/orders', '/api/stats'])
            method = random.choice(['GET', 'POST', 'PUT', 'DELETE'])
            status = random.choice([200, 200, 200, 201, 400, 401, 404, 500])
            response_time = random.randint(10, 500)
            ip = f'{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}'

            db.execute('''
                INSERT INTO api_logs (key_id, endpoint, method, status_code, response_time_ms, ip_address)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (key_id, endpoint, method, status, response_time, ip))

    demo_endpoints = [
        ('/api/users', 'GET', 'Get all users', 'json', 1),
        ('/api/users/:id', 'GET', 'Get user by ID', 'json', 1),
        ('/api/users', 'POST', 'Create new user', 'json', 1),
        ('/api/products', 'GET', 'Get all products', 'json', 1),
        ('/api/orders', 'GET', 'Get all orders', 'json', 1),
        ('/api/stats', 'GET', 'Get API statistics', 'json', 1),
    ]

    for path, method, desc, fmt, auth in demo_endpoints:
        db.execute('''
            INSERT OR IGNORE INTO endpoints (path, method, description, response_format, requires_auth)
            VALUES (?, ?, ?, ?, ?)
        ''', (path, method, desc, fmt, auth))

def generate_api_key():
    return {
        'key_id': secrets.token_hex(8),
        'key_secret': secrets.token_hex(24)
    }

def hash_secret(secret):
    return hashlib.sha256(secret.encode()).hexdigest()

@app.route('/')
def index():
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    with get_db() as db:
        stats = {
            'total_keys': db.execute('SELECT COUNT(*) as count FROM api_keys WHERE is_active = 1').fetchone()['count'],
            'total_requests': db.execute('SELECT SUM(usage_count) as total FROM api_keys').fetchone()['total'] or 0,
            'avg_response': db.execute('SELECT AVG(response_time_ms) as avg FROM api_logs').fetchone()['avg'] or 0,
            'error_rate': calculate_error_rate(db),
        }

        recent_logs = db.execute('''
            SELECT l.*, k.name as key_name
            FROM api_logs l
            JOIN api_keys k ON l.key_id = k.key_id
            ORDER BY l.created_at DESC LIMIT 20
        ''').fetchall()

        keys = db.execute('SELECT * FROM api_keys ORDER BY created_at DESC').fetchall()

        status_counts = db.execute('''
            SELECT status_code, COUNT(*) as count
            FROM api_logs
            GROUP BY status_code
            ORDER BY count DESC
        ''').fetchall()

        hourly_stats = db.execute('''
            SELECT
                strftime('%H', created_at) as hour,
                COUNT(*) as requests,
                AVG(response_time_ms) as avg_time
            FROM api_logs
            WHERE created_at > datetime('now', '-24 hours')
            GROUP BY hour
            ORDER BY hour
        ''').fetchall()

    return render_template('dashboard.html', stats=stats, recent_logs=recent_logs,
                         keys=keys, status_counts=status_counts, hourly_stats=hourly_stats)

@app.route('/keys')
def manage_keys():
    with get_db() as db:
        keys = db.execute('SELECT * FROM api_keys ORDER BY created_at DESC').fetchall()
    return render_template('keys.html', keys=keys)

@app.route('/keys/create', methods=['GET', 'POST'])
def create_key():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()
        expires_days = int(request.form.get('expires_days', 30))
        rate_limit = int(request.form.get('rate_limit', 100))

        if not name:
            flash('Name is required', 'error')
            return redirect(url_for('create_key'))

        key_data = generate_api_key()
        expires_at = (datetime.now() + timedelta(days=expires_days)).isoformat() if expires_days > 0 else None

        with get_db() as db:
            db.execute('''
                INSERT INTO api_keys (key_id, key_secret_hash, name, description, expires_at, rate_limit)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (key_data['key_id'], hash_secret(key_data['key_secret']), name, description, expires_at, rate_limit))
            db.commit()

        return render_template('key_created.html', key_id=key_data['key_id'], key_secret=key_data['key_secret'], name=name)

    return render_template('create_key.html')

@app.route('/keys/<key_id>/toggle', methods=['POST'])
def toggle_key(key_id):
    with get_db() as db:
        key = db.execute('SELECT * FROM api_keys WHERE key_id = ?', (key_id,)).fetchone()
        if key:
            db.execute('UPDATE api_keys SET is_active = ? WHERE key_id = ?', (not key['is_active'], key_id))
            db.commit()
    return redirect(url_for('manage_keys'))

@app.route('/keys/<key_id>/delete', methods=['POST'])
def delete_key(key_id):
    with get_db() as db:
        db.execute('DELETE FROM api_logs WHERE key_id = ?', (key_id,))
        db.execute('DELETE FROM api_keys WHERE key_id = ?', (key_id,))
        db.commit()
    flash('API key deleted', 'success')
    return redirect(url_for('manage_keys'))

@app.route('/logs')
def logs():
    page = int(request.args.get('page', 1))
    per_page = 50
    offset = (page - 1) * per_page

    with get_db() as db:
        logs = db.execute('''
            SELECT l.*, k.name as key_name
            FROM api_logs l
            JOIN api_keys k ON l.key_id = k.key_id
            ORDER BY l.created_at DESC
            LIMIT ? OFFSET ?
        ''', (per_page, offset)).fetchall()

        total = db.execute('SELECT COUNT(*) as count FROM api_logs').fetchone()['count']
        total_pages = (total + per_page - 1) // per_page

    return render_template('logs.html', logs=logs, page=page, total_pages=total_pages)

@app.route('/endpoints')
def endpoints():
    with get_db() as db:
        endpoint_list = db.execute('SELECT * FROM endpoints ORDER BY path').fetchall()
    return render_template('endpoints.html', endpoints=endpoint_list)

@app.route('/stats')
def stats():
    with get_db() as db:
        daily_requests = db.execute('''
            SELECT DATE(created_at) as date, COUNT(*) as requests, AVG(response_time_ms) as avg_time
            FROM api_logs
            GROUP BY DATE(created_at)
            ORDER BY date DESC LIMIT 30
        ''').fetchall()

        top_endpoints = db.execute('''
            SELECT endpoint, COUNT(*) as requests, AVG(response_time_ms) as avg_time
            FROM api_logs
            GROUP BY endpoint
            ORDER BY requests DESC LIMIT 10
        ''').fetchall()

        top_ips = db.execute('''
            SELECT ip_address, COUNT(*) as requests
            FROM api_logs
            GROUP BY ip_address
            ORDER BY requests DESC LIMIT 10
        ''').fetchall()
    return render_template('stats.html', daily_requests=daily_requests,
                         top_endpoints=top_endpoints, top_ips=top_ips)

@app.route('/api/simulate', methods=['POST'])
def simulate_request():
    key_id = request.form.get('key_id', '')
    endpoint = request.form.get('endpoint', '/api/test')
    method = request.form.get('method', 'GET')

    status_codes = [200, 201, 400, 401, 404, 500, 503]
    weights = [60, 15, 10, 5, 5, 3, 2]
    status = random.choices(status_codes, weights=weights)[0]
    response_time = random.randint(20, 800)

    with get_db() as db:
        db.execute('''
            INSERT INTO api_logs (key_id, endpoint, method, status_code, response_time_ms, ip_address, user_agent)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (key_id, endpoint, method, status, response_time, request.remote_addr, request.headers.get('User-Agent')))

        db.execute('UPDATE api_keys SET usage_count = usage_count + 1, last_used = CURRENT_TIMESTAMP WHERE key_id = ?', (key_id,))
        db.commit()

    return jsonify({
        'status': status,
        'response_time_ms': response_time,
        'endpoint': endpoint,
        'method': method
    })

def calculate_error_rate(db):
    total = db.execute('SELECT COUNT(*) as count FROM api_logs').fetchone()['count']
    errors = db.execute('SELECT COUNT(*) as count FROM api_logs WHERE status_code >= 400').fetchone()['count']
    if total == 0:
        return 0
    return round((errors / total) * 100, 2)

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5005)
