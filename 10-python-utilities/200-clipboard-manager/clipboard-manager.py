#!/usr/bin/env python3
"""
Clipboard Manager - Manage clipboard history with save, search, and paste functionality.
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import List, Optional


HISTORY_FILE = Path.home() / ".clipboard_history.json"
MAX_HISTORY = 1000


def load_history() -> List[dict]:
    """Load clipboard history from file."""
    if HISTORY_FILE.exists():
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []
    return []


def save_history(history: List[dict]) -> None:
    """Save clipboard history to file."""
    HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)


def add_to_history(content: str, history: List[dict]) -> List[dict]:
    """Add new entry to history, removing duplicates."""
    # Remove duplicates (keep most recent)
    history = [h for h in history if h.get("content") != content]

    entry = {
        "content": content,
        "timestamp": datetime.now().isoformat(),
        "length": len(content)
    }

    history.insert(0, entry)

    # Trim to max size
    if len(history) > MAX_HISTORY:
        history = history[:MAX_HISTORY]

    return history


def get_clipboard_content() -> Optional[str]:
    """Get current clipboard content using platform-specific method."""
    try:
        import pyperclip
        return pyperclip.paste()
    except ImportError:
        pass

    # Fallback for Windows
    if sys.platform == "win32":
        try:
            import subprocess
            result = subprocess.run(
                ["powershell", "-Command", "Get-Clipboard"],
                capture_output=True, text=True, timeout=2
            )
            return result.stdout.strip() if result.stdout else None
        except Exception:
            pass

    # Fallback for Linux/macOS
    else:
        try:
            import subprocess
            result = subprocess.run(
                ["xclip", "-selection", "clipboard", "-o"],
                capture_output=True, text=True, timeout=2
            )
            return result.stdout if result.stdout else None
        except Exception:
            pass

    return None


def set_clipboard_content(content: str) -> bool:
    """Set clipboard content using platform-specific method."""
    try:
        import pyperclip
        pyperclip.copy(content)
        return True
    except ImportError:
        pass

    # Fallback for Windows
    if sys.platform == "win32":
        try:
            import subprocess
            subprocess.run(
                ["powershell", "-Command", f"Set-Clipboard -Value '{content.replace(chr(39), chr(39)+chr(39))}'"],
                capture_output=True, timeout=2
            )
            return True
        except Exception:
            pass

    # Fallback for Linux
    else:
        try:
            import subprocess
            subprocess.run(
                ["xclip", "-selection", "clipboard"],
                input=content.encode(), timeout=2
            )
            return True
        except Exception:
            pass

    return False


def search_history(query: str, history: List[dict], case_sensitive: bool = False) -> List[dict]:
    """Search history for entries containing query."""
    results = []
    for entry in history:
        content = entry.get("content", "")
        if case_sensitive:
            if query in content:
                results.append(entry)
        else:
            if query.lower() in content.lower():
                results.append(entry)
    return results


def format_timestamp(ts: str) -> str:
    """Format ISO timestamp to readable string."""
    try:
        dt = datetime.fromisoformat(ts)
        now = datetime.now()
        diff = now - dt

        if diff.total_seconds() < 60:
            return "just now"
        elif diff.total_seconds() < 3600:
            mins = int(diff.total_seconds() / 60)
            return f"{mins} min{'s' if mins > 1 else ''} ago"
        elif diff.days == 0:
            return dt.strftime("%H:%M")
        elif diff.days == 1:
            return "yesterday"
        elif diff.days < 7:
            return f"{diff.days} days ago"
        else:
            return dt.strftime("%Y-%m-%d")
    except Exception:
        return ts


def truncate_content(content: str, max_len: int = 100) -> str:
    """Truncate content for display."""
    content = content.replace("\n", " ").replace("\r", "")
    if len(content) > max_len:
        return content[:max_len-3] + "..."
    return content


def display_history(history: List[dict], limit: int = 20, search: Optional[str] = None) -> None:
    """Display clipboard history."""
    if search:
        display_list = search_history(search, history)
        print(f"\nSearch results for '{search}': {len(display_list)} matches\n")
    else:
        display_list = history[:limit]
        print(f"\nClipboard History ({min(limit, len(history))} of {len(history)} entries)\n")

    print("-" * 80)

    for i, entry in enumerate(display_list):
        content = entry.get("content", "")
        timestamp = entry.get("timestamp", "")
        length = entry.get("length", len(content))

        preview = truncate_content(content, 80)
        time_str = format_timestamp(timestamp)

        print(f"[{i+1:3d}] {time_str:>12}  {length:>6} chars  {preview}")
        print(f"       {content[:100].replace(chr(10), ' ')}")

    print("-" * 80)


def clear_history(confirm: bool = True) -> None:
    """Clear all clipboard history."""
    if confirm:
        response = input("Clear all clipboard history? [y/N]: ").strip().lower()
        if response != "y":
            print("Cancelled.")
            return

    save_history([])
    print("Clipboard history cleared.")


def paste_from_history(index: int, history: List[dict]) -> bool:
    """Copy item from history to clipboard."""
    if index < 0 or index >= len(history):
        print(f"Error: Invalid index {index}. Valid range: 0-{len(history)-1}")
        return False

    content = history[index]["content"]
    if set_clipboard_content(content):
        print(f"Pasted entry [{index}]: {truncate_content(content, 50)}")
        return True
    else:
        print("Error: Failed to copy to clipboard. Is pyperclip installed?")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Manage clipboard history. Save copies, search, and paste from history.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Save current clipboard to history:
    python clipboard-manager.py save

  List recent history:
    python clipboard-manager.py list
    python clipboard-manager.py list -n 50

  Search history:
    python clipboard-manager.py search "error"
    python clipboard-manager.py search "TODO" -i

  Paste from history:
    python clipboard-manager.py paste 5

  Clear history:
    python clipboard-manager.py clear

  Watch clipboard (continuous):
    python clipboard-manager.py watch
        """
    )

    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Save command
    save_parser = subparsers.add_parser("save", help="Save current clipboard to history")
    save_parser.add_argument("--text", "-t", help="Text to save directly")

    # List command
    list_parser = subparsers.add_parser("list", help="List clipboard history")
    list_parser.add_argument("-n", "--number", type=int, default=20,
                             help="Number of entries to show (default: 20)")

    # Search command
    search_parser = subparsers.add_parser("search", help="Search clipboard history")
    search_parser.add_argument("query", help="Search query")
    search_parser.add_argument("-i", "--ignore-case", action="store_true",
                               help="Case insensitive search")

    # Paste command
    paste_parser = subparsers.add_parser("paste", help="Paste from history")
    paste_parser.add_argument("index", type=int, help="History index to paste")

    # Clear command
    clear_parser = subparsers.add_parser("clear", help="Clear clipboard history")
    clear_parser.add_argument("-f", "--force", action="store_true",
                              help="Skip confirmation")

    # Watch command
    watch_parser = subparsers.add_parser("watch", help="Watch clipboard continuously")
    watch_parser.add_argument("-i", "--interval", type=float, default=1.0,
                              help="Check interval in seconds (default: 1.0)")

    args = parser.parse_args()

    if not args.command:
        # Default: show history
        history = load_history()
        display_history(history)
        return

    if args.command == "save":
        history = load_history()
        if args.text:
            content = args.text
        else:
            content = get_clipboard_content()

        if content:
            history = add_to_history(content, history)
            save_history(history)
            print(f"Saved: {truncate_content(content, 50)}")
        else:
            print("Error: Clipboard is empty or unavailable.")

    elif args.command == "list":
        history = load_history()
        display_history(history, limit=args.number)

    elif args.command == "search":
        history = load_history()
        results = search_history(args.query, history, case_sensitive=not args.ignore_case)
        display_history(history, search=args.query)

    elif args.command == "paste":
        history = load_history()
        if not paste_from_history(args.index, history):
            sys.exit(1)

    elif args.command == "clear":
        clear_history(confirm=not args.force)

    elif args.command == "watch":
        print(f"Watching clipboard (Ctrl+C to stop)...")
        history = load_history()
        last_content = get_clipboard_content()

        try:
            while True:
                time.sleep(args.interval)
                current = get_clipboard_content()

                if current and current != last_content:
                    history = add_to_history(current, history)
                    save_history(history)
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] Saved: {truncate_content(current, 60)}")
                    last_content = current

        except KeyboardInterrupt:
            print("\nStopped watching.")


if __name__ == "__main__":
    main()
