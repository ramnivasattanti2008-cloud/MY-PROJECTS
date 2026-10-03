"""
Code Paste Site - Flask Backend with Syntax Highlighting
"""
from flask import Flask, request, jsonify, send_file, render_template_string
from flask_cors import CORS
import sqlite3
import os
import uuid
from datetime import datetime
from pygments import highlight
from pygments.lexers import get_lexer_by_name, get_all_lexers, guess_lexer
from pygments.formatters import HtmlFormatter

app = Flask(__name__)
app.config['SECRET_KEY'] = 'code-paste-secret-2026'
CORS(app)

DB_PATH = os.path.join(os.path.dirname(__file__), 'pastes.db')
LEXERS = {l[0].lower(): l[0] for l in get_all_lexers()}

def init_db():
    """Initialize the SQLite database."""
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS pastes (
                id TEXT PRIMARY KEY,
                title TEXT DEFAULT 'Untitled',
                language TEXT DEFAULT 'text',
                code TEXT NOT NULL,
                highlighted_html TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                view_count INTEGER DEFAULT 0,
                expires_at TIMESTAMP
            )
        ''')
        conn.commit()

init_db()

def generate_id():
    """Generate a short unique paste ID."""
    return str(uuid.uuid4())[:10]

def highlight_code(code, language):
    """Highlight code using Pygments."""
    try:
        if language and language != 'text' and language.lower() != 'plain':
            lexer = get_lexer_by_name(language)
        else:
            lexer = guess_lexer(code)
    except Exception:
        lexer = get_lexer_by_name('text')
    formatter = HtmlFormatter(linenos=True, cssclass='highlight', full=True)
    return highlight(code, lexer, formatter)

@app.route('/api/languages', methods=['GET'])
def get_languages():
    """Get available programming languages."""
    languages = sorted(LEXERS.keys())
    return jsonify({'success': True, 'data': languages})

@app.route('/api/pastes', methods=['POST'])
def create_paste():
    """Create a new code paste."""
    data = request.get_json()
    code = data.get('code', '').strip()
    if not code:
        return jsonify({'success': False, 'error': 'Code is required'}), 400
    language = data.get('language', 'text').strip().lower()
    title = data.get('title', 'Untitled').strip()[:100]
    if language not in LEXERS:
        language = 'text'
    highlighted = highlight_code(code, language)
    paste_id = generate_id()
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute(
            'INSERT INTO pastes (id, title, language, code, highlighted_html) VALUES (?, ?, ?, ?, ?)',
            (paste_id, title, language, code, highlighted)
        )
        conn.commit()
    return jsonify({'success': True, 'data': {'id': paste_id, 'url': f'/paste/{paste_id}'}}), 201

@app.route('/api/pastes/<paste_id>', methods=['GET'])
def get_paste(paste_id):
    """Get a paste by ID."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute('SELECT * FROM pastes WHERE id = ?', (paste_id,))
        paste = c.fetchone()
        if not paste:
            return jsonify({'success': False, 'error': 'Paste not found'}), 404
        paste = dict(paste)
        c.execute('UPDATE pastes SET view_count = view_count + 1 WHERE id = ?', (paste_id,))
        conn.commit()
    return jsonify({'success': True, 'data': paste})

@app.route('/api/pastes', methods=['GET'])
def list_pastes():
    """List recent pastes."""
    limit = request.args.get('limit', 20, type=int)
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute('SELECT id, title, language, created_at, view_count FROM pastes ORDER BY created_at DESC LIMIT ?', (limit,))
        pastes = [dict(row) for row in c.fetchall()]
    return jsonify({'success': True, 'data': pastes})

# HTML view for paste
@app.route('/paste/<paste_id>')
def view_paste(paste_id):
    """Render a paste as an HTML page."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute('SELECT * FROM pastes WHERE id = ?', (paste_id,))
        paste = c.fetchone()
    if not paste:
        return '<h1>404 - Paste not found</h1>', 404
    paste = dict(paste)
    highlighted = paste['highlighted_html'] or highlight_code(paste['code'], paste['language'])
    html = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{paste['title']} - CodePaste</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; margin: 0; padding: 20px; background: #1e1e1e; color: #d4d4d4; }}
        .container {{ max-width: 1100px; margin: 0 auto; }}
        .header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }}
        h1 {{ color: #569cd6; margin: 0; font-size: 1.3em; }}
        .meta {{ color: #858585; font-size: 0.85em; }}
        .highlight {{ background: #1e1e1e; border-radius: 6px; overflow-x: auto; }}
        .highlight .highlight {{ background: transparent; padding: 15px; }}
        .highlight pre {{ margin: 0; }}
        .copy-btn {{ background: #0e639c; color: white; border: none; padding: 8px 16px; border-radius: 4px; cursor: pointer; font-size: 0.9em; }}
        .copy-btn:hover {{ background: #1177bb; }}
        .copy-raw {{ background: #333; color: #ccc; border: none; padding: 8px 16px; border-radius: 4px; cursor: pointer; margin-left: 8px; font-size: 0.9em; text-decoration: none; }}
        /* Pygments theme */
        .highlight .hll {{ background-color: #1e1e1e }}
        .highlight .c {{ color: #6a9955 }} /* Comment */
        .highlight .k {{ color: #569cd6 }} /* Keyword */
        .highlight .o {{ color: #d4d4d4 }} /* Operator */
        .highlight .p {{ color: #d4d4d4 }} /* Punctuation */
        .highlight .nb {{ color: #4ec9b0 }} /* Name.Builtin */
        .highlight .nc {{ color: #4ec9b0 }} /* Name.Class */
        .highlight .nf {{ color: #dcdcaa }} /* Name.Function */
        .highlight .s {{ color: #ce9178 }} /* Literal.String */
        .highlight .n {{ color: #9cdcfe }} /* Name */
        .highlight .l {{ color: #b5cea8 }} /* Literal.Number */
        .highlight .err {{ border: 1px solid #f44747 }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{paste['title']} <span class="meta">({paste['language']})</span></h1>
            <div>
                <button class="copy-btn" onclick="navigator.clipboard.writeText(document.getElementById('raw-code').textContent)">Copy</button>
                <a href="/api/pastes/{paste_id}/raw" class="copy-raw">Raw</a>
            </div>
        </div>
        <div class="highlight"><pre class="highlight"><code>{highlighted}</code></pre></div>
        <p class="meta" style="margin-top:20px">Created: {paste['created_at']} | Views: {paste['view_count']}</p>
    </div>
    <pre id="raw-code" style="display:none">{paste['code']}</pre>
</body>
</html>'''
    return html

@app.route('/api/pastes/<paste_id>/raw', methods=['GET'])
def raw_paste(paste_id):
    """Get raw code of a paste."""
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('SELECT code, language FROM pastes WHERE id = ?', (paste_id,))
        row = c.fetchone()
        if not row:
            return jsonify({'success': False, 'error': 'Paste not found'}), 404
        c.execute('UPDATE pastes SET view_count = view_count + 1 WHERE id = ?', (paste_id,))
        conn.commit()
    from flask import make_response
    response = make_response(row[0])
    response.headers['Content-Type'] = 'text/plain'
    return response

if __name__ == '__main__':
    print('Starting Code Paste server on http://localhost:5004')
    app.run(host='0.0.0.0', port=5004, debug=True)
