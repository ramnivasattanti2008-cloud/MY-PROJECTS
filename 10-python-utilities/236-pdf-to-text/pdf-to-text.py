#!/usr/bin/env python3
"""
PDF to Text Extractor - Extract text content from PDF files.

Usage:
    Single file:    python pdf-to-text.py document.pdf
    Batch mode:     python pdf-to-text.py file1.pdf file2.pdf
    Directory:      python pdf-to-text.py /path/to/pdfs/
    Save to file:   python pdf-to-text.py document.pdf -o output.txt
    Page range:     python pdf-to-text.py document.pdf --pages 1-5
    Metadata only:  python pdf-to-text.py document.pdf --metadata
"""

import argparse
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import pdfplumber


@dataclass
class PDFInfo:
    """Stores PDF metadata and information."""
    filename: str
    page_count: int
    file_size: int
    title: Optional[str] = None
    author: Optional[str] = None
    subject: Optional[str] = None
    creator: Optional[str] = None
    producer: Optional[str] = None
    creation_date: Optional[str] = None
    modification_date: Optional[str] = None


@dataclass
class ExtractionResult:
    """Stores the result of text extraction."""
    filename: str
    text: str
    page_count: int
    success: bool
    error: Optional[str] = None


def get_pdf_info(filepath: str) -> Optional[PDFInfo]:
    """
    Get metadata and information about a PDF file.

    Args:
        filepath: Path to the PDF file

    Returns:
        PDFInfo object or None if file cannot be read
    """
    try:
        with pdfplumber.open(filepath) as pdf:
            metadata = pdf.metadata or {}

            # Get file size
            file_size = os.path.getsize(filepath)

            return PDFInfo(
                filename=os.path.basename(filepath),
                page_count=len(pdf.pages),
                file_size=file_size,
                title=metadata.get("Title"),
                author=metadata.get("Author"),
                subject=metadata.get("Subject"),
                creator=metadata.get("Creator"),
                producer=metadata.get("Producer"),
                creation_date=metadata.get("CreationDate"),
                modification_date=metadata.get("ModDate"),
            )
    except Exception as e:
        print(f"Error reading PDF info: {e}", file=sys.stderr)
        return None


def extract_text_from_pdf(filepath: str, pages: Optional[tuple[int, int]] = None) -> ExtractionResult:
    """
    Extract text content from a PDF file.

    Args:
        filepath: Path to the PDF file
        pages: Tuple of (start_page, end_page) or None for all pages

    Returns:
        ExtractionResult with extracted text
    """
    try:
        with pdfplumber.open(filepath) as pdf:
            total_pages = len(pdf.pages)

            # Determine page range
            if pages:
                start, end = pages
                start = max(1, start)
                end = min(total_pages, end)
            else:
                start, end = 1, total_pages

            # Extract text from each page
            text_parts = []
            for page_num in range(start, end + 1):
                page = pdf.pages[page_num - 1]  # pdfplumber uses 0-indexed
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(f"--- Page {page_num} ---\n{page_text}")

            full_text = "\n\n".join(text_parts)

            return ExtractionResult(
                filename=os.path.basename(filepath),
                text=full_text,
                page_count=end - start + 1,
                success=True,
            )
    except Exception as e:
        return ExtractionResult(
            filename=os.path.basename(filepath),
            text="",
            page_count=0,
            success=False,
            error=str(e),
        )


def extract_text_with_tables(filepath: str, pages: Optional[tuple[int, int]] = None) -> str:
    """
    Extract text and tables from a PDF file.

    Args:
        filepath: Path to the PDF file
        pages: Tuple of (start_page, end_page) or None for all pages

    Returns:
        Extracted text including tables as TSV
    """
    text_parts = []

    try:
        with pdfplumber.open(filepath) as pdf:
            total_pages = len(pdf.pages)

            if pages:
                start, end = pages
                start = max(1, start)
                end = min(total_pages, end)
            else:
                start, end = 1, total_pages

            for page_num in range(start, end + 1):
                page = pdf.pages[page_num - 1]

                # Extract text
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(f"--- Page {page_num} ---\n{page_text}")

                # Extract tables
                tables = page.extract_tables()
                for i, table in enumerate(tables):
                    text_parts.append(f"\n--- Page {page_num}, Table {i + 1} ---")
                    for row in table:
                        # Join cells with tab
                        row_text = "\t".join(str(cell) if cell else "" for cell in row)
                        text_parts.append(row_text)

    except Exception as e:
        text_parts.append(f"Error: {e}")

    return "\n".join(text_parts)


def format_file_size(size_bytes: int) -> str:
    """Format file size in human-readable format."""
    for unit in ["B", "KB", "MB", "GB"]:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"


def format_pdf_info(info: PDFInfo) -> str:
    """Format PDF metadata for display."""
    lines = [
        "",
        f"  PDF Information: {info.filename}",
        f"  {'─' * 50}",
        f"  Pages:          {info.page_count}",
        f"  Size:           {format_file_size(info.file_size)}",
        "",
        f"  Metadata",
        f"  ─────────────────────────────────────────",
    ]

    if info.title:
        lines.append(f"  Title:         {info.title}")
    if info.author:
        lines.append(f"  Author:        {info.author}")
    if info.subject:
        lines.append(f"  Subject:       {info.subject}")
    if info.creator:
        lines.append(f"  Creator:       {info.creator}")
    if info.producer:
        lines.append(f"  Producer:      {info.producer}")
    if info.creation_date:
        lines.append(f"  Created:       {info.creation_date}")
    if info.modification_date:
        lines.append(f"  Modified:      {info.modification_date}")

    if not any([info.title, info.author, info.subject, info.creator, info.producer, info.creation_date]):
        lines.append("  (No metadata available)")

    lines.append("")
    return "\n".join(lines)


def parse_page_range(pages_str: str) -> Optional[tuple[int, int]]:
    """
    Parse page range string like '1-5' or '1,2,3' or '5'.

    Returns:
        Tuple of (start_page, end_page) or None
    """
    if not pages_str:
        return None

    if "-" in pages_str:
        try:
            start, end = pages_str.split("-")
            return (int(start.strip()), int(end.strip()))
        except ValueError:
            return None
    elif "," in pages_str:
        # Return first and last page in list
        try:
            pages = [int(p.strip()) for p in pages_str.split(",")]
            return (min(pages), max(pages))
        except ValueError:
            return None
    else:
        try:
            page = int(pages_str)
            return (page, page)
        except ValueError:
            return None


def find_pdf_files(path: str) -> list[str]:
    """Find all PDF files in a path (file or directory)."""
    pdf_files = []
    path_obj = Path(path)

    if path_obj.is_file() and path_obj.suffix.lower() == ".pdf":
        pdf_files.append(str(path_obj))
    elif path_obj.is_dir():
        pdf_files.extend(str(p) for p in path_obj.rglob("*.pdf"))

    return pdf_files


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Extract text content from PDF files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "files",
        nargs="*",
        help="PDF file(s) or directory containing PDFs",
    )
    parser.add_argument(
        "--output", "-o",
        help="Output file path (default: print to stdout)",
    )
    parser.add_argument(
        "--pages", "-p",
        help="Page range to extract (e.g., '1-5' or '1,2,3' or '5')",
    )
    parser.add_argument(
        "--metadata", "-m",
        action="store_true",
        help="Show PDF metadata instead of text",
    )
    parser.add_argument(
        "--tables", "-t",
        action="store_true",
        help="Extract tables along with text",
    )
    parser.add_argument(
        "--silent",
        action="store_true",
        help="Suppress progress messages",
    )

    args = parser.parse_args()

    # Get PDF files
    if not args.files:
        parser.print_help()
        print("\n  Example: python pdf-to-text.py document.pdf")
        return 1

    pdf_files = []
    for path in args.files:
        pdf_files.extend(find_pdf_files(path))

    if not pdf_files:
        print(f"Error: No PDF files found in: {args.files}", file=sys.stderr)
        return 1

    # Parse page range
    pages = parse_page_range(args.pages) if args.pages else None

    # Process each PDF
    all_text = []
    errors = []

    for i, filepath in enumerate(pdf_files, 1):
        if not args.silent:
            print(f"[{i}/{len(pdf_files)}] Processing: {filepath}")

        if args.metadata:
            info = get_pdf_info(filepath)
            if info:
                print(format_pdf_info(info))
            else:
                errors.append(filepath)
        else:
            if args.tables:
                text = extract_text_with_tables(filepath, pages)
            else:
                result = extract_text_from_pdf(filepath, pages)
                text = result.text
                if not result.success:
                    errors.append(f"{filepath}: {result.error}")

            if len(pdf_files) > 1:
                header = f"\n{'='*60}\n{filepath}\n{'='*60}\n"
                all_text.append(header + text)
            else:
                all_text.append(text)

    # Output results
    full_text = "\n".join(all_text)

    if args.output:
        output_path = Path(args.output)
        output_path.write_text(full_text, encoding="utf-8")
        if not args.silent:
            print(f"\nText saved to: {args.output}")
            if pages:
                print(f"Extracted pages: {pages[0]}-{pages[1]}")
            else:
                print(f"Extracted {len(pdf_files)} file(s)")
    else:
        print(full_text)

    # Summary
    if errors and not args.silent:
        print(f"\nErrors encountered ({len(errors)}):")
        for error in errors:
            print(f"  - {error}")

    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
