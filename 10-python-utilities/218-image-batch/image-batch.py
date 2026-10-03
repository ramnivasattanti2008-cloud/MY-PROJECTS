#!/usr/bin/env python3
"""
Image Batch Processor - Resize, crop, compress multiple images.
"""

import os
import sys
import argparse
from pathlib import Path
from typing import Tuple, Optional

try:
    from PIL import Image, ImageOps, ImageFilter, ImageEnhance
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

try:
    import tkinter as tk
    from tkinter import ttk, filedialog, messagebox, scrolledtext
    HAS_TK = True
except ImportError:
    HAS_TK = False


class ImageProcessor:
    """Main image processing engine."""

    SUPPORTED_FORMATS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.tiff'}

    def __init__(self, quality: int = 85, output_dir: Optional[str] = None,
                 prefix: str = '', suffix: str = '', overwrite: bool = False):
        self.quality = quality
        self.output_dir = Path(output_dir) if output_dir else None
        self.prefix = prefix
        self.suffix = suffix
        self.overwrite = overwrite

        self.stats = {'processed': 0, 'skipped': 0, 'errors': 0}
        self.log = []

    def log_msg(self, msg: str):
        """Log a message."""
        self.log.append(msg)
        print(msg)

    def get_output_path(self, input_path: Path, output_format: Optional[str] = None) -> Path:
        """Generate output file path."""
        stem = f"{self.prefix}{input_path.stem}{self.suffix}"

        if output_format:
            ext = f".{output_format.lower()}"
        else:
            ext = input_path.suffix.lower()

        if self.output_dir:
            self.output_dir.mkdir(parents=True, exist_ok=True)
            return self.output_dir / f"{stem}{ext}"
        else:
            if self.overwrite:
                return input_path
            else:
                return input_path.parent / f"{stem}{ext}"

    def resize_image(self, img: Image.Image, width: Optional[int] = None,
                    height: Optional[int] = None, scale: Optional[float] = None,
                    maintain_aspect: bool = True) -> Image.Image:
        """Resize image."""
        if scale:
            new_width = int(img.width * scale)
            new_height = int(img.height * scale)
        elif width and height:
            if maintain_aspect:
                img.thumbnail((width, height), Image.Resampling.LANCZOS)
                return img
            else:
                new_width, new_height = width, height
        elif width:
            ratio = width / img.width
            new_width, new_height = width, int(img.height * ratio)
        elif height:
            ratio = height / img.height
            new_width, new_height = int(img.width * ratio), height
        else:
            return img

        return img.resize((new_width, new_height), Image.Resampling.LANCZOS)

    def crop_image(self, img: Image.Image, width: int, height: int,
                   position: str = 'center') -> Image.Image:
        """Crop image to specified dimensions."""
        img_width, img_height = img.size

        if position == 'center':
            left = (img_width - width) // 2
            top = (img_height - height) // 2
        elif position == 'top':
            left = (img_width - width) // 2
            top = 0
        elif position == 'bottom':
            left = (img_width - width) // 2
            top = img_height - height
        elif position == 'left':
            left = 0
            top = (img_height - height) // 2
        elif position == 'right':
            left = img_width - width
            top = (img_height - height) // 2
        else:
            left = top = 0

        right = left + width
        bottom = top + height

        return img.crop((left, top, right, bottom))

    def compress_image(self, img: Image.Image, quality: Optional[int] = None) -> Image.Image:
        """Optimize image for file size."""
        # For JPEG, reduce quality slightly; PIL handles optimization
        return img

    def process_image(self, input_path: Path, operations: dict) -> bool:
        """Process a single image with given operations."""
        try:
            # Open image
            img = Image.open(input_path)

            # Apply operations
            if 'resize' in operations:
                opts = operations['resize']
                img = self.resize_image(img, **opts)

            if 'crop' in operations:
                img = self.crop_image(img, **operations['crop'])

            if 'rotate' in operations:
                img = img.rotate(operations['rotate'], expand=True)

            if 'flip_h' in operations:
                img = ImageOps.mirror(img)

            if 'flip_v' in operations:
                img = ImageOps.flip(img)

            if 'grayscale' in operations:
                img = ImageOps.grayscale(img)
                if img.mode != 'RGB':
                    img = img.convert('RGB')

            if 'blur' in operations:
                img = img.filter(ImageFilter.GaussianBlur(radius=operations['blur']))

            if 'sharpen' in operations:
                img = img.filter(ImageFilter.SHARPEN)

            if 'brightness' in operations:
                enhancer = ImageEnhance.Brightness(img)
                img = enhancer.enhance(operations['brightness'])

            if 'contrast' in operations:
                enhancer = ImageEnhance.Contrast(img)
                img = enhancer.enhance(operations['contrast'])

            # Get output path
            output_path = self.get_output_path(input_path, operations.get('format'))

            # Ensure output format is supported
            if output_path.suffix.lower() not in self.SUPPORTED_FORMATS:
                output_path = output_path.with_suffix('.jpg')

            # Save with quality settings
            save_kwargs = {}
            if output_path.suffix.lower() in {'.jpg', '.jpeg'}:
                save_kwargs['quality'] = quality or self.quality
                save_kwargs['optimize'] = True
            elif output_path.suffix.lower() == '.png':
                save_kwargs['optimize'] = True

            img.save(output_path, **save_kwargs)

            self.log_msg(f"Processed: {input_path.name} -> {output_path.name}")
            self.stats['processed'] += 1
            return True

        except Exception as e:
            self.log_msg(f"ERROR: {input_path.name} - {e}")
            self.stats['errors'] += 1
            return False

    def process_folder(self, input_dir: str, operations: dict, recursive: bool = True) -> dict:
        """Process all images in a folder."""
        input_path = Path(input_dir)

        if not input_path.exists():
            raise FileNotFoundError(f"Folder not found: {input_dir}")

        self.log = []
        self.stats = {'processed': 0, 'skipped': 0, 'errors': 0}

        # Find all image files
        image_files = []
        pattern = '**/*' if recursive else '*'

        for ext in self.SUPPORTED_FORMATS:
            image_files.extend(input_path.glob(f"{pattern}{ext}"))
            image_files.extend(input_path.glob(f"{pattern}{ext.upper()}"))

        image_files = sorted(set(image_files))

        self.log_msg(f"Found {len(image_files)} images in {input_dir}")
        self.log_msg("-" * 50)

        # Process each image
        for img_path in image_files:
            self.process_image(img_path, operations)

        self.log_msg("-" * 50)
        self.log_msg(f"Done! Processed: {self.stats['processed']}, "
                    f"Skipped: {self.stats['skipped']}, Errors: {self.stats['errors']}")

        return self.stats


class BatchProcessorGUI:
    """GUI for batch image processing."""

    def __init__(self, root):
        self.root = root
        self.root.title("Image Batch Processor")
        self.root.geometry("800x700")
        self.root.configure(bg='#1e1e2e')

        self.input_dir = tk.StringVar()
        self.output_dir = tk.StringVar()
        self.quality = tk.IntVar(value=85)
        self.prefix = tk.StringVar()
        self.suffix = tk.StringVar(value='_processed')
        self.overwrite = tk.BooleanVar(value=False)
        self.recursive = tk.BooleanVar(value=True)

        # Operation variables
        self.resize_enabled = tk.BooleanVar(value=False)
        self.resize_width = tk.IntVar(value=800)
        self.resize_height = tk.IntVar(value=600)
        self.resize_scale = tk.DoubleVar(value=0.5)

        self.crop_enabled = tk.BooleanVar(value=False)
        self.crop_width = tk.IntVar(value=800)
        self.crop_height = tk.IntVar(value=600)
        self.crop_position = tk.StringVar(value='center')

        self.rotate_value = tk.IntVar(value=0)
        self.flip_h = tk.BooleanVar(value=False)
        self.flip_v = tk.BooleanVar(value=False)
        self.grayscale = tk.BooleanVar(value=False)
        self.blur_value = tk.IntVar(value=0)
        self.brightness_value = tk.DoubleVar(value=1.0)
        self.contrast_value = tk.DoubleVar(value=1.0)

        self.setup_styles()
        self.create_widgets()

    def setup_styles(self):
        """Configure ttk styles."""
        style = ttk.Style()
        style.theme_use('clam')

        style.configure('Dark.TFrame', background='#1e1e2e')
        style.configure('Dark.TLabel', background='#1e1e2e', foreground='#cdd6f4', font=('Segoe UI', 9))
        style.configure('Section.TLabel', background='#1e1e2e', foreground='#f5c2e7',
                      font=('Segoe UI', 10, 'bold'))
        style.configure('Dark.TButton', background='#313244', foreground='#cdd6f4', font=('Segoe UI', 9))
        style.map('Dark.TButton', background=[('active', '#45475a')])
        style.configure('Dark.TEntry', fieldbackground='#313244', foreground='#cdd6f4')
        style.configure('Dark.TCheckbutton', background='#1e1e2e', foreground='#cdd6f4')
        style.configure('Dark.TSpinbox', fieldbackground='#313244', foreground='#cdd6f4')
        style.configure('Dark.TCombobox', fieldbackground='#313244', foreground='#cdd6f4')

    def create_widgets(self):
        """Create GUI widgets."""
        main_frame = ttk.Frame(self.root, style='Dark.TFrame')
        main_frame.pack(fill='both', expand=True, padx=15, pady=15)

        # Title
        ttk.Label(main_frame, text="Image Batch Processor",
                 font=('Segoe UI', 14, 'bold')).pack(pady=(0, 15))

        # Scrollable canvas
        canvas = tk.Canvas(main_frame, bg='#1e1e2e', highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient='vertical', command=canvas.yview)
        scroll_frame = ttk.Frame(canvas, style='Dark.TFrame')

        scroll_frame.bind("<Configure>",
                         lambda e: canvas.configure(scrollregion=canvas.bbox('all')))

        canvas.create_window((0, 0), window=scroll_frame, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)

        # Input/Output folders
        self.add_section(scroll_frame, "Folders")

        row = ttk.Frame(scroll_frame, style='Dark.TFrame')
        row.pack(fill='x', pady=2)
        ttk.Label(row, text="Input:").pack(side='left', padx=5)
        ttk.Entry(row, textvariable=self.input_dir, width=40).pack(side='left', fill='x', expand=True)
        ttk.Button(row, text="Browse", command=self.browse_input).pack(side='left', padx=5)

        row = ttk.Frame(scroll_frame, style='Dark.TFrame')
        row.pack(fill='x', pady=2)
        ttk.Label(row, text="Output:").pack(side='left', padx=5)
        ttk.Entry(row, textvariable=self.output_dir, width=40).pack(side='left', fill='x', expand=True)
        ttk.Button(row, text="Browse", command=self.browse_output).pack(side='left', padx=5)

        # Output options
        self.add_section(scroll_frame, "Output Options")

        row = ttk.Frame(scroll_frame, style='Dark.TFrame')
        row.pack(fill='x', pady=2)
        ttk.Label(row, text="Quality (JPEG):").pack(side='left', padx=5)
        ttk.Spinbox(row, from_=1, to=100, textvariable=self.quality, width=8).pack(side='left')

        row = ttk.Frame(scroll_frame, style='Dark.TFrame')
        row.pack(fill='x', pady=2)
        ttk.Label(row, text="Prefix:").pack(side='left', padx=5)
        ttk.Entry(row, textvariable=self.prefix, width=15).pack(side='left')
        ttk.Label(row, text="Suffix:").pack(side='left', padx=(15, 5))
        ttk.Entry(row, textvariable=self.suffix, width=15).pack(side='left')
        ttk.Checkbutton(row, text="Overwrite", variable=self.overwrite).pack(side='left', padx=15)
        ttk.Checkbutton(row, text="Recursive", variable=self.recursive).pack(side='left')

        # Resize
        self.add_section(scroll_frame, "Resize")
        row = ttk.Frame(scroll_frame, style='Dark.TFrame')
        row.pack(fill='x', pady=2)
        ttk.Checkbutton(row, text="Enable", variable=self.resize_enabled).pack(side='left', padx=5)
        ttk.Label(row, text="Width:").pack(side='left', padx=5)
        ttk.Spinbox(row, from_=1, to=10000, textvariable=self.resize_width, width=8).pack(side='left')
        ttk.Label(row, text="Height:").pack(side='left', padx=5)
        ttk.Spinbox(row, from_=1, to=10000, textvariable=self.resize_height, width=8).pack(side='left')
        ttk.Label(row, text="Scale:").pack(side='left', padx=(15, 5))
        ttk.Entry(row, textvariable=self.resize_scale, width=8).pack(side='left')

        # Crop
        self.add_section(scroll_frame, "Crop")
        row = ttk.Frame(scroll_frame, style='Dark.TFrame')
        row.pack(fill='x', pady=2)
        ttk.Checkbutton(row, text="Enable", variable=self.crop_enabled).pack(side='left', padx=5)
        ttk.Label(row, text="Width:").pack(side='left', padx=5)
        ttk.Spinbox(row, from_=1, to=10000, textvariable=self.crop_width, width=8).pack(side='left')
        ttk.Label(row, text="Height:").pack(side='left', padx=5)
        ttk.Spinbox(row, from_=1, to=10000, textvariable=self.crop_height, width=8).pack(side='left')
        ttk.Label(row, text="Position:").pack(side='left', padx=(15, 5))
        ttk.Combobox(row, textvariable=self.crop_position, values=['center', 'top', 'bottom', 'left', 'right'],
                    width=10, state='readonly').pack(side='left')

        # Transform
        self.add_section(scroll_frame, "Transform")
        row = ttk.Frame(scroll_frame, style='Dark.TFrame')
        row.pack(fill='x', pady=2)
        ttk.Label(row, text="Rotate:").pack(side='left', padx=5)
        ttk.Spinbox(row, from_=0, to=360, textvariable=self.rotate_value, width=8).pack(side='left')
        ttk.Checkbutton(row, text="Flip H", variable=self.flip_h).pack(side='left', padx=15)
        ttk.Checkbutton(row, text="Flip V", variable=self.flip_v).pack(side='left', padx=15)
        ttk.Checkbutton(row, text="Grayscale", variable=self.grayscale).pack(side='left', padx=15)

        # Effects
        self.add_section(scroll_frame, "Effects")
        row = ttk.Frame(scroll_frame, style='Dark.TFrame')
        row.pack(fill='x', pady=2)
        ttk.Label(row, text="Blur:").pack(side='left', padx=5)
        ttk.Spinbox(row, from_=0, to=20, textvariable=self.blur_value, width=8).pack(side='left')
        ttk.Label(row, text="Brightness:").pack(side='left', padx=(15, 5))
        ttk.Entry(row, textvariable=self.brightness_value, width=8).pack(side='left')
        ttk.Label(row, text="Contrast:").pack(side='left', padx=(15, 5))
        ttk.Entry(row, textvariable=self.contrast_value, width=8).pack(side='left')

        # Buttons
        btn_frame = ttk.Frame(scroll_frame, style='Dark.TFrame')
        btn_frame.pack(pady=15)
        ttk.Button(btn_frame, text="Process Images", command=self.process_images).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Clear Log", command=self.clear_log).pack(side='left', padx=5)

        # Log
        ttk.Label(scroll_frame, text="Processing Log:").pack(anchor='w')
        self.log_text = scrolledtext.ScrolledText(scroll_frame, height=10, bg='#181825',
                                                    fg='#a6e3a1', font=('Consolas', 8))
        self.log_text.pack(fill='both', expand=True, pady=5)

        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

    def add_section(self, parent, title):
        """Add a section header."""
        ttk.Label(parent, text=title, style='Section.TLabel').pack(anchor='w', pady=(10, 2))

    def browse_input(self):
        folder = filedialog.askdirectory(title="Select Input Folder")
        if folder:
            self.input_dir.set(folder)

    def browse_output(self):
        folder = filedialog.askdirectory(title="Select Output Folder")
        if folder:
            self.output_dir.set(folder)

    def log(self, msg: str):
        """Add message to log."""
        self.log_text.insert('end', msg + '\n')
        self.log_text.see('end')
        self.root.update()

    def clear_log(self):
        self.log_text.delete('1.0', 'end')

    def get_operations(self) -> dict:
        """Build operations dict from GUI values."""
        ops = {}

        if self.resize_enabled.get():
            ops['resize'] = {
                'width': self.resize_width.get(),
                'height': self.resize_height.get(),
                'scale': self.resize_scale.get() if self.resize_scale.get() != 1.0 else None,
                'maintain_aspect': True
            }

        if self.crop_enabled.get():
            ops['crop'] = {
                'width': self.crop_width.get(),
                'height': self.crop_height.get(),
                'position': self.crop_position.get()
            }

        if self.rotate_value.get():
            ops['rotate'] = self.rotate_value.get()

        if self.flip_h.get():
            ops['flip_h'] = True

        if self.flip_v.get():
            ops['flip_v'] = True

        if self.grayscale.get():
            ops['grayscale'] = True

        if self.blur_value.get():
            ops['blur'] = self.blur_value.get()

        if self.brightness_value.get() != 1.0:
            ops['brightness'] = self.brightness_value.get()

        if self.contrast_value.get() != 1.0:
            ops['contrast'] = self.contrast_value.get()

        return ops

    def process_images(self):
        """Process images based on GUI settings."""
        input_dir = self.input_dir.get()

        if not input_dir:
            messagebox.showwarning("Missing Input", "Please select an input folder.")
            return

        self.clear_log()

        processor = ImageProcessor(
            quality=self.quality.get(),
            output_dir=self.output_dir.get() or None,
            prefix=self.prefix.get(),
            suffix=self.suffix.get(),
            overwrite=self.overwrite.get()
        )

        operations = self.get_operations()

        if not operations:
            messagebox.showinfo("No Operations", "Please enable at least one processing option.")
            return

        self.log(f"Processing with operations: {list(operations.keys())}")
        self.log("-" * 40)

        try:
            stats = processor.process_folder(input_dir, operations, self.recursive.get())

            for msg in processor.log:
                self.log(msg)

            messagebox.showinfo("Complete",
                              f"Processed: {stats['processed']}\nErrors: {stats['errors']}")

        except Exception as e:
            messagebox.showerror("Error", str(e))


def main():
    if not HAS_PIL:
        print("Error: Pillow library required")
        print("Install with: pip install Pillow")
        return 1

    parser = argparse.ArgumentParser(description="Image Batch Processor")
    parser.add_argument('input', nargs='?', help="Input folder")
    parser.add_argument('-o', '--output', help="Output folder")
    parser.add_argument('-q', '--quality', type=int, default=85, help="JPEG quality (1-100)")
    parser.add_argument('--prefix', default='', help="Output filename prefix")
    parser.add_argument('--suffix', default='_processed', help="Output filename suffix")
    parser.add_argument('--overwrite', action='store_true', help="Overwrite original files")
    parser.add_argument('-r', '--recursive', action='store_true', default=True, help="Recurse into subfolders")
    parser.add_argument('--width', type=int, help="Resize width")
    parser.add_argument('--height', type=int, help="Resize height")
    parser.add_argument('--scale', type=float, help="Resize scale factor")
    parser.add_argument('--crop-w', type=int, help="Crop width")
    parser.add_argument('--crop-h', type=int, help="Crop height")
    parser.add_argument('--rotate', type=int, default=0, help="Rotation angle")
    parser.add_argument('--flip-h', action='store_true', help="Flip horizontally")
    parser.add_argument('--flip-v', action='store_true', help="Flip vertically")
    parser.add_argument('--grayscale', action='store_true', help="Convert to grayscale")
    parser.add_argument('--blur', type=int, help="Blur radius")
    parser.add_argument('--gui', action='store_true', help="Force GUI mode")
    parser.add_argument('--no-gui', action='store_true', help="Force CLI mode")

    args = parser.parse_args()

    use_gui = (args.gui or (not args.no_gui and not args.input and HAS_TK and sys.stdout.isatty()))

    if use_gui and HAS_TK:
        root = tk.Tk()
        BatchProcessorGUI(root)
        root.mainloop()
    else:
        if not args.input:
            print("Image Batch Processor")
            print("Usage: image-batch.py <input_folder> [options]")
            print("       image-batch.py --gui  (to launch GUI)")
            print("\nOptions:")
            print("  -o, --output DIR      Output folder")
            print("  -q, --quality N       JPEG quality (1-100, default: 85)")
            print("  --prefix TEXT         Filename prefix")
            print("  --suffix TEXT         Filename suffix (default: _processed)")
            print("  --overwrite           Overwrite original files")
            print("  -r, --recursive       Recurse into subfolders")
            print("\nOperations:")
            print("  --width N --height N  Resize to dimensions")
            print("  --scale N             Resize by scale factor")
            print("  --crop-w N --crop-h N Crop to dimensions")
            print("  --rotate N            Rotate by degrees")
            print("  --flip-h / --flip-v   Flip horizontally/vertically")
            print("  --grayscale           Convert to grayscale")
            print("  --blur N              Apply Gaussian blur")
            print("\nExample:")
            print("  image-batch.py ./photos -o ./output --width 800 --height 600 --grayscale")
            return 1

        # Build operations
        ops = {}
        if args.width or args.height:
            ops['resize'] = {'width': args.width, 'height': args.height, 'maintain_aspect': True}
        if args.scale:
            ops['resize'] = {'scale': args.scale, 'maintain_aspect': True}
        if args.crop_w and args.crop_h:
            ops['crop'] = {'width': args.crop_w, 'height': args.crop_h}
        if args.rotate:
            ops['rotate'] = args.rotate
        if args.flip_h:
            ops['flip_h'] = True
        if args.flip_v:
            ops['flip_v'] = True
        if args.grayscale:
            ops['grayscale'] = True
        if args.blur:
            ops['blur'] = args.blur

        if not ops:
            print("Error: No operations specified. Use --gui for interactive mode.")
            return 1

        processor = ImageProcessor(
            quality=args.quality,
            output_dir=args.output,
            prefix=args.prefix,
            suffix=args.suffix,
            overwrite=args.overwrite
        )

        try:
            stats = processor.process_folder(args.input, ops, args.recursive)
            return 0 if stats['errors'] == 0 else 1
        except Exception as e:
            print(f"Error: {e}")
            return 1


if __name__ == '__main__':
    sys.exit(main())
