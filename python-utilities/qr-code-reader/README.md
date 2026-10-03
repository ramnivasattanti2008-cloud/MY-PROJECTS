# QR Code Reader/Generator

A versatile Python tool for generating and reading QR codes. Supports image files, webcam input, batch processing, and custom styling.

## Features

- Generate QR codes with customizable options
- Read QR codes from images
- Read QR codes from webcam
- Create QR codes with logos embedded
- Batch processing
- Multiple output formats (PNG, JPEG, SVG)
- Color customization

## Installation

```bash
pip install -r requirements.txt
```

### Optional Dependencies

For reading QR codes from images (recommended):
```bash
pip install pyzbar
```

For reading QR codes from webcam:
```bash
pip install opencv-python
```

### Windows Note

If `pyzbar` fails to install, try:
```bash
pip install pyzbar --no-binary :all:
```

## Quick Start

### Generate a QR Code

```bash
# Basic QR code
python qr-code-reader.py --generate "Hello World" --output qrcode.png

# QR code with custom colors
python qr-code-reader.py -g "https://example.com" -o qr.png --fg-color blue --bg-color white

# High error correction (for logos)
python qr-code-reader.py -g "https://example.com" -o qr.png -e H
```

### Read a QR Code from Image

```bash
python qr-code-reader.py --read qrcode.png
python qr-code-reader.py -r image.jpg
```

### Read QR Code from Webcam

```bash
python qr-code-reader.py --camera
# Press 'q' to quit
# Press 's' to save current frame
```

## Command Line Options

### Generation Options

| Option | Description |
|--------|-------------|
| `--generate, -g` | Text or URL to encode |
| `--output, -o` | Output file path |
| `--format, -f` | Output format: PNG, JPEG, SVG |
| `--show` | Display QR code after generation |
| `--version` | QR version (1-40, auto by default) |
| `--error-correction, -e` | Error correction: L, M, Q, H |
| `--box-size` | Box size in pixels (default: 10) |
| `--border` | Border width in boxes (default: 4) |
| `--fg-color` | Foreground color |
| `--bg-color` | Background color |
| `--logo` | Logo image path (embedded in QR) |
| `--logo-size` | Logo size ratio (0.1-0.4) |

### Reading Options

| Option | Description |
|--------|-------------|
| `--read, -r` | Read QR from image file |
| `--camera, -c` | Read QR from webcam |
| `--camera-index` | Camera device index |
| `--timeout` | Camera timeout in seconds |

### Batch Options

| Option | Description |
|--------|-------------|
| `--batch` | Batch mode: generate or read |
| `--input` | Input file/directory |
| `--input-dir` | Input directory for batch read |
| `--output-dir` | Output directory |

## Examples

### Generate QR Code for URL

```bash
python qr-code-reader.py -g "https://www.google.com" -o google_qr.png
```

### Generate with Logo

```bash
python qr-code-reader.py -g "https://shop.example.com" \
    --logo logo.png \
    --logo-size 0.25 \
    --output branded_qr.png
```

### Generate SVG Format

```bash
python qr-code-reader.py -g "Hello SVG" --format SVG -o qr.svg
```

### Batch Generate from Text File

Create `urls.txt`:
```
https://google.com
https://github.com
https://python.org
```

Run:
```bash
python qr-code-reader.py --batch generate \
    --input urls.txt \
    --output-dir ./qrcodes
```

### Batch Read from Directory

```bash
python qr-code-reader.py --batch read \
    --input-dir ./images \
    --output results.txt
```

### High Error Correction for Logos

QR codes with embedded logos need high error correction:

```bash
# H = 30% recovery (recommended for logos)
python qr-code-reader.py -g "Data with logo" -e H --logo logo.png

# Q = 25% recovery (good for logos)
python qr-code-reader.py -g "Data with logo" -e Q --logo logo.png
```

## Using as a Python Module

```python
from qr-code-reader import QRCodeGenerator, QRCodeReader

# Generate QR code
generator = QRCodeGenerator()
img = generator.generate(
    data="Hello World",
    output_path="qrcode.png",
    fill_color="blue",
    back_color="white",
    error_correction="H"
)

# Generate SVG
generator.generate_svg(
    data="https://example.com",
    output_path="qrcode.svg"
)

# Generate with logo
from qr-code-reader import create_qr_with_logo
create_qr_with_logo(
    data="https://shop.example.com",
    logo_path="logo.png",
    output_path="branded_qr.png"
)

# Read from image
reader = QRCodeReader()
results = reader.read_image("qrcode.png")

for result in results:
    print(f"Data: {result['data']}")
    print(f"Type: {result.get('type', 'UNKNOWN')}")

# Read from camera
reader = QRCodeReader()
result = reader.read_camera(timeout=30)  # 30 second timeout
if result:
    print(f"Decoded: {result}")
```

## Error Correction Levels

| Level | Recovery | Best Use Case |
|-------|----------|---------------|
| L | 7% | General use, maximum density |
| M | 15% | Standard use |
| Q | 25% | Logos/watermarks |
| H | 30% | High logos, industrial use |

## QR Code Versions

| Version | Size | Max Characters (Numeric) |
|---------|------|---------------------------|
| 1 | 21x21 | 41 |
| 10 | 57x57 | 1,114 |
| 20 | 97x97 | 4,296 |
| 40 | 177x177 | 18,296 |

The script auto-selects the minimum version needed for your data when `fit=True`.

## Troubleshooting

**"No module named 'pyzbar'"**
```bash
pip install pyzbar
```

**"DLL load failed" on Windows**
```bash
pip uninstall pyzbar
pip install pyzbar --no-binary :all:
```

**Camera not working**
- Check if camera is connected
- Try different `--camera-index` (0, 1, 2...)
- Install opencv-python: `pip install opencv-python`

**QR code won't scan**
- Increase error correction: `-e H`
- Make QR code larger
- Ensure sufficient contrast between colors
- Don't cover too much of the QR with logo (max 30%)

## License

MIT License
