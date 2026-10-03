from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)
DATABASE = 'reading.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT,
            genre TEXT,
            status TEXT DEFAULT 'to_read',
            rating INTEGER,
            review TEXT,
            started_at TEXT,
            finished_at TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    status_filter = request.args.get('status', '')
    genre_filter = request.args.get('genre', '')
    search = request.args.get('search', '')

    conn = get_db()
    query = 'SELECT * FROM books WHERE 1=1'
    params = []

    if search:
        query += ' AND (title LIKE ? OR author LIKE ?)'
        params.extend([f'%{search}%', f'%{search}%'])

    if status_filter:
        query += ' AND status = ?'
        params.append(status_filter)

    if genre_filter:
        query += ' AND genre = ?'
        params.append(genre_filter)

    query += ' ORDER BY created_at DESC'
    books = conn.execute(query, params).fetchall()

    # Get genres
    genres = conn.execute('SELECT DISTINCT genre FROM books WHERE genre IS NOT NULL AND genre != ""').fetchall()
    genres = [g['genre'] for g in genres]

    # Stats
    to_read = conn.execute("SELECT COUNT(*) as count FROM books WHERE status='to_read'").fetchone()['count']
    reading = conn.execute("SELECT COUNT(*) as count FROM books WHERE status='reading'").fetchone()['count']
    completed = conn.execute("SELECT COUNT(*) as count FROM books WHERE status='completed'").fetchone()['count']

    conn.close()
    return render_template('index.html', books=books, genres=genres,
                           status_filter=status_filter, genre_filter=genre_filter, search=search,
                           to_read=to_read, reading=reading, completed=completed)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form.get('author', '')
        genre = request.form.get('genre', '')
        status = request.form.get('status', 'to_read')

        conn = get_db()
        conn.execute(
            'INSERT INTO books (title, author, genre, status) VALUES (?, ?, ?, ?)',
            (title, author, genre, status)
        )
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('add.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = get_db()

    if request.method == 'POST':
        title = request.form['title']
        author = request.form.get('author', '')
        genre = request.form.get('genre', '')
        status = request.form.get('status', 'to_read')

        started_at = request.form.get('started_at', '') if status == 'reading' or status == 'completed' else None
        finished_at = request.form.get('finished_at', '') if status == 'completed' else None

        conn.execute(
            'UPDATE books SET title=?, author=?, genre=?, status=?, started_at=?, finished_at=? WHERE id=?',
            (title, author, genre, status, started_at, finished_at, id)
        )
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    book = conn.execute('SELECT * FROM books WHERE id=?', (id,)).fetchone()
    conn.close()
    return render_template('edit.html', book=book)

@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db()
    conn.execute('DELETE FROM books WHERE id=?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/update-status/<int:id>', methods=['POST'])
def update_status(id):
    new_status = request.form.get('status')

    conn = get_db()
    book = conn.execute('SELECT * FROM books WHERE id=?', (id,)).fetchone()

    started_at = book['started_at']
    finished_at = book['finished_at']

    if new_status == 'reading' and not started_at:
        started_at = datetime.now().strftime('%Y-%m-%d')

    if new_status == 'completed' and not finished_at:
        finished_at = datetime.now().strftime('%Y-%m-%d')

    conn.execute('UPDATE books SET status=?, started_at=?, finished_at=? WHERE id=?',
                 (new_status, started_at, finished_at, id))
    conn.commit()
    conn.close()

    return redirect(url_for('index'))

@app.route('/rate/<int:id>', methods=['POST'])
def rate(id):
    rating = int(request.form.get('rating', 0))

    conn = get_db()
    conn.execute('UPDATE books SET rating=? WHERE id=?', (rating, id))
    conn.commit()
    conn.close()

    return redirect(url_for('index'))

@app.route('/review/<int:id>', methods=['POST'])
def review(id):
    review = request.form.get('review', '')

    conn = get_db()
    conn.execute('UPDATE books SET review=? WHERE id=?', (review, id))
    conn.commit()
    conn.close()

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
