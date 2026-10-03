#!/usr/bin/env python3
"""
PDF Merge Tool
Merge multiple PDF files into a single PDF document.
"""

import argparse
import os
import sys
from pathlib import Path
from typing import List, Optional

try:
    from PyPDF2 import PdfMerger, PdfReader
    from PyPDF2.errors import PdfReadError
except ImportError:
    print("Error: PyPDF2 is required. Install with: pip install PyPDF2")
    sys.exit(1)


def merge_pdfs(
    input_files: List[str],
    output_path: str,
    verbose: bool = False
) -> None:
    """Merge multiple PDF files into one."""
    merger = PdfMerger()

    try:
        for i, pdf_path in enumerate(input_files):
            if not os.path.exists(pdf_path):
                print(f"Warning: File not found, skipping: {pdf_path}")
                continue

            try:
                merger.append(pdf_path)
                if verbose:
                    reader = PdfReader(pdf_path)
                    print(f"  Added: {pdf_path} ({len(reader.pages)} pages)")
            except PdfReadError as e:
                print(f"Warning: Could not read {pdf_path}, skipping: {e}")
                continue

        if len(merger.inputs) == 0:
            print("Error: No valid PDF files were provided")
            sys.exit(1)

        with open(output_path, "wb") as f:
            merger.write(f)

        total_pages = sum(len(PdfReader(pf).pages) for pf in input_files if os.path.exists(pf))
        print(f"Successfully merged {len(merger.inputs)} PDF files into: {output_path}")
        print(f"Total pages: {total_pages}")

    except Exception as e:
        print(f"Error during merge: {e}")
        sys.exit(1)
    finally:
        merger.close()


def merge_pdfs_from_file(
    file_list_path: str,
    output_path: str,
    verbose: bool = False
) -> None:
    """Merge PDFs listed in a text file."""
    if not os.path.exists(file_list_path):
        print(f"Error: File list not found: {file_list_path}")
        sys.exit(1)

    with open(file_list_path, 'r') as f:
        files = [line.strip() for line in f if line.strip() and not line.startswith('#')]

    if not files:
        print("Error: No files found in list")
        sys.exit(1)

    print(f"Found {len(files)} files to merge")
    merge_pdfs(files, output_path, verbose)


def merge_with_bookmarks(
    input_files: List[str],
    output_path: str,
    bookmarks: Optional[List[str]] = None
) -> None:
    """Merge PDFs with custom bookmark titles."""
    merger = PdfMerger()

    try:
        for i, pdf_path in enumerate(input_files):
            if not os.path.exists(pdf_path):
                print(f"Warning: File not found, skipping: {pdf_path}")
                continue

            title = bookmarks[i] if bookmarks and i < len(bookmarks) else os.path.basename(pdf_path)
            merger.append(pdf_path, outline_item=title)

            if bookmarks and i < len(bookmarks):
                print(f"  Added: {pdf_path} as '{bookmarks[i]}'")
            else:
                print(f"  Added: {pdf_path}")

        with open(output_path, "wb") as f:
            merger.write(f)

        print(f"Successfully merged with bookmarks: {output_path}")

    except Exception as e:
        print(f"Error during merge: {e}")
        sys.exit(1)
    finally:
        merger.close()


def show_preview(input_files: List[str]) -> None:
    """Show preview of files to be merged."""
    print("PDF Merge Preview")
    print("=" * 60)

    total_pages = 0
    for i, pdf_path in enumerate(input_files, 1):
        if not os.path.exists(pdf_path):
            print(f"  {i}. [NOT FOUND] {pdf_path}")
            continue

        try:
            reader = PdfReader(pdf_path)
            pages = len(reader.pages)
            total_pages += pages

            # Get title if available
            metadata = reader.metadata
            title = metadata.get('/Title', 'N/A') if metadata else 'N/A'

            print(f"  {i}. {os.path.basename(pdf_path)}")
            print(f"     Pages: {pages}")
            print(f"     Title: {title}")
        except Exception as e:
            print(f"  {i}. [ERROR] {pdf_path}: {e}")

    print("=" * 60)
    print(f"Total files: {len([f for f in input_files if os.path.exists(f)])}")
    print(f"Total pages: {total_pages}")


def main():
    parser = argparse.ArgumentParser(
        description="Merge multiple PDF files into one",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Merge files in order
  python pdf-merge.py file1.pdf file2.pdf file3.pdf -o merged.pdf

  # Use file list
  python pdf-merge.py -l files.txt -o merged.pdf

  # Merge with bookmarks
  python pdf-merge.py file1.pdf file2.pdf -o merged.pdf -b "Cover" "Content"

  # Preview before merging
  python pdf-merge.py file1.pdf file2.pdf --preview
        """
    )

    parser.add_argument("files", nargs="*", help="Input PDF files to merge")
    parser.add_argument("-o", "--output", required=True, help="Output PDF file path")
    parser.add_argument("-l", "--list", help="Text file containing list of PDF paths (one per line)")
    parser.add_argument("-b", "--bookmarks", nargs="+", help="Bookmark titles for each PDF")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    parser.add_argument("--preview", action="store_true", help="Preview files without merging")

    args = parser.parse_args()

    # Get input files
    if args.list:
        if not os.path.exists(args.list):
            print(f"Error: File list not found: {args.list}")
            sys.exit(1)
        with open(args.list, 'r') as f:
            input_files = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    else:
        input_files = args.files

    if not input_files:
        print("Error: No input files specified. Use positional args or -l/--list")
        sys.exit(1)

    # Filter existing files
    existing_files = [f for f in input_files if os.path.exists(f)]
    if not existing_files:
        print("Error: None of the specified files exist")
        sys.exit(1)

    if len(existing_files) < len(input_files):
        missing = set(input_files) - set(existing_files)
        print(f"Warning: {len(missing)} file(s) not found, skipping: {', '.join(missing)}")

    # Preview mode
    if args.preview:
        show_preview(input_files)
        return

    # Ensure output directory exists
    output_dir = os.path.dirname(args.output)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Merge with or without bookmarks
    if args.bookmarks:
        merge_with_bookmarks(existing_files, args.output, args.bookmarks)
    else:
        merge_pdfs(existing_files, args.output, args.verbose)


if __name__ == "__main__":
    main()
