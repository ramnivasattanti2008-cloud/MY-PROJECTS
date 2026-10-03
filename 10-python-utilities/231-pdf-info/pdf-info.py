#!/usr/bin/env python3
"""
PDF Info Tool
Extract metadata and information from PDF files.
"""

import argparse
import os
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

try:
    from PyPDF2 import PdfReader
    from PyPDF2.errors import PdfReadError
except ImportError:
    print("Error: PyPDF2 is required. Install with: pip install PyPDF2")
    sys.exit(1)


def get_pdf_info(input_path: str, verbose: bool = False) -> Dict:
    """Extract all available information from a PDF."""
    try:
        reader = PdfReader(input_path)

        info = {
            "file": input_path,
            "file_size": os.path.getsize(input_path),
            "encrypted": reader.is_encrypted,
            "page_count": len(reader.pages),
        }

        # Metadata
        if reader.metadata:
            metadata = {}
            for key, value in reader.metadata.items():
                # Clean up key names
                clean_key = key.replace("/", "")
                if hasattr(value, "replace"):
                    metadata[clean_key] = value
                else:
                    metadata[clean_key] = str(value)
            info["metadata"] = metadata

        # Page details
        if verbose:
            pages = []
            for i, page in enumerate(reader.pages, 1):
                page_info = {
                    "number": i,
                    "width": float(page.mediabox.width),
                    "height": float(page.mediabox.height),
                }
                pages.append(page_info)
            info["pages"] = pages

        return info

    except PdfReadError as e:
        print(f"Error reading PDF: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


def format_size(size_bytes: int) -> str:
    """Format file size in human-readable format."""
    for unit in ["B", "KB", "MB", "GB"]:
        if size_bytes < 1024:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.2f} TB"


def print_info(info: Dict, output_format: str = "text") -> None:
    """Print PDF information in specified format."""
    if output_format == "json":
        import json
        # Convert non-serializable items
        output = dict(info)
        print(json.dumps(output, indent=2, default=str))
    else:
        # Text format
        print(f"File: {info['file']}")
        print(f"Size: {format_size(info['file_size'])} ({info['file_size']:,} bytes)")
        print(f"Pages: {info['page_count']}")
        print(f"Encrypted: {'Yes' if info['encrypted'] else 'No'}")

        if "metadata" in info and info["metadata"]:
            print("\nMetadata:")
            for key, value in info["metadata"].items():
                print(f"  {key}: {value}")

        if "pages" in info and info["pages"]:
            print("\nPage Dimensions:")
            for page in info["pages"]:
                print(f"  Page {page['number']}: {page['width']:.1f} x {page['height']:.1f} pts")


def extract_text(input_path: str, pages: Optional[str] = None, max_length: int = 5000) -> None:
    """Extract text content from PDF."""
    try:
        reader = PdfReader(input_path)
        total_pages = len(reader.pages)

        # Parse pages to extract
        if pages:
            page_nums = set()
            for part in pages.split(","):
                part = part.strip()
                if "-" in part:
                    start, end = part.split("-")
                    start = int(start) if start.strip() else 1
                    end = int(end) if end.strip() else total_pages
                    page_nums.update(range(max(1, start), min(end, total_pages) + 1))
                else:
                    p = int(part)
                    if 1 <= p <= total_pages:
                        page_nums.add(p)
        else:
            page_nums = set(range(1, min(6, total_pages) + 1))

        print(f"Extracting text from {input_path}...")
        print("=" * 60)

        total_chars = 0
        for page_num in sorted(page_nums):
            page = reader.pages[page_num - 1]
            text = page.extract_text()

            if text:
                print(f"\n--- Page {page_num} ---")
                if len(text) > max_length:
                    print(text[:max_length] + f"\n... [{len(text) - max_length} more characters]")
                    total_chars += max_length
                else:
                    print(text)
                    total_chars += len(text)

        print("\n" + "=" * 60)
        print(f"Total characters extracted: {total_chars:,}")

    except PdfReadError as e:
        print(f"Error reading PDF: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


def extract_images(input_path: str, output_dir: str) -> None:
    """Extract images from PDF."""
    try:
        from PIL import Image
        import io

        reader = PdfReader(input_path)
        os.makedirs(output_dir, exist_ok=True)
        base_name = Path(input_path).stem

        print(f"Extracting images from {input_path}...")

        img_count = 0
        for page_num, page in enumerate(reader.pages, 1):
            if "/XObject" in page["/Resources"]:
                xobjects = page["/Resources"]["/XObject"].get_object()
                for obj in xobjects:
                    if xobjects[obj]["/Subtype"] == "/Image":
                        img_count += 1
                        try:
                            data = xobjects[obj].get_data()
                            img = Image.open(io.BytesIO(data))
                            output_path = os.path.join(
                                output_dir,
                                f"{base_name}_p{page_num}_{obj[1:]}.png"
                            )
                            img.save(output_path)
                            print(f"  Extracted: {os.path.basename(output_path)}")
                        except Exception as e:
                            print(f"  Warning: Could not extract {obj}: {e}")

        print(f"\nTotal images extracted: {img_count}")

    except ImportError:
        print("Error: Pillow required for image extraction. Install with: pip install Pillow")
        sys.exit(1)
    except PdfReadError as e:
        print(f"Error reading PDF: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


def compare_pdfs(files: List[str]) -> None:
    """Compare multiple PDFs."""
    if len(files) < 2:
        print("Error: Need at least 2 files to compare")
        sys.exit(1)

    print("PDF Comparison")
    print("=" * 60)

    infos = []
    for f in files:
        if not os.path.exists(f):
            print(f"Warning: File not found: {f}")
            continue
        infos.append(get_pdf_info(f))

    # Table header
    print(f"{'File':<30} {'Size':>10} {'Pages':>6} {'Encrypted':>10}")
    print("-" * 60)

    for info in infos:
        name = os.path.basename(info["file"])[:29]
        size = format_size(info["file_size"])
        pages = str(info["page_count"])
        enc = "Yes" if info["encrypted"] else "No"
        print(f"{name:<30} {size:>10} {pages:>6} {enc:>10}")

    print("-" * 60)

    # Summary
    page_counts = [i["page_count"] for i in infos]
    if len(set(page_counts)) == 1:
        print(f"All PDFs have the same page count: {page_counts[0]}")
    else:
        print(f"Page counts: {', '.join(str(p) for p in page_counts)}")


def list_pdfs_in_dir(directory: str, recursive: bool = False) -> None:
    """List all PDFs in a directory."""
    pdfs = []

    if recursive:
        pattern = "**/*.pdf"
    else:
        pattern = "*.pdf"

    for path in Path(directory).glob(pattern):
        pdfs.append(str(path))

    pdfs.sort()

    print(f"Found {len(pdfs)} PDF files in: {directory}")
    print("=" * 60)

    for pdf_path in pdfs:
        try:
            reader = PdfReader(pdf_path)
            size = os.path.getsize(pdf_path)
            pages = len(reader.pages)
            name = os.path.basename(pdf_path)
            print(f"{name:<40} {pages:>4} pages  {format_size(size):>10}")
        except Exception as e:
            print(f"{pdf_path}: Error - {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Extract metadata and information from PDF files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Get PDF info
  python pdf-info.py document.pdf

  # Verbose output with page details
  python pdf-info.py document.pdf -v

  # JSON output
  python pdf-info.py document.pdf --json

  # Extract text
  python pdf-info.py document.pdf --text

  # Extract text from specific pages
  python pdf-info.py document.pdf --text --pages "1-3,5"

  # Extract images
  python pdf-info.py document.pdf --extract-images -o images/

  # Compare multiple PDFs
  python pdf-info.py file1.pdf file2.pdf file3.pdf --compare

  # List PDFs in directory
  python pdf-info.py -l ./documents

  # List PDFs recursively
  python pdf-info.py -l ./documents -r
        """
    )

    parser.add_argument("input", nargs="?", help="Input PDF file path")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output with page details")
    parser.add_argument("--json", action="store_true", help="Output in JSON format")
    parser.add_argument("-t", "--text", action="store_true", help="Extract text content")
    parser.add_argument("--pages", help="Pages to extract text from (e.g., '1,3,5-10')")
    parser.add_argument("-i", "--extract-images", action="store_true", help="Extract images")
    parser.add_argument("-o", "--output-dir", help="Output directory for extracted content")
    parser.add_argument("--compare", action="store_true", help="Compare multiple PDFs")
    parser.add_argument("-l", "--list-dir", help="List all PDFs in directory")
    parser.add_argument("-r", "--recursive", action="store_true", help="Recursive search in directories")

    args = parser.parse_args()

    # List directory mode
    if args.list_dir:
        list_pdfs_in_dir(args.list_dir, args.recursive)
        return

    if not args.input:
        print("Error: Input file required (or use -l/--list-dir)")
        sys.exit(1)

    if not os.path.exists(args.input):
        print(f"Error: File not found: {args.input}")
        sys.exit(1)

    # Compare mode
    if args.compare:
        compare_pdfs([args.input])
        return

    # Extract images mode
    if args.extract_images:
        output_dir = args.output_dir or "extracted_images"
        extract_images(args.input, output_dir)
        return

    # Extract text mode
    if args.text:
        extract_text(args.input, args.pages)
        return

    # Default: show info
    info = get_pdf_info(args.input, args.verbose)
    format = "json" if args.json else "text"
    print_info(info, format)


if __name__ == "__main__":
    main()
