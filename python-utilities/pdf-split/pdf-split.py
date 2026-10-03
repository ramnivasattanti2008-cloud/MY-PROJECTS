#!/usr/bin/env python3
"""
PDF Split Tool
Split PDF files into separate pages or page ranges.
"""

import argparse
import os
import sys
from pathlib import Path
from typing import List, Tuple, Optional

try:
    from PyPDF2 import PdfReader, PdfWriter
    from PyPDF2.errors import PdfReadError
except ImportError:
    print("Error: PyPDF2 is required. Install with: pip install PyPDF2")
    sys.exit(1)


def parse_page_ranges(pages_str: str, max_pages: int) -> List[int]:
    """Parse page range string into list of page numbers."""
    pages = set()

    if pages_str.lower() == "all":
        return list(range(1, max_pages + 1))

    for part in pages_str.split(","):
        part = part.strip()
        if "-" in part:
            start, end = part.split("-", 1)
            start = int(start.strip()) if start.strip() else 1
            end = int(end.strip()) if end.strip() else max_pages
            for p in range(max(start, 1), min(end, max_pages) + 1):
                pages.add(p)
        else:
            p = int(part)
            if 1 <= p <= max_pages:
                pages.add(p)

    return sorted(list(pages))


def split_by_pages(
    input_path: str,
    output_dir: str,
    pages: str = "all",
    prefix: str = "page",
    extension: str = "pdf"
) -> None:
    """Split PDF into individual pages."""
    try:
        reader = PdfReader(input_path)
        total_pages = len(reader.pages)
        page_list = parse_page_ranges(pages, total_pages)

        os.makedirs(output_dir, exist_ok=True)
        base_name = Path(input_path).stem

        print(f"Splitting {input_path} ({total_pages} pages)...")
        print(f"Output directory: {output_dir}")

        for i, page_num in enumerate(page_list, 1):
            writer = PdfWriter()
            writer.add_page(reader.pages[page_num - 1])

            output_path = os.path.join(
                output_dir,
                f"{base_name}_{prefix}_{page_num:03d}.{extension}"
            )

            with open(output_path, "wb") as f:
                writer.write(f)

            print(f"  Created: {os.path.basename(output_path)}")

        print(f"\nSuccessfully created {len(page_list)} files")

    except PdfReadError as e:
        print(f"Error reading PDF: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


def split_by_ranges(
    input_path: str,
    output_dir: str,
    ranges: List[str],
    prefix: str = "split",
    extension: str = "pdf"
) -> None:
    """Split PDF by page ranges."""
    try:
        reader = PdfReader(input_path)
        total_pages = len(reader.pages)

        os.makedirs(output_dir, exist_ok=True)
        base_name = Path(input_path).stem

        print(f"Splitting {input_path} ({total_pages} pages) by ranges...")
        print(f"Output directory: {output_dir}")

        for i, range_str in enumerate(ranges, 1):
            page_list = parse_page_ranges(range_str, total_pages)

            if not page_list:
                print(f"  Warning: No valid pages in range '{range_str}', skipping")
                continue

            writer = PdfWriter()
            for page_num in page_list:
                writer.add_page(reader.pages[page_num - 1])

            output_path = os.path.join(
                output_dir,
                f"{base_name}_{prefix}_{i:02d}.{extension}"
            )

            with open(output_path, "wb") as f:
                writer.write(f)

            print(f"  Created: {os.path.basename(output_path)} ({len(page_list)} pages)")

        print(f"\nSuccessfully created {len(ranges)} files")

    except PdfReadError as e:
        print(f"Error reading PDF: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


def split_every_n(
    input_path: str,
    output_dir: str,
    n: int,
    prefix: str = "split",
    extension: str = "pdf"
) -> None:
    """Split PDF into chunks of N pages."""
    try:
        reader = PdfReader(input_path)
        total_pages = len(reader.pages)

        os.makedirs(output_dir, exist_ok=True)
        base_name = Path(input_path).stem

        print(f"Splitting {input_path} ({total_pages} pages) into groups of {n}...")

        num_files = (total_pages + n - 1) // n

        for i in range(num_files):
            writer = PdfWriter()
            start = i * n
            end = min(start + n, total_pages)

            for page_num in range(start, end):
                writer.add_page(reader.pages[page_num])

            output_path = os.path.join(
                output_dir,
                f"{base_name}_{prefix}_{i+1:02d}.{extension}"
            )

            with open(output_path, "wb") as f:
                writer.write(f)

            print(f"  Created: {os.path.basename(output_path)} ({end - start} pages)")

        print(f"\nSuccessfully created {num_files} files")

    except PdfReadError as e:
        print(f"Error reading PDF: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


def extract_pages(
    input_path: str,
    output_path: str,
    pages: str = "all"
) -> None:
    """Extract specific pages into a new PDF."""
    try:
        reader = PdfReader(input_path)
        total_pages = len(reader.pages)
        page_list = parse_page_ranges(pages, total_pages)

        writer = PdfWriter()
        for page_num in page_list:
            writer.add_page(reader.pages[page_num - 1])

        with open(output_path, "wb") as f:
            writer.write(f)

        print(f"Extracted {len(page_list)} pages to: {output_path}")

    except PdfReadError as e:
        print(f"Error reading PDF: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


def show_info(input_path: str) -> None:
    """Show PDF page information."""
    try:
        reader = PdfReader(input_path)
        total_pages = len(reader.pages)

        print(f"PDF: {input_path}")
        print(f"Total pages: {total_pages}")
        print("\nPage ranges:")

        # Group consecutive pages
        groups = []
        current = []

        for i in range(1, total_pages + 1):
            if not current:
                current = [i]
            elif i == current[-1] + 1:
                current.append(i)
            else:
                groups.append(current)
                current = [i]
        if current:
            groups.append(current)

        # Display groups
        for i, group in enumerate(groups, 1):
            if len(group) == 1:
                print(f"  {i}. Page {group[0]}")
            else:
                print(f"  {i}. Pages {group[0]}-{group[-1]} ({len(group)} pages)")

    except PdfReadError as e:
        print(f"Error reading PDF: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Split PDF files into separate pages or page ranges",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Extract all pages as separate files
  python pdf-split.py input.pdf -o pages/

  # Extract specific pages
  python pdf-split.py input.pdf -o pages/ --pages "1,3,5,7-10"

  # Split by ranges (first 5, then 6-10, then rest)
  python pdf-split.py input.pdf -o splits/ --ranges "1-5" "6-10" "11-20"

  # Split into chunks of 10 pages
  python pdf-split.py input.pdf -o chunks/ --every 10

  # Extract pages to single file
  python pdf-split.py input.pdf -o output.pdf --pages "1-5"

  # Show page info
  python pdf-split.py input.pdf --info
        """
    )

    parser.add_argument("input", help="Input PDF file path")
    parser.add_argument("-o", "--output", help="Output directory or file path")
    parser.add_argument("--pages", help="Pages to extract (e.g., '1,3,5-10' or 'all')")
    parser.add_argument("--ranges", nargs="+", help="Page ranges to split by (e.g., '1-5' '6-10')")
    parser.add_argument("--every", type=int, help="Split into chunks of N pages")
    parser.add_argument("--prefix", default="page", help="Output file prefix (default: page)")
    parser.add_argument("--info", action="store_true", help="Show PDF page information")
    parser.add_argument("--extract", action="store_true", help="Extract pages to single output file")

    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"Error: Input file not found: {args.input}")
        sys.exit(1)

    # Show info mode
    if args.info:
        show_info(args.input)
        return

    if not args.output:
        print("Error: Output path required (use -o/--output)")
        sys.exit(1)

    # Determine output directory
    if args.ranges or args.every:
        output_dir = args.output
    elif args.output.endswith(".pdf"):
        output_dir = args.output
    else:
        output_dir = args.output

    # Ensure output directory exists for file splits
    if not output_dir.endswith(".pdf"):
        os.makedirs(output_dir, exist_ok=True)

    # Perform split
    if args.ranges:
        split_by_ranges(args.input, output_dir, args.ranges, args.prefix)
    elif args.every:
        split_every_n(args.input, output_dir, args.every, args.prefix)
    elif args.pages:
        if output_dir.endswith(".pdf"):
            extract_pages(args.input, output_dir, args.pages)
        else:
            split_by_pages(args.input, output_dir, args.pages, args.prefix)
    else:
        split_by_pages(args.input, output_dir, "all", args.prefix)


if __name__ == "__main__":
    main()
