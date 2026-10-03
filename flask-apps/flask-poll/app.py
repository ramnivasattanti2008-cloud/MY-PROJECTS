from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'poll_secret_key_2026'

def get_db():
    conn = sqlite3.connect('polls.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS polls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS options (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            poll_id INTEGER NOT NULL,
            option_text TEXT NOT NULL,
            FOREIGN KEY (poll_id) REFERENCES polls(id) ON DELETE CASCADE
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS votes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            option_id INTEGER NOT NULL,
            voted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (option_id) REFERENCES options(id) ON DELETE CASCADE
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = get_db()
    polls = conn.execute('SELECT * FROM polls ORDER BY created_at DESC').fetchall()
    conn.close()
    return render_template('index.html', polls=polls)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        question = request.form['question']
        options = [opt for opt in request.form.getlist('options') if opt.strip()]

        if question and len(options) >= 2:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute('INSERT INTO polls (question) VALUES (?)', (question,))
            poll_id = cursor.lastrowid

            for option in options:
                conn.execute('INSERT INTO options (poll_id, option_text) VALUES (?, ?)',
                           (poll_id, option))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('create.html')

@app.route('/poll/<int:poll_id>', methods=['GET', 'POST'])
def poll(poll_id):
    conn = get_db()
    poll_data = conn.execute('SELECT * FROM polls WHERE id = ?', (poll_id,)).fetchone()

    if not poll_data:
        conn.close()
        return "Poll not found", 404

    options = conn.execute('SELECT * FROM options WHERE poll_id = ?', (poll_id,)).fetchall()

    if request.method == 'POST':
        option_id = request.form.get('option')
        if option_id:
            conn.execute('INSERT INTO votes (option_id) VALUES (?)', (option_id,))
            conn.commit()
            conn.close()
            return redirect(url_for('results', poll_id=poll_id))

    conn.close()
    return render_template('vote.html', poll=poll_data, options=options)

@app.route('/poll/<int:poll_id>/results')
def results(poll_id):
    conn = get_db()
    poll_data = conn.execute('SELECT * FROM polls WHERE id = ?', (poll_id,)).fetchone()

    if not poll_data:
        conn.close()
        return "Poll not found", 404

    options = conn.execute('SELECT * FROM options WHERE poll_id = ?', (poll_id,)).fetchall()

    results_data = []
    total_votes = 0

    for option in options:
        vote_count = conn.execute('SELECT COUNT(*) as count FROM votes WHERE option_id = ?',
                                 (option['id'],)).fetchone()['count']
        total_votes += vote_count
        results_data.append({
            'option': option,
            'votes': vote_count
        })

    conn.close()
    return render_template('results.html', poll=poll_data, results=results_data, total=total_votes)

@app.route('/poll/<int:poll_id>/delete', methods=['POST'])
def delete(poll_id):
    conn = get_db()
    conn.execute('DELETE FROM votes WHERE option_id IN (SELECT id FROM options WHERE poll_id = ?)', (poll_id,))
    conn.execute('DELETE FROM options WHERE poll_id = ?', (poll_id,))
    conn.execute('DELETE FROM polls WHERE id = ?', (poll_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5001)
