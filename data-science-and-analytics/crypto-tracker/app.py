from flask import Flask, render_template, jsonify, request
import requests
from datetime import datetime

app = Flask(__name__)

COINGECKO_API = "https://api.coingecko.com/api/v3"

def get_top_cryptos(limit=10):
    """Fetch top cryptocurrencies by market cap."""
    try:
        url = f"{COINGECKO_API}/coins/markets"
        params = {
            "vs_currency": "usd",
            "order": "market_cap_desc",
            "per_page": limit,
            "page": 1,
            "sparkline": True,
            "price_change_percentage": "1h,24h,7d"
        }
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching cryptos: {e}")
        return []

def get_crypto_history(crypto_id, days=7):
    """Get price history for a specific crypto."""
    try:
        url = f"{COINGECKO_API}/coins/{crypto_id}/market_chart"
        params = {"vs_currency": "usd", "days": days}
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        return None

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/cryptos")
def api_cryptos():
    limit = request.args.get("limit", 10, type=int)
    cryptos = get_top_cryptos(limit)
    return jsonify(cryptos)

@app.route("/api/crypto/<crypto_id>")
def api_crypto(crypto_id):
    history = get_crypto_history(crypto_id)
    if history:
        return jsonify(history)
    return jsonify({"error": "Crypto not found"}), 404

if __name__ == "__main__":
    app.run(debug=True, port=5001)
