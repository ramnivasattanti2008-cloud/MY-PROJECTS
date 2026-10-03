#!/usr/bin/env python3
"""
Image Resizer - Resize images to different dimensions with batch support.

Usage:
    Single file:    python image-resizer.py input.jpg --width 800 --height 600
    Batch mode:     python image-resizer.py input1.jpg input2.jpg --width 800
    Directory:      python image-resizer.py /path/to/images/ --width 800
    Maintain ratio: python image-resizer.py input.jpg --width 800 --keep-ratio
    Scale percent:  python image-resizer.py input.jpg --scale 50
    Output dir:     python image-resizer.py input.jpg -o output/
"""

import argparse
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from PIL import Image


@dataclass
class ResizeResult:
    """Stores the result of resizing an image."""
    input_path: str
    output_path: str
    original_size: tuple[int, int]
    new_size: tuple[int, int]
    success: bool
    error: Optional[str] = None


# Supported image formats
SUPPORTED_FORMATS = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp"}


def validate_image(path: str) -> bool:
    """Check if file is a valid image."""
    path_obj = Path(path)
    return path_obj.exists() and path_obj.suffix.lower() in SUPPORTED_FORMATS


def get_image_info(path: str) -> Optional[tuple[int, int, str]]:
    """
    Get image dimensions and format.

    Returns:
        Tuple of (width, height, format) or None
    """
    try:
        with Image.open(path) as img:
            return (img.width, img.height, img.format)
    except Exception:
        return None


def resize_image(
    input_path: str,
    output_path: str,
    width: Optional[int] = None,
    height: Optional[int] = None,
    keep_ratio: bool = False,
    scale_percent: Optional[int] = None,
    quality: int = 95,
    output_format: Optional[str] = None,
) -> ResizeResult:
    """
    Resize an image file.

    Args:
        input_path: Path to input image
        output_path: Path for output image
        width: Target width (None to calculate from ratio)
        height: Target height (None to calculate from ratio)
        keep_ratio: Maintain aspect ratio
        scale_percent: Scale by percentage (overrides width/height)
        quality: JPEG quality (1-100)
        output_format: Output format (JPEG, PNG, etc.)

    Returns:
        ResizeResult with operation details
    """
    try:
        with Image.open(input_path) as img:
            original_size = (img.width, img.height)

            # Determine new size
            if scale_percent is not None:
                new_width = int(img.width * scale_percent / 100)
                new_height = int(img.height * scale_percent / 100)
            elif keep_ratio and (width or height):
                # Calculate size maintaining aspect ratio
                if width and height:
                    # Fit to bounding box
                    ratio_w = width / img.width
                    ratio_h = height / img.height
                    ratio = min(ratio_w, ratio_h)
                elif width:
                    ratio = width / img.width
                else:
                    ratio = height / img.height
                new_width = int(img.width * ratio)
                new_height = int(img.height * ratio)
            else:
                new_width = width or img.width
                new_height = height or img.height

            # Ensure dimensions are valid
            new_width = max(1, new_width)
            new_height = max(1, new_height)

            # Convert palette images to RGB for JPEG
            if output_format == "JPEG" and img.mode in ("P", "LA", "RGBA"):
                img = img.convert("RGB")

            # Resize image
            resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

            # Determine output format
            if output_format:
                output_format = output_format.upper()
            elif output_path.lower().endswith(".png"):
                output_format = "PNG"
            elif output_path.lower().endswith((".jpg", ".jpeg")):
                output_format = "JPEG"
            elif output_path.lower().endswith(".webp"):
                output_format = "WEBP"
            elif output_path.lower().endswith(".gif"):
                output_format = "GIF"
            else:
                output_format = img.format or "PNG"

            # Prepare save parameters
            save_kwargs = {}
            if output_format == "JPEG":
                save_kwargs["quality"] = quality
                save_kwargs["optimize"] = True
            elif output_format == "PNG":
                save_kwargs["optimize"] = True

            # Create output directory if needed
            output_dir = os.path.dirname(output_path)
            if output_dir:
                os.makedirs(output_dir, exist_ok=True)

            # Save image
            resized.save(output_path, format=output_format, **save_kwargs)

            return ResizeResult(
                input_path=input_path,
                output_path=output_path,
                original_size=original_size,
                new_size=(new_width, new_height),
                success=True,
            )

    except Exception as e:
        return ResizeResult(
            input_path=input_path,
            output_path=output_path,
            original_size=(0, 0),
            new_size=(0, 0),
            success=False,
            error=str(e),
        )


def find_images(path: str) -> list[str]:
    """Find all image files in a path (file or directory)."""
    images = []
    path_obj = Path(path)

    if path_obj.is_file() and path_obj.suffix.lower() in SUPPORTED_FORMATS:
        images.append(str(path_obj))
    elif path_obj.is_dir():
        for ext in SUPPORTED_FORMATS:
            images.extend(str(p) for p in path_obj.rglob(f"*{ext}"))

    return images


def generate_output_path(input_path: str, output_dir: Optional[str], suffix: str = "_resized") -> str:
    """Generate output path for an image."""
    path = Path(input_path)
    stem = path.stem
    ext = path.suffix.lower()

    if output_dir:
        return os.path.join(output_dir, f"{stem}{suffix}{ext}")
    else:
        return str(path.parent / f"{stem}{suffix}{ext}")


def format_size(size: tuple[int, int]) -> str:
    """Format dimensions as string."""
    return f"{size[0]}x{size[1]}"


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Resize images to different dimensions with batch support",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "inputs",
        nargs="*",
        help="Image file(s) or directory containing images",
    )
    parser.add_argument(
        "--width", "-w",
        type=int,
        help="Target width in pixels",
    )
    parser.add_argument(
        "--height", "-h",
        type=int,
        help="Target height in pixels",
    )
    parser.add_argument(
        "--keep-ratio", "-k",
        action="store_true",
        help="Maintain aspect ratio",
    )
    parser.add_argument(
        "--scale", "-s",
        type=int,
        help="Scale by percentage (e.g., 50 for half size)",
    )
    parser.add_argument(
        "--quality", "-q",
        type=int,
        default=95,
        help="JPEG quality 1-100 (default: 95)",
    )
    parser.add_argument(
        "--output", "-o",
        help="Output file or directory",
    )
    parser.add_argument(
        "--suffix",
        default="_resized",
        help="Suffix for output files (default: _resized)",
    )
    parser.add_argument(
        "--format",
        choices=["JPEG", "PNG", "WEBP", "GIF"],
        help="Output format (default: same as input)",
    )
    parser.add_argument(
        "--quiet", "-Q",
        action="store_true",
        help="Suppress output except errors",
    )

    args = parser.parse_args()

    # Validate arguments
    if not any([args.width, args.height, args.scale]):
        parser.print_help()
        print("\n  Error: Must specify --width, --height, or --scale")
        print("  Example: python image-resizer.py photo.jpg --width 800")
        return 1

    if args.scale and (args.scale < 1 or args.scale > 500):
        print("Error: Scale must be between 1 and 500", file=sys.stderr)
        return 1

    # Get image files
    if not args.inputs:
        parser.print_help()
        print("\n  Example: python image-resizer.py photo.jpg --width 800")
        return 1

    image_files = []
    for path in args.inputs:
        image_files.extend(find_images(path))

    if not image_files:
        print(f"Error: No images found in: {args.inputs}", file=sys.stderr)
        return 1

    if not args.quiet:
        print(f"Found {len(image_files)} image(s) to resize")

    # Determine output directory
    output_dir = None
    if args.output and os.path.isdir(args.output):
        output_dir = args.output

    # Process images
    results = []
    for i, input_path in enumerate(image_files, 1):
        # Generate output path
        if output_dir:
            output_path = generate_output_path(input_path, output_dir, args.suffix)
        elif args.output:
            output_path = args.output
        else:
            output_path = generate_output_path(input_path, None, args.suffix)

        if not args.quiet:
            print(f"[{i}/{len(image_files)}] Resizing: {input_path}")

        result = resize_image(
            input_path=input_path,
            output_path=output_path,
            width=args.width,
            height=args.height,
            keep_ratio=args.keep_ratio,
            scale_percent=args.scale,
            quality=args.quality,
            output_format=args.format,
        )
        results.append(result)

        if result.success and not args.quiet:
            print(f"  {format_size(result.original_size)} -> {format_size(result.new_size)} -> {output_path}")
        elif not result.success:
            print(f"  ERROR: {result.error}", file=sys.stderr)

    # Summary
    success_count = sum(1 for r in results if r.success)
    if not args.quiet:
        print(f"\nCompleted: {success_count}/{len(results)} images resized successfully")

    return 0 if success_count == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())
