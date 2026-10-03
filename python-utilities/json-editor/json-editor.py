#!/usr/bin/env python3
"""
JSON Editor - Interactive CLI tool for editing JSON files.

This script provides an interactive command-line interface for viewing,
adding, editing, and deleting keys in JSON files.

Educational Purpose:
- Demonstrates JSON manipulation in Python
- Shows recursive dictionary traversal
- Teaches interactive CLI design
- Explains JSON schema operations

Author: Educational Example
License: MIT
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Union, List, Dict


class JSONEditor:
    """
    Interactive JSON file editor with CLI interface.

    Supports viewing, adding, editing, deleting, and searching
    within JSON files of any structure.
    """

    def __init__(self, file_path: str):
        """
        Initialize the editor with a JSON file.

        Args:
            file_path: Path to the JSON file
        """
        self.file_path = Path(file_path)
        self.data = None
        self.modified = False
        self._load()

    def _load(self):
        """Load JSON file into memory."""
        if not self.file_path.exists():
            raise FileNotFoundError(f"File not found: {self.file_path}")

        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON file: {e}")
        except Exception as e:
            raise IOError(f"Error reading file: {e}")

    def save(self, output_path: str = None):
        """
        Save the JSON data to a file.

        Args:
            output_path: Optional path for saving (defaults to original file)
        """
        if output_path:
            save_path = Path(output_path)
        else:
            save_path = self.file_path

        try:
            with open(save_path, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
            self.modified = False
            print(f"Saved: {save_path}")
        except Exception as e:
            raise IOError(f"Error saving file: {e}")

    def view(self, path: str = None, max_depth: int = 10) -> str:
        """
        View JSON data at a specific path.

        Args:
            path: Dot-notation path (e.g., 'user.profile.name')
            max_depth: Maximum nesting depth to display

        Returns:
            Formatted JSON string
        """
        data = self._navigate_to(path) if path else self.data
        return json.dumps(data, indent=2, ensure_ascii=False)

    def get(self, path: str) -> Any:
        """
        Get value at a specific path.

        Args:
            path: Dot-notation path

        Returns:
            Value at the path
        """
        return self._navigate_to(path)

    def set(self, path: str, value: Any):
        """
        Set value at a specific path.

        Args:
            path: Dot-notation path
            value: New value (can be any valid JSON type)
        """
        if '.' in path:
            # Navigate to parent and set child
            parts = path.rsplit('.', 1)
            parent = self._navigate_to(parts[0])
            if parent is None:
                # Create intermediate objects
                parent = self._create_path(parts[0])
            key = parts[1]
            parent[key] = value
        else:
            self.data[path] = value

        self.modified = True

    def delete(self, path: str):
        """
        Delete a key at a specific path.

        Args:
            path: Dot-notation path to the key to delete
        """
        if '.' in path:
            parts = path.rsplit('.', 1)
            parent = self._navigate_to(parts[0])
            if parent and parts[1] in parent:
                del parent[parts[1]]
                self.modified = True
            else:
                raise KeyError(f"Key not found: {path}")
        else:
            if path in self.data:
                del self.data[path]
                self.modified = True
            else:
                raise KeyError(f"Key not found: {path}")

    def add(self, path: str, key: str, value: Any):
        """
        Add a new key-value pair at a specific path.

        Args:
            path: Dot-notation path to the parent object
            key: Name of the new key
            value: Value to set
        """
        parent = self._navigate_to(path)
        if parent is None:
            # Create the path
            parent = self._create_path(path)

        if isinstance(parent, dict):
            if key in parent:
                raise ValueError(f"Key already exists: {path}.{key}")
            parent[key] = value
        elif isinstance(parent, list):
            index = self._parse_index(key)
            if index < 0 or index > len(parent):
                raise IndexError(f"List index out of range: {index}")
            parent.insert(index, value)
        else:
            raise TypeError(f"Cannot add to {type(parent).__name__}")

        self.modified = True

    def search(self, query: str, path: str = None) -> List[str]:
        """
        Search for keys or values containing a query string.

        Args:
            query: Search string
            path: Optional path to search within

        Returns:
            List of matching paths
        """
        root = self._navigate_to(path) if path else self.data
        matches = []
        base_path = path or ''

        self._search_recursive(root, base_path, query.lower(), matches)
        return matches

    def _search_recursive(self, obj: Any, current_path: str, query: str, matches: List[str]):
        """Recursively search through JSON structure."""
        if isinstance(obj, dict):
            for key, value in obj.items():
                full_path = f"{current_path}.{key}" if current_path else key

                # Check if key contains query
                if query in key.lower():
                    matches.append(full_path)

                # Search in value
                self._search_recursive(value, full_path, query, matches)

        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                full_path = f"{current_path}[{i}]"
                self._search_recursive(item, full_path, query, matches)

        elif isinstance(obj, str) and query in obj.lower():
            # Also match values
            if current_path not in matches:
                matches.append(current_path)

    def _navigate_to(self, path: str) -> Any:
        """
        Navigate to a specific path in the JSON structure.

        Args:
            path: Dot-notation path

        Returns:
            Value at the path, or None if path doesn't exist
        """
        if not path:
            return self.data

        current = self.data
        parts = self._parse_path_parts(path)

        for part in parts:
            if isinstance(current, dict):
                current = current.get(part)
            elif isinstance(current, list):
                index = self._parse_index(part)
                if index < len(current):
                    current = current[index]
                else:
                    return None
            else:
                return None

            if current is None:
                return None

        return current

    def _parse_path_parts(self, path: str) -> List[Union[str, int]]:
        """Parse path into parts, handling array indices."""
        parts = []
        current = ''

        i = 0
        while i < len(path):
            char = path[i]

            if char == '.':
                if current:
                    parts.append(current)
                    current = ''
            elif char == '[':
                if current:
                    parts.append(current)
                    current = ''
                # Find closing bracket
                j = i + 1
                while j < len(path) and path[j] != ']':
                    j += 1
                parts.append(path[i+1:j])
                i = j
            else:
                current += char

            i += 1

        if current:
            parts.append(current)

        return parts

    def _parse_index(self, value: str) -> int:
        """Parse array index from string."""
        if isinstance(value, int):
            return value
        return int(value)

    def _create_path(self, path: str) -> Dict:
        """Create intermediate objects for a path."""
        parts = self._parse_path_parts(path)
        current = self.data

        for i, part in enumerate(parts):
            if isinstance(current, dict):
                if part not in current:
                    # Create new object or list for remaining path
                    remaining = parts[i:]
                    if any(isinstance(self._parse_index(p), int) for p in remaining):
                        current[part] = []
                    else:
                        current[part] = {}
                current = current[part]
            elif isinstance(current, list):
                index = self._parse_index(part)
                while len(current) <= index:
                    current.append({})
                current = current[index]

        return current

    def get_structure(self, max_depth: int = 5) -> str:
        """
        Get a tree view of the JSON structure.

        Args:
            max_depth: Maximum depth to traverse

        Returns:
            Tree representation of structure
        """
        lines = []
        self._structure_recursive(self.data, '', lines, max_depth, 0)
        return '\n'.join(lines)

    def _structure_recursive(self, obj: Any, prefix: str, lines: List[str],
                            max_depth: int, current_depth: int):
        """Recursively build structure tree."""
        if current_depth >= max_depth:
            lines.append(f"{prefix}...")
            return

        indent = '  ' * current_depth

        if isinstance(obj, dict):
            keys = list(obj.keys())
            for i, key in enumerate(keys):
                is_last = (i == len(keys) - 1)
                new_prefix = prefix + ('└── ' if is_last else '├── ')

                if isinstance(obj[key], (dict, list)):
                    lines.append(f"{indent}{new_prefix}{key} ({type(obj[key]).__name__})")
                    self._structure_recursive(obj[key], new_prefix, lines,
                                             max_depth, current_depth + 1)
                else:
                    value_preview = self._value_preview(obj[key])
                    lines.append(f"{indent}{new_prefix}{key}: {value_preview}")

        elif isinstance(obj, list):
            lines.append(f"{indent}{prefix}[list of {len(obj)} items]")
            if len(obj) > 0:
                self._structure_recursive(obj[0], prefix, lines, max_depth, current_depth + 1)

    def _value_preview(self, value: Any) -> str:
        """Get a preview string for a value."""
        if value is None:
            return 'null'
        elif isinstance(value, bool):
            return str(value).lower()
        elif isinstance(value, (int, float)):
            return str(value)
        elif isinstance(value, str):
            if len(value) > 30:
                return f'"{value[:27]}..."'
            return f'"{value}"'
        elif isinstance(value, list):
            return f'[{type(value[0]).__name__ if value else "empty"}]'
        elif isinstance(value, dict):
            return f'{{{len(value)} keys}}'
        else:
            return str(type(value).__name__)


def interactive_editor(file_path: str):
    """
    Run the interactive JSON editor.

    Args:
        file_path: Path to the JSON file to edit
    """
    editor = JSONEditor(file_path)
    original_data = json.dumps(editor.data, sort_keys=True)

    print(f"\nJSON Editor - {file_path}")
    print("=" * 50)
    print("Commands: view, set, add, delete, search, structure, save, quit")
    print()

    while True:
        try:
            command = input("json> ").strip()

            if not command:
                continue

            parts = command.split(maxsplit=2)
            cmd = parts[0].lower()

            if cmd == 'quit' or cmd == 'exit' or cmd == 'q':
                if editor.modified:
                    confirm = input("Unsaved changes. Save before quitting? (y/n): ").lower()
                    if confirm == 'y':
                        editor.save()
                print("Goodbye!")
                break

            elif cmd == 'help' or cmd == '?':
                print("""
Commands:
  view [path]              View JSON data (optionally at path)
  set <path> <value>       Set a value at path
  add <path> <key> <value> Add new key-value pair
  delete <path>            Delete key at path
  search <query>           Search for key/value containing query
  structure                Show structure tree
  save [path]              Save to file
  quit                     Exit editor
                """.strip())

            elif cmd == 'view' or cmd == 'v':
                path = parts[1] if len(parts) > 1 else None
                try:
                    result = editor.view(path)
                    print(result)
                except Exception as e:
                    print(f"Error: {e}")

            elif cmd == 'set' or cmd == 's':
                if len(parts) < 3:
                    print("Usage: set <path> <value>")
                    continue
                path = parts[1]
                value_str = parts[2]

                # Try to parse value as JSON
                try:
                    value = json.loads(value_str)
                except json.JSONDecodeError:
                    # Treat as string
                    value = value_str

                try:
                    editor.set(path, value)
                    print(f"Set {path} = {json.dumps(value)}")
                except Exception as e:
                    print(f"Error: {e}")

            elif cmd == 'add' or cmd == 'a':
                if len(parts) < 4:
                    print("Usage: add <parent-path> <key> <value>")
                    continue
                parent_path = parts[1]
                key = parts[2]
                value_str = parts[3]

                try:
                    value = json.loads(value_str)
                except json.JSONDecodeError:
                    value = value_str

                try:
                    editor.add(parent_path, key, value)
                    print(f"Added {parent_path}.{key} = {json.dumps(value)}")
                except Exception as e:
                    print(f"Error: {e}")

            elif cmd == 'delete' or cmd == 'd':
                if len(parts) < 2:
                    print("Usage: delete <path>")
                    continue
                path = parts[1]

                try:
                    editor.delete(path)
                    print(f"Deleted: {path}")
                except KeyError as e:
                    print(f"Error: {e}")

            elif cmd == 'search' or cmd == '/':
                if len(parts) < 2:
                    print("Usage: search <query>")
                    continue
                query = parts[1]

                results = editor.search(query)
                if results:
                    print(f"Found {len(results)} matches:")
                    for path in results:
                        print(f"  - {path}")
                else:
                    print("No matches found.")

            elif cmd == 'structure' or cmd == 'tree':
                print(editor.get_structure())

            elif cmd == 'save' or cmd == 'w':
                output_path = parts[1] if len(parts) > 1 else None
                try:
                    editor.save(output_path)
                except Exception as e:
                    print(f"Error: {e}")

            elif cmd == 'reload' or cmd == 'r':
                editor._load()
                print("Reloaded from file.")

            else:
                print(f"Unknown command: {cmd}")
                print("Type 'help' for available commands.")

        except KeyboardInterrupt:
            print("\nUse 'quit' to exit.")
        except EOFError:
            print("\nGoodbye!")
            break


def main():
    """Main entry point with CLI argument parsing."""
    parser = argparse.ArgumentParser(
        description='Interactive CLI for editing JSON files.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Start interactive editor:
    python json-editor.py config.json

  View file contents (non-interactive):
    python json-editor.py config.json --view

  View specific path:
    python json-editor.py config.json --view "user.settings"

  Search for a key:
    python json-editor.py config.json --search "color"

Path notation:
  - Nested keys: user.profile.name
  - Array indices: items[0].title
  - Nested arrays: data[0].tags[1]
        """
    )

    parser.add_argument('file', help='Path to the JSON file')
    parser.add_argument('--view', metavar='PATH',
                        help='View JSON at path (non-interactive)')
    parser.add_argument('--set', nargs=2, metavar=('PATH', 'VALUE'),
                        help='Set value at path (non-interactive)')
    parser.add_argument('--search', metavar='QUERY',
                        help='Search for key/value')
    parser.add_argument('--structure', action='store_true',
                        help='Show structure tree')

    args = parser.parse_args()

    try:
        editor = JSONEditor(args.file)

        if args.view is not None:
            print(editor.view(args.view))
        elif args.set:
            path, value_str = args.set
            try:
                value = json.loads(value_str)
            except json.JSONDecodeError:
                value = value_str
            editor.set(path, value)
            editor.save()
        elif args.search:
            results = editor.search(args.search)
            for path in results:
                print(path)
        elif args.structure:
            print(editor.get_structure())
        else:
            interactive_editor(args.file)

    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
