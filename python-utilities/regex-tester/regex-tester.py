#!/usr/bin/env python3
"""
Regex Tester - Interactive regex pattern testing with highlighted matches.
"""

import argparse
import re
import sys
from dataclasses import dataclass
from typing import List, Optional, Tuple


@dataclass
class MatchInfo:
    """Information about a regex match."""
    start: int
    end: int
    text: str
    groups: List[Optional[str]]
    group_names: dict


def compile_pattern(pattern: str, flags: int = 0) -> Optional[re.Pattern]:
    """Compile regex pattern, return None with error message on failure."""
    try:
        return re.compile(pattern, flags)
    except re.error as e:
        print(f"Regex error: {e}")
        return None


def find_matches(pattern: re.Pattern, text: str) -> List[MatchInfo]:
    """Find all matches and return detailed info."""
    matches = []
    for match in pattern.finditer(text):
        groups = list(match.groups())
        group_names = {}

        # Get named groups
        if match.groupdict():
            for name, value in match.groupdict().items():
                if value is not None:
                    group_names[name] = value

        matches.append(MatchInfo(
            start=match.start(),
            end=match.end(),
            text=match.group(),
            groups=groups,
            group_names=group_names
        ))
    return matches


def highlight_matches(text: str, matches: List[MatchInfo],
                      highlight_start: str = "\033[92m",   # Green
                      highlight_end: str = "\033[0m",
                      group_colors: List[str] = None) -> str:
    """Create highlighted version of text with matches marked."""
    if not matches:
        return text

    # Build highlighted text
    result = []
    last_end = 0

    for match in matches:
        # Add text before match
        result.append(text[last_end:match.start])
        # Add highlighted match
        result.append(highlight_start)
        result.append(text[match.start:match.end])
        result.append(highlight_end)
        last_end = match.end

    # Add remaining text
    result.append(text[last_end:])
    return "".join(result)


def print_matches(text: str, matches: List[MatchInfo], show_details: bool = True) -> None:
    """Print matches with optional details."""
    if not matches:
        print("\nNo matches found.")
        return

    print(f"\n{'=' * 70}")
    print(f"Found {len(matches)} match{'es' if len(matches) > 1 else ''}")
    print('=' * 70)

    for i, match in enumerate(matches, 1):
        print(f"\n[Match {i}] Position: {match.start}-{match.end}")
        print(f"  Full match: {repr(match.text)}")

        # Show captured groups
        if match.groups:
            print(f"  Groups:")
            for j, group in enumerate(match.groups(), 1):
                if group is not None:
                    print(f"    Group {j}: {repr(group)}")

        # Show named groups
        if match.group_names:
            print(f"  Named groups:")
            for name, value in match.group_names.items():
                print(f"    {name}: {repr(value)}")

    print(f"\n{'=' * 70}")


def print_highlighted_text(text: str, matches: List[MatchInfo]) -> None:
    """Print text with matches highlighted."""
    highlighted = highlight_matches(text, matches)
    print("\nHighlighted Text (showing first 500 chars):")
    print("-" * 70)
    # Limit output for readability
    print(highlighted[:500] + ("..." if len(highlighted) > 500 else ""))
    print("-" * 70)


def interactive_mode() -> None:
    """Run interactive regex testing session."""
    print("Regex Tester - Interactive Mode")
    print("=" * 50)
    print("Commands:")
    print("  :q, :quit          - Exit")
    print("  :flags <flags>     - Set flags (i, m, s, x)")
    print("  :clear             - Clear text")
    print("  :help              - Show this help")
    print("=" * 50)

    pattern = None
    compiled_pattern = None
    text = ""
    flags = 0

    while True:
        try:
            user_input = input("\n> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not user_input:
            continue

        # Handle commands
        if user_input.startswith(":"):
            cmd = user_input[1:].split()[0].lower()

            if cmd in ("q", "quit"):
                print("Goodbye!")
                break

            elif cmd == "flags":
                flag_str = user_input.split(maxsplit=1)[1] if len(user_input.split()) > 1 else ""
                new_flags = 0
                for f in flag_str:
                    if f == "i":
                        new_flags |= re.IGNORECASE
                    elif f == "m":
                        new_flags |= re.MULTILINE
                    elif f == "s":
                        new_flags |= re.DOTALL
                    elif f == "x":
                        new_flags |= re.VERBOSE
                flags = new_flags
                # Recompile if pattern exists
                if pattern:
                    compiled_pattern = compile_pattern(pattern, flags)
                    if compiled_pattern:
                        matches = find_matches(compiled_pattern, text)
                        print_matches(text, matches)
                        print_highlighted_text(text, matches)
                print(f"Flags set: {flag_str or '(none)'}")

            elif cmd == "clear":
                text = ""
                print("Text cleared.")

            elif cmd == "help":
                print("Commands:")
                print("  :q, :quit          - Exit")
                print("  :flags <flags>     - Set flags (i=ignore case, m=multiline, s=dotall, x=verbose)")
                print("  :clear             - Clear text")
                print("  :help              - Show this help")

            else:
                print(f"Unknown command: {cmd}")

            continue

        # Check if it's a pattern (ends with /) or text
        if user_input.endswith("/") and len(user_input) > 1:
            pattern = user_input[:-1]
            compiled_pattern = compile_pattern(pattern, flags)

            if compiled_pattern:
                print(f"Pattern: {pattern}")
                if flags:
                    flag_names = []
                    if flags & re.IGNORECASE:
                        flag_names.append("IGNORECASE")
                    if flags & re.MULTILINE:
                        flag_names.append("MULTILINE")
                    if flags & re.DOTALL:
                        flag_names.append("DOTALL")
                    if flags & re.VERBOSE:
                        flag_names.append("VERBOSE")
                    print(f"Flags: {', '.join(flag_names)}")

                if text:
                    matches = find_matches(compiled_pattern, text)
                    print_matches(text, matches)
                    print_highlighted_text(text, matches)
                else:
                    print("No text to match. Enter text on next line.")

        else:
            # It's text
            text = user_input
            if compiled_pattern and pattern:
                matches = find_matches(compiled_pattern, text)
                print_matches(text, matches)
                print_highlighted_text(text, matches)
            else:
                print("Text updated. Enter a pattern (with /) to match.")


def test_mode(pattern: str, text: str, flags: int = 0, show_details: bool = True) -> int:
    """Test pattern against text (non-interactive)."""
    compiled = compile_pattern(pattern, flags)
    if not compiled:
        return 1

    print(f"Pattern: {pattern}")
    if flags:
        flag_names = []
        if flags & re.IGNORECASE:
            flag_names.append("IGNORECASE")
        if flags & re.MULTILINE:
            flag_names.append("MULTILINE")
        if flags & re.DOTALL:
            flag_names.append("DOTALL")
        if flags & re.VERBOSE:
            flag_names.append("VERBOSE")
        print(f"Flags: {', '.join(flag_names)}")

    print(f"\nText: {repr(text[:200])}")
    if len(text) > 200:
        print(f"       ({len(text)} total chars)")

    matches = find_matches(compiled, text)

    if show_details:
        print_matches(text, matches)
        print_highlighted_text(text, matches)

    return 0 if matches else 1


def main():
    parser = argparse.ArgumentParser(
        description="Interactive regex pattern testing with highlighted matches.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Interactive mode:
    python regex-tester.py

  One-shot test:
    python regex-tester.py -p "pattern" -t "text to search"

  With flags:
    python regex-tester.py -p "hello" -t "HELLO world" -f i

  Verbose pattern:
    python regex-tester.py -p "\\\\d{3}-\\\\d{4}" -t "123-4567"

Examples in interactive mode:
    /\\\\d+/           - Enter pattern
    some text         - Enter text to search
    :flags i          - Set case-insensitive flag
    :help             - Show all commands
    :q                - Quit
        """
    )

    parser.add_argument("-p", "--pattern", help="Regex pattern (use / delimiters)")
    parser.add_argument("-t", "--text", help="Text to search")
    parser.add_argument("-f", "--flags", default="",
                        help="Flags: i (ignore case), m (multiline), s (dotall), x (verbose)")
    parser.add_argument("-i", "--ignore-case", action="store_true",
                        help="Case insensitive matching")
    parser.add_argument("-m", "--multiline", action="store_true",
                        help="Multiline mode (^ and $ match line boundaries)")
    parser.add_argument("-s", "--dotall", action="store_true",
                        help="Dotall mode (. matches newlines)")
    parser.add_argument("-x", "--verbose", action="store_true",
                        help="Verbose mode (ignore whitespace and comments)")
    parser.add_argument("-q", "--quiet", action="store_true",
                        help="Suppress detailed output")

    args = parser.parse_args()

    # Build flags
    flags = 0
    if args.ignore_case or "i" in args.flags:
        flags |= re.IGNORECASE
    if args.multiline or "m" in args.flags:
        flags |= re.MULTILINE
    if args.dotall or "s" in args.flags:
        flags |= re.DOTALL
    if args.verbose or "x" in args.flags:
        flags |= re.VERBOSE

    # One-shot mode
    if args.pattern is not None or args.text is not None:
        if args.pattern is None:
            print("Error: --pattern required when using --text")
            sys.exit(1)
        if args.text is None:
            print("Error: --text required when using --pattern")
            sys.exit(1)

        exit_code = test_mode(args.pattern, args.text, flags, show_details=not args.quiet)
        sys.exit(exit_code)

    # Interactive mode
    interactive_mode()


if __name__ == "__main__":
    main()
