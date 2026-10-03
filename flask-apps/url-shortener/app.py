import string
import random
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urlshortener.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(2048), nullable=False)
    short_code = db.Column(db.String(10), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    click_count = db.Column(db.Integer, default=0)
    last_accessed = db.Column(db.DateTime, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'original_url': self.original_url,
            'short_code': self.short_code,
            'created_at': self.created_at.isoformat(),
            'click_count': self.click_count,
            'last_accessed': self.last_accessed.isoformat() if self.last_accessed else None
        }


def generate_short_code(length=6):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/shorten', methods=['POST'])
def shorten_url():
    data = request.get_json()
    original_url = data.get('url', '').strip()

    if not original_url:
        return jsonify({'error': 'URL is required'}), 400

    if not original_url.startswith(('http://', 'https://')):
        original_url = 'https://' + original_url

    custom_code = data.get('custom_code', '').strip()
    if custom_code:
        if URL.query.filter_by(short_code=custom_code).first():
            return jsonify({'error': 'Custom code already in use'}), 409
        short_code = custom_code
    else:
        short_code = generate_short_code()
        while URL.query.filter_by(short_code=short_code).first():
            short_code = generate_short_code()

    url_entry = URL(original_url=original_url, short_code=short_code)
    db.session.add(url_entry)
    db.session.commit()

    return jsonify({
        'short_url': request.host_url + short_code,
        'short_code': short_code,
        'original_url': original_url
    })


@app.route('/<short_code>')
def redirect_to_url(short_code):
    url_entry = URL.query.filter_by(short_code=short_code).first()
    if not url_entry:
        abort(404)
    url_entry.click_count += 1
    url_entry.last_accessed = datetime.utcnow()
    db.session.commit()
    return redirect(url_entry.original_url)


@app.route('/api/urls')
def get_all_urls():
    urls = URL.query.order_by(URL.created_at.desc()).all()
    return jsonify([url.to_dict() for url in urls])


@app.route('/api/urls/<short_code>')
def get_url(short_code):
    url_entry = URL.query.filter_by(short_code=short_code).first()
    if not url_entry:
        return jsonify({'error': 'URL not found'}), 404
    return jsonify(url_entry.to_dict())


@app.route('/api/urls/<short_code>', methods=['DELETE'])
def delete_url(short_code):
    url_entry = URL.query.filter_by(short_code=short_code).first()
    if not url_entry:
        return jsonify({'error': 'URL not found'}), 404
    db.session.delete(url_entry)
    db.session.commit()
    return jsonify({'message': 'URL deleted successfully'})


@app.route('/analytics')
def analytics():
    urls = URL.query.order_by(URL.click_count.desc()).limit(20).all()
    total_clicks = sum(url.click_count for url in URL.query.all())
    return render_template('analytics.html', urls=urls, total_clicks=total_clicks)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5001)
