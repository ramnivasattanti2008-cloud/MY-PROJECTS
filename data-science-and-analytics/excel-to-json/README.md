# Excel to JSON Converter

Convert Excel (.xlsx, .xls) and CSV files to JSON with support for multiple sheets.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python excel-to-json.py data.xlsx
python excel-to-json.py data.csv -o output.json
python excel-to-json.py data.xlsx --sheet "Sales"
python excel-to-json.py multi-sheet.xlsx --sheet "Overview"
```

## Options

| Flag | Description | Default |
|------|-------------|---------|
| `-o, --output` | Output JSON file | `<input>.json` |
| `--indent` | JSON indentation spaces | 2 |
| `--sheet` | Specific Excel sheet to convert | All sheets |
| `--encoding` | Input file encoding | utf-8 |

## Output Format

### Single Sheet
```json
[
  {"column1": "value1", "column2": "value2"},
  {"column1": "value3", "column2": "value4"}
]
```

### Multiple Sheets (Excel with no --sheet flag)
```json
{
  "Sheet1": [{"row": "data"}],
  "Sheet2": [{"row": "data"}]
}
```

## Requirements

- **openpyxl**: For reading .xlsx and .xls files
- Standard library: csv, json (for CSV files)

## Examples

```bash
# Convert Excel with all sheets as nested object
python excel-to-json.py workbook.xlsx -o data.json

# Convert specific sheet with pretty formatting
python excel-to-json.py report.xlsx --sheet "Q4 Sales" --indent 4

# Convert CSV with automatic encoding detection
python excel-to-json.py data.csv
```
