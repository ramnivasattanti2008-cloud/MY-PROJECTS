"""
Flask Notes REST API
Full CRUD operations with SQLite database
"""

import sqlite3
from datetime import datetime
from functools import wraps

from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

DATABASE = "notes.db"


# Database helpers
def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()


# Error handler decorator
def handle_errors(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    return wrapper


# Initialize database
with app.app_context():
    init_db()


@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    })


@app.route("/notes", methods=["GET"])
@handle_errors
def get_notes():
    """Get all notes with optional filtering"""
    search = request.args.get("search", "")

    with get_db() as conn:
        if search:
            cursor = conn.execute(
                """
                SELECT * FROM notes
                WHERE title LIKE ? OR content LIKE ?
                ORDER BY created_at DESC
                """,
                (f"%{search}%", f"%{search}%")
            )
        else:
            cursor = conn.execute(
                "SELECT * FROM notes ORDER BY created_at DESC"
            )

        notes = [dict(row) for row in cursor.fetchall()]

    return jsonify({
        "success": True,
        "count": len(notes),
        "data": notes
    })


@app.route("/notes/<int:note_id>", methods=["GET"])
@handle_errors
def get_note(note_id):
    """Get a single note by ID"""
    with get_db() as conn:
        cursor = conn.execute(
            "SELECT * FROM notes WHERE id = ?",
            (note_id,)
        )
        note = cursor.fetchone()

    if not note:
        return jsonify({"error": "Note not found"}), 404

    return jsonify({"success": True, "data": dict(note)})


@app.route("/notes", methods=["POST"])
@handle_errors
def create_note():
    """Create a new note"""
    data = request.get_json()

    if not data or not data.get("title"):
        return jsonify({"error": "Title is required"}), 400

    title = data["title"].strip()
    content = data.get("content", "").strip()

    with get_db() as conn:
        cursor = conn.execute(
            """
            INSERT INTO notes (title, content)
            VALUES (?, ?)
            """,
            (title, content)
        )
        conn.commit()
        note_id = cursor.lastrowid

        cursor = conn.execute(
            "SELECT * FROM notes WHERE id = ?",
            (note_id,)
        )
        note = cursor.fetchone()

    return jsonify({"success": True, "data": dict(note)}), 201


@app.route("/notes/<int:note_id>", methods=["PUT"])
@handle_errors
def update_note(note_id):
    """Update an existing note"""
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    with get_db() as conn:
        # Check if note exists
        cursor = conn.execute(
            "SELECT * FROM notes WHERE id = ?",
            (note_id,)
        )
        if not cursor.fetchone():
            return jsonify({"error": "Note not found"}), 404

        # Build update query dynamically
        updates = []
        params = []

        if "title" in data:
            updates.append("title = ?")
            params.append(data["title"].strip())
        if "content" in data:
            updates.append("content = ?")
            params.append(data["content"].strip())

        if updates:
            updates.append("updated_at = ?")
            params.append(datetime.now().isoformat())
            params.append(note_id)

            conn.execute(
                f"UPDATE notes SET {', '.join(updates)} WHERE id = ?",
                params
            )
            conn.commit()

        cursor = conn.execute(
            "SELECT * FROM notes WHERE id = ?",
            (note_id,)
        )
        note = cursor.fetchone()

    return jsonify({"success": True, "data": dict(note)})


@app.route("/notes/<int:note_id>", methods=["DELETE"])
@handle_errors
def delete_note(note_id):
    """Delete a note"""
    with get_db() as conn:
        cursor = conn.execute(
            "SELECT * FROM notes WHERE id = ?",
            (note_id,)
        )
        note = cursor.fetchone()

        if not note:
            return jsonify({"error": "Note not found"}), 404

        conn.execute("DELETE FROM notes WHERE id = ?", (note_id,))
        conn.commit()

    return jsonify({
        "success": True,
        "message": "Note deleted",
        "data": dict(note)
    })


@app.route("/notes/count", methods=["GET"])
@handle_errors
def count_notes():
    """Get total count of notes"""
    with get_db() as conn:
        cursor = conn.execute("SELECT COUNT(*) as count FROM notes")
        count = cursor.fetchone()["count"]

    return jsonify({
        "success": True,
        "count": count
    })


@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Resource not found"}), 404


@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "Internal server error"}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
