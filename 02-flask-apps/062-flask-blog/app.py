from flask import Flask, render_template, request, redirect, url_for, escape
import sqlite3
import re
import markdown

app = Flask(__name__)
DATABASE = "blog.db"


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            slug TEXT UNIQUE NOT NULL,
            content TEXT NOT NULL,
            author TEXT DEFAULT 'Admin',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            post_id INTEGER NOT NULL,
            author TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE
        )
    """)
    conn.commit()
    conn.close()


def generate_slug(title):
    slug = re.sub(r'[^\w\s-]', '', title.lower())
    slug = re.sub(r'[\s_-]+', '-', slug)
    slug = slug.strip('-')
    return slug


def markdown_to_html(content):
    return markdown.markdown(content, extensions=['fenced_code', 'tables', 'nl2br'])


@app.route("/")
def index():
    conn = get_db()
    cursor = conn.execute("SELECT * FROM posts ORDER BY created_at DESC")
    posts = cursor.fetchall()
    conn.close()
    return render_template("index.html", posts=posts)


@app.route("/post/<slug>")
def view_post(slug):
    conn = get_db()
    post = conn.execute("SELECT * FROM posts WHERE slug = ?", (slug,)).fetchone()

    if not post:
        conn.close()
        return redirect(url_for("index"))

    comments = conn.execute(
        "SELECT * FROM comments WHERE post_id = ? ORDER BY created_at DESC",
        (post["id"],)
    ).fetchall()
    conn.close()

    post_html = markdown_to_html(post["content"])
    return render_template("post.html", post=post, comments=comments, content_html=post_html)


@app.route("/create", methods=["GET", "POST"])
def create_post():
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        author = request.form.get("author") or "Admin"

        if title and content:
            slug = generate_slug(title)
            conn = get_db()

            counter = 1
            original_slug = slug
            while conn.execute("SELECT id FROM posts WHERE slug = ?", (slug,)).fetchone():
                slug = f"{original_slug}-{counter}"
                counter += 1

            conn.execute(
                "INSERT INTO posts (title, slug, content, author) VALUES (?, ?, ?, ?)",
                (title, slug, content, author)
            )
            conn.commit()
            conn.close()
            return redirect(url_for("view_post", slug=slug))

    return render_template("create_post.html")


@app.route("/edit/<int:post_id>", methods=["GET", "POST"])
def edit_post(post_id):
    conn = get_db()
    post = conn.execute("SELECT * FROM posts WHERE id = ?", (post_id,)).fetchone()
    conn.close()

    if not post:
        return redirect(url_for("index"))

    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        author = request.form.get("author") or "Admin"

        if title and content:
            conn = get_db()
            conn.execute(
                "UPDATE posts SET title = ?, content = ?, author = ? WHERE id = ?",
                (title, content, author, post_id)
            )
            conn.commit()
            conn.close()
            return redirect(url_for("view_post", slug=post["slug"]))

    return render_template("edit_post.html", post=post)


@app.route("/delete/<int:post_id>")
def delete_post(post_id):
    conn = get_db()
    conn.execute("DELETE FROM comments WHERE post_id = ?", (post_id,))
    conn.execute("DELETE FROM posts WHERE id = ?", (post_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))


@app.route("/post/<slug>/comment", methods=["POST"])
def add_comment(slug):
    author = request.form.get("author")
    content = request.form.get("content")

    if author and content:
        conn = get_db()
        post = conn.execute("SELECT id FROM posts WHERE slug = ?", (slug,)).fetchone()
        if post:
            conn.execute(
                "INSERT INTO comments (post_id, author, content) VALUES (?, ?, ?)",
                (post["id"], author, content)
            )
            conn.commit()
        conn.close()

    return redirect(url_for("view_post", slug=slug))


@app.route("/post/<slug>/comment/<int:comment_id>/delete")
def delete_comment(slug, comment_id):
    conn = get_db()
    conn.execute("DELETE FROM comments WHERE id = ?", (comment_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("view_post", slug=slug))


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
