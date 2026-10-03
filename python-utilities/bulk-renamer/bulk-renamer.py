#!/usr/bin/env python3
"""
Bulk File Renamer - Pattern-based file renaming with preview and undo support.
Usage: python bulk-renamer.py <directory> [options]
"""

import os
import re
import json
import argparse
from pathlib import Path
from datetime import datetime


class UndoManager:
    """Manages undo history for rename operations."""

    def __init__(self, history_file=".rename_history.json"):
        self.history_file = Path(history_file)
        self.history = self._load_history()

    def _load_history(self):
        if self.history_file.exists():
            try:
                with open(self.history_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return []
        return []

    def _save_history(self):
        with open(self.history_file, 'w') as f:
            json.dump(self.history, f, indent=2)

    def add_operation(self, old_path, new_path):
        self.history.append({
            "old": str(old_path),
            "new": str(new_path),
            "timestamp": datetime.now().isoformat()
        })
        self._save_history()

    def undo_last(self):
        if not self.history:
            print("No operations to undo.")
            return False

        last = self.history.pop()
        new_path = Path(last["new"])
        old_path = Path(last["old"])

        if new_path.exists():
            new_path.rename(old_path)
            print(f"Undone: {new_path.name} -> {old_path.name}")
            self._save_history()
            return True
        else:
            print(f"Cannot undo: {new_path} does not exist")
            return False

    def get_history(self):
        return self.history


class BulkRenamer:
    """Handles bulk file renaming operations."""

    def __init__(self, directory, undo_manager=None):
        self.directory = Path(directory)
        self.undo_manager = undo_manager or UndoManager()
        self.operations = []

    def set_pattern(self, search, replace, use_regex=False, case_sensitive=True):
        self.search_pattern = search
        self.replace_pattern = replace
        self.use_regex = use_regex
        self.case_sensitive = case_sensitive

    def filter_files(self, extensions=None, exclude_patterns=None):
        """Filter files by extensions and exclusion patterns."""
        files = []
        for f in self.directory.iterdir():
            if not f.is_file():
                continue

            if extensions:
                if f.suffix.lower() not in [ext.lower() for ext in extensions]:
                    continue

            if exclude_patterns:
                skip = False
                for pattern in exclude_patterns:
                    if pattern in f.name:
                        skip = True
                        break
                if skip:
                    continue

            files.append(f)
        return sorted(files)

    def preview(self, files=None):
        """Preview rename operations without applying them."""
        if files is None:
            files = self.filter_files()

        self.operations = []
        results = []

        for f in files:
            new_name = self._compute_new_name(f.name)
            if new_name and new_name != f.name:
                self.operations.append((f, self.directory / new_name))
                results.append((f.name, new_name))

        return results

    def _compute_new_name(self, filename):
        if self.use_regex:
            if self.case_sensitive:
                new_name = re.sub(self.search_pattern, self.replace_pattern, filename)
            else:
                new_name = re.sub(self.search_pattern, self.replace_pattern, filename, flags=re.IGNORECASE)
        else:
            if self.case_sensitive:
                new_name = filename.replace(self.search_pattern, self.replace_pattern)
            else:
                pattern = re.compile(re.escape(self.search_pattern), re.IGNORECASE)
                new_name = pattern.sub(self.replace_pattern, filename)

        return new_name

    def apply(self, dry_run=False):
        """Apply the rename operations."""
        if not self.operations:
            print("No operations to apply.")
            return 0

        if dry_run:
            print("\n[DRY RUN] Would rename:")
            for old, new in self.operations:
                print(f"  {old.name} -> {new.name}")
            return len(self.operations)

        count = 0
        for old_path, new_path in self.operations:
            if old_path.exists() and not new_path.exists():
                old_path.rename(new_path)
                self.undo_manager.add_operation(old_path, new_path)
                print(f"Renamed: {old_path.name} -> {new_path.name}")
                count += 1
            elif new_path.exists():
                print(f"Skipped (exists): {old_path.name} -> {new_path.name}")

        return count


def main():
    parser = argparse.ArgumentParser(
        description="Bulk File Renamer - Rename multiple files with pattern matching"
    )
    parser.add_argument("directory", help="Directory containing files to rename")
    parser.add_argument("-s", "--search", required=True, help="Search pattern")
    parser.add_argument("-r", "--replace", required=True, help="Replacement text")
    parser.add_argument("-e", "--extensions", nargs="+", help="Filter by extensions (e.g., .txt .md)")
    parser.add_argument("-x", "--exclude", nargs="+", help="Exclude files containing these patterns")
    parser.add_argument("-R", "--regex", action="store_true", help="Use regex patterns")
    parser.add_argument("-i", "--case-insensitive", action="store_true", help="Case insensitive matching")
    parser.add_argument("-p", "--preview", action="store_true", help="Preview changes only")
    parser.add_argument("-y", "--yes", action="store_true", help="Skip confirmation prompt")
    parser.add_argument("--undo", action="store_true", help="Undo last rename operation")
    parser.add_argument("--history", action="store_true", help="Show rename history")

    args = parser.parse_args()

    if not Path(args.directory).is_dir():
        print(f"Error: {args.directory} is not a valid directory")
        return 1

    undo_mgr = UndoManager()

    if args.undo:
        undo_mgr.undo_last()
        return 0

    if args.history:
        history = undo_mgr.get_history()
        if not history:
            print("No rename history.")
        else:
            print(f"\nRename History ({len(history)} operations):")
            for op in history[-10:]:  # Show last 10
                print(f"  {op['old']} -> {op['new']}")
        return 0

    renamer = BulkRenamer(args.directory, undo_mgr)
    renamer.set_pattern(
        args.search,
        args.replace,
        use_regex=args.regex,
        case_sensitive=not args.case_insensitive
    )

    files = renamer.filter_files(args.extensions, args.exclude)
    preview_results = renamer.preview(files)

    if not preview_results:
        print("No files match the pattern.")
        return 0

    print("\nPreview of changes:")
    print("-" * 60)
    for old_name, new_name in preview_results:
        print(f"  {old_name}")
        print(f"    -> {new_name}")
    print("-" * 60)
    print(f"Total: {len(preview_results)} file(s) will be renamed")

    if args.preview:
        return 0

    if not args.yes:
        confirm = input("\nApply these changes? [y/N]: ").strip().lower()
        if confirm != 'y':
            print("Cancelled.")
            return 0

    count = renamer.apply()
    print(f"\nRenamed {count} file(s) successfully.")

    return 0


if __name__ == "__main__":
    exit(main())
