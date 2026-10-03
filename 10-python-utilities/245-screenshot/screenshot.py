#!/usr/bin/env python3
"""
Screenshot Tool
Take screenshots - full screen or with region selection.
"""

import argparse
import os
import sys
import time
from datetime import datetime
from pathlib import Path

from PIL import Image, ImageGrab


class ScreenshotTool:
    """Screenshot capture utility."""

    def __init__(self):
        self.default_save_dir = Path.home() / "Pictures" / "Screenshots"
        self.default_save_dir.mkdir(parents=True, exist_ok=True)

    def generate_filename(self, prefix="screenshot", ext="png"):
        """Generate a timestamped filename."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{prefix}_{timestamp}.{ext}"

    def capture_full_screen(self, save_path=None, include_cursor=False):
        """Capture the entire screen."""
        screenshot = ImageGrab.grab(all_screens=True, includecursor=include_cursor)

        if save_path is None:
            save_path = self.default_save_dir / self.generate_filename()

        save_path = Path(save_path)
        save_path.parent.mkdir(parents=True, exist_ok=True)

        screenshot.save(save_path)
        return str(save_path)

    def capture_region(self, bbox, save_path=None):
        """Capture a specific region of the screen.

        Args:
            bbox: Tuple of (left, top, right, bottom) coordinates
        """
        screenshot = ImageGrab.grab(bbox=bbox)

        if save_path is None:
            save_path = self.default_save_dir / self.generate_filename()

        save_path = Path(save_path)
        save_path.parent.mkdir(parents=True, exist_ok=True)

        screenshot.save(save_path)
        return str(save_path)

    def interactive_region_select(self):
        """Let user select a region using a GUI overlay."""
        try:
            import tkinter as tk
            from tkinter import ttk
        except ImportError:
            print("Tkinter not available. Please specify region manually.")
            return None

        root = tk.Tk()
        root.attributes('-fullscreen', True)
        root.attributes('-alpha', 0.3)
        root.attributes('-topmost', True)

        canvas = tk.Canvas(root, cursor='cross', bg='gray50', highlightthickness=0)
        canvas.pack(fill='both', expand=True)

        selection = {'bbox': None}

        def on_click(event):
            selection['start_x'] = event.x
            selection['start_y'] = event.y

        def on_drag(event):
            canvas.delete('selection')
            canvas.create_rectangle(
                selection['start_x'], selection['start_y'],
                event.x, event.y,
                outline='white', width=2, tags='selection'
            )

        def on_release(event):
            x1, y1 = selection['start_x'], selection['start_y']
            x2, y2 = event.x, event.y

            left = min(x1, x2)
            top = min(y1, y2)
            right = max(x1, x2)
            bottom = max(y1, y2)

            if right - left > 5 and bottom - top > 5:
                selection['bbox'] = (left, top, right, bottom)

            root.destroy()

        canvas.bind('<Button-1>', on_click)
        canvas.bind('<B1-Motion>', on_drag)
        canvas.bind('<ButtonRelease-1>', on_release)

        # Cancel with Escape
        def on_escape(event):
            root.destroy()

        root.bind('<Escape>', on_escape)

        root.mainloop()

        return selection.get('bbox')


def main():
    parser = argparse.ArgumentParser(
        description='Take screenshots - full screen or region selection',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python screenshot.py                           # Full screen, interactive select
  python screenshot.py -f                         # Full screen capture
  python screenshot.py -r                         # Interactive region selection
  python screenshot.py -r -o my_screenshot.png    # Region with custom filename
  python screenshot.py -c 100,100,800,600        # Specific coordinates
  python screenshot.py -f -d ./captures/           # Custom save directory
        """
    )

    parser.add_argument('-f', '--full', action='store_true',
                       help='Capture full screen')
    parser.add_argument('-r', '--region', action='store_true',
                       help='Interactive region selection (click and drag)')
    parser.add_argument('-c', '--coords',
                       help='Region coordinates as left,top,right,bottom')
    parser.add_argument('-o', '--output',
                       help='Output filename (default: auto-generated)')
    parser.add_argument('-d', '--directory',
                       help='Save directory (default: ~/Pictures/Screenshots)')
    parser.add_argument('--delay', type=float, default=0,
                       help='Delay before capture in seconds (default: 0)')
    parser.add_argument('--cursor', action='store_true',
                       help='Include cursor in screenshot')
    parser.add_argument('--format', default='png',
                       choices=['png', 'jpg', 'bmp'],
                       help='Output format (default: png)')

    args = parser.parse_args()

    tool = ScreenshotTool()

    # Override save directory if specified
    if args.directory:
        tool.default_save_dir = Path(args.directory)
        tool.default_save_dir.mkdir(parents=True, exist_ok=True)

    # Determine output path
    output = args.output
    if output and not Path(output).suffix:
        output = str(Path(output).with_suffix(f'.{args.format}'))
    elif output and Path(output).suffix.lstrip('.') != args.format:
        output = str(Path(output).with_suffix(f'.{args.format}'))

    # Apply delay
    if args.delay > 0:
        print(f"Capturing in {args.delay} seconds...")
        time.sleep(args.delay)

    try:
        if args.coords:
            # Specific coordinates provided
            coords = tuple(int(c.strip()) for c in args.coords.split(','))
            if len(coords) != 4:
                print("Error: Coordinates must be 4 values (left,top,right,bottom)")
                return
            result = tool.capture_region(coords, output)
            print(f"Screenshot saved: {result}")

        elif args.region:
            # Interactive region selection
            print("Click and drag to select region. Press ESC to cancel.")
            bbox = tool.interactive_region_select()
            if bbox:
                result = tool.capture_region(bbox, output)
                print(f"Screenshot saved: {result}")
            else:
                print("Region selection cancelled.")

        elif args.full:
            # Full screen capture
            result = tool.capture_full_screen(output, args.cursor)
            print(f"Screenshot saved: {result}")

        else:
            # Default: interactive region selection
            print("Click and drag to select region. Press ESC to cancel.")
            bbox = tool.interactive_region_select()
            if bbox:
                result = tool.capture_region(bbox, output)
                print(f"Screenshot saved: {result}")
            else:
                print("Region selection cancelled.")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
