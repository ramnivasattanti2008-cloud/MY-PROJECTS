#!/usr/bin/env python3
"""
Regex Extractor - Extract emails, phone numbers, URLs, IPs, and more from text.

This script uses regular expressions to extract common patterns from text files
or pasted input. Demonstrates practical regex usage with educational examples.

Educational Purpose:
- Shows regex pattern construction for common data types
- Demonstrates named capture groups
- Explains regex flags and their effects
- Teaches efficient pattern matching

Author: Educational Example
License: MIT
"""

import argparse
import re
import sys
from pathlib import Path
from typing import List, Dict, Callable
from urllib.parse import urlparse


class RegexExtractor:
    """
    Extract structured data from text using regular expressions.

    Provides patterns for common data types with customization options.
    """

    # Pattern definitions with explanations
    PATTERNS = {
        'email': {
            'pattern': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'description': 'Email addresses',
            'example': 'user@example.com',
        },
        'phone_us': {
            'pattern': r'(?:\+?1[-.\s]?)?\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}',
            'description': 'US phone numbers',
            'example': '(555) 123-4567, 555-123-4567, +1-555-123-4567',
        },
        'phone_international': {
            'pattern': r'\+?[0-9]{1,3}[-.\s]?\(?[0-9]{1,4}\)?[-.\s]?[0-9]{1,4}[-.\s]?[0-9]{1,9}',
            'description': 'International phone numbers',
            'example': '+91-9876543210',
        },
        'url': {
            'pattern': r'https?://(?:www\.)?[-a-zA-Z0-9@:%._+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_+.~#?&/=]*)',
            'description': 'HTTP/HTTPS URLs',
            'example': 'https://example.com/path?query=1',
        },
        'ipv4': {
            'pattern': r'\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b',
            'description': 'IPv4 addresses',
            'example': '192.168.1.1',
        },
        'ipv6': {
            'pattern': r'\b(?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}\b',
            'description': 'IPv6 addresses',
            'example': '2001:0db8:85a3:0000:0000:8a2e:0370:7334',
        },
        'date_iso': {
            'pattern': r'\b[0-9]{4}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12][0-9]|3[01])\b',
            'description': 'ISO date format (YYYY-MM-DD)',
            'example': '2024-01-15',
        },
        'date_us': {
            'pattern': r'\b(?:0[1-9]|1[0-2])/(?:0[1-9]|[12][0-9]|3[01])/[0-9]{4}\b',
            'description': 'US date format (MM/DD/YYYY)',
            'example': '01/15/2024',
        },
        'time_24h': {
            'pattern': r'\b(?:[01]?[0-9]|2[0-3]):[0-5][0-9](?::[0-5][0-9])?\b',
            'description': '24-hour time format',
            'example': '14:30 or 14:30:45',
        },
        'credit_card': {
            'pattern': r'\b(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|3[47][0-9]{13}|6(?:011|5[0-9]{2})[0-9]{12})\b',
            'description': 'Credit card numbers (Visa, MC, Amex, Discover)',
            'example': '4111111111111111',
        },
        'ssn': {
            'pattern': r'\b[0-9]{3}-[0-9]{2}-[0-9]{4}\b',
            'description': 'US Social Security Numbers',
            'example': '123-45-6789',
        },
        'zip_us': {
            'pattern': r'\b[0-9]{5}(?:-[0-9]{4})?\b',
            'description': 'US ZIP codes',
            'example': '12345 or 12345-6789',
        },
        'hex_color': {
            'pattern': r'#(?:[0-9a-fA-F]{3}){1,2}\b',
            'description': 'Hex color codes',
            'example': '#fff or #a1b2c3',
        },
        'mac_address': {
            'pattern': r'\b(?:[0-9a-fA-F]{2}[:-]){5}[0-9a-fA-F]{2}\b',
            'description': 'MAC addresses',
            'example': '00:1A:2B:3C:4D:5E',
        },
        'uuid': {
            'pattern': r'\b[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}\b',
            'description': 'UUID/GUID',
            'example': '550e8400-e29b-41d4-a716-446655440000',
        },
        'hashtag': {
            'pattern': r'#[a-zA-Z][a-zA-Z0-9_]*',
            'description': 'Hashtags',
            'example': '#Python, #regex2024',
        },
        'mention': {
            'pattern': r'@[a-zA-Z][a-zA-Z0-9_]*',
            'description': 'Social media mentions',
            'example': '@username',
        },
        'money_usd': {
            'pattern': r'\$\d{1,3}(?:,\d{3})*(?:\.\d{2})?',
            'description': 'US Dollar amounts',
            'example': '$1,234.56',
        },
        'percentage': {
            'pattern': r'\b\d+(?:\.\d+)?%',
            'description': 'Percentages',
            'example': '42%, 3.14%',
        },
        'words': {
            'pattern': r'\b[a-zA-Z]+\b',
            'description': 'Individual words',
            'example': 'Hello, World',
        },
        'numbers': {
            'pattern': r'\b-?\d+(?:\.\d+)?\b',
            'description': 'Numbers (integers and decimals)',
            'example': '42, -3.14, 99.9',
        },
    }

    def __init__(self, text: str = None, file_path: str = None):
        """
        Initialize extractor with text or file.

        Args:
            text: Text content to analyze
            file_path: Path to text file
        """
        self.text = text if text else self._read_file(file_path)

    def _read_file(self, file_path: str) -> str:
        """Read text from file."""
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")

        encodings = ['utf-8', 'latin-1', 'cp1252']
        for encoding in encodings:
            try:
                return path.read_text(encoding=encoding)
            except UnicodeDecodeError:
                continue

        raise ValueError(f"Could not read file with any supported encoding")

    def extract(self, pattern_type: str, case_insensitive: bool = False) -> List[str]:
        """
        Extract all matches for a pattern type.

        Args:
            pattern_type: Name of pattern from PATTERNS dict
            case_insensitive: Whether to ignore case

        Returns:
            List of unique matches
        """
        if pattern_type not in self.PATTERNS:
            raise ValueError(f"Unknown pattern: {pattern_type}")

        pattern = self.PATTERNS[pattern_type]['pattern']

        flags = re.IGNORECASE if case_insensitive else 0
        matches = re.findall(pattern, self.text, flags)

        # Return unique matches, preserving order
        seen = set()
        unique = []
        for match in matches:
            if match not in seen:
                seen.add(match)
                unique.append(match)

        return unique

    def extract_custom(self, pattern: str, flags: int = 0,
                       group: int = 0) -> List[str]:
        """
        Extract using a custom regex pattern.

        Args:
            pattern: Regex pattern string
            flags: Regex flags (re.IGNORECASE, etc.)
            group: Capture group number to extract

        Returns:
            List of unique matches
        """
        try:
            compiled = re.compile(pattern, flags)
        except re.error as e:
            raise ValueError(f"Invalid regex: {e}")

        matches = compiled.findall(self.text)

        # Extract specified group if needed
        if group > 0:
            matches = [m[group - 1] if len(m) >= group else m for m in matches]

        # Return unique matches
        seen = set()
        unique = []
        for match in matches:
            if match not in seen:
                seen.add(match)
                unique.append(match)

        return unique

    def extract_all(self, include_stats: bool = True) -> Dict[str, List[str]]:
        """
        Extract all pattern types.

        Args:
            include_stats: Include count statistics

        Returns:
            Dictionary mapping pattern types to matches
        """
        results = {}
        for pattern_type in self.PATTERNS:
            matches = self.extract(pattern_type)
            if matches:
                if include_stats:
                    results[pattern_type] = matches
                else:
                    results[pattern_type] = matches

        return results

    def validate_pattern(self, pattern_type: str) -> bool:
        """
        Check if pattern matches anything in the text.

        Args:
            pattern_type: Name of pattern to test

        Returns:
            True if pattern found
        """
        matches = self.extract(pattern_type)
        return len(matches) > 0

    def count_patterns(self) -> Dict[str, int]:
        """Count occurrences of each pattern type."""
        counts = {}
        for pattern_type in self.PATTERNS:
            counts[pattern_type] = len(self.extract(pattern_type))
        return counts

    def extract_domains(self) -> List[str]:
        """Extract unique domain names from URLs."""
        urls = self.extract('url')
        domains = set()

        for url in urls:
            try:
                parsed = urlparse(url)
                domain = parsed.netloc
                # Remove www. prefix
                if domain.startswith('www.'):
                    domain = domain[4:]
                if domain:
                    domains.add(domain)
            except Exception:
                continue

        return sorted(domains)

    def validate_emails(self, emails: List[str] = None) -> Dict[str, bool]:
        """
        Basic email validation.

        Args:
            emails: List of emails to validate (uses extracted if None)

        Returns:
            Dictionary mapping email to validity
        """
        if emails is None:
            emails = self.extract('email')

        pattern = re.compile(
            r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'
        )

        return {email: bool(pattern.match(email)) for email in emails}

    def sanitize(self, keep_types: List[str] = None,
                 replace_with: str = '[REDACTED]') -> str:
        """
        Replace sensitive patterns with redaction placeholder.

        Args:
            keep_types: Pattern types to keep (None = redact all sensitive)
            replace_with: What to replace sensitive data with

        Returns:
            Sanitized text
        """
        sensitive_types = ['email', 'phone_us', 'ssn', 'credit_card', 'phone_international']
        types_to_redact = [t for t in sensitive_types if keep_types is None or t not in keep_types]

        result = self.text
        for pattern_type in types_to_redact:
            if pattern_type in self.PATTERNS:
                pattern = self.PATTERNS[pattern_type]['pattern']
                result = re.sub(pattern, replace_with, result)

        return result


def print_results(pattern_type: str, matches: List[str], description: str = None):
    """Print extraction results in a formatted way."""
    pattern_info = RegexExtractor.PATTERNS.get(pattern_type, {})
    desc = description or pattern_info.get('description', '')

    print(f"\n{'=' * 60}")
    print(f"Pattern: {pattern_type}")
    if desc:
        print(f"Description: {desc}")
    print(f"Matches found: {len(matches)}")
    print("=" * 60)

    if matches:
        for i, match in enumerate(matches, 1):
            print(f"  {i:3}. {match}")
    else:
        print("  No matches found.")


def main():
    """Main entry point with CLI argument parsing."""
    parser = argparse.ArgumentParser(
        description='Extract emails, phones, URLs, IPs and more from text.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Available patterns:
  email, phone_us, phone_international, url, ipv4, ipv6,
  date_iso, date_us, time_24h, credit_card, ssn, zip_us,
  hex_color, mac_address, uuid, hashtag, mention, money_usd,
  percentage, words, numbers

Examples:
  Extract emails from file:
    python regex-extractor.py data.txt --emails

  Extract multiple types:
    python regex-extractor.py data.txt --emails --urls --phones

  Use custom pattern:
    python regex-extractor.py data.txt --pattern "\\d{4}-\\d{4}"

  Interactive mode (extract all):
    python regex-extractor.py data.txt --all

  Redact sensitive data:
    python regex-extractor.py data.txt --sanitize
        """
    )

    parser.add_argument('input', help='Text or file path')
    parser.add_argument('-e', '--emails', action='store_true', help='Extract emails')
    parser.add_argument('-p', '--phones', action='store_true', help='Extract phone numbers')
    parser.add_argument('-u', '--urls', action='store_true', help='Extract URLs')
    parser.add_argument('-i', '--ips', action='store_true', help='Extract IP addresses')
    parser.add_argument('-a', '--all', action='store_true', help='Extract all patterns')
    parser.add_argument('--pattern', help='Custom regex pattern')
    parser.add_argument('--sanitize', action='store_true', help='Redact sensitive data')
    parser.add_argument('--list', action='store_true', help='List all available patterns')
    parser.add_argument('--stats', action='store_true', help='Show statistics')
    parser.add_argument('--domains', action='store_true', help='Extract unique domains from URLs')
    parser.add_argument('-o', '--output', help='Output file for results')

    args = parser.parse_args()

    # Handle input
    if Path(args.input).exists():
        extractor = RegexExtractor(file_path=args.input)
        input_desc = f"File: {args.input}"
    else:
        extractor = RegexExtractor(text=args.input)
        input_desc = "Input text"

    # List patterns
    if args.list:
        print("\nAvailable Patterns:")
        print("=" * 60)
        for name, info in RegexExtractor.PATTERNS.items():
            print(f"  {name:25} - {info['description']}")
            print(f"                               Example: {info['example']}")
        return

    results = {}

    # Extract requested patterns
    if args.all:
        results = extractor.extract_all()
    else:
        if args.emails:
            results['email'] = extractor.extract('email')
        if args.phones:
            results['phone_us'] = extractor.extract('phone_us')
            results['phone_international'] = extractor.extract('phone_international')
        if args.urls:
            results['url'] = extractor.extract('url')
        if args.ips:
            results['ipv4'] = extractor.extract('ipv4')
            results['ipv6'] = extractor.extract('ipv6')
        if args.pattern:
            results['custom'] = extractor.extract_custom(args.pattern)

    # Print results
    if args.stats:
        print(f"\nExtraction Statistics ({input_desc})")
        print("=" * 60)
        counts = extractor.count_patterns()
        for pattern_type, count in sorted(counts.items(), key=lambda x: -x[1]):
            if count > 0:
                print(f"  {pattern_type:25}: {count:4} matches")

    elif args.sanitize:
        sanitized = extractor.sanitize()
        print(f"\nSanitized Text ({input_desc}):")
        print("=" * 60)
        print(sanitized)

    elif args.domains:
        domains = extractor.extract_domains()
        print(f"\nUnique Domains ({input_desc}):")
        print("=" * 60)
        for domain in domains:
            print(f"  - {domain}")
        print(f"\nTotal unique domains: {len(domains)}")

    elif results:
        for pattern_type, matches in results.items():
            print_results(pattern_type, matches)

        # Save to file if requested
        if args.output:
            output = []
            for pattern_type, matches in results.items():
                output.append(f"# {pattern_type}")
                output.extend(matches)
                output.append("")

            Path(args.output).write_text('\n'.join(output), encoding='utf-8')
            print(f"\nResults saved to: {args.output}")

    else:
        # No specific extraction requested
        counts = extractor.count_patterns()
        found = {k: v for k, v in counts.items() if v > 0}

        if found:
            print(f"\nFound patterns ({input_desc}):")
            print("=" * 60)
            for pattern_type, count in sorted(found.items(), key=lambda x: -x[1]):
                info = RegexExtractor.PATTERNS[pattern_type]
                print(f"  {pattern_type:25}: {count:4} ({info['description']})")

            print("\nUse --all to extract, or specify pattern types with --emails, --urls, etc.")
        else:
            print(f"\nNo patterns found in {input_desc}")


if __name__ == '__main__':
    main()
