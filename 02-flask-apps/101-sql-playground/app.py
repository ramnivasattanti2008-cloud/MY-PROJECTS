"""
SQL Playground - Flask application for running SQL queries on SQLite databases.
"""
import os
import sqlite3
import json
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_file

app = Flask(__name__)
app.config['DATABASE'] = 'playground.db'
app.config['SAVED_QUERIES_FILE'] = 'saved_queries.json'

def get_db():
    """Get database connection."""
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the database with sample tables."""
    conn = get_db()
    cursor = conn.cursor()

    # Create sample tables if they don't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE,
            age INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL,
            category TEXT,
            stock INTEGER DEFAULT 0
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            product_id INTEGER,
            quantity INTEGER,
            order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
    ''')

    # Insert sample data if tables are empty
    cursor.execute('SELECT COUNT(*) FROM users')
    if cursor.fetchone()[0] == 0:
        sample_users = [
            ('Alice Johnson', 'alice@example.com', 28),
            ('Bob Smith', 'bob@example.com', 34),
            ('Carol White', 'carol@example.com', 45),
            ('David Brown', 'david@example.com', 23),
            ('Eve Davis', 'eve@example.com', 31),
        ]
        cursor.executemany('INSERT INTO users (name, email, age) VALUES (?, ?, ?)', sample_users)

        sample_products = [
            ('Laptop', 999.99, 'Electronics', 50),
            ('Mouse', 29.99, 'Electronics', 200),
            ('Keyboard', 79.99, 'Electronics', 150),
            ('Desk Chair', 249.99, 'Furniture', 30),
            ('Monitor', 399.99, 'Electronics', 75),
        ]
        cursor.executemany('INSERT INTO products (name, price, category, stock) VALUES (?, ?, ?, ?)', sample_products)

        sample_orders = [
            (1, 1, 2),
            (2, 3, 1),
            (3, 2, 3),
            (1, 5, 1),
            (4, 1, 1),
        ]
        cursor.executemany('INSERT INTO orders (user_id, product_id, quantity) VALUES (?, ?, ?)', sample_orders)

    conn.commit()
    conn.close()

def load_saved_queries():
    """Load saved queries from JSON file."""
    if os.path.exists(app.config['SAVED_QUERIES_FILE']):
        with open(app.config['SAVED_QUERIES_FILE'], 'r') as f:
            return json.load(f)
    return []

def save_queries(queries):
    """Save queries to JSON file."""
    with open(app.config['SAVED_QUERIES_FILE'], 'w') as f:
        json.dump(queries, f, indent=2)

@app.route('/')
def index():
    """Main page showing database schema and query interface."""
    conn = get_db()
    cursor = conn.cursor()

    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    tables = [row[0] for row in cursor.fetchall()]

    # Get schema for each table
    schema = {}
    for table in tables:
        cursor.execute(f"PRAGMA table_info({table})")
        schema[table] = [dict(row) for row in cursor.fetchall()]

    # Get saved queries
    saved_queries = load_saved_queries()

    conn.close()
    return render_template('index.html', tables=tables, schema=schema, saved_queries=saved_queries)

@app.route('/execute', methods=['POST'])
def execute_query():
    """Execute a SQL query and return results."""
    query = request.json.get('query', '').strip()

    if not query:
        return jsonify({'error': 'Query is required'}), 400

    try:
        conn = get_db()
        cursor = conn.cursor()

        # Check if it's a SELECT query
        is_select = query.upper().strip().startswith('SELECT')

        if is_select:
            cursor.execute(query)
            columns = [description[0] for description in cursor.description]
            rows = cursor.fetchall()
            results = {
                'columns': columns,
                'rows': [dict(row) for row in rows],
                'row_count': len(rows),
                'success': True
            }
        else:
            cursor.execute(query)
            conn.commit()
            results = {
                'message': f'Query executed successfully. {cursor.rowcount} rows affected.',
                'row_count': cursor.rowcount,
                'success': True
            }

        conn.close()
        return jsonify(results)

    except sqlite3.Error as e:
        return jsonify({'error': str(e), 'success': False}), 400

@app.route('/save-query', methods=['POST'])
def save_query():
    """Save a query for later use."""
    data = request.json
    name = data.get('name', '').strip()
    query = data.get('query', '').strip()

    if not name or not query:
        return jsonify({'error': 'Name and query are required'}), 400

    queries = load_saved_queries()
    queries.append({
        'name': name,
        'query': query,
        'created_at': datetime.now().isoformat()
    })
    save_queries(queries)

    return jsonify({'success': True, 'message': 'Query saved successfully'})

@app.route('/delete-query', methods=['POST'])
def delete_query():
    """Delete a saved query."""
    index = request.json.get('index')

    queries = load_saved_queries()
    if 0 <= index < len(queries):
        queries.pop(index)
        save_queries(queries)
        return jsonify({'success': True})

    return jsonify({'error': 'Invalid index'}), 400

@app.route('/export', methods=['POST'])
def export_table():
    """Export query results to CSV."""
    query = request.json.get('query', '').strip()

    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(query)
        columns = [description[0] for description in cursor.description]
        rows = cursor.fetchall()
        conn.close()

        # Create CSV content
        import csv
        import io

        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(columns)
        writer.writerows(rows)

        return output.getvalue(), 200, {
            'Content-Type': 'text/csv',
            'Content-Disposition': 'attachment; filename=query_results.csv'
        }

    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 400

@app.route('/tables')
def get_tables():
    """Get list of all tables."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    tables = [row[0] for row in cursor.fetchall()]
    conn.close()
    return jsonify({'tables': tables})

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)
