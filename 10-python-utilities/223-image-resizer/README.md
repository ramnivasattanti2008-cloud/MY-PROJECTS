# Image Resizer

Resize images by width, height, or percentage. Supports batch processing of entire directories.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Single Image

```bash
# Resize to 800px width, maintain aspect ratio
python image-resizer.py -i photo.jpg -o photo_800.jpg --width 800

# Resize to exact dimensions (may distort)
python image-resizer.py -i photo.jpg -o photo_800x600.jpg --width 800 --height 600 --no-aspect

# Resize to 50% of original
python image-resizer.py -i photo.jpg -o photo_half.jpg --percentage 50

# Resize to 200% (double size)
python image-resizer.py -i photo.jpg -o photo_double.jpg --percentage 200
```

### Batch Processing

```bash
# Resize all images in a directory
python image-resizer.py -i ./photos -o ./output --width 1024 --batch

# Recursive batch with custom prefix/suffix
python image-resizer.py -i ./photos -o ./output --width 800 --batch -r --prefix thumb_ --suffix _800

# Convert all PNGs to WebP at 50% size
python image-resizer.py -i ./images -o ./webp_output --percentage 50 --batch --format WEBP
```

## Options

| Option | Description |
|--------|-------------|
| `-i, --input` | Input file or directory (required) |
| `-o, --output` | Output file or directory (required) |
| `--width` | Target width in pixels |
| `--height` | Target height in pixels |
| `--percentage` | Resize by percentage (50 = half, 200 = double) |
| `--no-aspect` | Do not maintain aspect ratio |
| `--batch` | Enable batch directory processing |
| `-r, --recursive` | Recurse into subdirectories |
| `--prefix` | Prefix for output filenames (batch) |
| `--suffix` | Suffix for output filenames (default: `_resized`) |
| `--format` | Force output format (JPEG, PNG, WebP, etc.) |

## Supported Formats

JPEG, PNG, WebP, BMP, GIF, TIFF

## Notes

- Aspect ratio is maintained by default using Pillow's `thumbnail()` method
- RGBA images are automatically converted to RGB when saving as JPEG
- Batch mode preserves the original directory structure when using `-r`
