"""
Simple Proxy API
Flask API that proxies requests to external APIs to avoid CORS issues
"""

import os
from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

# Configuration
GITHUB_API_URL = "https://api.github.com"
WEATHER_API_BASE = "https://api.open-meteo.com/v1"
UNSPLASH_API_BASE = "https://api.unsplash.com"
JSONPLACEHOLDER_BASE = "https://jsonplaceholder.typicode.com"

# Optional: Set API keys via environment variables
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
UNSPLASH_ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY")


def proxy_request(url, headers=None, params=None):
    """Generic proxy function for GET requests"""
    try:
        response = requests.get(url, headers=headers, params=params, timeout=30)
        return {
            "success": True,
            "status_code": response.status_code,
            "data": response.json() if response.content else None,
            "headers": dict(response.headers),
        }
    except requests.exceptions.Timeout:
        return {"success": False, "error": "Request timed out"}, 504
    except requests.exceptions.RequestException as e:
        return {"success": False, "error": str(e)}, 500


# Health check
@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({
        "status": "healthy",
        "timestamp": request.headers.get("Date", "unknown")
    })


# GitHub proxy endpoints
@app.route("/proxy/github", methods=["GET"])
@app.route("/proxy/github/<path:endpoint>", methods=["GET", "POST"])
def proxy_github(endpoint=""):
    """Proxy requests to GitHub API"""
    # Build the target URL
    target_url = f"{GITHUB_API_URL}/{endpoint}" if endpoint else GITHUB_API_URL

    # Build headers
    headers = {"Accept": "application/json"}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"token {GITHUB_TOKEN}"

    # Forward query parameters
    params = dict(request.args) if request.args else None

    result = proxy_request(target_url, headers=headers, params=params)
    if not result.get("success"):
        return jsonify(result), result.get("status_code", 500)

    return jsonify({
        "proxied_from": "https://api.github.com",
        "endpoint": f"/{endpoint}" if endpoint else "/",
        **result
    })


# Weather proxy endpoint
@app.route("/proxy/weather", methods=["GET"])
def proxy_weather():
    """Proxy requests to Open-Meteo Weather API"""
    # Build the target URL
    latitude = request.args.get("latitude", "40.7128")  # Default: NYC
    longitude = request.args.get("longitude", "-74.0060")
    target_url = f"{WEATHER_API_BASE}/forecast?latitude={latitude}&longitude={longitude}&current_weather=true"

    # Forward all query parameters
    params = dict(request.args) if request.args else None

    result = proxy_request(target_url, params=params)
    if not result.get("success"):
        return jsonify(result), result.get("status_code", 500)

    return jsonify({
        "proxied_from": "https://api.open-meteo.com/v1",
        "endpoint": "/forecast",
        **result
    })


# JSONPlaceholder proxy (useful for testing)
@app.route("/proxy/jsonplaceholder", methods=["GET"])
@app.route("/proxy/jsonplaceholder/<resource>", methods=["GET"])
@app.route("/proxy/jsonplaceholder/<resource>/<int:resource_id>", methods=["GET"])
def proxy_jsonplaceholder(resource="posts", resource_id=None):
    """Proxy requests to JSONPlaceholder API for testing"""
    # Build the target URL
    if resource_id:
        target_url = f"{JSONPLACEHOLDER_BASE}/{resource}/{resource_id}"
    else:
        target_url = f"{JSONPLACEHOLDER_BASE}/{resource}"

    # Forward query parameters
    params = dict(request.args) if request.args else None

    result = proxy_request(target_url, params=params)
    if not result.get("success"):
        return jsonify(result), result.get("status_code", 500)

    return jsonify({
        "proxied_from": "https://jsonplaceholder.typicode.com",
        "endpoint": f"/{resource}" + (f"/{resource_id}" if resource_id else ""),
        **result
    })


# Generic proxy endpoint
@app.route("/proxy", methods=["GET", "POST"])
@app.route("/proxy/<path:url>", methods=["GET", "POST"])
def generic_proxy(url=None):
    """Generic proxy for any URL (use with caution)"""
    if not url:
        return jsonify({"error": "No URL specified"}), 400

    # Ensure URL has a scheme
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    try:
        headers = dict(request.headers)
        # Remove hop-by-hop headers
        for header in ["Host", "Connection", "Content-Length"]:
            headers.pop(header, None)

        params = dict(request.args) if request.args else None

        if request.method == "POST":
            response = requests.post(
                url,
                headers=headers,
                params=params,
                json=request.get_json(silent=True),
                timeout=30
            )
        else:
            response = requests.get(
                url,
                headers=headers,
                params=params,
                timeout=30
            )

        return jsonify({
            "success": True,
            "proxied_url": url,
            "status_code": response.status_code,
            "data": response.json() if response.content else None,
        })

    except requests.exceptions.Timeout:
        return jsonify({"success": False, "error": "Request timed out"}), 504
    except requests.exceptions.RequestException as e:
        return jsonify({"success": False, "error": str(e)}), 500


# Error handlers
@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Endpoint not found"}), 404


@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "Internal server error"}), 500


if __name__ == "__main__":
    print("Starting Simple Proxy API...")
    print("Available endpoints:")
    print("  /health                    - Health check")
    print("  /proxy/github              - GitHub API proxy")
    print("  /proxy/github/<endpoint>   - GitHub API with custom endpoint")
    print("  /proxy/weather            - Weather API proxy")
    print("  /proxy/jsonplaceholder     - JSONPlaceholder API proxy")
    print("  /proxy/<url>              - Generic URL proxy")
    print("")
    print("Set GITHUB_TOKEN environment variable for authenticated GitHub requests")
    app.run(debug=True, host="0.0.0.0", port=5000)
