#!/usr/bin/env python3
"""
PDF Watermark Tool
Add text or image watermarks to PDF documents.
"""

import argparse
import os
import sys
from pathlib import Path

try:
    from PyPDF2 import PdfReader, PdfWriter
    from PyPDF2.errors import PdfReadError
except ImportError:
    print("Error: PyPDF2 is required. Install with: pip install PyPDF2")
    sys.exit(1)


def add_text_watermark(
    input_path: str,
    output_path: str,
    text: str,
    font_size: int = 40,
    opacity: float = 0.3,
    rotation: int = 45,
    color: tuple = (128, 128, 128),
    pages: str = "all"
) -> None:
    """Add text watermark to PDF."""
    try:
        reader = PdfReader(input_path)
        writer = PdfWriter()

        for page_num, page in enumerate(reader.pages):
            if pages != "all" and str(page_num + 1) not in pages.split(","):
                writer.add_page(page)
                continue

            page.merge_page(
                _create_text_watermark_page(page, text, font_size, opacity, rotation, color)
            )
            writer.add_page(page)

        with open(output_path, "wb") as f:
            writer.write(f)

        print(f"Watermark added successfully: {output_path}")
    except PdfReadError as e:
        print(f"Error reading PDF: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


def _create_text_watermark_page(page, text: str, font_size: int, opacity: float, rotation: int, color: tuple):
    """Create a watermark overlay page."""
    from PyPDF2.generic import (
        NameObject, ArrayObject, DecimalObject,
        BooleanObject, TextStringObject
    )

    # Get page dimensions
    media_box = page.mediabox
    width = float(media_box.width)
    height = float(media_box.height)

    # Create watermark canvas using reportlab
    try:
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter
        from io import BytesIO
        import reportlab

        # Calculate page size tuple
        page_size = (width, height)

        packet = BytesIO()
        c = canvas.Canvas(packet, pagesize=page_size)

        # Set transparency
        c.setFillAlpha(opacity)
        c.setStrokeAlpha(opacity)

        # Set color
        r, g, b = [x / 255 for x in color]
        c.setFillColorRGB(r, g, b)

        # Set font
        c.setFont("Helvetica", font_size)

        # Draw text centered and rotated
        c.saveState()
        c.translate(width / 2, height / 2)
        c.rotate(rotation)
        c.drawCentredString(0, 0, text)
        c.restoreState()

        c.save()
        packet.seek(0)

        watermark_reader = PdfReader(packet)
        return watermark_reader.pages[0]

    except ImportError:
        print("Error: reportlab is required for text watermarks. Install with: pip install reportlab")
        sys.exit(1)


def add_image_watermark(
    input_path: str,
    output_path: str,
    image_path: str,
    opacity: float = 0.3,
    scale: float = 1.0,
    position: str = "center",
    pages: str = "all"
) -> None:
    """Add image watermark to PDF."""
    try:
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter
        from PIL import Image as PILImage
        from io import BytesIO
        from PyPDF2 import PdfReader, PdfWriter

        reader = PdfReader(input_path)
        writer = PdfWriter()

        # Get image dimensions
        with PILImage.open(image_path) as img:
            img_width, img_height = img.size

        for page_num, page in enumerate(reader.pages):
            if pages != "all" and str(page_num + 1) not in pages.split(","):
                writer.add_page(page)
                continue

            media_box = page.mediabox
            width = float(media_box.width)
            height = float(media_box.height)

            # Calculate scaled dimensions
            scaled_width = img_width * scale
            scaled_height = img_height * scale

            # Calculate position
            if position == "center":
                x = (width - scaled_width) / 2
                y = (height - scaled_height) / 2
            elif position == "top":
                x = (width - scaled_width) / 2
                y = height - scaled_height - 50
            elif position == "bottom":
                x = (width - scaled_width) / 2
                y = 50
            elif position == "top-left":
                x = 50
                y = height - scaled_height - 50
            elif position == "top-right":
                x = width - scaled_width - 50
                y = height - scaled_height - 50
            elif position == "bottom-left":
                x = 50
                y = 50
            elif position == "bottom-right":
                x = width - scaled_width - 50
                y = 50
            else:
                x = (width - scaled_width) / 2
                y = (height - scaled_height) / 2

            # Create overlay
            packet = BytesIO()
            c = canvas.Canvas(packet, pagesize=(width, height))
            c.drawImage(image_path, x, y, width=scaled_width, height=scaled_height, mask='auto')
            c.save()
            packet.seek(0)

            watermark_reader = PdfReader(packet)
            page.merge_page(watermark_reader.pages[0])
            writer.add_page(page)

        with open(output_path, "wb") as f:
            writer.write(f)

        print(f"Image watermark added successfully: {output_path}")

    except ImportError as e:
        print(f"Error: Missing dependency - {e}")
        print("Install required: pip install reportlab Pillow")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Add watermark (text or image) to PDF documents",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Add text watermark
  python pdf-watermark.py input.pdf output.pdf -t "CONFIDENTIAL"

  # Add image watermark
  python pdf-watermark.py input.pdf output.pdf -i logo.png

  # Text watermark with custom options
  python pdf-watermark.py input.pdf output.pdf -t "DRAFT" --font-size 60 --opacity 0.2 --rotation -30

  # Image watermark positioned at top-right
  python pdf-watermark.py input.pdf output.pdf -i logo.png --position top-right --scale 0.5
        """
    )

    parser.add_argument("input", help="Input PDF file path")
    parser.add_argument("output", help="Output PDF file path")
    parser.add_argument("-t", "--text", help="Text watermark")
    parser.add_argument("-i", "--image", help="Image file for watermark (PNG/JPG)")
    parser.add_argument("--font-size", type=int, default=40, help="Font size for text watermark (default: 40)")
    parser.add_argument("--opacity", type=float, default=0.3, help="Opacity 0.0-1.0 (default: 0.3)")
    parser.add_argument("--rotation", type=int, default=45, help="Rotation angle in degrees (default: 45)")
    parser.add_argument("--color", default="808080", help="Hex color code (default: 808080)")
    parser.add_argument("--position", default="center", choices=["center", "top", "bottom", "top-left", "top-right", "bottom-left", "bottom-right"], help="Image position (default: center)")
    parser.add_argument("--scale", type=float, default=1.0, help="Image scale factor (default: 1.0)")
    parser.add_argument("--pages", default="all", help="Pages to watermark (comma-separated or 'all', default: all)")

    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"Error: Input file not found: {args.input}")
        sys.exit(1)

    if args.image and not os.path.exists(args.image):
        print(f"Error: Image file not found: {args.image}")
        sys.exit(1)

    if not args.text and not args.image:
        print("Error: Either --text or --image must be specified")
        sys.exit(1)

    if args.text and args.image:
        print("Error: Specify either --text or --image, not both")
        sys.exit(1)

    # Parse color
    color = tuple(int(args.color[i:i+2], 16) for i in (0, 2, 4))

    if args.text:
        add_text_watermark(
            args.input, args.output, args.text,
            font_size=args.font_size, opacity=args.opacity,
            rotation=args.rotation, color=color, pages=args.pages
        )
    else:
        add_image_watermark(
            args.input, args.output, args.image,
            opacity=args.opacity, scale=args.scale,
            position=args.position, pages=args.pages
        )


if __name__ == "__main__":
    main()
