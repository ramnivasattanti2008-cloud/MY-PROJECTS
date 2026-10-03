#!/usr/bin/env python3
"""
Currency CMD - A currency converter CLI tool
Features: Convert between currencies, list rates, historical rates
Uses exchangerate-api.com (free tier available)
"""

import argparse
import os
import sys
import json
from datetime import datetime, timedelta

# Try to import colorama
try:
    from colorama import init, Fore, Style
    init(autoreset=True)
except ImportError:
    class Fore:
        RED = GREEN = YELLOW = CYAN = MAGENTA = WHITE = RESET = BLUE = ''
    class Style:
        BRIGHT = RESET_ALL = DIM = ''

# Import urllib for Python 3
try:
    import urllib.request
    import urllib.parse
    import urllib.error
except ImportError:
    print(f"{Fore.RED}Error: urllib not available{Style.RESET_ALL}")
    sys.exit(1)

# API Configuration
# Using exchangerate-api.com free tier
EXCHANGE_API_URL = "https://open.er-api.com/v6/latest"

# Popular currencies with descriptions
CURRENCIES = {
    "USD": {"name": "US Dollar", "symbol": "$", "color": Fore.GREEN},
    "EUR": {"name": "Euro", "symbol": "€", "color": Fore.BLUE},
    "GBP": {"name": "British Pound", "symbol": "£", "color": Fore.CYAN},
    "JPY": {"name": "Japanese Yen", "symbol": "¥", "color": Fore.RED},
    "INR": {"name": "Indian Rupee", "symbol": "₹", "color": Fore.MAGENTA},
    "AUD": {"name": "Australian Dollar", "symbol": "A$", "color": Fore.YELLOW},
    "CAD": {"name": "Canadian Dollar", "symbol": "C$", "color": Fore.RED},
    "CHF": {"name": "Swiss Franc", "symbol": "CHF", "color": Fore.RED},
    "CNY": {"name": "Chinese Yuan", "symbol": "¥", "color": Fore.YELLOW},
    "NZD": {"name": "New Zealand Dollar", "symbol": "NZ$", "color": Fore.CYAN},
    "SGD": {"name": "Singapore Dollar", "symbol": "S$", "color": Fore.RED},
    "HKD": {"name": "Hong Kong Dollar", "symbol": "HK$", "color": Fore.RED},
    "KRW": {"name": "South Korean Won", "symbol": "₩", "color": Fore.BLUE},
    "MXN": {"name": "Mexican Peso", "symbol": "$", "color": Fore.GREEN},
    "BRL": {"name": "Brazilian Real", "symbol": "R$", "color": Fore.GREEN},
    "RUB": {"name": "Russian Ruble", "symbol": "₽", "color": Fore.BLUE},
    "ZAR": {"name": "South African Rand", "symbol": "R", "color": Fore.GREEN},
    "AED": {"name": "UAE Dirham", "symbol": "د.إ", "color": Fore.GREEN},
    "THB": {"name": "Thai Baht", "symbol": "฿", "color": Fore.YELLOW},
    "TRY": {"name": "Turkish Lira", "symbol": "₺", "color": Fore.RED},
}


def fetch_exchange_rates(base_currency: str = "USD") -> dict:
    """Fetch exchange rates from API."""
    url = f"{EXCHANGE_API_URL}/{base_currency}"

    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))

            if data.get("result") != "success":
                return {"error": "Failed to fetch rates"}

            return {
                "base": data.get("base_code", base_currency),
                "rates": data.get("rates", {}),
                "time_last_update": data.get("time_last_update_utc", "")
            }
    except urllib.error.URLError as e:
        return {"error": f"Network error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}


def convert_currency(amount: float, from_currency: str, to_currency: str) -> float:
    """Convert amount from one currency to another."""
    rates_data = fetch_exchange_rates(from_currency.upper())

    if "error" in rates_data:
        return None

    rate = rates_data["rates"].get(to_currency.upper())
    if rate is None:
        return None

    return amount * rate


def display_conversion(amount: float, from_curr: str, to_curr: str,
                       result: float, rates_data: dict) -> None:
    """Display formatted conversion result."""
    from_info = CURRENCIES.get(from_curr.upper(), {"name": from_curr, "symbol": "", "color": Fore.WHITE})
    to_info = CURRENCIES.get(to_curr.upper(), {"name": to_curr, "symbol": "", "color": Fore.WHITE})

    # Calculate exchange rate
    rate = result / amount if amount else 0

    print(f"\n{Fore.CYAN}{'═'*60}{Style.RESET_ALL}")
    print(f"{Fore.WHITE}{Style.BRIGHT}  Currency Conversion{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'═'*60}{Style.RESET_ALL}\n")

    # From section
    print(f"{Fore.DIM}  From:{Style.RESET_ALL}")
    print(f"  {from_info['color']}{from_info['symbol']}{amount:,.2f}{Style.RESET_ALL}")
    print(f"  {Fore.WHITE}{from_curr} - {from_info['name']}{Style.RESET_ALL}")

    # Arrow
    print(f"\n  {Fore.YELLOW}        ↓{Style.RESET_ALL}")
    print(f"  {Fore.YELLOW}        ↓{Style.RESET_ALL}")
    print(f"  {Fore.YELLOW}        ↓{Style.RESET_ALL}\n")

    # To section
    print(f"{Fore.DIM}  To:{Style.RESET_ALL}")
    print(f"  {to_info['color']}{Style.BRIGHT}{to_info['symbol']}{result:,.2f}{Style.RESET_ALL}")
    print(f"  {Fore.WHITE}{to_curr} - {to_info['name']}{Style.RESET_ALL}")

    # Exchange rate
    print(f"\n{Fore.CYAN}{'─'*60}{Style.RESET_ALL}")
    print(f"  {Fore.WHITE}1 {from_curr} = {rate:,.4f} {to_curr}{Style.RESET_ALL}")

    # Timestamp
    if rates_data.get("time_last_update"):
        print(f"  {Fore.DIM}Rates updated: {rates_data['time_last_update'][:16]}{Style.RESET_ALL}")

    print()


def display_all_rates(base_currency: str) -> None:
    """Display all exchange rates for a currency."""
    rates_data = fetch_exchange_rates(base_currency)

    if "error" in rates_data:
        print(f"{Fore.RED}Error: {rates_data['error']}{Style.RESET_ALL}")
        return

    base_info = CURRENCIES.get(base_currency.upper(),
                              {"name": base_currency, "symbol": "", "color": Fore.WHITE})

    print(f"\n{Fore.CYAN}{'═'*60}{Style.RESET_ALL}")
    print(f"{Fore.WHITE}{Style.BRIGHT}  Exchange Rates for {base_currency}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'═'*60}{Style.RESET_ALL}\n")

    print(f"{Fore.DIM}  Base: {base_info['color']}{base_info['symbol']}{Style.RESET_ALL}")
    print(f"{Fore.DIM}  1 {base_currency} = ?{Style.RESET_ALL}\n")

    # Sort rates by value
    rates = rates_data["rates"]
    sorted_rates = sorted(rates.items(), key=lambda x: x[1])

    # Display in columns
    for i, (currency, rate) in enumerate(sorted_rates):
        curr_info = CURRENCIES.get(currency.upper(),
                                   {"name": currency, "symbol": "", "color": Fore.WHITE})

        print(f"  {curr_info['color']}{currency:4}{Style.RESET_ALL} "
              f"{Fore.WHITE}{rate:>12.4f}{Style.RESET_ALL} "
              f"{Fore.DIM}{curr_info['name'][:25]}{Style.RESET_ALL}")

        if (i + 1) % 3 == 0:
            print()


def display_popular_rates() -> None:
    """Display popular currency pairs."""
    # Get USD base rates
    rates_data = fetch_exchange_rates("USD")

    if "error" in rates_data:
        print(f"{Fore.RED}Error: {rates_data['error']}{Style.RESET_ALL}")
        return

    print(f"\n{Fore.CYAN}{'═'*60}{Style.RESET_ALL}")
    print(f"{Fore.WHITE}{Style.BRIGHT}  Popular Exchange Rates (Base: USD){Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'═'*60}{Style.RESET_ALL}\n")

    popular = ["EUR", "GBP", "JPY", "INR", "AUD", "CAD", "CHF", "CNY"]
    rates = rates_data["rates"]

    # Header
    print(f"{Fore.DIM}  {'Currency':<12} {'Rate':<12} {'Name':<25}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}  {'─'*50}{Style.RESET_ALL}\n")

    for curr in popular:
        rate = rates.get(curr)
        if rate:
            info = CURRENCIES.get(curr, {"name": curr, "symbol": "", "color": Fore.WHITE})
            print(f"  {info['color']}{curr:<12}{Style.RESET_ALL} "
                  f"{Fore.WHITE}{rate:<12.4f}{Style.RESET_ALL} "
                  f"{Fore.DIM}{info['name']:<25}{Style.RESET_ALL}")

    print()


def compare_currencies(from_currency: str, to_currencies: list) -> None:
    """Compare one currency against multiple others."""
    rates_data = fetch_exchange_rates(from_currency)

    if "error" in rates_data:
        print(f"{Fore.RED}Error: {rates_data['error']}{Style.RESET_ALL}")
        return

    from_info = CURRENCIES.get(from_currency.upper(),
                              {"name": from_currency, "symbol": "", "color": Fore.WHITE})

    print(f"\n{Fore.CYAN}{'═'*60}{Style.RESET_ALL}")
    print(f"{Fore.WHITE}{Style.BRIGHT}  Comparing {from_currency} to multiple currencies{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'═'*60}{Style.RESET_ALL}\n")

    rates = rates_data["rates"]

    for to_curr in to_currencies:
        rate = rates.get(to_curr.upper())
        if rate:
            to_info = CURRENCIES.get(to_curr.upper(),
                                    {"name": to_curr, "symbol": "", "color": Fore.WHITE})

            print(f"  {from_info['color']}{from_currency}{Style.RESET_ALL} "
                  f"{Fore.WHITE}→{Style.RESET_ALL} "
                  f"{to_info['color']}{to_curr}{Style.RESET_ALL}: "
                  f"{Fore.GREEN}{rate:,.4f}{Style.RESET_ALL}")
        else:
            print(f"  {Fore.RED}Unknown currency: {to_curr}{Style.RESET_ALL}")

    print()


def list_currencies() -> None:
    """List all supported currencies."""
    print(f"\n{Fore.CYAN}{'═'*60}{Style.RESET_ALL}")
    print(f"{Fore.WHITE}{Style.BRIGHT}  Supported Currencies{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'═'*60}{Style.RESET_ALL}\n")

    for code, info in sorted(CURRENCIES.items()):
        print(f"  {info['color']}{code:<6}{Style.RESET_ALL} "
              f"{Fore.WHITE}{info['symbol']:<4}{Style.RESET_ALL} "
              f"{Fore.DIM}{info['name']}{Style.RESET_ALL}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Currency CMD - Currency converter CLI tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  currency-cmd convert 100 USD EUR
  currency-cmd convert 50 EUR INR
  currency-cmd rates USD
  currency-cmd popular
  currency-cmd compare USD EUR GBP JPY INR
  currency-cmd list

Note: Exchange rates are fetched from open.er-api.com
        """
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Convert command
    convert_parser = subparsers.add_parser("convert", help="Convert currency")
    convert_parser.add_argument("amount", type=float, help="Amount to convert")
    convert_parser.add_argument("from_currency", help="Source currency code")
    convert_parser.add_argument("to_currency", help="Target currency code")

    # Rates command
    rates_parser = subparsers.add_parser("rates", help="Show exchange rates")
    rates_parser.add_argument("base", nargs="?", default="USD", help="Base currency")

    # Popular command
    popular_parser = subparsers.add_parser("popular", help="Show popular rates")

    # Compare command
    compare_parser = subparsers.add_parser("compare", help="Compare currencies")
    compare_parser.add_argument("from_currency", help="Source currency")
    compare_parser.add_argument("to_currencies", nargs="+", help="Target currencies")

    # List command
    list_parser = subparsers.add_parser("list", help="List all currencies")

    args = parser.parse_args()

    if args.command == "convert":
        # Show loading indicator
        print(f"{Fore.DIM}Fetching exchange rates...{Style.RESET_ALL}")

        result = convert_currency(args.amount, args.from_currency, args.to_currency)
        rates_data = fetch_exchange_rates(args.from_currency)

        if result is None:
            print(f"{Fore.RED}Error: Could not convert {args.from_currency} to {args.to_currency}{Style.RESET_ALL}")
            sys.exit(1)

        display_conversion(args.amount, args.from_currency, args.to_currency,
                         result, rates_data)

    elif args.command == "rates":
        display_all_rates(args.base)

    elif args.command == "popular":
        display_popular_rates()

    elif args.command == "compare":
        compare_currencies(args.from_currency, args.to_currencies)

    elif args.command == "list":
        list_currencies()

    else:
        # Default: show popular rates
        display_popular_rates()
        print(f"{Fore.DIM}Run 'currency-cmd --help' for more commands.{Style.RESET_ALL}")


if __name__ == "__main__":
    main()
