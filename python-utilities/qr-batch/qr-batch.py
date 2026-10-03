#!/usr/bin/env python3
"""
QR Batch Generator - Generate multiple QR codes from CSV input.
"""

import os
import sys
import csv
import argparse
from pathlib import Path
from typing import List, Dict, Optional

try:
    import qrcode
    HAS_QR = True
except ImportError:
    HAS_QR = False

try:
    import tkinter as tk
    from tkinter import ttk, filedialog, messagebox, scrolledtext
    HAS_TK = True
except ImportError:
    HAS_TK = False


class QRBatchGenerator:
    """Batch QR code generator from CSV data."""

    def __init__(self, output_dir: str = './qr-output', size: int = 10,
                 error_correction: str = 'M', format: str = 'PNG'):
        self.output_dir = Path(output_dir)
        self.size = size  # Module size in pixels
        self.error_correction = error_correction
        self.format = format.upper()

        self.ec_levels = {
            'L': qrcode.constants.ERROR_CORRECT_L,  # 7%
            'M': qrcode.constants.ERROR_CORRECT_M,  # 15%
            'Q': qrcode.constants.ERROR_CORRECT_Q,  # 25%
            'H': qrcode.constants.ERROR_CORRECT_H,   # 30%
        }

        self.stats = {'generated': 0, 'errors': 0, 'skipped': 0}
        self.log = []

    def log_msg(self, msg: str):
        """Log a message."""
        self.log.append(msg)
        print(msg)

    def create_qr(self, data: str, filename: str, include_border: bool = True) -> Optional[Path]:
        """Create a single QR code image."""
        try:
            qr = qrcode.QRCode(
                version=1,
                error_correction=self.ec_levels.get(self.error_correction, qrcode.constants.ERROR_CORRECT_M),
                box_size=self.size,
                border=4 if include_border else 0,
            )

            qr.add_data(data)
            qr.make(fit=True)

            # Create image
            img = qr.make_image(fill_color='black', back_color='white')

            # Ensure output directory exists
            self.output_dir.mkdir(parents=True, exist_ok=True)

            # Save image
            output_path = self.output_dir / filename
            img.save(output_path, format=self.format)

            return output_path

        except Exception as e:
            self.log_msg(f"ERROR creating QR for '{data[:30]}...': {e}")
            self.stats['errors'] += 1
            return None

    def process_csv(self, csv_path: str, data_column: str = None,
                   name_column: str = None, custom_columns: Dict = None) -> List[Path]:
        """Process a CSV file and generate QR codes."""
        csv_file = Path(csv_path)

        if not csv_file.exists():
            raise FileNotFoundError(f"CSV file not found: {csv_path}")

        self.log = []
        self.stats = {'generated': 0, 'errors': 0, 'skipped': 0}
        generated_files = []

        self.log_msg(f"Processing CSV: {csv_path}")
        self.log_msg(f"Output directory: {self.output_dir}")
        self.log_msg("-" * 50)

        # Read CSV
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        if not rows:
            raise ValueError("CSV file is empty or has no headers")

        # Determine column names
        headers = rows[0].keys()

        if data_column is None:
            # Auto-detect: look for common column names
            for col in ['url', 'link', 'data', 'content', 'text', 'value', 'code']:
                if col in headers:
                    data_column = col
                    break
            if data_column is None:
                data_column = list(headers)[0]  # Use first column

        if name_column is None:
            # Auto-detect: look for name/id column
            for col in ['name', 'id', 'title', 'filename', 'file', 'label']:
                if col in headers and col != data_column:
                    name_column = col
                    break

        self.log_msg(f"Data column: {data_column}")
        self.log_msg(f"Name column: {name_column}")
        self.log_msg(f"Rows to process: {len(rows)}")
        self.log_msg("-" * 50)

        # Process each row
        for i, row in enumerate(rows, 1):
            data = row.get(data_column, '').strip()

            if not data:
                self.log_msg(f"Row {i}: Skipped (empty data)")
                self.stats['skipped'] += 1
                continue

            # Generate filename
            if name_column and row.get(name_column):
                name = row[name_column].strip()
                # Sanitize filename
                name = ''.join(c for c in name if c.isalnum() or c in '._- ')
                name = name.replace(' ', '_')
                if not name:
                    name = f"qr_{i}"
            else:
                name = f"qr_{i}"

            filename = f"{name}.png"

            # Create QR code
            result = self.create_qr(data, filename)

            if result:
                self.log_msg(f"Row {i}: Generated {filename}")
                generated_files.append(result)
                self.stats['generated'] += 1
            else:
                self.stats['errors'] += 1

        self.log_msg("-" * 50)
        self.log_msg(f"Complete! Generated: {self.stats['generated']}, "
                    f"Skipped: {self.stats['skipped']}, Errors: {self.stats['errors']}")

        return generated_files

    def generate_list(self, items: List[str], prefix: str = "qr") -> List[Path]:
        """Generate QR codes from a list of strings."""
        self.log = []
        self.stats = {'generated': 0, 'errors': 0, 'skipped': 0}
        generated_files = []

        self.output_dir.mkdir(parents=True, exist_ok=True)

        for i, data in enumerate(items, 1):
            if not data.strip():
                continue

            filename = f"{prefix}_{i}.png"
            result = self.create_qr(data.strip(), filename)

            if result:
                self.stats['generated'] += 1
                generated_files.append(result)

        return generated_files


class QRBatchGUI:
    """GUI for batch QR code generation."""

    def __init__(self, root):
        self.root = root
        self.root.title("QR Batch Generator")
        self.root.geometry("700x600")
        self.root.configure(bg='#1e1e2e')

        self.csv_path = tk.StringVar()
        self.output_dir = tk.StringVar(value='./qr-output')
        self.data_column = tk.StringVar()
        self.name_column = tk.StringVar()
        self.size = tk.IntVar(value=10)
        self.error_level = tk.StringVar(value='M')
        self.format = tk.StringVar(value='PNG')

        self.setup_styles()
        self.create_widgets()

    def setup_styles(self):
        """Configure ttk styles."""
        style = ttk.Style()
        style.theme_use('clam')

        style.configure('Dark.TFrame', background='#1e1e2e')
        style.configure('Dark.TLabel', background='#1e1e2e', foreground='#cdd6f4')
        style.configure('Title.TLabel', background='#1e1e2e', foreground='#f5c2e7',
                       font=('Segoe UI', 14, 'bold'))
        style.configure('Dark.TButton', background='#313244', foreground='#cdd6f4')
        style.map('Dark.TButton', background=[('active', '#45475a')])
        style.configure('Dark.TEntry', fieldbackground='#313244', foreground='#cdd6f4')
        style.configure('Dark.TCombobox', fieldbackground='#313244', foreground='#cdd6f4')
        style.configure('Dark.TSpinbox', fieldbackground='#313244', foreground='#cdd6f4')

    def create_widgets(self):
        """Create GUI widgets."""
        main_frame = ttk.Frame(self.root, style='Dark.TFrame')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)

        # Title
        ttk.Label(main_frame, text="QR Batch Generator", style='Title.TLabel').pack(pady=(0, 15))

        # CSV input
        ttk.Label(main_frame, text="CSV File:", style='Dark.TLabel').pack(anchor='w')
        row = ttk.Frame(main_frame, style='Dark.TFrame')
        row.pack(fill='x', pady=5)
        ttk.Entry(row, textvariable=self.csv_path, width=50).pack(side='left', fill='x', expand=True)
        ttk.Button(row, text="Browse", command=self.browse_csv).pack(side='left', padx=(5, 0))
        ttk.Button(row, text="Create Sample CSV", command=self.create_sample_csv).pack(side='left', padx=(5, 0))

        # Output directory
        ttk.Label(main_frame, text="Output Folder:", style='Dark.TLabel').pack(anchor='w', pady=(10, 0))
        row = ttk.Frame(main_frame, style='Dark.TFrame')
        row.pack(fill='x', pady=5)
        ttk.Entry(row, textvariable=self.output_dir, width=50).pack(side='left', fill='x', expand=True)
        ttk.Button(row, text="Browse", command=self.browse_output).pack(side='left', padx=(5, 0))
        ttk.Button(row, text="Open", command=self.open_output).pack(side='left', padx=(5, 0))

        # Column settings
        options_frame = ttk.LabelFrame(main_frame, text="CSV Column Settings", style='Dark.TFrame')
        options_frame.pack(fill='x', pady=15)

        row = ttk.Frame(options_frame, style='Dark.TFrame')
        row.pack(fill='x', padx=10, pady=5)
        ttk.Label(row, text="Data Column:", width=15).pack(side='left')
        ttk.Entry(row, textvariable=self.data_column, width=20).pack(side='left', padx=5)
        ttk.Label(row, text="(URL/Text)", style='Dark.TLabel').pack(side='left')

        row = ttk.Frame(options_frame, style='Dark.TFrame')
        row.pack(fill='x', padx=10, pady=5)
        ttk.Label(row, text="Name Column:", width=15).pack(side='left')
        ttk.Entry(row, textvariable=self.name_column, width=20).pack(side='left', padx=5)
        ttk.Label(row, text="(Optional, for filenames)", style='Dark.TLabel').pack(side='left')

        # QR Settings
        settings_frame = ttk.LabelFrame(main_frame, text="QR Code Settings", style='Dark.TFrame')
        settings_frame.pack(fill='x', pady=10)

        row = ttk.Frame(settings_frame, style='Dark.TFrame')
        row.pack(fill='x', padx=10, pady=5)
        ttk.Label(row, text="Module Size:").pack(side='left')
        ttk.Spinbox(row, from_=1, to=50, textvariable=self.size, width=5).pack(side='left', padx=5)
        ttk.Label(row, text="pixels", style='Dark.TLabel').pack(side='left')

        row = ttk.Frame(settings_frame, style='Dark.TFrame')
        row.pack(fill='x', padx=10, pady=5)
        ttk.Label(row, text="Error Correction:").pack(side='left')
        ttk.Combobox(row, textvariable=self.error_level, values=['L', 'M', 'Q', 'H'],
                    width=5, state='readonly').pack(side='left', padx=5)

        row = ttk.Frame(settings_frame, style='Dark.TFrame')
        row.pack(fill='x', padx=10, pady=5)
        ttk.Label(row, text="Format:").pack(side='left')
        ttk.Combobox(row, textvariable=self.format, values=['PNG', 'JPEG', 'GIF', 'BMP'],
                    width=8, state='readonly').pack(side='left', padx=5)

        # Info labels
        info_frame = ttk.Frame(settings_frame, style='Dark.TFrame')
        info_frame.pack(fill='x', padx=10, pady=5)
        ttk.Label(info_frame, text="L=7% M=15% Q=25% H=30% recovery | Larger = better quality but bigger files",
                 style='Dark.TLabel').pack()

        # Generate button
        ttk.Button(main_frame, text="Generate QR Codes", command=self.generate).pack(pady=15)

        # Log
        ttk.Label(main_frame, text="Log:", style='Dark.TLabel').pack(anchor='w')
        self.log_text = scrolledtext.ScrolledText(main_frame, height=10, bg='#181825',
                                                    fg='#a6e3a1', font=('Consolas', 8))
        self.log_text.pack(fill='both', expand=True, pady=5)

    def browse_csv(self):
        """Browse for CSV file."""
        path = filedialog.askopenfilename(
            title="Select CSV File",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if path:
            self.csv_path.set(path)
            # Auto-detect columns
            self.detect_columns(path)

    def detect_columns(self, csv_path: str):
        """Auto-detect column names from CSV."""
        try:
            with open(csv_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                headers = reader.fieldnames
                if headers:
                    self.data_column.set(headers[0] if headers else '')
        except Exception as e:
            pass

    def browse_output(self):
        """Browse for output directory."""
        folder = filedialog.askdirectory(title="Select Output Folder")
        if folder:
            self.output_dir.set(folder)

    def open_output(self):
        """Open output folder in file explorer."""
        folder = self.output_dir.get()
        if folder and os.path.exists(folder):
            os.startfile(folder) if sys.platform == 'win32' else os.system(f'open "{folder}"')

    def create_sample_csv(self):
        """Create a sample CSV file."""
        sample_data = [
            ['name', 'url'],
            ['Google', 'https://www.google.com'],
            ['GitHub', 'https://github.com'],
            ['Python', 'https://www.python.org'],
            ['Stack Overflow', 'https://stackoverflow.com'],
            ['Wikipedia', 'https://www.wikipedia.org'],
        ]

        path = filedialog.asksaveasfilename(
            title="Save Sample CSV",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")]
        )

        if path:
            with open(path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerows(sample_data)

            self.csv_path.set(path)
            self.data_column.set('url')
            self.name_column.set('name')
            messagebox.showinfo("Created", f"Sample CSV created:\n{path}")

    def log(self, msg: str):
        """Add message to log."""
        self.log_text.insert('end', msg + '\n')
        self.log_text.see('end')
        self.root.update()

    def clear_log(self):
        self.log_text.delete('1.0', 'end')

    def generate(self):
        """Generate QR codes."""
        csv_path = self.csv_path.get()
        output_dir = self.output_dir.get()

        if not csv_path:
            messagebox.showwarning("Missing Input", "Please select a CSV file.")
            return

        self.clear_log()
        self.log("Starting QR code generation...")

        generator = QRBatchGenerator(
            output_dir=output_dir,
            size=self.size.get(),
            error_correction=self.error_level.get(),
            format=self.format.get()
        )

        try:
            data_col = self.data_column.get() or None
            name_col = self.name_column.get() or None

            files = generator.process_csv(
                csv_path,
                data_column=data_col,
                name_column=name_col
            )

            for msg in generator.log:
                self.log(msg)

            if files:
                self.log(f"\nFiles saved to: {output_dir}")

            messagebox.showinfo("Complete",
                              f"Generated: {generator.stats['generated']}\n"
                              f"Skipped: {generator.stats['skipped']}\n"
                              f"Errors: {generator.stats['errors']}")

        except Exception as e:
            messagebox.showerror("Error", str(e))


def main():
    if not HAS_QR:
        print("Error: qrcode library required")
        print("Install with: pip install qrcode[pil]")
        return 1

    parser = argparse.ArgumentParser(description="QR Batch Generator")
    parser.add_argument('csv', nargs='?', help="CSV file with data")
    parser.add_argument('-o', '--output', default='./qr-output', help="Output directory")
    parser.add_argument('-d', '--data-column', help="Column name for QR data")
    parser.add_argument('-n', '--name-column', help="Column name for filenames")
    parser.add_argument('-s', '--size', type=int, default=10, help="Module size in pixels")
    parser.add_argument('-e', '--error-level', default='M', choices=['L', 'M', 'Q', 'H'],
                        help="Error correction level")
    parser.add_argument('-f', '--format', default='PNG', choices=['PNG', 'JPEG', 'GIF', 'BMP'],
                        help="Image format")
    parser.add_argument('--gui', action='store_true', help="Force GUI mode")
    parser.add_argument('--no-gui', action='store_true', help="Force CLI mode")
    parser.add_argument('--sample', action='store_true', help="Create sample CSV and exit")

    args = parser.parse_args()

    if args.sample:
        import csv
        sample = [
            ['name', 'url'],
            ['Google', 'https://www.google.com'],
            ['GitHub', 'https://github.com'],
            ['Python', 'https://www.python.org'],
        ]
        with open('sample-qr.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(sample)
        print("Sample CSV created: sample-qr.csv")
        return 0

    use_gui = (args.gui or (not args.no_gui and not args.csv and HAS_TK and sys.stdout.isatty()))

    if use_gui and HAS_TK:
        root = tk.Tk()
        QRBatchGUI(root)
        root.mainloop()
    else:
        if not args.csv:
            print("QR Batch Generator")
            print("Usage: qr-batch.py <csv_file> [options]")
            print("       qr-batch.py --gui  (to launch GUI)")
            print("       qr-batch.py --sample  (create sample CSV)")
            print("\nOptions:")
            print("  -o, --output DIR      Output directory (default: ./qr-output)")
            print("  -d, --data-column     CSV column with QR data")
            print("  -n, --name-column     CSV column for filenames")
            print("  -s, --size N          Module size in pixels (default: 10)")
            print("  -e, --error-level     L/M/Q/H (default: M)")
            print("  -f, --format          PNG/JPEG/GIF/BMP (default: PNG)")
            return 1

        generator = QRBatchGenerator(
            output_dir=args.output,
            size=args.size,
            error_correction=args.error_level,
            format=args.format
        )

        try:
            files = generator.process_csv(
                args.csv,
                data_column=args.data_column,
                name_column=args.name_column
            )

            for msg in generator.log:
                print(msg)

            return 0 if generator.stats['errors'] == 0 else 1

        except Exception as e:
            print(f"Error: {e}")
            return 1


if __name__ == '__main__':
    sys.exit(main())
