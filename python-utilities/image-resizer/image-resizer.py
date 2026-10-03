"""
Image Resizer - Batch resize images with width/height/percentage control.
Supports JPEG, PNG, WebP, and more.
"""

import argparse
import sys
from pathlib import Path
from PIL import Image
import os


def resize_image(input_path: str, output_path: str, width: int = None, height: int = None,
                 percentage: float = None, maintain_aspect: bool = True,
                 output_format: str = None) -> dict:
    """
    Resize a single image.

    Args:
        input_path: Path to input image
        output_path: Path to save resized image
        width: Target width in pixels
        height: Target height in pixels
        percentage: Resize by percentage (0-100 scale: 50 = half size)
        maintain_aspect: Keep aspect ratio if True
        output_format: Force output format (JPEG/PNG/WebP/etc)

    Returns:
        dict with resize info
    """
    with Image.open(input_path) as img:
        original_size = img.size
        original_mode = img.mode

        # Determine target size
        if percentage is not None:
            w = int(original_size[0] * percentage / 100)
            h = int(original_size[1] * percentage / 100)
            target_size = (w, h)
        elif width is not None or height is not None:
            w = width if width is not None else original_size[0]
            h = height if height is not None else original_size[1]
            if maintain_aspect:
                img.thumbnail((w, h), Image.Resampling.LANCZOS)
                target_size = img.size
            else:
                target_size = (w, h)
                img = img.resize(target_size, Image.Resampling.LANCZOS)
        else:
            raise ValueError("Must specify width, height, or percentage")

        if maintain_aspect and percentage is None:
            pass  # thumbnail already handled
        elif maintain_aspect and percentage is not None:
            img = img.resize(target_size, Image.Resampling.LANCZOS)

        # Convert RGBA to RGB for JPEG
        if output_format and output_format.upper() in ('JPEG', 'JPG') and img.mode == 'RGBA':
            img = img.convert('RGB')

        # Save
        save_kwargs = {}
        if output_format:
            save_kwargs['format'] = output_format.upper()
        elif Path(output_path).suffix.upper() == '.JPG':
            save_kwargs['format'] = 'JPEG'

        if save_kwargs.get('format') == 'JPEG':
            save_kwargs['quality'] = 95
            save_kwargs['optimize'] = True

        os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
        img.save(output_path, **save_kwargs)

        new_size = img.size
        original_size_bytes = os.path.getsize(input_path)
        new_size_bytes = os.path.getsize(output_path)

        return {
            'input': input_path,
            'output': output_path,
            'original_size': original_size,
            'new_size': new_size,
            'original_bytes': original_size_bytes,
            'new_bytes': new_size_bytes,
            'compression_ratio': round(new_size_bytes / original_size_bytes, 3) if original_size_bytes else 1
        }


def batch_resize(input_paths: list, output_dir: str, width: int = None, height: int = None,
                 percentage: float = None, maintain_aspect: bool = True,
                 output_format: str = None, prefix: str = '', suffix: str = '_resized') -> list:
    """
    Resize multiple images and save to output directory.
    """
    os.makedirs(output_dir, exist_ok=True)
    results = []
    for input_path in input_paths:
        p = Path(input_path)
        stem = p.stem
        ext = p.suffix
        output_name = f"{prefix}{stem}{suffix}{ext}"
        output_path = os.path.join(output_dir, output_name)
        try:
            result = resize_image(
                input_path, output_path, width, height, percentage,
                maintain_aspect, output_format
            )
            results.append(result)
            print(f"  [OK] {p.name} -> {result['new_size'][0]}x{result['new_size'][1]} "
                  f"({result['compression_ratio']:.1%} of original size)")
        except Exception as e:
            print(f"  [FAIL] {p.name}: {e}")
            results.append({'input': input_path, 'error': str(e)})
    return results


def discover_images(directory: str, recursive: bool = False, extensions: list = None) -> list:
    """Find all image files in a directory."""
    if extensions is None:
        extensions = ['.jpg', '.jpeg', '.png', '.webp', '.bmp', '.gif', '.tiff', '.tif']
    ext_set = set(ext.lower() for ext in extensions)
    paths = []
    if recursive:
        for root, _, files in os.walk(directory):
            for f in files:
                if Path(f).suffix.lower() in ext_set:
                    paths.append(os.path.join(root, f))
    else:
        for f in os.listdir(directory):
            full = os.path.join(directory, f)
            if os.path.isfile(full) and Path(f).suffix.lower() in ext_set:
                paths.append(full)
    return sorted(paths)


def main():
    parser = argparse.ArgumentParser(
        description='Image Resizer - Resize images by width, height, or percentage',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Resize single image to 800px width, maintain aspect
  python image-resizer.py -i photo.jpg -o photo_800.jpg --width 800

  # Resize to 50%% of original
  python image-resizer.py -i photo.jpg -o photo_half.jpg --percentage 50

  # Batch resize directory to 1024px width
  python image-resizer.py -i ./photos -o ./output --width 1024 --batch

  # Batch resize with prefix/suffix
  python image-resizer.py -i ./photos -o ./output --width 800 --batch --prefix thumb_ --suffix _800
'''
    )
    parser.add_argument('-i', '--input', required=True, help='Input image file or directory')
    parser.add_argument('-o', '--output', required=True, help='Output file or directory')
    parser.add_argument('--width', type=int, help='Target width in pixels')
    parser.add_argument('--height', type=int, help='Target height in pixels')
    parser.add_argument('--percentage', type=float, help='Resize by percentage (e.g. 50 = half size)')
    parser.add_argument('--no-aspect', action='store_true', help='Do NOT maintain aspect ratio')
    parser.add_argument('--batch', action='store_true', help='Batch process directory')
    parser.add_argument('-r', '--recursive', action='store_true', help='Recurse into subdirectories (batch mode)')
    parser.add_argument('--prefix', default='', help='Prefix for output filenames (batch mode)')
    parser.add_argument('--suffix', default='_resized', help='Suffix for output filenames (batch mode, default: _resized)')
    parser.add_argument('--format', help='Output format (JPEG, PNG, WebP, etc.)')

    args = parser.parse_args()

    if not any([args.width, args.height, args.percentage]):
        parser.error('Must specify --width, --height, or --percentage')

    maintain_aspect = not args.no_aspect

    if args.batch:
        images = discover_images(args.input, args.recursive)
        if not images:
            print(f"No images found in '{args.input}'")
            sys.exit(1)
        print(f"Batch resizing {len(images)} image(s)...\n")
        results = batch_resize(
            images, args.output,
            width=args.width, height=args.height,
            percentage=args.percentage,
            maintain_aspect=maintain_aspect,
            output_format=args.format,
            prefix=args.prefix, suffix=args.suffix
        )
        succeeded = sum(1 for r in results if 'error' not in r)
        print(f"\nDone: {succeeded}/{len(results)} succeeded")
    else:
        print(f"Resizing '{args.input}'...")
        result = resize_image(
            args.input, args.output,
            width=args.width, height=args.height,
            percentage=args.percentage,
            maintain_aspect=maintain_aspect,
            output_format=args.format
        )
        print(f"Saved to '{args.output}'")
        print(f"  Original size: {result['original_size'][0]}x{result['original_size'][1]}")
        print(f"  New size:      {result['new_size'][0]}x{result['new_size'][1]}")
        print(f"  Size ratio:    {result['compression_ratio']:.1%} of original")


if __name__ == '__main__':
    main()
