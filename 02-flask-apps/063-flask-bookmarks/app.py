from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from urllib.parse import urlparse

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect('bookmarks.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS bookmarks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL,
            title TEXT NOT NULL,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS tags (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS bookmark_tags (
            bookmark_id INTEGER NOT NULL,
            tag_id INTEGER NOT NULL,
            PRIMARY KEY (bookmark_id, tag_id),
            FOREIGN KEY (bookmark_id) REFERENCES bookmarks(id) ON DELETE CASCADE,
            FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = get_db()
    search = request.args.get('search', '')
    tag_filter = request.args.get('tag', '')

    query = '''
        SELECT DISTINCT b.*, GROUP_CONCAT(t.name) as tags
        FROM bookmarks b
        LEFT JOIN bookmark_tags bt ON b.id = bt.bookmark_id
        LEFT JOIN tags t ON bt.tag_id = t.id
        WHERE 1=1
    '''
    params = []

    if search:
        query += ' AND (b.title LIKE ? OR b.description LIKE ? OR b.url LIKE ?)'
        params.extend([f'%{search}%', f'%{search}%', f'%{search}%'])

    if tag_filter:
        query += ' AND t.name = ?'
        params.append(tag_filter)

    query += ' GROUP BY b.id ORDER BY b.created_at DESC'

    bookmarks = conn.execute(query, params).fetchall()
    all_tags = conn.execute('SELECT * FROM tags ORDER BY name').fetchall()
    conn.close()

    return render_template('index.html', bookmarks=bookmarks, tags=all_tags,
                         search=search, tag_filter=tag_filter)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        url = request.form['url']
        title = request.form['title']
        description = request.form.get('description', '')
        tags = [t.strip() for t in request.form.get('tags', '').split(',') if t.strip()]

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO bookmarks (url, title, description) VALUES (?, ?, ?)',
                      (url, title, description))
        bookmark_id = cursor.lastrowid

        for tag_name in tags:
            cursor.execute('INSERT OR IGNORE INTO tags (name) VALUES (?)', (tag_name,))
            tag_row = cursor.execute('SELECT id FROM tags WHERE name = ?', (tag_name,)).fetchone()
            if tag_row:
                cursor.execute('INSERT OR IGNORE INTO bookmark_tags (bookmark_id, tag_id) VALUES (?, ?)',
                             (bookmark_id, tag_row['id']))

        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('add.html')

@app.route('/edit/<int:bookmark_id>', methods=['GET', 'POST'])
def edit(bookmark_id):
    conn = get_db()

    if request.method == 'POST':
        url = request.form['url']
        title = request.form['title']
        description = request.form.get('description', '')
        tags = [t.strip() for t in request.form.get('tags', '').split(',') if t.strip()]

        conn.execute('UPDATE bookmarks SET url = ?, title = ?, description = ? WHERE id = ?',
                    (url, title, description, bookmark_id))

        conn.execute('DELETE FROM bookmark_tags WHERE bookmark_id = ?', (bookmark_id,))

        cursor = conn.cursor()
        for tag_name in tags:
            cursor.execute('INSERT OR IGNORE INTO tags (name) VALUES (?)', (tag_name,))
            tag_row = cursor.execute('SELECT id FROM tags WHERE name = ?', (tag_name,)).fetchone()
            if tag_row:
                cursor.execute('INSERT OR IGNORE INTO bookmark_tags (bookmark_id, tag_id) VALUES (?, ?)',
                             (bookmark_id, tag_row['id']))

        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    bookmark = conn.execute('SELECT * FROM bookmarks WHERE id = ?', (bookmark_id,)).fetchone()
    tags = conn.execute('''
        SELECT t.name FROM tags t
        JOIN bookmark_tags bt ON t.id = bt.tag_id
        WHERE bt.bookmark_id = ?
    ''', (bookmark_id,)).fetchall()
    all_tags = conn.execute('SELECT * FROM tags ORDER BY name').fetchall()
    conn.close()

    return render_template('edit.html', bookmark=bookmark,
                         current_tags=','.join([t['name'] for t in tags]), all_tags=all_tags)

@app.route('/delete/<int:bookmark_id>', methods=['POST'])
def delete(bookmark_id):
    conn = get_db()
    conn.execute('DELETE FROM bookmark_tags WHERE bookmark_id = ?', (bookmark_id,))
    conn.execute('DELETE FROM bookmarks WHERE id = ?', (bookmark_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.context_processor
def utility_processor():
    def get_favicon(url):
        parsed = urlparse(url)
        return f"https://www.google.com/s2/favicons?domain={parsed.netloc}&sz=32"
    return dict(get_favicon=get_favicon)

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5002)
