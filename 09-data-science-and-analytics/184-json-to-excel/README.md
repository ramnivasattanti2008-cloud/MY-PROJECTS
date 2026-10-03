# JSON to Excel Converter

Convert JSON data to Excel (.xlsx) files with formatting and nested structure support.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python json-to-excel.py data.json
python json-to-excel.py data.json -o output.xlsx
python json-to-excel.py nested.json --no-flatten
python json-to-excel.py data.json --sheet "Sales Data"
```

## Options

| Flag | Description | Default |
|------|-------------|---------|
| `-o, --output` | Output Excel file | `<input>.xlsx` |
| `--sheet` | Sheet name | Data |
| `--no-flatten` | Keep nested objects as JSON strings | False (flatten) |
| `--max-col-width` | Maximum column width | 50 |

## Input Formats

### Array of Objects (Most Common)
```json
[
  {"name": "Alice", "age": 30},
  {"name": "Bob", "age": 25}
]
```

### Single Object
```json
{"name": "Alice", "age": 30}
```

### Nested Objects
```json
{"user": {"name": "Alice", "address": {"city": "NYC"}}}
```

## Output Features

- **Formatted headers** with styling
- **Auto column width** adjustment
- **Frozen header row**
- **Nested data flattening** (default) or preserved as JSON strings

## Examples

```bash
# Standard conversion
python json-to-excel.py records.json

# Keep nested structure as JSON strings
python json-to-excel.py nested.json --no-flatten

# Custom sheet name
python json-to-excel.py api_response.json --sheet "API Results"
```
