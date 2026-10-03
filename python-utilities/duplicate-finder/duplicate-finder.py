#!/usr/bin/env python3
"""
Duplicate Finder - Find duplicate files by content hash.
Scans folders, reports duplicates, optionally deletes them.
"""

import argparse
import hashlib
import os
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, List


@dataclass
class DuplicateGroup:
    """Represents a group of duplicate files."""
    hash_value: str
    files: List[Path]
    size: int

    @property
    def wasted_space(self) -> int:
        """Calculate wasted space (all copies minus one)."""
        return self.size * (len(self.files) - 1)

    @property
    def savings_percent(self) -> float:
        """Percentage of space that could be saved."""
        if not self.files:
            return 0.0
        total = self.size * len(self.files)
        return (self.wasted_space / total) * 100 if total > 0 else 0.0


def calculate_file_hash(filepath: Path, algorithm: str = "sha256") -> str:
    """Calculate hash of file contents."""
    if algorithm == "md5":
        hasher = hashlib.md5()
    elif algorithm == "sha1":
        hasher = hashlib.sha1()
    else:
        hasher = hashlib.sha256()

    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            hasher.update(chunk)

    return hasher.hexdigest()


def format_size(size_bytes: int) -> str:
    """Format bytes to human-readable string."""
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size_bytes < 1024:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.2f} PB"


def scan_directory(
    directory: Path,
    extensions: Optional[List[str]] = None,
    min_size: int = 1,
    max_size: Optional[int] = None,
    recursive: bool = True
) -> dict:
    """
    Scan directory and group files by size first (optimization).
    Only hashes files with matching sizes.
    """
    print(f"Scanning: {directory}")
    print(f"Extensions filter: {extensions or 'All'}")
    print(f"Minimum size: {format_size(min_size)}")

    size_groups = defaultdict(list)
    file_count = 0
    dir_count = 0

    # First pass: group by size
    pattern = "**/*" if recursive else "*"
    for filepath in directory.glob(pattern):
        if filepath.is_dir():
            dir_count += 1
            continue

        if extensions and filepath.suffix.lower() not in extensions:
            continue

        try:
            size = filepath.stat().st_size
            if size < min_size:
                continue
            if max_size and size > max_size:
                continue
            size_groups[size].append(filepath)
            file_count += 1
        except (OSError, PermissionError) as e:
            print(f"  Warning: Cannot access {filepath}: {e}", file=sys.stderr)

    print(f"Found {file_count} files in {dir_count} directories")
    print(f"Grouping by size...")

    # Second pass: hash only files with duplicate sizes
    hash_groups = defaultdict(list)
    hash_progress = 0
    files_to_hash = sum(1 for files in size_groups.values() if len(files) > 1)
    hashes_computed = 0

    for size, files in size_groups.items():
        if len(files) < 2:
            continue

        for filepath in files:
            hash_progress += 1
            file_hash = calculate_file_hash(filepath)
            hash_groups[file_hash].append(filepath)
            hashes_computed += 1

            if hashes_computed % 100 == 0:
                print(f"  Hashed {hashes_computed}/{files_to_hash} files...", end="\r")

    print(f"\nComputed {hashes_computed} hashes")
    return hash_groups


def find_duplicates(
    directory: Path,
    extensions: Optional[List[str]] = None,
    min_size: int = 1,
    max_size: Optional[int] = None,
    delete: bool = False,
    keep: str = "first"
) -> List[DuplicateGroup]:
    """Find duplicate files in directory."""
    hash_groups = scan_directory(directory, extensions, min_size, max_size)

    duplicates = []
    for file_hash, files in hash_groups.items():
        if len(files) > 1:
            duplicates.append(DuplicateGroup(
                hash_value=file_hash,
                files=sorted(files),
                size=files[0].stat().st_size
            ))

    # Sort by wasted space (largest waste first)
    duplicates.sort(key=lambda d: d.wasted_space, reverse=True)

    # Optionally delete duplicates
    if delete and duplicates:
        print("\n" + "=" * 60)
        print("DELETE MODE: Will remove duplicate files")
        print(f"Strategy: Keep '{keep}', delete others")
        print("=" * 60)

        deleted_total = 0
        for dup in duplicates:
            if keep == "first":
                to_delete = dup.files[1:]
            elif keep == "last":
                to_delete = dup.files[:-1]
            elif keep == "smallest":
                to_delete = [f for f in dup.files if f != min(dup.files, key=lambda p: len(p.name))]
            else:  # newest
                to_delete = sorted(dup.files, key=lambda p: p.stat().st_mtime)[1:]

            for filepath in to_delete:
                try:
                    filepath.unlink()
                    print(f"  Deleted: {filepath}")
                    deleted_total += 1
                except OSError as e:
                    print(f"  Failed to delete {filepath}: {e}", file=sys.stderr)

        print(f"\nDeleted {deleted_total} duplicate files")

    return duplicates


def print_report(duplicates: List[DuplicateGroup], show_hashes: bool = False) -> None:
    """Print duplicate files report."""
    if not duplicates:
        print("\nNo duplicate files found!")
        return

    total_wasted = sum(d.wasted_space for d in duplicates)
    total_duplicates = sum(len(d.files) - 1 for d in duplicates)

    print("\n" + "=" * 70)
    print("DUPLICATE FILES REPORT")
    print("=" * 70)
    print(f"Found {len(duplicates)} groups of duplicates")
    print(f"Total duplicate files: {total_duplicates}")
    print(f"Wasted space: {format_size(total_wasted)}")
    print("=" * 70)

    for i, dup in enumerate(duplicates, 1):
        print(f"\n[{i}] Duplicate Group - {len(dup.files)} files")
        print(f"    Size per file: {format_size(dup.size)}")
        print(f"    Wasted space: {format_size(dup.wasted_space)} ({dup.savings_percent:.1f}%)")
        if show_hashes:
            print(f"    Hash: {dup.hash_value}")
        print(f"    Files:")
        for j, filepath in enumerate(dup.files):
            try:
                mtime = filepath.stat().st_mtime
                mtime_str = f" (modified: {mtime})"
            except OSError:
                mtime_str = ""
            marker = " [KEEP]" if j == 0 else ""
            print(f"      {j+1}. {filepath}{marker}{mtime_str}")

    print("\n" + "=" * 70)
    print(f"Total wasted space: {format_size(total_wasted)}")
    if total_wasted > 0:
        print(f"Potential savings: Run with --delete to free up space")
    print("=" * 70)


def main():
    parser = argparse.ArgumentParser(
        description="Find duplicate files by content hash.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Scan current directory:
    python duplicate-finder.py .

  Scan with specific extensions:
    python duplicate-finder.py . --extensions .jpg .png .mp4

  Only show large duplicates (>1MB):
    python duplicate-finder.py . --min-size 1048576

  Show hashes in report:
    python duplicate-finder.py . --show-hashes

  Delete duplicates (keeps first found):
    python duplicate-finder.py . --delete --keep first

  Delete duplicates (keeps newest):
    python duplicate-finder.py . --delete --keep newest
        """
    )

    parser.add_argument("directory", type=Path, help="Directory to scan")
    parser.add_argument("-e", "--extensions", nargs="+", metavar="EXT",
                        help="File extensions to include (e.g., .jpg .png)")
    parser.add_argument("--min-size", type=int, default=1,
                        help="Minimum file size in bytes (default: 1)")
    parser.add_argument("--max-size", type=int,
                        help="Maximum file size in bytes")
    parser.add_argument("-s", "--show-hashes", action="store_true",
                        help="Show file hashes in report")
    parser.add_argument("-d", "--delete", action="store_true",
                        help="Delete duplicate files (keeps one)")
    parser.add_argument("-k", "--keep", choices=["first", "last", "smallest", "newest"],
                        default="first",
                        help="Which file to keep (default: first)")

    args = parser.parse_args()

    if not args.directory.exists():
        print(f"Error: Directory not found: {args.directory}")
        sys.exit(1)

    # Process extensions
    extensions = None
    if args.extensions:
        extensions = [ext if ext.startswith(".") else f".{ext}" for ext in args.extensions]
        extensions = [e.lower() for e in extensions]

    duplicates = find_duplicates(
        args.directory,
        extensions=extensions,
        min_size=args.min_size,
        max_size=args.max_size,
        delete=args.delete,
        keep=args.keep
    )

    print_report(duplicates, show_hashes=args.show_hashes)


if __name__ == "__main__":
    main()
