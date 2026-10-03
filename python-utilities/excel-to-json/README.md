# Excel to JSON Converter

A Python CLI tool for converting Excel and CSV files to JSON format.

## Features

- Convert CSV files to JSON
- Convert Excel files (.xlsx, .xls) to JSON
- Handle multiple sheets from Excel files
- Create nested structures from dot-notation headers
- Flatten nested objects into dot-notation keys
- Configurable header row selection
- Custom JSON indentation

## Installation

```bash
# Install dependencies
pip install -r excel-to-json-requirements.txt

# Or just install openpyxl for Excel support
pip install openpyxl
```

## Usage

### Basic Examples

```bash
# Convert CSV to JSON (output to stdout)
python excel-to-json.py data.csv

# Convert CSV to JSON file
python excel-to-json.py data.csv -o output.json

# Convert Excel file (all sheets)
python excel-to-json.py data.xlsx -o output.json

# Convert specific Excel sheet
python excel-to-json.py data.xlsx --sheet "Sales" -o output.json
```

### Nested Structures

```bash
# Create nested JSON from dot-notation headers
# e.g., "user.name.first" -> {"user": {"name": {"first": "..."}}}
python excel-to-json.py data.csv --nested -o output.json

# Flatten nested objects to dot-notation
python excel-to-json.py nested.json --flatten -o flat.json
```

### Advanced Options

```bash
# Custom header row (0-indexed)
python excel-to-json.py data.csv --header-row 2 -o output.json

# Custom JSON indentation
python excel-to-json.py data.csv --indent 4 -o output.json

# Different encoding
python excel-to-json.py data.csv --encoding latin-1 -o output.json
```

## Options

| Option | Description |
|--------|-------------|
| `input` | Input file (CSV or Excel) |
| `-o, --output` | Output JSON file (default: stdout) |
| `--sheet` | Specific sheet name to convert (Excel only) |
| `--all-sheets` | Convert all sheets (Excel only) |
| `--nested` | Create nested structure from dot-notation headers |
| `--header-row` | Row number to use as headers (0-indexed, default: 0) |
| `--indent` | JSON indentation spaces (default: 2) |
| `--flatten` | Flatten nested objects to dot-notation |
| `--encoding` | Input file encoding (default: utf-8) |

## Output Format

### Single Sheet (CSV or --sheet)
```json
[
  {"column1": "value1", "column2": "value2"},
  {"column1": "value3", "column2": "value4"}
]
```

### Multiple Sheets (Excel with --all-sheets)
```json
{
  "Sheet1": [...],
  "Sheet2": [...],
  "Data": [...]
}
```

## License

MIT
