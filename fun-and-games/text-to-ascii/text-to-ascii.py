#!/usr/bin/env python3
"""
Image to ASCII Art Converter
Transform images into beautiful ASCII art representations
"""

import argparse
import os
import sys

try:
    from PIL import Image
except ImportError:
    print("Error: Pillow not installed.")
    print("Run: pip install -r requirements.txt")
    sys.exit(1)

# Predefined character sets
CHAR_SETS = {
    "simple": " .:-=+*#%@",
    "standard": " .'-:^+!rc*?zLsLT4JU0|",
    "detailed": " .',:;!|\\(){}[]~*rz?tycxlcJU0OZXYI5SHVNM&8%B#@$",
    "blocks": " ░▒▓█",
    "binary": "01",
    "arrows": " ▁▂▃▄▅▆▇█▇▆▅▄▃▂▁",
    "circles": " ·:;+xX$@#",
    "extended": " .·:;'+xXnnoO0OKXYYII5SVUNMRBZ/?<>()|▓▒░",
}

class ImageToASCII:
    """Convert images to ASCII art"""

    def __init__(self):
        self.image = None
        self.image_path = None
        self.width = 100
        self.height = 0
        self.chars = CHAR_SETS["standard"]

    def load_image(self, image_path: str):
        """Load an image from file"""
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found: {image_path}")

        self.image_path = image_path
        self.image = Image.open(image_path)
        return self

    def set_characters(self, chars: str):
        """Set the character set for conversion"""
        self.chars = chars
        return self

    def set_width(self, width: int):
        """Set the output width in characters"""
        self.width = width
        return self

    def _resize_image(self):
        """Resize image maintaining aspect ratio"""
        # Calculate new height based on aspect ratio
        # ASCII characters are typically taller than wide
        aspect_ratio = self.image.height / self.image.width
        self.height = int(self.width * aspect_ratio * 0.5)

        # Resize the image
        resized = self.image.resize((self.width, self.height), Image.Resampling.LANCZOS)
        return resized.convert('L')  # Convert to grayscale

    def convert(self, width: int = None, chars: str = None) -> str:
        """Convert image to ASCII art string"""
        if self.image is None:
            raise ValueError("No image loaded. Call load_image() first.")

        if width:
            self.width = width
        if chars:
            self.chars = chars

        # Resize and convert to grayscale
        gray_image = self._resize_image()
        pixels = list(gray_image.getdata())

        # Convert pixels to ASCII characters
        ascii_lines = []
        for y in range(self.height):
            line = []
            for x in range(self.width):
                pixel_index = y * self.width + x
                pixel_value = pixels[pixel_index]

                # Map pixel value to character
                char_index = int((pixel_value / 255) * (len(self.chars) - 1))
                char = self.chars[char_index]
                line.append(char)

            ascii_lines.append(''.join(line))

        return '\n'.join(ascii_lines)

    def convert_color(self, width: int = None, chars: str = None) -> list:
        """Convert image to colored ASCII art (returns list of tuples)"""
        if self.image is None:
            raise ValueError("No image loaded. Call load_image() first.")

        if width:
            self.width = width
        if chars:
            self.chars = chars

        # Resize while keeping color
        aspect_ratio = self.image.height / self.image.width
        height = int(self.width * aspect_ratio * 0.5)
        resized = self.image.resize((self.width, height), Image.Resampling.LANCZOS)

        # Get pixel data
        pixels = list(resized.getdata())

        # Convert to colored ASCII
        ascii_lines = []
        for y in range(height):
            line = []
            for x in range(self.width):
                pixel_index = y * self.width + x
                pixel = pixels[pixel_index]

                # Handle RGBA images
                if len(pixel) == 4:
                    r, g, b = pixel[0], pixel[1], pixel[2]
                else:
                    r, g, b = pixel, pixel, pixel

                # Calculate grayscale value
                gray = int(0.299 * r + 0.587 * g + 0.114 * b)

                # Map to character
                char_index = int((gray / 255) * (len(self.chars) - 1))
                char = self.chars[char_index]

                # Store character with color info
                line.append((char, (r, g, b)))

            ascii_lines.append(line)

        return ascii_lines

    def print_ascii(self, ascii_art: str):
        """Print ASCII art to console"""
        print(ascii_art)

    def print_color_ascii(self, colored_ascii: list):
        """Print colored ASCII art to console (if supported)"""
        try:
            for line in colored_ascii:
                for char, (r, g, b) in line:
                    # Check if terminal supports color
                    if hasattr(sys.stdout, 'isatty') and sys.stdout.isatty():
                        print(f"\033[38;2;{r};{g};{b}m{char}\033[0m", end='')
                    else:
                        print(char, end='')
                print()
        except Exception:
            # Fallback to non-colored output
            for line in colored_ascii:
                print(''.join(c for c, _ in line))

    def save_to_file(self, ascii_art: str, output_path: str):
        """Save ASCII art to a text file"""
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(ascii_art)
        print(f"ASCII art saved to: {output_path}")

def main():
    parser = argparse.ArgumentParser(
        description="Image to ASCII Art Converter",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Character Sets:
  simple    : ' .:-=+*#%@'
  standard  : ' .\\'-:^+!rc*?zLsLT4JU0|'
  detailed  : Full gradient set
  blocks    : ' ░▒▓█'
  binary    : '01'

Examples:
  python text-to-ascii.py --image photo.jpg
  python text-to-ascii.py -i photo.jpg --width 120
  python text-to-ascii.py -i photo.jpg --chars " ░▒▓█" --save art.txt
        """
    )

    parser.add_argument("-i", "--image", required=True,
                       help="Path to the input image")
    parser.add_argument("-w", "--width", type=int, default=80,
                       help="Output width in characters (default: 80)")
    parser.add_argument("-c", "--chars",
                       help="Character set to use (or specify preset)")
    parser.add_argument("-s", "--save",
                       help="Save ASCII art to file")
    parser.add_argument("--color", action="store_true",
                       help="Use colored output (if terminal supports)")
    parser.add_argument("--list-presets", action="store_true",
                       help="List available character set presets")

    args = parser.parse_args()

    # List presets
    if args.list_presets:
        print("\nAvailable Character Set Presets:")
        print("-" * 40)
        for name, chars in CHAR_SETS.items():
            print(f"  {name:12}: {chars}")
        print()
        return

    # Get character set
    if args.chars:
        if args.chars in CHAR_SETS:
            chars = CHAR_SETS[args.chars]
        else:
            chars = args.chars
    else:
        chars = CHAR_SETS["standard"]

    try:
        converter = ImageToASCII()
        converter.load_image(args.image)

        print(f"\nConverting: {args.image}")
        print(f"Width: {args.width} characters")
        print(f"Character set: {chars}")
        print("\n" + "=" * 60 + "\n")

        if args.color:
            colored = converter.convert_color(args.width, chars)
            converter.print_color_ascii(colored)
        else:
            ascii_art = converter.convert(args.width, chars)
            converter.print_ascii(ascii_art)

        print("\n" + "=" * 60)

        if args.save:
            if args.color:
                print("Note: Color not preserved in text file. Saving monochrome version.")
            ascii_art = converter.convert(args.width, chars)
            converter.save_to_file(ascii_art, args.save)

    except FileNotFoundError as e:
        print(f"Error: {e}")
        return 1
    except Exception as e:
        print(f"Error converting image: {e}")
        return 1

    return 0

if __name__ == "__main__":
    exit(main())
