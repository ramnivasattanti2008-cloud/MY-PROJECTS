#!/usr/bin/env python3
"""
File Encrypter/Decrypter using Fernet symmetric encryption.

This script demonstrates symmetric encryption basics using the Fernet scheme
from the cryptography library. Fernet guarantees that a message encrypted using
it cannot be manipulated or read without the key.

Educational Purpose:
- Shows how symmetric encryption works (same key for encrypt/decrypt)
- Demonstrates secure key derivation from passwords
- Illustrates proper error handling for file operations
- Shows how to use salt for key derivation to prevent rainbow table attacks

Author: Educational Example
License: MIT
"""

import argparse
import base64
import hashlib
import os
import sys
from pathlib import Path

try:
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
except ImportError:
    print("Error: cryptography library not installed.")
    print("Run: pip install cryptography")
    sys.exit(1)


class FileEncrypter:
    """
    Handles file encryption and decryption using Fernet symmetric encryption.

    Attributes:
        key (bytes): The encryption key derived from the user's password
        cipher (Fernet): The Fernet cipher instance for encrypt/decrypt operations
    """

    def __init__(self, password: str, salt: bytes = None):
        """
        Initialize the encrypter with a password.

        Args:
            password: The user's password for encryption/decryption
            salt: Optional salt for key derivation. If None, a new random salt is generated.
                  The salt is stored alongside the encrypted file for decryption.
        """
        self.salt = salt if salt else os.urandom(16)
        self.key = self._derive_key(password, self.salt)
        self.cipher = Fernet(self.key)

    @staticmethod
    def _derive_key(password: str, salt: bytes) -> bytes:
        """
        Derive a cryptographic key from a password using PBKDF2.

        PBKDF2 (Password-Based Key Derivation Function 2) is designed to make
        brute-force attacks more expensive by requiring many iterations.

        Args:
            password: The user's password
            salt: Random bytes to prevent rainbow table attacks

        Returns:
            A URL-safe base64-encoded 32-byte key
        """
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=480000,  # OWASP recommended minimum for PBKDF2-SHA256
        )
        return base64.urlsafe_b64encode(kdf.derive(password.encode()))

    def encrypt_file(self, input_path: str, output_path: str = None) -> str:
        """
        Encrypt a file using Fernet symmetric encryption.

        The encrypted output format:
        - First 16 bytes: Salt used for key derivation
        - Remaining bytes: Fernet-encrypted data (includes timestamp and HMAC)

        Args:
            input_path: Path to the file to encrypt
            output_path: Path for the encrypted output. If None, adds .encrypted extension.

        Returns:
            Path to the encrypted file

        Raises:
            FileNotFoundError: If input file doesn't exist
            PermissionError: If file cannot be read/written
        """
        input_path = Path(input_path)

        if not input_path.exists():
            raise FileNotFoundError(f"Input file not found: {input_path}")

        if not input_path.is_file():
            raise ValueError(f"Input path is not a file: {input_path}")

        # Determine output path
        if output_path is None:
            output_path = input_path.with_suffix(input_path.suffix + '.encrypted')
        else:
            output_path = Path(output_path)

        print(f"Encrypting: {input_path.name}")
        print(f"  File size: {input_path.stat().st_size:,} bytes")
        print(f"  Using salt: {self.salt.hex()}")

        try:
            # Read the file content
            with open(input_path, 'rb') as f:
                plaintext = f.read()

            # Encrypt using Fernet (adds timestamp and HMAC automatically)
            ciphertext = self.cipher.encrypt(plaintext)

            # Write salt + encrypted data
            with open(output_path, 'wb') as f:
                f.write(self.salt)
                f.write(ciphertext)

            print(f"  Encrypted size: {output_path.stat().st_size:,} bytes")
            print(f"Output: {output_path}")

            return str(output_path)

        except PermissionError as e:
            raise PermissionError(f"Permission denied: {e}")
        except IOError as e:
            raise IOError(f"Error reading/writing file: {e}")

    def decrypt_file(self, input_path: str, output_path: str = None) -> str:
        """
        Decrypt a file that was encrypted with this encrypter.

        The encrypted file format is expected to be:
        - First 16 bytes: Salt
        - Remaining bytes: Fernet-encrypted data

        Args:
            input_path: Path to the encrypted file
            output_path: Path for the decrypted output. If None, removes .encrypted extension
                        or adds .decrypted suffix.

        Returns:
            Path to the decrypted file

        Raises:
            FileNotFoundError: If encrypted file doesn't exist
            ValueError: If the file format is invalid or decryption fails
        """
        input_path = Path(input_path)

        if not input_path.exists():
            raise FileNotFoundError(f"Encrypted file not found: {input_path}")

        # Determine output path
        if output_path is None:
            if input_path.suffix == '.encrypted':
                output_path = input_path.with_suffix('')
            else:
                output_path = input_path.with_suffix(input_path.suffix + '.decrypted')
        else:
            output_path = Path(output_path)

        print(f"Decrypting: {input_path.name}")

        try:
            # Read the encrypted file
            with open(input_path, 'rb') as f:
                file_data = f.read()

            # Extract salt (first 16 bytes) and ciphertext
            if len(file_data) < 17:
                raise ValueError("Invalid encrypted file: too short")

            salt = file_data[:16]
            ciphertext = file_data[16:]

            # If salt matches, re-derive the key
            if salt != self.salt:
                print(f"  Note: Salt differs, re-deriving key...")
                self.salt = salt
                self.key = self._derive_key(
                    self._original_password, self.salt
                ) if hasattr(self, '_original_password') else self._derive_key("", salt)
                self.cipher = Fernet(self.key)

            # Decrypt and verify
            plaintext = self.cipher.decrypt(ciphertext)

            # Write decrypted content
            with open(output_path, 'wb') as f:
                f.write(plaintext)

            print(f"  Decrypted size: {output_path.stat().st_size:,} bytes")
            print(f"Output: {output_path}")

            return str(output_path)

        except Exception as e:
            raise ValueError(f"Decryption failed: {e}. Possible wrong password.")


def main():
    """Main entry point with CLI argument parsing."""
    parser = argparse.ArgumentParser(
        description='Encrypt and decrypt files using Fernet symmetric encryption.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Encrypt a file:
    python file-encrypter.py encrypt secret.txt

  Decrypt with custom output:
    python file-encrypter.py decrypt secret.txt.encrypted -o original.txt

  Use a specific password:
    python file-encrypter.py encrypt document.pdf -p MySecretPassword

Security Notes:
  - Use strong passwords (at least 12 characters with mixed case, numbers, symbols)
  - The same password always produces different ciphertexts due to random IVs
  - PBKDF2 with 480,000 iterations protects against brute-force attacks
  - Keep your password safe - there's no recovery without it!
        """
    )

    parser.add_argument(
        'action',
        choices=['encrypt', 'decrypt'],
        help='Action to perform'
    )
    parser.add_argument(
        'input',
        help='Input file path'
    )
    parser.add_argument(
        '-o', '--output',
        help='Output file path (default: adds .encrypted or removes it)'
    )
    parser.add_argument(
        '-p', '--password',
        help='Encryption/decryption password (will prompt if not provided)'
    )
    parser.add_argument(
        '-s', '--salt',
        help='Salt as hex string for reproducible key derivation'
    )

    args = parser.parse_args()

    # Get password securely
    password = args.password
    if not password:
        try:
            import getpass
            password = getpass.getpass('Enter password: ')
            if not password:
                print("Error: Password cannot be empty")
                sys.exit(1)
        except (ImportError, EOFError):
            password = input('Enter password: ')

    # Parse salt if provided
    salt = None
    if args.salt:
        try:
            salt = bytes.fromhex(args.salt)
            if len(salt) != 16:
                print("Error: Salt must be exactly 16 bytes (32 hex characters)")
                sys.exit(1)
        except ValueError:
            print("Error: Invalid hex string for salt")
            sys.exit(1)

    # Perform the requested action
    encrypter = FileEncrypter(password, salt)
    if hasattr(encrypter, '_original_password'):
        encrypter._original_password = password
    else:
        # Store password for re-derivation during decryption
        encrypter._original_password = password

    try:
        if args.action == 'encrypt':
            result = encrypter.encrypt_file(args.input, args.output)
            print(f"\nEncryption successful!")
        else:
            result = encrypter.decrypt_file(args.input, args.output)
            print(f"\nDecryption successful!")

        print(f"File saved: {result}")

    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except (ValueError, PermissionError, IOError) as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
