from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from cryptography.fernet import Fernet
import hashlib
import os
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vault.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production')

db = SQLAlchemy(app)

KEY_FILE = 'vault.key'


def get_key():
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, 'rb') as f:
            return f.read()
    key = Fernet.generate_key()
    with open(KEY_FILE, 'wb') as f:
        f.write(key)
    return key


def get_fernet():
    return Fernet(get_key())


def encrypt_password(password):
    fernet = get_fernet()
    return fernet.encrypt(password.encode()).decode()


def decrypt_password(encrypted):
    fernet = get_fernet()
    return fernet.decrypt(encrypted.encode()).decode()


def hash_master_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


class PasswordEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), nullable=True)
    password = db.Column(db.String(500), nullable=False)
    url = db.Column(db.String(200), nullable=True)
    notes = db.Column(db.Text, nullable=True)
    tags = db.Column(db.String(200), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class MasterPassword(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    password_hash = db.Column(db.String(64), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


@app.route('/')
def index():
    if 'authenticated' not in session:
        return redirect(url_for('login'))

    tag_filter = request.args.get('tag')
    search = request.args.get('search')

    query = PasswordEntry.query

    if tag_filter:
        query = query.filter(PasswordEntry.tags.ilike(f'%{tag_filter}%'))

    if search:
        query = query.filter(
            PasswordEntry.title.ilike(f'%{search}%') |
            PasswordEntry.username.ilike(f'%{search}%') |
            PasswordEntry.notes.ilike(f'%{search}%')
        )

    entries = query.order_by(PasswordEntry.created_at.desc()).all()

    all_tags = set()
    for entry in PasswordEntry.query.all():
        if entry.tags:
            for tag in entry.tags.split(','):
                all_tags.add(tag.strip())
    all_tags = sorted(all_tags)

    return render_template('index.html', entries=entries, all_tags=all_tags,
                           tag_filter=tag_filter, search_query=search)


@app.route('/setup', methods=['GET', 'POST'])
def setup():
    if MasterPassword.query.first():
        return redirect(url_for('login'))

    if request.method == 'POST':
        password = request.form['password']
        confirm = request.form['confirm']

        if password != confirm:
            flash('Passwords do not match', 'error')
            return render_template('setup.html')

        if len(password) < 8:
            flash('Password must be at least 8 characters', 'error')
            return render_template('setup.html')

        master = MasterPassword(password_hash=hash_master_password(password))
        db.session.add(master)
        db.session.commit()

        flash('Master password set successfully', 'success')
        return redirect(url_for('login'))

    return render_template('setup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    master = MasterPassword.query.first()
    if not master:
        return redirect(url_for('setup'))

    if request.method == 'POST':
        password = request.form['password']

        if hash_master_password(password) == master.password_hash:
            session['authenticated'] = True
            session['master_id'] = master.id
            return redirect(url_for('index'))
        else:
            flash('Incorrect password', 'error')

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/add', methods=['GET', 'POST'])
def add_entry():
    if 'authenticated' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        entry = PasswordEntry(
            title=request.form['title'],
            username=request.form.get('username', ''),
            password=encrypt_password(request.form['password']),
            url=request.form.get('url', ''),
            notes=request.form.get('notes', ''),
            tags=request.form.get('tags', '')
        )
        db.session.add(entry)
        db.session.commit()
        flash('Password saved successfully', 'success')
        return redirect(url_for('index'))

    return render_template('add_entry.html')


@app.route('/entry/<int:id>')
def view_entry(id):
    if 'authenticated' not in session:
        return redirect(url_for('login'))

    entry = PasswordEntry.query.get_or_404(id)
    decrypted_password = decrypt_password(entry.password)

    return render_template('view_entry.html', entry=entry,
                           decrypted_password=decrypted_password)


@app.route('/entry/<int:id>/edit', methods=['GET', 'POST'])
def edit_entry(id):
    if 'authenticated' not in session:
        return redirect(url_for('login'))

    entry = PasswordEntry.query.get_or_404(id)

    if request.method == 'POST':
        entry.title = request.form['title']
        entry.username = request.form.get('username', '')
        entry.password = encrypt_password(request.form['password'])
        entry.url = request.form.get('url', '')
        entry.notes = request.form.get('notes', '')
        entry.tags = request.form.get('tags', '')
        db.session.commit()
        flash('Entry updated', 'success')
        return redirect(url_for('view_entry', id=id))

    decrypted_password = decrypt_password(entry.password)
    return render_template('edit_entry.html', entry=entry,
                           decrypted_password=decrypted_password)


@app.route('/entry/<int:id>/delete', methods=['POST'])
def delete_entry(id):
    if 'authenticated' not in session:
        return redirect(url_for('login'))

    entry = PasswordEntry.query.get_or_404(id)
    db.session.delete(entry)
    db.session.commit()
    flash('Entry deleted', 'success')
    return redirect(url_for('index'))


@app.route('/generator')
def generator():
    if 'authenticated' not in session:
        return redirect(url_for('login'))

    import secrets
    import string

    length = int(request.args.get('length', 16))
    use_uppercase = request.args.get('uppercase', 'on')
    use_digits = request.args.get('digits', 'on')
    use_special = request.args.get('special', 'on')

    chars = ''
    if use_uppercase:
        chars += string.ascii_uppercase
    if use_digits:
        chars += string.digits
    if use_special:
        chars += string.punctuation
    chars += string.ascii_lowercase

    password = ''.join(secrets.choice(chars) for _ in range(length))

    return {'password': password}


def init_db():
    with app.app_context():
        db.create_all()


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
