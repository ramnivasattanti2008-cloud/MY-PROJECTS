#!/usr/bin/env python3
"""
Excel/CSV to JSON Converter
Convert Excel (.xlsx, .xls) and CSV files to JSON with support for multiple sheets.
"""

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Any


def read_csv(file_path: Path, encoding: str = "utf-8") -> list[dict]:
    """Read CSV file and return list of dictionaries."""
    rows = []
    try:
        with open(file_path, "r", encoding=encoding, newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                cleaned_row = {k: v.strip() if isinstance(v, str) else v for k, v in row.items()}
                rows.append(cleaned_row)
    except UnicodeDecodeError:
        # Try with different encodings
        for enc in ["latin-1", "cp1252", "iso-8859-1"]:
            try:
                rows = []
                with open(file_path, "r", encoding=enc, newline="") as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        cleaned_row = {k: v.strip() if isinstance(v, str) else v for k, v in row.items()}
                        rows.append(cleaned_row)
                break
            except UnicodeDecodeError:
                continue
        else:
            raise
    return rows


def read_excel_sheets(file_path: Path, sheet_name: str = None) -> dict[str, list[dict]]:
    """Read Excel file and return dictionary of sheet_name -> list of rows."""
    try:
        import openpyxl
    except ImportError:
        print("Error: openpyxl not installed. Run: pip install openpyxl")
        sys.exit(1)

    wb = openpyxl.load_workbook(str(file_path), data_only=True)
    result = {}

    sheets_to_process = [sheet_name] if sheet_name else wb.sheetnames

    for sheet in sheets_to_process:
        if sheet not in wb.sheetnames:
            print(f"Warning: Sheet '{sheet}' not found")
            continue

        ws = wb[sheet]
        rows = []

        # Get headers from first row
        headers = []
        for cell in next(ws.iter_rows(min_row=1, max_row=1)):
            headers.append(cell.value if cell.value is not None else f"column_{cell.column}")

        # Read data rows
        for row_idx, row in enumerate(ws.iter_rows(min_row=2, values_only=True), start=2):
            row_dict = {}
            for header, value in zip(headers, row):
                if value is None:
                    row_dict[header] = None
                elif isinstance(value, (int, float)):
                    row_dict[header] = value
                elif isinstance(value, str):
                    row_dict[header] = value.strip()
                else:
                    row_dict[header] = str(value)
            rows.append(row_dict)

        result[sheet] = rows

    wb.close()
    return result


def convert_file(input_path: Path, output_path: Path = None, indent: int = 2,
                  sheet: str = None, encoding: str = "utf-8"):
    """Convert Excel/CSV file to JSON."""

    if input_path.suffix.lower() in [".xlsx", ".xls", ".xlsm"]:
        data = read_excel_sheets(input_path, sheet)

        # Single sheet requested -> output as array
        if sheet:
            output_data = data.get(sheet, [])
        else:
            output_data = data

    elif input_path.suffix.lower() == ".csv":
        rows = read_csv(input_path, encoding)
        output_data = rows
    else:
        print(f"Error: Unsupported file type: {input_path.suffix}")
        sys.exit(1)

    # Determine output path
    if output_path is None:
        output_path = input_path.with_suffix(".json")

    # Write JSON
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=indent, ensure_ascii=False)

    return output_path, len(output_data if isinstance(output_data, list) else sum(len(v) for v in output_data.values()))


def main():
    parser = argparse.ArgumentParser(
        description="Convert Excel/CSV files to JSON",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  excel-to-json.py data.xlsx
  excel-to-json.py data.csv -o output.json
  excel-to-json.py data.xlsx --sheet "Sales 2024"
  excel-to-json.py data.xlsx --indent 4
        """
    )
    parser.add_argument("input", type=Path, help="Input Excel (.xlsx, .xls) or CSV file")
    parser.add_argument("-o", "--output", type=Path, help="Output JSON file (default: <input>.json)")
    parser.add_argument("--indent", type=int, default=2, help="JSON indentation (default: 2)")
    parser.add_argument("--sheet", help="Specific sheet to convert (Excel only)")
    parser.add_argument("--encoding", default="utf-8", help="Input file encoding (default: utf-8)")

    args = parser.parse_args()

    if not args.input.exists():
        print(f"Error: File not found: {args.input}")
        sys.exit(1)

    try:
        output_path, count = convert_file(
            args.input, args.output, args.indent, args.sheet, args.encoding
        )
        print(f"Converted {count} row(s) -> {output_path}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
