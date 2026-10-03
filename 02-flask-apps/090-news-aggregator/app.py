from flask import Flask, render_template, jsonify, request
import requests
from datetime import datetime, timedelta
import os

app = Flask(__name__)

NEWS_API_KEY = os.environ.get("NEWS_API_KEY", "")
NEWS_API_BASE = "https://newsapi.org/v2"

CATEGORIES = ["general", "business", "technology", "science", "health", "sports", "entertainment"]

def get_top_headlines(category=None, country="us", page_size=20):
    """Fetch top headlines from NewsAPI."""
    if not NEWS_API_KEY:
        return None, "NewsAPI key not configured"

    try:
        url = f"{NEWS_API_BASE}/top-headlines"
        params = {
            "apiKey": NEWS_API_KEY,
            "country": country,
            "pageSize": page_size
        }
        if category:
            params["category"] = category

        response = requests.get(url, params=params, timeout=10)
        data = response.json()

        if data.get("status") == "ok":
            return data.get("articles", []), None
        else:
            return None, data.get("message", "API error")
    except requests.RequestException as e:
        return None, str(e)

def search_news(query, page_size=20):
    """Search news articles."""
    if not NEWS_API_KEY:
        return None, "NewsAPI key not configured"

    try:
        url = f"{NEWS_API_BASE}/everything"
        params = {
            "apiKey": NEWS_API_KEY,
            "q": query,
            "pageSize": page_size,
            "sortBy": "publishedAt",
            "language": "en"
        }
        response = requests.get(url, params=params, timeout=10)
        data = response.json()

        if data.get("status") == "ok":
            return data.get("articles", []), None
        else:
            return None, data.get("message", "API error")
    except requests.RequestException as e:
        return None, str(e)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/headlines")
def api_headlines():
    category = request.args.get("category")
    articles, error = get_top_headlines(category=category)
    if error:
        return jsonify({"error": error, "articles": []})
    return jsonify({"articles": articles, "error": None})

@app.route("/api/search")
def api_search():
    query = request.args.get("q", "")
    if not query:
        return jsonify({"error": "Query required", "articles": []})
    articles, error = search_news(query)
    if error:
        return jsonify({"error": error, "articles": []})
    return jsonify({"articles": articles, "error": None})

if __name__ == "__main__":
    print("NewsAggregator starting...")
    if not NEWS_API_KEY:
        print("WARNING: NEWS_API_KEY not set. Get a free key at https://newsapi.org/register")
    app.run(debug=True, port=5002)
