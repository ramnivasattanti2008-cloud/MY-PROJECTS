# JSON to CSV Converter

A Python CLI tool for converting JSON files to CSV format with support for nested JSON, flattening, and batch processing.

## Features

- Convert single JSON files to CSV
- Batch convert multiple files
- Flatten nested JSON objects
- Custom CSV delimiters (comma, tab, semicolon)
- Interactive mode for quick conversions
- Dry-run mode for previewing
- Preserve data types where possible

## Installation

```bash
pip install -r requirements.txt
```

No external dependencies required - uses only Python standard library.

## Usage

### Basic Conversion

```bash
# Convert a single file
python json-to-csv.py data.json

# Convert with custom output filename
python json-to-csv.py data.json -o output.csv

# Flatten nested JSON
python json-to-csv.py data.json --flatten

# Use tab delimiter
python json-to-csv.py data.json --tab
```

### Batch Conversion

```bash
# Convert all JSON files in current directory
python json-to-csv.py *.json

# Convert to a specific output directory
python json-to-csv.py *.json -o csv_output/

# Flatten and batch convert
python json-to-csv.py *.json --flatten -o flattened/
```

### Interactive Mode

```bash
python json-to-csv.py --interactive
```

Paste JSON data directly or enter a file path, choose options, and see the result.

### Options

| Option | Description |
|--------|-------------|
| `-o, --output` | Output file or directory |
| `-f, --flatten` | Flatten nested JSON objects |
| `-d, --delimiter` | CSV delimiter (default: comma) |
| `-t, --tab` | Use tab as delimiter |
| `-s, --semicolon` | Use semicolon as delimiter |
| `-i, --interactive` | Run in interactive mode |
| `--dry-run` | Preview without writing files |

## Examples

### Sample JSON Input

```json
{
  "users": [
    {"name": "John", "age": 30, "address": {"city": "NYC"}},
    {"name": "Jane", "age": 25, "address": {"city": "LA"}}
  ]
}
```

### Standard CSV Output

```csv
name,age,address
John,30,"{'city': 'NYC'}"
Jane,25,"{'city': 'LA'}"
```

### Flattened CSV Output

```csv
name,age,address_city
John,30,NYC
Jane,25,LA
```

## Requirements

- Python 3.6+
