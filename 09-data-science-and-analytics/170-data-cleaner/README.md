# Data Cleaner

Clean messy CSV data by removing duplicates, fixing encoding issues, and trimming whitespace.

## Installation

No external dependencies required - uses Python standard library only.

```bash
pip install -r requirements.txt  # Optional (empty file, no installs needed)
```

## Usage

```bash
python data-cleaner.py dirty.csv
python data-cleaner.py dirty.csv -o cleaned.csv
python data-cleaner.py dirty.csv --dupe-keys name,email
python data-cleaner.py dirty.csv --normalize title
```

## Cleaning Operations

By default, the cleaner performs these operations:
1. **Fix encoding** - Converts smart quotes, em-dashes, non-breaking spaces
2. **Trim whitespace** - Removes leading/trailing spaces, normalizes multiple spaces
3. **Remove empty rows** - Removes rows where all values are empty
4. **Remove duplicates** - Removes duplicate rows based on all columns

## Options

| Flag | Description | Default |
|------|-------------|---------|
| `-o, --output` | Output file | `<input>_cleaned.csv` |
| `--no-dedupe` | Skip duplicate removal | False |
| `--dupe-keys` | Columns to check for duplicates | All columns |
| `--no-encoding` | Skip encoding fixes | False |
| `--no-whitespace` | Skip whitespace trimming | False |
| `--no-empty` | Skip empty row removal | False |
| `--normalize` | Case normalization (lower/upper/title) | None |
| `--encoding` | Input file encoding | utf-8 |
| `--output-encoding` | Output file encoding | utf-8 |
| `-v, --verbose` | Show detailed output | False |

## Encoding Fixes

Automatically fixes:
- Smart quotes: `'` `'` `'` `'` to `'`
- Smart quotes: `"` `"` `"` `"` to `"`
- Dashes: `-` `--` to `-`
- Non-breaking space: `` to space
- Degree symbol: `°` to `deg`

## Examples

```bash
# Standard cleaning
python data-cleaner.py contacts.csv

# Keep duplicates based on email only
python data-cleaner.py users.csv --dupe-keys email

# Normalize to title case
python data-cleaner.py names.csv --normalize title

# Minimal cleaning (just whitespace)
python data-cleaner.py data.csv --no-dedupe --no-encoding --no-empty

# Handle different encodings
python data-cleaner.py latin_data.csv --encoding latin-1
```

## Requirements

- Python 3.7+
- Standard library only (csv module)
