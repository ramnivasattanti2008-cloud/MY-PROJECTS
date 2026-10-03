#!/usr/bin/env python3
"""
Leak Checker - Educational Data Breach Checker

This tool checks if an email has appeared in known data breaches
using the HaveIBeenPwned API (free tier, no authentication required).

EDUCATIONAL PURPOSE ONLY - Learn about data breach exposure.
Author: Educational Security Project
"""

import sys
import argparse
import hashlib
import urllib.request
import urllib.parse
import urllib.error
import json
import time
from typing import Optional, List, Dict, Any

# ==============================================================================
# Configuration
# ==============================================================================

API_BASE_URL = "https://haveibeenpwned.com/api/v3"

# User agent required by HIBP API
USER_AGENT = "Educational Breach Checker Python Script"

# Rate limiting (HIBP free tier: polite requests)
REQUEST_DELAY = 1.6  # seconds between requests


# ==============================================================================
# API Functions
# ==============================================================================

def check_breaches(email: str, include_unverified: bool = True) -> Optional[List[Dict[str, Any]]]:
    """
    Check if an email has been in any data breaches.

    Uses the HaveIBeenPwned API free tier.

    Args:
        email: Email address to check
        include_unverified: Include breaches that haven't been verified

    Returns:
        List of breach dictionaries if found, None on error

    API Details:
        - Free tier: No API key required
        - Rate limit: 1 request per 1.6 seconds
        - Endpoint: GET /breachedaccount/{email}
    """
    # Encode email for URL
    encoded_email = urllib.parse.quote(email)

    # Build URL with query parameters
    url = f"{API_BASE_URL}/breachedaccount/{encoded_email}"

    params = {
        "truncateResponse": "false"
    }

    if include_unverified:
        params["includeUnverified"] = "true"

    url += "?" + urllib.parse.urlencode(params)

    try:
        # Create request with proper headers
        request = urllib.request.Request(
            url,
            headers={
                "User-Agent": USER_AGENT,
                "Accept": "application/json"
            }
        )

        # Make request
        with urllib.request.urlopen(request, timeout=10) as response:
            if response.status == 200:
                data = json.loads(response.read().decode('utf-8'))
                return data
            else:
                return []

    except urllib.error.HTTPError as e:
        if e.code == 404:
            # No breaches found - this is good!
            return []
        elif e.code == 429:
            print("[!] Rate limited. Please wait before making more requests.")
            return None
        elif e.code == 401:
            print("[!] API requires authentication (401).")
            return None
        else:
            print(f"[!] HTTP Error: {e.code} - {e.reason}")
            return None

    except urllib.error.URLError as e:
        print(f"[!] Network error: {e.reason}")
        return None

    except Exception as e:
        print(f"[!] Error checking breaches: {e}")
        return None


def get_paste_account(email: str) -> Optional[List[Dict[str, Any]]]:
    """
    Check if an email appears in paste dumps.

    Pastes are often from clipboard leaks, paste sites, etc.

    Args:
        email: Email address to check

    Returns:
        List of paste dictionaries if found, None on error
    """
    encoded_email = urllib.parse.quote(email)
    url = f"{API_BASE_URL}/pasteaccount/{encoded_email}"

    try:
        request = urllib.request.Request(
            url,
            headers={
                "User-Agent": USER_AGENT,
                "Accept": "application/json"
            }
        )

        with urllib.request.urlopen(request, timeout=10) as response:
            if response.status == 200:
                data = json.loads(response.read().decode('utf-8'))
                return data
            return []

    except urllib.error.HTTPError as e:
        if e.code == 404:
            return []
        print(f"[!] HTTP Error checking pastes: {e.code}")
        return None

    except Exception as e:
        print(f"[!] Error checking pastes: {e}")
        return None


def get_password_range(password: str) -> Optional[str]:
    """
    Check if a password has been seen in breaches.

    Uses k-Anonymity model: only sends first 5 chars of SHA-1 hash
    to the API, protecting your full password.

    Args:
        password: Password to check

    Returns:
        API response with hash suffix counts, or None on error

    How k-Anonymity works:
        Password: "password123"
        SHA-1:    "ef92b778bafe771e89245b89ecbc08a44a4e166c"

        Send to API: 5 char prefix = "ef92b"
        API returns: All hashes starting with "ef92b"

        You then check locally if your hash is in the list.
        This way, the API never sees your full hash or password!
    """
    # Hash the password with SHA-1
    sha1_hash = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()

    # Take only first 5 characters (k-Anonymity)
    prefix = sha1_hash[:5]
    suffix = sha1_hash[5:]

    # Build URL
    url = f"https://api.pwnedpasswords.com/range/{prefix}"

    try:
        request = urllib.request.Request(
            url,
            headers={"User-Agent": USER_AGENT}
        )

        with urllib.request.urlopen(request, timeout=10) as response:
            if response.status == 200:
                return response.read().decode('utf-8')
            return None

    except Exception as e:
        print(f"[!] Error checking password: {e}")
        return None


def check_password_breached(password: str) -> Optional[int]:
    """
    Check if a password has appeared in known breaches.

    Uses k-Anonymity so the API never sees your actual password.

    Args:
        password: Password to check

    Returns:
        Number of times password was found in breaches, or None on error
    """
    response = get_password_range(password)

    if response is None:
        return None

    # Parse response (format: "SUFFIX:COUNT\r\n...")
    for line in response.split('\r\n'):
        if ':' in line:
            suffix, count = line.split(':', 1)
            # Our suffix (remaining 35 chars of hash)
            our_hash = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()[5:]
            if suffix == our_hash:
                return int(count)

    # Password not found in breaches
    return 0


# ==============================================================================
# Output Formatting
# ==============================================================================

def format_breach(breach: Dict[str, Any]) -> str:
    """
    Format a breach record for display.

    Args:
        breach: Dictionary with breach information

    Returns:
        Formatted string with breach details
    """
    name = breach.get('Name', 'Unknown')
    title = breach.get('Title', 'Unknown')
    domain = breach.get('Domain', 'Unknown')
    breach_date = breach.get('BreachDate', 'Unknown')
    description = breach.get('Description', 'No description')[:100]

    # Strip HTML tags from description
    import re
    description = re.sub(r'<[^>]+>', '', description)

    data_classes = breach.get('DataClasses', [])

    output = f"""
  ╔══════════════════════════════════════════════════════════╗
  ║  {title:<54} ║
  ╠══════════════════════════════════════════════════════════╣
  ║  Name:        {name:<44} ║
  ║  Domain:      {domain:<44} ║
  ║  Date:        {breach_date:<44} ║
  ║  Description: {description[:44]:<44} ║
  ║  Exposed Data: {', '.join(data_classes[:5]):<41} ║
  ╚══════════════════════════════════════════════════════════╝
"""
    return output


def format_paste(paste: Dict[str, Any]) -> str:
    """Format a paste record for display."""
    source = paste.get('Source', 'Unknown')
    title = paste.get('Title', 'Unknown')
    date = paste.get('Date', 'Unknown')

    return f"""
  - Source: {source}
    Title:  {title}
    Date:   {date}
"""


def print_banner():
    """Display educational banner."""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║             EDUCATIONAL DATA BREACH CHECKER                   ║
║                                                              ║
║  Check if your email or passwords have appeared in known     ║
║  data breaches. Learn about breach exposure and protect      ║
║  your online accounts.                                        ║
║                                                              ║
║  Uses HaveIBeenPwned.com API (free, no account needed)       ║
║                                                              ║
║  ⚠️  EDUCATIONAL PURPOSE - Stay informed, stay safe!          ║
╚══════════════════════════════════════════════════════════════╝
"""
    print(banner)


def print_results(email: str, breaches: List[Dict], pastes: List[Dict] = None):
    """
    Print formatted breach check results.

    Args:
        email: Email that was checked
        breaches: List of breach records
        pastes: List of paste records
    """
    print("\n" + "=" * 60)
    print(f"              BREACH CHECK RESULTS")
    print("=" * 60)

    print(f"\n  Email: {email}")

    if breaches:
        print(f"\n  [!] FOUND IN {len(breaches)} BREACH(ES)!")
        print("\n  Your data was exposed in the following breaches:\n")

        for breach in breaches:
            print(format_breach(breach))

    else:
        print("\n  [OK] No breaches found!")
        print("       This email was NOT found in known data breaches.")

    if pastes:
        print(f"\n  [!] FOUND IN {len(pastes)} PASTE(S)!")
        print("\n  Your email appeared in the following paste dumps:\n")

        for paste in pastes:
            print(format_paste(paste))

    print("\n" + "-" * 60)


def print_password_check_result(password: str, count: int):
    """
    Print password breach check result.

    Args:
        password: Password that was checked
        count: Number of times found in breaches
    """
    print("\n" + "=" * 60)
    print("              PASSWORD CHECK RESULT")
    print("=" * 60)

    # Mask password for display
    masked = password[:2] + "*" * (len(password) - 4) + password[-2:] if len(password) > 4 else "*" * len(password)

    print(f"\n  Password: {masked}")

    if count and count > 0:
        print(f"\n  [!] DANGER: This password has been seen {count:,} times")
        print("       in known data breaches!")
        print("\n  This password is COMPROMISED and should NEVER be used.")
        print("  If you use this password anywhere, CHANGE IT IMMEDIATELY!")
    else:
        print("\n  [OK] This password was NOT found in known breaches.")
        print("       However, this doesn't mean it's a GOOD password.")


def print_security_advice():
    """Print educational security advice."""
    advice = """
╔══════════════════════════════════════════════════════════════╗
║                    SECURITY RECOMMENDATIONS                   ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  IF YOUR DATA WAS FOUND IN A BREACH:                         ║
║                                                              ║
║    1. CHANGE PASSWORDS immediately for affected accounts     ║
║    2. Enable TWO-FACTOR AUTHENTICATION (2FA)                ║
║    3. Use a PASSWORD MANAGER (Bitwarden, KeePass)           ║
║    4. Monitor your accounts for suspicious activity          ║
║    5. Check your credit reports                             ║
║    6. Be wary of PHISHING emails referencing the breach     ║
║                                                              ║
║  PREVENTIVE MEASURES:                                        ║
║                                                              ║
║    1. Use unique passwords for every account                ║
║    2. Use a password manager to generate/store passwords    ║
║    3. Enable 2FA wherever possible                          ║
║    4. Regularly check if your email appears in breaches     ║
║    5. Use a dedicated email for important accounts          ║
║    6. Don't click links in unexpected emails                ║
║                                                              ║
║  HOW BREACHES HAPPEN:                                        ║
║                                                              ║
║    - Database SQL injection                                  ║
║    - Phishing attacks                                        ║
║    - Weak or reused passwords                                ║
║    - Insider threats                                        ║
║    - Unsecured backups                                       ║
║    - Third-party service compromises                        ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
"""
    print(advice)


# ==============================================================================
# CLI Interface
# ==============================================================================

def validate_email(email: str) -> bool:
    """
    Basic email validation.

    Args:
        email: Email address to validate

    Returns:
        True if valid format, False otherwise
    """
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Educational Data Breach Checker",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s user@example.com                    # Check email for breaches
  %(prog)s user@example.com --pastes            # Also check paste dumps
  %(prog)s --password "myPassword123"         # Check if password breached
  %(prog)s user@example.com --check-password   # Check email AND password

Note: This uses the HaveIBeenPwned.com API (free tier).
      Rate limiting may apply for multiple requests.
        """
    )

    parser.add_argument(
        "email",
        nargs="?",
        help="Email address to check"
    )

    parser.add_argument(
        "-p", "--password",
        metavar="PASSWORD",
        help="Check if a password has been in a breach"
    )

    parser.add_argument(
        "-c", "--check-password",
        action="store_true",
        help="Prompt for password to check (secure input)"
    )

    parser.add_argument(
        "--pastes",
        action="store_true",
        help="Also check paste dumps (clipboard leaks)"
    )

    parser.add_argument(
        "--no-unverified",
        action="store_true",
        help="Exclude unverified breaches from results"
    )

    parser.add_argument(
        "-q", "--quiet",
        action="store_true",
        help="Suppress detailed output"
    )

    args = parser.parse_args()

    print_banner()

    # Check password only mode
    if args.password:
        print("[*] Checking password (using k-Anonymity for privacy)...")
        print("[*] Your full password never leaves your machine!")

        count = check_password_breached(args.password)
        if count is not None:
            print_password_check_result(args.password, count)
        else:
            print("[!] Could not check password. Check your internet connection.")

        return 0

    # Secure password input mode
    if args.check_password:
        try:
            import getpass
            password = getpass.getpass("Enter password to check: ")
            if password:
                print("\n[*] Checking password (using k-Anonymity for privacy)...")
                count = check_password_breached(password)
                if count is not None:
                    print_password_check_result(password, count)
        except Exception as e:
            print(f"[!] Error: {e}")
            return 1

        return 0

    # Email check mode
    if not args.email:
        parser.print_help()
        print("\n[!] Please provide an email to check, or use --password option.")
        return 1

    # Validate email
    if not validate_email(args.email):
        print(f"[!] Invalid email format: {args.email}")
        return 1

    print(f"[*] Checking breaches for: {args.email}")
    print("[*] This may take a moment...")

    # Rate limiting
    time.sleep(REQUEST_DELAY)

    # Check breaches
    breaches = check_breaches(
        args.email,
        include_unverified=not args.no_unverified
    )

    if breaches is None:
        print("[!] Could not complete breach check. Try again later.")
        return 1

    # Check pastes if requested
    pastes = None
    if args.pastes:
        print("[*] Also checking paste dumps...")
        time.sleep(REQUEST_DELAY)
        pastes = get_paste_account(args.email)

    # Print results
    if not args.quiet:
        print_results(args.email, breaches, pastes)

        if breaches:
            print_security_advice()
        else:
            print("\n[+] Great news! No breaches found for this email.")
            print("    Stay safe by using unique, strong passwords!")

    # Summary output for scripting
    print(f"\nSUMMARY: {args.email}")
    print(f"  Breaches found: {len(breaches)}")
    if pastes:
        print(f"  Pastes found:   {len(pastes)}")

    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n[!] Interrupted by user.")
        sys.exit(130)
    except Exception as e:
        print(f"[!] Error: {e}")
        sys.exit(1)
