# Image Converter

Convert images between formats: JPEG, PNG, WebP, GIF, BMP, TIFF, ICO. Batch conversion supported.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Single File Conversion

```bash
# PNG to JPEG
python image-converter.py -i photo.png -o photo.jpg --format JPEG

# JPEG to WebP
python image-converter.py -i photo.jpg -o photo.webp --format WEBP --quality 80

# Lossless WebP
python image-converter.py -i photo.png -o photo.webp --format WEBP --lossless

# PNG to GIF
python image-converter.py -i animation.png -o animation.gif --format GIF

# Any to BMP
python image-converter.py -i photo.jpg -o photo.bmp --format BMP

# Create ICO (favicon)
python image-converter.py -i logo.png -o favicon.ico --format ICO
```

### Batch Conversion

```bash
# Convert all images in directory to PNG
python image-converter.py -i ./photos -o ./png_output --format PNG --batch

# Convert all to JPEG with quality 85
python image-converter.py -i ./photos -o ./jpeg_output --format JPEG --quality 85 --batch

# Add suffix to converted files
python image-converter.py -i ./photos -o ./output --format WEBP --batch --suffix _converted
```

## Options

| Option | Description |
|--------|-------------|
| `-i, --input` | Input file or directory (required) |
| `-o, --output` | Output file or directory (required) |
| `-f, --format` | Target format: JPEG, PNG, WebP, GIF, BMP, TIFF, ICO (required) |
| `-q, --quality` | Quality for JPEG/WebP 1-100 (default: 95) |
| `--no-optimize` | Disable compression optimization |
| `--lossless` | Lossless compression (WebP only) |
| `--batch` | Enable batch directory processing |
| `--suffix` | Suffix added to output filenames (batch) |

## Format Notes

- **JPEG**: RGB conversion, transparency replaced with white background
- **PNG**: RGBA preserved, compress_level 9 for max optimization
- **WebP**: Supports both lossy (quality) and lossless modes
- **GIF**: Color-quantized to 256 colors
- **ICO**: Auto-resized to max 256x256
- **TIFF**: LZW compression when optimization enabled
- **BMP**: Always RGB output
