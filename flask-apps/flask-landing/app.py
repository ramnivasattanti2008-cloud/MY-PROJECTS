from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

features = [
    {"icon": "bi-lightning", "title": "Lightning Fast", "desc": "Optimized performance for seamless user experience"},
    {"icon": "bi-shield", "title": "Secure", "desc": "Enterprise-grade security for your data"},
    {"icon": "bi-cloud", "title": "Cloud Native", "desc": "Deploy anywhere with our cloud infrastructure"},
    {"icon": "bi-graph-up", "title": "Analytics", "desc": "Real-time insights and reporting dashboard"},
    {"icon": "bi-people", "title": "Team Collaboration", "desc": "Work together with your team effortlessly"},
    {"icon": "bi-headset", "title": "24/7 Support", "desc": "Round-the-clock customer support team"},
]

pricing = [
    {"name": "Starter", "price": "Free", "features": ["5 Projects", "1GB Storage", "Email Support"], "popular": False},
    {"name": "Pro", "price": "$29/mo", "features": ["Unlimited Projects", "100GB Storage", "Priority Support", "Analytics"], "popular": True},
    {"name": "Enterprise", "price": "$99/mo", "features": ["Everything in Pro", "Unlimited Storage", "Dedicated Support", "Custom Integrations"], "popular": False},
]

contacts = []


@app.route("/")
def index():
    return render_template("index.html", features=features, pricing=pricing)


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
