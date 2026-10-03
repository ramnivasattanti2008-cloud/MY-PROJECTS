#!/usr/bin/env python3
"""
File Hasher - Calculate MD5, SHA1, SHA256 hashes for files.
Supports drag & drop (GUI mode) or CLI arguments.
"""

import hashlib
import sys
import os
import argparse
from pathlib import Path

try:
    import tkinter as tk
    from tkinter import ttk, filedialog, messagebox
    HAS_TK = True
except ImportError:
    HAS_TK = False


def calculate_hash(filepath: str, algorithm: str = 'sha256', chunk_size: int = 65536) -> str:
    """Calculate hash of a file using specified algorithm."""
    algorithms = {
        'md5': hashlib.md5,
        'sha1': hashlib.sha1,
        'sha256': hashlib.sha256,
        'sha512': hashlib.sha512
    }

    if algorithm.lower() not in algorithms:
        raise ValueError(f"Unsupported algorithm: {algorithm}")

    hasher = algorithms[algorithm.lower()]()

    with open(filepath, 'rb') as f:
        while chunk := f.read(chunk_size):
            hasher.update(chunk)

    return hasher.hexdigest()


def format_file_size(size_bytes: int) -> str:
    """Format file size in human-readable format."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.2f} PB"


def hash_file(filepath: str) -> dict:
    """Calculate all hashes for a file."""
    file_size = os.path.getsize(filepath)
    return {
        'path': filepath,
        'size': file_size,
        'size_formatted': format_file_size(file_size),
        'md5': calculate_hash(filepath, 'md5'),
        'sha1': calculate_hash(filepath, 'sha1'),
        'sha256': calculate_hash(filepath, 'sha256'),
        'sha512': calculate_hash(filepath, 'sha512')
    }


def print_hash_result(result: dict, verbose: bool = False):
    """Print hash result in formatted output."""
    print(f"\n{'='*60}")
    print(f"File: {result['path']}")
    print(f"Size: {result['size_formatted']} ({result['size']:,} bytes)")
    print(f"{'='*60}")
    print(f"MD5:    {result['md5']}")
    print(f"SHA1:   {result['sha1']}")
    print(f"SHA256: {result['sha256']}")
    if verbose:
        print(f"SHA512: {result['sha512']}")
    print(f"{'='*60}")


def verify_file(filepath: str, expected_hash: str, algorithm: str = 'sha256') -> bool:
    """Verify a file against an expected hash."""
    actual = calculate_hash(filepath, algorithm)
    match = actual.lower() == expected_hash.lower()
    return match, actual


class HashGUI:
    """GUI for file hashing with drag & drop support."""

    def __init__(self, root):
        self.root = root
        self.root.title("File Hasher")
        self.root.geometry("600x500")
        self.root.configure(bg='#1e1e2e')

        self.setup_styles()
        self.create_widgets()

        # Configure drag & drop
        self.root.drop_target_register('DND_Files')
        self.root.dnd_bind('<<Drop>>', self.handle_drop)

    def setup_styles(self):
        """Configure ttk styles for dark theme."""
        style = ttk.Style()
        style.theme_use('clam')

        style.configure('Dark.TFrame', background='#1e1e2e')
        style.configure('Dark.TLabel', background='#1e1e2e', foreground='#cdd6f4', font=('Segoe UI', 10))
        style.configure('Title.TLabel', background='#1e1e2e', foreground='#f5c2e7', font=('Segoe UI', 16, 'bold'))
        style.configure('Hash.TLabel', background='#181825', foreground='#a6e3a1', font=('Consolas', 9))
        style.configure('Dark.TButton', background='#313244', foreground='#cdd6f4', font=('Segoe UI', 10))
        style.map('Dark.TButton', background=[('active', '#45475a')])

    def create_widgets(self):
        """Create GUI widgets."""
        main_frame = ttk.Frame(self.root, style='Dark.TFrame')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)

        # Title
        ttk.Label(main_frame, text="File Hasher", style='Title.TLabel').pack(pady=(0, 10))
        ttk.Label(main_frame, text="Drag & drop files or click Browse", style='Dark.TLabel').pack(pady=(0, 20))

        # Drop zone
        self.drop_frame = tk.Frame(main_frame, bg='#313244', relief='solid', bd=2, width=500, height=150)
        self.drop_frame.pack(pady=10)
        self.drop_frame.pack_propagate(False)

        self.drop_label = tk.Label(self.drop_frame, text="Drop files here", bg='#313244', fg='#6c7086',
                                   font=('Segoe UI', 14))
        self.drop_label.place(relx=0.5, rely=0.5, anchor='center')

        # Browse button
        ttk.Button(main_frame, text="Browse Files", command=self.browse_files, style='Dark.TButton').pack(pady=10)

        # Results frame
        self.results_frame = ttk.Frame(main_frame, style='Dark.TFrame')
        self.results_frame.pack(fill='both', expand=True, pady=10)

        self.result_labels = {}
        algorithms = ['MD5', 'SHA1', 'SHA256', 'SHA512']

        for i, algo in enumerate(algorithms):
            row = ttk.Frame(self.results_frame, style='Dark.TFrame')
            row.pack(fill='x', pady=2)

            ttk.Label(row, text=f"{algo}:", width=8, style='Dark.TLabel').pack(side='left')

            label = tk.Label(row, text="-", bg='#181825', fg='#a6e3a1', font=('Consolas', 9),
                           anchor='w', padx=5, width=70)
            label.pack(side='left', fill='x', expand=True)
            self.result_labels[algo] = label

        # Copy buttons
        btn_frame = ttk.Frame(main_frame, style='Dark.TFrame')
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="Copy All", command=self.copy_all, style='Dark.TButton').pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Clear", command=self.clear_results, style='Dark.TButton').pack(side='left', padx=5)

        # File info
        self.info_label = ttk.Label(main_frame, text="", style='Dark.TLabel')
        self.info_label.pack(pady=5)

    def handle_drop(self, event):
        """Handle file drop event."""
        files = self.root.tk.splitlist(event.data)
        if files:
            self.process_file(files[0])

    def browse_files(self):
        """Open file browser dialog."""
        filepath = filedialog.askopenfilename(title="Select a file to hash")
        if filepath:
            self.process_file(filepath)

    def process_file(self, filepath: str):
        """Process and display file hashes."""
        try:
            result = hash_file(filepath)

            self.result_labels['MD5'].config(text=result['md5'])
            self.result_labels['SHA1'].config(text=result['sha1'])
            self.result_labels['SHA256'].config(text=result['sha256'])
            self.result_labels['SHA512'].config(text=result['sha512'])

            self.info_label.config(text=f"File: {os.path.basename(filepath)} | Size: {result['size_formatted']}")
            self.drop_label.config(text=os.path.basename(filepath), fg='#cdd6f4')

        except Exception as e:
            messagebox.showerror("Error", f"Failed to hash file:\n{str(e)}")

    def copy_all(self):
        """Copy all hashes to clipboard."""
        text = '\n'.join([f"{algo}: {label.cget('text')}" for algo, label in self.result_labels.items()])
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        messagebox.showinfo("Copied", "All hashes copied to clipboard!")

    def clear_results(self):
        """Clear all results."""
        for label in self.result_labels.values():
            label.config(text="-")
        self.info_label.config(text="")
        self.drop_label.config(text="Drop files here", fg='#6c7086')


def main():
    parser = argparse.ArgumentParser(description="File Hasher - Calculate file hashes")
    parser.add_argument('files', nargs='*', help="Files to hash")
    parser.add_argument('-a', '--algorithm', default='sha256', choices=['md5', 'sha1', 'sha256', 'sha512'],
                       help="Hash algorithm (default: sha256)")
    parser.add_argument('-v', '--verbose', action='store_true', help="Show all hash types")
    parser.add_argument('--verify', help="Verify against expected hash")
    parser.add_argument('--gui', action='store_true', help="Force GUI mode")
    parser.add_argument('--no-gui', action='store_true', help="Force CLI mode")

    args = parser.parse_args()

    # Determine mode
    use_gui = (args.gui or (not args.no_gui and not args.files and HAS_TK and sys.stdout.isatty()))

    if use_gui and HAS_TK:
        root = tk.Tk()
        HashGUI(root)
        root.mainloop()
    else:
        if not args.files:
            print("File Hasher - Calculate file hashes")
            print("Usage: file-hasher.py [-a ALGORITHM] [-v] <files...>")
            print("       file-hasher.py --gui  (to launch GUI)")
            print("\nAlgorithms: md5, sha1, sha256, sha512 (default: sha256)")
            print("Examples:")
            print("  file-hasher.py document.pdf")
            print("  file-hasher.py -a md5 -v file1.txt file2.txt")
            print("  file-hasher.py --verify abc123 file.txt")
            return 1

        for filepath in args.files:
            if not os.path.exists(filepath):
                print(f"Error: File not found: {filepath}")
                continue

            try:
                if args.verify:
                    match, actual = verify_file(filepath, args.verify, args.algorithm)
                    status = "MATCH" if match else "MISMATCH"
                    print(f"\n{filepath}: {status}")
                    print(f"Expected: {args.verify}")
                    print(f"Actual:   {actual}")
                else:
                    result = hash_file(filepath)
                    print_hash_result(result, args.verbose)
            except Exception as e:
                print(f"Error processing {filepath}: {e}")

        return 0


if __name__ == '__main__':
    sys.exit(main())
