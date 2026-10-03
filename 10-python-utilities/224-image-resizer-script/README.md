# Image Resizer

A Python CLI tool to resize images to different dimensions with batch processing support.

## Features

- Resize single or multiple images
- Batch processing from directories
- Maintain aspect ratio option
- Scale by percentage
- Custom output quality (JPEG)
- Multiple output formats (JPEG, PNG, WEBP, GIF)
- Custom output naming
- Quiet mode for scripting

## Installation

```bash
pip install -r requirements/image-resizer-requirements.txt
```

## Usage

### Basic resize

```bash
# Resize by width only (maintains aspect ratio)
python image-resizer.py photo.jpg --width 800

# Resize by height only
python image-resizer.py photo.jpg --height 600

# Resize to exact dimensions
python image-resizer.py photo.jpg --width 800 --height 600
```

### Batch processing

```bash
# Resize multiple files
python image-resizer.py img1.jpg img2.jpg img3.png --width 800

# Resize all images in a directory
python image-resizer.py /path/to/images/ --width 800

# Resize with output directory
python image-resizer.py /path/to/images/ --width 800 -o output/
```

### Scale by percentage

```bash
# Reduce to 50%
python image-resizer.py photo.jpg --scale 50

# Double the size
python image-resizer.py photo.jpg --scale 200

# Reduce to 25%
python image-resizer.py photo.jpg --scale 25
```

### Keep aspect ratio

```bash
# Fit within 800x600 while keeping ratio
python image-resizer.py photo.jpg --width 800 --height 600 --keep-ratio

# Resize width, height auto-calculated
python image-resizer.py photo.jpg --width 800 --keep-ratio
```

### Output options

```bash
# Custom output file
python image-resizer.py photo.jpg --width 800 -o resized.jpg

# Custom output directory
python image-resizer.py photo.jpg --width 800 -o output/

# Custom suffix for batch output (default: _resized)
python image-resizer.py photo.jpg --width 800 --suffix "_small"

# Change output format
python image-resizer.py photo.png --width 800 --format JPEG

# JPEG quality
python image-resizer.py photo.jpg --width 800 --quality 85
```

### Options

| Option | Description |
|--------|-------------|
| `inputs` | Image file(s) or directory |
| `--width`, `-w` | Target width in pixels |
| `--height`, `-h` | Target height in pixels |
| `--keep-ratio`, `-k` | Maintain aspect ratio |
| `--scale`, `-s` | Scale by percentage (1-500) |
| `--quality`, `-q` | JPEG quality 1-100 (default: 95) |
| `--output`, `-o` | Output file or directory |
| `--suffix` | Suffix for output files (default: _resized) |
| `--format` | Output format (JPEG, PNG, WEBP, GIF) |
| `--quiet`, `-Q` | Suppress output |

## Supported Formats

| Format | Extensions |
|--------|------------|
| JPEG | .jpg, .jpeg |
| PNG | .png |
| GIF | .gif |
| BMP | .bmp |
| TIFF | .tiff |
| WebP | .webp |

## Example Output

```
Found 3 image(s) to resize
[1/3] Resizing: photo1.jpg
  1920x1080 -> 800x450 -> output/photo1_resized.jpg
[2/3] Resizing: photo2.jpg
  3840x2160 -> 800x450 -> output/photo2_resized.jpg
[3/3] Resizing: photo3.png
  1024x768 -> 800x600 -> output/photo3_resized.png

Completed: 3/3 images resized successfully
```

## Resize Modes

### Exact dimensions (no --keep-ratio)
Image is stretched to exactly match width/height.

### Maintain ratio (--keep-ratio)
Image is scaled to fit within bounding box while maintaining aspect ratio.

### Scale percentage (--scale)
Image is scaled uniformly by percentage.

## Performance

- Uses LANCZOS resampling for high quality
- Efficient memory usage for large images
- Processes images one at a time for batch mode
- Supports processing thousands of images

## Error Handling

Exit codes:
- `0`: All images processed successfully
- `1`: One or more images failed

Errors are displayed for:
- Non-image files
- Corrupted images
- Invalid dimensions
- Permission errors
