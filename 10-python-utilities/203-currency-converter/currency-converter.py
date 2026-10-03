#!/usr/bin/env python3
"""
Currency Converter - Convert between currencies using free exchange rate API.

Usage:
    Single conversion: python currency-converter.py 100 USD to INR
    List currencies: python currency-converter.py --list
    Exchange rates:   python currency-converter.py --rates USD

No API key required - uses the free exchangerate.host API.
"""

import argparse
import json
import sys
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

import requests


# Common currency codes and their names
CURRENCIES = {
    "USD": "United States Dollar",
    "EUR": "Euro",
    "GBP": "British Pound Sterling",
    "INR": "Indian Rupee",
    "JPY": "Japanese Yen",
    "AUD": "Australian Dollar",
    "CAD": "Canadian Dollar",
    "CHF": "Swiss Franc",
    "CNY": "Chinese Yuan",
    "RUB": "Russian Ruble",
    "BRL": "Brazilian Real",
    "MXN": "Mexican Peso",
    "SGD": "Singapore Dollar",
    "HKD": "Hong Kong Dollar",
    "KRW": "South Korean Won",
    "AED": "United Arab Emirates Dirham",
    "SAR": "Saudi Riyal",
    "NZD": "New Zealand Dollar",
    "ZAR": "South African Rand",
    "THB": "Thai Baht",
}


@dataclass
class ConversionResult:
    """Stores the result of a currency conversion."""
    from_currency: str
    to_currency: str
    from_amount: float
    to_amount: float
    rate: float
    timestamp: datetime


def get_exchange_rates(base: str = "USD") -> Optional[dict]:
    """
    Fetch latest exchange rates from the API.

    Args:
        base: Base currency code (default: USD)

    Returns:
        Dictionary of exchange rates or None if request fails
    """
    url = "https://api.exchangerate.host/latest"
    params = {"base": base}

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if data.get("success", True):  # API returns success field
            return data.get("rates", {})
        return None
    except requests.exceptions.RequestException:
        # Fallback to alternative API
        return get_exchange_rates_fallback(base)


def get_exchange_rates_fallback(base: str = "USD") -> Optional[dict]:
    """Fallback API using frankfurter.app."""
    url = f"https://api.frankfurter.app/latest"
    params = {"from": base}

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get("rates", {})
    except requests.exceptions.RequestException as e:
        print(f"Error fetching exchange rates: {e}", file=sys.stderr)
        return None


def get_all_rates() -> Optional[dict]:
    """Get all available exchange rates in USD."""
    url = "https://api.exchangerate.host/latest"
    params = {"base": "USD"}

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get("rates", {})
    except requests.exceptions.RequestException:
        return get_all_rates_fallback()


def get_all_rates_fallback() -> Optional[dict]:
    """Fallback: Get rates from frankfurter.app."""
    url = "https://api.frankfurter.app/latest"
    params = {"from": "USD"}

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        rates = data.get("rates", {})
        rates["USD"] = 1.0  # Add base currency
        return rates
    except requests.exceptions.RequestException as e:
        print(f"Error fetching exchange rates: {e}", file=sys.stderr)
        return None


def convert_currency(amount: float, from_curr: str, to_curr: str) -> Optional[ConversionResult]:
    """
    Convert an amount from one currency to another.

    Args:
        amount: Amount to convert
        from_curr: Source currency code
        to_curr: Target currency code

    Returns:
        ConversionResult with conversion details or None if fails
    """
    from_curr = from_curr.upper()
    to_curr = to_curr.upper()

    # Same currency
    if from_curr == to_curr:
        return ConversionResult(
            from_currency=from_curr,
            to_currency=to_curr,
            from_amount=amount,
            to_amount=amount,
            rate=1.0,
            timestamp=datetime.now(),
        )

    # Get exchange rates
    rates = get_exchange_rates(base=from_curr)
    if not rates:
        return None

    # Check if target currency exists
    if to_curr not in rates:
        print(f"Error: Currency '{to_curr}' not found", file=sys.stderr)
        return None

    rate = rates[to_curr]
    converted_amount = amount * rate

    return ConversionResult(
        from_currency=from_curr,
        to_currency=to_curr,
        from_amount=amount,
        to_amount=converted_amount,
        rate=rate,
        timestamp=datetime.now(),
    )


def format_currency(amount: float, code: str) -> str:
    """Format amount with appropriate decimal places."""
    # Most currencies use 2 decimal places
    if code in ["JPY", "KRW"]:
        return f"{amount:,.0f} {code}"
    elif code == "INR":
        return f"{amount:,.2f} {code}"
    else:
        return f"{amount:,.2f} {code}"


def format_result(result: ConversionResult, show_rate: bool = True) -> str:
    """Format conversion result for display."""
    lines = [
        "",
        f"  Currency Conversion",
        f"  {'─' * 40}",
        f"  {format_currency(result.from_amount, result.from_currency)}",
        f"  equals",
        f"  {format_currency(result.to_amount, result.to_currency)}",
        "",
    ]

    if show_rate:
        lines.insert(4, f"  (Rate: 1 {result.from_currency} = {result.rate:.4f} {result.to_currency})")

    lines.append(f"  As of: {result.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("")

    return "\n".join(lines)


def list_currencies() -> None:
    """Display list of supported currencies."""
    print("\n  Supported Currencies")
    print(f"  {'─' * 50}")
    print(f"  {'Code':<8} {'Currency Name'}")
    print(f"  {'─' * 50}")

    for code in sorted(CURRENCIES.keys()):
        print(f"  {code:<8} {CURRENCIES[code]}")

    print(f"  {'─' * 50}")
    print(f"  Total: {len(CURRENCIES)} currencies")
    print("")


def show_exchange_rates(base: str) -> None:
    """Show exchange rates for a base currency."""
    base = base.upper()

    if base not in CURRENCIES:
        print(f"Warning: Unknown currency code '{base}'", file=sys.stderr)

    print(f"\n  Exchange Rates (Base: {base})")
    print(f"  {'─' * 50}")
    print(f"  {'Currency':<8} {'Name':<30} {'Rate'}")
    print(f"  {'─' * 50}")

    rates = get_exchange_rates(base=base)
    if rates:
        for code in sorted(rates.keys()):
            name = CURRENCIES.get(code, "Unknown")
            rate = rates[code]
            print(f"  {code:<8} {name:<30} {rate:.4f}")
    else:
        print("  Error: Could not fetch exchange rates")

    print(f"  {'─' * 50}")
    print("")


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Convert between currencies using free exchange rates",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "amount",
        nargs="?",
        type=float,
        help="Amount to convert (optional if using --list or --rates)",
    )
    parser.add_argument(
        "from_currency",
        nargs="?",
        help="Source currency code (e.g., USD, EUR)",
    )
    parser.add_argument(
        "to_currency",
        nargs="?",
        help="Target currency code (e.g., INR, GBP)",
    )
    parser.add_argument(
        "--list", "-l",
        action="store_true",
        help="List all supported currencies",
    )
    parser.add_argument(
        "--rates", "-r",
        metavar="BASE",
        help="Show exchange rates for a base currency",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output result as JSON",
    )
    parser.add_argument(
        "--no-rate",
        action="store_true",
        help="Hide exchange rate in output",
    )

    args = parser.parse_args()

    # List currencies
    if args.list:
        list_currencies()
        return 0

    # Show exchange rates
    if args.rates:
        show_exchange_rates(args.rates)
        return 0

    # Conversion mode
    if not all([args.amount is not None, args.from_currency, args.to_currency]):
        parser.print_help()
        print("\n  Example: python currency-converter.py 100 USD to INR")
        return 1

    # Parse "100 USD to INR" syntax
    from_curr = args.from_currency.upper()
    to_curr = args.to_currency.upper()

    # Handle "to" keyword in from_currency
    if "TO" in from_curr:
        parts = args.from_currency.upper().split("TO")
        if len(parts) == 2:
            from_curr = parts[0].strip()
            to_curr = parts[1].strip()

    print(f"Converting {args.amount} {from_curr} to {to_curr}...")

    # Perform conversion
    result = convert_currency(args.amount, from_curr, to_curr)

    if not result:
        print("Error: Conversion failed", file=sys.stderr)
        return 1

    # Output result
    if args.json:
        output = {
            "from": {
                "currency": result.from_currency,
                "amount": result.from_amount,
            },
            "to": {
                "currency": result.to_currency,
                "amount": result.to_amount,
            },
            "rate": result.rate,
            "timestamp": result.timestamp.isoformat(),
        }
        print(json.dumps(output, indent=2))
    else:
        print(format_result(result, show_rate=not args.no_rate))

    return 0


if __name__ == "__main__":
    sys.exit(main())
