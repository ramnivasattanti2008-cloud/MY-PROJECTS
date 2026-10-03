"""
Blog Models - Database helper functions
"""

import sqlite3
from datetime import datetime

DB_PATH = 'blog.db'


def get_connection():
    """Get database connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def create_user(username, email, password_hash):
    """Create a new user."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            'INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)',
            (username, email, password_hash)
        )
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        return user_id
    except sqlite3.IntegrityError:
        conn.close()
        return None


def get_user_by_username(username):
    """Get user by username."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()
    return dict(user) if user else None


def get_all_posts(limit=50, offset=0):
    """Get all posts with author info."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT p.*, u.username as author_name,
               (SELECT COUNT(*) FROM comments WHERE post_id = p.id) as comment_count
        FROM posts p
        JOIN users u ON p.author_id = u.id
        ORDER BY p.created_at DESC
        LIMIT ? OFFSET ?
    ''', (limit, offset))
    posts = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return posts


def get_post_by_slug(slug):
    """Get single post by slug."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT p.*, u.username as author_name
        FROM posts p
        JOIN users u ON p.author_id = u.id
        WHERE p.slug = ?
    ''', (slug,))
    post = cursor.fetchone()
    conn.close()
    return dict(post) if post else None


def get_post_comments(post_id):
    """Get comments for a post."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        'SELECT * FROM comments WHERE post_id = ? ORDER BY created_at DESC',
        (post_id,)
    )
    comments = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return comments


def create_comment(post_id, author_name, content):
    """Create a new comment."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO comments (post_id, author_name, content) VALUES (?, ?, ?)',
        (post_id, author_name, content)
    )
    conn.commit()
    comment_id = cursor.lastrowid
    conn.close()
    return comment_id


def get_posts_by_tag(tag_slug):
    """Get posts filtered by tag."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT p.*, u.username as author_name
        FROM posts p
        JOIN users u ON p.author_id = u.id
        JOIN post_tags pt ON p.id = pt.post_id
        JOIN tags t ON t.id = pt.tag_id
        WHERE t.slug = ?
        ORDER BY p.created_at DESC
    ''', (tag_slug,))
    posts = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return posts


def get_all_tags():
    """Get all tags with post counts."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT t.*, COUNT(pt.post_id) as post_count
        FROM tags t
        LEFT JOIN post_tags pt ON t.id = pt.tag_id
        GROUP BY t.id
        ORDER BY post_count DESC
    ''')
    tags = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return tags


def get_user_posts(user_id):
    """Get all posts by a specific user."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT p.*,
               (SELECT COUNT(*) FROM comments WHERE post_id = p.id) as comment_count
        FROM posts p
        WHERE p.author_id = ?
        ORDER BY p.created_at DESC
    ''', (user_id,))
    posts = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return posts


def search_posts(query):
    """Search posts by title or content."""
    conn = get_connection()
    cursor = conn.cursor()
    search_term = f'%{query}%'
    cursor.execute('''
        SELECT p.*, u.username as author_name
        FROM posts p
        JOIN users u ON p.author_id = u.id
        WHERE p.title LIKE ? OR p.content LIKE ?
        ORDER BY p.created_at DESC
    ''', (search_term, search_term))
    posts = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return posts
