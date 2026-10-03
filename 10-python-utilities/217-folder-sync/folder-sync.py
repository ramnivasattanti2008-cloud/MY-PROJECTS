#!/usr/bin/env python3
"""
Folder Sync - Synchronize two folders by copying new and modified files.
"""

import os
import sys
import shutil
import argparse
from pathlib import Path
from datetime import datetime
from typing import List, Tuple, Optional

try:
    import tkinter as tk
    from tkinter import ttk, filedialog, messagebox, scrolledtext
    HAS_TK = True
except ImportError:
    HAS_TK = False


class FolderSync:
    """Main folder synchronization engine."""

    def __init__(self, source: str, dest: str, delete_orphans: bool = False,
                 dry_run: bool = False, verbose: bool = True):
        self.source = Path(source).resolve()
        self.dest = Path(dest).resolve()
        self.delete_orphans = delete_orphans
        self.dry_run = dry_run
        self.verbose = verbose

        self.stats = {
            'copied': 0,
            'skipped': 0,
            'deleted': 0,
            'errors': 0,
            'total_size': 0
        }

        self.log = []

    def log_msg(self, msg: str, level: str = 'info'):
        """Log a message."""
        timestamp = datetime.now().strftime('%H:%M:%S')
        formatted = f"[{timestamp}] {msg}"
        self.log.append((level, formatted))
        if self.verbose:
            print(formatted)

    def get_file_hash(self, filepath: Path) -> str:
        """Get modification time as proxy for change detection."""
        return str(filepath.stat().st_mtime)

    def should_copy(self, src_file: Path, dst_file: Path) -> bool:
        """Determine if file should be copied."""
        if not dst_file.exists():
            return True

        # Compare by size and modification time
        src_stat = src_file.stat()
        dst_stat = dst_file.stat()

        # Copy if source is newer or different size
        if src_stat.st_size != dst_stat.st_size:
            return True
        if src_stat.st_mtime > dst_stat.st_mtime + 1:  # 1 second tolerance
            return True

        return False

    def sync_file(self, src_file: Path, rel_path: Path) -> bool:
        """Sync a single file."""
        dst_file = self.dest / rel_path

        try:
            # Ensure destination directory exists
            dst_file.parent.mkdir(parents=True, exist_ok=True)

            if self.should_copy(src_file, dst_file):
                if self.dry_run:
                    self.log_msg(f"[DRY RUN] Would copy: {rel_path}", 'dry')
                else:
                    shutil.copy2(src_file, dst_file)
                    self.log_msg(f"Copied: {rel_path}", 'copy')

                self.stats['copied'] += 1
                self.stats['total_size'] += src_file.stat().st_size
                return True
            else:
                self.log_msg(f"Skipped (unchanged): {rel_path}", 'skip')
                self.stats['skipped'] += 1
                return False

        except Exception as e:
            self.log_msg(f"ERROR copying {rel_path}: {e}", 'error')
            self.stats['errors'] += 1
            return False

    def sync_folders(self) -> dict:
        """Synchronize source to destination."""
        self.log = []
        self.stats = {'copied': 0, 'skipped': 0, 'deleted': 0, 'errors': 0, 'total_size': 0}

        if not self.source.exists():
            raise FileNotFoundError(f"Source folder not found: {self.source}")

        # Create destination if it doesn't exist
        if not self.dest.exists() and not self.dry_run:
            self.dest.mkdir(parents=True, exist_ok=True)
            self.log_msg(f"Created destination folder: {self.dest}")

        self.log_msg(f"Syncing: {self.source} -> {self.dest}")
        self.log_msg("-" * 50)

        # Collect all files in source
        source_files = []
        for root, dirs, files in os.walk(self.source):
            for filename in files:
                src_file = Path(root) / filename
                rel_path = src_file.relative_to(self.source)
                source_files.append((src_file, rel_path))

        self.log_msg(f"Found {len(source_files)} files in source")

        # Sync each file
        for src_file, rel_path in source_files:
            self.sync_file(src_file, rel_path)

        # Delete orphans if requested
        if self.delete_orphans and not self.dry_run:
            orphans = self.find_orphans()
            for orphan in orphans:
                try:
                    orphan_path = self.dest / orphan
                    orphan_path.unlink()
                    self.log_msg(f"Deleted orphan: {orphan}", 'delete')
                    self.stats['deleted'] += 1
                except Exception as e:
                    self.log_msg(f"ERROR deleting {orphan}: {e}", 'error')
                    self.stats['errors'] += 1

        self.log_msg("-" * 50)
        self.log_msg(f"Done! Copied: {self.stats['copied']}, Skipped: {self.stats['skipped']}, "
                    f"Deleted: {self.stats['deleted']}, Errors: {self.stats['errors']}")

        if self.stats['total_size'] > 0:
            size_mb = self.stats['total_size'] / (1024 * 1024)
            self.log_msg(f"Total data copied: {size_mb:.2f} MB")

        return self.stats

    def find_orphans(self) -> List[Path]:
        """Find files in destination that don't exist in source."""
        orphans = []

        for root, dirs, files in os.walk(self.dest):
            for filename in files:
                dst_file = Path(root) / filename
                rel_path = dst_file.relative_to(self.dest)

                if not (self.source / rel_path).exists():
                    orphans.append(rel_path)

        return orphans

    def preview_sync(self) -> Tuple[List[Tuple], List[Path], List[Path]]:
        """Preview what would be synced without making changes."""
        to_copy = []
        to_skip = []
        orphans = self.find_orphans() if self.delete_orphans else []

        for root, dirs, files in os.walk(self.source):
            for filename in files:
                src_file = Path(root) / filename
                rel_path = src_file.relative_to(self.source)
                dst_file = self.dest / rel_path

                if self.should_copy(src_file, dst_file):
                    size = src_file.stat().st_size
                    to_copy.append((str(rel_path), size))
                else:
                    to_skip.append(str(rel_path))

        return to_copy, to_skip, orphans


class SyncGUI:
    """GUI for folder synchronization."""

    def __init__(self, root):
        self.root = root
        self.root.title("Folder Sync")
        self.root.geometry("700x600")
        self.root.configure(bg='#1e1e2e')

        self.source_path = tk.StringVar()
        self.dest_path = tk.StringVar()
        self.delete_orphans = tk.BooleanVar(value=False)
        self.dry_run = tk.BooleanVar(value=True)
        self.is_syncing = False

        self.setup_styles()
        self.create_widgets()

    def setup_styles(self):
        """Configure ttk styles."""
        style = ttk.Style()
        style.theme_use('clam')

        style.configure('Dark.TFrame', background='#1e1e2e')
        style.configure('Dark.TLabel', background='#1e1e2e', foreground='#cdd6f4', font=('Segoe UI', 10))
        style.configure('Title.TLabel', background='#1e1e2e', foreground='#f5c2e7', font=('Segoe UI', 16, 'bold'))
        style.configure('Dark.TButton', background='#313244', foreground='#cdd6f4', font=('Segoe UI', 10))
        style.map('Dark.TButton', background=[('active', '#45475a')])
        style.configure('Dark.TEntry', fieldbackground='#313244', foreground='#cdd6f4')
        style.configure('Dark.TCheckbutton', background='#1e1e2e', foreground='#cdd6f4')
        style.configure('Dark.TRadiobutton', background='#1e1e2e', foreground='#cdd6f4')

    def create_widgets(self):
        """Create GUI widgets."""
        main_frame = ttk.Frame(self.root, style='Dark.TFrame')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)

        # Title
        ttk.Label(main_frame, text="Folder Sync", style='Title.TLabel').pack(pady=(0, 20))

        # Source folder
        ttk.Label(main_frame, text="Source Folder:", style='Dark.TLabel').pack(anchor='w')
        source_frame = ttk.Frame(main_frame, style='Dark.TFrame')
        source_frame.pack(fill='x', pady=(5, 10))
        ttk.Entry(source_frame, textvariable=self.source_path, width=50).pack(side='left', fill='x', expand=True)
        ttk.Button(source_frame, text="Browse", command=lambda: self.browse_folder(self.source_path)).pack(side='left', padx=(5, 0))

        # Destination folder
        ttk.Label(main_frame, text="Destination Folder:", style='Dark.TLabel').pack(anchor='w')
        dest_frame = ttk.Frame(main_frame, style='Dark.TFrame')
        dest_frame.pack(fill='x', pady=(5, 10))
        ttk.Entry(dest_frame, textvariable=self.dest_path, width=50).pack(side='left', fill='x', expand=True)
        ttk.Button(dest_frame, text="Browse", command=lambda: self.browse_folder(self.dest_path)).pack(side='left', padx=(5, 0))

        # Options
        options_frame = ttk.Frame(main_frame, style='Dark.TFrame')
        options_frame.pack(fill='x', pady=10)

        ttk.Checkbutton(options_frame, text="Delete files in destination not in source",
                       variable=self.delete_orphans, style='Dark.TCheckbutton').pack(anchor='w')

        # Dry run toggle
        mode_frame = ttk.Frame(main_frame, style='Dark.TFrame')
        mode_frame.pack(fill='x', pady=10)
        ttk.Radiobutton(mode_frame, text="Preview (Dry Run)", variable=self.dry_run, value=True,
                       style='Dark.TRadiobutton').pack(side='left', padx=10)
        ttk.Radiobutton(mode_frame, text="Execute Sync", variable=self.dry_run, value=False,
                       style='Dark.TRadiobutton').pack(side='left', padx=10)

        # Buttons
        btn_frame = ttk.Frame(main_frame, style='Dark.TFrame')
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="Preview Changes", command=self.preview).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Start Sync", command=self.start_sync).pack(side='left', padx=5)

        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.pack(fill='x', pady=10)

        # Stats
        self.stats_label = ttk.Label(main_frame, text="", style='Dark.TLabel')
        self.stats_label.pack(pady=5)

        # Log output
        ttk.Label(main_frame, text="Sync Log:", style='Dark.TLabel').pack(anchor='w')
        self.log_text = scrolledtext.ScrolledText(main_frame, height=15, bg='#181825',
                                                   fg='#a6e3a1', font=('Consolas', 9))
        self.log_text.pack(fill='both', expand=True, pady=5)

    def browse_folder(self, var: tk.StringVar):
        """Open folder browser dialog."""
        folder = filedialog.askdirectory(title="Select Folder")
        if folder:
            var.set(folder)

    def log(self, msg: str):
        """Add message to log."""
        self.log_text.insert('end', msg + '\n')
        self.log_text.see('end')
        self.root.update()

    def preview(self):
        """Preview changes without syncing."""
        source = self.source_path.get()
        dest = self.dest_path.get()

        if not source or not dest:
            messagebox.showwarning("Missing Input", "Please select both source and destination folders.")
            return

        self.log_text.delete('1.0', 'end')
        self.log("=== PREVIEW MODE ===\n")

        try:
            syncer = FolderSync(source, dest, self.delete_orphans.get(), dry_run=True)
            to_copy, to_skip, orphans = syncer.preview_sync()

            self.log(f"Files to copy: {len(to_copy)}")
            self.log(f"Files unchanged: {len(to_skip)}")
            if self.delete_orphans.get():
                self.log(f"Files to delete: {len(orphans)}")
            self.log("")

            if to_copy:
                self.log("--- Files to copy ---")
                for path, size in to_copy[:20]:
                    self.log(f"  + {path} ({size:,} bytes)")
                if len(to_copy) > 20:
                    self.log(f"  ... and {len(to_copy) - 20} more")

            if orphans:
                self.log("\n--- Files to delete ---")
                for path in orphans[:20]:
                    self.log(f"  - {path}")
                if len(orphans) > 20:
                    self.log(f"  ... and {len(orphans) - 20} more")

            total_size = sum(size for _, size in to_copy)
            self.log(f"\nTotal data to copy: {total_size / (1024*1024):.2f} MB")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def start_sync(self):
        """Start the synchronization."""
        source = self.source_path.get()
        dest = self.dest_path.get()

        if not source or not dest:
            messagebox.showwarning("Missing Input", "Please select both source and destination folders.")
            return

        if self.dry_run.get():
            self.preview()
            messagebox.showinfo("Dry Run", "Preview complete. Select 'Execute Sync' to make changes.")
            return

        self.log_text.delete('1.0', 'end')
        self.log("=== SYNCING ===\n")
        self.progress.start()

        try:
            syncer = FolderSync(source, dest, self.delete_orphans.get(), dry_run=False)
            stats = syncer.sync_folders()

            self.progress.stop()

            self.stats_label.config(text=f"Copied: {stats['copied']} | Skipped: {stats['skipped']} | "
                                        f"Deleted: {stats['deleted']} | Errors: {stats['errors']}")

            for _, msg in syncer.log:
                self.log(msg)

            if stats['errors'] == 0:
                messagebox.showinfo("Success", f"Sync complete!\n\n"
                                              f"Copied: {stats['copied']}\n"
                                              f"Skipped: {stats['skipped']}\n"
                                              f"Deleted: {stats['deleted']}")
            else:
                messagebox.showwarning("Completed with Errors",
                                      f"Copied: {stats['copied']}, Errors: {stats['errors']}")

        except Exception as e:
            self.progress.stop()
            messagebox.showerror("Error", str(e))


def main():
    parser = argparse.ArgumentParser(description="Folder Sync - Synchronize two folders")
    parser.add_argument('source', nargs='?', help="Source folder path")
    parser.add_argument('destination', nargs='?', help="Destination folder path")
    parser.add_argument('-d', '--delete', action='store_true', help="Delete files in destination not in source")
    parser.add_argument('--dry-run', action='store_true', help="Preview without copying")
    parser.add_argument('-q', '--quiet', action='store_true', help="Suppress verbose output")
    parser.add_argument('--gui', action='store_true', help="Force GUI mode")
    parser.add_argument('--no-gui', action='store_true', help="Force CLI mode")

    args = parser.parse_args()

    # Determine mode
    use_gui = (args.gui or (not args.no_gui and not args.source and HAS_TK and sys.stdout.isatty()))

    if use_gui and HAS_TK:
        root = tk.Tk()
        SyncGUI(root)
        root.mainloop()
    else:
        if not args.source or not args.destination:
            print("Folder Sync - Synchronize two folders")
            print("Usage: folder-sync.py <source> <destination> [options]")
            print("       folder-sync.py --gui  (to launch GUI)")
            print("\nOptions:")
            print("  -d, --delete       Delete files in destination not in source")
            print("  --dry-run          Preview changes without copying")
            print("  -q, --quiet        Suppress verbose output")
            print("\nExamples:")
            print("  folder-sync.py ./backup /mnt/usb/backup")
            print("  folder-sync.py ./source ./dest --dry-run")
            print("  folder-sync.py ./source ./dest -d  # Also delete orphans")
            return 1

        try:
            syncer = FolderSync(
                args.source,
                args.destination,
                delete_orphans=args.delete,
                dry_run=args.dry_run,
                verbose=not args.quiet
            )
            stats = syncer.sync_folders()

            if stats['errors'] > 0:
                return 2
            return 0

        except Exception as e:
            print(f"Error: {e}")
            return 1


if __name__ == '__main__':
    sys.exit(main())
