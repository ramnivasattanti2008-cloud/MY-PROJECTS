from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
DATABASE = 'forum.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute('''CREATE TABLE IF NOT EXISTS categories
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                     name TEXT NOT NULL UNIQUE,
                     description TEXT,
                     created_at TEXT DEFAULT CURRENT_TIMESTAMP)''')

    conn.execute('''CREATE TABLE IF NOT EXISTS threads
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                     title TEXT NOT NULL,
                     content TEXT NOT NULL,
                     category_id INTEGER,
                     author TEXT DEFAULT 'Anonymous',
                     created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                     FOREIGN KEY (category_id) REFERENCES categories(id))''')

    conn.execute('''CREATE TABLE IF NOT EXISTS replies
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                     thread_id INTEGER NOT NULL,
                     content TEXT NOT NULL,
                     author TEXT DEFAULT 'Anonymous',
                     created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                     FOREIGN KEY (thread_id) REFERENCES threads(id))''')

    # Add some default categories if none exist
    cursor = conn.execute('SELECT COUNT(*) FROM categories')
    if cursor.fetchone()[0] == 0:
        default_categories = [
            ('General', 'General discussion topics'),
            ('Help', 'Get help with any topic'),
            ('Ideas', 'Share your ideas and suggestions'),
            ('Announcements', 'Official announcements')
        ]
        conn.executemany('INSERT INTO categories (name, description) VALUES (?, ?)', default_categories)

    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = get_db()
    categories = conn.execute('SELECT * FROM categories ORDER BY name').fetchall()

    # Get thread counts per category
    thread_counts = {}
    cursor = conn.execute('SELECT category_id, COUNT(*) FROM threads GROUP BY category_id')
    for row in cursor:
        thread_counts[row['category_id']] = row[1]

    # Get recent threads
    recent_threads = conn.execute('''
        SELECT threads.*, categories.name as category_name,
               (SELECT COUNT(*) FROM replies WHERE replies.thread_id = threads.id) as reply_count
        FROM threads
        LEFT JOIN categories ON threads.category_id = categories.id
        ORDER BY threads.created_at DESC LIMIT 10
    ''').fetchall()

    conn.close()
    return render_template('index.html', categories=categories, thread_counts=thread_counts, recent_threads=recent_threads)

@app.route('/category/<int:category_id>')
def category(category_id):
    conn = get_db()
    category = conn.execute('SELECT * FROM categories WHERE id=?', (category_id,)).fetchone()

    threads = conn.execute('''
        SELECT threads.*,
               (SELECT COUNT(*) FROM replies WHERE replies.thread_id = threads.id) as reply_count
        FROM threads
        WHERE threads.category_id=?
        ORDER BY threads.created_at DESC
    ''', (category_id,)).fetchall()
    conn.close()
    return render_template('category.html', category=category, threads=threads)

@app.route('/thread/<int:thread_id>')
def thread(thread_id):
    conn = get_db()
    thread = conn.execute('''
        SELECT threads.*, categories.name as category_name
        FROM threads
        LEFT JOIN categories ON threads.category_id = categories.id
        WHERE threads.id=?
    ''', (thread_id,)).fetchone()

    replies = conn.execute('SELECT * FROM replies WHERE thread_id=? ORDER BY created_at', (thread_id,)).fetchall()
    conn.close()
    return render_template('thread.html', thread=thread, replies=replies)

@app.route('/new-thread', methods=['GET', 'POST'])
def new_thread():
    conn = get_db()
    categories = conn.execute('SELECT * FROM categories ORDER BY name').fetchall()
    conn.close()

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        category_id = request.form['category_id']
        author = request.form['author'] or 'Anonymous'

        conn = get_db()
        conn.execute('INSERT INTO threads (title, content, category_id, author) VALUES (?, ?, ?, ?)',
                    (title, content, category_id, author))
        conn.commit()
        conn.close()
        return redirect(url_for('category', category_id=category_id))

    return render_template('new_thread.html', categories=categories)

@app.route('/reply/<int:thread_id>', methods=['POST'])
def reply(thread_id):
    content = request.form['content']
    author = request.form['author'] or 'Anonymous'

    conn = get_db()
    conn.execute('INSERT INTO replies (thread_id, content, author) VALUES (?, ?, ?)',
                (thread_id, content, author))
    conn.commit()
    conn.close()
    return redirect(url_for('thread', thread_id=thread_id))

@app.route('/delete-thread/<int:thread_id>')
def delete_thread(thread_id):
    conn = get_db()
    conn.execute('DELETE FROM replies WHERE thread_id=?', (thread_id,))
    conn.execute('DELETE FROM threads WHERE id=?', (thread_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
