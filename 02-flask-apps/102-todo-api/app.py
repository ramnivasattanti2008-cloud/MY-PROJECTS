from datetime import datetime
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    completed = db.Column(db.Boolean, default=False)
    priority = db.Column(db.String(20), default='medium')
    tags = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    due_date = db.Column(db.DateTime, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'completed': self.completed,
            'priority': self.priority,
            'tags': self.tags.split(',') if self.tags else [],
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'due_date': self.due_date.isoformat() if self.due_date else None
        }


def parse_tags(tags_str):
    if not tags_str:
        return None
    return ','.join(tag.strip() for tag in tags_str.split(',') if tag.strip())


@app.route('/api/todos', methods=['GET'])
def get_todos():
    query = Todo.query

    completed = request.args.get('completed')
    if completed is not None:
        query = query.filter_by(completed=completed.lower() == 'true')

    priority = request.args.get('priority')
    if priority:
        query = query.filter_by(priority=priority.lower())

    tag = request.args.get('tag')
    if tag:
        query = query.filter(Todo.tags.contains(tag))

    search = request.args.get('search')
    if search:
        search_term = f'%{search}%'
        query = query.filter(
            db.or_(
                Todo.title.ilike(search_term),
                Todo.description.ilike(search_term)
            )
        )

    todos = query.order_by(Todo.created_at.desc()).all()
    return jsonify([todo.to_dict() for todo in todos])


@app.route('/api/todos', methods=['POST'])
def create_todo():
    data = request.get_json()

    if not data.get('title'):
        return jsonify({'error': 'Title is required'}), 400

    priority = data.get('priority', 'medium')
    if priority not in ['low', 'medium', 'high']:
        priority = 'medium'

    due_date = None
    if data.get('due_date'):
        try:
            due_date = datetime.fromisoformat(data['due_date'].replace('Z', '+00:00'))
        except ValueError:
            return jsonify({'error': 'Invalid due_date format'}), 400

    todo = Todo(
        title=data['title'],
        description=data.get('description', ''),
        completed=data.get('completed', False),
        priority=priority,
        tags=parse_tags(data.get('tags', '')),
        due_date=due_date
    )
    db.session.add(todo)
    db.session.commit()

    return jsonify(todo.to_dict()), 201


@app.route('/api/todos/<int:todo_id>', methods=['GET'])
def get_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    return jsonify(todo.to_dict())


@app.route('/api/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    data = request.get_json()

    if 'title' in data:
        todo.title = data['title']
    if 'description' in data:
        todo.description = data['description']
    if 'completed' in data:
        todo.completed = data['completed']
    if 'priority' in data:
        if data['priority'] in ['low', 'medium', 'high']:
            todo.priority = data['priority']
    if 'tags' in data:
        todo.tags = parse_tags(data['tags'])
    if 'due_date' in data:
        if data['due_date']:
            try:
                todo.due_date = datetime.fromisoformat(data['due_date'].replace('Z', '+00:00'))
            except ValueError:
                return jsonify({'error': 'Invalid due_date format'}), 400
        else:
            todo.due_date = None

    db.session.commit()
    return jsonify(todo.to_dict())


@app.route('/api/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    db.session.delete(todo)
    db.session.commit()
    return jsonify({'message': 'Todo deleted successfully'})


@app.route('/api/todos/stats', methods=['GET'])
def get_stats():
    total = Todo.query.count()
    completed = Todo.query.filter_by(completed=True).count()
    pending = total - completed
    high_priority_pending = Todo.query.filter_by(completed=False, priority='high').count()

    return jsonify({
        'total': total,
        'completed': completed,
        'pending': pending,
        'high_priority_pending': high_priority_pending
    })


@app.route('/api/todos/bulk', methods=['POST'])
def bulk_update():
    data = request.get_json()
    action = data.get('action')

    if action == 'complete':
        ids = data.get('ids', [])
        Todo.query.filter(Todo.id.in_(ids)).update({Todo.completed: True}, synchronize_session=False)
    elif action == 'uncomplete':
        ids = data.get('ids', [])
        Todo.query.filter(Todo.id.in_(ids)).update({Todo.completed: False}, synchronize_session=False)
    elif action == 'delete':
        ids = data.get('ids', [])
        Todo.query.filter(Todo.id.in_(ids)).delete(synchronize_session=False)
    else:
        return jsonify({'error': 'Invalid action'}), 400

    db.session.commit()
    return jsonify({'message': f'Action {action} completed'})


@app.route('/')
def index():
    return jsonify({
        'message': 'Todo API',
        'version': '1.0',
        'endpoints': {
            'GET /api/todos': 'List all todos',
            'POST /api/todos': 'Create a todo',
            'GET /api/todos/<id>': 'Get a specific todo',
            'PUT /api/todos/<id>': 'Update a todo',
            'DELETE /api/todos/<id>': 'Delete a todo',
            'GET /api/todos/stats': 'Get statistics'
        }
    })


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5003)
