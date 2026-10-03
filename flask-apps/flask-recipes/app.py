from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-key-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipes.db'
db = SQLAlchemy(app)


class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    ingredients = db.Column(db.Text, nullable=False)
    instructions = db.Column(db.Text, nullable=False)
    prep_time = db.Column(db.Integer)
    cook_time = db.Column(db.Integer)
    servings = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


@app.route('/')
def index():
    search = request.args.get('search', '')
    if search:
        recipes = Recipe.query.filter(
            (Recipe.name.contains(search)) |
            (Recipe.description.contains(search))
        ).order_by(Recipe.created_at.desc()).all()
    else:
        recipes = Recipe.query.order_by(Recipe.created_at.desc()).all()
    return render_template('index.html', recipes=recipes, search=search)


@app.route('/recipe/<int:id>')
def detail(id):
    recipe = Recipe.query.get_or_404(id)
    return render_template('detail.html', recipe=recipe)


@app.route('/add', methods=['GET', 'POST'])
def add_recipe():
    if request.method == 'POST':
        recipe = Recipe(
            name=request.form['name'],
            description=request.form['description'],
            ingredients=request.form['ingredients'],
            instructions=request.form['instructions'],
            prep_time=int(request.form['prep_time']) if request.form.get('prep_time') else None,
            cook_time=int(request.form['cook_time']) if request.form.get('cook_time') else None,
            servings=int(request.form['servings']) if request.form.get('servings') else None
        )
        db.session.add(recipe)
        db.session.commit()
        flash('Recipe added!', 'success')
        return redirect(url_for('index'))
    return render_template('add.html')


@app.route('/delete/<int:id>')
def delete_recipe(id):
    recipe = Recipe.query.get_or_404(id)
    db.session.delete(recipe)
    db.session.commit()
    flash('Recipe deleted.', 'info')
    return redirect(url_for('index'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5005)
