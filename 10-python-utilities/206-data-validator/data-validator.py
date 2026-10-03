#!/usr/bin/env python3
"""
Data Validator Tool
Validates data against common rules (email, phone, dates, etc.)
and reports errors in a clear format.
"""

import argparse
import csv
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any


@dataclass
class ValidationError:
    """Represents a single validation error."""
    row: int
    field: str
    value: str
    rule: str
    message: str


@dataclass
class ValidationReport:
    """Collection of validation results."""
    errors: list[ValidationError] = field(default_factory=list)

    def add_error(self, row: int, field: str, value: str, rule: str, message: str) -> None:
        """Add a validation error to the report."""
        self.errors.append(ValidationError(row, field, value, rule, message))

    def has_errors(self) -> bool:
        """Check if any errors were found."""
        return len(self.errors) > 0

    def print_report(self, verbose: bool = False) -> None:
        """Print the validation report."""
        if not self.errors:
            print("\nValidation passed! No errors found.")
            return

        print(f"\n{'='*60}")
        print(f"VALIDATION REPORT: {len(self.errors)} error(s) found")
        print(f"{'='*60}")

        # Group errors by type
        errors_by_rule: dict[str, list[ValidationError]] = {}
        for error in self.errors:
            if error.rule not in errors_by_rule:
                errors_by_rule[error.rule] = []
            errors_by_rule[error.rule].append(error)

        # Print summary by rule
        print("\nErrors by Rule:")
        for rule, rule_errors in errors_by_rule.items():
            print(f"  - {rule}: {len(rule_errors)} error(s)")

        # Print detailed errors
        if verbose:
            print(f"\nDetailed Errors (showing first 50):")
            for error in self.errors[:50]:
                print(f"\n  Row {error.row}, Field '{error.field}':")
                print(f"    Value: '{error.value}'")
                print(f"    Rule: {error.rule}")
                print(f"    Message: {error.message}")

            if len(self.errors) > 50:
                print(f"\n  ... and {len(self.errors) - 50} more errors")


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Validate data against rules (email, phone, dates, etc.)"
    )
    parser.add_argument("input", help="Input CSV file path")
    parser.add_argument(
        "--rules",
        nargs="+",
        default=["all"],
        choices=["all", "email", "phone", "date", "url", "number", "required", "length"],
        help="Validation rules to apply (default: all)",
    )
    parser.add_argument(
        "--required-fields",
        nargs="+",
        help="Fields that are required (cannot be empty)",
    )
    parser.add_argument(
        "--date-format",
        default="%Y-%m-%d",
        help="Expected date format (default: %%Y-%%m-%%d)",
    )
    parser.add_argument(
        "--phone-format",
        default="international",
        choices=["international", "us", "india", "any"],
        help="Expected phone format (default: international)",
    )
    parser.add_argument(
        "--output",
        help="Output file for error report (CSV format)",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show detailed error output",
    )
    parser.add_argument(
        "--encoding",
        default="utf-8",
        help="Input file encoding (default: utf-8)",
    )
    return parser.parse_args()


# Validation patterns
EMAIL_PATTERN = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")

URL_PATTERN = re.compile(
    r"^https?://"
    r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|"
    r"localhost|"
    r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"
    r"(?::\d+)?"
    r"(?:/?|[/?]\S+)$",
    re.IGNORECASE,
)

# Phone patterns for different formats
PHONE_PATTERNS = {
    "international": re.compile(r"^\+?[1-9]\d{6,14}$"),  # E.164 format
    "us": re.compile(r"^\+?1?\s*\(?[0-9]{3}\)?[\s.-]?[0-9]{3}[\s.-]?[0-9]{4}$"),
    "india": re.compile(r"^(\+91[\-\s]?)?[6-9]\d{9}$"),
    "any": re.compile(r"^[\d\s\-\+\(\)]{7,20}$"),
}


def validate_email(value: str) -> tuple[bool, str]:
    """Validate email format."""
    if not value.strip():
        return True, ""  # Empty handled by required check
    if EMAIL_PATTERN.match(value.strip()):
        return True, ""
    return False, "Invalid email format"


def validate_phone(value: str, format_type: str) -> tuple[bool, str]:
    """Validate phone number format."""
    if not value.strip():
        return True, ""  # Empty handled by required check

    pattern = PHONE_PATTERNS.get(format_type, PHONE_PATTERNS["any"])
    cleaned = re.sub(r"[\s\-\(\)]", "", value.strip())

    if pattern.match(cleaned):
        return True, ""
    return False, f"Invalid phone format (expected {format_type} format)"


def validate_date(value: str, date_format: str) -> tuple[bool, str]:
    """Validate date format."""
    if not value.strip():
        return True, ""  # Empty handled by required check
    try:
        datetime.strptime(value.strip(), date_format)
        return True, ""
    except ValueError:
        return False, f"Invalid date format (expected: {date_format})"


def validate_url(value: str) -> tuple[bool, str]:
    """Validate URL format."""
    if not value.strip():
        return True, ""  # Empty handled by required check
    if URL_PATTERN.match(value.strip()):
        return True, ""
    return False, "Invalid URL format"


def validate_number(value: str) -> tuple[bool, str]:
    """Validate that value is a number."""
    if not value.strip():
        return True, ""  # Empty handled by required check
    try:
        float(value.strip())
        return True, ""
    except ValueError:
        return False, "Value is not a valid number"


def validate_required(value: str) -> tuple[bool, str]:
    """Validate that value is not empty."""
    if value.strip():
        return True, ""
    return False, "Field is required but empty"


def validate_length(value: str, max_length: int = 255) -> tuple[bool, str]:
    """Validate string length."""
    if len(value) <= max_length:
        return True, ""
    return False, f"Value exceeds maximum length of {max_length} characters"


def read_csv(filepath: Path, encoding: str) -> tuple[list[dict[str, Any]], list[str]]:
    """
    Read CSV file and return rows as list of dicts and fieldnames.
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


def infer_field_type(fieldname: str) -> list[str]:
    """
    Infer validation rules based on field name.
    """
    field_lower = fieldname.lower()
    rules = []

    if "email" in field_lower:
        rules.append("email")
    if "phone" in field_lower or "mobile" in field_lower or "tel" in field_lower:
        rules.append("phone")
    if "date" in field_lower or "dob" in field_lower or "birth" in field_lower:
        rules.append("date")
    if "url" in field_lower or "website" in field_lower or "link" in field_lower:
        rules.append("url")
    if "id" in field_lower or "count" in field_lower or "amount" in field_lower or "price" in field_lower:
        rules.append("number")

    return rules


def validate_row(
    row: dict[str, Any],
    row_num: int,
    fieldnames: list[str],
    rules: list[str],
    required_fields: set[str],
    date_format: str,
    phone_format: str,
) -> ValidationReport:
    """
    Validate a single row against all specified rules.
    """
    report = ValidationReport()

    # Build field-specific rules
    for field in fieldnames:
        value = row.get(field, "")
        field_rules = set()

        if "all" in rules:
            # Infer rules from field name
            field_rules.update(infer_field_type(field))
        else:
            field_rules.update(rules)

        # Add required check if specified
        if required_fields and field in required_fields:
            valid, msg = validate_required(value)
            if not valid:
                report.add_error(row_num, field, value, "required", msg)

        # Apply each rule
        for rule in field_rules:
            if rule == "email":
                valid, msg = validate_email(value)
            elif rule == "phone":
                valid, msg = validate_phone(value, phone_format)
            elif rule == "date":
                valid, msg = validate_date(value, date_format)
            elif rule == "url":
                valid, msg = validate_url(value)
            elif rule == "number":
                valid, msg = validate_number(value)
            elif rule == "required":
                valid, msg = validate_required(value)
            elif rule == "length":
                valid, msg = validate_length(value)
            else:
                continue

            if not valid:
                report.add_error(row_num, field, value, rule, msg)

    return report


def write_error_csv(output_path: Path, report: ValidationReport, fieldnames: list[str]) -> None:
    """Write errors to CSV file."""
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Row", "Field", "Value", "Rule", "Message"])

        for error in report.errors:
            writer.writerow([
                error.row,
                error.field,
                error.value,
                error.rule,
                error.message,
            ])


def main() -> None:
    """Main entry point for data validator."""
    args = parse_args()

    input_path = Path(args.input)
    print(f"Validating '{input_path}'...")

    # Read input file
    rows, fieldnames = read_csv(input_path, args.encoding)
    print(f"  Loaded {len(rows)} rows with {len(fieldnames)} columns")

    # Build required fields set
    required_fields = set(args.required_fields) if args.required_fields else set()

    # Validate all rows
    full_report = ValidationReport()
    for i, row in enumerate(rows, start=1):
        row_report = validate_row(
            row, i, fieldnames, args.rules,
            required_fields, args.date_format, args.phone_format,
        )
        full_report.errors.extend(row_report.errors)

    # Print report
    full_report.print_report(args.verbose)

    # Write error CSV if requested
    if args.output:
        write_error_csv(Path(args.output), full_report, fieldnames)
        print(f"\nError report written to '{args.output}'")

    # Exit with appropriate code
    sys.exit(1 if full_report.has_errors() else 0)


if __name__ == "__main__":
    main()
