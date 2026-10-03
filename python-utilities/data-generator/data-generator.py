#!/usr/bin/env python3
"""
Data Generator Tool
Generates fake data (names, addresses, emails, companies) for testing.
Fully configurable via CLI arguments.
"""

import argparse
import csv
import json
import random
import sys
from pathlib import Path
from typing import Any


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate fake data for testing purposes"
    )
    parser.add_argument(
        "-n", "--count",
        type=int,
        default=10,
        help="Number of records to generate (default: 10)",
    )
    parser.add_argument(
        "-o", "--output",
        help="Output file (CSV or JSON, default: stdout)",
    )
    parser.add_argument(
        "--format",
        choices=["csv", "json", "both"],
        default="csv",
        help="Output format (default: csv)",
    )
    parser.add_argument(
        "--fields",
        nargs="+",
        default=["name", "email", "phone", "address", "company"],
        help="Fields to generate (default: all)",
    )
    parser.add_argument(
        "--seed",
        type=int,
        help="Random seed for reproducible data",
    )
    parser.add_argument(
        "--locale",
        default="us",
        choices=["us", "uk", "india"],
        help="Locale for data generation (default: us)",
    )
    parser.add_argument(
        "--indent",
        type=int,
        default=2,
        help="JSON indentation spaces (default: 2)",
    )
    return parser.parse_args()


# Sample data for generation
FIRST_NAMES = {
    "us": ["James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda",
           "William", "Elizabeth", "David", "Barbara", "Richard", "Susan", "Joseph", "Jessica"],
    "uk": ["Oliver", "Amelia", "Harry", "Emily", "Jack", " Isla", "George", "Ava",
           "Noah", "Sophia", "William", "Poppy", "Thomas", "Grace", "Charlie", "Mia"],
    "india": ["Arjun", "Sneha", "Vikram", "Priya", "Rohan", "Ananya", "Aditya", "Diya",
              "Raj", "Kavya", "Amit", "Riya", "Sanjay", "Meera", "Nikhil", "Pooja"],
}

LAST_NAMES = {
    "us": ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
           "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas"],
    "uk": ["Smith", "Jones", "Williams", "Brown", "Taylor", "Davies", "Wilson", "Evans",
           "Thomas", "Roberts", "Walker", "Wright", "Robinson", "Thompson", "White", "Hughes"],
    "india": ["Sharma", "Singh", "Patel", "Kumar", "Reddy", "Gupta", "Singh", "Agarwal",
              "Verma", "Joshi", "Mehta", "Shah", "Chandra", "Nair", "Rao", "Iyengar"],
}

COMPANIES = [
    "Acme Corp", "TechStart Inc", "Global Solutions", "Innovate Labs",
    "Prime Systems", "Nexus Group", "Quantum Tech", "Stellar Industries",
    "Alpha Dynamics", "Beta Works", "Gamma Solutions", "Delta Partners",
    "Epsilon Ventures", "Zeta Holdings", "Omega Enterprises", "Sigma Group",
    "Phoenix Technologies", "Aurora Systems", "Nova Industries", "Vertex Corp",
]

STREET_NAMES = [
    "Main St", "Oak Ave", "Maple Dr", "Cedar Ln", "Pine Rd", "Elm St",
    "Washington Blvd", "Lincoln Ave", "Park Dr", "Lake View Rd",
    "Sunset Blvd", "Highland Ave", "Valley Dr", "River Rd", "Hill St",
]

CITIES = {
    "us": ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix",
           "Philadelphia", "San Antonio", "San Diego", "Dallas", "San Jose"],
    "uk": ["London", "Birmingham", "Manchester", "Leeds", "Glasgow",
           "Liverpool", "Newcastle", "Sheffield", "Bristol", "Edinburgh"],
    "india": ["Mumbai", "Delhi", "Bangalore", "Hyderabad", "Chennai",
              "Kolkata", "Pune", "Ahmedabad", "Jaipur", "Lucknow"],
}

STATES = {
    "us": ["NY", "CA", "IL", "TX", "AZ", "PA", "TX", "CA", "TX", "CA"],
    "uk": ["England", "England", "England", "England", "Scotland",
           "England", "England", "England", "England", "Scotland"],
    "india": ["MH", "DL", "KA", "TS", "TN", "WB", "MH", "GJ", "RJ", "UP"],
}

COUNTRIES = {
    "us": "USA",
    "uk": "United Kingdom",
    "india": "India",
}

COMPANY_PREFIXES = ["Dr.", "Mr.", "Ms.", "Mrs."]
COMPANY_SUFFIXES = ["LLC", "Inc", "Corp", "Ltd", "Group", "Solutions", "Technologies"]


def random_choice(lst: list[str]) -> str:
    """Get a random element from a list."""
    return random.choice(lst)


def generate_name(locale: str) -> str:
    """Generate a random name."""
    first = random_choice(FIRST_NAMES.get(locale, FIRST_NAMES["us"]))
    last = random_choice(LAST_NAMES.get(locale, LAST_NAMES["us"]))
    return f"{first} {last}"


def generate_email(name: str) -> str:
    """Generate an email address from a name."""
    # Clean the name
    clean_name = name.lower().replace(" ", ".")

    # Choose email domain
    domains = ["gmail.com", "yahoo.com", "outlook.com", "hotmail.com", "company.com"]
    domain = random_choice(domains)

    # Add random number sometimes
    if random.random() > 0.7:
        return f"{clean_name}{random.randint(1, 999)}@{domain}"
    return f"{clean_name}@{domain}"


def generate_phone(locale: str) -> str:
    """Generate a phone number."""
    if locale == "us":
        area = random.randint(200, 999)
        prefix = random.randint(200, 999)
        line = random.randint(1000, 9999)
        return f"+1-{area}-{prefix}-{line}"
    elif locale == "uk":
        return f"+44-{random.randint(10, 99)}-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}"
    elif locale == "india":
        return f"+91-{random.randint(6000000000, 9999999999)}"
    return f"+1-{random.randint(200, 999)}-{random.randint(200, 999)}-{random.randint(1000, 9999)}"


def generate_address(locale: str) -> dict[str, str]:
    """Generate a random address."""
    street_num = random.randint(1, 9999)
    street = random_choice(STREET_NAMES)
    city = random_choice(CITIES.get(locale, CITIES["us"]))
    state = random_choice(STATES.get(locale, STATES["us"]))
    country = COUNTRIES.get(locale, "USA")
    zip_code = f"{random.randint(10000, 99999)}"

    return {
        "street": f"{street_num} {street}",
        "city": city,
        "state": state,
        "zip": zip_code,
        "country": country,
    }


def generate_company() -> str:
    """Generate a random company name."""
    base = random_choice(COMPANIES)
    suffix = random_choice(COMPANY_SUFFIXES)

    if random.random() > 0.5:
        return f"{base} {suffix}"
    return base


def generate_date() -> str:
    """Generate a random date in ISO format."""
    year = random.randint(2020, 2026)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    return f"{year}-{month:02d}-{day:02d}"


def generate_age() -> int:
    """Generate a random age."""
    return random.randint(18, 80)


def generate_salary() -> int:
    """Generate a random salary."""
    return random.randint(30000, 200000)


def generate_record(fields: list[str], locale: str) -> dict[str, Any]:
    """
    Generate a single record with specified fields.

    Args:
        fields: List of field names to generate
        locale: Locale for data generation

    Returns:
        Dictionary with generated data
    """
    record: dict[str, Any] = {}

    for field in fields:
        field_lower = field.lower()

        if field_lower == "name":
            record["name"] = generate_name(locale)
        elif field_lower == "email":
            # Use name if already generated, otherwise generate
            name = record.get("name", generate_name(locale))
            record["email"] = generate_email(name)
        elif field_lower == "phone":
            record["phone"] = generate_phone(locale)
        elif field_lower == "address":
            record["address"] = generate_address(locale)
        elif field_lower == "company":
            record["company"] = generate_company()
        elif field_lower == "date":
            record["date"] = generate_date()
        elif field_lower == "age":
            record["age"] = generate_age()
        elif field_lower == "salary":
            record["salary"] = generate_salary()
        elif field_lower == "id":
            record["id"] = f"ID-{random.randint(10000, 99999)}"
        elif field_lower == "username":
            name = record.get("name", generate_name(locale))
            record["username"] = name.lower().replace(" ", "_")
        elif field_lower == "country":
            record["country"] = COUNTRIES.get(locale, "USA")

    return record


def flatten_address(record: dict[str, Any]) -> dict[str, Any]:
    """Flatten address objects into separate fields."""
    result = {}
    for key, value in record.items():
        if isinstance(value, dict):
            for subkey, subvalue in value.items():
                result[f"{key}_{subkey}"] = subvalue
        else:
            result[key] = value
    return result


def write_csv(filepath: Path, records: list[dict[str, Any]]) -> None:
    """Write records to CSV file."""
    if not records:
        return

    # Flatten nested structures for CSV
    flat_records = []
    for record in records:
        flat_records.append(flatten_address(record))

    # Get all field names
    fieldnames = list(flat_records[0].keys())

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(flat_records)


def write_json(filepath: Path, records: list[dict[str, Any]], indent: int) -> None:
    """Write records to JSON file."""
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=indent, ensure_ascii=False, default=str)


def main() -> None:
    """Main entry point for data generator."""
    args = parse_args()

    # Set random seed for reproducibility
    if args.seed is not None:
        random.seed(args.seed)
        print(f"Using random seed: {args.seed}")

    print(f"Generating {args.count} records...")

    # Generate records
    records = []
    for _ in range(args.count):
        record = generate_record(args.fields, args.locale)
        records.append(record)

    print(f"  Fields: {', '.join(args.fields)}")
    print(f"  Locale: {args.locale}")

    # Determine output path
    output_path = Path(args.output) if args.output else None

    # Write output
    if args.format in ["csv", "both"]:
        csv_path = output_path.with_suffix(".csv") if output_path else None
        if csv_path:
            write_csv(csv_path, records)
            print(f"\nCSV written to '{csv_path}'")

    if args.format in ["json", "both"]:
        json_path = output_path.with_suffix(".json") if output_path else None
        if json_path:
            write_json(json_path, records, args.indent)
            print(f"JSON written to '{json_path}'")

    if not output_path:
        # Print to stdout in CSV format
        output = csv.StringIO()
        writer = csv.DictWriter(output, fieldnames=records[0].keys() if records else [])
        writer.writeheader()
        writer.writerows([flatten_address(r) for r in records])
        print("\n" + output.getvalue())

    print("\nDone!")


if __name__ == "__main__":
    main()
