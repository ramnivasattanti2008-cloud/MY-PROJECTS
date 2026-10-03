#!/usr/bin/env python3
"""
Data Cleaner
Clean messy data by removing duplicates, fixing encoding, and trimming whitespace.
"""

import argparse
import csv
import sys
from pathlib import Path
from typing import Any, Callable


def read_csv(file_path: Path, encoding: str = "utf-8") -> tuple[list[str], list[dict]]:
    """Read CSV file with encoding fallback."""
    encodings_to_try = [encoding, "utf-8", "latin-1", "cp1252", "iso-8859-1"]

    for enc in encodings_to_try:
        try:
            with open(file_path, "r", encoding=enc, newline="") as f:
                reader = csv.DictReader(f)
                headers = reader.fieldnames or []
                rows = list(reader)
                return headers, rows
        except UnicodeDecodeError:
            continue

    raise ValueError(f"Could not read file with any supported encoding")


def write_csv(file_path: Path, headers: list[str], rows: list[dict], encoding: str = "utf-8"):
    """Write CSV file."""
    with open(file_path, "w", encoding=encoding, newline="") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)


def clean_text(value: Any) -> str:
    """Clean a single text value."""
    if value is None:
        return ""
    if not isinstance(value, str):
        value = str(value)

    # Fix common encoding issues
    replacements = {
        "‘": "'",  # Left single quote
        "’": "'",  # Right single quote
        "“": '"',  # Left double quote
        "”": '"',  # Right double quote
        "–": "-",  # En dash
        "—": "-",  # Em dash
        " ": " ",  # Non-breaking space
        "°": "deg",  # Degree symbol
    }
    for bad, good in replacements.items():
        value = value.replace(bad, good)

    # Trim whitespace
    value = value.strip()

    # Normalize multiple spaces
    while "  " in value:
        value = value.replace("  ", " ")

    return value


def remove_duplicates(rows: list[dict], key_columns: list[str] = None) -> list[dict]:
    """Remove duplicate rows based on key columns or entire row."""
    seen = set()
    unique_rows = []

    for row in rows:
        if key_columns:
            key = tuple(row.get(col, "").strip().lower() for col in key_columns if col in row)
        else:
            key = tuple(sorted(row.items()))

        # Create hashable key
        try:
            key_hash = hash(key)
        except TypeError:
            # Handle unhashable items
            key_str = str(key).lower()
            key_hash = hash(key_str)

        if key_hash not in seen:
            seen.add(key_hash)
            unique_rows.append(row)

    return unique_rows


def fix_encoding(rows: list[dict], headers: list[str]) -> list[dict]:
    """Fix encoding issues in data."""
    cleaned_rows = []
    for row in rows:
        cleaned_row = {}
        for header in headers:
            value = row.get(header, "")
            cleaned_row[header] = clean_text(value)
        cleaned_rows.append(cleaned_row)
    return cleaned_rows


def trim_whitespace(rows: list[dict], headers: list[str]) -> list[dict]:
    """Trim whitespace from all string values."""
    cleaned_rows = []
    for row in rows:
        cleaned_row = {h: row.get(h, "").strip() if isinstance(row.get(h), str) else row.get(h, "")
                       for h in headers}
        cleaned_rows.append(cleaned_row)
    return cleaned_rows


def remove_empty_rows(rows: list[dict], headers: list[str]) -> list[dict]:
    """Remove rows where all values are empty."""
    cleaned_rows = []
    for row in rows:
        if any(row.get(h, "").strip() for h in headers):
            cleaned_rows.append(row)
    return cleaned_rows


def normalize_case(rows: list[dict], headers: list[str], mode: str = "lower") -> list[dict]:
    """Normalize case of string values."""
    cleaned_rows = []
    for row in rows:
        cleaned_row = {}
        for header in headers:
            value = row.get(header, "")
            if isinstance(value, str):
                if mode == "lower":
                    value = value.lower()
                elif mode == "upper":
                    value = value.upper()
                elif mode == "title":
                    value = value.title()
            cleaned_row[header] = value
        cleaned_rows.append(cleaned_row)
    return cleaned_rows


def clean_data(input_path: Path, output_path: Path = None,
               remove_dupe: bool = True, dupe_keys: list[str] = None,
               fix_encoding_issues: bool = True, trim_whitespace_: bool = True,
               remove_empty: bool = True, normalize_to: str = None,
               encoding: str = "utf-8", output_encoding: str = "utf-8"):
    """Clean data with specified options."""

    # Read data
    headers, rows = read_csv(input_path, encoding)
    original_count = len(rows)

    if not rows:
        print("Warning: Input file is empty")
        return 0, 0

    # Apply cleaning operations
    operations = []

    if fix_encoding_issues:
        rows = fix_encoding(rows, headers)
        operations.append("encoding")

    if trim_whitespace_:
        rows = trim_whitespace(rows, headers)
        operations.append("whitespace")

    if remove_empty:
        before = len(rows)
        rows = remove_empty_rows(rows, headers)
        if len(rows) < before:
            operations.append("empty rows")

    if normalize_to:
        rows = normalize_case(rows, headers, normalize_to)
        operations.append(f"case ({normalize_to})")

    if remove_dupe:
        before = len(rows)
        rows = remove_duplicates(rows, dupe_keys)
        if len(rows) < before:
            operations.append(f"duplicates ({before - len(rows)} removed)")

    # Determine output path
    if output_path is None:
        output_path = input_path.with_name(f"{input_path.stem}_cleaned{input_path.suffix}")

    # Write output
    write_csv(output_path, headers, rows, output_encoding)

    return original_count, len(rows)


def main():
    parser = argparse.ArgumentParser(
        description="Clean messy CSV data",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  data-cleaner.py dirty.csv
  data-cleaner.py dirty.csv -o cleaned.csv
  data-cleaner.py dirty.csv --no-dedupe
  data-cleaner.py dirty.csv --dupe-keys name,email
  data-cleaner.py dirty.csv --normalize title
        """
    )
    parser.add_argument("input", type=Path, help="Input CSV file")
    parser.add_argument("-o", "--output", type=Path, help="Output file (default: <input>_cleaned.csv)")
    parser.add_argument("--no-dedupe", action="store_true", help="Skip duplicate removal")
    parser.add_argument("--dupe-keys", help="Comma-separated columns to check for duplicates")
    parser.add_argument("--no-encoding", action="store_true", help="Skip encoding fixes")
    parser.add_argument("--no-whitespace", action="store_true", help="Skip whitespace trimming")
    parser.add_argument("--no-empty", action="store_true", help="Skip empty row removal")
    parser.add_argument("--normalize", choices=["lower", "upper", "title"], help="Normalize text case")
    parser.add_argument("--encoding", default="utf-8", help="Input file encoding")
    parser.add_argument("--output-encoding", default="utf-8", help="Output file encoding")
    parser.add_argument("-v", "--verbose", action="store_true", help="Show details")

    args = parser.parse_args()

    if not args.input.exists():
        print(f"Error: File not found: {args.input}")
        sys.exit(1)

    dupe_keys = args.dupe_keys.split(",") if args.dupe_keys else None

    try:
        original, cleaned = clean_data(
            args.input, args.output,
            remove_dupe=not args.no_dupe,
            dupe_keys=dupe_keys,
            fix_encoding_issues=not args.no_encoding,
            trim_whitespace_=not args.no_whitespace,
            remove_empty=not args.no_empty,
            normalize_to=args.normalize,
            encoding=args.encoding,
            output_encoding=args.output_encoding
        )

        removed = original - cleaned
        print(f"Cleaned: {original} -> {cleaned} rows ({removed} removed)")

        if args.verbose and removed > 0:
            print(f"  Removed {removed} duplicate/empty rows")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
