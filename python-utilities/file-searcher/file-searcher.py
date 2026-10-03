#!/usr/bin/env python3
"""
File Searcher - Fast file search by name, content, size, and date.
Usage: python file-searcher.py [options] [path]
"""

import os
import re
import argparse
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Optional


class FileSearcher:
    """Fast file search engine with multiple criteria."""

    def __init__(self, root_path: str):
        self.root_path = Path(root_path)
        self.results = []

    def search_by_name(self, pattern: str, regex: bool = False,
                       case_sensitive: bool = False) -> List[Path]:
        """Search files by name pattern."""
        self.results = []

        if regex:
            flags = 0 if case_sensitive else re.IGNORECASE
            compiled = re.compile(pattern, flags)

            for path in self._fast_walk():
                if path.is_file() and compiled.search(path.name):
                    self.results.append(path)
        else:
            search_term = pattern if case_sensitive else pattern.lower()
            for path in self._fast_walk():
                if path.is_file():
                    name = path.name if case_sensitive else path.name.lower()
                    if search_term in name:
                        self.results.append(path)

        return self.results

    def search_by_content(self, pattern: str, extensions: List[str] = None,
                          regex: bool = False, case_sensitive: bool = False,
                          max_size_mb: float = 10) -> List[dict]:
        """Search files by content."""
        self.results = []
        compiled = None

        if regex:
            flags = 0 if case_sensitive else re.IGNORECASE
            compiled = re.compile(pattern, flags)

        search_term = None if regex else (pattern if case_sensitive else pattern.lower())

        for path in self._fast_walk():
            if not path.is_file():
                continue

            # Skip binary files and large files
            try:
                size_mb = path.stat().st_size / (1024 * 1024)
                if size_mb > max_size_mb:
                    continue
            except OSError:
                continue

            # Filter by extension if specified
            if extensions:
                if path.suffix.lower() not in [ext.lower() for ext in extensions]:
                    continue

            # Search content
            try:
                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    for line_num, line in enumerate(f, 1):
                        check_line = line if case_sensitive else line.lower()
                        check_pattern = line if regex else search_term

                        if regex:
                            matches = compiled.finditer(check_line)
                            for match in matches:
                                self.results.append({
                                    'path': path,
                                    'line': line_num,
                                    'content': line.strip(),
                                    'match': match.group() if regex else pattern
                                })
                                break  # One match per line
                        else:
                            if check_pattern in check_line:
                                self.results.append({
                                    'path': path,
                                    'line': line_num,
                                    'content': line.strip(),
                                    'match': pattern
                                })
                                break  # One match per file
            except (OSError, UnicodeDecodeError):
                continue

        return self.results

    def search_by_size(self, min_size: int = None, max_size: int = None,
                       size_unit: str = 'b') -> List[Path]:
        """Search files by size constraints."""
        self.results = []
        units = {'b': 1, 'kb': 1024, 'mb': 1024**2, 'gb': 1024**3}
        multiplier = units.get(size_unit.lower(), 1)

        min_bytes = (min_size * multiplier) if min_size else 0
        max_bytes = (max_size * multiplier) if max_size else float('inf')

        for path in self._fast_walk():
            if not path.is_file():
                continue
            try:
                size = path.stat().st_size
                if min_bytes <= size <= max_bytes:
                    self.results.append(path)
            except OSError:
                continue

        return self.results

    def search_by_date(self, days: int = None, start_date: str = None,
                       end_date: str = None, date_type: str = 'modified') -> List[Path]:
        """Search files by modification/access/creation date."""
        self.results = []

        # Parse dates
        if days:
            cutoff = datetime.now() - timedelta(days=days)
        else:
            cutoff = None
            if start_date:
                start_dt = datetime.strptime(start_date, '%Y-%m-%d')
            if end_date:
                end_dt = datetime.strptime(end_date, '%Y-%m-%d')

        for path in self._fast_walk():
            if not path.is_file():
                continue
            try:
                stat = path.stat()
                if date_type == 'modified':
                    file_date = datetime.fromtimestamp(stat.st_mtime)
                elif date_type == 'accessed':
                    file_date = datetime.fromtimestamp(stat.st_atime)
                elif date_type == 'created':
                    file_date = datetime.fromtimestamp(stat.st_ctime)
                else:
                    continue

                if days:
                    if file_date >= cutoff:
                        self.results.append(path)
                else:
                    if start_date and file_date < start_dt:
                        continue
                    if end_date and file_date > end_dt:
                        continue
                    self.results.append(path)
            except OSError:
                continue

        return self.results

    def _fast_walk(self):
        """Fast directory traversal using os.scandir."""
        try:
            for entry in os.scandir(self.root_path):
                yield Path(entry.path)
        except PermissionError:
            pass

    def format_results(self, show_path: bool = True, show_size: bool = False,
                       show_date: bool = False) -> str:
        """Format search results as string."""
        if not self.results:
            return "No results found."

        output = []
        if isinstance(self.results[0], dict):
            # Content search results
            for item in self.results:
                path = item['path']
                line = item['line']
                content = item['content'][:80] + ('...' if len(item['content']) > 80 else '')

                if show_path and show_size:
                    size = path.stat().st_size if path.exists() else 0
                    output.append(f"[{self._format_size(size)}] {path} (line {line})")
                elif show_path:
                    output.append(f"{path} (line {line})")
                else:
                    output.append(f"{path.name} (line {line})")

                output.append(f"  -> {content}")
        else:
            # File path results
            for path in self.results:
                line_parts = []

                if show_path:
                    line_parts.append(str(path))
                else:
                    line_parts.append(path.name)

                if show_size:
                    try:
                        size = path.stat().st_size
                        line_parts.insert(0, f"[{self._format_size(size)}]")
                    except OSError:
                        line_parts.insert(0, "[?B]")

                if show_date:
                    try:
                        mtime = datetime.fromtimestamp(path.stat().st_mtime)
                        line_parts.append(f"({mtime.strftime('%Y-%m-%d %H:%M')})")
                    except OSError:
                        pass

                output.append(' '.join(line_parts))

        return '\n'.join(output)

    def _format_size(self, size: int) -> str:
        """Format file size in human-readable format."""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.1f}{unit}"
            size /= 1024
        return f"{size:.1f}TB"


def main():
    parser = argparse.ArgumentParser(
        description="File Searcher - Fast search by name, content, size, or date"
    )
    parser.add_argument("path", nargs="?", default=".", help="Root path to search")
    parser.add_argument("-n", "--name", help="Search by filename pattern")
    parser.add_argument("-c", "--content", help="Search by file content")
    parser.add_argument("-s", "--size", help="Search by size (e.g., 10mb, 100kb)")
    parser.add_argument("-d", "--days", type=int, help="Modified within N days")
    parser.add_argument("--start-date", help="Modified after date (YYYY-MM-DD)")
    parser.add_argument("--end-date", help="Modified before date (YYYY-MM-DD)")
    parser.add_argument("-t", "--date-type", choices=['modified', 'accessed', 'created'],
                        default='modified', help="Date type to search")
    parser.add_argument("-e", "--extensions", nargs="+", help="File extensions to include")
    parser.add_argument("-R", "--regex", action="store_true", help="Use regex pattern")
    parser.add_argument("-i", "--case-insensitive", action="store_true", help="Case insensitive")
    parser.add_argument("--no-path", action="store_true", help="Show filenames only")
    parser.add_argument("--show-size", action="store_true", help="Show file sizes")
    parser.add_argument("--show-date", action="store_true", help="Show modification dates")
    parser.add_argument("-m", "--max-size", help="Maximum file size for content search (MB)")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")

    args = parser.parse_args()

    searcher = FileSearcher(args.path)

    # Determine search type
    search_performed = False

    if args.name:
        search_performed = True
        if args.verbose:
            print(f"Searching for files matching: {args.name}")
        searcher.search_by_name(
            args.name,
            regex=args.regex,
            case_sensitive=not args.case_insensitive
        )

    if args.content:
        search_performed = True
        if args.verbose:
            print(f"Searching for content: {args.content}")
        max_size = float(args.max_size) if args.max_size else 10
        searcher.search_by_content(
            args.content,
            extensions=args.extensions,
            regex=args.regex,
            case_sensitive=not args.case_insensitive,
            max_size_mb=max_size
        )

    if args.size:
        search_performed = True
        if args.verbose:
            print(f"Searching for size: {args.size}")
        # Parse size (e.g., "10mb", "100kb")
        size_str = args.size.lower()
        units = {'b': 1, 'kb': 1024, 'mb': 1024**2, 'gb': 1024**3}
        for unit, mult in units.items():
            if size_str.endswith(unit):
                size_val = float(size_str[:-len(unit)])
                searcher.search_by_size(min_size=0, max_size=int(size_val),
                                       size_unit=unit)
                break
        else:
            # Bytes by default
            searcher.search_by_size(min_size=0, max_size=int(size_str))

    if args.days or args.start_date or args.end_date:
        search_performed = True
        if args.verbose:
            print(f"Searching by date: {args.date_type}")
        searcher.search_by_date(
            days=args.days,
            start_date=args.start_date,
            end_date=args.end_date,
            date_type=args.date_type
        )

    if not search_performed:
        parser.print_help()
        return 1

    # Display results
    result_count = len(searcher.results)
    print(f"\nFound {result_count} result(s):\n")
    print(searcher.format_results(
        show_path=not args.no_path,
        show_size=args.show_size,
        show_date=args.show_date
    ))

    return 0


if __name__ == "__main__":
    exit(main())
