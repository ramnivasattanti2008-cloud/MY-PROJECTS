#!/usr/bin/env python3
"""
Quick Notes - A simple CLI note-taking application
Features: Add, list, delete, search, and tag notes
Stores notes in a JSON file with colorama styling
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Try to import colorama, install if not available
try:
    from colorama import init, Fore, Style
    init(autoreset=True)
    COLORAMA_AVAILABLE = True
except ImportError:
    COLORAMA_AVAILABLE = False
    # Fallback colors as empty strings
    class Fore:
        RED = GREEN = YELLOW = CYAN = MAGENTA = WHITE = RESET = ''
    class Style:
        BRIGHT = RESET_ALL = DIM = ''

# Configuration
NOTES_FILE = Path.home() / ".quick-notes.json"


def load_notes() -> dict:
    """Load notes from JSON file or return empty structure."""
    if NOTES_FILE.exists():
        try:
            with open(NOTES_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"{Fore.RED}Error: Corrupted notes file. Starting fresh.{Style.RESET_ALL}")
            return {"notes": []}
    return {"notes": []}


def save_notes(data: dict) -> None:
    """Save notes to JSON file."""
    with open(NOTES_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def generate_id() -> str:
    """Generate a unique ID based on timestamp."""
    return datetime.now().strftime("%Y%m%d%H%M%S%f")


def add_note(title: str, content: str, tags: list) -> None:
    """Add a new note."""
    notes_data = load_notes()

    note = {
        "id": generate_id(),
        "title": title,
        "content": content,
        "tags": [t.strip().lower() for t in tags if t.strip()],
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }

    notes_data["notes"].insert(0, note)  # Add to beginning
    save_notes(notes_data)

    print(f"{Fore.GREEN}Note added successfully!{Style.RESET_ALL}")
    print(f"{Fore.CYAN}ID: {note['id']}{Style.RESET_ALL}")
    if note['tags']:
        print(f"{Fore.YELLOW}Tags: {', '.join(note['tags'])}{Style.RESET_ALL}")


def list_notes(tag_filter: str = None, search_query: str = None) -> None:
    """List all notes, optionally filtered by tag or search query."""
    notes_data = load_notes()
    notes = notes_data.get("notes", [])

    if not notes:
        print(f"{Fore.YELLOW}No notes found. Add one with: quick-notes add{Style.RESET_ALL}")
        return

    # Apply filters
    if tag_filter:
        tag_filter = tag_filter.lower()
        notes = [n for n in notes if tag_filter in n.get("tags", [])]
        if not notes:
            print(f"{Fore.YELLOW}No notes found with tag: {tag_filter}{Style.RESET_ALL}")
            return

    if search_query:
        query = search_query.lower()
        notes = [n for n in notes if
                 query in n.get("title", "").lower() or
                 query in n.get("content", "").lower()]
        if not notes:
            print(f"{Fore.YELLOW}No notes found matching: {search_query}{Style.RESET_ALL}")
            return

    # Display notes
    print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.WHITE}{Style.BRIGHT}Found {len(notes)} note(s){Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")

    for i, note in enumerate(notes, 1):
        created = datetime.fromisoformat(note['created_at']).strftime("%Y-%m-%d %H:%M")
        print(f"{Fore.GREEN}{i}. {note['title']}{Style.RESET_ALL}")
        print(f"   {Fore.DIM}ID: {note['id']} | Created: {created}{Style.RESET_ALL}")

        # Show content preview (first 100 chars)
        content = note['content'][:100]
        if len(note['content']) > 100:
            content += "..."
        print(f"   {note['content'][:80]}...")

        if note.get('tags'):
            tags_str = " ".join([f"[{t}]" for t in note['tags']])
            print(f"   {Fore.YELLOW}Tags: {tags_str}{Style.RESET_ALL}")
        print()


def view_note(note_id: str) -> None:
    """View a specific note by ID."""
    notes_data = load_notes()
    notes = notes_data.get("notes", [])

    for note in notes:
        if note['id'] == note_id:
            print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
            print(f"{Fore.GREEN}{Style.BRIGHT}{note['title']}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
            print(f"{Fore.DIM}ID: {note['id']}{Style.RESET_ALL}")
            print(f"{Fore.DIM}Created: {datetime.fromisoformat(note['created_at']).strftime('%Y-%m-%d %H:%M:%S')}{Style.RESET_ALL}")
            print(f"{Fore.DIM}Updated: {datetime.fromisoformat(note['updated_at']).strftime('%Y-%m-%d %H:%M:%S')}{Style.RESET_ALL}")

            if note.get('tags'):
                print(f"{Fore.YELLOW}Tags: {', '.join(note['tags'])}{Style.RESET_ALL}")

            print(f"\n{note['content']}\n")
            return

    print(f"{Fore.RED}Note not found: {note_id}{Style.RESET_ALL}")


def delete_note(note_id: str) -> None:
    """Delete a note by ID."""
    notes_data = load_notes()
    notes = notes_data.get("notes", [])

    original_count = len(notes)
    notes_data["notes"] = [n for n in notes if n['id'] != note_id]

    if len(notes_data["notes"]) < original_count:
        save_notes(notes_data)
        print(f"{Fore.GREEN}Note deleted successfully!{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}Note not found: {note_id}{Style.RESET_ALL}")


def update_note(note_id: str, title: str = None, content: str = None, tags: list = None) -> None:
    """Update an existing note."""
    notes_data = load_notes()

    for note in notes_data["notes"]:
        if note['id'] == note_id:
            if title is not None:
                note['title'] = title
            if content is not None:
                note['content'] = content
            if tags is not None:
                note['tags'] = [t.strip().lower() for t in tags if t.strip()]

            note['updated_at'] = datetime.now().isoformat()
            save_notes(notes_data)
            print(f"{Fore.GREEN}Note updated successfully!{Style.RESET_ALL}")
            return

    print(f"{Fore.RED}Note not found: {note_id}{Style.RESET_ALL}")


def list_tags() -> None:
    """List all unique tags."""
    notes_data = load_notes()
    all_tags = set()

    for note in notes_data.get("notes", []):
        all_tags.update(note.get("tags", []))

    if not all_tags:
        print(f"{Fore.YELLOW}No tags found. Add tags to your notes!{Style.RESET_ALL}")
        return

    print(f"\n{Fore.CYAN}{'='*40}{Style.RESET_ALL}")
    print(f"{Fore.WHITE}{Style.BRIGHT}All Tags:{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*40}{Style.RESET_ALL}\n")

    # Group tags alphabetically
    for tag in sorted(all_tags):
        print(f"  {Fore.YELLOW}[{tag}]{Style.RESET_ALL}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Quick Notes - A simple CLI note-taking app",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  quick-notes add "My Note" "Note content here" --tags work important
  quick-notes list
  quick-notes list --tag work
  quick-notes list --search "keyword"
  quick-notes view 20231015123456
  quick-notes delete 20231015123456
  quick-notes tags
        """
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Add command
    add_parser = subparsers.add_parser("add", help="Add a new note")
    add_parser.add_argument("title", help="Note title")
    add_parser.add_argument("content", help="Note content")
    add_parser.add_argument("--tags", "-t", nargs="*", default=[], help="Tags for the note")

    # List command
    list_parser = subparsers.add_parser("list", help="List all notes")
    list_parser.add_argument("--tag", help="Filter by tag")
    list_parser.add_argument("--search", "-s", help="Search in title and content")

    # View command
    view_parser = subparsers.add_parser("view", help="View a specific note")
    view_parser.add_argument("id", help="Note ID")

    # Delete command
    delete_parser = subparsers.add_parser("delete", help="Delete a note")
    delete_parser.add_argument("id", help="Note ID")

    # Update command
    update_parser = subparsers.add_parser("update", help="Update a note")
    update_parser.add_argument("id", help="Note ID")
    update_parser.add_argument("--title", help="New title")
    update_parser.add_argument("--content", help="New content")
    update_parser.add_argument("--tags", "-t", nargs="*", help="New tags")

    # Tags command
    tags_parser = subparsers.add_parser("tags", help="List all tags")

    args = parser.parse_args()

    # Handle commands
    if args.command == "add":
        add_note(args.title, args.content, args.tags)
    elif args.command == "list":
        list_notes(tag_filter=args.tag, search_query=args.search)
    elif args.command == "view":
        view_note(args.id)
    elif args.command == "delete":
        delete_note(args.id)
    elif args.command == "update":
        update_note(args.id, args.title, args.content, args.tags)
    elif args.command == "tags":
        list_tags()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
