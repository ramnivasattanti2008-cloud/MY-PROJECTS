#!/usr/bin/env python3
"""
Image Cropper Tool
Crop images - interactive selection or CLI with coordinates.
"""

import argparse
import os
import sys
from pathlib import Path
from typing import Tuple, Optional

from PIL import Image, ImageDraw


class ImageCropper:
    """Image cropping utility with interactive and CLI modes."""

    def __init__(self):
        self.supported_formats = ['.png', '.jpg', '.jpeg', '.bmp', '.webp', '.tiff', '.gif']

    def crop(self, input_path: str, output_path: str,
             left: int, top: int, right: int, bottom: int) -> str:
        """Crop an image using pixel coordinates."""
        img = Image.open(input_path)

        # Validate coordinates
        width, height = img.size
        left = max(0, min(left, width))
        top = max(0, min(top, height))
        right = max(left, min(right, width))
        bottom = max(top, min(bottom, height))

        if right <= left or bottom <= top:
            raise ValueError("Invalid crop region: width and height must be positive")

        cropped = img.crop((left, top, right, bottom))

        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)
        cropped.save(output)

        return str(output.resolve())

    def crop_percent(self, input_path: str, output_path: str,
                     left_pct: float, top_pct: float,
                     right_pct: float, bottom_pct: float) -> str:
        """Crop an image using percentage coordinates (0-100)."""
        img = Image.open(input_path)
        width, height = img.size

        left = int(width * left_pct / 100)
        top = int(height * top_pct / 100)
        right = int(width * right_pct / 100)
        bottom = int(height * bottom_pct / 100)

        return self.crop(input_path, output_path, left, top, right, bottom)

    def batch_crop(self, input_dir: str, output_dir: str,
                   left: int, top: int, right: int, bottom: int) -> list:
        """Crop all images in a directory."""
        input_path = Path(input_dir)
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        results = []
        for fmt in self.supported_formats:
            for img_file in input_path.glob(f'*{fmt}'):
                out_file = output_path / img_file.name
                try:
                    self.crop(str(img_file), str(out_file), left, top, right, bottom)
                    results.append((str(img_file), str(out_file), 'Success'))
                except Exception as e:
                    results.append((str(img_file), str(out_file), f'Error: {e}'))

        return results


def interactive_crop(image_path: str) -> Optional[Tuple[int, int, int, int]]:
    """Interactive image cropping with visual selection."""
    try:
        import tkinter as tk
        from tkinter import ttk
    except ImportError:
        print("Tkinter not available for interactive mode.")
        return None

    img = Image.open(image_path)

    # Scale for display (max 800x600 preview)
    max_width, max_height = 800, 600
    scale = min(max_width / img.width, max_height / img.height, 1)

    display_width = int(img.width * scale)
    display_height = int(img.height * scale)

    root = tk.Tk()
    root.title("Image Cropper - Select Region")

    # Create frame for image display
    frame = ttk.Frame(root, padding=10)
    frame.pack(fill='both', expand=True)

    # Canvas for image and selection
    canvas = tk.Canvas(frame, width=display_width, height=display_height,
                       cursor='cross', bg='black')
    canvas.pack()

    # Display image
    display_img = img.resize((display_width, display_height), Image.Resampling.LANCZOS)
    img_tk = ImageTk.PhotoImage(display_img)
    canvas.create_image(0, 0, anchor='nw', image=img_tk)

    result = {'bbox': None}

    def on_click(event):
        result['start_x'] = event.x
        result['start_y'] = event.y
        canvas.delete('selection')
        canvas.delete('coords')

    def on_drag(event):
        canvas.delete('selection')
        canvas.delete('coords')

        x1, y1 = result['start_x'], result['start_y']
        x2, y2 = event.x, event.y

        left = min(x1, x2)
        top = min(y1, y2)
        right = max(x1, x2)
        bottom = max(y1, y2)

        # Draw rectangle
        canvas.create_rectangle(left, top, right, bottom,
                               outline='red', width=2, tags='selection')

        # Draw coordinates
        canvas.delete('coords')
        canvas.create_text(left + 5, top + 5, anchor='nw',
                         text=f'({left}, {top}) - ({right}, {bottom})',
                         fill='white', font=('Arial', 10, 'bold'),
                         tags='coords')

    def on_release(event):
        x1, y1 = result['start_x'], result['start_y']
        x2, y2 = event.x, event.y

        left = min(x1, x2)
        top = min(y1, y2)
        right = max(x1, x2)
        bottom = max(y1, y2)

        # Convert back to original coordinates
        result['bbox'] = (
            int(left / scale),
            int(top / scale),
            int(right / scale),
            int(bottom / scale)
        )

    def on_double_click(event):
        result['bbox'] = (0, 0, img.width, img.height)
        root.destroy()

    def on_escape(event):
        root.destroy()

    canvas.bind('<Button-1>', on_click)
    canvas.bind('<B1-Motion>', on_drag)
    canvas.bind('<ButtonRelease-1>', on_release)
    canvas.bind('<Double-Button-1>', on_double_click)
    root.bind('<Escape>', on_escape)

    # Buttons
    button_frame = ttk.Frame(frame)
    button_frame.pack(pady=10)

    ttk.Button(button_frame, text="Crop Selected",
               command=lambda: root.destroy() if result['bbox'] else None).pack(side='left', padx=5)
    ttk.Button(button_frame, text="Full Image",
               command=lambda: [root.destroy(),
                               result.update({'bbox': (0, 0, img.width, img.height)})]).pack(side='left', padx=5)
    ttk.Button(button_frame, text="Cancel",
               command=root.destroy).pack(side='left', padx=5)

    # Help text
    help_label = ttk.Label(frame, text="Click and drag to select region | Double-click for full image | ESC to cancel")
    help_label.pack(pady=5)

    root.mainloop()

    return result.get('bbox')


def main():
    parser = argparse.ArgumentParser(
        description='Crop images - interactive or CLI with coordinates',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python image-cropper.py -i photo.jpg -o cropped.jpg
  python image-cropper.py -i photo.jpg -o cropped.jpg -c 100,100,400,400
  python image-cropper.py -i photo.jpg -o cropped.jpg -p 10,10,90,90
  python image-cropper.py -i photos/ -o cropped/ -c 0,0,800,600
        """
    )

    parser.add_argument('-i', '--input', required=True,
                       help='Input image file or directory')
    parser.add_argument('-o', '--output', required=True,
                       help='Output file or directory')
    parser.add_argument('-c', '--coords',
                       help='Crop region as left,top,right,bottom (pixels)')
    parser.add_argument('-p', '--percent',
                       help='Crop region as left,top,right,bottom (percentages 0-100)')
    parser.add_argument('--left', type=int, help='Left coordinate')
    parser.add_argument('--top', type=int, help='Top coordinate')
    parser.add_argument('--right', type=int, help='Right coordinate')
    parser.add_argument('--bottom', type=int, help='Bottom coordinate')

    args = parser.parse_args()

    cropper = ImageCropper()

    # Parse coordinates
    coords = None
    if args.coords:
        coords = tuple(int(c.strip()) for c in args.coords.split(','))
        if len(coords) != 4:
            print("Error: Coordinates must be 4 values (left,top,right,bottom)")
            return
    elif all([args.left is not None, args.top is not None,
              args.right is not None, args.bottom is not None]):
        coords = (args.left, args.top, args.right, args.bottom)

    # Determine if input is directory
    is_directory = os.path.isdir(args.input)

    if is_directory:
        if not coords:
            print("Error: Coordinates required for batch processing")
            return

        results = cropper.batch_crop(args.input, args.output, *coords)
        print(f"\nProcessed {len(results)} images:")
        for input_file, output_file, status in results:
            print(f"  {status}: {Path(input_file).name}")
    else:
        # Single file
        if coords:
            # CLI mode with coordinates
            output = cropper.crop(args.input, args.output, *coords)
            print(f"Cropped image saved to: {output}")
        else:
            # Interactive mode
            print("Opening interactive crop tool...")
            bbox = interactive_crop(args.input)
            if bbox:
                output = cropper.crop(args.input, args.output, *bbox)
                print(f"Cropped image saved to: {output}")
                print(f"Coordinates used: {bbox}")
            else:
                print("Crop cancelled.")


if __name__ == '__main__':
    main()
