#!/usr/bin/env python3
"""
GIF Maker Tool
Create animated GIFs from images with adjustable speed and loop settings.
"""

import argparse
import os
import sys
from pathlib import Path
from typing import List, Optional

from PIL import Image


class GIFMaker:
    """Animated GIF creation utility."""

    def __init__(self):
        self.supported_formats = ['.png', '.jpg', '.jpeg', '.bmp', '.webp', '.tiff', '.gif']

    def make_gif(self, image_paths: List[str], output_path: str,
                 duration: float = 500, loop: int = 0,
                 resize: Optional[tuple] = None,
                 optimize: bool = True) -> str:
        """Create a GIF from a list of image files.

        Args:
            image_paths: List of image file paths
            output_path: Output GIF path
            duration: Frame duration in milliseconds
            loop: Number of loops (0 = infinite)
            resize: Optional (width, height) to resize frames
            optimize: Whether to optimize GIF palette

        Returns:
            Path to created GIF
        """
        if not image_paths:
            raise ValueError("No images provided")

        frames = []

        for path in image_paths:
            img = Image.open(path)

            # Convert to RGB (GIF doesn't support RGBA well)
            if img.mode == 'RGBA':
                # Create white background for transparency
                background = Image.new('RGB', img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[3])
                img = background
            elif img.mode != 'RGB':
                img = img.convert('RGB')

            # Resize if specified
            if resize:
                img = img.resize(resize, Image.Resampling.LANCZOS)

            frames.append(img)

        if not frames:
            raise ValueError("No valid frames loaded")

        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)

        # Save as GIF
        frames[0].save(
            output,
            save_all=True,
            append_images=frames[1:],
            duration=int(duration),
            loop=loop,
            optimize=optimize
        )

        return str(output.resolve())

    def make_gif_from_folder(self, folder_path: str, output_path: str,
                             duration: float = 500, loop: int = 0,
                             pattern: str = "*",
                             resize: Optional[tuple] = None,
                             sort_natural: bool = True) -> str:
        """Create a GIF from all images in a folder.

        Args:
            folder_path: Directory containing images
            output_path: Output GIF path
            duration: Frame duration in milliseconds
            loop: Number of loops (0 = infinite)
            pattern: Glob pattern for image selection
            resize: Optional (width, height) to resize frames
            sort_natural: Sort files using natural ordering

        Returns:
            Path to created GIF
        """
        folder = Path(folder_path)
        if not folder.is_dir():
            raise NotADirectoryError(f"Not a directory: {folder_path}")

        # Collect image files
        image_files = []
        for fmt in self.supported_formats:
            image_files.extend(folder.glob(f'{pattern}{fmt}'))
            image_files.extend(folder.glob(f'{pattern}{fmt.upper()}'))

        if not image_files:
            raise ValueError(f"No images found in {folder_path}")

        # Sort naturally if requested
        if sort_natural:
            image_files = sorted(image_files, key=lambda x: self._natural_sort_key(x.name))
        else:
            image_files = sorted(image_files)

        return self.make_gif(
            [str(f) for f in image_files],
            output_path,
            duration=duration,
            loop=loop,
            resize=resize
        )

    @staticmethod
    def _natural_sort_key(s: str) -> List:
        """Generate a natural sort key."""
        import re
        return [int(text) if text.isdigit() else text.lower()
                for text in re.split(r'(\d+)', s)]

    def preview_gif(self, gif_path: str, frame_count: int = 10):
        """Preview GIF frames."""
        gif = Image.open(gif_path)

        print(f"GIF: {gif_path}")
        print(f"Size: {gif.size}")
        print(f"Frames: {gif.n_frames}")
        print(f"Duration: {gif.info.get('duration', 'N/A')} ms per frame")
        print(f"Loop: {'infinite' if gif.info.get('loop', 1) == 0 else gif.info.get('loop', 1)}")

        # Extract some frames as preview
        print("\nExtracting preview frames...")
        for i in range(min(frame_count, gif.n_frames)):
            gif.seek(i)
            frame = gif.copy()
            preview_path = f"frame_{i:03d}.png"
            frame.save(preview_path)
            print(f"  Saved: {preview_path}")


def main():
    parser = argparse.ArgumentParser(
        description='Create animated GIFs from images with adjustable speed and loop',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python gif-maker.py frame1.png frame2.png frame3.png -o animation.gif
  python gif-maker.py -d ./frames/ -o animation.gif -d 300
  python gif-maker.py -d ./frames/ -o animation.gif --resize 640 480
  python gif-maker.py -d ./frames/ -o animation.gif --no-loop --fps 10
        """
    )

    parser.add_argument('files', nargs='*', help='Image files to combine')
    parser.add_argument('-d', '--directory', help='Directory containing images')
    parser.add_argument('-o', '--output', default='output.gif', help='Output GIF file')
    parser.add_argument('-t', '--duration', type=float, default=500,
                       help='Frame duration in milliseconds (default: 500)')
    parser.add_argument('-f', '--fps', type=float,
                       help='Frames per second (overrides --duration)')
    parser.add_argument('-l', '--loop', type=int, default=0,
                       help='Number of loops (0 = infinite, default: 0)')
    parser.add_argument('-n', '--no-loop', action='store_true',
                       help='Play once only (same as --loop 1)')
    parser.add_argument('-r', '--resize',
                       help='Resize frames to WIDTHxHEIGHT')
    parser.add_argument('--pattern', default='*',
                       help='Pattern for directory mode (default: *)')
    parser.add_argument('-p', '--preview', action='store_true',
                       help='Preview existing GIF info and frames')

    args = parser.parse_args()

    maker = GIFMaker()

    # Preview mode
    if args.preview:
        if not args.files and not args.directory:
            print("Error: Provide a GIF file to preview")
            return
        path = args.files[0] if args.files else args.directory
        maker.preview_gif(path)
        return

    # Calculate duration from FPS if provided
    duration = args.duration
    if args.fps:
        duration = 1000 / args.fps

    # Loop setting
    loop = 0 if not args.no_loop else 1
    if args.no_loop:
        loop = 1

    # Resize setting
    resize = None
    if args.resize:
        dims = args.resize.split('x')
        if len(dims) == 2:
            resize = (int(dims[0]), int(dims[1]))
        else:
            print("Error: Resize must be WIDTHxHEIGHT (e.g., 640x480)")
            return

    try:
        if args.directory:
            # Directory mode
            print(f"Creating GIF from {args.directory}...")
            result = maker.make_gif_from_folder(
                args.directory,
                args.output,
                duration=duration,
                loop=loop,
                resize=resize,
                pattern=args.pattern
            )
            print(f"GIF created: {result}")

        elif args.files:
            # Files mode
            print(f"Creating GIF from {len(args.files)} images...")
            result = maker.make_gif(
                args.files,
                args.output,
                duration=duration,
                loop=loop,
                resize=resize
            )
            print(f"GIF created: {result}")

        else:
            print("Error: Provide image files or use --directory")
            return

        # Show info
        print(f"\nGIF Settings:")
        print(f"  Duration: {duration:.1f}ms per frame")
        print(f"  Loop: {'infinite' if loop == 0 else loop}")
        if resize:
            print(f"  Resize: {resize[0]}x{resize[1]}")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
