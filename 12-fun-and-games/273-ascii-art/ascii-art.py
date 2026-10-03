#!/usr/bin/env python3
"""
ASCII Art Generator - Create beautiful ASCII art from text
Supports multiple fonts and color output
"""

import argparse
import sys
from colorama import init, Fore, Style

# Initialize colorama for cross-platform color support
init(autoreset=True)

def list_fonts():
    """Display all available ASCII art fonts"""
    fonts = [
        "block", "banner", "standard", "avatar", "avatar-flipped",
        "banner3", "banner3-flipped", "banner4", "digital",
        "doh", "epic", "eftiwall", "fender", "isometric1",
        "isometric2", "isometric3", "isometric4", "letters",
        "musical", "peaks", "rusto", "rusto-flipped", "slblock",
        "small", "isometric", "univers", "weird"
    ]
    print("\nAvailable Fonts:")
    print("-" * 40)
    for i, font in enumerate(fonts, 1):
        print(f"  {i:2}. {font}")
    print()

def get_color_code(color_name):
    """Map color name to Fore color code"""
    colors = {
        'red': Fore.RED,
        'green': Fore.GREEN,
        'yellow': Fore.YELLOW,
        'blue': Fore.BLUE,
        'magenta': Fore.MAGENTA,
        'cyan': Fore.CYAN,
        'white': Fore.WHITE,
    }
    return colors.get(color_name.lower(), Fore.WHITE)

def generate_art(text, font="standard", color=None):
    """Generate ASCII art from text using available methods"""
    # Simple built-in ASCII art fonts (no external dependency needed)
    fonts = {
        'block': _block_font,
        'banner': _banner_font,
        'standard': _standard_font,
        'shadow': _shadow_font,
        'slant': _slant_font,
    }

    # If using external art library, try that first
    try:
        from art import text2art
        art_text = text2art(text, font=font)
        return art_text
    except Exception:
        # Fall back to built-in fonts
        font_func = fonts.get(font, _standard_font)
        return font_func(text)

def _standard_font(text):
    """Simple standard ASCII art"""
    result = []
    for char in text.upper():
        if char == ' ':
            result.append("   ")
        elif char.isalpha():
            result.append(_letter_standard(char))
        else:
            result.append(" _ ")
    return "\n".join(["  ".join(chars) for chars in zip(*result)])

def _letter_standard(char):
    """Standard font letter patterns"""
    letters = {
        'A': [" _ ", "/|\\", "/_\\"],
        'B': ["_  ", "(_ ", "(_) "],
        'C': [" _ ", "/  ", "\\ _"],
        'D': ["_  ", "| \\", "|_|"],
        'E': ["___", "|  ", "|__"],
        'F': ["___", "|  ", "|   "],
        'G': [" _ ", "/  ", "\\_|"],
        'H': ["   ", "|_|", "| |"],
        'I': ["___", " | ", " | "],
        'J': ["___", "  |", "\\_|"],
        'K': ["   ", "|_>", "|<  "],
        'L': ["   ", "|  ", "|___"],
        'M': ["   ", "|\\|", "| |"],
        'N': ["   ", "|\\|", "| \\|"],
        'O': [" _ ", "| |", "|_|"],
        'P': ["_  ", "|_ ", "|   "],
        'Q': [" _ ", "| |", "|_>"],
        'R': ["_  ", "|_ ", "|  \\"],
        'S': [" ___", "/   ", "___/"],
        'T': ["___", " | ", " | "],
        'U': ["   ", "| |", "|_|"],
        'V': ["   ", "\\ /", " V "],
        'W': ["   ", "| |", "|/\\|"],
        'X': ["   ", "\\ /", " X "],
        'Y': ["   ", "\\|/", " | "],
        'Z': ["___", "  /", "/__"],
    }
    return letters.get(char, [" ? ", " ? ", " ? "])

def _block_font(text):
    """Block-style ASCII art"""
    block_chars = {
        'A': ["█████", "█   █", "█████", "█   █", "█   █"],
        'B': ["████ ", "█   █", "████ ", "█   █", "████ "],
        'C': ["█████", "█    ", "█    ", "█    ", "█████"],
        'D': ["████ ", "█   █", "█   █", "█   █", "████ "],
        'E': ["█████", "█    ", "████ ", "█    ", "█████"],
        'F': ["█████", "█    ", "████ ", "█    ", "█    "],
        'G': ["█████", "█    ", "█  ██", "█   █", "█████"],
        'H': ["█   █", "█   █", "█████", "█   █", "█   █"],
        'I': ["█████", "  █  ", "  █  ", "  █  ", "█████"],
        'J': ["█████", "   █ ", "   █ ", "█  █ ", "████ "],
        'K': ["█   █", "█  █ ", "████ ", "█  █ ", "█   █"],
        'L': ["█    ", "█    ", "█    ", "█    ", "█████"],
        'M': ["█   █", "██ ██", "█ █ █", "█   █", "█   █"],
        'N': ["█   █", "██  █", "█ █ █", "█  ██", "█   █"],
        'O': ["█████", "█   █", "█   █", "█   █", "█████"],
        'P': ["█████", "█   █", "█████", "█    ", "█    "],
        'Q': ["█████", "█   █", "█ █ █", "█  █ ", "███ █"],
        'R': ["█████", "█   █", "█████", "█  █ ", "█   █"],
        'S': ["█████", "█    ", "█████", "    █", "█████"],
        'T': ["█████", "  █  ", "  █  ", "  █  ", "  █  "],
        'U': ["█   █", "█   █", "█   █", "█   █", "█████"],
        'V': ["█   █", "█   █", "█   █", " █ █ ", "  █  "],
        'W': ["█   █", "█   █", "█ █ █", "██ ██", "█   █"],
        'X': ["█   █", " █ █ ", "  █  ", " █ █ ", "█   █"],
        'Y': ["█   █", " █ █ ", "  █  ", "  █  ", "  █  "],
        'Z': ["█████", "   █ ", "  █  ", " █   ", "█████"],
        '0': ["█████", "█   █", "█   █", "█   █", "█████"],
        '1': ["  █  ", " ██  ", "  █  ", "  █  ", "█████"],
        '2': ["█████", "    █", "█████", "█    ", "█████"],
        '3': ["█████", "    █", "█████", "    █", "█████"],
        '4': ["█   █", "█   █", "█████", "    █", "    █"],
        '5': ["█████", "█    ", "█████", "    █", "█████"],
        '6': ["█████", "█    ", "█████", "█   █", "█████"],
        '7': ["█████", "    █", "   █ ", "  █  ", "  █  "],
        '8': ["█████", "█   █", "█████", "█   █", "█████"],
        '9': ["█████", "█   █", "█████", "    █", "█████"],
        ' ': ["     ", "     ", "     ", "     ", "     "],
        '!': [" █  ", " █  ", " █  ", "    ", " █  "],
        '.': ["   ", "   ", "   ", "   ", "███"],
        '?': ["█████", "    █", " ████", "     ", "  █  "],
    }

    lines = ["", "", "", "", ""]
    for char in text.upper():
        char_lines = block_chars.get(char, ["     ", "     ", "     ", "     ", "     "])
        for i in range(5):
            lines[i] += char_lines[i] + " "
    return "\n".join(lines)

def _banner_font(text):
    """Banner-style ASCII art"""
    return f"""
╔═══════════════════════════════════════╗
║                                       ║
║   {' '.join(text.upper())}   ║
║                                       ║
╚═══════════════════════════════════════╝
"""

def _shadow_font(text):
    """Shadow-style ASCII art"""
    result = []
    for char in text.upper():
        result.append(_letter_shadow(char))

    lines = ["", "", "", "", ""]
    for letter_lines in result:
        for i in range(5):
            lines[i] += letter_lines[i] + "  "

    return "\n".join(lines)

def _letter_shadow(char):
    """Shadow font letter patterns"""
    letters = {
        'A': [" ▄▄█", "▄█▀▄", "███ ", "▀▀▀ "],
        'B': ["▄██▄", "█▀▄ ", "███▄", "▀▀▀ "],
        'C': [" ▄██", "▐█  ", " █▌ ", "███▀"],
        'D': ["▄██ ", "█▀▄ ", "█▄▀ ", "███▄"],
        'E': ["▄██▄", "█▀  ", "██▄ ", "▀▀▀▀"],
        'F': ["████", "█▀  ", "█▀  ", "▀▀▀ "],
        'G': [" ▄██", "▐█▄▄", " █▀▄", "███▀"],
        'H': ["▀▀▀ ", "███ ", " █▀▄", "▀▀▀ "],
        'I': ["█▀▀█", " ▐█ ", "▄█▄ ", "▀▀▀▀"],
        'J': ["▀▀█▄", "  ▐█", " ▐█ ", "███▀"],
        'K': ["█▄█▀", "█▀█▐", "▐██ ", "▀▀▀ "],
        'L': ["▐█  ", "▐█  ", "▐█▄▄", "▀▀▀▀"],
        'M': ["█▀█▄", "▐██▌", " ▐▐▌ ", " ▀ ▀ "],
        'N': ["█▀▀▄", "▐█ ▐", " ▐ ▐", " ▀ ▀ "],
        'O': [" ▄██▄", "█▀▀▀█", "▐ ▀▀ ▐", " ████ "],
        'P': ["▄██▄", "█▀▀▄", "███▀", "▀▀▀ "],
        'Q': [" ▄██▄", "█▀▀▀█", " ▐▀▀▌", "  ██ "],
        'R': ["▄██▄", "█▀▀▄", "███▀", "▀ ▀ "],
        'S': ["▄████", "█▀   ", " ███▄", "████▀"],
        'T': ["█████", " ▐█  ", "  █  ", "  ▀  "],
        'U': ["▀▀▀ ", " █▀▄", "  ▐█", " ██▀"],
        'V': ["▀▀▀ ", " █▀▄", "  ▐█", "  ▀ "],
        'W': ["▀▀▀ ", " █▀▄", " ▐██▌", "▄▐█▄▀"],
        'X': ["▀▀▀ ", " █▀▄", "▄█▀ ", "▀▀▀ "],
        'Y': ["▀▀▀ ", " █▀▄", "  ▐█", "  ▀ "],
        'Z': ["█████", "  ▀▀", "▄█▀ ", "█████"],
    }
    return letters.get(char, ["    ", "    ", "    ", "    "])

def _slant_font(text):
    """Slant-style ASCII art"""
    result = []
    for char in text.upper():
        result.append(_letter_slant(char))

    lines = ["", "", "", "", ""]
    for letter_lines in result:
        for i in range(5):
            lines[i] += letter_lines[i] + " "

    return "\n".join(lines)

def _letter_slant(char):
    """Slant font letter patterns"""
    letters = {
        'A': ["  /\\", " /__\\", "/    \\"],
        'B': ["/\\  ", "|\\  |", "\\__/"],
        'C': ["  /\\", " |  ", " \\/"],
        'D': ["/\\  ", "|  \\", "|__/"],
        'E': ["/\\  ", "|_  ", "|__\\"],
        'F': ["/\\  ", "|_  ", "|   "],
        'G': ["  /\\", " |_\\", "/_ |\\_"],
        'H': ["   |", " |_|", " | |"],
        'I': ["  |", " | ", " |_/"],
        'J': ["   |", "   |", "  _|"],
        'K': ["   |", " |< ", " | \\"],
        'L': [" |  ", " |  ", " |__"],
        'M': ["  |\\|/","|   |","|   |"],
        'N': ["  |\\", " | \\|","|  \\|"],
        'O': ["  /\\", " |  |", " \\/"],
        'P': ["/\\  ", "|\\  ", "|   "],
        'Q': ["  /\\", " |  |", " \\/\\"],
        'R': ["/\\  ", "|\\  |","| \\ "],
        'S': ["  /\\", "  |", " /\\"],
        'T': ["  |", "  |", "  |"],
        'U': ["   |", "   |", " \\_/"],
        'V': ["   \\/", "   /\\", "   "],
        'W': ["   |", "  /|\\", " / | \\"],
        'X': ["   \\/", "   X", "  /\\"],
        'Y': ["   \\/", "  |", "  |"],
        'Z': ["  /", " / ", "/  "],
    }
    return letters.get(char, ["   ", "   ", "   "])

def interactive_mode():
    """Interactive mode for creating ASCII art"""
    print("\n" + "="*50)
    print("       Welcome to ASCII Art Generator!")
    print("="*50)
    print("\nType 'quit' or 'exit' to leave the program.")
    print("Type 'fonts' to see available fonts.")
    print("Type 'colors' to see available colors.\n")

    while True:
        try:
            text = input("Enter text: ").strip()
            if text.lower() in ['quit', 'exit', 'q']:
                print("\nThanks for using ASCII Art Generator! Goodbye!\n")
                break

            if text.lower() == 'fonts':
                list_fonts()
                continue

            if text.lower() == 'colors':
                print("\nAvailable Colors: red, green, yellow, blue, magenta, cyan, white\n")
                continue

            if not text:
                print("Please enter some text!\n")
                continue

            print("\nSelect font (press Enter for default 'block'):")
            print("  1. block (default)")
            print("  2. banner")
            print("  3. shadow")
            print("  4. slant")
            font_choice = input("Choice: ").strip()

            fonts_map = {
                '1': 'block', '2': 'banner', '3': 'shadow', '4': 'slant', ''
                : 'block'
            }
            font = fonts_map.get(font_choice, 'block')

            print("\nSelect color (press Enter for no color):")
            print("  1. red    2. green   3. yellow")
            print("  4. blue   5. magenta 6. cyan    7. white")
            color_choice = input("Choice: ").strip()

            colors_map = {
                '1': 'red', '2': 'green', '3': 'yellow', '4': 'blue',
                '5': 'magenta', '6': 'cyan', '7': 'white'
            }
            color = colors_map.get(color_choice)

            print()
            art = generate_art(text, font, color)

            if color:
                color_code = get_color_code(color)
                print(f"{color_code}{art}{Style.RESET_ALL}")
            else:
                print(art)
            print()

        except KeyboardInterrupt:
            print("\n\nInterrupted. Goodbye!\n")
            break

def main():
    parser = argparse.ArgumentParser(
        description="ASCII Art Generator - Create beautiful ASCII art from text",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python ascii-art.py "Hello World"
  python ascii-art.py "Python" --font block --color cyan
  python ascii-art.py --list-fonts
  python ascii-art.py -i
        """
    )

    parser.add_argument("text", nargs="?", help="Text to convert to ASCII art")
    parser.add_argument("-f", "--font", default="block",
                       help="Font style (default: block)")
    parser.add_argument("-c", "--color",
                       help="Text color (red, green, yellow, blue, magenta, cyan, white)")
    parser.add_argument("-s", "--save", metavar="FILE",
                       help="Save ASCII art to file")
    parser.add_argument("-l", "--list-fonts", action="store_true",
                       help="List all available fonts")
    parser.add_argument("-i", "--interactive", action="store_true",
                       help="Interactive mode")

    args = parser.parse_args()

    if args.list_fonts:
        list_fonts()
        return

    if args.interactive or (not args.text and not args.list_fonts):
        interactive_mode()
        return

    if not args.text:
        parser.print_help()
        return

    # Generate the ASCII art
    art = generate_art(args.text, args.font, args.color)

    # Display with color if specified
    if args.color:
        color_code = get_color_code(args.color)
        print(f"{color_code}{art}{Style.RESET_ALL}")
    else:
        print(art)

    # Save to file if requested
    if args.save:
        try:
            with open(args.save, 'w', encoding='utf-8') as f:
                f.write(art)
            print(f"\nASCII art saved to: {args.save}")
        except Exception as e:
            print(f"\nError saving file: {e}")

if __name__ == "__main__":
    main()
