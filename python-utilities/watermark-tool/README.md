# Watermark Tool

Add text or image watermarks to images with full position, opacity, and batch control.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Text Watermark

```bash
# Simple text watermark bottom-right
python watermark-tool.py -i photo.jpg -o photo_wm.jpg --text "My Company"

# Center position, semi-transparent
python watermark-tool.py -i photo.jpg -o photo_wm.jpg --text "DRAFT" \
  --position center --opacity 0.3 --font-size 120

# Custom color and font size
python watermark-tool.py -i photo.jpg -o photo_wm.jpg --text "COPY" \
  --color 255,0,0 --font-size 80 --opacity 0.6

# Tiled watermark (repeating pattern)
python watermark-tool.py -i photo.jpg -o photo_wm.jpg --text "CONFIDENTIAL" \
  --position tile --opacity 0.12 --font-size 28
```

### Image Watermark

```bash
# Logo watermark bottom-right
python watermark-tool.py -i photo.jpg -o photo_wm.jpg \
  --watermark-image logo.png --position bottom-right --opacity 0.4

# Scale watermark (15% of image width)
python watermark-tool.py -i photo.jpg -o photo_wm.jpg \
  --watermark-image logo.png --scale 0.25 --position top-left --opacity 0.3

# Tiled image watermark
python watermark-tool.py -i photo.jpg -o photo_wm.jpg \
  --watermark-image pattern.png --position tile --opacity 0.2
```

### Batch Processing

```bash
# Batch text watermark
python watermark-tool.py -i ./photos -o ./watermarked \
  --text "MyCompany" --position bottom-center --opacity 0.5 --batch

# Batch with custom naming
python watermark-tool.py -i ./photos -o ./watermarked \
  --text "DRAFT" --batch --prefix draft_ --suffix "" --format JPEG
```

## Options

| Option | Description |
|--------|-------------|
| `-i, --input` | Input file or directory (required) |
| `-o, --output` | Output file or directory (required) |
| `--text` | Text watermark content |
| `--watermark-image` | Image file to use as watermark |
| `--position` | Position: top-left, top-center, top-right, center-left, center, center-right, bottom-left, bottom-center, bottom-right, tile, stretch |
| `--opacity` | Opacity 0.0-1.0 (default: 0.5) |
| `--font-size` | Font size in pixels (auto if omitted) |
| `--color` | Text color as R,G,B (e.g. `255,200,0`) |
| `--scale` | Image watermark scale vs image width (default: 0.15) |
| `--margin` | Distance from edges in pixels (default: 20) |
| `--batch` | Enable batch directory processing |
| `--format` | Output format (JPEG, PNG, WebP) |

## Position Modes

- **Corner/Edge**: `top-left`, `top-center`, `top-right`, `center-left`, `center`, `center-right`, `bottom-left`, `bottom-center`, `bottom-right`
- **Tile**: Repeating pattern across entire image
- **Stretch**: Stretched across the bottom of the image

## Notes

- Text watermarks include a shadow for visibility on any background
- Image watermarks work best with PNG files that have alpha channels
- Opacity affects the alpha channel of the watermark
