"""
Simple Blog Flask Application
Create and view blog posts with markdown support and comments
"""
import os
import sqlite3
import re
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, abort
from markdown import markdown
import models

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')


def generate_slug(title):
    """Generate URL-friendly slug from title"""
    slug = title.lower()
    slug = re.sub(r'[^\w\s-]', '', slug)
    slug = re.sub(r'[-\s]+', '-', slug)
    return slug.strip('-')


def render_markdown(content):
    """Convert markdown to HTML with safe rendering"""
    return markdown(content, extensions=['fenced_code', 'tables', 'nl2br'])


@app.route('/')
def index():
    """Home page with all blog posts"""
    conn = models.get_db()
    cursor = conn.cursor()

    posts = cursor.execute('''
        SELECT p.*,
               (SELECT COUNT(*) FROM comments WHERE post_id = p.id) as comment_count
        FROM posts p
        ORDER BY created_at DESC
    ''').fetchall()

    conn.close()

    return render_template('index.html', posts=posts)


@app.route('/post/<slug>')
def view_post(slug):
    """View a single blog post with comments"""
    conn = models.get_db()
    cursor = conn.cursor()

    post = cursor.execute(
        'SELECT * FROM posts WHERE slug = ?',
        (slug,)
    ).fetchone()

    if not post:
        conn.close()
        abort(404)

    # Get comments
    comments = cursor.execute('''
        SELECT * FROM comments
        WHERE post_id = ?
        ORDER BY created_at ASC
    ''', (post['id'],)).fetchall()

    conn.close()

    # Render markdown content
    post_content = render_markdown(post['content'])

    return render_template('post.html',
                         post=post,
                         content=post_content,
                         comments=comments)


@app.route('/create', methods=['GET', 'POST'])
def create_post():
    """Create a new blog post"""
    if request.method == 'GET':
        return render_template('create.html')

    title = request.form.get('title', '').strip()
    content = request.form.get('content', '').strip()
    author = request.form.get('author', '').strip() or 'Anonymous'

    if not title or not content:
        flash('Title and content are required', 'error')
        return redirect(url_for('create_post'))

    # Generate unique slug
    slug = generate_slug(title)
    conn = models.get_db()
    cursor = conn.cursor()

    # Ensure slug is unique
    original_slug = slug
    counter = 1
    while cursor.execute('SELECT 1 FROM posts WHERE slug = ?', (slug,)).fetchone():
        slug = f'{original_slug}-{counter}'
        counter += 1

    try:
        cursor.execute('''
            INSERT INTO posts (title, slug, content, author)
            VALUES (?, ?, ?, ?)
        ''', (title, slug, content, author))
        conn.commit()
        conn.close()

        flash('Post created successfully!', 'success')
        return redirect(url_for('view_post', slug=slug))

    except Exception as e:
        conn.close()
        flash(f'Error creating post: {str(e)}', 'error')
        return redirect(url_for('create_post'))


@app.route('/post/<slug>/edit', methods=['GET', 'POST'])
def edit_post(slug):
    """Edit an existing blog post"""
    conn = models.get_db()
    cursor = conn.cursor()

    post = cursor.execute('SELECT * FROM posts WHERE slug = ?', (slug,)).fetchone()

    if not post:
        conn.close()
        abort(404)

    if request.method == 'GET':
        conn.close()
        return render_template('edit.html', post=post)

    title = request.form.get('title', '').strip()
    content = request.form.get('content', '').strip()
    author = request.form.get('author', '').strip() or 'Anonymous'

    if not title or not content:
        conn.close()
        flash('Title and content are required', 'error')
        return redirect(url_for('edit_post', slug=slug))

    try:
        cursor.execute('''
            UPDATE posts
            SET title = ?, content = ?, author = ?, updated_at = ?
            WHERE id = ?
        ''', (title, content, author, datetime.now().isoformat(), post['id']))
        conn.commit()
        conn.close()

        flash('Post updated successfully!', 'success')
        return redirect(url_for('view_post', slug=slug))

    except Exception as e:
        conn.close()
        flash(f'Error updating post: {str(e)}', 'error')
        return redirect(url_for('edit_post', slug=slug))


@app.route('/post/<slug>/delete', methods=['POST'])
def delete_post(slug):
    """Delete a blog post"""
    conn = models.get_db()
    cursor = conn.cursor()

    post = cursor.execute('SELECT * FROM posts WHERE slug = ?', (slug,)).fetchone()

    if not post:
        conn.close()
        abort(404)

    try:
        cursor.execute('DELETE FROM posts WHERE id = ?', (post['id'],))
        conn.commit()
        conn.close()

        flash('Post deleted successfully!', 'success')
        return redirect(url_for('index'))

    except Exception as e:
        conn.close()
        flash(f'Error deleting post: {str(e)}', 'error')
        return redirect(url_for('view_post', slug=slug))


@app.route('/post/<slug>/comment', methods=['POST'])
def add_comment(slug):
    """Add a comment to a post"""
    conn = models.get_db()
    cursor = conn.cursor()

    post = cursor.execute('SELECT * FROM posts WHERE slug = ?', (slug,)).fetchone()

    if not post:
        conn.close()
        abort(404)

    author = request.form.get('author', '').strip()
    content = request.form.get('content', '').strip()

    if not author or not content:
        flash('Name and comment are required', 'error')
        return redirect(url_for('view_post', slug=slug))

    try:
        cursor.execute('''
            INSERT INTO comments (post_id, author, content)
            VALUES (?, ?, ?)
        ''', (post['id'], author, content))
        conn.commit()
        conn.close()

        flash('Comment added!', 'success')
        return redirect(url_for('view_post', slug=slug))

    except Exception as e:
        conn.close()
        flash(f'Error adding comment: {str(e)}', 'error')
        return redirect(url_for('view_post', slug=slug))


@app.route('/post/<slug>/<int:comment_id>/delete', methods=['POST'])
def delete_comment(slug, comment_id):
    """Delete a comment"""
    conn = models.get_db()
    cursor = conn.cursor()

    comment = cursor.execute(
        'SELECT * FROM comments WHERE id = ? AND post_id = (SELECT id FROM posts WHERE slug = ?)',
        (comment_id, slug)
    ).fetchone()

    if not comment:
        conn.close()
        abort(404)

    try:
        cursor.execute('DELETE FROM comments WHERE id = ?', (comment_id,))
        conn.commit()
        conn.close()

        flash('Comment deleted', 'success')
        return redirect(url_for('view_post', slug=slug))

    except Exception as e:
        conn.close()
        flash(f'Error deleting comment: {str(e)}', 'error')
        return redirect(url_for('view_post', slug=slug))


@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    models.init_db()
    app.run(debug=True, host='0.0.0.0', port=5003)
