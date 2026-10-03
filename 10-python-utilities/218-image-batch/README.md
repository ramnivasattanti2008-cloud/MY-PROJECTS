# Image Batch Processor

Batch resize, crop, compress, and transform multiple images with a single command.

## Features

- **Resize**: By dimensions or scale factor
- **Crop**: To specific dimensions with position control
- **Transform**: Rotate, flip horizontal/vertical
- **Effects**: Grayscale, blur, brightness, contrast
- **Batch**: Process entire folders recursively
- **GUI Mode**: Visual interface with live preview of operations

## Installation

```bash
pip install Pillow
```

## Usage

### GUI Mode (Recommended)

```bash
python image-batch.py
```

Launch the graphical interface to visually configure all operations.

### CLI Mode

```bash
# Resize all images to 800x600
image-batch.py ./photos -o ./output --width 800 --height 600

# Convert to grayscale with 50% scale
image-batch.py ./photos -o ./output --scale 0.5 --grayscale

# Rotate 90 degrees and blur
image-batch.py ./photos -o ./output --rotate 90 --blur 2

# Crop to 16:9 aspect ratio
image-batch.py ./photos -o ./output --crop-w 1920 --crop-h 1080
```

## Operations

| Operation | CLI Flag | Description |
|-----------|----------|-------------|
| Resize (dimensions) | `--width N --height N` | Resize to exact dimensions |
| Resize (scale) | `--scale N` | Scale by factor (0.5 = 50%) |
| Crop | `--crop-w N --crop-h N` | Crop to specific dimensions |
| Rotate | `--rotate N` | Rotate by degrees |
| Flip H | `--flip-h` | Mirror horizontally |
| Flip V | `--flip-v` | Mirror vertically |
| Grayscale | `--grayscale` | Convert to B&W |
| Blur | `--blur N` | Gaussian blur radius |
| Brightness | `--brightness N` | Brightness factor (1.0 = normal) |
| Contrast | `--contrast N` | Contrast factor (1.0 = normal) |

## Output Options

| Option | CLI Flag | Description |
|--------|----------|-------------|
| Output folder | `-o, --output DIR` | Save to different folder |
| Filename prefix | `--prefix TEXT` | Add prefix to filenames |
| Filename suffix | `--suffix TEXT` | Add suffix (default: _processed) |
| JPEG quality | `-q, --quality N` | Quality 1-100 (default: 85) |
| Overwrite | `--overwrite` | Replace original files |
| Recursive | `-r, --recursive` | Process subfolders |

## Examples

### Website Thumbnails

```bash
image-batch.py ./photos -o ./thumbnails --width 300 --height 200 --quality 70
```

### Social Media Prep

```bash
image-batch.py ./raw -o ./instagram --width 1080 --height 1080 --contrast 1.2
```

### Document Scanning

```bash
image-batch.py ./scans -o ./cleaned --grayscale --contrast 1.3 --sharpen
```

### Archive old photos

```bash
image-batch.py ./old_photos -o ./archived --scale 0.25 --grayscale --quality 60
```

## Supported Formats

- JPEG (.jpg, .jpeg)
- PNG (.png)
- GIF (.gif)
- BMP (.bmp)
- WebP (.webp)
- TIFF (.tiff)

## Troubleshooting

**"Pillow library required" error?**
```bash
pip install Pillow
```

**Out of memory with large images?**
Process in smaller batches or use the `--recursive` flag to limit scope.

**Images are too large?**
Use `--quality 70` or lower for JPEG compression.
