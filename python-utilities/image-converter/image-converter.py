"""
Image Converter - Convert images between formats (PNG/JPEG/WebP/GIF/BMP/TIFF).
Batch conversion support with quality control.
"""

import argparse
import sys
import os
from pathlib import Path
from PIL import Image


SUPPORTED_FORMATS = ['JPEG', 'PNG', 'WebP', 'GIF', 'BMP', 'TIFF', 'ICO']


def convert_image(input_path: str, output_path: str,
                  target_format: str = None, quality: int = 95,
                  optimize: bool = True, lossless: bool = False) -> dict:
    """
    Convert a single image to another format.

    Args:
        input_path: Source image path
        output_path: Destination path
        target_format: Target format (JPEG, PNG, WebP, GIF, BMP, TIFF)
        quality: Quality for lossy formats (JPEG, WebP)
        optimize: Enable optimization
        lossless: Use lossless compression (WebP)

    Returns:
        dict with conversion stats
    """
    os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
    original_bytes = os.path.getsize(input_path)

    with Image.open(input_path) as img:
        original_size = img.size
        original_mode = img.mode
        original_format = img.format

        fmt = target_format or Path(output_path).suffix.lstrip('.').upper()
        if fmt == 'JPG':
            fmt = 'JPEG'

        # Handle format-specific conversions
        if fmt == 'JPEG':
            if img.mode == 'RGBA':
                # White background for JPEG (no transparency)
                bg = Image.new('RGB', img.size, (255, 255, 255))
                bg.paste(img, mask=img.split()[3])
                img = bg
            elif img.mode != 'RGB':
                img = img.convert('RGB')
            img.save(output_path, 'JPEG', quality=quality, optimize=optimize)

        elif fmt == 'PNG':
            if img.mode == 'RGB':
                # Add alpha channel for PNG
                img = img.convert('RGBA')
            save_kwargs = {'format': 'PNG'}
            if optimize:
                save_kwargs['compress_level'] = 9
            img.save(output_path, **save_kwargs)

        elif fmt == 'WEBP':
            save_kwargs = {'format': 'WebP'}
            if lossless:
                save_kwargs['method'] = 0
            else:
                save_kwargs['quality'] = quality
                save_kwargs['method'] = 6
            if img.mode == 'RGBA':
                pass
            elif img.mode != 'RGB':
                img = img.convert('RGB')
            img.save(output_path, **save_kwargs)

        elif fmt == 'GIF':
            if img.mode != 'P':
                img = img.convert('RGB')
                img = img.quantize(colors=256, method=Image.Quantize.MEDIANCUT)
            img.save(output_path, 'GIF', optimize=optimize)

        elif fmt == 'BMP':
            if img.mode != 'RGB':
                img = img.convert('RGB')
            img.save(output_path, 'BMP')

        elif fmt == 'TIFF':
            img.save(output_path, 'TIFF', compression='tiff_lzw' if optimize else None)

        elif fmt == 'ICO':
            # ICO needs 256x256 max
            ico_img = img.copy()
            ico_img.thumbnail((256, 256), Image.Resampling.LANCZOS)
            if ico_img.mode != 'RGBA':
                ico_img = ico_img.convert('RGBA')
            ico_img.save(output_path, 'ICO')

        else:
            img.save(output_path)

    new_bytes = os.path.getsize(output_path)
    return {
        'input': input_path, 'output': output_path,
        'from': original_format or Path(input_path).suffix,
        'to': fmt,
        'original_bytes': original_bytes, 'new_bytes': new_bytes,
        'original_size': original_size,
        'ratio': round(new_bytes / original_bytes, 3) if original_bytes else 1
    }


def batch_convert(input_dir: str, output_dir: str,
                  target_format: str, quality: int = 95,
                  optimize: bool = True, lossless: bool = False,
                  suffix: str = '') -> list:
    """Convert all images in a directory to target format."""
    os.makedirs(output_dir, exist_ok=True)
    extensions = ['.jpg', '.jpeg', '.png', '.webp', '.gif', '.bmp', '.tiff', '.tif', '.ico']
    images = [f for f in os.listdir(input_dir)
              if os.path.isfile(os.path.join(input_dir, f))
              and Path(f).suffix.lower() in extensions]

    ext_map = {
        'JPEG': '.jpg', 'PNG': '.png', 'WEBP': '.webp',
        'GIF': '.gif', 'BMP': '.bmp', 'TIFF': '.tiff', 'ICO': '.ico'
    }
    out_ext = ext_map.get(target_format.upper(), '.jpg')

    results = []
    for fname in images:
        input_path = os.path.join(input_dir, fname)
        p = Path(fname)
        output_path = os.path.join(output_dir, f"{p.stem}{suffix}{out_ext}")
        try:
            result = convert_image(input_path, output_path, target_format,
                                   quality, optimize, lossless)
            results.append(result)
            print(f"  [OK] {fname} -> {Path(output_path).name} "
                  f"({result['ratio']:.1%} of original)")
        except Exception as e:
            print(f"  [FAIL] {fname}: {e}")
            results.append({'input': input_path, 'error': str(e)})
    return results


def format_bytes(num_bytes: int) -> str:
    if num_bytes < 1024:
        return f"{num_bytes}B"
    elif num_bytes < 1024 * 1024:
        return f"{num_bytes / 1024:.1f}KB"
    else:
        return f"{num_bytes / (1024 * 1024):.2f}MB"


def main():
    parser = argparse.ArgumentParser(
        description='Image Converter - Convert images between formats',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Supported formats: JPEG, PNG, WebP, GIF, BMP, TIFF, ICO

Examples:
  # Convert PNG to JPEG
  python image-converter.py -i photo.png -o photo.jpg --format JPEG

  # Convert to WebP with quality 80
  python image-converter.py -i photo.jpg -o photo.webp --format WEBP --quality 80

  # Lossless WebP
  python image-converter.py -i photo.png -o photo.webp --format WEBP --lossless

  # Batch convert directory to PNG
  python image-converter.py -i ./photos -o ./png_output --format PNG --batch

  # Batch with suffix
  python image-converter.py -i ./photos -o ./output --format JPEG --batch --suffix _converted
'''
    )
    parser.add_argument('-i', '--input', required=True, help='Input file or directory')
    parser.add_argument('-o', '--output', required=True, help='Output file or directory')
    parser.add_argument('-f', '--format', required=True,
                        choices=['JPEG', 'PNG', 'WebP', 'GIF', 'BMP', 'TIFF', 'ICO',
                                'JPG', 'jpg', 'png', 'webp', 'gif', 'bmp', 'tiff', 'ico'],
                        help='Target format')
    parser.add_argument('-q', '--quality', type=int, default=95,
                        help='Quality for JPEG/WebP 1-100 (default: 95)')
    parser.add_argument('--no-optimize', action='store_true', help='Disable optimization')
    parser.add_argument('--lossless', action='store_true',
                        help='Use lossless compression (WebP)')
    parser.add_argument('--batch', action='store_true', help='Batch process directory')
    parser.add_argument('--suffix', default='',
                        help='Suffix for output filenames (batch, default: none)')

    args = parser.parse_args()

    optimize = not args.no_optimize
    target = args.format.upper()
    if target == 'JPG':
        target = 'JPEG'

    if args.batch:
        print(f"Batch converting images from '{args.input}' to {target}...\n")
        results = batch_convert(args.input, args.output, target,
                                args.quality, optimize, args.lossless, args.suffix)
        succeeded = [r for r in results if 'error' not in r]
        if succeeded:
            total_orig = sum(r['original_bytes'] for r in succeeded)
            total_new = sum(r['new_bytes'] for r in succeeded)
            print(f"\nDone: {len(succeeded)}/{len(results)} succeeded")
            print(f"Total: {format_bytes(total_orig)} -> {format_bytes(total_new)}")
        else:
            print(f"\nDone: 0/{len(results)} succeeded")
    else:
        print(f"Converting '{args.input}' to {target}...")
        result = convert_image(args.input, args.output, target,
                              args.quality, optimize, args.lossless)
        print(f"Saved to '{args.output}'")
        print(f"  {result['from']} -> {result['to']}")
        print(f"  Size: {format_bytes(result['original_bytes'])} -> {format_bytes(result['new_bytes'])} "
              f"({result['ratio']:.1%})")


if __name__ == '__main__':
    main()
