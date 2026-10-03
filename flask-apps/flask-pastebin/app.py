"""
Flask Code Pastebin with syntax highlighting, expiration, and password protection.
"""
import hashlib
import secrets
from datetime import datetime, timedelta
from flask import Flask, render_template, request, redirect, url_for, jsonify, abort, session
import sqlite3
from contextlib import contextmanager

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(32)
app.config['DATABASE'] = 'pastebin.db'


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
            CREATE TABLE IF NOT EXISTS pastes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                paste_id TEXT UNIQUE NOT NULL,
                title TEXT,
                content TEXT NOT NULL,
                language TEXT DEFAULT 'plaintext',
                password_hash TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                expires_at TIMESTAMP,
                view_count INTEGER DEFAULT 0,
                is_public BOOLEAN DEFAULT 1
            )
        ''')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_paste_id ON pastes(paste_id)')


def generate_paste_id(length=8):
    """Generate a unique paste ID."""
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))


def hash_password(password):
    """Hash a password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(password, password_hash):
    """Verify a password against its hash."""
    return hashlib.sha256(password.encode()).hexdigest() == password_hash


def is_expired(expires_at):
    """Check if a paste has expired."""
    if not expires_at:
        return False
    expires = datetime.fromisoformat(expires_at)
    return datetime.now() > expires


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


@app.route('/')
def index():
    """Home page with paste creation form."""
    return render_template('index.html', languages=LANGUAGES)


@app.route('/create', methods=['POST'])
def create_paste():
    """Create a new paste."""
    content = request.form.get('content', '').strip()
    title = request.form.get('title', '').strip()
    language = request.form.get('language', 'plaintext')
    password = request.form.get('password', '').strip()
    expiration = request.form.get('expiration', 'never')
    is_public = request.form.get('is_public', '1') == '1'

    if not content:
        return jsonify({'error': 'Content is required'}), 400

    paste_id = generate_paste_id()

    expires_at = None
    if expiration == '1h':
        expires_at = (datetime.now() + timedelta(hours=1)).isoformat()
    elif expiration == '24h':
        expires_at = (datetime.now() + timedelta(hours=24)).isoformat()
    elif expiration == '7d':
        expires_at = (datetime.now() + timedelta(days=7)).isoformat()
    elif expiration == '30d':
        expires_at = (datetime.now() + timedelta(days=30)).isoformat()

    password_hash = hash_password(password) if password else None

    try:
        with get_db_conn() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO pastes (paste_id, title, content, language, password_hash, expires_at, is_public)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (paste_id, title, content, language, password_hash, expires_at, is_public))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify({
        'success': True,
        'paste_id': paste_id,
        'url': url_for('view_paste', paste_id=paste_id, _external=True)
    })


@app.route('/p/<paste_id>')
def view_paste(paste_id):
    """View a paste. May require password."""
    with get_db_conn() as conn:
        cursor = conn.cursor()
        cursor.execute(
            'SELECT * FROM pastes WHERE paste_id = ?',
            (paste_id,)
        )
        paste = cursor.fetchone()

        if not paste:
            abort(404)

        if is_expired(paste['expires_at']):
            return render_template('error.html', error='Paste Expired',
                                 message='This paste has expired and is no longer available.')

        if paste['password_hash']:
            if session.get('unlocked_pastes') and paste_id in session['unlocked_pastes']:
                cursor.execute('UPDATE pastes SET view_count = view_count + 1 WHERE paste_id = ?', (paste_id,))
                return render_template('view.html', paste=dict(paste), languages=LANGUAGES, unlocked=True)

            return render_template('password.html', paste_id=paste_id, languages=LANGUAGES)

        cursor.execute('UPDATE pastes SET view_count = view_count + 1 WHERE paste_id = ?', (paste_id,))

    return render_template('view.html', paste=dict(paste), languages=LANGUAGES, unlocked=True)


@app.route('/p/<paste_id>/unlock', methods=['POST'])
def unlock_paste(paste_id):
    """Unlock a password-protected paste."""
    password = request.form.get('password', '')

    with get_db_conn() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT password_hash FROM pastes WHERE paste_id = ?', (paste_id,))
        paste = cursor.fetchone()

        if not paste or not verify_password(password, paste['password_hash']):
            return render_template('password.html', paste_id=paste_id, error='Incorrect password', languages=LANGUAGES)

        if 'unlocked_pastes' not in session:
            session['unlocked_pastes'] = []
        session['unlocked_pastes'].append(paste_id)
        session.modified = True

    return redirect(url_for('view_paste', paste_id=paste_id))


@app.route('/api/paste/<paste_id>', methods=['GET'])
def api_get_paste(paste_id):
    """API endpoint to get paste content."""
    with get_db_conn() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM pastes WHERE paste_id = ?', (paste_id,))
        paste = cursor.fetchone()

        if not paste:
            return jsonify({'error': 'Paste not found'}), 404

        if is_expired(paste['expires_at']):
            return jsonify({'error': 'Paste expired'}), 410

        return jsonify(dict(paste))


@app.route('/raw/<paste_id>')
def raw_paste(paste_id):
    """View raw paste content."""
    with get_db_conn() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT content FROM pastes WHERE paste_id = ?', (paste_id,))
        paste = cursor.fetchone()

        if not paste:
            abort(404)

    from flask import Response
    return Response(paste['content'], mimetype='text/plain')


@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors."""
    return render_template('error.html', error='Not Found', message='The requested paste does not exist.'), 404


if __name__ == '__main__':
    import string
    init_db()
    app.run(debug=True, port=5002)
