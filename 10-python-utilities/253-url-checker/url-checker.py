#!/usr/bin/env python3
"""
URL Checker - Check if URLs are alive and measure response time.

Usage:
    Single URL:  python url-checker.py https://example.com
    Batch mode:  python url-checker.py urls.txt
    JSON output: python url-checker.py urls.txt --json
"""

import argparse
import csv
import json
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import requests
from requests.exceptions import RequestException


@dataclass
class URLResult:
    """Stores the result of checking a single URL."""
    url: str
    status_code: Optional[int]
    response_time_ms: Optional[float]
    is_alive: bool
    error: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "url": self.url,
            "status_code": self.status_code,
            "response_time_ms": round(self.response_time_ms, 2) if self.response_time_ms else None,
            "is_alive": self.is_alive,
            "error": self.error,
        }


def check_url(url: str, timeout: int = 10) -> URLResult:
    """
    Check if a URL is reachable and measure response time.

    Args:
        url: The URL to check
        timeout: Request timeout in seconds

    Returns:
        URLResult with status, response time, and any error message
    """
    # Ensure URL has a scheme
    if not url.startswith(("http://", "https://")):
        url = f"https://{url}"

    try:
        start_time = time.perf_counter()
        response = requests.head(url, timeout=timeout, allow_redirects=True)
        end_time = time.perf_counter()

        response_time_ms = (end_time - start_time) * 1000
        is_alive = 200 <= response.status_code < 400

        return URLResult(
            url=url,
            status_code=response.status_code,
            response_time_ms=response_time_ms,
            is_alive=is_alive,
        )
    except RequestException as e:
        return URLResult(
            url=url,
            status_code=None,
            response_time_ms=None,
            is_alive=False,
            error=str(e),
        )


def load_urls_from_file(filepath: str) -> list[str]:
    """Load URLs from a text file (one URL per line)."""
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {filepath}")

    urls = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            url = line.strip()
            if url and not url.startswith("#"):
                urls.append(url)
    return urls


def print_result_table(results: list[URLResult]) -> None:
    """Print results in a formatted table."""
    # Header
    print(f"\n{'URL':<50} {'Status':<8} {'Time (ms)':<12} {'Result'}")
    print("-" * 90)

    for result in results:
        status = str(result.status_code) if result.status_code else "ERROR"
        response_time = f"{result.response_time_ms:.1f}" if result.response_time_ms else "-"
        result_text = "OK" if result.is_alive else "FAILED"

        # Truncate long URLs
        display_url = result.url[:47] + "..." if len(result.url) > 50 else result.url
        if result.error:
            result_text = f"ERROR: {result.error[:30]}"

        print(f"{display_url:<50} {status:<8} {response_time:<12} {result_text}")

    # Summary
    alive_count = sum(1 for r in results if r.is_alive)
    print("-" * 90)
    print(f"Summary: {alive_count}/{len(results)} URLs are alive")


def save_results_json(results: list[URLResult], output_path: str) -> None:
    """Save results to a JSON file."""
    output_data = {
        "summary": {
            "total": len(results),
            "alive": sum(1 for r in results if r.is_alive),
            "failed": sum(1 for r in results if not r.is_alive),
        },
        "results": [r.to_dict() for r in results],
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=2)

    print(f"Results saved to: {output_path}")


def save_results_csv(results: list[URLResult], output_path: str) -> None:
    """Save results to a CSV file."""
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["url", "status_code", "response_time_ms", "is_alive", "error"])
        writer.writeheader()
        for result in results:
            writer.writerow(result.to_dict())

    print(f"Results saved to: {output_path}")


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Check if URLs are alive and measure response time",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "source",
        help="URL to check or path to text file containing URLs (one per line)",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=10,
        help="Request timeout in seconds (default: 10)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON",
    )
    parser.add_argument(
        "--csv",
        action="store_true",
        help="Output results as CSV",
    )
    parser.add_argument(
        "--output",
        "-o",
        help="Output file path (requires --json or --csv)",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=0,
        help="Delay between requests in seconds (for rate limiting)",
    )

    args = parser.parse_args()

    # Determine if source is a file or single URL
    source_path = Path(args.source)
    if source_path.exists() and source_path.is_file():
        urls = load_urls_from_file(args.source)
        print(f"Checking {len(urls)} URLs from file: {args.source}")
    else:
        urls = [args.source]
        print(f"Checking URL: {args.source}")

    # Check all URLs
    results = []
    for i, url in enumerate(urls, 1):
        print(f"[{i}/{len(urls)}] Checking: {url}", end="\r")
        result = check_url(url, timeout=args.timeout)
        results.append(result)

        if args.delay > 0 and i < len(urls):
            time.sleep(args.delay)

    print(" " * 80)  # Clear the progress line

    # Output results
    if args.json or args.csv:
        output_path = args.output or "url-checker-results.json" if args.json else "url-checker-results.csv"
        if args.json:
            save_results_json(results, output_path)
        else:
            save_results_csv(results, output_path)
    else:
        print_result_table(results)

    # Return exit code based on results
    failed_count = sum(1 for r in results if not r.is_alive)
    return 1 if failed_count > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
