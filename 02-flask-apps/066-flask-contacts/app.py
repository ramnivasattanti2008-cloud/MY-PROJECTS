from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
DATABASE = 'contacts.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT,
            phone TEXT,
            address TEXT,
            category TEXT,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    search = request.args.get('search', '')
    category_filter = request.args.get('category', '')

    conn = get_db()
    query = 'SELECT * FROM contacts WHERE 1=1'
    params = []

    if search:
        query += ' AND (name LIKE ? OR email LIKE ? OR phone LIKE ? OR notes LIKE ?)'
        search_param = f'%{search}%'
        params.extend([search_param, search_param, search_param, search_param])

    if category_filter:
        query += ' AND category = ?'
        params.append(category_filter)

    query += ' ORDER BY name ASC'
    contacts = conn.execute(query, params).fetchall()

    categories = conn.execute('SELECT DISTINCT category FROM contacts WHERE category IS NOT NULL AND category != ""').fetchall()
    categories = [c['category'] for c in categories]

    conn.close()
    return render_template('index.html', contacts=contacts, categories=categories, search=search, category_filter=category_filter)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form.get('email', '')
        phone = request.form.get('phone', '')
        address = request.form.get('address', '')
        category = request.form.get('category', '')
        notes = request.form.get('notes', '')

        conn = get_db()
        conn.execute(
            'INSERT INTO contacts (name, email, phone, address, category, notes) VALUES (?, ?, ?, ?, ?, ?)',
            (name, email, phone, address, category, notes)
        )
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('add.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = get_db()

    if request.method == 'POST':
        name = request.form['name']
        email = request.form.get('email', '')
        phone = request.form.get('phone', '')
        address = request.form.get('address', '')
        category = request.form.get('category', '')
        notes = request.form.get('notes', '')

        conn.execute(
            'UPDATE contacts SET name=?, email=?, phone=?, address=?, category=?, notes=? WHERE id=?',
            (name, email, phone, address, category, notes, id)
        )
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    contact = conn.execute('SELECT * FROM contacts WHERE id=?', (id,)).fetchone()
    conn.close()
    return render_template('edit.html', contact=contact)

@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db()
    conn.execute('DELETE FROM contacts WHERE id=?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/view/<int:id>')
def view(id):
    conn = get_db()
    contact = conn.execute('SELECT * FROM contacts WHERE id=?', (id,)).fetchone()
    conn.close()
    return render_template('view.html', contact=contact)

if __name__ == '__main__':
    app.run(debug=True)
