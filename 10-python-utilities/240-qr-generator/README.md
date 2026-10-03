# QR Generator

A Python command-line tool to generate QR codes from text or URLs and save them as PNG images.

## Features

- **Multiple formats**: PNG and SVG output
- **ASCII preview**: Print QR code as ASCII art in terminal
- **Customizable appearance**: Colors, size, border, box size
- **Error correction**: L, M, Q, H levels (up to 30% recovery)
- **WiFi QR codes**: Generate QR codes for WiFi network sharing
- **Logo embedding**: Add logo to center of QR code
- **Interactive mode**: Continuous QR code generation
- **File input**: Generate QR from file contents
- **Validation**: Validate existing QR code images

## Installation

```bash
pip install -r requirements.txt
```

Required dependencies:
- `qrcode[pil]` - QR code generation
- `Pillow` - Image processing

## Usage

### Basic usage

```bash
# Generate from URL
python qr-generator.py "https://example.com" -o qr.png

# Generate from text
python qr-generator.py "Hello World" -o hello.png

# Specify size
python qr-generator.py "https://example.com" -o qr.png -s 500
```

### ASCII art preview

```bash
python qr-generator.py "https://example.com" --ascii
```

### WiFi QR code

```bash
# Standard WiFi QR (WPA/WPA2)
python qr-generator.py --wifi "MyWiFi:WPA:password123" -o wifi.png

# WEP (older networks)
python qr-generator.py --wifi "NetworkName:WEP:key123" -o wifi.png

# Open network
python qr-generator.py --wifi "OpenNetwork::" -o wifi.png
```

### Read from file

```bash
# Generate from file contents
python qr-generator.py -f text.txt -o output.png
```

### Custom appearance

```bash
# Custom colors
python qr-generator.py "https://example.com" -o qr.png -d "0033FF" -l "FFFFFF"

# Custom border and box size
python qr-generator.py "https://example.com" -b 2 --box-size 15 -o qr.png

# No quiet zone (border)
python qr-generator.py "https://example.com" --no-quiet-zone -o qr.png
```

### Error correction levels

```bash
# High error correction (H) - for logos or damage resistance
python qr-generator.py "https://example.com" -e H -o qr.png

# Low error correction (L) - smaller QR code
python qr-generator.py "https://example.com" -e L -o qr.png
```

### SVG output

```bash
python qr-generator.py "https://example.com" -F svg -o qr.svg
```

### Add logo to QR

```bash
python qr-generator.py "https://example.com" --logo logo.png -o qr_with_logo.png

# Adjust logo size
python qr-generator.py "https://example.com" --logo logo.png --logo-size 0.15 -o qr.png
```

### Interactive mode

```bash
python qr-generator.py --interactive
```

### Validate QR code

```bash
python qr-generator.py --validate qrcode.png
```

## Arguments

| Argument | Short | Description |
|----------|-------|-------------|
| `text` | - | Text or URL to encode |
| `--file` | `-f` | Read text from file |
| `--output` | `-o` | Output file path |
| `--format` | `-F` | Output format: png or svg |
| `--size` | `-s` | Image size in pixels |
| `--border` | `-b` | Border size in modules |
| `--dark` | `-d` | Dark module color |
| `--light` | `-l` | Light module color |
| `--error` | `-e` | Error correction: L, M, Q, H |
| `--box-size` | - | Box size in pixels |
| `--ascii` | - | Print as ASCII art |
| `--wifi` | - | Generate WiFi QR code |
| `--logo` | - | Add logo to center |
| `--logo-size` | - | Logo size ratio |
| `--no-quiet-zone` | - | Remove quiet zone |
| `--validate` | - | Validate QR code image |
| `--interactive` | `-i` | Interactive mode |

## Error Correction Levels

| Level | Recovery | Use Case |
|-------|----------|----------|
| L | ~7% | Small codes, clean environment |
| M | ~15% | Default, general use |
| Q | ~25% | Industrial, some damage |
| H | ~30% | Logos, heavy damage |

Higher error correction creates larger QR codes but allows for logos or physical damage.

## WiFi QR Format

Format: `SSID:AUTH:PASSWORD`

- **SSID**: Network name
- **AUTH**: Authentication type (WPA, WEP, nopass)
- **PASSWORD**: Network password
- For open networks: `SSID:nopass:`

## Interactive Mode Commands

| Command | Description |
|---------|-------------|
| `:wifi <ssid> <pass>` | Generate WiFi QR |
| `:size <pixels>` | Set image size |
| `:color <dark> <light>` | Set colors |
| `:quit` | Exit mode |

## Examples

### Contact card

```bash
python qr-generator.py "BEGIN:VCARD\nFN:John Doe\nTEL:1234567890\nEND:VCARD" -o contact.png
```

### Email

```bash
python qr-generator.py "mailto:hello@example.com?subject=Hello" -o email.png
```

### Phone number

```bash
python qr-generator.py "tel:+1234567890" -o phone.png
```

### SMS

```bash
python qr-generator.py "smsto:+1234567890:Hello" -o sms.png
```

### Calendar event

```bash
python qr-generator.py "BEGIN:VEVENT\nSUMMARY:Meeting\nDTSTART:20240901T090000\nDTEND:20240901T100000\nEND:VEVENT" -o event.png
```

## Troubleshooting

### Library not found

```bash
pip install qrcode[pil]
```

### Logo not appearing

Increase error correction level to H for more redundancy:
```bash
python qr-generator.py "text" --logo logo.png -e H -o qr.png
```

### QR code not scanning

1. Try increasing the image size
2. Increase error correction level
3. Ensure good contrast between colors
4. Check if logo is too large

## License

MIT License
