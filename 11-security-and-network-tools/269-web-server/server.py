"""
Simple Python HTTP Web Server with Routing
Built-in http.server only - no external dependencies
"""

import json
import os
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from datetime import datetime


class Router(SimpleHTTPRequestHandler):
    """HTTP server with routing support for static files and API endpoints."""

    # In-memory data store for API demo
    users = [
        {"id": 1, "name": "Alice", "email": "alice@example.com"},
        {"id": 2, "name": "Bob", "email": "bob@example.com"},
        {"id": 3, "name": "Charlie", "email": "charlie@example.com"},
    ]

    posts = [
        {"id": 1, "title": "First Post", "author": "Alice", "content": "Hello World!"},
        {"id": 2, "title": "Second Post", "author": "Bob", "content": "Python is awesome."},
    ]

    def do_GET(self):
        """Route GET requests to appropriate handlers."""
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)

        # API Routes
        if path.startswith("/api/"):
            self.handle_api(path, query)
        # Serve static files
        elif path == "/" or path == "/index.html":
            self.serve_html("index.html")
        else:
            # Try to serve from static directory
            super().do_GET()

    def do_POST(self):
        """Handle POST requests for API endpoints."""
        parsed = urlparse(self.path)
        path = parsed.path
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode("utf-8")

        try:
            data = json.loads(body) if body else {}
        except json.JSONDecodeError:
            self.send_json_response({"error": "Invalid JSON"}, status=400)
            return

        if path == "/api/users":
            # Create new user
            new_id = max(u["id"] for u in self.users) + 1
            new_user = {"id": new_id, "name": data.get("name", ""), "email": data.get("email", "")}
            self.users.append(new_user)
            self.send_json_response({"message": "User created", "user": new_user}, status=201)
        elif path == "/api/posts":
            # Create new post
            new_id = max(p["id"] for p in self.posts) + 1
            new_post = {
                "id": new_id,
                "title": data.get("title", ""),
                "author": data.get("author", "Anonymous"),
                "content": data.get("content", ""),
            }
            self.posts.append(new_post)
            self.send_json_response({"message": "Post created", "post": new_post}, status=201)
        else:
            self.send_json_response({"error": "Endpoint not found"}, status=404)

    def handle_api(self, path, query):
        """Handle API routes."""
        # Health check
        if path == "/api/health":
            self.send_json_response({
                "status": "healthy",
                "timestamp": datetime.now().isoformat(),
                "server": "Python HTTP Server"
            })

        # List all users
        elif path == "/api/users":
            self.send_json_response({"users": self.users})

        # Get single user
        elif path.startswith("/api/users/") and path.count("/") == 2:
            user_id = int(path.split("/")[-1])
            user = next((u for u in self.users if u["id"] == user_id), None)
            if user:
                self.send_json_response({"user": user})
            else:
                self.send_json_response({"error": "User not found"}, status=404)

        # List all posts
        elif path == "/api/posts":
            self.send_json_response({"posts": self.posts})

        # Get single post
        elif path.startswith("/api/posts/") and path.count("/") == 2:
            post_id = int(path.split("/")[-1])
            post = next((p for p in self.posts if p["id"] == post_id), None)
            if post:
                self.send_json_response({"post": post})
            else:
                self.send_json_response({"error": "Post not found"}, status=404)

        # Server info
        elif path == "/api/info":
            self.send_json_response({
                "version": "1.0.0",
                "endpoints": [
                    "GET /api/health - Health check",
                    "GET /api/users - List all users",
                    "GET /api/users/{id} - Get user by ID",
                    "POST /api/users - Create user",
                    "GET /api/posts - List all posts",
                    "GET /api/posts/{id} - Get post by ID",
                    "POST /api/posts - Create post",
                    "GET /api/info - Server info",
                ],
                "static_files": ["/", "/index.html", "/static/*"]
            })

        else:
            self.send_json_response({"error": "API endpoint not found"}, status=404)

    def serve_html(self, filename):
        """Serve HTML file from static directory."""
        static_dir = os.path.join(os.path.dirname(__file__), "static")
        filepath = os.path.join(static_dir, filename)

        if os.path.exists(filepath):
            self.path = f"/static/{filename}"
            super().do_GET()
        else:
            self.send_json_response({"error": "File not found"}, status=404)

    def send_json_response(self, data, status=200):
        """Send JSON response."""
        response = json.dumps(data, indent=2)
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", len(response))
        self.end_headers()
        self.wfile.write(response.encode("utf-8"))


def run_server(port=8000):
    """Start the HTTP server."""
    server_address = ("", port)
    httpd = HTTPServer(server_address, Router)

    print(f"=" * 50)
    print(f"  Python HTTP Web Server")
    print(f"=" * 50)
    print(f"  Server running at: http://localhost:{port}")
    print(f"  API endpoints at: http://localhost:{port}/api/")
    print(f"  Press Ctrl+C to stop")
    print(f"=" * 50)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
        httpd.shutdown()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Simple Python HTTP Server")
    parser.add_argument("-p", "--port", type=int, default=8000, help="Port to run server on")
    args = parser.parse_args()

    run_server(args.port)
