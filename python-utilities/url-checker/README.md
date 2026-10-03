# URL Checker

A Python CLI tool to check if URLs are alive, returning status codes and response times.

## Features

- Check single or multiple URLs
- Batch processing from a text file
- Measure response time in milliseconds
- Support for redirects
- JSON/CSV export options
- Configurable timeout and rate limiting

## Installation

```bash
pip install -r requirements/url-checker-requirements.txt
```

## Usage

### Check a single URL

```bash
python url-checker.py https://example.com
```

### Batch check from file

Create a file `urls.txt` with one URL per line:
```
https://example.com
https://google.com
https://github.com
```

Then run:
```bash
python url-checker.py urls.txt
```

### Export results

```bash
# JSON format
python url-checker.py urls.txt --json -o results.json

# CSV format
python url-checker.py urls.txt --csv -o results.csv
```

### Options

| Option | Description | Default |
|--------|-------------|---------|
| `--timeout` | Request timeout in seconds | 10 |
| `--delay` | Delay between requests (rate limiting) | 0 |
| `--json` | Output as JSON | False |
| `--csv` | Output as CSV | False |
| `-o, --output` | Output file path | results.json/csv |

## Example Output

```
URL                                                  Status   Time (ms)   Result
------------------------------------------------------------------------------------------
https://example.com                                  200      145.3       OK
https://google.com                                   200      89.7        OK
https://nonexistent.invalid                          ERROR    -           ERROR: Connection...
------------------------------------------------------------------------------------------
Summary: 2/3 URLs are alive
```

## Exit Codes

- `0`: All URLs are alive
- `1`: One or more URLs failed
