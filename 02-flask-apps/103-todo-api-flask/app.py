"""
Todo REST API Flask Application
CRUD endpoints for todo list management
"""
import os
import sqlite3
from datetime import datetime
from flask import Flask, request, jsonify

app = Flask(__name__)
DATABASE = os.path.join(os.path.dirname(__file__), 'todos.db')


def get_db():
    """Get database connection with row factory"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize the database schema"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            completed INTEGER DEFAULT 0,
            priority TEXT DEFAULT 'medium',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()


def row_to_dict(row):
    """Convert sqlite3.Row to dictionary"""
    if row is None:
        return None
    return dict(row)


@app.route('/api/todos', methods=['GET'])
def get_todos():
    """
    Get all todos
    Query params:
        - completed: filter by completion status (0 or 1)
        - priority: filter by priority (low, medium, high)
        - search: search in title and description
    """
    conn = get_db()
    cursor = conn.cursor()

    query = 'SELECT * FROM todos WHERE 1=1'
    params = []

    # Filter by completion status
    completed = request.args.get('completed')
    if completed is not None:
        query += ' AND completed = ?'
        params.append(int(completed))

    # Filter by priority
    priority = request.args.get('priority')
    if priority:
        query += ' AND priority = ?'
        params.append(priority)

    # Search in title and description
    search = request.args.get('search')
    if search:
        query += ' AND (title LIKE ? OR description LIKE ?)'
        search_param = f'%{search}%'
        params.extend([search_param, search_param])

    query += ' ORDER BY completed ASC, created_at DESC'

    todos = cursor.execute(query, params).fetchall()
    conn.close()

    return jsonify({
        'success': True,
        'data': [row_to_dict(todo) for todo in todos],
        'count': len(todos)
    })


@app.route('/api/todos/<int:todo_id>', methods=['GET'])
def get_todo(todo_id):
    """Get a specific todo by ID"""
    conn = get_db()
    cursor = conn.cursor()

    todo = cursor.execute('SELECT * FROM todos WHERE id = ?', (todo_id,)).fetchone()
    conn.close()

    if not todo:
        return jsonify({
            'success': False,
            'error': 'Todo not found'
        }), 404

    return jsonify({
        'success': True,
        'data': row_to_dict(todo)
    })


@app.route('/api/todos', methods=['POST'])
def create_todo():
    """
    Create a new todo
    Body: { title, description?, priority? }
    """
    data = request.get_json()

    if not data or 'title' not in data:
        return jsonify({
            'success': False,
            'error': 'Title is required'
        }), 400

    title = data['title'].strip()
    if not title:
        return jsonify({
            'success': False,
            'error': 'Title cannot be empty'
        }), 400

    description = data.get('description', '').strip() or None
    priority = data.get('priority', 'medium')

    # Validate priority
    valid_priorities = ['low', 'medium', 'high']
    if priority not in valid_priorities:
        priority = 'medium'

    conn = get_db()
    cursor = conn.cursor()

    try:
        cursor.execute('''
            INSERT INTO todos (title, description, priority)
            VALUES (?, ?, ?)
        ''', (title, description, priority))
        todo_id = cursor.lastrowid
        conn.commit()

        todo = cursor.execute('SELECT * FROM todos WHERE id = ?', (todo_id,)).fetchone()
        conn.close()

        return jsonify({
            'success': True,
            'data': row_to_dict(todo),
            'message': 'Todo created successfully'
        }), 201

    except Exception as e:
        conn.close()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    """
    Update a todo
    Body: { title?, description?, completed?, priority? }
    """
    data = request.get_json()

    if not data:
        return jsonify({
            'success': False,
            'error': 'No data provided'
        }), 400

    conn = get_db()
    cursor = conn.cursor()

    # Check if todo exists
    existing = cursor.execute('SELECT * FROM todos WHERE id = ?', (todo_id,)).fetchone()
    if not existing:
        conn.close()
        return jsonify({
            'success': False,
            'error': 'Todo not found'
        }), 404

    # Build update query dynamically
    updates = []
    params = []

    if 'title' in data:
        title = data['title'].strip()
        if not title:
            conn.close()
            return jsonify({
                'success': False,
                'error': 'Title cannot be empty'
            }), 400
        updates.append('title = ?')
        params.append(title)

    if 'description' in data:
        updates.append('description = ?')
        params.append(data['description'].strip() or None)

    if 'completed' in data:
        updates.append('completed = ?')
        params.append(1 if data['completed'] else 0)

    if 'priority' in data:
        priority = data['priority']
        if priority not in ['low', 'medium', 'high']:
            priority = 'medium'
        updates.append('priority = ?')
        params.append(priority)

    if not updates:
        conn.close()
        return jsonify({
            'success': False,
            'error': 'No valid fields to update'
        }), 400

    updates.append('updated_at = ?')
    params.append(datetime.now().isoformat())
    params.append(todo_id)

    try:
        query = f"UPDATE todos SET {', '.join(updates)} WHERE id = ?"
        cursor.execute(query, params)
        conn.commit()

        todo = cursor.execute('SELECT * FROM todos WHERE id = ?', (todo_id,)).fetchone()
        conn.close()

        return jsonify({
            'success': True,
            'data': row_to_dict(todo),
            'message': 'Todo updated successfully'
        })

    except Exception as e:
        conn.close()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    """Delete a todo"""
    conn = get_db()
    cursor = conn.cursor()

    existing = cursor.execute('SELECT * FROM todos WHERE id = ?', (todo_id,)).fetchone()
    if not existing:
        conn.close()
        return jsonify({
            'success': False,
            'error': 'Todo not found'
        }), 404

    try:
        cursor.execute('DELETE FROM todos WHERE id = ?', (todo_id,))
        conn.commit()
        conn.close()

        return jsonify({
            'success': True,
            'message': 'Todo deleted successfully'
        })

    except Exception as e:
        conn.close()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/todos/stats', methods=['GET'])
def get_stats():
    """Get todo statistics"""
    conn = get_db()
    cursor = conn.cursor()

    total = cursor.execute('SELECT COUNT(*) as count FROM todos').fetchone()['count']
    completed = cursor.execute('SELECT COUNT(*) as count FROM todos WHERE completed = 1').fetchone()['count']
    pending = total - completed

    by_priority = cursor.execute('''
        SELECT priority, COUNT(*) as count
        FROM todos
        GROUP BY priority
    ''').fetchall()

    conn.close()

    return jsonify({
        'success': True,
        'data': {
            'total': total,
            'completed': completed,
            'pending': pending,
            'completion_rate': round(completed / total * 100, 1) if total > 0 else 0,
            'by_priority': {row['priority']: row['count'] for row in by_priority}
        }
    })


@app.route('/api/todos/complete-all', methods=['POST'])
def complete_all():
    """Mark all todos as completed"""
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('''
        UPDATE todos
        SET completed = 1, updated_at = ?
        WHERE completed = 0
    ''', (datetime.now().isoformat(),))

    count = cursor.rowcount
    conn.commit()
    conn.close()

    return jsonify({
        'success': True,
        'message': f'{count} todos marked as completed'
    })


@app.route('/api/todos/clear-completed', methods=['DELETE'])
def clear_completed():
    """Delete all completed todos"""
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('DELETE FROM todos WHERE completed = 1')
    count = cursor.rowcount
    conn.commit()
    conn.close()

    return jsonify({
        'success': True,
        'message': f'{count} completed todos deleted'
    })


@app.errorhandler(404)
def not_found(e):
    return jsonify({
        'success': False,
        'error': 'Endpoint not found'
    }), 404


@app.errorhandler(500)
def server_error(e):
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500


if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5002)
