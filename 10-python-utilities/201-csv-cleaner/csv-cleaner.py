#!/usr/bin/env python3
"""
CSV Cleaner Tool
Cleans CSV files by removing duplicates, handling missing values,
standardizing formats, and validating data.
"""

import argparse
import csv
import sys
from pathlib import Path
from typing import Any


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Clean CSV files - remove duplicates, handle missing values, standardize formats"
    )
    parser.add_argument("input", help="Input CSV file path")
    parser.add_argument("output", help="Output CSV file path")
    parser.add_argument(
        "--deduplicate",
        action="store_true",
        help="Remove duplicate rows",
    )
    parser.add_argument(
        "--dropna",
        action="store_true",
        help="Drop rows with missing values",
    )
    parser.add_argument(
        "--fillna",
        metavar="VALUE",
        help="Fill missing values with specified value",
    )
    parser.add_argument(
        "--strip-whitespace",
        action="store_true",
        help="Strip whitespace from all string values",
    )
    parser.add_argument(
        "--lowercase",
        action="store_true",
        help="Convert string values to lowercase",
    )
    parser.add_argument(
        "--uppercase",
        action="store_true",
        help="Convert string values to uppercase",
    )
    parser.add_argument(
        "--remove-empty-rows",
        action="store_true",
        help="Remove completely empty rows",
    )
    parser.add_argument(
        "--encoding",
        default="utf-8",
        help="Input file encoding (default: utf-8)",
    )
    return parser.parse_args()


def read_csv(filepath: Path, encoding: str) -> tuple[list[dict[str, Any]], list[str]]:
    """
    Read CSV file and return rows as list of dicts and fieldnames.

    Args:
        filepath: Path to the CSV file
        encoding: File encoding

    Returns:
        Tuple of (rows, fieldnames)
    """
    try:
        with open(filepath, "r", newline="", encoding=encoding) as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            fieldnames = reader.fieldnames or []
            return rows, fieldnames
    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found", file=sys.stderr)
        sys.exit(1)
    except UnicodeDecodeError:
        print(f"Error: Could not decode file with {encoding} encoding", file=sys.stderr)
        sys.exit(1)


def write_csv(
    filepath: Path,
    rows: list[dict[str, Any]],
    fieldnames: list[str],
    encoding: str,
) -> None:
    """
    Write rows to CSV file.

    Args:
        filepath: Output file path
        rows: List of row dictionaries
        fieldnames: Column names
        encoding: File encoding
    """
    with open(filepath, "w", newline="", encoding=encoding) as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def remove_duplicates(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """
    Remove duplicate rows from the data.

    Args:
        rows: List of row dictionaries

    Returns:
        List with duplicates removed
    """
    seen = set()
    unique_rows = []

    for row in rows:
        # Create a hashable representation of the row
        row_tuple = tuple(sorted(row.items()))
        if row_tuple not in seen:
            seen.add(row_tuple)
            unique_rows.append(row)

    return unique_rows


def drop_na_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """
    Remove rows that contain any missing (empty) values.

    Args:
        rows: List of row dictionaries

    Returns:
        List with NA rows removed
    """
    return [row for row in rows if all(value.strip() for value in row.values())]


def fill_na_rows(
    rows: list[dict[str, Any]],
    fill_value: str,
) -> list[dict[str, Any]]:
    """
    Fill missing values in all rows with specified value.

    Args:
        rows: List of row dictionaries
        fill_value: Value to fill missing cells with

    Returns:
        List with filled values
    """
    for row in rows:
        for key, value in row.items():
            if not value.strip():
                row[key] = fill_value
    return rows


def strip_whitespace(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """
    Strip whitespace from all string values.

    Args:
        rows: List of row dictionaries

    Returns:
        List with whitespace stripped
    """
    for row in rows:
        for key, value in row.items():
            if isinstance(value, str):
                row[key] = value.strip()
    return rows


def lowercase_strings(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """
    Convert all string values to lowercase.

    Args:
        rows: List of row dictionaries

    Returns:
        List with lowercase strings
    """
    for row in rows:
        for key, value in row.items():
            if isinstance(value, str):
                row[key] = value.lower()
    return rows


def uppercase_strings(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """
    Convert all string values to uppercase.

    Args:
        rows: List of row dictionaries

    Returns:
        List with uppercase strings
    """
    for row in rows:
        for key, value in row.items():
            if isinstance(value, str):
                row[key] = value.upper()
    return rows


def remove_empty_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """
    Remove rows where all values are empty.

    Args:
        rows: List of row dictionaries

    Returns:
        List with empty rows removed
    """
    return [row for row in rows if any(value.strip() for value in row.values())]


def main() -> None:
    """Main entry point for CSV cleaner."""
    args = parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)

    # Read input file
    print(f"Reading '{input_path}'...")
    rows, fieldnames = read_csv(input_path, args.encoding)
    original_count = len(rows)
    print(f"  Loaded {original_count} rows with {len(fieldnames)} columns")

    # Apply cleaning operations
    if args.deduplicate:
        rows = remove_duplicates(rows)
        print(f"  Removed {original_count - len(rows)} duplicate rows")

    if args.remove_empty_rows:
        rows = remove_empty_rows(rows)
        print(f"  Removed {original_count - len(rows)} empty rows")

    if args.dropna:
        rows = drop_na_rows(rows)
        print(f"  Dropped {original_count - len(rows)} rows with missing values")

    if args.fillna is not None:
        rows = fill_na_rows(rows, args.fillna)
        print(f"  Filled missing values with '{args.fillna}'")

    if args.strip_whitespace:
        rows = strip_whitespace(rows)
        print("  Stripped whitespace from all values")

    if args.lowercase:
        rows = lowercase_strings(rows)
        print("  Converted strings to lowercase")

    if args.uppercase:
        rows = uppercase_strings(rows)
        print("  Converted strings to uppercase")

    # Write output file
    print(f"Writing '{output_path}'...")
    write_csv(output_path, rows, fieldnames, args.encoding)
    print(f"  Wrote {len(rows)} rows")

    print("\nDone!")


if __name__ == "__main__":
    main()
