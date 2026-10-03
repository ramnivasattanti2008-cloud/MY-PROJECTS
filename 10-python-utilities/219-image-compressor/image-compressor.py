"""
Image Compressor - Reduce image file sizes with quality control.
Supports JPEG quality tuning, PNG optimization, and batch processing.
"""

import argparse
import sys
import os
from pathlib import Path
from PIL import Image


def get_image_info(path: str) -> dict:
    """Get basic image info without loading full pixels."""
    with Image.open(path) as img:
        return {
            'size': img.size,
            'mode': img.mode,
            'format': img.format,
            'bytes': os.path.getsize(path)
        }


def compress_image(input_path: str, output_path: str,
                   jpeg_quality: int = 85, png_optimize: bool = True,
                   max_width: int = None, max_height: int = None,
                   target_size_kb: int = None) -> dict:
    """
    Compress a single image.

    Args:
        input_path: Source image path
        output_path: Destination path
        jpeg_quality: JPEG quality 1-100 (default 85)
        png_optimize: Enable PNG optimization
        max_width: Resize if wider than this
        max_height: Resize if taller than this
        target_size_kb: Target file size in KB (JPEG only, iterative)

    Returns:
        dict with compression stats
    """
    os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
    original_bytes = os.path.getsize(input_path)

    with Image.open(input_path) as img:
        original_size = img.size
        original_mode = img.mode

        # Optional resize
        if max_width or max_height:
            max_w = max_width or original_size[0]
            max_h = max_height or original_size[1]
            img.thumbnail((max_w, max_h), Image.Resampling.LANCZOS)

        ext = Path(output_path).suffix.upper()

        if ext in ('.JPG', '.JPEG'):
            # JPEG compression
            if target_size_kb:
                quality = jpeg_quality
                best_quality = quality
                best_bytes = original_bytes
                step = 5

                # Binary search for target size
                for q in range(jpeg_quality, 9, -step):
                    img.save(output_path, 'JPEG', quality=q, optimize=png_optimize)
                    size = os.path.getsize(output_path)
                    if size <= target_size_kb * 1024:
                        best_quality = q
                        best_bytes = size
                        break
                    best_quality = q
                    best_bytes = size

                # Fine-tune around best quality
                for q in range(max(10, best_quality - step), min(jpeg_quality + 1, best_quality + step + 1)):
                    img.save(output_path, 'JPEG', quality=q, optimize=png_optimize)
                    size = os.path.getsize(output_path)
                    if size <= target_size_kb * 1024:
                        best_quality = q
                        best_bytes = size
                        break
                    if size < best_bytes:
                        best_quality = q
                        best_bytes = size

                quality = best_quality
                img.save(output_path, 'JPEG', quality=quality, optimize=png_optimize)
                new_bytes = os.path.getsize(output_path)
            else:
                # Convert RGBA to RGB first for smaller JPEG
                if img.mode == 'RGBA':
                    img = img.convert('RGB')
                img.save(output_path, 'JPEG', quality=jpeg_quality, optimize=png_optimize)
                new_bytes = os.path.getsize(output_path)
                quality = jpeg_quality

            compression_ratio = new_bytes / original_bytes if original_bytes else 1
            return {
                'input': input_path, 'output': output_path,
                'original_bytes': original_bytes, 'new_bytes': new_bytes,
                'ratio': round(compression_ratio, 3),
                'saved_pct': round((1 - compression_ratio) * 100, 1),
                'quality': quality, 'format': 'JPEG'
            }

        elif ext == '.PNG':
            png_level = 9 if png_optimize else 0
            if img.mode == 'P':
                img.save(output_path, 'PNG', optimize=1)
            else:
                img.save(output_path, 'PNG', compress_level=png_level)
            new_bytes = os.path.getsize(output_path)
            compression_ratio = new_bytes / original_bytes if original_bytes else 1
            return {
                'input': input_path, 'output': output_path,
                'original_bytes': original_bytes, 'new_bytes': new_bytes,
                'ratio': round(compression_ratio, 3),
                'saved_pct': round((1 - compression_ratio) * 100, 1),
                'format': 'PNG'
            }

        else:
            # WebP or other - save with default compression
            if img.mode == 'RGBA' and ext == '.WEBP':
                pass
            elif img.mode == 'RGBA' and ext not in ('.WEBP',):
                img = img.convert('RGB')
            img.save(output_path)
            new_bytes = os.path.getsize(output_path)
            compression_ratio = new_bytes / original_bytes if original_bytes else 1
            return {
                'input': input_path, 'output': output_path,
                'original_bytes': original_bytes, 'new_bytes': new_bytes,
                'ratio': round(compression_ratio, 3),
                'saved_pct': round((1 - compression_ratio) * 100, 1),
                'format': ext.lstrip('.')
            }


def batch_compress(input_dir: str, output_dir: str,
                  jpeg_quality: int = 85, png_optimize: bool = True,
                  max_width: int = None, max_height: int = None,
                  target_size_kb: int = None,
                  prefix: str = '', suffix: str = '_compressed') -> list:
    """Compress all images in a directory."""
    os.makedirs(output_dir, exist_ok=True)
    extensions = ['.jpg', '.jpeg', '.png', '.webp', '.bmp', '.gif']
    images = [f for f in os.listdir(input_dir)
              if os.path.isfile(os.path.join(input_dir, f))
              and Path(f).suffix.lower() in extensions]

    results = []
    for fname in images:
        input_path = os.path.join(input_dir, fname)
        p = Path(fname)
        output_path = os.path.join(output_dir, f"{prefix}{p.stem}{suffix}{p.suffix}")
        try:
            result = compress_image(input_path, output_path, jpeg_quality,
                                    png_optimize, max_width, max_height, target_size_kb)
            results.append(result)
            print(f"  [OK] {fname}: {result['new_bytes']//1024}KB "
                  f"({result['saved_pct']:.1f}% saved)")
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
        description='Image Compressor - Reduce image file sizes',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Compress JPEG to quality 75
  python image-compressor.py -i photo.jpg -o photo_small.jpg --quality 75

  # Compress PNG with optimization
  python image-compressor.py -i image.png -o image_opt.png --png-optimize

  # Target max file size (500KB)
  python image-compressor.py -i photo.jpg -o photo_500kb.jpg --target-kb 500

  # Batch compress directory
  python image-compressor.py -i ./photos -o ./compressed --quality 80 --batch

  # Compress and resize to max 1920px wide
  python image-compressor.py -i photo.jpg -o photo_opt.jpg --max-width 1920 --quality 85
'''
    )
    parser.add_argument('-i', '--input', required=True, help='Input file or directory')
    parser.add_argument('-o', '--output', required=True, help='Output file or directory')
    parser.add_argument('-q', '--quality', type=int, default=85,
                        help='JPEG quality 1-100 (default: 85)')
    parser.add_argument('--png-optimize', action='store_true',
                        help='Enable PNG optimization (compress level 9)')
    parser.add_argument('--no-png-optimize', action='store_true',
                        help='Disable PNG optimization')
    parser.add_argument('--max-width', type=int, help='Max width in pixels (resize if larger)')
    parser.add_argument('--max-height', type=int, help='Max height in pixels (resize if larger)')
    parser.add_argument('--target-kb', type=int,
                        help='Target file size in KB (JPEG only, iterative quality search)')
    parser.add_argument('--batch', action='store_true', help='Batch process directory')
    parser.add_argument('--prefix', default='', help='Output filename prefix (batch)')
    parser.add_argument('--suffix', default='_compressed', help='Output filename suffix (batch)')

    args = parser.parse_args()

    if args.no_png_optimize:
        png_optimize = False
    else:
        png_optimize = args.png_optimize

    if args.batch:
        print(f"Batch compressing images from '{args.input}'...\n")
        results = batch_compress(args.input, args.output, args.quality, png_optimize,
                                 args.max_width, args.max_height, args.target_kb,
                                 args.prefix, args.suffix)
        succeeded = [r for r in results if 'error' not in r]
        if succeeded:
            total_orig = sum(r['original_bytes'] for r in succeeded)
            total_new = sum(r['new_bytes'] for r in succeeded)
            total_saved = (1 - total_new / total_orig) * 100 if total_orig else 0
            print(f"\nDone: {len(succeeded)}/{len(results)} succeeded")
            print(f"Total: {format_bytes(total_orig)} -> {format_bytes(total_new)} "
                  f"({total_saved:.1f}% saved)")
    else:
        print(f"Compressing '{args.input}'...")
        info = get_image_info(args.input)
        print(f"  Input: {info['size'][0]}x{info['size'][1]}, "
              f"{info['format']}, {format_bytes(info['bytes'])}")

        result = compress_image(args.input, args.output, args.quality,
                                png_optimize, args.max_width, args.max_height,
                                args.target_kb)

        print(f"Saved to '{args.output}'")
        print(f"  Output size: {format_bytes(result['new_bytes'])}")
        print(f"  Saved: {result['saved_pct']:.1f}% ({result['ratio']:.1%} of original)")
        if 'quality' in result:
            print(f"  Quality: {result['quality']}")


if __name__ == '__main__':
    main()
