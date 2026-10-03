from flask import Flask, render_template, redirect, url_for, flash, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from wtforms import StringField, TextAreaField, SubmitField, PasswordField, EmailField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import markdown2

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    bio = db.Column(db.Text)
    avatar = db.Column(db.String(200))
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    slug = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text)
    posts = db.relationship('Post', backref='category', lazy=True)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), unique=True, nullable=False)
    summary = db.Column(db.Text)
    content = db.Column(db.Text, nullable=False)
    content_html = db.Column(db.Text)
    featured_image = db.Column(db.String(200))
    view_count = db.Column(db.Integer, default=0)
    is_published = db.Column(db.Boolean, default=True)
    is_featured = db.Column(db.Boolean, default=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    author = db.relationship('User', backref='posts')
    tags = db.relationship('Tag', secondary='post_tags', backref='posts')


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    slug = db.Column(db.String(50), unique=True, nullable=False)


class PostTag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'), nullable=False)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    author_name = db.Column(db.String(100), nullable=False)
    author_email = db.Column(db.String(120), nullable=False)
    is_approved = db.Column(db.Boolean, default=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    post = db.relationship('Post', backref='comments')
    replies = db.relationship('Comment', backref='parent', remote_side=[id])


# Forms
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=80)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        if User.query.filter_by(username=username.data).first():
            raise ValidationError('Username already taken')

    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError('Email already registered')


class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=200)])
    slug = StringField('Slug', validators=[DataRequired(), Length(max=200)])
    summary = TextAreaField('Summary')
    content = TextAreaField('Content (Markdown)', validators=[DataRequired()])
    category = SelectField('Category', coerce=int)
    tags = StringField('Tags (comma separated)')
    featured_image = StringField('Featured Image URL')
    is_published = SelectField('Status', choices=[('1', 'Published'), ('0', 'Draft')])
    is_featured = SelectField('Featured', choices=[('0', 'No'), ('1', 'Yes')])
    submit = SubmitField('Save Post')


class CommentForm(FlaskForm):
    author_name = StringField('Name', validators=[DataRequired(), Length(max=100)])
    author_email = EmailField('Email', validators=[DataRequired(), Email()])
    content = TextAreaField('Comment', validators=[DataRequired(), Length(max=2000)])
    submit = SubmitField('Post Comment')


# Helpers
def get_all_tags():
    return Tag.query.all()


def get_featured_posts(limit=3):
    return Post.query.filter_by(is_published=True, is_featured=True).order_by(Post.created_at.desc()).limit(limit).all()


def get_recent_posts(limit=5):
    return Post.query.filter_by(is_published=True).order_by(Post.created_at.desc()).limit(limit).all()


def get_popular_posts(limit=5):
    return Post.query.filter_by(is_published=True).order_by(Post.view_count.desc()).limit(limit).all()


# Routes - Public
@app.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(is_published=True).order_by(Post.created_at.desc()).paginate(page=page, per_page=10)
    featured = get_featured_posts()
    return render_template('blog/index.html', posts=posts, featured=featured)


@app.route('/post/<slug>')
def post(slug):
    post = Post.query.filter_by(slug=slug, is_published=True).first_or_404()
    post.view_count += 1
    db.session.commit()

    form = CommentForm()
    comments = Comment.query.filter_by(post_id=post.id, is_approved=True, parent_id=None).all()
    related = Post.query.filter(Post.category_id == post.category_id, Post.id != post.id, is_published=True).limit(3).all()

    return render_template('blog/post.html', post=post, form=form, comments=comments, related=related)


@app.route('/category/<slug>')
def category(slug):
    cat = Category.query.filter_by(slug=slug).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(category_id=cat.id, is_published=True).order_by(Post.created_at.desc()).paginate(page=page, per_page=10)
    return render_template('blog/category.html', category=cat, posts=posts)


@app.route('/tag/<slug>')
def tag(slug):
    tag = Tag.query.filter_by(slug=slug).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter(Post.tags.any(id=tag.id), is_published=True).order_by(Post.created_at.desc()).paginate(page=page, per_page=10)
    return render_template('blog/tag.html', tag=tag, posts=posts)


@app.route('/search')
def search():
    query = request.args.get('q', '')
    page = request.args.get('page', 1, type=int)

    if query:
        posts = Post.query.filter(
            (Post.title.contains(query) | Post.content.contains(query)),
            is_published=True
        ).order_by(Post.created_at.desc()).paginate(page=page, per_page=10)
    else:
        posts = None

    return render_template('blog/search.html', posts=posts, query=query)


@app.route('/comment/<int:post_id>', methods=['POST'])
def add_comment(post_id):
    post = Post.query.get_or_404(post_id)
    form = CommentForm()

    if form.validate_on_submit():
        comment = Comment(
            content=form.content.data,
            author_name=form.author_name.data,
            author_email=form.author_email.data,
            post_id=post.id
        )
        db.session.add(comment)
        db.session.commit()
        flash('Comment submitted for review.', 'success')
    else:
        flash('Please fill out all fields correctly.', 'error')

    return redirect(url_for('post', slug=post.slug))


# Routes - Auth
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! Please sign in.', 'success')
        return redirect(url_for('login'))

    return render_template('auth/register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Welcome back!', 'success')
            return redirect(url_for('index'))
        flash('Invalid email or password', 'error')

    return render_template('auth/login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))


# Routes - Admin
@app.route('/admin')
@login_required
def admin():
    if not current_user.is_admin:
        abort(403)

    stats = {
        'posts': Post.query.count(),
        'users': User.query.count(),
        'comments': Comment.query.count(),
        'categories': Category.query.count()
    }
    recent_comments = Comment.query.order_by(Comment.created_at.desc()).limit(5).all()
    recent_posts = get_recent_posts(5)

    return render_template('admin/index.html', stats=stats, comments=recent_comments, posts=recent_posts)


@app.route('/admin/posts')
@login_required
def admin_posts():
    if not current_user.is_admin:
        abort(403)

    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.created_at.desc()).paginate(page=page, per_page=20)
    return render_template('admin/posts.html', posts=posts)


@app.route('/admin/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    if not current_user.is_admin:
        abort(403)

    form = PostForm()
    form.category.choices = [(0, 'No Category')] + [(c.id, c.name) for c in Category.query.all()]

    if form.validate_on_submit():
        content_html = markdown2.markdown(form.content.data)

        post = Post(
            title=form.title.data,
            slug=form.slug.data,
            summary=form.summary.data,
            content=form.content.data,
            content_html=content_html,
            featured_image=form.featured_image.data,
            category_id=form.category.data if form.category.data != 0 else None,
            author_id=current_user.id,
            is_published=form.is_published.data == '1',
            is_featured=form.is_featured.data == '1'
        )

        # Handle tags
        tag_names = [t.strip() for t in form.tags.data.split(',') if t.strip()]
        for name in tag_names:
            tag = Tag.query.filter_by(name=name).first()
            if not tag:
                tag = Tag(name=name, slug=name.lower().replace(' ', '-'))
                db.session.add(tag)
            post.tags.append(tag)

        db.session.add(post)
        db.session.commit()
        flash('Post created successfully!', 'success')
        return redirect(url_for('admin_posts'))

    form.category.choices = [(0, 'No Category')] + [(c.id, c.name) for c in Category.query.all()]
    return render_template('admin/post_edit.html', form=form, post=None)


@app.route('/admin/post/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(id):
    if not current_user.is_admin:
        abort(403)

    post = Post.query.get_or_404(id)
    form = PostForm(obj=post)

    if request.method == 'GET':
        form.tags.data = ', '.join([t.name for t in post.tags])

    if form.validate_on_submit():
        post.title = form.title.data
        post.slug = form.slug.data
        post.summary = form.summary.data
        post.content = form.content.data
        post.content_html = markdown2.markdown(form.content.data)
        post.featured_image = form.featured_image.data
        post.category_id = form.category.data if form.category.data != 0 else None
        post.is_published = form.is_published.data == '1'
        post.is_featured = form.is_featured.data == '1'
        post.updated_at = datetime.utcnow()

        # Update tags
        post.tags.clear()
        tag_names = [t.strip() for t in form.tags.data.split(',') if t.strip()]
        for name in tag_names:
            tag = Tag.query.filter_by(name=name).first()
            if not tag:
                tag = Tag(name=name, slug=name.lower().replace(' ', '-'))
                db.session.add(tag)
            post.tags.append(tag)

        db.session.commit()
        flash('Post updated successfully!', 'success')
        return redirect(url_for('admin_posts'))

    return render_template('admin/post_edit.html', form=form, post=post)


@app.route('/admin/comments')
@login_required
def admin_comments():
    if not current_user.is_admin:
        abort(403)

    page = request.args.get('page', 1, type=int)
    status = request.args.get('status', 'pending')

    query = Comment.query
    if status == 'pending':
        query = query.filter_by(is_approved=False)
    elif status == 'approved':
        query = query.filter_by(is_approved=True)

    comments = query.order_by(Comment.created_at.desc()).paginate(page=page, per_page=20)
    return render_template('admin/comments.html', comments=comments, status=status)


@app.route('/admin/comment/<int:id>/approve')
@login_required
def approve_comment(id):
    if not current_user.is_admin:
        abort(403)

    comment = Comment.query.get_or_404(id)
    comment.is_approved = True
    db.session.commit()
    flash('Comment approved.', 'success')
    return redirect(url_for('admin_comments'))


@app.route('/admin/comment/<int:id>/delete')
@login_required
def delete_comment(id):
    if not current_user.is_admin:
        abort(403)

    comment = Comment.query.get_or_404(id)
    db.session.delete(comment)
    db.session.commit()
    flash('Comment deleted.', 'success')
    return redirect(url_for('admin_comments'))


# Context
@app.context_processor
def inject_categories():
    categories = Category.query.all()
    return dict(categories=categories, get_all_tags=get_all_tags)


@app.cli.command('init-db')
def init_db():
    db.create_all()

    # Create admin user
    if not User.query.filter_by(email='admin@example.com').first():
        admin = User(username='admin', email='admin@example.com', bio='Blog administrator', is_admin=True)
        admin.set_password('admin123')
        db.session.add(admin)

    # Create sample categories
    cats = [
        {'name': 'Technology', 'slug': 'technology', 'description': 'Tech news and tutorials'},
        {'name': 'Design', 'slug': 'design', 'description': 'UI/UX and graphic design'},
        {'name': 'Business', 'slug': 'business', 'description': 'Business and entrepreneurship'},
        {'name': 'Lifestyle', 'slug': 'lifestyle', 'description': 'Life and culture'},
    ]
    for cat in cats:
        if not Category.query.filter_by(slug=cat['slug']).first():
            db.session.add(Category(**cat))

    db.session.commit()
    print('Database initialized. Admin: admin@example.com / admin123')


if __name__ == '__main__':
    app.run(debug=True)
