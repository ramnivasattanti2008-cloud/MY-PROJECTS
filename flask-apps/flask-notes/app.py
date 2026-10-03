from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
DATABASE = "notes.db"


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tags (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS note_tags (
            note_id INTEGER,
            tag_id INTEGER,
            PRIMARY KEY (note_id, tag_id),
            FOREIGN KEY (note_id) REFERENCES notes(id) ON DELETE CASCADE,
            FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE
        )
    """)
    conn.commit()
    conn.close()


def get_all_tags():
    conn = get_db()
    cursor = conn.execute("SELECT * FROM tags ORDER BY name")
    tags = cursor.fetchall()
    conn.close()
    return tags


def get_notes_with_tags():
    conn = get_db()
    cursor = conn.execute("""
        SELECT n.*, GROUP_CONCAT(t.name) as tags, GROUP_CONCAT(t.id) as tag_ids
        FROM notes n
        LEFT JOIN note_tags nt ON n.id = nt.note_id
        LEFT JOIN tags t ON nt.tag_id = t.id
        GROUP BY n.id
        ORDER BY n.updated_at DESC
    """)
    notes = cursor.fetchall()
    conn.close()
    return notes


def get_note_with_tags(note_id):
    conn = get_db()
    note = conn.execute("SELECT * FROM notes WHERE id = ?", (note_id,)).fetchone()
    if note:
        tags = conn.execute("""
            SELECT t.* FROM tags t
            JOIN note_tags nt ON t.id = nt.tag_id
            WHERE nt.note_id = ?
        """, (note_id,)).fetchall()
    else:
        tags = []
    conn.close()
    return note, tags


@app.route("/")
def index():
    filter_tag = request.args.get("tag")
    notes = get_notes_with_tags()

    if filter_tag:
        notes = [n for n in notes if n["tags"] and filter_tag in n["tags"].split(",")]

    tags = get_all_tags()
    return render_template("index.html", notes=notes, tags=tags, filter_tag=filter_tag)


@app.route("/note/<int:note_id>")
def view_note(note_id):
    note, tags = get_note_with_tags(note_id)
    if not note:
        return redirect(url_for("index"))
    return render_template("view_note.html", note=note, tags=tags)


@app.route("/create", methods=["GET", "POST"])
def create():
    tags = get_all_tags()

    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        tag_names = request.form.getlist("tags")

        conn = get_db()
        cursor = conn.execute("INSERT INTO notes (title, content) VALUES (?, ?)", (title, content))
        note_id = cursor.lastrowid

        for tag_name in tag_names:
            if tag_name.strip():
                existing = conn.execute("SELECT id FROM tags WHERE name = ?", (tag_name.strip(),)).fetchone()
                if existing:
                    tag_id = existing["id"]
                else:
                    cursor = conn.execute("INSERT INTO tags (name) VALUES (?)", (tag_name.strip(),))
                    tag_id = cursor.lastrowid
                conn.execute("INSERT OR IGNORE INTO note_tags (note_id, tag_id) VALUES (?, ?)", (note_id, tag_id))

        conn.commit()
        conn.close()
        return redirect(url_for("index"))

    return render_template("create_note.html", tags=tags)


@app.route("/edit/<int:note_id>", methods=["GET", "POST"])
def edit(note_id):
    note, note_tags = get_note_with_tags(note_id)
    all_tags = get_all_tags()
    note_tag_ids = [t["id"] for t in note_tags]

    if not note:
        return redirect(url_for("index"))

    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        tag_names = request.form.getlist("tags")

        conn = get_db()
        conn.execute("UPDATE notes SET title = ?, content = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                     (title, content, note_id))
        conn.execute("DELETE FROM note_tags WHERE note_id = ?", (note_id,))

        for tag_name in tag_names:
            if tag_name.strip():
                existing = conn.execute("SELECT id FROM tags WHERE name = ?", (tag_name.strip(),)).fetchone()
                if existing:
                    tag_id = existing["id"]
                else:
                    cursor = conn.execute("INSERT INTO tags (name) VALUES (?)", (tag_name.strip(),))
                    tag_id = cursor.lastrowid
                conn.execute("INSERT OR IGNORE INTO note_tags (note_id, tag_id) VALUES (?, ?)", (note_id, tag_id))

        conn.commit()
        conn.close()
        return redirect(url_for("view_note", note_id=note_id))

    return render_template("edit_note.html", note=note, tags=all_tags, note_tag_ids=note_tag_ids)


@app.route("/delete/<int:note_id>")
def delete(note_id):
    conn = get_db()
    conn.execute("DELETE FROM note_tags WHERE note_id = ?", (note_id,))
    conn.execute("DELETE FROM notes WHERE id = ?", (note_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
