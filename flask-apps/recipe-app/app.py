from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    ingredients = db.Column(db.Text, nullable=False)
    instructions = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    prep_time = db.Column(db.Integer, default=0)
    cook_time = db.Column(db.Integer, default=0)
    servings = db.Column(db.Integer, default=1)
    rating = db.Column(db.Float, default=0)
    rating_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


@app.route('/')
def index():
    category = request.args.get('category')
    search = request.args.get('search')

    query = Recipe.query
    if category:
        query = query.filter_by(category=category)
    if search:
        query = query.filter(Recipe.name.ilike(f'%{search}%'))

    recipes = query.order_by(Recipe.created_at.desc()).all()
    categories = db.session.query(Recipe.category).distinct().all()
    categories = [c[0] for c in categories]

    return render_template('index.html', recipes=recipes, categories=categories,
                           selected_category=category, search_query=search)


@app.route('/add', methods=['GET', 'POST'])
def add_recipe():
    if request.method == 'POST':
        recipe = Recipe(
            name=request.form['name'],
            description=request.form.get('description', ''),
            ingredients=request.form['ingredients'],
            instructions=request.form['instructions'],
            category=request.form['category'],
            prep_time=int(request.form.get('prep_time', 0)),
            cook_time=int(request.form.get('cook_time', 0)),
            servings=int(request.form.get('servings', 1))
        )
        db.session.add(recipe)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('add_recipe.html')


@app.route('/recipe/<int:id>')
def recipe_detail(id):
    recipe = Recipe.query.get_or_404(id)
    return render_template('recipe_detail.html', recipe=recipe)


@app.route('/recipe/<int:id>/rate', methods=['POST'])
def rate_recipe(id):
    recipe = Recipe.query.get_or_404(id)
    rating = int(request.form['rating'])

    total_rating = recipe.rating * recipe.rating_count + rating
    recipe.rating_count += 1
    recipe.rating = total_rating / recipe.rating_count

    db.session.commit()
    return redirect(url_for('recipe_detail', id=id))


@app.route('/recipe/<int:id>/delete', methods=['POST'])
def delete_recipe(id):
    recipe = Recipe.query.get_or_404(id)
    db.session.delete(recipe)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_recipe(id):
    recipe = Recipe.query.get_or_404(id)

    if request.method == 'POST':
        recipe.name = request.form['name']
        recipe.description = request.form.get('description', '')
        recipe.ingredients = request.form['ingredients']
        recipe.instructions = request.form['instructions']
        recipe.category = request.form['category']
        recipe.prep_time = int(request.form.get('prep_time', 0))
        recipe.cook_time = int(request.form.get('cook_time', 0))
        recipe.servings = int(request.form.get('servings', 1))
        db.session.commit()
        return redirect(url_for('recipe_detail', id=id))

    return render_template('edit_recipe.html', recipe=recipe)


def init_db():
    with app.app_context():
        db.create_all()
        if not Recipe.query.first():
            sample_recipes = [
                Recipe(
                    name='Classic Pasta Carbonara',
                    description='Creamy Italian pasta with bacon and parmesan',
                    ingredients='400g spaghetti\n200g bacon\n4 egg yolks\n100g parmesan cheese\nBlack pepper\nSalt',
                    instructions='1. Cook pasta according to package directions\n2. Fry bacon until crispy\n3. Mix egg yolks with cheese\n4. Combine hot pasta with bacon\n5. Add egg mixture off heat\n6. Season with pepper',
                    category='Italian',
                    prep_time=10,
                    cook_time=20,
                    servings=4,
                    rating=4.5,
                    rating_count=10
                ),
                Recipe(
                    name='Vegetable Stir Fry',
                    description='Quick and healthy Asian-style vegetables',
                    ingredients='2 cups mixed vegetables\n2 tbsp soy sauce\n1 tbsp sesame oil\n2 cloves garlic\nGinger\nCornstarch slurry',
                    instructions='1. Heat oil in wok\n2. Add garlic and ginger\n3. Add vegetables\n4. Stir fry 5 minutes\n5. Add soy sauce\n6. Thicken with cornstarch',
                    category='Asian',
                    prep_time=15,
                    cook_time=10,
                    servings=2,
                    rating=4.2,
                    rating_count=5
                ),
                Recipe(
                    name='Chocolate Chip Cookies',
                    description='Classic homemade cookies',
                    ingredients='2 cups flour\n1 cup butter\n3/4 cup sugar\n3/4 cup brown sugar\n2 eggs\n2 cups chocolate chips',
                    instructions='1. Cream butter and sugars\n2. Beat in eggs\n3. Mix in flour\n4. Fold in chocolate chips\n5. Bake at 375F for 10 minutes',
                    category='Dessert',
                    prep_time=15,
                    cook_time=10,
                    servings=24,
                    rating=4.8,
                    rating_count=15
                )
            ]
            for recipe in sample_recipes:
                db.session.add(recipe)
            db.session.commit()


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
