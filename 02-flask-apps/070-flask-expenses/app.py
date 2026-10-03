from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import func

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-key-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expenses.db'
db = SQLAlchemy(app)


class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(100))
    date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


@app.route('/')
def index():
    month = request.args.get('month')
    year = request.args.get('year')
    query = Expense.query

    if month and year:
        query = query.filter(
            func.strftime('%m', Expense.date) == month.zfill(2),
            func.strftime('%Y', Expense.date) == year
        )

    expenses = query.order_by(Expense.date.desc()).all()

    total = db.session.query(func.sum(Expense.amount)).scalar() or 0
    total_filtered = db.session.query(func.sum(Expense.amount)).filter(
        Expense.date >= datetime(int(year), int(month), 1).date() if month and year else True
    ).scalar() or 0

    category_totals = db.session.query(
        Expense.category,
        func.sum(Expense.amount)
    ).group_by(Expense.category).all()

    return render_template('index.html', expenses=expenses, total=total,
                           total_filtered=total_filtered, category_totals=category_totals,
                           selected_month=month, selected_year=year)


@app.route('/add', methods=['GET', 'POST'])
def add_expense():
    if request.method == 'POST':
        expense = Expense(
            description=request.form['description'],
            amount=float(request.form['amount']),
            category=request.form['category'] or 'Other',
            date=datetime.strptime(request.form['date'], '%Y-%m-%d').date()
        )
        db.session.add(expense)
        db.session.commit()
        flash('Expense added!', 'success')
        return redirect(url_for('index'))
    return render_template('add.html', today=datetime.now().strftime('%Y-%m-%d'))


@app.route('/delete/<int:id>')
def delete_expense(id):
    expense = Expense.query.get_or_404(id)
    db.session.delete(expense)
    db.session.commit()
    flash('Expense deleted.', 'info')
    return redirect(url_for('index'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5004)
