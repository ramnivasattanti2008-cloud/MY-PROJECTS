# CSV Cleaner

A Python CLI tool for cleaning and standardizing CSV files.

## Features

- Remove duplicate rows
- Handle missing values (drop or fill)
- Strip whitespace from values
- Convert text to uppercase or lowercase
- Remove empty rows
- Configurable file encoding

## Installation

No external dependencies required - uses Python standard library.

```bash
# Optional: create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Run directly
python csv-cleaner.py input.csv output.csv [options]
```

## Usage

### Basic Examples

```bash
# Remove duplicates
python csv-cleaner.py input.csv output.csv --deduplicate

# Drop rows with missing values
python csv-cleaner.py input.csv output.csv --dropna

# Fill missing values with "N/A"
python csv-cleaner.py output.csv output.csv --fillna "N/A"

# Strip whitespace from all values
python csv-cleaner.py input.csv output.csv --strip-whitespace

# Convert all strings to lowercase
python csv-cleaner.py input.csv output.csv --lowercase
```

### Combined Operations

```bash
# Clean a CSV with multiple operations
python csv-cleaner.py input.csv output.csv \
  --deduplicate \
  --strip-whitespace \
  --lowercase \
  --fillna "UNKNOWN"
```

### Working with Different Encodings

```bash
# Handle non-UTF8 files
python csv-cleaner.py input.csv output.csv --encoding latin-1
```

## Options

| Option | Description |
|--------|-------------|
| `input` | Input CSV file path (required) |
| `output` | Output CSV file path (required) |
| `--deduplicate` | Remove duplicate rows |
| `--dropna` | Drop rows with any missing values |
| `--fillna VALUE` | Fill missing values with VALUE |
| `--strip-whitespace` | Strip leading/trailing whitespace |
| `--lowercase` | Convert strings to lowercase |
| `--uppercase` | Convert strings to uppercase |
| `--remove-empty-rows` | Remove rows where all values are empty |
| `--encoding` | Input file encoding (default: utf-8) |

## License

MIT
