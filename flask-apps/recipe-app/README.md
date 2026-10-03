# Recipe Manager

A Flask-based recipe management application with search, categories, and ratings.

## Features

- Add, edit, and delete recipes
- Categorize recipes (Breakfast, Lunch, Dinner, Dessert, etc.)
- Search recipes by name
- Filter by category
- Rate recipes (1-5 stars)
- Track prep time, cook time, and servings
- SQLite database for persistence

## Installation

```bash
cd recipe-app
pip install -r requirements.txt
python app.py
```

## Usage

1. Open your browser to `http://localhost:5000`
2. View existing recipes or add new ones
3. Search by name or filter by category
4. Rate recipes you have tried

## Database

The app uses SQLite and creates `recipes.db` automatically on first run.
Sample recipes are loaded if the database is empty.

## Project Structure

```
recipe-app/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── templates/          # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── add_recipe.html
│   ├── recipe_detail.html
│   └── edit_recipe.html
└── README.md
```
