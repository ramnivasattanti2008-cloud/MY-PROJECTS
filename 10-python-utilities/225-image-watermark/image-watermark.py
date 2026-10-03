#!/usr/bin/env python3
"""
Image Watermark Tool
Add text or image watermarks to images with position control.
"""

import argparse
import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


class WatermarkTool:
    """Watermark application tool for images."""

    POSITIONS = {
        'top-left': (10, 10),
        'top-center': ('center', 10),
        'top-right': ('right', 10),
        'center-left': (10, 'center'),
        'center': ('center', 'center'),
        'center-right': ('right', 'center'),
        'bottom-left': (10, 'bottom'),
        'bottom-center': ('center', 'bottom'),
        'bottom-right': ('right', 'bottom'),
    }

    def __init__(self):
        self.supported_formats = ['.png', '.jpg', '.jpeg', '.bmp', '.webp', '.tiff']

    def calculate_position(self, img_width, img_height, wm_width, wm_height, position):
        """Calculate watermark position based on anchor."""
        anchor = self.POSITIONS.get(position, self.POSITIONS['bottom-right'])

        x_anchor, y_anchor = anchor

        if x_anchor == 'center':
            x = (img_width - wm_width) // 2
        elif x_anchor == 'right':
            x = img_width - wm_width - 10
        else:
            x = x_anchor

        if y_anchor == 'center':
            y = (img_height - wm_height) // 2
        elif y_anchor == 'bottom':
            y = img_height - wm_height - 10
        else:
            y = y_anchor

        return x, y

    def add_text_watermark(self, image_path, output_path, text, position='bottom-right',
                           font_size=36, color=(255, 255, 255, 128), opacity=128):
        """Add text watermark to an image."""
        img = Image.open(image_path).convert('RGBA')
        overlay = Image.new('RGBA', img.size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(overlay)

        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()

        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        x, y = self.calculate_position(
            img.width, img.height, text_width, text_height, position
        )

        color = (*color[:3], opacity)
        draw.text((x, y), text, font=font, fill=color)

        watermarked = Image.alpha_composite(img, overlay)

        if watermarked.mode == 'RGBA':
            watermarked = watermarked.convert('RGB')

        watermarked.save(output_path, quality=95)
        return output_path

    def add_image_watermark(self, image_path, watermark_path, output_path, position='bottom-right',
                            opacity=128, scale=0.2):
        """Add image watermark to an image."""
        img = Image.open(image_path).convert('RGBA')
        wm = Image.open(watermark_path).convert('RGBA')

        wm_width = int(img.width * scale)
        wm_height = int(wm_width * wm.width / wm.height)
        wm = wm.resize((wm_width, wm_height), Image.Resampling.LANCZOS)

        mask = Image.new('L', wm.size, opacity)
        wm.putalpha(mask)

        x, y = self.calculate_position(
            img.width, img.height, wm_width, wm_height, position
        )

        overlay = Image.new('RGBA', img.size, (255, 255, 255, 0))
        overlay.paste(wm, (x, y), wm)

        watermarked = Image.alpha_composite(img, overlay)

        if watermarked.mode == 'RGBA':
            watermarked = watermarked.convert('RGB')

        watermarked.save(output_path, quality=95)
        return output_path

    def batch_watermark(self, input_dir, output_dir, text=None, watermark_path=None,
                        position='bottom-right', **kwargs):
        """Apply watermarks to all images in a directory."""
        input_dir = Path(input_dir)
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        files = []
        for fmt in self.supported_formats:
            files.extend(input_dir.glob(f'*{fmt}'))
            files.extend(input_dir.glob(f'*{fmt.upper()}'))

        results = []
        for file in files:
            output_file = output_dir / file.name
            try:
                if text:
                    self.add_text_watermark(file, output_file, text, position, **kwargs)
                elif watermark_path:
                    self.add_image_watermark(file, watermark_path, output_file, position, **kwargs)
                results.append((str(file), str(output_file), 'Success'))
            except Exception as e:
                results.append((str(file), str(output_file), f'Error: {e}'))

        return results


def main():
    parser = argparse.ArgumentParser(
        description='Add watermark to images - text or image overlay with position control',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python image-watermark.py -i photo.jpg -o watermarked.jpg -t "Copyright 2024" -p bottom-right
  python image-watermark.py -i photo.jpg -o watermarked.jpg -w logo.png -p center
  python image-watermark.py -i photos/ -o output/ -t "Draft" --opacity 80 --font-size 48
        """
    )

    parser.add_argument('-i', '--input', required=True, help='Input image file or directory')
    parser.add_argument('-o', '--output', required=True, help='Output file or directory')
    parser.add_argument('-t', '--text', help='Text watermark')
    parser.add_argument('-w', '--watermark', help='Image watermark file')
    parser.add_argument('-p', '--position', default='bottom-right',
                        choices=['top-left', 'top-center', 'top-right',
                                'center-left', 'center', 'center-right',
                                'bottom-left', 'bottom-center', 'bottom-right'],
                        help='Watermark position (default: bottom-right)')
    parser.add_argument('--font-size', type=int, default=36, help='Font size for text watermark')
    parser.add_argument('--color', default='255,255,255', help='Text color as R,G,B (default: 255,255,255)')
    parser.add_argument('--opacity', type=int, default=128, help='Watermark opacity 0-255 (default: 128)')
    parser.add_argument('--scale', type=float, default=0.2, help='Image watermark scale (default: 0.2)')

    args = parser.parse_args()

    tool = WatermarkTool()

    color = tuple(int(c) for c in args.color.split(','))

    if os.path.isdir(args.input):
        results = tool.batch_watermark(
            args.input, args.output,
            text=args.text, watermark_path=args.watermark,
            position=args.position,
            font_size=args.font_size,
            color=color,
            opacity=args.opacity,
            scale=args.scale
        )
        print(f"\nProcessed {len(results)} images:")
        for input_file, output_file, status in results:
            print(f"  {status}: {input_file} -> {output_file}")
    else:
        if args.text:
            output = tool.add_text_watermark(
                args.input, args.output, args.text,
                position=args.position,
                font_size=args.font_size,
                color=color,
                opacity=args.opacity
            )
        elif args.watermark:
            output = tool.add_image_watermark(
                args.input, args.watermark, args.output,
                position=args.position,
                opacity=args.opacity,
                scale=args.scale
            )
        else:
            parser.error('Either --text or --watermark must be specified')
            return

        print(f"Watermarked image saved to: {output}")


if __name__ == '__main__':
    main()
