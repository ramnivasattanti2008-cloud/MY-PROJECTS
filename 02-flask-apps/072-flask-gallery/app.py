from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import sqlite3
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
DATABASE = 'gallery.db'
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    conn = get_db()
    conn.execute('''CREATE TABLE IF NOT EXISTS images
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                     filename TEXT NOT NULL,
                     title TEXT,
                     category TEXT,
                     description TEXT,
                     created_at TEXT DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    category = request.args.get('category')
    conn = get_db()

    if category:
        cursor = conn.execute('SELECT * FROM images WHERE category=? ORDER BY created_at DESC', (category,))
    else:
        cursor = conn.execute('SELECT * FROM images ORDER BY created_at DESC')

    images = cursor.fetchall()

    # Get all unique categories
    cats = conn.execute('SELECT DISTINCT category FROM images WHERE category IS NOT NULL').fetchall()
    categories = [c['category'] for c in cats if c['category']]

    conn.close()
    return render_template('index.html', images=images, categories=categories, selected_category=category)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)

        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # Add timestamp to filename to avoid conflicts
            import time
            filename = f"{int(time.time())}_{filename}"
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            title = request.form['title']
            category = request.form['category']
            description = request.form['description']

            conn = get_db()
            conn.execute('INSERT INTO images (filename, title, category, description) VALUES (?, ?, ?, ?)',
                         (filename, title, category, description))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    conn = get_db()
    cats = conn.execute('SELECT DISTINCT category FROM images WHERE category IS NOT NULL').fetchall()
    categories = [c['category'] for c in cats if c['category']]
    conn.close()
    return render_template('upload.html', categories=categories)

@app.route('/delete/<int:id>')
def delete_image(id):
    conn = get_db()
    cursor = conn.execute('SELECT filename FROM images WHERE id=?', (id,))
    image = cursor.fetchone()

    if image:
        # Delete file
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], image['filename'])
        if os.path.exists(filepath):
            os.remove(filepath)

        conn.execute('DELETE FROM images WHERE id=?', (id,))
        conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/category', methods=['POST'])
def add_category():
    category = request.form['category']
    if category:
        # Categories are stored per image, no separate table needed
        pass
    return redirect(url_for('upload'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
