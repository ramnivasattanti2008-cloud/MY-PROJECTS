#!/usr/bin/env python3
"""
JSON to Excel Converter
Convert JSON data to Excel (.xlsx) files, preserving nested structure.
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Any


def flatten_dict(d: dict, parent_key: str = "", sep: str = "_") -> dict:
    """Flatten nested dictionary."""
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        elif isinstance(v, list):
            # Convert lists to JSON string representation
            items.append((new_key, json.dumps(v)))
        else:
            items.append((new_key, v))
    return dict(items)


def json_to_rows(data: Any, flatten: bool = True) -> list[dict]:
    """Convert JSON data to list of row dictionaries."""

    # Handle array of objects
    if isinstance(data, list):
        if not data:
            return []
        if isinstance(data[0], dict):
            if flatten:
                return [flatten_dict(item) for item in data]
            return data
        # Array of primitives -> single column
        return [{"value": item} for item in data]

    # Handle single object
    if isinstance(data, dict):
        return [data]

    # Primitive value
    return [{"value": data}]


def convert_to_excel(json_path: Path, output_path: Path, sheet_name: str = "Data",
                     flatten: bool = True, max_col_width: int = 50):
    """Convert JSON file to Excel."""
    try:
        import openpyxl
        from openpyxl.styles import Font, Alignment, PatternFill
    except ImportError:
        print("Error: openpyxl not installed. Run: pip install openpyxl")
        sys.exit(1)

    # Read JSON
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Create workbook
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = sheet_name[:31]  # Excel sheet name limit

    # Convert to rows
    rows = json_to_rows(data, flatten)

    if not rows:
        wb.save(str(output_path))
        return 0

    # Get all columns from first row
    columns = list(rows[0].keys())

    # Write header
    header_font = Font(bold=True, color="FFFFFF")
    header_fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
    header_alignment = Alignment(horizontal="center")

    for col_idx, col_name in enumerate(columns, start=1):
        cell = ws.cell(row=1, column=col_idx, value=col_name)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = header_alignment

    # Write data rows
    for row_idx, row_data in enumerate(rows, start=2):
        for col_idx, col_name in enumerate(columns, start=1):
            value = row_data.get(col_name, "")
            cell = ws.cell(row=row_idx, column=col_idx, value=value)
            # Truncate long strings
            if isinstance(value, str) and len(value) > 32767:
                cell.value = value[:32764] + "..."
            # Auto-adjust column width
            col_letter = openpyxl.utils.get_column_letter(col_idx)
            col_width = min(max(len(str(col_name)), len(str(value))) + 2, max_col_width)
            if ws.column_dimensions[col_letter].width < col_width:
                ws.column_dimensions[col_letter].width = col_width

    # Freeze header row
    ws.freeze_panes = "A2"

    wb.save(str(output_path))
    return len(rows)


def main():
    parser = argparse.ArgumentParser(
        description="Convert JSON to Excel (.xlsx)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  json-to-excel.py data.json
  json-to-excel.py data.json -o output.xlsx
  json-to-excel.py nested.json --no-flatten
  json-to-excel.py data.json --sheet "Sales Data"
        """
    )
    parser.add_argument("input", type=Path, help="Input JSON file")
    parser.add_argument("-o", "--output", type=Path, help="Output Excel file (default: <input>.xlsx)")
    parser.add_argument("--sheet", default="Data", help="Sheet name (default: Data)")
    parser.add_argument("--no-flatten", action="store_true", help="Keep nested objects as-is (JSON string)")
    parser.add_argument("--max-col-width", type=int, default=50, help="Maximum column width")

    args = parser.parse_args()

    if not args.input.exists():
        print(f"Error: File not found: {args.input}")
        sys.exit(1)

    if args.output is None:
        output_path = args.input.with_suffix(".xlsx")
    else:
        output_path = args.output

    try:
        count = convert_to_excel(
            args.input, output_path, args.sheet,
            flatten=not args.no_flatten, max_col_width=args.max_col_width
        )
        print(f"Converted {count} row(s) -> {output_path}")
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON file: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
