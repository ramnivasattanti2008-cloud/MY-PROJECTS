from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bookmarks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Bookmark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    url = db.Column(db.String(500), nullable=False)
    description = db.Column(db.Text, nullable=True)
    tags = db.Column(db.String(200), nullable=True)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    click_count = db.Column(db.Integer, default=0)


@app.route('/')
def index():
    tag_filter = request.args.get('tag')
    search = request.args.get('search')
    sort = request.args.get('sort', 'newest')

    query = Bookmark.query

    if tag_filter:
        query = query.filter(Bookmark.tags.ilike(f'%{tag_filter}%'))

    if search:
        query = query.filter(
            db.or_(
                Bookmark.title.ilike(f'%{search}%'),
                Bookmark.description.ilike(f'%{search}%'),
                Bookmark.notes.ilike(f'%{search}%')
            )
        )

    if sort == 'newest':
        query = query.order_by(Bookmark.created_at.desc())
    elif sort == 'oldest':
        query = query.order_by(Bookmark.created_at.asc())
    elif sort == 'title':
        query = query.order_by(Bookmark.title.asc())
    elif sort == 'popular':
        query = query.order_by(Bookmark.click_count.desc())

    bookmarks = query.all()

    all_tags = set()
    for bm in Bookmark.query.all():
        if bm.tags:
            for tag in bm.tags.split(','):
                all_tags.add(tag.strip())
    all_tags = sorted(all_tags)

    return render_template('index.html', bookmarks=bookmarks, all_tags=all_tags,
                           tag_filter=tag_filter, search_query=search, sort=sort)


@app.route('/add', methods=['GET', 'POST'])
def add_bookmark():
    if request.method == 'POST':
        bookmark = Bookmark(
            title=request.form['title'],
            url=request.form['url'],
            description=request.form.get('description', ''),
            tags=request.form.get('tags', ''),
            notes=request.form.get('notes', '')
        )
        db.session.add(bookmark)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('add_bookmark.html')


@app.route('/bookmark/<int:id>')
def bookmark_detail(id):
    bookmark = Bookmark.query.get_or_404(id)
    bookmark.click_count += 1
    db.session.commit()
    return redirect(bookmark.url)


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_bookmark(id):
    bookmark = Bookmark.query.get_or_404(id)

    if request.method == 'POST':
        bookmark.title = request.form['title']
        bookmark.url = request.form['url']
        bookmark.description = request.form.get('description', '')
        bookmark.tags = request.form.get('tags', '')
        bookmark.notes = request.form.get('notes', '')
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('edit_bookmark.html', bookmark=bookmark)


@app.route('/delete/<int:id>', methods=['POST'])
def delete_bookmark(id):
    bookmark = Bookmark.query.get_or_404(id)
    db.session.delete(bookmark)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/export')
def export_bookmarks():
    bookmarks = Bookmark.query.order_by(Bookmark.created_at.desc()).all()
    content = []
    for bm in bookmarks:
        content.append(f"- {bm.title} ({bm.url})")
        if bm.tags:
            content.append(f"  Tags: {bm.tags}")
        if bm.notes:
            content.append(f"  Notes: {bm.notes}")
        content.append("")

    return "\n".join(content), 200, {
        'Content-Type': 'text/plain',
        'Content-Disposition': 'attachment; filename=bookmarks.txt'
    }


def init_db():
    with app.app_context():
        db.create_all()
        if not Bookmark.query.first():
            sample_bookmarks = [
                Bookmark(
                    title='Google',
                    url='https://www.google.com',
                    description='Search engine',
                    tags='search, utility',
                    notes='Main search engine'
                ),
                Bookmark(
                    title='GitHub',
                    url='https://www.github.com',
                    description='Code hosting platform',
                    tags='development, code, git',
                    notes='My repositories'
                ),
                Bookmark(
                    title='Stack Overflow',
                    url='https://www.stackoverflow.com',
                    description='Programming Q&A',
                    tags='development, help, code',
                    notes='Great for debugging'
                )
            ]
            for bm in sample_bookmarks:
                db.session.add(bm)
            db.session.commit()


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
