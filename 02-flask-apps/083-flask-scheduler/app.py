from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import sqlite3

app = Flask(__name__)
DATABASE = 'tasks.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute('''CREATE TABLE IF NOT EXISTS tasks
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                     title TEXT NOT NULL,
                     description TEXT,
                     due_date TEXT,
                     priority TEXT DEFAULT 'medium',
                     status TEXT DEFAULT 'pending',
                     created_at TEXT DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = get_db()
    cursor = conn.execute('SELECT * FROM tasks ORDER BY due_date ASC')
    tasks = cursor.fetchall()
    conn.close()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['GET', 'POST'])
def add_task():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        due_date = request.form['due_date']
        priority = request.form['priority']

        conn = get_db()
        conn.execute('INSERT INTO tasks (title, description, due_date, priority) VALUES (?, ?, ?, ?)',
                     (title, description, due_date, priority))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('add_task.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_task(id):
    conn = get_db()
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        due_date = request.form['due_date']
        priority = request.form['priority']
        status = request.form['status']

        conn.execute('UPDATE tasks SET title=?, description=?, due_date=?, priority=?, status=? WHERE id=?',
                     (title, description, due_date, priority, status, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    cursor = conn.execute('SELECT * FROM tasks WHERE id=?', (id,))
    task = cursor.fetchone()
    conn.close()
    return render_template('edit_task.html', task=task)

@app.route('/delete/<int:id>')
def delete_task(id):
    conn = get_db()
    conn.execute('DELETE FROM tasks WHERE id=?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/complete/<int:id>')
def complete_task(id):
    conn = get_db()
    conn.execute('UPDATE tasks SET status=? WHERE id=?', ('completed', id))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
