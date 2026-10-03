#!/usr/bin/env python3
"""
SSL Certificate Checker - Educational Security Tool

This tool demonstrates SSL/TLS certificate inspection for learning
about certificate security and HTTPS implementation.

EDUCATIONAL PURPOSE ONLY - Learn about certificate security.
Author: Educational Security Project
"""

import sys
import argparse
import socket
import ssl
import datetime
import json
from typing import Optional, Dict, Any, Tuple
from urllib.parse import urlparse

# ==============================================================================
# Configuration
# ==============================================================================

# Default port
DEFAULT_HTTPS_PORT = 443

# Common certificate issues for education
CERTIFICATE_ISSUES = {
    "expired": "Certificate has expired!",
    "self_signed": "Certificate is self-signed (not from trusted CA)",
    "mismatch": "Certificate hostname mismatch!",
    "weak_hash": "Certificate uses weak hash algorithm (MD5/SHA1)",
    "short_key": "Certificate uses short key length",
    "no_chain": "Certificate chain incomplete",
}

# Minimum acceptable key sizes
MIN_KEY_SIZES = {
    "RSA": 2048,
    "DSA": 2048,
    "EC": 256,
}


# ==============================================================================
# Certificate Functions
# ==============================================================================

def get_certificate(host: str, port: int = DEFAULT_HTTPS_PORT, timeout: float = 10.0) -> Optional[Dict[str, Any]]:
    """
    Retrieve SSL/TLS certificate information from a server.

    Args:
        host: Target hostname or IP address
        port: HTTPS port (default: 443)
        timeout: Connection timeout in seconds

    Returns:
        Dictionary with certificate information, or None on error
    """
    # Create SSL context - we want to get the cert, so we don't verify
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    try:
        # Connect to server
        with socket.create_connection((host, port), timeout=timeout) as sock:
            with context.wrap_socket(sock, server_hostname=host) as ssock:
                # Get certificate
                cert = ssock.getpeercert(binary_form=True)

                # Get certificate details
                cert_dict = ssock.getpeercert()

                # Parse certificate info
                return parse_certificate(cert_dict, host)

    except ssl.SSLCertVerificationError as e:
        print(f"[!] Certificate verification error: {e}")
        return None
    except ssl.SSLError as e:
        print(f"[!] SSL error: {e}")
        return None
    except socket.timeout:
        print(f"[!] Connection timeout")
        return None
    except socket.gaierror as e:
        print(f"[!] DNS resolution error: {e}")
        return None
    except ConnectionRefusedError:
        print(f"[!] Connection refused - is HTTPS enabled on port {port}?")
        return None
    except Exception as e:
        print(f"[!] Error: {e}")
        return None


def parse_certificate(cert: Dict, host: str) -> Dict[str, Any]:
    """
    Parse certificate dictionary into structured format.

    Args:
        cert: Certificate dictionary from ssl socket
        host: Target hostname

    Returns:
        Structured certificate information
    """
    if not cert:
        return {}

    info = {
        "subject": dict(x[0] for x in cert.get("subject", [])),
        "issuer": dict(x[0] for x in cert.get("issuer", [])),
        "version": cert.get("version"),
        "serialNumber": cert.get("serialNumber"),
        "notBefore": cert.get("notBefore"),
        "notAfter": cert.get("notAfter"),
        "subjectAltName": cert.get("subjectAltName", []),
        "OCSP": cert.get("OCSP", []),
        "caIssuers": cert.get("caIssuers", []),
        "crlDistributionPoints": cert.get("crlDistributionPoints", []),
    }

    # Add parsed dates
    try:
        info["notBefore_dt"] = datetime.datetime.strptime(
            cert.get("notBefore", ""), "%b %d %H:%M:%S %Y %Z"
        )
    except:
        info["notBefore_dt"] = None

    try:
        info["notAfter_dt"] = datetime.datetime.strptime(
            cert.get("notAfter", ""), "%b %d %H:%M:%S %Y %Z"
        )
    except:
        info["notAfter_dt"] = None

    # Add hostname
    info["host"] = host

    # Analyze certificate
    info["issues"] = analyze_certificate(info)

    return info


def analyze_certificate(cert_info: Dict[str, Any]) -> list:
    """
    Analyze certificate for security issues.

    Args:
        cert_info: Parsed certificate information

    Returns:
        List of issues found
    """
    issues = []

    # Check expiration
    if cert_info.get("notAfter_dt"):
        if cert_info["notAfter_dt"] < datetime.datetime.now():
            issues.append("expired")
        elif cert_info["notAfter_dt"] < datetime.datetime.now() + datetime.timedelta(days=30):
            issues.append("expiring_soon")

    # Check self-signed (issuer same as subject)
    subject = cert_info.get("subject", {})
    issuer = cert_info.get("issuer", {})
    if subject.get("commonName") == issuer.get("commonName"):
        issues.append("self_signed")

    # Check hostname match
    host = cert_info.get("host", "")
    san_list = [name for (typ, name) in cert_info.get("subjectAltName", [])]

    if not san_list:
        # Fall back to CN
        if host and host not in str(subject.get("commonName", "")):
            issues.append("mismatch")
    else:
        # Check if host is in SAN list
        host_matched = any(
            host == san or (san.startswith("*.") and host.endswith(san[2:]))
            for san in san_list
        )
        if not host_matched:
            issues.append("mismatch")

    return issues


def get_certificate_chain(host: str, port: int = DEFAULT_HTTPS_PORT) -> list:
    """
    Get the full certificate chain from a server.

    Args:
        host: Target hostname
        port: HTTPS port

    Returns:
        List of certificates in the chain
    """
    chain = []

    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    try:
        with socket.create_connection((host, port), timeout=10) as sock:
            with context.wrap_socket(sock, server_hostname=host) as ssock:
                # Get peer certificate chain
                cert_bin = ssock.getpeercert(binary_form=True)
                if cert_bin:
                    chain.append(cert_bin)

    except Exception:
        pass

    return chain


def check_certificate_transparency(host: str, port: int = DEFAULT_HTTPS_PORT) -> Dict[str, Any]:
    """
    Educational note about Certificate Transparency.

    Certificate Transparency (CT) is a system for logging
    SSL certificates. This demonstrates the concept.

    Args:
        host: Target hostname
        port: HTTPS port

    Returns:
        Information about CT
    """
    # In a full implementation, you would query CT logs
    # For education, we explain the concept

    return {
        "explanation": "Certificate Transparency (CT) is a public log",
        "benefit": "Allows detection of unauthorized certificates",
        "how_it_works": "CAs must submit certificates to CT logs before issuing",
        "check_ct": "Use crt.sh or certspotter.com to see certificate history",
        "note": "Full CT verification requires access to CT log APIs"
    }


# ==============================================================================
# Output Functions
# ==============================================================================

def format_datetime(dt: datetime.datetime) -> str:
    """Format datetime for display."""
    if dt:
        return dt.strftime("%Y-%m-%d %H:%M:%S %Z")
    return "Unknown"


def print_certificate_info(cert_info: Dict[str, Any], verbose: bool = True):
    """
    Print formatted certificate information.

    Args:
        cert_info: Parsed certificate information
        verbose: Show detailed output
    """
    if not cert_info:
        print("[!] Could not retrieve certificate information")
        return

    print("\n" + "=" * 70)
    print("                  SSL CERTIFICATE INFORMATION")
    print("=" * 70)

    # Host
    print(f"\n  Target:        {cert_info.get('host', 'Unknown')}")

    # Subject
    subject = cert_info.get('subject', {})
    print(f"  Common Name:   {subject.get('commonName', 'N/A')}")
    print(f"  Organization: {subject.get('organizationName', 'N/A')}")

    # Issuer
    issuer = cert_info.get('issuer', {})
    print(f"\n  Issuer:")
    print(f"    Common Name:   {issuer.get('commonName', 'N/A')}")
    print(f"    Organization:  {issuer.get('organizationName', 'N/A')}")

    # Validity
    print(f"\n  Validity:")
    print(f"    Valid From:   {format_datetime(cert_info.get('notBefore_dt'))}")
    print(f"    Valid Until:  {format_datetime(cert_info.get('notAfter_dt'))}")

    # Days remaining
    if cert_info.get('notAfter_dt'):
        delta = cert_info['notAfter_dt'] - datetime.datetime.now()
        if delta.days >= 0:
            print(f"    Days Remaining: {delta.days} days")
        else:
            print(f"    Days Expired: {-delta.days} days ago!")

    # Serial number
    print(f"\n  Serial Number: {cert_info.get('serialNumber', 'N/A')}")

    # Version
    print(f"  Version:       {cert_info.get('version', 'N/A')}")

    # Subject Alternative Names
    san_list = cert_info.get('subjectAltName', [])
    if san_list:
        print(f"\n  Valid Hostnames:")
        for typ, name in san_list[:10]:
            print(f"    - {name}")
        if len(san_list) > 10:
            print(f"    ... and {len(san_list) - 10} more")

    # Certificate chain
    if verbose:
        print(f"\n  CA Issuers: {', '.join(cert_info.get('caIssuers', [])[:2]) or 'N/A'}")

        ct_info = check_certificate_transparency(cert_info['host'])
        print(f"\n  Certificate Transparency:")
        print(f"    Note: {ct_info['explanation']}")

    # Issues
    issues = cert_info.get('issues', [])
    if issues:
        print("\n  " + "!" * 30)
        print("  SECURITY ISSUES FOUND:")
        print("  " + "!" * 30)
        for issue in issues:
            if issue in CERTIFICATE_ISSUES:
                print(f"    [!] {CERTIFICATE_ISSUES[issue]}")
            else:
                print(f"    [!] {issue}")

    print("\n" + "=" * 70)


def print_security_grade(cert_info: Dict[str, Any]) -> str:
    """
    Calculate and print a simple security grade.

    Args:
        cert_info: Certificate information

    Returns:
        Grade letter (A-F)
    """
    if not cert_info:
        return "F"

    score = 100
    issues = cert_info.get('issues', [])

    # Deduct for issues
    if 'expired' in issues:
        score -= 50
    if 'self_signed' in issues:
        score -= 20
    if 'mismatch' in issues:
        score -= 40
    if 'weak_hash' in issues:
        score -= 30
    if 'short_key' in issues:
        score -= 30

    # Check expiration warning
    if cert_info.get('notAfter_dt'):
        days_left = (cert_info['notAfter_dt'] - datetime.datetime.now()).days
        if days_left < 0:
            score = 0
        elif days_left < 30:
            score -= 15
        elif days_left < 90:
            score -= 5

    # Determine grade
    if score >= 90:
        grade = "A"
    elif score >= 80:
        grade = "B"
    elif score >= 70:
        grade = "C"
    elif score >= 50:
        grade = "D"
    else:
        grade = "F"

    # Print grade
    colors = {
        "A": "\033[92m",  # Green
        "B": "\033[92m",  # Green
        "C": "\033[93m",  # Yellow
        "D": "\033[91m",  # Red
        "F": "\033[91m",  # Red
    }
    reset = "\033[0m"

    try:
        print(f"\n  Security Grade: {colors[grade]}{grade}{reset}")
    except:
        print(f"\n  Security Grade: {grade}")

    return grade


def print_security_tips():
    """Print educational security tips about SSL/TLS."""
    tips = """
╔══════════════════════════════════════════════════════════════╗
║                 SSL/TLS CERTIFICATE SECURITY TIPS             ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  UNDERSTANDING SSL/TLS:                                     ║
║    - SSL/TLS encrypts data between you and the server       ║
║    - Certificates prove the server's identity              ║
║    - HTTPS = HTTP over TLS (secure HTTP)                    ║
║                                                              ║
║  WHAT TO CHECK:                                             ║
║    ✓ Certificate validity dates (not expired)              ║
║    ✓ Certificate issuer (trusted CA?)                       ║
║    ✓ Hostname matches the site you're visiting             ║
║    ✓ Key size (RSA 2048+ or EC 256+)                       ║
║    ✓ Certificate chain is complete                         ║
║                                                              ║
║  COMMON ISSUES:                                             ║
║    ✗ Expired certificates                                  ║
║    ✗ Self-signed certificates (not from trusted CA)       ║
║    ✗ Hostname mismatch (potential phishing)                 ║
║    ✗ Weak algorithms (MD5, SHA1)                           ║
║    ✗ Short key lengths                                     ║
║                                                              ║
║  BROWSER SECURITY INDICATORS:                               ║
║    - Lock icon: Connection is encrypted                     ║
║    - Green bar: Extended validation (EV) certificate       ║
║    - Red warning: Certificate problem                      ║
║                                                              ║
║  PROTECT YOURSELF:                                          ║
║    - Never ignore certificate warnings                      ║
║    - Keep your system's CA certificates updated             ║
║    - Use modern browsers with up-to-date security           ║
║    - Report suspicious certificate errors                   ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
"""
    print(tips)


def print_banner():
    """Display educational banner."""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║          EDUCATIONAL SSL CERTIFICATE CHECKER                ║
║                                                              ║
║  This tool demonstrates SSL/TLS certificate inspection      ║
║  for learning about HTTPS security and certificates.       ║
║                                                              ║
║  ⚠️  EDUCATIONAL PURPOSE - DO NOT USE FOR MALICIOUS         ║
║     PURPOSES LIKE IMPERSONATING WEBSITES                    ║
╚══════════════════════════════════════════════════════════════╝
"""
    print(banner)


# ==============================================================================
# CLI Interface
# ==============================================================================

def parse_url(url: str) -> Tuple[str, int]:
    """
    Parse URL to extract host and port.

    Args:
        url: URL string (with or without scheme)

    Returns:
        Tuple of (host, port)
    """
    # Add scheme if missing
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url

    parsed = urlparse(url)

    host = parsed.hostname or ""
    port = parsed.port or 443

    return host, port


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Educational SSL Certificate Checker",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s example.com                   # Check certificate
  %(prog)s https://example.com           # Check with URL
  %(prog)s example.com:8443              # Check custom port
  %(prog)s example.com -j                 # JSON output
  %(prog)s example.com --check-expiry    # Show expiry info

Certificate Checks:
  - Expiration date
  - Issuer information
  - Hostname match
  - Certificate chain
  - Security issues
        """
    )

    parser.add_argument(
        "host",
        nargs="?",
        help="Target hostname or URL"
    )

    parser.add_argument(
        "-p", "--port",
        type=int,
        default=DEFAULT_HTTPS_PORT,
        help=f"HTTPS port (default: {DEFAULT_HTTPS_PORT})"
    )

    parser.add_argument(
        "-j", "--json",
        action="store_true",
        help="Output results as JSON"
    )

    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Show detailed output"
    )

    parser.add_argument(
        "--check-expiry",
        action="store_true",
        help="Show detailed expiration information"
    )

    parser.add_argument(
        "-q", "--quiet",
        action="store_true",
        help="Suppress informational output"
    )

    args = parser.parse_args()

    print_banner()

    if not args.host:
        parser.print_help()
        print("\n[!] Please provide a hostname to check.")
        return 1

    # Parse host and port
    try:
        if args.host.startswith(('http://', 'https://')):
            host, port = parse_url(args.host)
        else:
            host = args.host
            port = args.port

        # Remove port from host if included
        if ':' in host and not args.host.startswith('http'):
            host = host.split(':')[0]

    except Exception as e:
        print(f"[!] Error parsing host: {e}")
        return 1

    if not args.quiet:
        print(f"[*] Checking certificate for: {host}:{port}")

    # Get certificate
    cert_info = get_certificate(host, port)

    if args.json:
        # JSON output
        output = {
            "host": host,
            "port": port,
            "success": cert_info is not None,
            "certificate": None
        }

        if cert_info:
            # Convert datetime objects for JSON serialization
            cert_json = cert_info.copy()
            cert_json['notBefore_dt'] = format_datetime(cert_info.get('notBefore_dt'))
            cert_json['notAfter_dt'] = format_datetime(cert_info.get('notAfter_dt'))
            output['certificate'] = cert_json

        print(json.dumps(output, indent=2))

    else:
        # Formatted output
        print_certificate_info(cert_info, verbose=args.verbose)

        if cert_info:
            grade = print_security_grade(cert_info)

            if args.check_expiry and cert_info.get('notAfter_dt'):
                expiry = cert_info['notAfter_dt']
                now = datetime.datetime.now()
                delta = expiry - now

                if delta.days >= 0:
                    print(f"\n  [!] Certificate expires in {delta.days} days")
                    if delta.days < 30:
                        print(f"  [!] WARNING: Certificate expiring soon!")
                else:
                    print(f"\n  [!] CRITICAL: Certificate expired {-delta.days} days ago!")

        if not args.quiet:
            print_security_tips()

    return 0 if cert_info else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n[!] Interrupted by user.")
        sys.exit(130)
    except Exception as e:
        print(f"[!] Error: {e}")
        sys.exit(1)
