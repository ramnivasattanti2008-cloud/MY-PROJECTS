#!/usr/bin/env python3
"""
Color Detector - Extract dominant colors from images
"""

import argparse
import os
from collections import Counter
from dataclasses import dataclass
from typing import List, Tuple

try:
    from PIL import Image
    import numpy as np
except ImportError:
    print("Error: Required packages not installed.")
    print("Run: pip install -r requirements.txt")
    exit(1)

# Color names for matching
COLOR_NAMES = {
    (255, 0, 0): "Red",
    (0, 255, 0): "Green",
    (0, 0, 255): "Blue",
    (255, 255, 0): "Yellow",
    (255, 0, 255): "Magenta",
    (0, 255, 255): "Cyan",
    (255, 165, 0): "Orange",
    (128, 0, 128): "Purple",
    (255, 192, 203): "Pink",
    (0, 128, 0): "Dark Green",
    (128, 128, 0): "Olive",
    (0, 128, 128): "Teal",
    (0, 0, 128): "Navy",
    (128, 0, 0): "Maroon",
    (165, 42, 42): "Brown",
    (255, 255, 255): "White",
    (192, 192, 192): "Silver",
    (128, 128, 128): "Gray",
    (0, 0, 0): "Black",
    (255, 127, 80): "Coral",
    (64, 224, 208): "Turquoise",
    (230, 230, 250): "Lavender",
    (255, 228, 181): "Cornsilk",
    (245, 245, 220): "Beige",
    (210, 105, 30): "Chocolate",
    (255, 99, 71): "Tomato",
    (100, 149, 237): "Cornflower Blue",
    (147, 112, 219): "Medium Purple",
    (60, 179, 113): "Medium Sea Green",
    (255, 140, 0): "Dark Orange",
    (220, 20, 60): "Crimson",
    (139, 69, 19): "Saddle Brown",
    (0, 191, 255): "Deep Sky Blue",
    (50, 205, 50): "Lime Green",
    (255, 215, 0): "Gold",
    (186, 85, 211): "Medium Orchid",
    (143, 188, 143): "Sea Green",
    (72, 61, 139): "Dark Slate Blue",
    (95, 158, 160): "Cadet Blue",
    (255, 105, 180): "Hot Pink",
    (255, 228, 196): "Bisque",
    (245, 255, 250): "Mint Cream",
    (245, 245, 245): "White Smoke",
    (250, 240, 230): "Linen",
    (253, 245, 230): "Old Lace",
    (255, 250, 205): "Lemon Chiffon",
    (250, 250, 210): "Light Goldenrod",
    (255, 245, 238): "Seashell",
    (245, 245, 220): "Pale Goldenrod",
}

@dataclass
class ColorInfo:
    """Store information about a detected color"""
    rgb: Tuple[int, int, int]
    hex: str
    percentage: float
    name: str = ""

    def __post_init__(self):
        if not self.name:
            self.name = self._find_closest_color()

    def _find_closest_color(self) -> str:
        """Find the closest named color"""
        min_distance = float('inf')
        closest_name = "Custom"

        for target_rgb, name in COLOR_NAMES.items():
            distance = sum((a - b) ** 2 for a, b in zip(self.rgb, target_rgb))
            if distance < min_distance:
                min_distance = distance
                closest_name = name

        return closest_name

class ColorDetector:
    """Detect dominant colors in an image"""

    def __init__(self, image_path: str):
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found: {image_path}")

        self.image_path = image_path
        self.image = Image.open(image_path)
        self.colors: List[ColorInfo] = []

    def _resize_image(self, max_size: int = 200) -> Image.Image:
        """Resize image for faster processing while maintaining aspect ratio"""
        img = self.image.copy()
        img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
        return img

    def _extract_colors(self, num_colors: int = 5) -> List[Tuple[int, int, int]]:
        """Extract dominant colors using k-means-like clustering"""
        img = self._resize_image()
        img = img.convert('RGB')
        pixels = list(img.getdata())

        # Sample pixels if too many
        if len(pixels) > 10000:
            pixels = [pixels[i] for i in range(0, len(pixels), len(pixels) // 10000)]

        # Simple quantization for color clustering
        quantized = []
        for r, g, b in pixels:
            # Reduce color space to group similar colors
            qr, qg, qb = r // 16 * 16, g // 16 * 16, b // 16 * 16
            quantized.append((qr, qg, qb))

        # Count color occurrences
        color_counts = Counter(quantized)

        # Get top colors
        total_pixels = len(quantized)
        top_colors = color_counts.most_common(num_colors * 2)

        # Filter out very similar colors
        unique_colors = []
        for color, count in top_colors:
            is_similar = False
            for unique in unique_colors:
                if sum(abs(a - b) for a, b in zip(color, unique)) < 50:
                    is_similar = True
                    break
            if not is_similar:
                unique_colors.append(color)
                if len(unique_colors) >= num_colors:
                    break

        # Calculate percentages
        results = []
        for color in unique_colors[:num_colors]:
            count = quantized.count(color)
            percentage = (count / total_pixels) * 100
            results.append((color, percentage))

        return results

    def get_dominant_colors(self, num_colors: int = 5) -> List[ColorInfo]:
        """Get the dominant colors from the image"""
        raw_colors = self._extract_colors(num_colors)

        self.colors = [
            ColorInfo(
                rgb=rgb,
                hex=f"#{rgb[0]:02X}{rgb[1]:02X}{rgb[2]:02X}",
                percentage=pct
            )
            for rgb, pct in raw_colors
        ]

        return self.colors

    def print_colors(self):
        """Print color information to console"""
        print(f"\nAnalyzing image: {self.image_path}")
        print(f"Image size: {self.image.size[0]}x{self.image.size[1]}")
        print(f"\nTop {len(self.colors)} Dominant Colors:")
        print("━" * 50)

        for i, color in enumerate(self.colors, 1):
            # Create color bar
            bar = "█" * int(color.percentage / 2)

            print(f"\n  {i}. {color.hex}  {color.name}")
            print(f"     RGB{color.rgb}  {color.percentage:.1f}%")
            print(f"     {bar}")

        print("\n" + "━" * 50)

        # Print hex codes for easy copying
        hex_codes = [c.hex for c in self.colors]
        print(f"\nHex codes: {', '.join(hex_codes)}")

    def save_palette(self, output_path: str, width: int = 400, height: int = 100):
        """Save color palette as an image"""
        if not self.colors:
            raise ValueError("No colors detected. Call get_dominant_colors() first.")

        num_colors = len(self.colors)
        swatch_width = width // num_colors

        palette = Image.new('RGB', (width, height))

        for i, color in enumerate(self.colors):
            for x in range(i * swatch_width, (i + 1) * swatch_width):
                for y in range(height):
                    palette.putpixel((x, y), color.rgb)

        palette.save(output_path)
        print(f"\nPalette saved to: {output_path}")

    def print_visual_palette(self):
        """Print a visual representation of the palette"""
        if not self.colors:
            raise ValueError("No colors detected. Call get_dominant_colors() first.")

        print("\nColor Palette:")
        print("[", end="")

        for color in self.colors:
            # Use ANSI color codes for terminal
            r, g, b = color.rgb
            if r + g + b > 380:
                text_color = "\033[30m"  # Dark text
            else:
                text_color = "\033[97m"  # Light text
            reset = "\033[0m"

            # Create block with hex code
            block = f"{text_color}\033[48;2;{r};{g};{b}m {color.hex} {reset}"
            print(block, end="")

        print("]")

def main():
    parser = argparse.ArgumentParser(
        description="Color Detector - Extract dominant colors from images",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python color-detect.py --image photo.jpg
  python color-detect.py -i photo.jpg --count 10
  python color-detect.py -i photo.jpg --save palette.png
        """
    )

    parser.add_argument("-i", "--image", required=True,
                       help="Path to the input image")
    parser.add_argument("-c", "--count", type=int, default=5,
                       help="Number of colors to extract (default: 5)")
    parser.add_argument("-s", "--save",
                       help="Save palette to file")
    parser.add_argument("-v", "--visual", action="store_true",
                       help="Show visual palette in terminal")

    args = parser.parse_args()

    try:
        detector = ColorDetector(args.image)
        detector.get_dominant_colors(args.count)
        detector.print_colors()

        if args.visual:
            detector.print_visual_palette()
            print()

        if args.save:
            detector.save_palette(args.save)

    except FileNotFoundError as e:
        print(f"Error: {e}")
        return 1
    except Exception as e:
        print(f"Error analyzing image: {e}")
        return 1

    return 0

if __name__ == "__main__":
    exit(main())
