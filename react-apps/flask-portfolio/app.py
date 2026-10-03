from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

projects = [
    {"title": "E-Commerce Platform", "description": "Full-stack shopping cart with payment integration", "tech": ["Python", "Flask", "PostgreSQL"]},
    {"title": "Task Manager API", "description": "RESTful API for task management", "tech": ["FastAPI", "Redis", "Docker"]},
    {"title": "Portfolio Website", "description": "Personal portfolio with blog functionality", "tech": ["Flask", "SQLAlchemy", "Bootstrap"]},
    {"title": "Data Dashboard", "description": "Real-time analytics dashboard", "tech": ["Python", "Plotly", "SQLite"]},
]

skills = [
    {"category": "Backend", "items": ["Python", "Flask", "FastAPI", "SQLAlchemy"]},
    {"category": "Frontend", "items": ["HTML/CSS", "JavaScript", "React", "Bootstrap"]},
    {"category": "Database", "items": ["PostgreSQL", "SQLite", "MongoDB", "Redis"]},
    {"category": "DevOps", "items": ["Docker", "Git", "CI/CD", "Linux"]},
]

contacts = []


@app.route("/")
def index():
    return render_template("index.html", projects=projects, skills=skills)


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")
        contacts.append({"name": name, "email": email, "message": message})
        return redirect(url_for("index"))
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True)
