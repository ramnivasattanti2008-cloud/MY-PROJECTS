from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-key-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///links.db'
db = SQLAlchemy(app)


class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(500), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500))
    tags = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


@app.route('/')
def index():
    tag_filter = request.args.get('tag')
    if tag_filter:
        links = Link.query.filter(Link.tags.contains(tag_filter)).order_by(Link.created_at.desc()).all()
    else:
        links = Link.query.order_by(Link.created_at.desc()).all()
    all_tags = set()
    for link in Link.query.all():
        if link.tags:
            for t in link.tags.split(','):
                all_tags.add(t.strip())
    return render_template('index.html', links=links, all_tags=sorted(all_tags), tag_filter=tag_filter)


@app.route('/add', methods=['GET', 'POST'])
def add_link():
    if request.method == 'POST':
        link = Link(
            url=request.form['url'],
            title=request.form['title'],
            description=request.form['description'],
            tags=request.form['tags']
        )
        db.session.add(link)
        db.session.commit()
        flash('Link added successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('add.html')


@app.route('/delete/<int:id>')
def delete_link(id):
    link = Link.query.get_or_404(id)
    db.session.delete(link)
    db.session.commit()
    flash('Link deleted.', 'info')
    return redirect(url_for('index'))


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_link(id):
    link = Link.query.get_or_404(id)
    if request.method == 'POST':
        link.url = request.form['url']
        link.title = request.form['title']
        link.description = request.form['description']
        link.tags = request.form['tags']
        db.session.commit()
        flash('Link updated!', 'success')
        return redirect(url_for('index'))
    return render_template('edit.html', link=link)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5001)
