"""
Pastebin Flask Application
Share code snippets with syntax highlighting
"""
import os
import sqlite3
import hashlib
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, abort

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
DATABASE = os.path.join(os.path.dirname(__file__), 'pastebin.db')

# Supported languages for syntax highlighting
LANGUAGES = [
    ('plaintext', 'Plain Text'),
    ('python', 'Python'),
    ('javascript', 'JavaScript'),
    ('java', 'Java'),
    ('c', 'C'),
    ('cpp', 'C++'),
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
        CREATE TABLE IF NOT EXISTS pastes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            paste_id VARCHAR(16) UNIQUE NOT NULL,
            title TEXT,
            content TEXT NOT NULL,
            language TEXT DEFAULT 'plaintext',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            view_count INTEGER DEFAULT 0,
            expires_at TIMESTAMP,
            is_private INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()


def generate_paste_id(length=8):
    """Generate a unique paste ID"""
    timestamp = str(datetime.now().timestamp()).encode()
    hash_obj = hashlib.sha256(timestamp)
    return hash_obj.hexdigest()[:length]


@app.route('/')
def index():
    """Home page with paste creation form"""
    return render_template('index.html', languages=LANGUAGES)


@app.route('/create', methods=['POST'])
def create_paste():
    """Create a new paste"""
    content = request.form.get('content', '').strip()
    title = request.form.get('title', '').strip() or None
    language = request.form.get('language', 'plaintext')
    expiry_days = request.form.get('expiry', 'never')

    if not content:
        flash('Please enter some content to paste', 'error')
        return redirect(url_for('index'))

    # Validate language
    valid_languages = [lang[0] for lang in LANGUAGES]
    if language not in valid_languages:
        language = 'plaintext'

    conn = get_db()
    cursor = conn.cursor()

    # Generate unique paste ID
    paste_id = generate_paste_id()
    while cursor.execute('SELECT 1 FROM pastes WHERE paste_id = ?', (paste_id,)).fetchone():
        paste_id = generate_paste_id()

    # Calculate expiry
    expires_at = None
    if expiry_days != 'never':
        try:
            days = int(expiry_days)
            if days > 0:
                from datetime import timedelta
                expires_at = (datetime.now() + timedelta(days=days)).isoformat()
        except ValueError:
            pass

    try:
        cursor.execute('''
            INSERT INTO pastes (paste_id, title, content, language, expires_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (paste_id, title, content, language, expires_at))
        conn.commit()
        conn.close()
        return redirect(url_for('view_paste', paste_id=paste_id))
    except Exception as e:
        conn.close()
        flash(f'Error creating paste: {str(e)}', 'error')
        return redirect(url_for('index'))


@app.route('/<paste_id>')
def view_paste(paste_id):
    """View a paste with syntax highlighting"""
    conn = get_db()
    cursor = conn.cursor()

    paste = cursor.execute(
        'SELECT * FROM pastes WHERE paste_id = ?',
        (paste_id,)
    ).fetchone()

    if not paste:
        conn.close()
        abort(404)

    # Check if paste has expired
    if paste['expires_at']:
        expires_at = datetime.fromisoformat(paste['expires_at'])
        if datetime.now() > expires_at:
            cursor.execute('DELETE FROM pastes WHERE paste_id = ?', (paste_id,))
            conn.commit()
            conn.close()
            abort(404)

    # Increment view count
    cursor.execute(
        'UPDATE pastes SET view_count = view_count + 1 WHERE paste_id = ?',
        (paste_id,)
    )
    conn.commit()

    # Get language name
    language_name = paste['language']
    for lang_code, lang_name in LANGUAGES:
        if lang_code == paste['language']:
            language_name = lang_name
            break

    conn.close()

    return render_template('view.html',
                         paste=paste,
                         language_name=language_name,
                         languages=LANGUAGES)


@app.route('/raw/<paste_id>')
def raw_paste(paste_id):
    """View raw paste content"""
    conn = get_db()
    cursor = conn.cursor()

    paste = cursor.execute(
        'SELECT content, language FROM pastes WHERE paste_id = ?',
        (paste_id,)
    ).fetchone()

    conn.close()

    if not paste:
        abort(404)

    from flask import Response
    return Response(paste['content'], mimetype='text/plain')


@app.route('/clone/<paste_id>')
def clone_paste(paste_id):
    """Clone a paste to create a new one"""
    conn = get_db()
    cursor = conn.cursor()

    paste = cursor.execute(
        'SELECT title, content, language FROM pastes WHERE paste_id = ?',
        (paste_id,)
    ).fetchone()

    conn.close()

    if not paste:
        abort(404)

    return render_template('index.html',
                         languages=LANGUAGES,
                         clone_content=paste['content'],
                         clone_title=paste['title'],
                         clone_language=paste['language'])


@app.route('/api/pastes', methods=['GET'])
def api_list_pastes():
    """API endpoint to list recent pastes"""
    conn = get_db()
    cursor = conn.cursor()

    pastes = cursor.execute('''
        SELECT paste_id, title, language, created_at, view_count
        FROM pastes
        ORDER BY created_at DESC
        LIMIT 50
    ''').fetchall()

    conn.close()

    return {'pastes': [dict(p) for p in pastes]}


@app.route('/api/pastes/<paste_id>', methods=['GET'])
def api_get_paste(paste_id):
    """API endpoint to get a specific paste"""
    conn = get_db()
    cursor = conn.cursor()

    paste = cursor.execute(
        'SELECT * FROM pastes WHERE paste_id = ?',
        (paste_id,)
    ).fetchone()

    conn.close()

    if not paste:
        return {'error': 'Paste not found'}, 404

    return dict(paste)


if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5001)
