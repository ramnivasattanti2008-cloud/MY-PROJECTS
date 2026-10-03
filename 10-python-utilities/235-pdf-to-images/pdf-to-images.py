#!/usr/bin/env python3
"""
PDF to Images Converter
Convert PDF pages to images using PyMuPDF or pdf2image.
"""

import argparse
import sys
from pathlib import Path


def convert_with_pymupdf(pdf_path: Path, output_dir: Path, dpi: int, fmt: str, first_page: int = None, last_page: int = None):
    """Convert PDF to images using PyMuPDF (fitz)."""
    try:
        import fitz  # PyMuPDF
    except ImportError:
        print("Error: PyMuPDF not installed. Run: pip install pymupdf")
        sys.exit(1)

    output_dir.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(str(pdf_path))

    start = first_page if first_page is not None else 0
    end = last_page if last_page is not None else len(doc)

    page_count = 0
    for page_num in range(start, min(end, len(doc))):
        page = doc[page_num]
        zoom = dpi / 72
        mat = fitz.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=mat)

        output_name = f"page_{page_num + 1:04d}.{fmt}"
        output_path = output_dir / output_name
        pix.save(str(output_path))
        page_count += 1
        print(f"  Converted page {page_num + 1} -> {output_path.name}")

    doc.close()
    return page_count


def convert_with_pdf2image(pdf_path: Path, output_dir: Path, dpi: int, fmt: str, first_page: int = None, last_page: int = None):
    """Convert PDF to images using pdf2image + poppler."""
    try:
        from pdf2image import convert_from_path
    except ImportError:
        print("Error: pdf2image not installed. Run: pip install pdf2image")
        sys.exit(1)

    output_dir.mkdir(parents=True, exist_ok=True)

    kwargs = {"dpi": dpi, "fmt": fmt}
    if first_page is not None:
        kwargs["first_page"] = first_page
    if last_page is not None:
        kwargs["last_page"] = last_page

    images = convert_from_path(str(pdf_path), **kwargs)

    for i, image in enumerate(images):
        output_name = f"page_{i + 1:04d}.{fmt.lower()}"
        output_path = output_dir / output_name
        image.save(str(output_path))
        print(f"  Converted page {i + 1} -> {output_path.name}")

    return len(images)


def main():
    parser = argparse.ArgumentParser(
        description="Convert PDF pages to images",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  pdf-to-images.py input.pdf
  pdf-to-images.py input.pdf -o output_images
  pdf-to-images.py input.pdf --dpi 150 --format png
  pdf-to-images.py input.pdf --pages 1-5
  pdf-to-images.py input.pdf --engine pymupdf
        """
    )
    parser.add_argument("input", type=Path, help="Input PDF file")
    parser.add_argument("-o", "--output", type=Path, help="Output directory (default: <input>_images)")
    parser.add_argument("--dpi", type=int, default=150, help="Output resolution DPI (default: 150)")
    parser.add_argument("--format", choices=["png", "jpg", "jpeg", "webp"], default="png", help="Output image format (default: png)")
    parser.add_argument("--pages", help="Page range, e.g. '1-5' or '3'")
    parser.add_argument("--engine", choices=["auto", "pymupdf", "pdf2image"], default="auto", help="Conversion engine")
    parser.add_argument("-q", "--quiet", action="store_true", help="Suppress progress output")

    args = parser.parse_args()

    if not args.input.exists():
        print(f"Error: File not found: {args.input}")
        sys.exit(1)

    if not args.input.suffix.lower() == ".pdf":
        print(f"Error: Input file must be a PDF: {args.input}")
        sys.exit(1)

    # Determine output directory
    if args.output:
        output_dir = args.output
    else:
        output_dir = args.input.with_name(f"{args.input.stem}_images")

    # Parse page range
    first_page = last_page = None
    if args.pages:
        if "-" in args.pages:
            parts = args.pages.split("-")
            first_page = int(parts[0]) - 1  # Convert to 0-indexed
            last_page = int(parts[1])
        else:
            first_page = last_page = int(args.pages)
            last_page = first_page + 1

    # Choose engine
    engine = args.engine
    if engine == "auto":
        try:
            import fitz
            engine = "pymupdf"
        except ImportError:
            engine = "pdf2image"

    # Convert
    if not args.quiet:
        print(f"Converting: {args.input}")
        print(f"Output: {output_dir}")
        print(f"Engine: {engine}, DPI: {args.dpi}, Format: {args.format}")

    if engine == "pymupdf":
        count = convert_with_pymupdf(args.input, output_dir, args.dpi, args.format, first_page, last_page)
    else:
        count = convert_with_pdf2image(args.input, output_dir, args.dpi, args.format, first_page, last_page)

    if not args.quiet:
        print(f"\nDone! Converted {count} page(s) to {output_dir}")


if __name__ == "__main__":
    main()
