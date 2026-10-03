#!/usr/bin/env python3
"""
Hash Cracker - Educational Hash Lookup Tool

This tool demonstrates why password hashing is critical for security.
It performs hash lookups against a small embedded wordlist to show
how easily weak passwords can be cracked.

EDUCATIONAL PURPOSE ONLY - Do NOT use for unauthorized access.
Author: Educational Security Project
"""

import hashlib
import argparse
import sys
import string
from typing import Optional, List, Tuple

try:
    from wordlist import get_all_words, COMMON_PASSWORDS
except ImportError:
    from .wordlist import get_all_words, COMMON_PASSWORDS


# ==============================================================================
# Hash Algorithms Supported
# ==============================================================================

SUPPORTED_ALGORITHMS = {
    "md5": hashlib.md5,
    "sha1": hashlib.sha1,
    "sha256": hashlib.sha256,
    "sha512": hashlib.sha512,
}


# ==============================================================================
# Core Hash Functions
# ==============================================================================

def hash_password(password: str, algorithm: str) -> str:
    """
    Hash a password using the specified algorithm.

    Args:
        password: The plaintext password to hash
        algorithm: Hash algorithm name (md5, sha1, sha256, sha512)

    Returns:
        Hexadecimal hash string

    Raises:
        ValueError: If algorithm is not supported
    """
    if algorithm not in SUPPORTED_ALGORITHMS:
        raise ValueError(f"Unsupported algorithm: {algorithm}")

    hasher = SUPPORTED_ALGORITHMS[algorithm]()
    hasher.update(password.encode('utf-8'))
    return hasher.hexdigest()


def generate_hash_variants(password: str) -> List[Tuple[str, str]]:
    """
    Generate all hash variants for a password.

    Args:
        password: Plaintext password

    Returns:
        List of (algorithm, hash) tuples
    """
    variants = []
    for algo_name in SUPPORTED_ALGORITHMS:
        try:
            h = hash_password(password, algo_name)
            variants.append((algo_name, h))
        except Exception:
            pass
    return variants


def identify_hash_type(hash_str: str) -> Optional[str]:
    """
    Attempt to identify the hash algorithm based on length.

    Args:
        hash_str: The hash string to identify

    Returns:
        Algorithm name if identified, None otherwise
    """
    length = len(hash_str)

    hash_lengths = {
        32: "md5",
        40: "sha1",
        64: "sha256",
        128: "sha512",
    }

    return hash_lengths.get(length)


# ==============================================================================
# Dictionary Attack
# ==============================================================================

def dictionary_attack(
    target_hash: str,
    wordlist: Optional[List[str]] = None,
    algorithm: Optional[str] = None,
    case_sensitive: bool = False
) -> Optional[str]:
    """
    Perform a dictionary attack against a hash.

    Args:
        target_hash: The hash to crack (lowercase)
        wordlist: List of passwords to try (default: embedded wordlist)
        algorithm: Hash algorithm to use (auto-detect if None)
        case_sensitive: Whether to try case variants

    Returns:
        The cracked password if found, None otherwise
    """
    if wordlist is None:
        wordlist = get_all_words()

    # Auto-detect algorithm if not specified
    if algorithm is None:
        algorithm = identify_hash_type(target_hash)
        if algorithm is None:
            print(f"[!] Could not identify hash type. Please specify with -a/--algorithm")
            return None
        print(f"[*] Auto-detected algorithm: {algorithm}")

    # Try each word in the wordlist
    for word in wordlist:
        passwords_to_try = [word]

        # Add case variants if not case-sensitive
        if not case_sensitive:
            passwords_to_try.extend([
                word.upper(),
                word.capitalize(),
                word.lower(),
            ])

        for pwd in passwords_to_try:
            try:
                computed = hash_password(pwd, algorithm)
                if computed.lower() == target_hash.lower():
                    return pwd
            except Exception:
                pass

    return None


def rainbow_table_demo(hash_str: str) -> dict:
    """
    Educational demonstration of rainbow table attacks.

    A rainbow table is a precomputed table for reversing cryptographic
    hash functions. It trades storage space for computation time.

    Args:
        hash_str: Hash to look up

    Returns:
        Dictionary with educational info about rainbow tables
    """
    return {
        "hash": hash_str,
        "vulnerability": "Rainbow tables can crack unsalted hashes instantly",
        "protection": "Use salted passwords + strong hash functions (bcrypt, Argon2)",
        "note": "Modern systems use bcrypt/Argon2/scrypt which are resistant to rainbow tables"
    }


# ==============================================================================
# Hash Generation Mode
# ==============================================================================

def generate_all_hashes(password: str) -> List[Tuple[str, str]]:
    """
    Generate all hash variants for a password.
    Useful for comparing how different algorithms encode the same input.

    Args:
        password: Plaintext password

    Returns:
        List of (algorithm, hash) tuples
    """
    results = []
    for algo_name, hasher_func in SUPPORTED_ALGORITHMS.items():
        h = hash_password(password, algo_name)
        results.append((algo_name, h))
        print(f"  {algo_name:8s}: {h}")

    return results


# ==============================================================================
# CLI Interface
# ==============================================================================

def print_banner():
    """Display educational banner."""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║           EDUCATIONAL HASH CRACKER - LEARN SECURITY          ║
║                                                              ║
║  This tool demonstrates why HASHING matters for passwords.   ║
║  Strong, unique passwords + proper hashing = security.        ║
║                                                              ║
║  ⚠️  EDUCATIONAL PURPOSE ONLY - DO NOT USE FOR ILLEGAL       ║
║     UNAUTHORIZED ACCESS TO SYSTEMS YOU DON'T OWN             ║
╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Educational Hash Lookup Tool - Learn Password Security",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s -g password123           # Generate all hashes for a password
  %(prog)s 5f4dcc3b5aa765d61d8327deb882cf99  # Crack a hash (MD5 auto-detected)
  %(prog)s -c 5f4dcc3b5aa765d61d8327deb882cf99 -a md5
  %(prog)s -i e10adc3949ba59abbe56e057f20f883e -a md5 --info

Disclaimer: This tool is for EDUCATIONAL purposes only. Always follow
ethical guidelines and only test systems you have permission to test.
        """
    )

    parser.add_argument(
        "hash",
        nargs="?",
        help="Hash to crack (hexadecimal string)"
    )

    parser.add_argument(
        "-g", "--generate",
        metavar="PASSWORD",
        help="Generate hash for a password (educational)"
    )

    parser.add_argument(
        "-a", "--algorithm",
        choices=list(SUPPORTED_ALGORITHMS.keys()),
        help="Hash algorithm (auto-detected if not specified)"
    )

    parser.add_argument(
        "-c", "--check",
        metavar="HASH",
        help="Check hash against wordlist (same as passing hash directly)"
    )

    parser.add_argument(
        "-i", "--info",
        action="store_true",
        help="Show educational info about the hash"
    )

    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Show verbose output"
    )

    args = parser.parse_args()

    print_banner()

    # Generate mode
    if args.generate:
        password = args.generate
        print(f"[*] Generating hashes for: '{password}'")
        print(f"[*] Password length: {len(password)} characters")
        print()

        generate_all_hashes(password)

        # Show why hashing matters
        print("\n[*] WHY HASHING MATTERS:")
        print("    - Storing passwords in plaintext is DANGEROUS")
        print("    - Hashing is ONE-WAY: can't reverse a hash")
        print("    - Always use salt + strong algorithms (bcrypt, Argon2)")
        print("    - This tool uses weak algorithms (MD5/SHA1) for education")
        return 0

    # Check/ crack mode
    target_hash = args.check or args.hash

    if not target_hash:
        parser.print_help()
        print("\n[!] No hash provided. Use -g to generate a hash, or provide a hash to crack.")
        return 1

    # Clean up the hash
    target_hash = target_hash.strip().lower()

    # Validate hash format
    if not all(c in "0123456789abcdef" for c in target_hash):
        print(f"[!] Invalid hash format. Hash should be hexadecimal.")
        return 1

    # Info mode
    if args.info:
        print(f"[*] Hash: {target_hash}")
        algo = identify_hash_type(target_hash)
        if algo:
            print(f"[*] Detected algorithm: {algo}")
            print(f"[*] Hash length: {len(target_hash)} characters")

        info = rainbow_table_demo(target_hash)
        print("\n[*] EDUCATIONAL INFO:")
        print(f"    Vulnerability: {info['vulnerability']}")
        print(f"    Protection: {info['protection']}")
        print(f"    Note: {info['note']}")

        # Try to crack anyway for education
        print("\n[*] Attempting dictionary crack...")

    # Attempt dictionary attack
    print(f"[*] Starting dictionary attack...")
    print(f"[*] Wordlist size: {len(get_all_words())} words")
    print(f"[*] Algorithms to try: {', '.join(SUPPORTED_ALGORITHMS.keys())}")

    # Try each algorithm
    found_password = None
    found_algo = None

    algorithms_to_try = [args.algorithm] if args.algorithm else list(SUPPORTED_ALGORITHMS.keys())

    for algo in algorithms_to_try:
        if args.verbose:
            print(f"[*] Trying {algo}...")

        result = dictionary_attack(target_hash, algorithm=algo)
        if result:
            found_password = result
            found_algo = algo
            break

    print()  # Blank line for readability

    if found_password:
        print("=" * 60)
        print(f"  [FOUND!] Password: {found_password}")
        print(f"  Algorithm: {found_algo}")
        print("=" * 60)

        print("\n[*] SECURITY LESSON:")
        print("    - This password was found in a small wordlist")
        print("    - Real attackers use BILLIONS of passwords")
        print("    - ALWAYS use strong, unique passwords")
        print("    - Enable 2FA wherever possible")
    else:
        print("[*] Password NOT found in wordlist.")
        print("    This could mean:")
        print("    - The password is not in our small wordlist")
        print("    - The hash algorithm is different")
        print("    - The hash uses a salt")

        print("\n[*] TRY STRONGER PASSWORDS:")
        print("    - Use 12+ characters minimum")
        print("    - Mix uppercase, lowercase, numbers, symbols")
        print("    - Use a password manager (Bitwarden, KeePass)")
        print("    - Never reuse passwords across sites")

    print("\n[*] Protection tips:")
    print("    1. Use unique, strong passwords for each account")
    print("    2. Enable two-factor authentication (2FA)")
    print("    3. Use a reputable password manager")
    print("    4. Check passwords at haveibeenpwned.com")
    print("    5. Never share passwords or send them via email")

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
