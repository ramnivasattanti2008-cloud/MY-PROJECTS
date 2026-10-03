"""
Webhook Tester
Flask app to receive and display webhook payloads
"""

import json
from datetime import datetime
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

# Store recent webhook payloads (in-memory, max 100)
webhook_store = []
MAX_PAYLOADS = 100


@app.route("/")
def index():
    """Render the webhook viewer page"""
    return render_template("index.html")


@app.route("/webhook", methods=["POST", "GET"])
@app.route("/webhook/<path:path>", methods=["POST", "GET"])
def receive_webhook(path=""):
    """Receive and store webhook payloads"""
    # Create payload record
    payload = {
        "id": len(webhook_store) + 1,
        "timestamp": datetime.now().isoformat(),
        "method": request.method,
        "path": f"/webhook/{path}" if path else "/webhook",
        "headers": dict(request.headers),
        "query_params": dict(request.args),
        "body": None,
        "body_raw": None,
    }

    # Parse body
    content_type = request.headers.get("Content-Type", "")

    if request.content_length and request.content_length > 0:
        if "application/json" in content_type:
            try:
                payload["body"] = request.get_json()
                payload["body_raw"] = request.get_data(as_text=True)
            except Exception:
                payload["body_raw"] = request.get_data(as_text=True)
        else:
            payload["body_raw"] = request.get_data(as_text=True)

    # Store the payload
    webhook_store.insert(0, payload)

    # Trim to max size
    if len(webhook_store) > MAX_PAYLOADS:
        webhook_store.pop()

    return jsonify({
        "success": True,
        "message": "Webhook received",
        "webhook_id": payload["id"]
    })


@app.route("/api/webhooks", methods=["GET"])
def get_webhooks():
    """Get all stored webhooks (summary)"""
    summaries = [
        {
            "id": p["id"],
            "timestamp": p["timestamp"],
            "method": p["method"],
            "path": p["path"],
            "content_type": p["headers"].get("Content-Type", "unknown"),
        }
        for p in webhook_store
    ]
    return jsonify({
        "success": True,
        "count": len(summaries),
        "webhooks": summaries
    })


@app.route("/api/webhooks/<int:webhook_id>", methods=["GET"])
def get_webhook(webhook_id):
    """Get a specific webhook payload"""
    for payload in webhook_store:
        if payload["id"] == webhook_id:
            return jsonify({
                "success": True,
                "webhook": payload
            })
    return jsonify({
        "success": False,
        "error": "Webhook not found"
    }), 404


@app.route("/api/webhooks/latest", methods=["GET"])
def get_latest_webhook():
    """Get the most recent webhook"""
    if webhook_store:
        return jsonify({
            "success": True,
            "webhook": webhook_store[0]
        })
    return jsonify({
        "success": False,
        "error": "No webhooks received yet"
    }), 404


@app.route("/api/webhooks/clear", methods=["POST", "DELETE"])
def clear_webhooks():
    """Clear all stored webhooks"""
    webhook_store.clear()
    return jsonify({
        "success": True,
        "message": "All webhooks cleared"
    })


@app.route("/api/webhooks/<int:webhook_id>", methods=["DELETE"])
def delete_webhook(webhook_id):
    """Delete a specific webhook"""
    for i, payload in enumerate(webhook_store):
        if payload["id"] == webhook_id:
            webhook_store.pop(i)
            return jsonify({
                "success": True,
                "message": "Webhook deleted"
            })
    return jsonify({
        "success": False,
        "error": "Webhook not found"
    }), 404


@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "stored_webhooks": len(webhook_store)
    })


if __name__ == "__main__":
    print("Starting Webhook Tester...")
    print("  Web UI:      http://localhost:5000/")
    print("  Webhook URL: http://localhost:5000/webhook")
    print("")
    print("Example webhook curl command:")
    print('  curl -X POST http://localhost:5000/webhook \\')
    print('    -H "Content-Type: application/json" \\')
    print('    -d \'{"event": "test", "data": {"message": "Hello"}}\'')
    app.run(debug=True, host="0.0.0.0", port=5000)
