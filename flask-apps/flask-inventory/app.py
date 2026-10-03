from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'inventory-secret-key'
DATABASE = 'inventory.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            category TEXT,
            quantity INTEGER DEFAULT 0,
            min_quantity INTEGER DEFAULT 0,
            unit TEXT DEFAULT 'pcs',
            location TEXT,
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
    low_stock = request.args.get('low_stock', '')

    conn = get_db()
    query = 'SELECT * FROM items WHERE 1=1'
    params = []

    if search:
        query += ' AND (name LIKE ? OR description LIKE ? OR location LIKE ?)'
        search_param = f'%{search}%'
        params.extend([search_param, search_param, search_param])

    if category_filter:
        query += ' AND category = ?'
        params.append(category_filter)

    if low_stock:
        query += ' AND quantity <= min_quantity'

    query += ' ORDER BY category, name'
    items = conn.execute(query, params).fetchall()

    categories = conn.execute('SELECT DISTINCT category FROM items WHERE category IS NOT NULL AND category != ""').fetchall()
    categories = [c['category'] for c in categories]

    # Summary stats
    total_items = conn.execute('SELECT COUNT(*) as count FROM items').fetchone()['count']
    low_stock_count = conn.execute('SELECT COUNT(*) as count FROM items WHERE quantity <= min_quantity').fetchone()['count']
    total_value = conn.execute('SELECT SUM(quantity) as total FROM items').fetchone()['total'] or 0

    conn.close()
    return render_template('index.html', items=items, categories=categories,
                           search=search, category_filter=category_filter, low_stock=low_stock,
                           total_items=total_items, low_stock_count=low_stock_count, total_value=total_value)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form.get('description', '')
        category = request.form.get('category', '')
        quantity = int(request.form.get('quantity', 0))
        min_quantity = int(request.form.get('min_quantity', 0))
        unit = request.form.get('unit', 'pcs')
        location = request.form.get('location', '')

        conn = get_db()
        conn.execute(
            'INSERT INTO items (name, description, category, quantity, min_quantity, unit, location) VALUES (?, ?, ?, ?, ?, ?, ?)',
            (name, description, category, quantity, min_quantity, unit, location)
        )
        conn.commit()
        conn.close()

        if quantity <= min_quantity:
            flash(f'Warning: {name} is at or below minimum quantity!', 'warning')
        else:
            flash(f'{name} added successfully!', 'success')

        return redirect(url_for('index'))

    return render_template('add.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = get_db()

    if request.method == 'POST':
        name = request.form['name']
        description = request.form.get('description', '')
        category = request.form.get('category', '')
        quantity = int(request.form.get('quantity', 0))
        min_quantity = int(request.form.get('min_quantity', 0))
        unit = request.form.get('unit', 'pcs')
        location = request.form.get('location', '')

        conn.execute(
            'UPDATE items SET name=?, description=?, category=?, quantity=?, min_quantity=?, unit=?, location=? WHERE id=?',
            (name, description, category, quantity, min_quantity, unit, location, id)
        )
        conn.commit()
        conn.close()

        if quantity <= min_quantity:
            flash(f'Warning: {name} is at or below minimum quantity!', 'warning')

        return redirect(url_for('index'))

    item = conn.execute('SELECT * FROM items WHERE id=?', (id,)).fetchone()
    conn.close()
    return render_template('edit.html', item=item)

@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db()
    conn.execute('DELETE FROM items WHERE id=?', (id,))
    conn.commit()
    conn.close()
    flash('Item deleted.', 'info')
    return redirect(url_for('index'))

@app.route('/adjust/<int:id>', methods=['GET', 'POST'])
def adjust(id):
    conn = get_db()
    item = conn.execute('SELECT * FROM items WHERE id=?', (id,)).fetchone()

    if request.method == 'POST':
        adjustment = int(request.form.get('adjustment', 0))
        new_quantity = item['quantity'] + adjustment

        if new_quantity < 0:
            flash('Cannot reduce below zero!', 'danger')
            return redirect(url_for('adjust', id=id))

        conn.execute('UPDATE items SET quantity=? WHERE id=?', (new_quantity, id))
        conn.commit()
        conn.close()

        if new_quantity <= item['min_quantity']:
            flash(f'Warning: {item["name"]} is now at or below minimum!', 'warning')

        return redirect(url_for('index'))

    conn.close()
    return render_template('adjust.html', item=item)

if __name__ == '__main__':
    app.run(debug=True)
