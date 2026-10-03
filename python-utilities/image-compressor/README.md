# Image Compressor

Reduce image file sizes with configurable JPEG quality, PNG optimization, and batch processing.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Single Image

```bash
# Compress JPEG at quality 75
python image-compressor.py -i photo.jpg -o photo_small.jpg --quality 75

# Compress PNG with maximum optimization
python image-compressor.py -i image.png -o image_opt.png --png-optimize

# Target a specific file size (500KB)
python image-compressor.py -i photo.jpg -o photo_500kb.jpg --target-kb 500

# Compress and resize if too large
python image-compressor.py -i photo.jpg -o photo_opt.jpg --max-width 1920 --quality 85
```

### Batch Processing

```bash
# Compress all images in a directory
python image-compressor.py -i ./photos -o ./compressed --quality 80 --batch

# Batch with custom naming
python image-compressor.py -i ./photos -o ./compressed --quality 75 --batch --prefix opt_ --suffix _75
```

## Options

| Option | Description |
|--------|-------------|
| `-i, --input` | Input file or directory (required) |
| `-o, --output` | Output file or directory (required) |
| `-q, --quality` | JPEG quality 1-100 (default: 85) |
| `--png-optimize` | Enable max PNG optimization (level 9) |
| `--max-width` | Max width in pixels - resize if larger |
| `--max-height` | Max height in pixels - resize if larger |
| `--target-kb` | Target file size in KB (JPEG, iterative quality search) |
| `--batch` | Enable batch directory processing |
| `--prefix` | Output filename prefix (batch) |
| `--suffix` | Output filename suffix (default: `_compressed`) |

## How Target Size Works

The `--target-kb` option uses iterative binary search to find the JPEG quality that produces a file closest to (but not exceeding) the target size.

## Supported Formats

Input: JPEG, PNG, WebP, BMP, GIF
Output: JPEG, PNG, WebP
