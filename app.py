import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash, g

app = Flask(__name__)
app.secret_key = "dev-secret-key"
DATABASE = "notes.db"


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db


def init_db():
    db = get_db()
    db.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL
        )
    """)
    db.commit()


@app.before_request
def before_request():
    init_db()


@app.teardown_appcontext
def close_db(error):
    db = g.pop("db", None)
    if db is not None:
        db.close()


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/notes", methods=["GET", "POST"])
def notes():
    db = get_db()

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        content = request.form.get("content", "").strip()

        if not title or not content:
            flash("Please provide both a title and content for the note.", "error")
            return redirect(url_for("notes"))

        db.execute(
            "INSERT INTO notes (title, content) VALUES (?, ?)",
            (title, content)
        )
        db.commit()
        flash("Note added successfully!", "success")
        return redirect(url_for("notes"))

    all_notes = db.execute("SELECT * FROM notes ORDER BY id DESC").fetchall()
    return render_template("notes.html", notes=all_notes)


@app.route("/notes/edit/<int:note_id>", methods=["GET", "POST"])
def edit_note(note_id):
    db = get_db()
    note = db.execute("SELECT * FROM notes WHERE id = ?", (note_id,)).fetchone()

    if note is None:
        flash("Note not found.", "error")
        return redirect(url_for("notes"))

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        content = request.form.get("content", "").strip()

        if not title or not content:
            flash("Both fields are required.", "error")
            return redirect(url_for("edit_note", note_id=note_id))

        db.execute(
            "UPDATE notes SET title = ?, content = ? WHERE id = ?",
            (title, content, note_id)
        )
        db.commit()
        flash("Note updated successfully.", "success")
        return redirect(url_for("notes"))

    return render_template("edit_note.html", note=note)


@app.route("/notes/delete/<int:note_id>", methods=["POST"])
def delete_note(note_id):
    db = get_db()
    db.execute("DELETE FROM notes WHERE id = ?", (note_id,))
    db.commit()
    flash("Note deleted.", "success")
    return redirect(url_for("notes"))


if __name__ == "__main__":
    with app.app_context():
        init_db()
    app.run(debug=True)