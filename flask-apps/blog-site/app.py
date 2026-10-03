from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
import markdown

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(255), unique=True, nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(100), default='Anonymous')
    tags = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    published = db.Column(db.Boolean, default=True)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'slug': self.slug,
            'content': self.content,
            'author': self.author,
            'tags': self.tags.split(',') if self.tags else [],
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'published': self.published
        }


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    author = db.Column(db.String(100), default='Anonymous')
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'post_id': self.post_id,
            'author': self.author,
            'content': self.content,
            'created_at': self.created_at.isoformat()
        }


def generate_slug(title):
    slug = title.lower().replace(' ', '-')
    slug = ''.join(c for c in slug if c.isalnum() or c == '-')
    original_slug = slug
    counter = 1
    while Post.query.filter_by(slug=slug).first():
        slug = f"{original_slug}-{counter}"
        counter += 1
    return slug


@app.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    tag = request.args.get('tag', '')
    search = request.args.get('search', '')

    query = Post.query.filter_by(published=True)

    if tag:
        query = query.filter(Post.tags.contains(tag))
    if search:
        query = query.filter(
            db.or_(
                Post.title.ilike(f'%{search}%'),
                Post.content.ilike(f'%{search}%')
            )
        )

    posts = query.order_by(Post.created_at.desc()).paginate(page=page, per_page=10)
    all_tags = db.session.query(db.func.distinct(db.func.substr(Post.tags, 1, db.func.instr(Post.tags, ',') - 1))).all()
    all_tags = [t[0] for t in all_tags if t[0]]

    return render_template('index.html', posts=posts, current_tag=tag, search=search)


@app.route('/post/<slug>')
def view_post(slug):
    post = Post.query.filter_by(slug=slug, published=True).first_or_404()
    comments = Comment.query.filter_by(post_id=post.id).order_by(Comment.created_at.asc()).all()
    content_html = markdown.markdown(post.content, extensions=['fenced_code', 'codehilite'])
    return render_template('post.html', post=post, content_html=content_html, comments=comments)


@app.route('/create', methods=['GET', 'POST'])
def create_post():
    if request.method == 'POST':
        data = request.form
        title = data.get('title', '').strip()
        content = data.get('content', '').strip()
        author = data.get('author', 'Anonymous').strip()
        tags = data.get('tags', '').strip()

        if not title or not content:
            return render_template('create.html', error='Title and content are required')

        slug = generate_slug(title)
        post = Post(title=title, slug=slug, content=content, author=author, tags=tags)
        db.session.add(post)
        db.session.commit()

        return redirect(url_for('view_post', slug=slug))

    return render_template('create.html')


@app.route('/post/<slug>/comment', methods=['POST'])
def add_comment(slug):
    post = Post.query.filter_by(slug=slug, published=True).first_or_404()
    data = request.get_json()

    author = data.get('author', 'Anonymous').strip()
    content = data.get('content', '').strip()

    if not content:
        return jsonify({'error': 'Comment content is required'}), 400

    comment = Comment(post_id=post.id, author=author, content=content)
    db.session.add(comment)
    db.session.commit()

    return jsonify(comment.to_dict()), 201


@app.route('/api/posts')
def api_posts():
    posts = Post.query.filter_by(published=True).order_by(Post.created_at.desc()).all()
    return jsonify([post.to_dict() for post in posts])


@app.route('/api/posts/<slug>')
def api_post(slug):
    post = Post.query.filter_by(slug=slug, published=True).first_or_404()
    return jsonify(post.to_dict())


@app.route('/api/posts/<slug>', methods=['DELETE'])
def delete_post(slug):
    post = Post.query.filter_by(slug=slug).first_or_404()
    db.session.delete(post)
    db.session.commit()
    return jsonify({'message': 'Post deleted successfully'})


@app.route('/api/tags')
def api_tags():
    posts = Post.query.filter_by(published=True).all()
    tags = set()
    for post in posts:
        if post.tags:
            for tag in post.tags.split(','):
                tags.add(tag.strip())
    return jsonify(sorted(list(tags)))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5004)
