# Web Scraper

A powerful and flexible web scraping tool using Python with requests and BeautifulSoup. Extract structured data from websites and export to CSV or JSON.

## Features

- CSS selector-based extraction
- Table extraction
- Link extraction
- Follow links across pages
- Rate limiting (polite scraping)
- Proxy support
- Custom headers
- Export to CSV and JSON
- Configuration file support

## Installation

```bash
pip install -r requirements.txt
```

## Quick Start

### Extract all links from a page

```bash
python web-scraper.py --url "https://example.com" --extract-links
```

### Extract specific elements using CSS selector

```bash
python web-scraper.py --url "https://example.com" --selector "h2.article-title"
```

### Extract multiple fields

```bash
python web-scraper.py --url "https://example.com" \
    --selectors '{"title": "h1", "text": "p", "href": "a.read-more"}'
```

### Follow links and scrape multiple pages

```bash
python web-scraper.py --url "https://example.com/blog" \
    --selector "article" \
    --follow \
    --max-pages 20
```

### Extract HTML tables

```bash
python web-scraper.py --url "https://example.com/data" --extract-tables
python web-scraper.py --url "https://example.com/data" --extract-tables --table-index 1
```

### Export to CSV

```bash
python web-scraper.py --url "https://example.com" --selector "li.product" \
    --output results.csv
```

### Export to JSON

```bash
python web-scraper.py --url "https://example.com" --selector "li.product" \
    --output results.json --format json
```

## Using Configuration Files

Create a `config.json`:
```json
{
    "selectors": {
        "title": "h2.product-name",
        "price": "span.price",
        "href": "a.product-link"
    },
    "follow": true,
    "max_pages": 50,
    "delay": 2.0,
    "timeout": 30
}
```

Run with config:
```bash
python web-scraper.py --url "https://shop.example.com" --config config.json --output products.csv
```

## Using as a Python Module

```python
from web-scraper import WebScraper, ExportManager

# Create scraper with rate limiting
scraper = WebScraper(delay=2.0, timeout=30)

# Scrape with selectors
result = scraper.scrape(
    url="https://example.com",
    selectors={
        'title': 'h1',
        'text': 'article p',
        'href': 'a.read-more'
    }
)

# Export to CSV
ExportManager.to_csv(result.items, 'output.csv')

# Export to JSON
ExportManager.to_json(result, 'output.json')

# Extract all links
links = scraper.extract_links("https://example.com")

# Extract tables
data = scraper.extract_tables("https://example.com/pricing")
```

## Command Line Options

| Option | Description |
|--------|-------------|
| `--url, -u` | URL to scrape (required) |
| `--config, -c` | Path to JSON configuration file |
| `--selector, -s` | CSS selector for elements |
| `--selectors` | JSON string of selectors |
| `--container` | CSS selector for container elements |
| `--extract-links` | Extract all links from page |
| `--extract-tables` | Extract HTML tables |
| `--table-index` | Table index to extract (default: 0) |
| `--follow` | Follow links on the page |
| `--max-pages` | Maximum pages to scrape (default: 10) |
| `--output, -o` | Output file path (CSV or JSON) |
| `--format, -f` | Output format: csv or json |
| `--delay` | Delay between requests (default: 1.0) |
| `--timeout` | Request timeout (default: 30) |
| `--user-agent` | Custom User-Agent string |
| `--proxy` | HTTP proxy URL |

## Example: Scraping a News Site

```bash
python web-scraper.py \
    --url "https://news.ycombinator.com/" \
    --selector "tr.athing" \
    --selectors '{"title": "a.storylink", "href": "a.storylink", "points": "span.score"}' \
    --output hacker_news.csv
```

## Example: Scraping Products

```bash
python web-scraper.py \
    --url "https://books.toscrape.com/" \
    --selector "article.product_pod" \
    --selectors '{"title": "h3 a", "price": "p.price_color", "href": "h3 a"}' \
    --follow \
    --max-pages 5 \
    --output books.csv
```

## Configuration File Schema

```json
{
    "selectors": {
        "field_name": "css.selector"
    },
    "follow": false,
    "max_pages": 10,
    "delay": 1.0,
    "timeout": 30,
    "user_agent": "Custom User Agent",
    "proxies": {
        "http": "http://proxy:8080",
        "https": "http://proxy:8080"
    },
    "headers": {
        "Authorization": "Bearer token"
    }
}
```

## Ethical Scraping

Please respect the following guidelines:

1. **Check robots.txt** - Look at `https://example.com/robots.txt`
2. **Rate limit** - Use `--delay` to add delays between requests
3. **Don't overload servers** - Keep concurrent requests low
4. **Respect terms of service** - Some sites prohibit scraping
5. **Use data responsibly** - Don't republish copyrighted content

## Troubleshooting

**"No module named 'requests'"**
```bash
pip install requests beautifulsoup4
```

**"Connection refused"**
- Check the URL is correct
- Some sites block scrapers - try with a different User-Agent
- You might need a proxy

**"Encoding error"**
- The script uses UTF-8 encoding by default
- For other encodings, modify the request headers

**Empty results**
- Check the CSS selector is correct
- Elements might be loaded dynamically (JavaScript)
- Try `--extract-links` to see what links are found

## License

MIT License
