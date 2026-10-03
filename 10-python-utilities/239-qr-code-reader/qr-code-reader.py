#!/usr/bin/env python3
"""
QR Code Reader/Generator - Read and generate QR codes

Features:
- Generate QR codes from text/URLs
- Read QR codes from images
- Read QR codes from webcam (if available)
- Save QR codes as images
- Batch processing
- Multiple output formats (PNG, SVG, EPS)

Usage:
    python qr-code-reader.py --generate "Hello World" --output qrcode.png
    python qr-code-reader.py --read image.png
    python qr-code-reader.py --camera
"""

import argparse
import os
import sys
from pathlib import Path
from typing import Optional

try:
    import qrcode
    from PIL import Image
except ImportError:
    print("Error: Required packages not installed.")
    print("Run: pip install qrcode[pil] pillow")
    sys.exit(1)

# Try to import optional dependencies
HAS_CV2 = False
HAS_PYQT = False
HAS_PYGAME = False

try:
    import cv2
    HAS_CV2 = True
except ImportError:
    pass

try:
    from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget
    from PyQt5.QtGui import QImage, QPixmap
    from PyQt5.QtCore import Qt
    HAS_PYQT = True
except ImportError:
    pass

try:
    import pygame
    HAS_PYGAME = True
except ImportError:
    pass


class QRCodeGenerator:
    """Generate QR codes with customizable options."""

    def __init__(self):
        """Initialize the QR code generator."""
        self.default_qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )

    def generate(
        self,
        data: str,
        output_path: str = None,
        format: str = 'PNG',
        version: int = 1,
        error_correction: str = 'L',
        box_size: int = 10,
        border: int = 4,
        fill_color: str = 'black',
        back_color: str = 'white',
        fit: bool = True,
        image_format: str = None
    ) -> Image.Image:
        """
        Generate a QR code image.

        Args:
            data: Text or URL to encode
            output_path: Path to save the QR code
            format: Output format (PNG, JPEG, etc.)
            version: QR code version (1-40, auto if fit=True)
            error_correction: Error correction level (L, M, Q, H)
            box_size: Size of each box in pixels
            border: Border width in boxes
            fill_color: Foreground color
            back_color: Background color
            fit: Automatically determine version
            image_format: PIL format (defaults to format)

        Returns:
            PIL Image object
        """
        # Map error correction string to constant
        error_map = {
            'L': qrcode.constants.ERROR_CORRECT_L,
            'M': qrcode.constants.ERROR_CORRECT_M,
            'Q': qrcode.constants.ERROR_CORRECT_Q,
            'H': qrcode.constants.ERROR_CORRECT_H,
        }

        # Create QR code
        qr = qrcode.QRCode(
            version=version if not fit else None,
            error_correction=error_map.get(error_correction.upper(), qrcode.constants.ERROR_CORRECT_L),
            box_size=box_size,
            border=border,
        )

        qr.add_data(data)
        qr.make(fit=fit)

        # Create image
        img = qr.make_image(
            fill_color=fill_color,
            back_color=back_color
        )

        # Save if output path provided
        if output_path:
            img.save(output_path, format=image_format or format.upper())
            print(f"QR code saved to: {output_path}")

        return img

    def generate_svg(
        self,
        data: str,
        output_path: str,
        version: int = 1,
        error_correction: str = 'L',
        box_size: int = 10,
        border: int = 4
    ) -> str:
        """
        Generate an SVG QR code.

        Args:
            data: Text or URL to encode
            output_path: Path to save the SVG
            version: QR code version
            error_correction: Error correction level
            box_size: Size of each box
            border: Border width

        Returns:
            SVG content as string
        """
        error_map = {
            'L': qrcode.constants.ERROR_CORRECT_L,
            'M': qrcode.constants.ERROR_CORRECT_M,
            'Q': qrcode.constants.ERROR_CORRECT_Q,
            'H': qrcode.constants.ERROR_CORRECT_H,
        }

        qr = qrcode.QRCode(
            version=version,
            error_correction=error_map.get(error_correction.upper(), qrcode.constants.ERROR_CORRECT_L),
            box_size=box_size,
            border=border,
        )

        qr.add_data(data)
        qr.make()

        # Generate SVG manually
        matrix = qr.get_matrix()
        size = len(matrix)
        module_size = box_size
        total_size = size * module_size

        svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg"
     width="{total_size}" height="{total_size}"
     viewBox="0 0 {total_size} {total_size}">
  <rect width="100%" height="100%" fill="white"/>
  <path fill="black" d="'''

        for row_idx, row in enumerate(matrix):
            for col_idx, cell in enumerate(row):
                if cell:
                    x = col_idx * module_size
                    y = row_idx * module_size
                    svg += f'M{x},{y}h{module_size}v{module_size}h-{module_size}z'

        svg += '"/>'
        svg += '</svg>'

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(svg)

        print(f"SVG QR code saved to: {output_path}")
        return svg


class QRCodeReader:
    """Read QR codes from images and camera."""

    def __init__(self):
        """Initialize the QR code reader."""
        self.has_cv2 = HAS_CV2

    def read_image(self, image_path: str) -> list[dict]:
        """
        Read QR codes from an image file.

        Args:
            image_path: Path to image file

        Returns:
            List of detected QR codes with data and location
        """
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found: {image_path}")

        try:
            from pyzbar.pyzbar import decode as pyzbar_decode
            has_pyzbar = True
        except ImportError:
            has_pyzbar = False

        if has_pyzbar:
            return self._read_with_pyzbar(image_path)
        elif HAS_CV2:
            return self._read_with_cv2(image_path)
        else:
            # Fallback: use basic PIL decoding
            return self._read_with_pil(image_path)

    def _read_with_pyzbar(self, image_path: str) -> list[dict]:
        """Read QR codes using pyzbar library."""
        try:
            from pyzbar.pyzbar import decode
        except ImportError:
            print("Installing pyzbar...")
            import subprocess
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pyzbar'])
            from pyzbar.pyzbar import decode

        image = Image.open(image_path)
        results = []

        for obj in decode(image):
            results.append({
                'data': obj.data.decode('utf-8'),
                'type': obj.type,
                'rect': {
                    'left': obj.rect.left,
                    'top': obj.rect.top,
                    'width': obj.rect.width,
                    'height': obj.rect.height
                },
                'polygon': [(p.x, p.y) for p in obj.polygon]
            })

        return results

    def _read_with_cv2(self, image_path: str) -> list[dict]:
        """Read QR codes using OpenCV."""
        image = cv2.imread(image_path)
        detector = cv2.QRCodeDetector()

        data, vertices, _ = detector.detectAndDecodeMulti(image)

        if vertices is not None:
            return [{
                'data': data,
                'type': 'QRCODE',
                'rect': {'vertices': vertices.tolist()}
            }]

        return []

    def _read_with_pil(self, image_path: str) -> list[dict]:
        """Fallback: basic PIL-based reading."""
        # Try to use qrcode library's fallback detection
        from PIL import Image
        import zxingcpp

        try:
            image = Image.open(image_path)
            results = zxingcpp.read_barcodes(image)
            return [{
                'data': str(r.text),
                'type': r.format.name,
                'rect': {'x': r.position.x, 'y': r.position.y}
            } for r in results]
        except ImportError:
            pass

        raise ImportError(
            "QR reading requires pyzbar, opencv-python, or zxingcpp.\n"
            "Install one of: pip install pyzbar  # Recommended"
        )

    def read_camera(self, camera_index: int = 0, timeout: int = 0) -> Optional[str]:
        """
        Read QR codes from webcam in real-time.

        Args:
            camera_index: Camera device index
            timeout: Timeout in seconds (0 = infinite)

        Returns:
            Decoded QR code data or None
        """
        if not HAS_CV2:
            raise ImportError(
                "Camera reading requires OpenCV.\n"
                "Install with: pip install opencv-python"
            )

        cap = cv2.VideoCapture(camera_index)

        if not cap.isOpened():
            raise RuntimeError(f"Cannot open camera {camera_index}")

        detector = cv2.QRCodeDetector()
        start_time = time.time()

        print(f"Press 'q' to quit, 's' to save frame")

        while True:
            ret, frame = cap.read()

            if not ret:
                print("Failed to grab frame")
                break

            # Detect and decode QR code
            data, vertices, _ = detector.detectAndDecode(frame)

            if data:
                print(f"\nQR Code detected: {data}")
                cap.release()
                cv2.destroyAllWindows()
                return data

            # Draw rectangle around QR code if detected
            if vertices is not None and len(vertices) > 0:
                vertices = vertices[0].astype(int)
                for i in range(len(vertices)):
                    pt1 = tuple(vertices[i])
                    pt2 = tuple(vertices[(i + 1) % 4])
                    cv2.line(frame, pt1, pt2, (0, 255, 0), 2)

            # Display frame
            cv2.imshow('QR Code Scanner', frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('s'):
                cv2.imwrite('qr_capture.png', frame)
                print("Frame saved to qr_capture.png")

            # Check timeout
            if timeout > 0 and (time.time() - start_time) > timeout:
                print("Timeout reached")
                break

        cap.release()
        cv2.destroyAllWindows()
        return None


def create_qr_with_logo(
    data: str,
    logo_path: str,
    output_path: str,
    logo_size_ratio: float = 0.2
) -> Image.Image:
    """
    Create a QR code with a logo in the center.

    Args:
        data: Text or URL to encode
        logo_path: Path to logo image
        output_path: Output file path
        logo_size_ratio: Size of logo relative to QR code

    Returns:
        PIL Image with logo
    """
    # Generate QR code with high error correction
    qr = qrcode.QRCode(
        version=4,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color='black', back_color='white')

    # Calculate logo position
    qr_size = img.size[0]
    logo_size = int(qr_size * logo_size_ratio)
    logo = Image.open(logo_path).convert('RGBA')

    # Resize logo
    logo.thumbnail((logo_size, logo_size), Image.Resampling.LANCZOS)

    # Create white center circle
    center = qr_size // 2
    half_logo = logo_size // 2
    mask = Image.new('L', (logo_size, logo_size), 0)
    from PIL.ImageDraw import Draw
    draw = Draw(mask)
    draw.ellipse((0, 0, logo_size, logo_size), fill=255)

    # Paste logo with circular mask
    img.paste(logo, (center - half_logo, center - half_logo), mask)

    img.save(output_path)
    print(f"QR code with logo saved to: {output_path}")

    return img


def main():
    """Main entry point with CLI argument parsing."""
    import time

    parser = argparse.ArgumentParser(
        description='QR Code Reader/Generator',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Generate QR code:
    %(prog)s --generate "Hello World" --output qrcode.png
    %(prog)s -g "https://example.com" -o qr.png --fg-color blue --bg-color white

  Read QR from image:
    %(prog)s --read qrcode.png
    %(prog)s -r image.jpg

  Read QR from camera:
    %(prog)s --camera

  Batch generate:
    %(prog)s --batch generate --input urls.txt --output-dir ./qrcodes
        """
    )

    # Mode selection
    mode_group = parser.add_argument_group('Mode')
    mode_group.add_argument('--generate', '-g', metavar='TEXT',
                           help='Generate QR code with TEXT')
    mode_group.add_argument('--read', '-r', metavar='FILE',
                           help='Read QR code from image file')
    mode_group.add_argument('--camera', '-c', action='store_true',
                           help='Read QR code from webcam')
    mode_group.add_argument('--batch', choices=['generate', 'read'],
                           help='Batch processing mode')

    # Output options
    output_group = parser.add_argument_group('Output')
    output_group.add_argument('--output', '-o',
                             help='Output file path')
    output_group.add_argument('--format', '-f', default='PNG',
                             choices=['PNG', 'JPEG', 'SVG'],
                             help='Output format (default: PNG)')
    output_group.add_argument('--show', action='store_true',
                             help='Display generated QR code')

    # QR code options
    qr_group = parser.add_argument_group('QR Code Options')
    qr_group.add_argument('--version', type=int, default=1,
                         help='QR version (1-40, default: auto)')
    qr_group.add_argument('--error-correction', '-e', default='L',
                         choices=['L', 'M', 'Q', 'H'],
                         help='Error correction level (default: L)')
    qr_group.add_argument('--box-size', type=int, default=10,
                         help='Box size in pixels (default: 10)')
    qr_group.add_argument('--border', type=int, default=4,
                         help='Border width in boxes (default: 4)')
    qr_group.add_argument('--fg-color', default='black',
                         help='Foreground color (default: black)')
    qr_group.add_argument('--bg-color', default='white',
                         help='Background color (default: white)')

    # Logo options
    logo_group = parser.add_argument_group('Logo Options')
    logo_group.add_argument('--logo', help='Logo image path to embed in QR')
    logo_group.add_argument('--logo-size', type=float, default=0.2,
                           help='Logo size ratio (0.1-0.4, default: 0.2)')

    # Batch options
    batch_group = parser.add_argument_group('Batch Options')
    batch_group.add_argument('--input', help='Input file for batch mode')
    batch_group.add_argument('--input-dir', help='Input directory for batch mode')
    batch_group.add_argument('--output-dir', help='Output directory')

    # Camera options
    camera_group = parser.add_argument_group('Camera Options')
    camera_group.add_argument('--camera-index', type=int, default=0,
                             help='Camera device index (default: 0)')
    camera_group.add_argument('--timeout', type=int, default=0,
                             help='Camera timeout in seconds (0 = infinite)')

    args = parser.parse_args()

    try:
        # Generate mode
        if args.generate:
            output_path = args.output or 'qrcode.png'

            if args.format.upper() == 'SVG':
                generator = QRCodeGenerator()
                generator.generate_svg(
                    data=args.generate,
                    output_path=output_path,
                    error_correction=args.error_correction,
                    version=args.version,
                    box_size=args.box_size,
                    border=args.border
                )
            elif args.logo:
                create_qr_with_logo(
                    data=args.generate,
                    logo_path=args.logo,
                    output_path=output_path,
                    logo_size_ratio=args.logo_size
                )
            else:
                generator = QRCodeGenerator()
                img = generator.generate(
                    data=args.generate,
                    output_path=output_path,
                    format=args.format,
                    version=args.version,
                    error_correction=args.error_correction,
                    box_size=args.box_size,
                    border=args.border,
                    fill_color=args.fg_color,
                    back_color=args.bg_color
                )

                if args.show:
                    img.show()

        # Read mode
        elif args.read:
            reader = QRCodeReader()
            results = reader.read_image(args.read)

            if results:
                print(f"\nFound {len(results)} QR code(s):\n")
                for i, result in enumerate(results, 1):
                    print(f"QR Code {i}:")
                    print(f"  Data: {result['data']}")
                    print(f"  Type: {result.get('type', 'UNKNOWN')}")
                    print()
            else:
                print("No QR code found in image")

        # Camera mode
        elif args.camera:
            reader = QRCodeReader()
            result = reader.read_camera(
                camera_index=args.camera_index,
                timeout=args.timeout
            )

            if result:
                print(f"\nDecoded: {result}")

        # Batch generate mode
        elif args.batch == 'generate':
            if not args.input:
                print("Error: --input required for batch generate")
                sys.exit(1)

            output_dir = Path(args.output_dir or 'qrcodes')
            output_dir.mkdir(parents=True, exist_ok=True)

            with open(args.input, 'r') as f:
                lines = f.readlines()

            generator = QRCodeGenerator()

            for i, line in enumerate(lines, 1):
                data = line.strip()
                if not data:
                    continue

                output_path = output_dir / f'qrcode_{i}.png'
                generator.generate(
                    data=data,
                    output_path=str(output_path),
                    error_correction=args.error_correction,
                    version=args.version,
                    box_size=args.box_size
                )

            print(f"Generated {len(lines)} QR codes in {output_dir}")

        # Batch read mode
        elif args.batch == 'read':
            input_dir = Path(args.input_dir or '.')

            reader = QRCodeReader()
            extensions = {'.png', '.jpg', '.jpeg', '.gif', '.bmp'}

            files = [f for f in input_dir.iterdir() if f.suffix.lower() in extensions]

            print(f"Scanning {len(files)} images...\n")

            for file in files:
                results = reader.read_image(str(file))
                if results:
                    for result in results:
                        print(f"{file.name}: {result['data']}")

        else:
            parser.print_help()

    except ImportError as e:
        print(f"\nError: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\nError: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
