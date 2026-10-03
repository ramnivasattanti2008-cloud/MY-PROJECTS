#!/usr/bin/env python3
"""
REST Client CLI - A command-line HTTP client for making API requests.
Supports GET, POST, PUT, DELETE with custom headers and formatted JSON output.
"""

import argparse
import json
import sys
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from datetime import datetime


def format_json(data: dict | list, indent: int = 2) -> str:
    """Format JSON data with proper indentation and sorting."""
    return json.dumps(data, indent=indent, sort_keys=True, ensure_ascii=False)


def parse_headers(headers_list: list[str]) -> dict:
    """Parse header strings into a dictionary."""
    headers = {}
    for header in headers_list:
        if ':' in header:
            key, value = header.split(':', 1)
            headers[key.strip()] = value.strip()
    return headers


def make_request(
    method: str,
    url: str,
    headers: dict,
    data: str | None,
    verbose: bool
) -> dict:
    """Execute HTTP request and return formatted response."""
    start_time = datetime.now()

    try:
        # Prepare request
        request = Request(url, method=method)

        # Add headers
        for key, value in headers.items():
            request.add_header(key, value)

        # Add body for POST/PUT
        if data and method in ('POST', 'PUT', 'PATCH'):
            if isinstance(data, str):
                request.data = data.encode('utf-8')
            else:
                request.data = json.dumps(data).encode('utf-8')
            if 'Content-Type' not in headers:
                request.add_header('Content-Type', 'application/json')

        # Make request
        with urlopen(request, timeout=30) as response:
            body = response.read()
            status_code = response.status
            response_headers = dict(response.headers)

            # Parse response body
            try:
                response_data = json.loads(body.decode('utf-8'))
                formatted_body = format_json(response_data)
            except (json.JSONDecodeError, UnicodeDecodeError):
                formatted_body = body.decode('utf-8', errors='replace')

            elapsed = (datetime.now() - start_time).total_seconds() * 1000

            return {
                'success': True,
                'status_code': status_code,
                'headers': response_headers,
                'body': formatted_body,
                'elapsed_ms': round(elapsed, 2),
                'method': method,
                'url': url
            }

    except HTTPError as e:
        elapsed = (datetime.now() - start_time).total_seconds() * 1000
        error_body = e.read().decode('utf-8', errors='replace')
        try:
            error_body = format_json(json.loads(error_body))
        except json.JSONDecodeError:
            pass

        return {
            'success': False,
            'status_code': e.code,
            'error': str(e),
            'body': error_body,
            'elapsed_ms': round(elapsed, 2),
            'method': method,
            'url': url
        }

    except URLError as e:
        return {
            'success': False,
            'status_code': None,
            'error': f"Connection error: {e.reason}",
            'elapsed_ms': 0,
            'method': method,
            'url': url
        }

    except Exception as e:
        return {
            'success': False,
            'status_code': None,
            'error': str(e),
            'elapsed_ms': 0,
            'method': method,
            'url': url
        }


def print_response(result: dict, verbose: bool = False):
    """Print formatted response to console."""
    # Status line
    status_symbol = '✓' if result['success'] else '✗'
    status_text = f"{status_symbol} {result['method']} {result['url']}"

    if result.get('status_code'):
        status_text += f" → {result['status_code']}"

    print(f"\n{'=' * 60}")
    print(status_text)
    print(f"Time: {result['elapsed_ms']}ms")
    print('=' * 60)

    # Error message
    if not result['success'] and result.get('error'):
        print(f"\nERROR: {result['error']}")
        if result.get('body'):
            print(f"\nResponse body:\n{result['body']}")
        return

    # Response headers (verbose)
    if verbose and result.get('headers'):
        print("\nResponse Headers:")
        for key, value in result['headers'].items():
            if key.lower() not in ('set-cookie', 'transfer-encoding'):
                print(f"  {key}: {value}")

    # Response body
    print("\nResponse Body:")
    print(result.get('body', '(empty)'))


def main():
    parser = argparse.ArgumentParser(
        description='REST Client CLI - Make HTTP requests from the command line',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s GET https://api.example.com/users
  %(prog)s POST https://api.example.com/users -d '{"name": "John"}'
  %(prog)s PUT https://api.example.com/users/1 -H "Authorization: Bearer token"
  %(prog)s DELETE https://api.example.com/users/1 -v
        """
    )

    parser.add_argument(
        'method',
        choices=['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'HEAD'],
        help='HTTP method'
    )

    parser.add_argument(
        'url',
        help='Request URL'
    )

    parser.add_argument(
        '-d', '--data',
        help='Request body (JSON string or @filename)'
    )

    parser.add_argument(
        '-H', '--header',
        action='append',
        dest='headers',
        metavar='HEADER',
        help='Custom header (format: "Key: Value"). Can be used multiple times.'
    )

    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Show response headers'
    )

    parser.add_argument(
        '-o', '--output',
        help='Save response body to file'
    )

    args = parser.parse_args()

    # Parse headers
    headers = parse_headers(args.headers or [])

    # Parse data
    data = args.data
    if data and data.startswith('@'):
        # Read from file
        filename = data[1:]
        try:
            with open(filename, 'r') as f:
                data = f.read()
        except FileNotFoundError:
            print(f"Error: File not found: {filename}", file=sys.stderr)
            sys.exit(1)
        except IOError as e:
            print(f"Error reading file: {e}", file=sys.stderr)
            sys.exit(1)

    # Make request
    result = make_request(args.method.upper(), args.url, headers, data, args.verbose)

    # Output handling
    if args.output:
        # Save to file
        try:
            with open(args.output, 'w') as f:
                f.write(result.get('body', ''))
            print(f"Response saved to: {args.output}")
        except IOError as e:
            print(f"Error saving file: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        # Print to console
        print_response(result, args.verbose)

    # Exit code based on status
    if result.get('status_code'):
        sys.exit(0 if result['status_code'] < 400 else 1)
    else:
        sys.exit(1)


if __name__ == '__main__':
    main()
