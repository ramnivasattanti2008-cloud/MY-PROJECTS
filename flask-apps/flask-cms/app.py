from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'cms-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cms.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Page(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), unique=True, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), unique=True, nullable=False)
    content = db.Column(db.Text, nullable=False)
    published = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()
    if not Page.query.first():
        home = Page(title='Home', slug='home', content='Welcome to our CMS. This is the homepage.')
        about = Page(title='About', slug='about', content='About us page content goes here.')
        db.session.add_all([home, about])
    if not Post.query.first():
        p1 = Post(title='First Post', slug='first-post', content='This is our first blog post.', published=True)
        p2 = Post(title='Second Post', slug='second-post', content='Another interesting article.', published=True)
        db.session.add_all([p1, p2])
    db.session.commit()

@app.route('/')
def index():
    posts = Post.query.filter_by(published=True).order_by(Post.created_at.desc()).all()
    return render_template('index.html', posts=posts)

@app.route('/page/<slug>')
def page(slug):
    page = Page.query.filter_by(slug=slug).first_or_404()
    return render_template('page.html', page=page)

@app.route('/post/<slug>')
def post(slug):
    post = Post.query.filter_by(slug=slug, published=True).first_or_404()
    return render_template('post.html', post=post)

@app.route('/admin')
def admin():
    pages = Page.query.all()
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template('admin.html', pages=pages, posts=posts)

@app.route('/admin/page/new', methods=['GET', 'POST'])
def new_page():
    if request.method == 'POST':
        page = Page(
            title=request.form['title'],
            slug=request.form['slug'],
            content=request.form['content']
        )
        db.session.add(page)
        db.session.commit()
        return redirect(url_for('admin'))
    return render_template('page_form.html', action='Create')

@app.route('/admin/post/new', methods=['GET', 'POST'])
def new_post():
    if request.method == 'POST':
        post = Post(
            title=request.form['title'],
            slug=request.form['slug'],
            content=request.form['content'],
            published='published' in request.form
        )
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('admin'))
    return render_template('post_form.html', action='Create')

@app.route('/admin/page/<int:id>/delete', methods=['POST'])
def delete_page(id):
    page = Page.query.get_or_404(id)
    db.session.delete(page)
    db.session.commit()
    return redirect(url_for('admin'))

@app.route('/admin/post/<int:id>/delete', methods=['POST'])
def delete_post(id):
    post = Post.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('admin'))

@app.route('/admin/post/<int:id>/toggle', methods=['POST'])
def toggle_post(id):
    post = Post.query.get_or_404(id)
    post.published = not post.published
    db.session.commit()
    return redirect(url_for('admin'))

if __name__ == '__main__':
    app.run(debug=True)
