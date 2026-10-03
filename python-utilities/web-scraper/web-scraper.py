#!/usr/bin/env python3
"""
Web Scraper - Extract data from websites using requests and BeautifulSoup

Features:
- Scrape HTML content and extract structured data
- Support for CSS selectors and XPath
- Export to CSV and JSON formats
- Respectful scraping with rate limiting
- Custom extraction functions
- Proxy support
- Error handling

Usage:
    python web-scraper.py --url "https://example.com" --selector "h2"
    python web-scraper.py --url "https://example.com" --config scraper_config.json
"""

import argparse
import csv
import json
import os
import sys
import time
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Callable, Optional
from urllib.parse import urljoin, urlparse

try:
    import requests
    from bs4 import BeautifulSoup, Tag
except ImportError:
    print("Error: Required packages not installed.")
    print("Run: pip install requests beautifulsoup4")
    sys.exit(1)


@dataclass
class ScrapedItem:
    """Represents a single scraped data item."""
    url: str
    title: str = ""
    text: str = ""
    href: str = ""
    src: str = ""
    data: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        """Convert to dictionary, flattening for CSV export."""
        result = {
            'url': self.url,
            'title': self.title,
            'text': self.text,
            'href': self.href,
            'src': self.src,
        }
        result.update(self.data)
        return result


@dataclass
class ScrapeResult:
    """Results from a scraping operation."""
    url: str
    status_code: int
    items: list[ScrapedItem]
    errors: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON export."""
        return {
            'url': self.url,
            'status_code': self.status_code,
            'item_count': len(self.items),
            'items': [item.to_dict() for item in self.items],
            'errors': self.errors
        }


class WebScraper:
    """Web scraper with configurable extraction options."""

    def __init__(
        self,
        delay: float = 1.0,
        timeout: int = 30,
        user_agent: str = None,
        proxies: dict = None,
        headers: dict = None
    ):
        """
        Initialize the web scraper.

        Args:
            delay: Delay between requests in seconds (rate limiting)
            timeout: Request timeout in seconds
            user_agent: Custom User-Agent string
            proxies: Proxy configuration dict
            headers: Custom HTTP headers
        """
        self.delay = delay
        self.timeout = timeout
        self.proxies = proxies

        # Default headers
        self.default_headers = {
            'User-Agent': user_agent or 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                                    'AppleWebKit/537.36 (KHTML, like Gecko) '
                                    'Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }

        if headers:
            self.default_headers.update(headers)

        self.last_request_time = 0

    def _rate_limit(self):
        """Enforce rate limiting between requests."""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.delay:
            time.sleep(self.delay - elapsed)
        self.last_request_time = time.time()

    def fetch(self, url: str) -> requests.Response:
        """
        Fetch a URL with rate limiting and error handling.

        Args:
            url: URL to fetch

        Returns:
            Response object

        Raises:
            requests.RequestException: If request fails
        """
        self._rate_limit()

        try:
            response = requests.get(
                url,
                headers=self.default_headers,
                timeout=self.timeout,
                proxies=self.proxies,
                allow_redirects=True
            )
            response.raise_for_status()
            return response
        except requests.exceptions.Timeout:
            raise TimeoutError(f"Request timed out for: {url}")
        except requests.exceptions.HTTPError as e:
            raise RuntimeError(f"HTTP error {e.response.status_code} for: {url}")
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Request failed for {url}: {e}")

    def parse_html(self, html: str) -> BeautifulSoup:
        """
        Parse HTML content into BeautifulSoup object.

        Args:
            html: HTML string

        Returns:
            BeautifulSoup parser instance
        """
        return BeautifulSoup(html, 'html.parser')

    def scrape(
        self,
        url: str,
        selectors: dict[str, str] = None,
        custom_extractor: Callable[[BeautifulSoup, str], list[ScrapedItem]] = None,
        follow_links: bool = False,
        max_pages: int = 10
    ) -> ScrapeResult:
        """
        Scrape a URL and extract data.

        Args:
            url: URL to scrape
            selectors: Dict of selector names to CSS selectors
            custom_extractor: Custom extraction function
            follow_links: Whether to follow links on the page
            max_pages: Maximum pages to scrape when following links

        Returns:
            ScrapeResult with extracted items
        """
        errors = []
        all_items = []
        visited_urls = set()
        urls_to_scrape = [url]
        page_count = 0

        while urls_to_scrape and page_count < max_pages:
            current_url = urls_to_scrape.pop(0)

            if current_url in visited_urls:
                continue

            visited_urls.add(current_url)
            page_count += 1
            print(f"Scraping page {page_count}: {current_url}")

            try:
                response = self.fetch(current_url)
                soup = self.parse_html(response.text)

                if custom_extractor:
                    # Use custom extraction function
                    items = custom_extractor(soup, current_url)
                    all_items.extend(items)
                elif selectors:
                    # Use CSS selectors
                    items = self._extract_with_selectors(soup, current_url, selectors)
                    all_items.extend(items)

                    # Collect links for following
                    if follow_links:
                        for link in soup.find_all('a', href=True):
                            href = link['href']
                            full_url = urljoin(current_url, href)
                            # Only follow same-domain links
                            if urlparse(full_url).netloc == urlparse(url).netloc:
                                if full_url not in visited_urls:
                                    urls_to_scrape.append(full_url)

                print(f"  Found {len(items)} items")

            except (TimeoutError, RuntimeError) as e:
                error_msg = f"{current_url}: {str(e)}"
                print(f"  Error: {error_msg}")
                errors.append(error_msg)

        return ScrapeResult(
            url=url,
            status_code=200,
            items=all_items,
            errors=errors
        )

    def _extract_with_selectors(
        self,
        soup: BeautifulSoup,
        url: str,
        selectors: dict[str, str]
    ) -> list[ScrapedItem]:
        """
        Extract items using CSS selectors.

        Args:
            soup: BeautifulSoup object
            url: Source URL
            selectors: Dict mapping field names to CSS selectors

        Returns:
            List of ScrapedItems
        """
        items = []

        # Find all containers that match the main selector
        main_selector = selectors.get('_container', list(selectors.values())[0])
        containers = soup.select(main_selector)

        for container in containers:
            item = ScrapedItem(url=url)

            for field_name, selector in selectors.items():
                if field_name == '_container':
                    continue

                elements = container.select(selector) if container != soup else soup.select(selector)

                if not elements:
                    continue

                # Extract data based on field type
                if field_name == 'text' or field_name == 'title':
                    item.__dict__[field_name] = ' '.join(
                        el.get_text(strip=True) for el in elements
                    )
                elif field_name == 'href':
                    item.href = elements[0].get('href', '') if elements else ''
                elif field_name == 'src':
                    item.src = elements[0].get('src', '') if elements else ''
                elif field_name.startswith('data_'):
                    # Extract custom data attributes
                    attr_name = field_name[5:]  # Remove 'data_' prefix
                    item.data[field_name] = elements[0].get(attr_name, '') if elements else ''

            items.append(item)

        return items

    def extract_links(self, url: str, selector: str = 'a') -> list[dict]:
        """
        Extract all links from a page.

        Args:
            url: URL to scrape
            selector: CSS selector for links

        Returns:
            List of dicts with link text and href
        """
        response = self.fetch(url)
        soup = self.parse_html(response.text)

        links = []
        for link in soup.select(selector):
            links.append({
                'text': link.get_text(strip=True),
                'href': link.get('href', ''),
                'title': link.get('title', '')
            })

        return links

    def extract_tables(self, url: str, table_index: int = 0) -> list[dict]:
        """
        Extract data from HTML tables.

        Args:
            url: URL to scrape
            table_index: Index of table to extract (0-based)

        Returns:
            List of dicts representing table rows
        """
        response = self.fetch(url)
        soup = self.parse_html(response.text)

        tables = soup.find_all('table')
        if table_index >= len(tables):
            raise ValueError(f"Table index {table_index} not found. Page has {len(tables)} tables.")

        table = tables[table_index]
        rows = table.find_all('tr')

        if not rows:
            return []

        # Extract headers
        headers = []
        header_row = rows[0]
        for th in header_row.find_all(['th', 'td']):
            headers.append(th.get_text(strip=True) or f"col_{len(headers)}")

        # Extract data rows
        data = []
        for row in rows[1:]:
            cells = row.find_all(['td', 'th'])
            if cells:
                row_data = {}
                for i, cell in enumerate(cells):
                    header = headers[i] if i < len(headers) else f"col_{i}"
                    row_data[header] = cell.get_text(strip=True)
                data.append(row_data)

        return data


class ExportManager:
    """Handle exporting scraped data to various formats."""

    @staticmethod
    def to_csv(items: list[ScrapedItem], output_path: str):
        """
        Export items to CSV file.

        Args:
            items: List of ScrapedItems
            output_path: Output file path
        """
        if not items:
            print("No items to export")
            return

        # Get all possible fields
        all_fields = set(['url', 'title', 'text', 'href', 'src'])
        for item in items:
            all_fields.update(item.data.keys())

        fieldnames = sorted(all_fields)

        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

            for item in items:
                row = item.to_dict()
                # Ensure all fields are present
                for field in fieldnames:
                    if field not in row:
                        row[field] = ''
                writer.writerow(row)

        print(f"Exported {len(items)} items to {output_path}")

    @staticmethod
    def to_json(result: ScrapeResult, output_path: str, pretty: bool = True):
        """
        Export scrape result to JSON file.

        Args:
            result: ScrapeResult object
            output_path: Output file path
            pretty: Use pretty printing
        """
        with open(output_path, 'w', encoding='utf-8') as f:
            if pretty:
                json.dump(result.to_dict(), f, indent=2, ensure_ascii=False)
            else:
                json.dump(result.to_dict(), f, ensure_ascii=False)

        print(f"Exported {len(result.items)} items to {output_path}")


def load_config(config_path: str) -> dict:
    """
    Load scraper configuration from JSON file.

    Args:
        config_path: Path to config file

    Returns:
        Configuration dictionary
    """
    with open(config_path, 'r') as f:
        return json.load(f)


def main():
    """Main entry point with CLI argument parsing."""
    parser = argparse.ArgumentParser(
        description='Web Scraper - Extract data from websites',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    # URL options
    parser.add_argument('--url', '-u', required=True,
                       help='URL to scrape')
    parser.add_argument('--config', '-c',
                       help='Path to JSON configuration file')

    # Extraction options
    extraction_group = parser.add_argument_group('Extraction')
    extraction_group.add_argument('--selector', '-s',
                                  help='CSS selector for elements to extract')
    extraction_group.add_argument('--selectors',
                                  help='JSON string of selectors (e.g., \'{"title":"h1","text":"p"}\')')
    extraction_group.add_argument('--container',
                                  help='CSS selector for container elements')
    extraction_group.add_argument('--extract-links', action='store_true',
                                  help='Extract all links from page')
    extraction_group.add_argument('--extract-tables', action='store_true',
                                  help='Extract HTML tables')
    extraction_group.add_argument('--table-index', type=int, default=0,
                                  help='Table index to extract (default: 0)')

    # Follow options
    follow_group = parser.add_argument_group('Following Links')
    follow_group.add_argument('--follow', action='store_true',
                             help='Follow links on the page')
    follow_group.add_argument('--max-pages', type=int, default=10,
                             help='Maximum pages to scrape (default: 10)')

    # Output options
    output_group = parser.add_argument_group('Output')
    output_group.add_argument('--output', '-o',
                             help='Output file path (CSV or JSON based on extension)')
    output_group.add_argument('--format', '-f', choices=['csv', 'json'],
                             help='Output format (default: infer from extension)')
    output_group.add_argument('--pretty', action='store_true', default=True,
                             help='Pretty print JSON output')

    # Request options
    request_group = parser.add_argument_group('Request Settings')
    request_group.add_argument('--delay', type=float, default=1.0,
                              help='Delay between requests in seconds (default: 1.0)')
    request_group.add_argument('--timeout', type=int, default=30,
                              help='Request timeout in seconds (default: 30)')
    request_group.add_argument('--user-agent',
                              help='Custom User-Agent string')
    request_group.add_argument('--proxy',
                              help='HTTP proxy URL')

    args = parser.parse_args()

    # Load config if provided
    if args.config:
        config = load_config(args.config)
        scraper = WebScraper(
            delay=config.get('delay', args.delay),
            timeout=config.get('timeout', args.timeout),
            user_agent=config.get('user_agent', args.user_agent),
            proxies=config.get('proxies'),
            headers=config.get('headers')
        )
        selectors = config.get('selectors', {})
        follow = config.get('follow', args.follow)
        max_pages = config.get('max_pages', args.max_pages)
    else:
        scraper = WebScraper(
            delay=args.delay,
            timeout=args.timeout,
            user_agent=args.user_agent,
            proxies={'http': args.proxy} if args.proxy else None
        )
        selectors = {}
        follow = args.follow
        max_pages = args.max_pages

    # Handle different extraction modes
    try:
        if args.extract_links:
            print(f"Extracting links from: {args.url}")
            links = scraper.extract_links(args.url, args.selector or 'a')
            print(f"Found {len(links)} links")

            result = ScrapeResult(
                url=args.url,
                status_code=200,
                items=[ScrapedItem(url=args.url, href=l['href'], title=l['text'])
                       for l in links]
            )

        elif args.extract_tables:
            print(f"Extracting tables from: {args.url}")
            data = scraper.extract_tables(args.url, args.table_index)
            print(f"Found {len(data)} rows")

            # Convert to ScrapedItems
            items = []
            for row in data:
                item = ScrapedItem(url=args.url)
                item.data = row
                items.append(item)

            result = ScrapeResult(
                url=args.url,
                status_code=200,
                items=items
            )

        else:
            # Standard extraction
            if args.selectors:
                selectors = json.loads(args.selectors)
            elif args.selector:
                selectors = {'text': args.selector}
                if args.container:
                    selectors['_container'] = args.container

            if not selectors:
                # Default: extract all links
                selectors = {'href': 'a'}

            print(f"Scraping: {args.url}")
            print(f"Selectors: {selectors}")

            result = scraper.scrape(
                url=args.url,
                selectors=selectors,
                follow_links=follow,
                max_pages=max_pages
            )

        # Print summary
        print(f"\nScraping complete!")
        print(f"  URL: {result.url}")
        print(f"  Items found: {len(result.items)}")
        print(f"  Errors: {len(result.errors)}")

        if result.errors:
            for error in result.errors:
                print(f"    - {error}")

        # Save output
        if args.output:
            output_path = Path(args.output)
            output_format = args.format or output_path.suffix[1:].lower()

            if output_format == 'csv':
                ExportManager.to_csv(result.items, str(output_path))
            elif output_format == 'json':
                ExportManager.to_json(result, str(output_path), args.pretty)
            else:
                print(f"Unknown format: {output_format}")
                sys.exit(1)
        else:
            # Print first few items
            print("\nFirst 5 items:")
            for i, item in enumerate(result.items[:5]):
                print(f"  {i+1}. {item.title or item.text[:50] or item.href[:50]}")
                if item.title:
                    print(f"     Text: {item.text[:100]}")

    except (ValueError, TimeoutError, RuntimeError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
