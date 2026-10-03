from flask import Flask, render_template, request, redirect, url_for, flash, abort
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import sqlite3

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-in-production'
DATABASE = 'microblog.db'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as db:
        db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username VARCHAR(50) UNIQUE NOT NULL,
                email VARCHAR(120) UNIQUE NOT NULL,
                password_hash VARCHAR(256) NOT NULL,
                bio TEXT,
                avatar_color VARCHAR(7) DEFAULT '#6366f1',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        db.execute('''
            CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')

        db.execute('''
            CREATE TABLE IF NOT EXISTS followers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                follower_id INTEGER NOT NULL,
                followed_id INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (follower_id) REFERENCES users(id),
                FOREIGN KEY (followed_id) REFERENCES users(id),
                UNIQUE(follower_id, followed_id)
            )
        ''')

        db.execute('''
            CREATE TABLE IF NOT EXISTS likes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                post_id INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (post_id) REFERENCES posts(id),
                UNIQUE(user_id, post_id)
            )
        ''')

        existing = db.execute('SELECT COUNT(*) as count FROM users').fetchone()['count']
        if existing == 0:
            seed_demo_users(db)

        db.commit()

def seed_demo_users(db):
    demo_users = [
        ('alice', 'alice@example.com', 'password123', 'Tech enthusiast and coffee lover.', '#6366f1'),
        ('bob', 'bob@example.com', 'password123', 'Software developer by day, musician by night.', '#22c55e'),
        ('charlie', 'charlie@example.com', 'password123', 'Design thinking advocate.', '#f59e0b'),
    ]

    for username, email, password, bio, color in demo_users:
        user_id = db.execute(
            'INSERT INTO users (username, email, password_hash, bio, avatar_color) VALUES (?, ?, ?, ?, ?)',
            (username, email, generate_password_hash(password), bio, color)
        ).lastrowid

        sample_posts = [
            f'Hello from {username}! This is my first post.',
            f'Just discovered something amazing today!',
            f'Working on some exciting projects.',
            f'Great meeting with the team today.',
        ]

        for content in sample_posts[:2]:
            db.execute('INSERT INTO posts (user_id, content) VALUES (?, ?)', (user_id, content))

    alice_id = db.execute('SELECT id FROM users WHERE username = ?', ('alice',)).fetchone()['id']
    bob_id = db.execute('SELECT id FROM users WHERE username = ?', ('bob',)).fetchone()['id']
    charlie_id = db.execute('SELECT id FROM users WHERE username = ?', ('charlie',)).fetchone()['id']

    db.execute('INSERT OR IGNORE INTO followers (follower_id, followed_id) VALUES (?, ?)', (alice_id, bob_id))
    db.execute('INSERT OR IGNORE INTO followers (follower_id, followed_id) VALUES (?, ?)', (alice_id, charlie_id))
    db.execute('INSERT OR IGNORE INTO followers (follower_id, followed_id) VALUES (?, ?)', (bob_id, alice_id))

class User(UserMixin):
    def __init__(self, id, username, email, password_hash, bio, avatar_color):
        self.id = id
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.bio = bio
        self.avatar_color = avatar_color

    @staticmethod
    def from_db(user_id):
        with get_db() as db:
            user = db.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
            if user:
                return User(user['id'], user['username'], user['email'],
                          user['password_hash'], user['bio'], user['avatar_color'])
        return None

@login_manager.user_loader
def load_user(user_id):
    return User.from_db(int(user_id))

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('timeline'))

    with get_db() as db:
        recent_posts = db.execute('''
            SELECT posts.*, users.username, users.avatar_color,
                   (SELECT COUNT(*) FROM likes WHERE likes.post_id = posts.id) as like_count
            FROM posts
            JOIN users ON posts.user_id = users.id
            ORDER BY posts.created_at DESC LIMIT 20
        ''').fetchall()

    return render_template('index.html', posts=recent_posts)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('timeline'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        bio = request.form.get('bio', '').strip()

        if not username or not email or not password:
            flash('All fields are required', 'error')
            return render_template('register.html')

        with get_db() as db:
            existing = db.execute(
                'SELECT id FROM users WHERE username = ? OR email = ?',
                (username, email)
            ).fetchone()

            if existing:
                flash('Username or email already exists', 'error')
                return render_template('register.html')

            import random
            colors = ['#6366f1', '#22c55e', '#f59e0b', '#ef4444', '#ec4899', '#14b8a6']
            avatar_color = random.choice(colors)

            user_id = db.execute('''
                INSERT INTO users (username, email, password_hash, bio, avatar_color)
                VALUES (?, ?, ?, ?, ?)
            ''', (username, email, generate_password_hash(password), bio, avatar_color))
            db.commit()

            user = User.from_db(user_id.lastrowid)
            login_user(user)
            return redirect(url_for('timeline'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('timeline'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        if not username or not password:
            flash('Username and password are required', 'error')
            return render_template('login.html')

        with get_db() as db:
            user = db.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()

            if user and check_password_hash(user['password_hash'], password):
                user_obj = User.from_db(user['id'])
                login_user(user_obj)
                return redirect(url_for('timeline'))

            flash('Invalid username or password', 'error')

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/timeline')
@login_required
def timeline():
    with get_db() as db:
        posts = db.execute('''
            SELECT posts.*, users.username, users.avatar_color,
                   (SELECT COUNT(*) FROM likes WHERE likes.post_id = posts.id) as like_count,
                   (SELECT COUNT(*) FROM likes WHERE likes.post_id = posts.id AND likes.user_id = ?) as user_liked
            FROM posts
            JOIN users ON posts.user_id = users.id
            WHERE posts.user_id IN (
                SELECT followed_id FROM followers WHERE follower_id = ?
            ) OR posts.user_id = ?
            ORDER BY posts.created_at DESC
            LIMIT 50
        ''', (current_user.id, current_user.id, current_user.id)).fetchall()

        trending = db.execute('''
            SELECT posts.*, users.username, users.avatar_color,
                   (SELECT COUNT(*) FROM likes WHERE likes.post_id = posts.id) as like_count
            FROM posts
            JOIN users ON posts.user_id = users.id
            ORDER BY like_count DESC, posts.created_at DESC
            LIMIT 5
        ''').fetchall()

    return render_template('timeline.html', posts=posts, trending=trending)

@app.route('/explore')
@login_required
def explore():
    with get_db() as db:
        posts = db.execute('''
            SELECT posts.*, users.username, users.avatar_color,
                   (SELECT COUNT(*) FROM likes WHERE likes.post_id = posts.id) as like_count,
                   (SELECT COUNT(*) FROM likes WHERE likes.post_id = posts.id AND likes.user_id = ?) as user_liked
            FROM posts
            JOIN users ON posts.user_id = users.id
            ORDER BY posts.created_at DESC
            LIMIT 50
        ''', (current_user.id,)).fetchall()

    return render_template('explore.html', posts=posts)

@app.route('/post', methods=['POST'])
@login_required
def create_post():
    content = request.form.get('content', '').strip()

    if not content:
        flash('Post content is required', 'error')
        return redirect(url_for('timeline'))

    if len(content) > 280:
        flash('Post must be 280 characters or less', 'error')
        return redirect(url_for('timeline'))

    with get_db() as db:
        db.execute('INSERT INTO posts (user_id, content) VALUES (?, ?)', (current_user.id, content))
        db.commit()

    return redirect(url_for('timeline'))

@app.route('/delete_post/<int:post_id>', methods=['POST'])
@login_required
def delete_post(post_id):
    with get_db() as db:
        post = db.execute('SELECT * FROM posts WHERE id = ? AND user_id = ?', (post_id, current_user.id)).fetchone()
        if post:
            db.execute('DELETE FROM likes WHERE post_id = ?', (post_id,))
            db.execute('DELETE FROM posts WHERE id = ?', (post_id,))
            db.commit()
    return redirect(request.referrer or url_for('timeline'))

@app.route('/like/<int:post_id>', methods=['POST'])
@login_required
def like_post(post_id):
    with get_db() as db:
        existing = db.execute(
            'SELECT id FROM likes WHERE user_id = ? AND post_id = ?',
            (current_user.id, post_id)
        ).fetchone()

        if existing:
            db.execute('DELETE FROM likes WHERE user_id = ? AND post_id = ?', (current_user.id, post_id))
        else:
            db.execute('INSERT INTO likes (user_id, post_id) VALUES (?, ?)', (current_user.id, post_id))

        db.commit()

    return redirect(request.referrer or url_for('timeline'))

@app.route('/user/<username>')
@login_required
def profile(username):
    with get_db() as db:
        user = db.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        if not user:
            abort(404)

        posts = db.execute('''
            SELECT posts.*, users.username, users.avatar_color,
                   (SELECT COUNT(*) FROM likes WHERE likes.post_id = posts.id) as like_count,
                   (SELECT COUNT(*) FROM likes WHERE likes.post_id = posts.id AND likes.user_id = ?) as user_liked
            FROM posts
            JOIN users ON posts.user_id = users.id
            WHERE posts.user_id = ?
            ORDER BY posts.created_at DESC
        ''', (current_user.id, user['id'])).fetchall()

        followers_count = db.execute(
            'SELECT COUNT(*) as count FROM followers WHERE followed_id = ?', (user['id'],)
        ).fetchone()['count']

        following_count = db.execute(
            'SELECT COUNT(*) as count FROM followers WHERE follower_id = ?', (user['id'],)
        ).fetchone()['count']

        is_following = db.execute(
            'SELECT id FROM followers WHERE follower_id = ? AND followed_id = ?',
            (current_user.id, user['id'])
        ).fetchone() is not None

    return render_template('profile.html', profile_user=dict(user),
                         posts=posts, followers_count=followers_count,
                         following_count=following_count, is_following=is_following)

@app.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
    with get_db() as db:
        user = db.execute('SELECT id FROM users WHERE username = ?', (username,)).fetchone()
        if user and user['id'] != current_user.id:
            existing = db.execute(
                'SELECT id FROM followers WHERE follower_id = ? AND followed_id = ?',
                (current_user.id, user['id'])
            ).fetchone()

            if existing:
                db.execute('DELETE FROM followers WHERE follower_id = ? AND followed_id = ?',
                          (current_user.id, user['id']))
            else:
                db.execute('INSERT INTO followers (follower_id, followed_id) VALUES (?, ?)',
                          (current_user.id, user['id']))
            db.commit()

    return redirect(url_for('profile', username=username))

@app.route('/users')
@login_required
def users():
    with get_db() as db:
        users_list = db.execute('''
            SELECT users.*,
                   (SELECT COUNT(*) FROM followers WHERE followed_id = users.id) as followers,
                   (SELECT COUNT(*) FROM posts WHERE user_id = users.id) as posts_count
            FROM users
            WHERE users.id != ?
            ORDER BY followers DESC
            LIMIT 20
        ''', (current_user.id,)).fetchall()
    return render_template('users.html', users=users_list)

@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        bio = request.form.get('bio', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')

        with get_db() as db:
            if email and email != current_user.email:
                existing = db.execute('SELECT id FROM users WHERE email = ? AND id != ?',
                                     (email, current_user.id)).fetchone()
                if existing:
                    flash('Email already in use', 'error')
                    return render_template('settings.html')

            if password:
                db.execute('UPDATE users SET bio = ?, email = ?, password_hash = ? WHERE id = ?',
                          (bio, email, generate_password_hash(password), current_user.id))
            else:
                db.execute('UPDATE users SET bio = ?, email = ? WHERE id = ?',
                          (bio, email, current_user.id))
            db.commit()

            flash('Settings updated', 'success')
            return redirect(url_for('profile', username=current_user.username))

    return render_template('settings.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5004)
