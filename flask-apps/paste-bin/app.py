import hashlib
import secrets
from datetime import datetime, timedelta
from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from flask_sqlAlchemy import SQLAlchemy
import markdown

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pastebin.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Paste(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    paste_id = db.Column(db.String(32), unique=True, nullable=False)
    title = db.Column(db.String(255), nullable=True)
    content = db.Column(db.Text, nullable=False)
    language = db.Column(db.String(50), default='plaintext')
    password_hash = db.Column(db.String(64), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=True)
    view_count = db.Column(db.Integer, default=0)

    def is_expired(self):
        if self.expires_at and datetime.utcnow() > self.expires_at:
            return True
        return False

    def to_dict(self):
        return {
            'paste_id': self.paste_id,
            'title': self.title,
            'language': self.language,
            'created_at': self.created_at.isoformat(),
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'view_count': self.view_count
        }


def generate_paste_id():
    return secrets.token_hex(16)


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/create', methods=['POST'])
def create_paste():
    data = request.get_json()
    content = data.get('content', '').strip()

    if not content:
        return jsonify({'error': 'Content is required'}), 400

    paste_id = generate_paste_id()
    title = data.get('title', '').strip() or 'Untitled'
    language = data.get('language', 'plaintext')
    password = data.get('password', '').strip()
    expiration = data.get('expiration', 'never')

    expires_at = None
    if expiration == '1h':
        expires_at = datetime.utcnow() + timedelta(hours=1)
    elif expiration == '24h':
        expires_at = datetime.utcnow() + timedelta(hours=24)
    elif expiration == '7d':
        expires_at = datetime.utcnow() + timedelta(days=7)
    elif expiration == '30d':
        expires_at = datetime.utcnow() + timedelta(days=30)

    password_hash = hash_password(password) if password else None

    paste = Paste(
        paste_id=paste_id,
        title=title,
        content=content,
        language=language,
        password_hash=password_hash,
        expires_at=expires_at
    )
    db.session.add(paste)
    db.session.commit()

    return jsonify({
        'paste_id': paste_id,
        'view_url': request.host_url + 'p/' + paste_id
    })


@app.route('/p/<paste_id>')
def view_paste(paste_id):
    paste = Paste.query.filter_by(paste_id=paste_id).first()
    if not paste:
        abort(404)
    if paste.is_expired():
        db.session.delete(paste)
        db.session.commit()
        abort(404)

    paste.view_count += 1
    db.session.commit()

    has_password = bool(paste.password_hash)
    return render_template('view.html', paste=paste, has_password=has_password)


@app.route('/p/<paste_id>/raw')
def raw_paste(paste_id):
    paste = Paste.query.filter_by(paste_id=paste_id).first()
    if not paste or paste.is_expired():
        abort(404)
    return paste.content, 200, {'Content-Type': 'text/plain; charset=utf-8'}


@app.route('/p/<paste_id>/verify', methods=['POST'])
def verify_password(paste_id):
    paste = Paste.query.filter_by(paste_id=paste_id).first()
    if not paste:
        abort(404)

    data = request.get_json()
    password = data.get('password', '')

    if not paste.password_hash:
        return jsonify({'success': True})

    if hash_password(password) == paste.password_hash:
        return jsonify({'success': True})
    return jsonify({'success': False, 'error': 'Invalid password'}), 401


@app.route('/api/pastes')
def list_pastes():
    pastes = Paste.query.filter(
        Paste.expires_at.is_(None) | Paste.expires_at > datetime.utcnow()
    ).order_by(Paste.created_at.desc()).limit(50).all()
    return jsonify([p.to_dict() for p in pastes])


@app.route('/api/pastes/<paste_id>', methods=['DELETE'])
def delete_paste(paste_id):
    paste = Paste.query.filter_by(paste_id=paste_id).first()
    if not paste:
        return jsonify({'error': 'Paste not found'}), 404
    db.session.delete(paste)
    db.session.commit()
    return jsonify({'message': 'Paste deleted successfully'})


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5002)
