from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-key-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
db = SQLAlchemy(app)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    priority = db.Column(db.String(20), default='medium')
    completed = db.Column(db.Boolean, default=False)
    due_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


@app.route('/')
def index():
    filter_type = request.args.get('filter', 'all')
    if filter_type == 'active':
        tasks = Task.query.filter_by(completed=False).order_by(Task.created_at.desc()).all()
    elif filter_type == 'completed':
        tasks = Task.query.filter_by(completed=True).order_by(Task.created_at.desc()).all()
    else:
        tasks = Task.query.order_by(Task.created_at.desc()).all()

    active_count = Task.query.filter_by(completed=False).count()
    completed_count = Task.query.filter_by(completed=True).count()
    return render_template('index.html', tasks=tasks, filter_type=filter_type,
                           active_count=active_count, completed_count=completed_count)


@app.route('/add', methods=['GET', 'POST'])
def add_task():
    if request.method == 'POST':
        due = None
        if request.form.get('due_date'):
            due = datetime.strptime(request.form['due_date'], '%Y-%m-%d').date()
        task = Task(
            title=request.form['title'],
            description=request.form['description'],
            priority=request.form['priority'],
            due_date=due
        )
        db.session.add(task)
        db.session.commit()
        flash('Task added!', 'success')
        return redirect(url_for('index'))
    return render_template('add.html')


@app.route('/complete/<int:id>')
def complete_task(id):
    task = Task.query.get_or_404(id)
    task.completed = not task.completed
    db.session.commit()
    flash(f'Task marked as {"completed" if task.completed else "active"}.', 'success')
    return redirect(url_for('index'))


@app.route('/delete/<int:id>')
def delete_task(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    flash('Task deleted.', 'info')
    return redirect(url_for('index'))


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_task(id):
    task = Task.query.get_or_404(id)
    if request.method == 'POST':
        task.title = request.form['title']
        task.description = request.form['description']
        task.priority = request.form['priority']
        if request.form.get('due_date'):
            task.due_date = datetime.strptime(request.form['due_date'], '%Y-%m-%d').date()
        else:
            task.due_date = None
        db.session.commit()
        flash('Task updated!', 'success')
        return redirect(url_for('index'))
    return render_template('edit.html', task=task)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5003)
