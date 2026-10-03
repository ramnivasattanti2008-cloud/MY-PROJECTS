#!/usr/bin/env python3
"""
PDF Encrypt/Decrypt Tool
Encrypt or decrypt PDF files with password protection.
"""

import argparse
import os
import sys
import getpass
from pathlib import Path

try:
    from PyPDF2 import PdfReader, PdfWriter
    from PyPDF2.errors import PdfReadError
except ImportError:
    print("Error: PyPDF2 is required. Install with: pip install PyPDF2")
    sys.exit(1)


def encrypt_pdf(
    input_path: str,
    output_path: str,
    password: str,
    user_password: str = None,
    allow_print: bool = True,
    allow_copy: bool = True,
    allow_modify: bool = True,
    allow_annotations: bool = True,
    allow_form_fill: bool = True,
    allow_accessibility: bool = True
) -> None:
    """Encrypt a PDF file with password protection."""
    try:
        reader = PdfReader(input_path)
        writer = PdfWriter()

        # Copy all pages
        for page in reader.pages:
            writer.add_page(page)

        # Set permissions
        permissions = 0
        if allow_print:
            permissions |= 0b00000100  # PRINT
        if allow_copy:
            permissions |= 0b00010000  # COPY
        if allow_modify:
            permissions |= 0b00001000  # MODIFY
        if allow_annotations:
            permissions |= 0b00100000  # ANNOTATE
        if allow_form_fill:
            permissions |= 0b01000000  # FILL_FORM
        if allow_accessibility:
            permissions |= 0b10000000  # ACCESSIBILITY

        # Encrypt with both owner and user passwords
        writer.encrypt(
            user_password=password if user_password is None else user_password,
            owner_password=password,
            permissions_flag=permissions
        )

        with open(output_path, "wb") as f:
            writer.write(f)

        print(f"Successfully encrypted: {output_path}")
        print(f"Password protection enabled")

    except PdfReadError as e:
        print(f"Error reading PDF: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error encrypting PDF: {e}")
        sys.exit(1)


def decrypt_pdf(
    input_path: str,
    output_path: str,
    password: str
) -> None:
    """Decrypt a PDF file using password."""
    try:
        reader = PdfReader(input_path)

        if not reader.is_encrypted:
            print("Warning: PDF is not encrypted, copying as-is")
        else:
            if not reader.decrypt(password):
                print("Error: Incorrect password")
                sys.exit(1)
            print("Successfully decrypted")

        writer = PdfWriter()
        for page in reader.pages:
            writer.add_page(page)

        with open(output_path, "wb") as f:
            writer.write(f)

        print(f"Saved to: {output_path}")

    except PdfReadError as e:
        print(f"Error reading PDF: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error decrypting PDF: {e}")
        sys.exit(1)


def remove_password(
    input_path: str,
    output_path: str,
    owner_password: str
) -> None:
    """Remove password protection from PDF (requires owner password)."""
    try:
        reader = PdfReader(input_path)

        if not reader.is_encrypted:
            print("Warning: PDF is not encrypted")
            # Just copy
            writer = PdfWriter()
            for page in reader.pages:
                writer.add_page(page)
            with open(output_path, "wb") as f:
                writer.write(f)
        else:
            if not reader.decrypt(owner_password):
                print("Error: Incorrect password")
                sys.exit(1)

            writer = PdfWriter()
            for page in reader.pages:
                writer.add_page(page)

            with open(output_path, "wb") as f:
                writer.write(f)

        print(f"Password removed: {output_path}")

    except PdfReadError as e:
        print(f"Error reading PDF: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error removing password: {e}")
        sys.exit(1)


def check_encryption(input_path: str) -> None:
    """Check encryption status of a PDF."""
    try:
        reader = PdfReader(input_path)

        print(f"File: {input_path}")
        print(f"Encrypted: {'Yes' if reader.is_encrypted else 'No'}")

        if reader.is_encrypted:
            if reader.decrypt(""):
                print("Empty password: No password required")
            else:
                print("Password required to open")

        # Try to get metadata
        if reader.metadata:
            print("\nMetadata:")
            for key, value in reader.metadata.items():
                if value:
                    print(f"  {key}: {value}")

    except PdfReadError as e:
        print(f"Error reading PDF: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


def batch_encrypt(
    input_files: list,
    output_dir: str,
    password: str,
    suffix: str = "_encrypted"
) -> None:
    """Encrypt multiple PDF files."""
    os.makedirs(output_dir, exist_ok=True)

    success = 0
    failed = []

    for input_path in input_files:
        if not os.path.exists(input_path):
            print(f"Warning: File not found, skipping: {input_path}")
            failed.append(input_path)
            continue

        base_name = Path(input_path).stem
        output_path = os.path.join(output_dir, f"{base_name}{suffix}.pdf")

        try:
            encrypt_pdf(input_path, output_path, password)
            success += 1
        except Exception as e:
            print(f"Error processing {input_path}: {e}")
            failed.append(input_path)

    print(f"\nBatch encryption complete: {success} succeeded, {len(failed)} failed")


def main():
    parser = argparse.ArgumentParser(
        description="Encrypt or decrypt PDF files with password protection",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Encrypt a PDF (will prompt for password)
  python pdf-encrypt.py input.pdf output.pdf --encrypt

  # Encrypt with explicit password
  python pdf-encrypt.py input.pdf output.pdf -e -p MyPassword123

  # Decrypt a PDF
  python pdf-encrypt.py encrypted.pdf decrypted.pdf --decrypt

  # Remove password protection
  python pdf-encrypt.py protected.pdf unprotected.pdf --remove

  # Check encryption status
  python pdf-encrypt.py document.pdf --check

  # Batch encrypt files
  python pdf-encrypt.py file1.pdf file2.pdf -o encrypted/ --encrypt -p secret
        """
    )

    parser.add_argument("input", help="Input PDF file path")
    parser.add_argument("output", nargs="?", help="Output PDF file path")
    parser.add_argument("-e", "--encrypt", action="store_true", help="Encrypt the PDF")
    parser.add_argument("-d", "--decrypt", action="store_true", help="Decrypt the PDF")
    parser.add_argument("-r", "--remove", action="store_true", help="Remove password protection")
    parser.add_argument("-p", "--password", help="Password (will prompt if not provided)")
    parser.add_argument("-o", "--output-dir", help="Output directory for batch operations")
    parser.add_argument("--check", action="store_true", help="Check encryption status")
    parser.add_argument("--user-password", help="Separate user password (optional)")
    parser.add_argument("--suffix", default="_encrypted", help="Suffix for batch output files")
    parser.add_argument("--no-print", action="store_true", help="Disable printing")
    parser.add_argument("--no-copy", action="store_true", help="Disable copying")
    parser.add_argument("--no-modify", action="store_true", help="Disable modifications")

    args = parser.parse_args()

    # Check mode
    if args.check:
        check_encryption(args.input)
        return

    # Determine action
    if args.encrypt:
        action = "encrypt"
    elif args.decrypt:
        action = "decrypt"
    elif args.remove:
        action = "remove"
    else:
        # Auto-detect based on input encryption
        try:
            reader = PdfReader(args.input)
            action = "decrypt" if reader.is_encrypted else "encrypt"
            print(f"Auto-detected action: {action}")
        except:
            action = "encrypt"

    # Get password
    password = args.password
    if not password:
        if action in ("encrypt", "decrypt", "remove"):
            password = getpass.getpass("Enter password: ")
            if action == "encrypt" and args.remove:
                confirm = getpass.getpass("Confirm password: ")
                if password != confirm:
                    print("Error: Passwords do not match")
                    sys.exit(1)

    if not password:
        print("Error: Password is required")
        sys.exit(1)

    # Determine output path
    output_path = args.output
    if not output_path:
        if args.output_dir:
            base_name = Path(args.input).stem
            suffix = args.suffix if action == "encrypt" else "_decrypted"
            output_path = os.path.join(args.output_dir, f"{base_name}{suffix}.pdf")
        else:
            base_name = Path(args.input).stem
            suffix = args.suffix if action == "encrypt" else "_decrypted"
            output_path = f"{base_name}{suffix}.pdf"

    # Ensure output directory exists
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Execute action
    if action == "encrypt":
        encrypt_pdf(
            args.input, output_path, password,
            user_password=args.user_password,
            allow_print=not args.no_print,
            allow_copy=not args.no_copy,
            allow_modify=not args.no_modify
        )
    elif action == "decrypt":
        decrypt_pdf(args.input, output_path, password)
    elif action == "remove":
        remove_password(args.input, output_path, password)


if __name__ == "__main__":
    main()
