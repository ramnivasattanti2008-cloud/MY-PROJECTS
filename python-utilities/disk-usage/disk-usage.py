#!/usr/bin/env python3
"""
Disk Usage Analyzer - Analyze disk usage and visualize largest files/folders.
Shows largest files/folders with visual bar charts.
"""

import argparse
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple, Optional


@dataclass
class FileInfo:
    """Information about a file or directory."""
    path: Path
    size: int
    is_dir: bool


def format_size(size_bytes: int) -> str:
    """Format bytes to human-readable string."""
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size_bytes < 1024:
            return f"{size_bytes:>10.2f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:>10.2f} PB"


def format_path(path: Path, max_len: int = 50) -> str:
    """Format path with ellipsis if too long."""
    path_str = str(path)
    if len(path_str) > max_len:
        return "..." + path_str[-(max_len-3):]
    return path_str


def scan_directory(directory: Path, max_depth: Optional[int] = None) -> dict:
    """Recursively scan directory and return sizes."""
    sizes = {}
    total_size = 0
    dir_count = 0
    file_count = 0

    def scan(path: Path, depth: int = 0) -> int:
        nonlocal total_size, dir_count, file_count

        if max_depth is not None and depth > max_depth:
            return 0

        size = 0
        try:
            for entry in path.iterdir():
                try:
                    if entry.is_symlink():
                        continue
                    if entry.is_file():
                        size += entry.stat().st_size
                        file_count += 1
                        sizes[entry] = size
                    elif entry.is_dir():
                        dir_count += 1
                        sub_size = scan(entry, depth + 1)
                        size += sub_size
                        sizes[entry] = sub_size
                except (PermissionError, OSError):
                    pass
        except (PermissionError, OSError):
            pass

        total_size += size
        return size

    scan(directory)
    return {"sizes": sizes, "total": total_size, "dirs": dir_count, "files": file_count}


def get_largest_items(sizes: dict, n: int = 20) -> List[FileInfo]:
    """Get N largest items from size dictionary."""
    items = [
        FileInfo(path=path, size=size, is_dir=path.is_dir())
        for path, size in sizes.items()
    ]
    items.sort(key=lambda x: x.size, reverse=True)
    return items[:n]


def get_directory_tree(directory: Path, max_depth: int = 3) -> List[Tuple[int, Path, int]]:
    """
    Get directory tree structure with sizes.
    Returns list of (depth, path, size) tuples.
    """
    result = []

    def walk(path: Path, depth: int = 0) -> int:
        total = 0
        try:
            for entry in path.iterdir():
                try:
                    if entry.is_symlink():
                        continue
                    if entry.is_file():
                        size = entry.stat().st_size
                        total += size
                        result.append((depth + 1, entry, size))
                    elif entry.is_dir():
                        size = walk(entry, depth + 1)
                        total += size
                        if depth < max_depth:
                            result.append((depth + 1, entry, size))
                except (PermissionError, OSError):
                    pass
        except (PermissionError, OSError):
            pass

        return total

    result.append((0, directory, walk(directory)))
    return result


def draw_bar_chart(items: List[FileInfo], max_width: int = 50, max_items: int = 15) -> None:
    """Draw a horizontal bar chart of file/folder sizes."""
    if not items:
        return

    max_size = items[0].size
    display_items = items[:max_items]

    print("\n" + "=" * 80)
    print("DISK USAGE BAR CHART")
    print("=" * 80)

    for item in display_items:
        bar_len = int((item.size / max_size) * max_width)
        bar = "█" * bar_len
        size_str = format_size(item.size)
        icon = "[D]" if item.is_dir else "[F]"
        path_str = format_path(item.path, 40)

        print(f"{size_str} {icon} {bar} {path_str}")


def print_tree_view(directory: Path, max_depth: int = 3) -> None:
    """Print directory tree with sizes."""
    tree = get_directory_tree(directory, max_depth)

    print("\n" + "=" * 80)
    print("DIRECTORY TREE")
    print("=" * 80)

    max_size = max(size for _, _, size in tree) if tree else 1

    for depth, path, size in tree:
        indent = "  " * depth
        icon = "+-- " if path.is_dir() else ""
        bar_len = int((size / max_size) * 20)
        bar = "▓" * bar_len
        size_str = format_size(size).strip()

        if depth == 0:
            print(f"{indent}{path}/ {size_str}")
        else:
            name = path.name + "/" if path.is_dir() else path.name
            print(f"{indent}{icon}{name} {size_str}")


def print_summary(result: dict, directory: Path) -> None:
    """Print scan summary."""
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Directory:     {directory}")
    print(f"Total size:    {format_size(result['total'])}")
    print(f"Files:         {result['files']:,}")
    print(f"Directories:   {result['dirs']:,}")
    print("=" * 80)


def print_top_files(items: List[FileInfo], title: str = "LARGEST ITEMS") -> None:
    """Print top files/folders in table format."""
    if not items:
        return

    print(f"\n{title}")
    print("-" * 80)
    print(f"{'Size':>14}  {'Type':<6}  Path")
    print("-" * 80)

    for item in items:
        item_type = "DIR " if item.is_dir else "FILE"
        size_str = format_size(item.size)
        path_str = str(item.path)
        print(f"{size_str}  {item_type:<6}  {path_str}")


def analyze_by_extension(sizes: dict) -> dict:
    """Analyze sizes grouped by file extension."""
    ext_sizes = {}

    for path, size in sizes.items():
        if path.is_file():
            ext = path.suffix.lower() or "(no extension)"
            ext_sizes[ext] = ext_sizes.get(ext, 0) + size

    return sorted(ext_sizes.items(), key=lambda x: x[1], reverse=True)


def print_extension_breakdown(ext_sizes: List[Tuple[str, int]]) -> None:
    """Print breakdown by file extension."""
    if not ext_sizes:
        return

    print("\n" + "=" * 80)
    print("BREAKDOWN BY FILE TYPE")
    print("=" * 80)

    max_size = ext_sizes[0][1]
    max_width = 40

    for ext, size in ext_sizes[:20]:
        bar_len = int((size / max_size) * max_width)
        bar = "█" * bar_len
        size_str = format_size(size)
        print(f"{size_str}  {ext:<20} {bar}")


def main():
    parser = argparse.ArgumentParser(
        description="Analyze disk usage and visualize largest files/folders.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Analyze current directory:
    python disk-usage.py

  Analyze specific directory:
    python disk-usage.py /home/user/documents

  Show top 50 items:
    python disk-usage.py . -n 50

  Directory tree view:
    python disk-usage.py . --tree

  Don't show bar chart:
    python disk-usage.py . --no-chart

  Max directory depth:
    python disk-usage.py /home -d 5
        """
    )

    parser.add_argument("directory", type=Path, nargs="?", default=Path("."),
                        help="Directory to analyze (default: current)")
    parser.add_argument("-n", "--number", type=int, default=20,
                        help="Number of items to show (default: 20)")
    parser.add_argument("-t", "--tree", action="store_true",
                        help="Show directory tree view")
    parser.add_argument("--no-chart", action="store_true",
                        help="Don't show bar chart")
    parser.add_argument("-d", "--depth", type=int,
                        help="Maximum directory depth for tree view")
    parser.add_argument("--extensions", action="store_true",
                        help="Show breakdown by file extension")

    args = parser.parse_args()

    if not args.directory.exists():
        print(f"Error: Directory not found: {args.directory}")
        sys.exit(1)

    print(f"Analyzing: {args.directory}")
    print("Scanning...")

    result = scan_directory(args.directory)

    print_summary(result, args.directory)

    largest = get_largest_items(result["sizes"], args.number)
    print_top_files(largest)

    if not args.no_chart:
        draw_bar_chart(largest, max_items=args.number)

    if args.tree:
        print_tree_view(args.directory, args.depth or 3)

    if args.extensions:
        ext_sizes = analyze_by_extension(result["sizes"])
        print_extension_breakdown(ext_sizes)

    print()


if __name__ == "__main__":
    main()
