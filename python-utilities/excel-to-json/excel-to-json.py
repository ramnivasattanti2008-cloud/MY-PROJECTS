#!/usr/bin/env python3
"""
Excel to JSON Converter
Converts Excel (.xlsx, .xls) and CSV files to JSON format.
Supports multiple sheets and nested data structures.
"""

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Any


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Convert Excel/CSV files to JSON format"
    )
    parser.add_argument("input", help="Input file (CSV or Excel)")
    parser.add_argument(
        "-o", "--output",
        help="Output JSON file (default: stdout)",
    )
    parser.add_argument(
        "--sheet",
        help="Specific sheet name to convert (Excel only)",
    )
    parser.add_argument(
        "--all-sheets",
        action="store_true",
        help="Convert all sheets (Excel only, default: true)",
    )
    parser.add_argument(
        "--nested",
        action="store_true",
        help="Create nested structure from column headers",
    )
    parser.add_argument(
        "--header-row",
        type=int,
        default=0,
        help="Row number to use as headers (0-indexed, default: 0)",
    )
    parser.add_argument(
        "--indent",
        type=int,
        default=2,
        help="JSON indentation spaces (default: 2)",
    )
    parser.add_argument(
        "--flatten",
        action="store_true",
        help="Flatten nested objects into dot-notation keys",
    )
    parser.add_argument(
        "--encoding",
        default="utf-8",
        help="Input file encoding (default: utf-8)",
    )
    return parser.parse_args()


def read_csv(filepath: Path, encoding: str, header_row: int) -> list[dict[str, Any]]:
    """
    Read CSV file and return list of dictionaries.

    Args:
        filepath: Path to CSV file
        encoding: File encoding
        header_row: Row number to use as headers

    Returns:
        List of row dictionaries
    """
    try:
        with open(filepath, "r", newline="", encoding=encoding) as f:
            reader = csv.reader(f)
            rows = list(reader)
    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found", file=sys.stderr)
        sys.exit(1)
    except UnicodeDecodeError:
        print(f"Error: Could not decode file with {encoding} encoding", file=sys.stderr)
        sys.exit(1)

    if not rows:
        return []

    # Handle header row selection
    if header_row > 0:
        headers = rows[header_row]
        data_rows = rows[header_row + 1 :]
    else:
        headers = rows[0]
        data_rows = rows[1:]

    # Build list of dictionaries
    result = []
    for row in data_rows:
        record = {}
        for i, header in enumerate(headers):
            value = row[i] if i < len(row) else ""
            record[header.strip()] = value.strip()
        result.append(record)

    return result


def try_read_excel(filepath: Path) -> tuple[bool, Any, Any]:
    """
    Try to read Excel file. Returns (success, sheets, workbook).

    Args:
        filepath: Path to Excel file

    Returns:
        Tuple of (success, sheet_names or error_message, workbook or None)
    """
    try:
        import openpyxl

        try:
            wb = openpyxl.load_workbook(filepath, data_only=True)
            return True, wb.sheetnames, wb
        except ImportError:
            return False, "openpyxl not installed", None
        except Exception as e:
            return False, str(e), None

    except ImportError:
        return False, "openpyxl not installed", None


def read_excel_sheet(wb: Any, sheet_name: str, header_row: int) -> list[dict[str, Any]]:
    """
    Read a single Excel sheet and return list of dictionaries.

    Args:
        wb: openpyxl workbook
        sheet_name: Name of sheet to read
        header_row: Row number to use as headers (0-indexed)

    Returns:
        List of row dictionaries
    """
    sheet = wb[sheet_name]
    rows = list(sheet.iter_rows(values_only=True))

    if not rows:
        return []

    # Handle header row selection
    if header_row > 0:
        headers = rows[header_row]
        data_rows = rows[header_row + 1 :]
    else:
        headers = rows[0]
        data_rows = rows[1:]

    # Convert headers to strings and clean
    headers = [str(h).strip() if h is not None else f"Column_{i}" for i, h in enumerate(headers)]

    # Build list of dictionaries
    result = []
    for row in data_rows:
        record = {}
        for i, header in enumerate(headers):
            value = row[i] if i < len(row) else None
            # Clean up the value
            if isinstance(value, str):
                value = value.strip()
            elif value is None:
                value = ""
            record[header] = value
        result.append(record)

    return result


def flatten_object(obj: dict[str, Any], parent_key: str = "", sep: str = ".") -> dict[str, Any]:
    """
    Flatten a nested dictionary into dot-notation keys.

    Args:
        obj: Dictionary to flatten
        parent_key: Prefix for keys
        sep: Separator character

    Returns:
        Flattened dictionary
    """
    items: list[tuple[str, Any]] = []

    for key, value in obj.items():
        new_key = f"{parent_key}{sep}{key}" if parent_key else key

        if isinstance(value, dict):
            items.extend(flatten_object(value, new_key, sep=sep).items())
        elif isinstance(value, list) and value and isinstance(value[0], dict):
            # Handle list of objects
            for i, item in enumerate(value):
                if isinstance(item, dict):
                    items.extend(flatten_object(item, f"{new_key}[{i}]", sep=sep).items())
                else:
                    items.append((f"{new_key}[{i}]", item))
        else:
            items.append((new_key, value))

    return dict(items)


def create_nested_structure(rows: list[dict[str, Any]]) -> dict[str, Any]:
    """
    Convert flat rows with dot-notation keys into nested structures.

    Args:
        rows: List of flat dictionaries

    Returns:
        List of nested dictionaries
    """
    result = []

    for row in rows:
        nested = {}
        for key, value in row.items():
            if "." in key:
                # Create nested structure
                parts = key.split(".")
                current = nested
                for part in parts[:-1]:
                    if part not in current:
                        current[part] = {}
                    current = current[part]
                current[parts[-1]] = value
            else:
                nested[key] = value
        result.append(nested)

    return result


def convert_to_json(
    data: list[dict[str, Any]],
    indent: int,
    flatten: bool,
    nested: bool,
) -> str:
    """
    Convert data to JSON string.

    Args:
        data: List of row dictionaries
        indent: JSON indentation
        flatten: Whether to flatten nested objects
        nested: Whether to create nested structures

    Returns:
        JSON string
    """
    # Apply nested structure if requested
    if nested:
        data = create_nested_structure(data)

    # Apply flattening if requested
    if flatten:
        data = [flatten_object(row) for row in data]

    return json.dumps(data, indent=indent, ensure_ascii=False, default=str)


def main() -> None:
    """Main entry point for Excel to JSON converter."""
    args = parse_args()

    input_path = Path(args.input)
    print(f"Converting '{input_path}'...")

    # Determine file type
    suffix = input_path.suffix.lower()

    if suffix == ".csv":
        # CSV conversion
        print("  Format: CSV")
        data = read_csv(input_path, args.encoding, args.header_row)
        print(f"  Rows: {len(data)}")

        # Convert single sheet format
        output_data = {"sheet1": data} if args.all_sheets else data

    elif suffix in [".xlsx", ".xls"]:
        # Excel conversion
        print("  Format: Excel")

        success, sheets_or_error, wb = try_read_excel(input_path)

        if not success:
            print(f"Error: Could not read Excel file - {sheets_or_error}", file=sys.stderr)
            print("\nInstall openpyxl to read Excel files:", file=sys.stderr)
            print("  pip install openpyxl", file=sys.stderr)
            sys.exit(1)

        output_data = {}

        if args.sheet:
            # Single sheet specified
            if args.sheet in sheets_or_error:
                data = read_excel_sheet(wb, args.sheet, args.header_row)
                output_data[args.sheet] = data
                print(f"  Sheet: {args.sheet}")
                print(f"  Rows: {len(data)}")
            else:
                print(f"Error: Sheet '{args.sheet}' not found", file=sys.stderr)
                print(f"Available sheets: {', '.join(sheets_or_error)}", file=sys.stderr)
                sys.exit(1)
        else:
            # All sheets
            for sheet_name in sheets_or_error:
                data = read_excel_sheet(wb, sheet_name, args.header_row)
                output_data[sheet_name] = data
                print(f"  Sheet '{sheet_name}': {len(data)} rows")

    else:
        print(f"Error: Unsupported file format '{suffix}'", file=sys.stderr)
        print("Supported formats: .csv, .xlsx, .xls", file=sys.stderr)
        sys.exit(1)

    # Convert to JSON
    json_output = convert_to_json(
        output_data if args.all_sheets or suffix != ".csv" else output_data,
        args.indent,
        args.flatten,
        args.nested,
    )

    # Output
    if args.output:
        output_path = Path(args.output)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(json_output)
        print(f"\nOutput written to '{output_path}'")
    else:
        print("\n" + json_output)


if __name__ == "__main__":
    main()
