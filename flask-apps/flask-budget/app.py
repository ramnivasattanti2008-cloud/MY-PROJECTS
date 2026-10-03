from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'budget-secret-key'
DATABASE = 'budget.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS budgets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            month TEXT NOT NULL,
            amount REAL NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            budget_id INTEGER,
            description TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT,
            date TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (budget_id) REFERENCES budgets(id)
        )
    ''')
    conn.commit()
    conn.close()

init_db()

def get_current_month():
    return datetime.now().strftime('%Y-%m')

@app.route('/')
def index():
    current_month = request.args.get('month', get_current_month())

    conn = get_db()
    budget = conn.execute('SELECT * FROM budgets WHERE month=?', (current_month,)).fetchone()
    expenses = conn.execute(
        'SELECT * FROM expenses WHERE budget_id=? ORDER BY date DESC',
        (budget['id'],)
    ).fetchall() if budget else []

    total_spent = sum(e['amount'] for e in expenses)
    remaining = budget['amount'] - total_spent if budget else 0
    percentage = (total_spent / budget['amount'] * 100) if budget and budget['amount'] > 0 else 0

    # Category breakdown
    categories = conn.execute('''
        SELECT category, SUM(amount) as total
        FROM expenses
        WHERE budget_id=? AND category IS NOT NULL
        GROUP BY category
    ''', (budget['id'],) if budget else (None,)).fetchall()

    # Get all months with budgets
    months = conn.execute('SELECT DISTINCT month FROM budgets ORDER BY month DESC').fetchall()

    conn.close()
    return render_template('index.html', budget=budget, expenses=expenses,
                           total_spent=total_spent, remaining=remaining,
                           percentage=percentage, categories=categories,
                           current_month=current_month, months=[m['month'] for m in months])

@app.route('/set-budget', methods=['POST'])
def set_budget():
    month = request.form['month']
    amount = float(request.form['amount'])

    conn = get_db()
    existing = conn.execute('SELECT * FROM budgets WHERE month=?', (month,)).fetchone()

    if existing:
        conn.execute('UPDATE budgets SET amount=? WHERE month=?', (amount, month))
        flash(f'Budget for {month} updated!', 'success')
    else:
        conn.execute('INSERT INTO budgets (month, amount) VALUES (?, ?)', (month, amount))
        # Create budget and get ID
        budget = conn.execute('SELECT * FROM budgets WHERE month=?', (month,)).fetchone()
        conn.execute('UPDATE budgets SET id=id WHERE id=?', (budget['id'],))
        flash(f'Budget for {month} set!', 'success')

    conn.commit()
    conn.close()
    return redirect(url_for('index', month=month))

@app.route('/add-expense', methods=['POST'])
def add_expense():
    budget_id = request.form['budget_id']
    description = request.form['description']
    amount = float(request.form['amount'])
    category = request.form.get('category', '')
    date = request.form.get('date', datetime.now().strftime('%Y-%m-%d'))

    conn = get_db()
    conn.execute(
        'INSERT INTO expenses (budget_id, description, amount, category, date) VALUES (?, ?, ?, ?, ?)',
        (budget_id, description, amount, category, date)
    )
    conn.commit()

    # Check budget
    budget = conn.execute('SELECT * FROM budgets WHERE id=?', (budget_id,)).fetchone()
    total_spent = conn.execute('SELECT SUM(amount) as total FROM expenses WHERE budget_id=?', (budget_id,)).fetchone()['total'] or 0

    if total_spent > budget['amount']:
        flash(f'Warning: You have exceeded your budget!', 'danger')
    elif total_spent > budget['amount'] * 0.8:
        flash(f'Warning: You have used over 80% of your budget.', 'warning')

    conn.close()
    return redirect(url_for('index', month=budget['month']))

@app.route('/delete-expense/<int:id>')
def delete_expense(id):
    conn = get_db()
    expense = conn.execute('SELECT * FROM expenses WHERE id=?', (id,)).fetchone()
    conn.execute('DELETE FROM expenses WHERE id=?', (id,))
    conn.commit()
    conn.close()

    flash('Expense deleted.', 'info')
    return redirect(url_for('index'))

@app.route('/edit-expense/<int:id>', methods=['GET', 'POST'])
def edit_expense(id):
    conn = get_db()

    if request.method == 'POST':
        description = request.form['description']
        amount = float(request.form['amount'])
        category = request.form.get('category', '')
        date = request.form.get('date', '')

        conn.execute(
            'UPDATE expenses SET description=?, amount=?, category=?, date=? WHERE id=?',
            (description, amount, category, date, id)
        )
        conn.commit()

        expense = conn.execute('SELECT * FROM expenses WHERE id=?', (id,)).fetchone()
        budget = conn.execute('SELECT * FROM budgets WHERE id=?', (expense['budget_id'],)).fetchone()

        conn.close()
        return redirect(url_for('index', month=budget['month']))

    expense = conn.execute('SELECT * FROM expenses WHERE id=?', (id,)).fetchone()
    conn.close()
    return render_template('edit_expense.html', expense=expense)

if __name__ == '__main__':
    app.run(debug=True)
