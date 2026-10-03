#!/usr/bin/env python3
"""
Meme Generator - Create classic memes with top and bottom text
"""

import argparse
import os
from PIL import Image, ImageDraw, ImageFont

class MemeGenerator:
    """Generate memes by adding text to images"""

    def __init__(self):
        self.image = None
        self.draw = None
        self.current_image = None

    def load_image(self, image_path):
        """Load an image from file"""
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found: {image_path}")

        self.image = Image.open(image_path)
        self.current_image = self.image.copy()
        self.draw = ImageDraw.Draw(self.current_image)
        return self

    def create_meme(self, image_path, top_text="", bottom_text=""):
        """Create a meme with top and bottom text"""
        self.load_image(image_path)

        width, height = self.current_image.size

        # Calculate font size based on image width
        font_size = max(int(width / 12), 20)

        try:
            # Try to use Impact font (classic meme font)
            font = ImageFont.truetype("arial.ttf", font_size)
            if font is None:
                font = ImageFont.load_default()
        except Exception:
            try:
                # Try common font paths on Windows
                font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", font_size)
            except Exception:
                # Fall back to default font
                font = ImageFont.load_default()

        # Add top text
        if top_text:
            self._add_meme_text(top_text.upper(), height * 0.1, font)

        # Add bottom text
        if bottom_text:
            self._add_meme_text(bottom_text.upper(), height * 0.85, font)

        return self

    def _add_meme_text(self, text, y_position, font):
        """Add styled text to the image with outline effect"""
        width, _ = self.current_image.size

        # Calculate text position (centered)
        bbox = self.draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        x_position = (width - text_width) // 2

        # Draw text outline (black)
        outline_range = max(2, font.size // 20)
        for ox in range(-outline_range, outline_range + 1, 1):
            for oy in range(-outline_range, outline_range + 1, 1):
                if ox == 0 and oy == 0:
                    continue
                self.draw.text(
                    (x_position + ox, y_position + oy),
                    text,
                    font=font,
                    fill="black"
                )

        # Draw main text (white)
        self.draw.text(
            (x_position, y_position),
            text,
            font=font,
            fill="white"
        )

    def save(self, output_path):
        """Save the meme to a file"""
        if self.current_image is None:
            raise ValueError("No image loaded. Call create_meme() first.")

        self.current_image.save(output_path)
        print(f"Meme saved to: {output_path}")
        return self

    def show(self):
        """Display the meme (if supported by the platform)"""
        if self.current_image is None:
            raise ValueError("No image loaded. Call create_meme() first.")

        self.current_image.show()

def create_meme_cli(args):
    """Command-line interface for meme creation"""
    meme = MemeGenerator()

    try:
        meme.create_meme(
            image_path=args.image,
            top_text=args.top or "",
            bottom_text=args.bottom or ""
        )

        if args.output:
            meme.save(args.output)
        else:
            # Generate default output filename
            base_name = os.path.splitext(os.path.basename(args.image))[0]
            output_path = f"{base_name}_meme.png"
            meme.save(output_path)

        if args.preview:
            meme.show()

    except FileNotFoundError as e:
        print(f"Error: {e}")
        return 1
    except Exception as e:
        print(f"Error creating meme: {e}")
        return 1

    return 0

def main():
    parser = argparse.ArgumentParser(
        description="Meme Generator - Create classic memes with text",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python meme-generator.py --image photo.jpg --top "Top Text" --bottom "Bottom Text"
  python meme-generator.py -i photo.jpg -t "When you fix a bug" -b "It creates 10 more"
  python meme-generator.py --image photo.jpg -t "Top Only"
        """
    )

    parser.add_argument("-i", "--image", required=True,
                       help="Path to the input image")
    parser.add_argument("-t", "--top",
                       help="Text for the top of the meme")
    parser.add_argument("-b", "--bottom",
                       help="Text for the bottom of the meme")
    parser.add_argument("-o", "--output",
                       help="Output file path (default: <image>_meme.png)")
    parser.add_argument("-p", "--preview", action="store_true",
                       help="Preview the meme before saving")

    args = parser.parse_args()

    # Validate that at least one text option is provided
    if not args.top and not args.bottom:
        parser.error("At least one of --top or --bottom text is required")

    return create_meme_cli(args)

if __name__ == "__main__":
    exit(main())
