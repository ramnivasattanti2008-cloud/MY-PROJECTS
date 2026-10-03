#!/usr/bin/env python3
"""
Mock API Server - Define API endpoints in YAML and serve mock responses.
Useful for testing frontend applications without a real backend.
"""

import argparse
import json
import random
import re
import string
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

import yaml


@dataclass
class Endpoint:
    """Represents a mock API endpoint."""
    path: str
    method: str
    status_code: int = 200
    response: dict | list | str = field(default_factory=dict)
    delay_ms: int = 0
    headers: dict = field(default_factory=dict)
    description: str = ""
    dynamic: dict | None = None


@dataclass
class MockServer:
    """Mock API server configuration."""
    name: str = "Mock API Server"
    port: int = 8080
    host: str = "localhost"
    base_path: str = ""
    endpoints: list[Endpoint] = field(default_factory=list)
    variables: dict = field(default_factory=dict)


def load_yaml(path: Path) -> dict:
    """Load and parse YAML file."""
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def save_yaml(data: dict, path: Path):
    """Save data to YAML file."""
    with open(path, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False)


def generate_dynamic_value(dynamic_config: dict) -> Any:
    """Generate dynamic values based on configuration."""
    value_type = dynamic_config.get('type', 'static')

    if value_type == 'uuid':
        length = dynamic_config.get('length', 36)
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

    elif value_type == 'random':
        min_val = dynamic_config.get('min', 0)
        max_val = dynamic_config.get('max', 100)
        return random.randint(min_val, max_val)

    elif value_type == 'random_float':
        min_val = dynamic_config.get('min', 0.0)
        max_val = dynamic_config.get('max', 100.0)
        return round(random.uniform(min_val, max_val), 2)

    elif value_type == 'choice':
        return random.choice(dynamic_config.get('values', []))

    elif value_type == 'date':
        format_str = dynamic_config.get('format', '%Y-%m-%d')
        offset_days = dynamic_config.get('offset_days', 0)
        d = datetime.now() + timedelta(days=offset_days)
        return d.strftime(format_str)

    elif value_type == 'datetime':
        format_str = dynamic_config.get('format', '%Y-%m-%dT%H:%M:%SZ')
        offset_days = dynamic_config.get('offset_days', 0)
        offset_hours = dynamic_config.get('offset_hours', 0)
        d = datetime.now() + timedelta(days=offset_days, hours=offset_hours)
        return d.strftime(format_str)

    elif value_type == 'increment':
        # Note: In a real implementation, you'd use a counter
        return dynamic_config.get('start', 1)

    elif value_type == 'boolean':
        return random.choice([True, False])

    elif value_type == 'email':
        return dynamic_config.get('pattern', 'user{id}@example.com').replace('{id}', str(random.randint(1, 1000)))

    elif value_type == 'name':
        first_names = ['John', 'Jane', 'Bob', 'Alice', 'Charlie', 'Diana', 'Eve', 'Frank']
        last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis']
        return f"{random.choice(first_names)} {random.choice(last_names)}"

    elif value_type == 'lorem':
        word_count = dynamic_config.get('words', 10)
        lorem = "lorem ipsum dolor sit amet consectetur adipiscing elit sed do eiusmod tempor incididunt ut labore et dolore magna aliqua"
        words = lorem.split()
        return ' '.join(random.choices(words, k=word_count))

    elif value_type == 'url':
        domains = ['example.com', 'api.test.com', 'data.io', 'service.dev']
        return f"https://{random.choice(domains)}/{random.choice(['users', 'posts', 'comments', 'images'])}/{random.randint(1, 1000)}"

    elif value_type == 'image_url':
        width = dynamic_config.get('width', 640)
        height = dynamic_config.get('height', 480)
        return f"https://picsum.photos/{width}/{height}"

    return dynamic_config.get('value', None)


def process_template(template: Any, context: dict) -> Any:
    """Process template with dynamic values."""
    if isinstance(template, dict):
        result = {}
        for key, value in template.items():
            processed_key = process_template(key, context)
            result[processed_key] = process_template(value, context)
        return result
    elif isinstance(template, list):
        return [process_template(item, context) for item in template]
    elif isinstance(template, str):
        # Process dynamic values in strings
        if '{{' in template and '}}' in template:
            # Check for function calls
            if template.startswith('{{') and template.endswith('}}'):
                func_name = template[2:-2].strip()
                return generate_dynamic_value({'type': func_name})

            # Replace placeholders
            result = template
            for match in re.finditer(r'\{\{(.+?)\}\}', template):
                expr = match.group(1).strip()
                try:
                    value = generate_dynamic_value({'type': expr})
                    result = result.replace(match.group(0), str(value))
                except Exception:
                    pass
            return result
        return template
    elif isinstance(template, dict) and 'dynamic' in template:
        return generate_dynamic_value(template['dynamic'])
    return template


def parse_endpoints(config: dict) -> list[Endpoint]:
    """Parse endpoints from configuration."""
    endpoints = []
    routes = config.get('routes', [])

    for route in routes:
        path = route.get('path', '/')
        method = route.get('method', 'GET').upper()
        status_code = route.get('status', 200)
        response = route.get('response', {})
        delay_ms = route.get('delay', 0)
        headers = route.get('headers', {})
        description = route.get('description', '')

        endpoints.append(Endpoint(
            path=path,
            method=method,
            status_code=status_code,
            response=response,
            delay_ms=delay_ms,
            headers=headers,
            description=description
        ))

    return endpoints


def load_config(config_path: Path) -> MockServer:
    """Load server configuration from YAML."""
    config = load_yaml(config_path)

    server = MockServer(
        name=config.get('name', 'Mock API Server'),
        port=config.get('port', 8080),
        host=config.get('host', 'localhost'),
        base_path=config.get('base_path', ''),
        variables=config.get('variables', {})
    )

    server.endpoints = parse_endpoints(config)

    return server


def create_sample_config() -> dict:
    """Create a sample configuration."""
    return {
        'name': 'Sample Mock API',
        'port': 8080,
        'host': 'localhost',
        'base_path': '/api/v1',
        'variables': {
            'api_version': '1.0.0'
        },
        'routes': [
            {
                'path': '/users',
                'method': 'GET',
                'description': 'List all users',
                'response': {
                    'users': [
                        {
                            'id': 1,
                            'name': 'John Doe',
                            'email': 'john@example.com'
                        },
                        {
                            'id': 2,
                            'name': 'Jane Smith',
                            'email': 'jane@example.com'
                        }
                    ],
                    'total': 2
                }
            },
            {
                'path': '/users/{id}',
                'method': 'GET',
                'description': 'Get user by ID',
                'response': {
                    'id': '{{increment}}',
                    'name': '{{name}}',
                    'email': '{{email}}',
                    'created_at': '{{datetime}}'
                }
            },
            {
                'path': '/users',
                'method': 'POST',
                'description': 'Create new user',
                'status': 201,
                'response': {
                    'id': 3,
                    'name': 'Created User',
                    'email': 'new@example.com',
                    'created_at': '{{datetime}}'
                }
            },
            {
                'path': '/posts',
                'method': 'GET',
                'description': 'List posts with pagination',
                'response': {
                    'posts': [
                        {
                            'id': '{{increment}}',
                            'title': '{{lorem words=5}}',
                            'author': '{{name}}',
                            'published_at': '{{datetime offset_days=-1}}',
                            'image': '{{image_url}}'
                        }
                    ],
                    'page': 1,
                    'total_pages': 5
                }
            }
        ]
    }


def match_path(route_pattern: str, request_path: str) -> dict | None:
    """Match request path against route pattern."""
    # Convert route pattern to regex
    pattern = route_pattern.replace('{id}', r'(?P<id>\w+)')
    pattern = pattern.replace('{name}', r'(?P<name>\w+)')

    match = re.match(f'^{pattern}$', request_path)
    if match:
        return match.groupdict()
    return None


def handle_request(
    method: str,
    path: str,
    server: MockServer,
    request_body: bytes | None = None
) -> tuple[int, dict, Any]:
    """Handle incoming request and return response."""
    # Build full path
    full_path = f"{server.base_path}{path}" if server.base_path else path

    # Find matching endpoint
    for endpoint in server.endpoints:
        # Check method
        if endpoint.method != method and endpoint.method != '*':
            continue

        # Check path
        params = match_path(endpoint.path, full_path)
        if params:
            # Apply delay if configured
            if endpoint.delay_ms > 0:
                time.sleep(endpoint.delay_ms / 1000)

            # Build context
            context = {
                **server.variables,
                **params,
                'request_body': request_body
            }

            # Process response template
            response = process_template(endpoint.response, context)

            # Add default headers
            headers = {
                'Content-Type': 'application/json',
                'X-Powered-By': 'MockAPI',
                'Access-Control-Allow-Origin': '*',
                **endpoint.headers
            }

            return endpoint.status_code, headers, response

    # No match found
    return 404, {'Content-Type': 'application/json'}, {
        'error': 'Not Found',
        'message': f'No endpoint found for {method} {path}'
    }


def run_server(server: MockServer):
    """Run the mock server using built-in http module."""
    from http.server import HTTPServer, BaseHTTPRequestHandler
    import json

    class MockHandler(BaseHTTPRequestHandler):
        server_instance = server

        def do_GET(self):
            self._handle_request('GET')

        def do_POST(self):
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length) if content_length > 0 else None
            self._handle_request('POST', body)

        def do_PUT(self):
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length) if content_length > 0 else None
            self._handle_request('PUT', body)

        def do_PATCH(self):
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length) if content_length > 0 else None
            self._handle_request('PATCH', body)

        def do_DELETE(self):
            self._handle_request('DELETE')

        def do_OPTIONS(self):
            self.send_response(204)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, PATCH, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', '*')
            self.end_headers()

        def _handle_request(self, method: str, body: bytes | None = None):
            # Remove query string
            path = self.path.split('?')[0]

            status, headers, response = handle_request(
                method, path, self.server_instance, body
            )

            # Send response
            self.send_response(status)
            for key, value in headers.items():
                self.send_header(key, value)
            self.end_headers()

            # Write response body
            if isinstance(response, (dict, list)):
                self.wfile.write(json.dumps(response, indent=2).encode('utf-8'))
            else:
                self.wfile.write(str(response).encode('utf-8'))

            # Log request
            print(f"{method:7} {self.path} -> {status}")

        def log_message(self, format, *args):
            # Suppress default logging
            pass

    addr = (server.host, server.port)
    print(f"Starting {server.name} at http://{server.host}:{server.port}")
    print(f"Base path: {server.base_path or '(none)'}")
    print(f"Endpoints: {len(server.endpoints)}")
    print("-" * 50)

    try:
        httpd = HTTPServer(addr, MockHandler)
        print("Server running... (Ctrl+C to stop)")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
        sys.exit(0)


def main():
    parser = argparse.ArgumentParser(
        description="Mock API Server - Serve mock API responses from YAML config",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        '-c', '--config',
        type=Path,
        help='YAML configuration file'
    )

    parser.add_argument(
        '-p', '--port',
        type=int,
        help='Server port (overrides config)'
    )

    parser.add_argument(
        '--host',
        help='Server host (overrides config)'
    )

    parser.add_argument(
        '--init',
        action='store_true',
        help='Create sample config.yaml'
    )

    parser.add_argument(
        '-l', '--list',
        action='store_true',
        help='List available endpoints'
    )

    args = parser.parse_args()

    if args.init:
        config = create_sample_config()
        save_yaml(config, Path('mock-config.yaml'))
        print("Created: mock-config.yaml")
        return

    if args.config:
        server = load_config(args.config)

        # Override from args
        if args.port:
            server.port = args.port
        if args.host:
            server.host = args.host

        if args.list:
            print(f"\n{server.name}")
            print("=" * 60)
            for ep in server.endpoints:
                print(f"  {ep.method:7} {ep.path}")
                if ep.description:
                    print(f"           {ep.description}")
            print()
            return

        run_server(server)
    else:
        # Run with sample config
        server = MockServer()
        server.endpoints = parse_endpoints(create_sample_config()['routes'])

        if args.port:
            server.port = args.port
        if args.host:
            server.host = args.host

        if args.list:
            print(f"\n{server.name}")
            print("=" * 60)
            for ep in server.endpoints:
                print(f"  {ep.method:7} {ep.path}")
            print()
            return

        run_server(server)


if __name__ == '__main__':
    main()
