#!/usr/bin/env python3
"""
PDF Merger Tool
Merge multiple PDF files into one. Supports drag & drop and CLI usage.
"""

import argparse
import os
import sys
import re
from pathlib import Path
from typing import List, Optional

try:
    from PyPDF2 import PdfMerger
except ImportError:
    print("PyPDF2 not found. Installing...")
    os.system(f"{sys.executable} -m pip install PyPDF2")
    from PyPDF2 import PdfMerger


class PDFMerger:
    """PDF merging utility with multiple input methods."""

    def __init__(self):
        self.merger = PdfMerger()

    def add_pdf(self, pdf_path: str):
        """Add a single PDF to the merger."""
        path = Path(pdf_path)
        if not path.exists():
            raise FileNotFoundError(f"PDF not found: {pdf_path}")
        if path.suffix.lower() != '.pdf':
            raise ValueError(f"Not a PDF file: {pdf_path}")
        self.merger.append(str(path.resolve()))

    def add_pdfs_from_directory(self, directory: str, pattern: str = "*.pdf"):
        """Add all PDFs from a directory."""
        dir_path = Path(directory)
        if not dir_path.is_dir():
            raise NotADirectoryError(f"Not a directory: {directory}")

        pdfs = sorted(dir_path.glob(pattern))
        for pdf in pdfs:
            self.merger.append(str(pdf.resolve()))
        return len(pdfs)

    def merge(self, output_path: str, flatten: bool = True):
        """Merge all added PDFs and save to output."""
        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)

        with open(output, 'wb') as f:
            self.merger.write(f)

        self.merger.close()
        return str(output.resolve())

    def merge_files(self, input_files: List[str], output_path: str) -> str:
        """Convenience method to merge multiple files."""
        for pdf in input_files:
            self.add_pdf(pdf)
        return self.merge(output_path)


def natural_sort_key(s: str) -> List:
    """Generate a natural sort key for strings containing numbers."""
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', s)]


def get_pdf_files_from_drag_drop(paths: List[str]) -> List[str]:
    """Process drag-dropped files and directories."""
    pdf_files = []

    for path in paths:
        p = Path(path)
        if p.is_file() and p.suffix.lower() == '.pdf':
            pdf_files.append(str(p))
        elif p.is_dir():
            dir_pdfs = sorted(p.glob('*.pdf'), key=lambda x: natural_sort_key(str(x)))
            pdf_files.extend(str(f) for f in dir_pdfs)

    return pdf_files


def interactive_mode():
    """Interactive mode for selecting PDFs."""
    print("\n" + "=" * 50)
    print("PDF Merger - Interactive Mode")
    print("=" * 50)

    merger = PDFMerger()
    pdf_files = []

    while True:
        print("\nOptions:")
        print("  1. Add PDF file")
        print("  2. Add all PDFs from directory")
        print("  3. List added files")
        print("  4. Remove last file")
        print("  5. Merge and save")
        print("  6. Exit")

        choice = input("\nSelect option (1-6): ").strip()

        if choice == '1':
            path = input("  Enter PDF file path: ").strip().strip('"')
            try:
                merger.add_pdf(path)
                pdf_files.append(path)
                print(f"  Added: {Path(path).name}")
            except Exception as e:
                print(f"  Error: {e}")

        elif choice == '2':
            path = input("  Enter directory path: ").strip().strip('"')
            try:
                count = merger.add_pdfs_from_directory(path)
                print(f"  Added {count} PDFs from directory")
            except Exception as e:
                print(f"  Error: {e}")

        elif choice == '3':
            print(f"\n  Files to merge ({len(pdf_files)}):")
            for i, f in enumerate(pdf_files, 1):
                print(f"    {i}. {Path(f).name}")

        elif choice == '4':
            if pdf_files:
                removed = pdf_files.pop()
                print(f"  Removed: {Path(removed).name}")
            else:
                print("  No files to remove")

        elif choice == '5':
            if not pdf_files:
                print("  No files added yet!")
                continue

            output = input("  Enter output filename (default: merged.pdf): ").strip()
            if not output:
                output = "merged.pdf"
            if not output.endswith('.pdf'):
                output += '.pdf'

            try:
                result = merger.merge(output)
                print(f"\n  SUCCESS! Merged PDF saved to: {result}")
                print(f"  Total pages: {len(pdf_files)} files combined")
            except Exception as e:
                print(f"  Error: {e}")

        elif choice == '6':
            print("\nExiting...")
            break

        else:
            print("  Invalid option")


def main():
    parser = argparse.ArgumentParser(
        description='Merge multiple PDF files into one',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive mode
  python pdf-merger.py

  # Command line mode - specific files
  python pdf-merger.py file1.pdf file2.pdf file3.pdf -o merged.pdf

  # Command line mode - from directory
  python pdf-merger.py -d ./pdfs/ -o merged.pdf

  # Drag and drop (use quoted paths with wildcards)
  python pdf-merger.py "report*.pdf" "appendix*.pdf" -o final.pdf
        """
    )

    parser.add_argument('files', nargs='*', help='PDF files to merge (or use -d for directory)')
    parser.add_argument('-d', '--directory', help='Directory containing PDFs to merge')
    parser.add_argument('-o', '--output', default='merged.pdf', help='Output filename (default: merged.pdf)')
    parser.add_argument('-s', '--sort', action='store_true', help='Sort files naturally before merging')
    parser.add_argument('-i', '--interactive', action='store_true', help='Start in interactive mode')
    parser.add_argument('--reverse', action='store_true', help='Reverse file order')

    args = parser.parse_args()

    # Interactive mode
    if args.interactive or (not args.files and not args.directory):
        interactive_mode()
        return

    merger = PDFMerger()
    pdf_files = []

    # Collect PDF files
    if args.directory:
        dir_path = Path(args.directory)
        if not dir_path.is_dir():
            print(f"Error: Directory not found: {args.directory}")
            return
        files = sorted(dir_path.glob('*.pdf'))
        pdf_files = [str(f) for f in files]
        print(f"Found {len(pdf_files)} PDFs in {args.directory}")
    elif args.files:
        pdf_files = get_pdf_files_from_drag_drop(args.files)

    if not pdf_files:
        print("No PDF files found.")
        return

    # Sort if requested
    if args.sort:
        pdf_files = sorted(pdf_files, key=natural_sort_key)

    # Reverse if requested
    if args.reverse:
        pdf_files = list(reversed(pdf_files))

    # Merge
    print(f"Merging {len(pdf_files)} files...")
    for i, f in enumerate(pdf_files, 1):
        print(f"  [{i}/{len(pdf_files)}] {Path(f).name}")

    try:
        result = merger.merge_files(pdf_files, args.output)
        print(f"\nSuccess! Merged PDF saved to: {result}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
