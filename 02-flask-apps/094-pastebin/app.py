from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, make_response
from datetime import datetime, timedelta
import sqlite3
import hashlib
import random
import string
import re

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-in-production'
DATABASE = 'pastebin.db'

LANGUAGES = [
    ('plaintext', 'Plain Text'),
    ('python', 'Python'),
    ('javascript', 'JavaScript'),
    ('java', 'Java'),
    ('cpp', 'C++'),
    ('c', 'C'),
    ('csharp', 'C#'),
    ('go', 'Go'),
    ('rust', 'Rust'),
    ('ruby', 'Ruby'),
    ('php', 'PHP'),
    ('swift', 'Swift'),
    ('kotlin', 'Kotlin'),
    ('typescript', 'TypeScript'),
    ('html', 'HTML'),
    ('css', 'CSS'),
    ('sql', 'SQL'),
    ('bash', 'Bash'),
    ('json', 'JSON'),
    ('xml', 'XML'),
    ('yaml', 'YAML'),
    ('markdown', 'Markdown'),
]

EXPIRATION_OPTIONS = [
    ('never', 'Never'),
    ('10min', '10 Minutes'),
    ('1hour', '1 Hour'),
    ('1day', '1 Day'),
    ('1week', '1 Week'),
    ('1month', '1 Month'),
]

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as db:
        db.execute('''
            CREATE TABLE IF NOT EXISTS pastes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                paste_id VARCHAR(20) UNIQUE NOT NULL,
                title VARCHAR(255),
                content TEXT NOT NULL,
                language VARCHAR(50) DEFAULT 'plaintext',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                expires_at TIMESTAMP,
                password_hash VARCHAR(64),
                is_encrypted BOOLEAN DEFAULT 0,
                view_count INTEGER DEFAULT 0,
                exposure VARCHAR(20) DEFAULT 'public'
            )
        ''')
        db.commit()

def generate_paste_id(length=12):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def get_expiration_time(option):
    now = datetime.now()
    options = {
        '10min': now + timedelta(minutes=10),
        '1hour': now + timedelta(hours=1),
        '1day': now + timedelta(days=1),
        '1week': now + timedelta(weeks=1),
        '1month': now + timedelta(days=30),
    }
    return options.get(option)

def is_expired(expires_at):
    if not expires_at:
        return False
    return datetime.now() > datetime.fromisoformat(expires_at)

def detect_language(content):
    patterns = {
        'python': [r'\bdef\s+\w+\s*\(', r'\bimport\s+\w+', r'\bclass\s+\w+:'],
        'javascript': [r'\bfunction\s+\w+\s*\(', r'\bconst\s+\w+\s*=', r'\blet\s+\w+\s*='],
        'java': [r'\bpublic\s+class\s+', r'\bSystem\.out\.', r'\bvoid\s+\w+\s*\('],
        'cpp': [r'#include\s*<', r'\bstd::', r'\bint\s+main\s*\('],
        'sql': [r'\bSELECT\s+', r'\bFROM\s+', r'\bWHERE\s+'],
        'html': [r'<!DOCTYPE', r'<html', r'<div', r'<span'],
        'css': [r'\{[\s\S]*:[\s\S]*;[\s\S]*\}', r'\.[\w-]+\s*\{', r'#[\w-]+\s*\{'],
        'json': [r'^\s*\{[\s\S]*"[\w]+":', r'^\s*\[[\s\S]*\{'],
        'bash': [r'^#!/bin/bash', r'^\s*\$\s*', r'\becho\s+'],
    }

    for lang, pattern_list in patterns.items():
        for pattern in pattern_list:
            if re.search(pattern, content, re.MULTILINE):
                return lang
    return 'plaintext'

@app.route('/')
def index():
    with get_db() as db:
        recent_pastes = db.execute('''
            SELECT * FROM pastes
            WHERE (expires_at IS NULL OR expires_at > ?)
            AND is_encrypted = 0
            ORDER BY created_at DESC LIMIT 20
        ''', (datetime.now().isoformat(),)).fetchall()

        stats = {
            'total': db.execute('SELECT COUNT(*) as count FROM pastes').fetchone()['count'],
            'public': db.execute('SELECT COUNT(*) as count FROM pastes WHERE exposure = "public"').fetchone()['count'],
        }

    return render_template('index.html',
                         languages=LANGUAGES,
                         expiration_options=EXPIRATION_OPTIONS,
                         recent_pastes=recent_pastes,
                         stats=stats)

@app.route('/create', methods=['POST'])
def create_paste():
    content = request.form.get('content', '').strip()
    title = request.form.get('title', '').strip()
    language = request.form.get('language', 'plaintext')
    expiration = request.form.get('expiration', 'never')
    password = request.form.get('password', '')
    exposure = request.form.get('exposure', 'public')

    if not content:
        flash('Content is required', 'error')
        return redirect(url_for('index'))

    paste_id = generate_paste_id()
    expires_at = None
    if expiration != 'never':
        exp_time = get_expiration_time(expiration)
        if exp_time:
            expires_at = exp_time.isoformat()

    password_hash = None
    is_encrypted = 0
    if password:
        password_hash = hash_password(password)
        is_encrypted = 1

    if language == 'auto':
        language = detect_language(content)

    with get_db() as db:
        while db.execute('SELECT id FROM pastes WHERE paste_id = ?', (paste_id,)).fetchone():
            paste_id = generate_paste_id()

        db.execute('''
            INSERT INTO pastes (paste_id, title, content, language, expires_at, password_hash, is_encrypted, exposure)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (paste_id, title, content, language, expires_at, password_hash, is_encrypted, exposure))
        db.commit()

    return redirect(url_for('view_paste', paste_id=paste_id))

@app.route('/p/<paste_id>')
def view_paste(paste_id):
    with get_db() as db:
        paste = db.execute('SELECT * FROM pastes WHERE paste_id = ?', (paste_id,)).fetchone()

        if not paste:
            flash('Paste not found', 'error')
            return redirect(url_for('index'))

        if is_expired(paste['expires_at']):
            flash('This paste has expired', 'error')
            return redirect(url_for('index'))

    return render_template('view.html', paste=paste, languages=LANGUAGES)

@app.route('/p/<paste_id>/raw')
def raw_paste(paste_id):
    with get_db() as db:
        paste = db.execute('SELECT * FROM pastes WHERE paste_id = ?', (paste_id,)).fetchone()

        if not paste:
            return 'Paste not found', 404

        if is_expired(paste['expires_at']):
            return 'This paste has expired', 410

    response = make_response(paste['content'])
    response.headers['Content-Type'] = 'text/plain'
    return response

@app.route('/p/<paste_id>/download')
def download_paste(paste_id):
    with get_db() as db:
        paste = db.execute('SELECT * FROM pastes WHERE paste_id = ?', (paste_id,)).fetchone()

        if not paste:
            return 'Paste not found', 404

        if is_expired(paste['expires_at']):
            return 'This paste has expired', 410

    response = make_response(paste['content'])
    response.headers['Content-Type'] = 'text/plain'
    response.headers['Content-Disposition'] = f'attachment; filename={paste_id}.txt'
    return response

@app.route('/api/paste/<paste_id>')
def api_get_paste(paste_id):
    with get_db() as db:
        paste = db.execute('SELECT * FROM pastes WHERE paste_id = ?', (paste_id,)).fetchone()

        if not paste:
            return jsonify({'error': 'Paste not found'}), 404

        if is_expired(paste['expires_at']):
            return jsonify({'error': 'Paste has expired'}), 410

        db.execute('UPDATE pastes SET view_count = view_count + 1 WHERE paste_id = ?', (paste_id,))
        db.commit()

    return jsonify({
        'paste_id': paste['paste_id'],
        'title': paste['title'],
        'content': paste['content'],
        'language': paste['language'],
        'created_at': paste['created_at'],
        'view_count': paste['view_count']
    })

@app.route('/api/create', methods=['POST'])
def api_create_paste():
    data = request.get_json()
    content = data.get('content', '')

    if not content:
        return jsonify({'error': 'Content is required'}), 400

    paste_id = generate_paste_id()
    language = data.get('language', detect_language(content))

    with get_db() as db:
        db.execute('''
            INSERT INTO pastes (paste_id, content, language) VALUES (?, ?, ?)
        ''', (paste_id, content, language))
        db.commit()

    return jsonify({
        'paste_id': paste_id,
        'url': url_for('view_paste', paste_id=paste_id, _external=True)
    })

@app.route('/trending')
def trending():
    with get_db() as db:
        pastes = db.execute('''
            SELECT * FROM pastes
            WHERE is_encrypted = 0
            AND (expires_at IS NULL OR expires_at > ?)
            ORDER BY view_count DESC, created_at DESC
            LIMIT 50
        ''', (datetime.now().isoformat(),)).fetchall()
    return render_template('trending.html', pastes=pastes)

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5002)
