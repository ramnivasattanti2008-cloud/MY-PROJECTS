#!/usr/bin/env python3
"""
QR Generator - Command-line QR code generator.
Generate QR codes from text/URL and save as PNG images.
Usage: python qr-generator.py [text/URL] [options]
"""

import os
import sys
import argparse
from pathlib import Path

# Check for qrcode library
try:
    import qrcode
    from qrcode.image.pure import PymagingPNGImage
    from qrcode.image.svg import SvgImage
    QRCODE_AVAILABLE = True
except ImportError:
    QRCODE_AVAILABLE = False

# Optional: image processing
try:
    from PIL import Image, ImageDraw
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False


def generate_qr(text: str, output_path: str = None,
                size: int = 300, border: int = 4,
                box_size: int = 10, error_correction: str = 'M',
                format: str = 'png', dark: str = 'black',
                light: str = 'white', logo_path: str = None,
                quiet_zone: bool = True) -> str:
    """Generate a QR code and save it to a file."""

    if not QRCODE_AVAILABLE:
        raise ImportError("qrcode library not installed. Run: pip install qrcode[pil]")

    # Error correction levels
    error_levels = {
        'L': qrcode.constants.ERROR_CORRECT_L,  # 7%
        'M': qrcode.constants.ERROR_CORRECT_M,   # 15%
        'Q': qrcode.constants.ERROR_CORRECT_Q,   # 25%
        'H': qrcode.constants.ERROR_CORRECT_H,   # 30%
    }

    # Create QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=error_levels.get(error_correction.upper(), qrcode.constants.ERROR_CORRECT_M),
        box_size=box_size,
        border=border if quiet_zone else 0,
    )

    qr.add_data(text)
    qr.make(fit=True)

    # Create image
    if PIL_AVAILABLE and format == 'png':
        img = qr.make_image(fill_color=dark, back_color=light)

        # Resize if needed
        if size != 300:
            img = img.resize((size, size), Image.Resampling.LANCZOS)

        # Add logo if provided
        if logo_path and os.path.exists(logo_path):
            img = add_logo_to_qr(img, logo_path)

        # Save
        if output_path is None:
            output_path = f"qrcode_{hash(text) % 100000}.png"

        img.save(output_path)
    else:
        # Fallback to pure Python image
        if format == 'png':
            img = qr.make_image(image_factory=PymagingPNGImage)
        elif format == 'svg':
            img = qr.make_image(image_factory=SvgImage)
        else:
            img = qr.make_image()

        if output_path is None:
            output_path = f"qrcode_{hash(text) % 100000}.{format}"

        img.save(output_path)

    return output_path


def add_logo_to_qr(qr_image, logo_path: str, logo_size_ratio: float = 0.2):
    """Add a logo to the center of a QR code."""
    if not PIL_AVAILABLE:
        print("Warning: PIL not available, skipping logo")
        return qr_image

    try:
        # Open logo
        logo = Image.open(logo_path)

        # Convert to RGBA if needed
        if logo.mode != 'RGBA':
            logo = logo.convert('RGBA')

        # Calculate logo size (20% of QR code by default)
        qr_size = qr_image.size[0]
        logo_size = int(qr_size * logo_size_ratio)

        # Resize logo
        logo = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)

        # Create a white background for logo (for non-transparent images)
        background = Image.new('RGBA', logo.size, (255, 255, 255, 255))
        background.paste(logo, (0, 0), logo)

        # Calculate position (center)
        position = ((qr_size - logo_size) // 2, (qr_size - logo_size) // 2)

        # Create a mask for the logo area
        # QR codes have modules, so we need to clear a region first
        qr_copy = qr_image.copy()
        if qr_copy.mode != 'RGBA':
            qr_copy = qr_copy.convert('RGBA')

        # Clear the center area with white
        from PIL import ImageDraw
        draw = ImageDraw.Draw(qr_copy)
        draw.rectangle(
            [position[0] - 5, position[1] - 5,
             position[0] + logo_size + 5, position[1] + logo_size + 5],
            fill=(255, 255, 255, 255)
        )

        # Paste logo
        qr_copy.paste(background, position, background)

        return qr_copy

    except Exception as e:
        print(f"Warning: Could not add logo: {e}")
        return qr_image


def generate_svg(text: str, output_path: str = None,
                  size: int = 300, border: int = 4) -> str:
    """Generate an SVG QR code."""
    if not QRCODE_AVAILABLE:
        raise ImportError("qrcode library not installed. Run: pip install qrcode[pil]")

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=border,
    )

    qr.add_data(text)
    qr.make(fit=True)

    if output_path is None:
        output_path = f"qrcode_{hash(text) % 100000}.svg"

    img = qr.make_image(back_color='white')
    img.save(output_path)

    return output_path


def print_qr_ascii(text: str, size: int = 21):
    """Print QR code as ASCII art (for terminal display)."""
    if not QRCODE_AVAILABLE:
        print("Error: qrcode library not installed")
        return

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=1,
        border=1,
    )

    qr.add_data(text)
    qr.make(fit=True)

    matrix = qr.get_matrix()

    # Print top border
    print("┌" + "─" * len(matrix) + "┐")

    for row in matrix:
        line = "│"
        for cell in row:
            line += "█" if cell else " "
        line += "│"
        print(line)

    # Print bottom border
    print("└" + "─" * len(matrix) + "┘")


def validate_qr(file_path: str) -> bool:
    """Validate a QR code image."""
    if not PIL_AVAILABLE:
        print("Warning: PIL not available for validation")
        return False

    try:
        img = Image.open(file_path)

        # Check if it's a valid image
        img.verify()

        # Re-open after verify
        img = Image.open(file_path)

        # Try to decode QR
        try:
            import zxingcpp
            result = zxingcpp.read_barcodes(str(file_path))
            if result:
                print(f"Valid QR Code: {result[0].text}")
                return True
        except ImportError:
            pass

        return True

    except Exception as e:
        print(f"Invalid QR code: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="QR Generator - Generate QR codes from text/URL",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "https://example.com" -o qr.png
  %(prog)s "Hello World" --size 500
  %(prog)s "My WiFi:WPA:password:H" --wifi
  %(prog)s --ascii "https://example.com"
  %(prog)s --interactive
        """
    )

    # Input
    parser.add_argument('text', nargs='?', help='Text or URL to encode')
    parser.add_argument('-f', '--file', help='Read text from file')
    parser.add_argument('--interactive', action='store_true', help='Interactive mode')

    # Output
    parser.add_argument('-o', '--output', help='Output file path')
    parser.add_argument('-F', '--format', choices=['png', 'svg'], default='png',
                        help='Output format (default: png)')

    # Appearance
    parser.add_argument('-s', '--size', type=int, default=300,
                        help='Image size in pixels (default: 300)')
    parser.add_argument('-b', '--border', type=int, default=4,
                        help='Border size in modules (default: 4)')
    parser.add_argument('-d', '--dark', default='black',
                        help='Dark module color (default: black)')
    parser.add_argument('-l', '--light', default='white',
                        help='Light module color (default: white)')
    parser.add_argument('--no-quiet-zone', action='store_true',
                        help='Remove quiet zone (border)')

    # QR settings
    parser.add_argument('-e', '--error', choices=['L', 'M', 'Q', 'H'],
                        default='M', help='Error correction level (default: M)')
    parser.add_argument('--box-size', type=int, default=10,
                        help='Box size in pixels (default: 10)')

    # Special modes
    parser.add_argument('--ascii', action='store_true',
                        help='Print QR code as ASCII art in terminal')
    parser.add_argument('--wifi', metavar='SSID:WPA:PASSWORD:H',
                        help='Generate WiFi QR code')
    parser.add_argument('--validate', metavar='FILE',
                        help='Validate a QR code image')

    # Logo
    parser.add_argument('--logo', help='Add logo to center of QR code')
    parser.add_argument('--logo-size', type=float, default=0.2,
                        help='Logo size ratio (0.1-0.3, default: 0.2)')

    args = parser.parse_args()

    # Validate library
    if not QRCODE_AVAILABLE:
        print("Error: qrcode library is not installed.")
        print("\nPlease install it with:")
        print("  pip install qrcode[pil]")
        print("\nOr simply:")
        print("  pip install qrcode")
        return 1

    # Validate QR code
    if args.validate:
        valid = validate_qr(args.validate)
        return 0 if valid else 1

    # Interactive mode
    if args.interactive:
        print("\nInteractive QR Code Generator")
        print("=" * 40)
        print("Enter text/URL to generate QR code")
        print("Commands:")
        print("  :wifi <ssid> <password> - Generate WiFi QR")
        print("  :size <pixels> - Set image size")
        print("  :color <dark> <light> - Set colors")
        print("  :quit - Exit")
        print("=" * 40)

        while True:
            try:
                text = input("\n> ").strip()

                if not text:
                    continue

                if text == ':quit':
                    print("Goodbye!")
                    break

                if text.startswith(':wifi'):
                    parts = text.split()
                    if len(parts) >= 3:
                        ssid = parts[1]
                        password = parts[2]
                        auth = parts[3] if len(parts) > 3 else 'WPA'
                        text = f"WIFI:T:{auth};S:{ssid};P:{password};;"
                        print(f"Generating WiFi QR for: {ssid}")
                    else:
                        print("Usage: :wifi <ssid> <password> [auth]")
                        continue

                if text.startswith(':size'):
                    try:
                        size = int(text.split()[1])
                        print(f"Size set to: {size}px")
                        continue
                    except (IndexError, ValueError):
                        print("Usage: :size <pixels>")
                        continue

                if text.startswith(':color'):
                    parts = text.split()
                    if len(parts) >= 3:
                        print(f"Colors set to: dark={parts[1]}, light={parts[2]}")
                    continue

                output_path = f"qrcode_{hash(text) % 100000}.png"
                path = generate_qr(
                    text,
                    output_path=output_path,
                    size=300,
                    dark='black',
                    light='white',
                    logo_path=args.logo
                )
                print(f"QR code saved to: {path}")

            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except EOFError:
                break

        return 0

    # Build text to encode
    text = None

    if args.text:
        text = args.text
    elif args.file:
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                text = f.read().strip()
        except FileNotFoundError:
            print(f"Error: File not found: {args.file}")
            return 1
        except Exception as e:
            print(f"Error reading file: {e}")
            return 1
    elif args.wifi:
        # Parse WiFi string: SSID:WPA:PASSWORD:H
        parts = args.wifi.split(':')
        if len(parts) >= 3:
            ssid = parts[0]
            auth = parts[1]
            password = parts[2]
            text = f"WIFI:T:{auth};S:{ssid};P:{password};;"
        else:
            print("Error: WiFi format should be: SSID:WPA:PASSWORD")
            return 1
    else:
        parser.print_help()
        print("\nNote: Provide text/URL as argument or use -f/--file")
        return 1

    # ASCII mode
    if args.ascii:
        print_qr_ascii(text)
        return 0

    # Generate QR code
    try:
        output_path = args.output

        if args.format == 'svg':
            output_path = generate_svg(
                text,
                output_path=output_path,
                size=args.size,
                border=args.border
            )
        else:
            output_path = generate_qr(
                text,
                output_path=output_path,
                size=args.size,
                border=args.border,
                box_size=args.box_size,
                error_correction=args.error,
                format=args.format,
                dark=args.dark,
                light=args.light,
                logo_path=args.logo,
                quiet_zone=not args.no_quiet_zone
            )

        print(f"QR code generated successfully!")
        print(f"Saved to: {output_path}")

        # Print ASCII preview
        print("\nASCII Preview:")
        print_qr_ascii(text)

        return 0

    except Exception as e:
        print(f"Error generating QR code: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
