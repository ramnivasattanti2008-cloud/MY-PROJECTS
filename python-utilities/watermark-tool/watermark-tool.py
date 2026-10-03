"""
Watermark Tool - Add text or image watermarks to images.
Supports opacity, position control, batch processing.
"""

import argparse
import sys
import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageEnhance


POSITIONS = {
    'top-left':     (0, 0),
    'top-center':   (0.5, 0),
    'top-right':    (1, 0),
    'center-left':  (0, 0.5),
    'center':       (0.5, 0.5),
    'center-right': (1, 0.5),
    'bottom-left':  (0, 1),
    'bottom-center':(0.5, 1),
    'bottom-right': (1, 1),
    'tile':         'tile',    # repeating pattern
    'stretch':      'stretch', # stretch across entire image
}

FONT_CACHE = {}


def load_font(size: int) -> ImageFont.FreeTypeFont:
    """Load a font, caching by size for performance."""
    if size not in FONT_CACHE:
        # Try common font paths on Windows
        font_paths = [
            "C:/Windows/Fonts/arial.ttf",
            "C:/Windows/Fonts/arialbd.ttf",
            "C:/Windows/Fonts/segoeui.ttf",
            "C:/Windows/Fonts/tahoma.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        ]
        for fp in font_paths:
            if os.path.exists(fp):
                FONT_CACHE[size] = ImageFont.truetype(fp, size)
                return FONT_CACHE[size]
        # Fallback to default
        FONT_CACHE[size] = ImageFont.load_default()
    return FONT_CACHE[size]


def add_text_watermark(img: Image.Image, text: str, position: str = 'bottom-right',
                        opacity: float = 0.5, font_size: int = None,
                        color: tuple = None, margin: int = 20) -> Image.Image:
    """
    Add a text watermark to an image.

    Args:
        img: PIL Image
        text: Watermark text
        position: Position name or 'tile'
        opacity: Opacity 0.0-1.0
        font_size: Font size in pixels (auto if None)
        color: RGBA color tuple (auto white if None)
        margin: Distance from edges in pixels
    """
    # Create overlay
    overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    # Auto font size based on image dimensions
    if font_size is None:
        font_size = max(16, min(img.size[0], img.size[1]) // 20)

    font = load_font(font_size)

    # Auto color
    if color is None:
        color = (255, 255, 255, int(255 * opacity))
    elif len(color) == 3:
        color = color + (int(255 * opacity),)

    if position == 'tile':
        # Tile watermark across image
        step_x = font.getlength(text) + 60
        step_y = font_size + 40
        for y in range(0, img.size[1], step_y):
            for x in range(0, img.size[0], step_x):
                draw.text((x, y), text, font=font, fill=color)
    elif position == 'stretch':
        # Draw stretched across center
        x = img.size[0] // 2
        y = img.size[1] // 2
        draw.text((x, y), text, font=font, fill=color, anchor='mm')
    else:
        # Position-based placement
        bbox = draw.textbbox((0, 0), text, font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]

        px, py = POSITIONS.get(position, POSITIONS['bottom-right'])

        if position == 'center':
            x = (img.size[0] - text_w) // 2
            y = (img.size[1] - text_h) // 2
        else:
            x = int(px * (img.size[0] - text_w - margin))
            y = int(py * (img.size[1] - text_h - margin))

        # Shadow for visibility
        shadow_color = (0, 0, 0, int(128 * opacity))
        draw.text((x + 2, y + 2), text, font=font, fill=shadow_color)
        draw.text((x, y), text, font=font, fill=color)

    # Composite onto image
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    return Image.alpha_composite(img, overlay)


def add_image_watermark(img: Image.Image, watermark_path: str, position: str = 'bottom-right',
                       opacity: float = 0.5, scale: float = 0.15,
                       margin: int = 20) -> Image.Image:
    """
    Add an image watermark to another image.

    Args:
        img: PIL Image (base)
        watermark_path: Path to watermark PNG/TGA with alpha
        position: Position name or 'tile' or 'stretch'
        opacity: Opacity 0.0-1.0
        scale: Watermark size relative to image (0.15 = 15%% of image width)
        margin: Distance from edges in pixels
    """
    with Image.open(watermark_path) as wm:
        # Scale watermark
        target_w = max(50, int(img.size[0] * scale))
        ratio = target_w / wm.size[0]
        target_h = int(wm.size[1] * ratio)
        wm = wm.resize((target_w, target_h), Image.Resampling.LANCZOS)

        # Apply opacity
        if wm.mode != 'RGBA':
            wm = wm.convert('RGBA')
        alpha = wm.split()[3]
        alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
        wm.putalpha(alpha)

        # Create overlay
        overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))

        if position == 'tile':
            step_x = wm.size[0] + 40
            step_y = wm.size[1] + 40
            for y in range(0, img.size[1], step_y):
                for x in range(0, img.size[0], step_x):
                    overlay.paste(wm, (x, y), wm)
        elif position == 'stretch':
            # Stretch watermark to fill image width at bottom
            stretched = wm.resize((img.size[0], max(10, int(img.size[1] * scale))),
                                   Image.Resampling.LANCZOS)
            overlay.paste(stretched, (0, img.size[1] - stretched.size[1]), stretched)
        else:
            px, py = POSITIONS.get(position, POSITIONS['bottom-right'])
            x = int(px * (img.size[0] - wm.size[0] - margin))
            y = int(py * (img.size[1] - wm.size[1] - margin))
            overlay.paste(wm, (x, y), wm)

        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        return Image.alpha_composite(img, overlay)


def apply_watermark(input_path: str, output_path: str,
                    text: str = None, watermark_image: str = None,
                    position: str = 'bottom-right', opacity: float = 0.5,
                    font_size: int = None, color: tuple = None,
                    scale: float = 0.15, margin: int = 20,
                    output_format: str = None) -> dict:
    """Apply watermark to a single image."""
    os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
    original_bytes = os.path.getsize(input_path)

    img = Image.open(input_path)

    if text:
        img = add_text_watermark(img, text, position, opacity, font_size, color, margin)
    elif watermark_image:
        img = add_image_watermark(img, watermark_image, position, opacity, scale, margin)
    else:
        raise ValueError("Must specify --text or --watermark-image")

    # Save
    save_path = output_path
    save_kwargs = {}
    if output_format:
        fmt = output_format.upper()
        save_kwargs['format'] = fmt
        if fmt == 'JPEG':
            save_kwargs['quality'] = 95
            save_kwargs['optimize'] = True
            img = img.convert('RGB')
    elif Path(save_path).suffix.upper() == '.JPG':
        img = img.convert('RGB')
        save_kwargs['format'] = 'JPEG'
        save_kwargs['quality'] = 95
        save_kwargs['optimize'] = True

    img.save(save_path, **save_kwargs)
    new_bytes = os.path.getsize(save_path)

    return {
        'input': input_path, 'output': save_path,
        'original_bytes': original_bytes, 'new_bytes': new_bytes,
        'type': 'text' if text else 'image',
        'opacity': opacity, 'position': position
    }


def batch_watermark(input_dir: str, output_dir: str,
                    text: str = None, watermark_image: str = None,
                    position: str = 'bottom-right', opacity: float = 0.5,
                    font_size: int = None, color: tuple = None,
                    scale: float = 0.15, margin: int = 20,
                    prefix: str = '', suffix: str = '_watermarked',
                    output_format: str = None) -> list:
    """Apply watermarks to all images in a directory."""
    os.makedirs(output_dir, exist_ok=True)
    extensions = ['.jpg', '.jpeg', '.png', '.webp', '.bmp', '.gif', '.tiff']
    images = [f for f in os.listdir(input_dir)
              if os.path.isfile(os.path.join(input_dir, f))
              and Path(f).suffix.lower() in extensions]

    results = []
    for fname in images:
        input_path = os.path.join(input_dir, fname)
        p = Path(fname)
        out_ext = output_format.lower() if output_format else p.suffix
        output_path = os.path.join(output_dir, f"{prefix}{p.stem}{suffix}{out_ext}")
        try:
            result = apply_watermark(input_path, output_path, text, watermark_image,
                                     position, opacity, font_size, color, scale, margin,
                                     output_format)
            results.append(result)
            print(f"  [OK] {fname} -> {Path(output_path).name}")
        except Exception as e:
            print(f"  [FAIL] {fname}: {e}")
            results.append({'input': input_path, 'error': str(e)})
    return results


def main():
    parser = argparse.ArgumentParser(
        description='Watermark Tool - Add text or image watermarks',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Positions: top-left, top-center, top-right, center-left, center,
           center-right, bottom-left, bottom-center, bottom-right,
           tile, stretch

Examples:
  # Text watermark bottom-right
  python watermark-tool.py -i photo.jpg -o photo_wm.jpg --text "My Company"

  # Semi-transparent text watermark center
  python watermark-tool.py -i photo.jpg -o photo_wm.jpg --text "DRAFT" \\
    --position center --opacity 0.3 --font-size 120

  # Image watermark (logo)
  python watermark-tool.py -i photo.jpg -o photo_wm.jpg \\
    --watermark-image logo.png --position bottom-right --opacity 0.4

  # Tiled text watermark
  python watermark-tool.py -i photo.jpg -o photo_wm.jpg \\
    --text "CONFIDENTIAL" --position tile --opacity 0.15 --font-size 30

  # Batch with image watermark
  python watermark-tool.py -i ./photos -o ./watermarked \\
    --text "Sample" --position bottom-center --opacity 0.5 --batch
'''
    )
    parser.add_argument('-i', '--input', required=True, help='Input image or directory')
    parser.add_argument('-o', '--output', required=True, help='Output file or directory')
    parser.add_argument('--text', help='Text watermark')
    parser.add_argument('--watermark-image', help='Image file to use as watermark')
    parser.add_argument('--position', default='bottom-right',
                        choices=list(POSITIONS.keys()),
                        help='Watermark position (default: bottom-right)')
    parser.add_argument('--opacity', type=float, default=0.5,
                        help='Opacity 0.0-1.0 (default: 0.5)')
    parser.add_argument('--font-size', type=int, help='Font size in pixels (auto if omitted)')
    parser.add_argument('--color', help='Text color as R,G,B (e.g. 255,255,255)')
    parser.add_argument('--scale', type=float, default=0.15,
                        help='Image watermark scale relative to image (default: 0.15)')
    parser.add_argument('--margin', type=int, default=20,
                        help='Margin from edges in pixels (default: 20)')
    parser.add_argument('--batch', action='store_true', help='Batch process directory')
    parser.add_argument('--prefix', default='', help='Output filename prefix (batch)')
    parser.add_argument('--suffix', default='_watermarked', help='Output suffix (batch)')
    parser.add_argument('--format', help='Output format (JPEG, PNG, WebP)')

    args = parser.parse_args()

    if not args.text and not args.watermark_image:
        parser.error('Must specify --text or --watermark-image')

    color = None
    if args.color:
        parts = args.color.split(',')
        if len(parts) == 3:
            color = tuple(int(p.strip()) for p in parts)

    if args.batch:
        print(f"Batch watermarking images from '{args.input}'...\n")
        results = batch_watermark(
            args.input, args.output,
            text=args.text, watermark_image=args.watermark_image,
            position=args.position, opacity=args.opacity,
            font_size=args.font_size, color=color,
            scale=args.scale, margin=args.margin,
            prefix=args.prefix, suffix=args.suffix,
            output_format=args.format
        )
        succeeded = sum(1 for r in results if 'error' not in r)
        print(f"\nDone: {succeeded}/{len(results)} succeeded")
    else:
        wm_type = 'Text' if args.text else 'Image'
        print(f"Adding {wm_type} watermark to '{args.input}'...")
        result = apply_watermark(
            args.input, args.output,
            text=args.text, watermark_image=args.watermark_image,
            position=args.position, opacity=args.opacity,
            font_size=args.font_size, color=color,
            scale=args.scale, margin=args.margin,
            output_format=args.format
        )
        print(f"Saved to '{args.output}'")
        print(f"  Type: {result['type']}, Position: {result['position']}, Opacity: {result['opacity']}")


if __name__ == '__main__':
    main()
