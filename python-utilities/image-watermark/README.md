# Image Watermark Tool

Add text or image watermarks to images with customizable position control.

## Features

- **Text Watermarks**: Add custom text with configurable font size and color
- **Image Watermarks**: Overlay a logo or another image as watermark
- **9 Position Options**: Precise placement control (corners, edges, center)
- **Opacity Control**: Adjust watermark transparency (0-255)
- **Batch Processing**: Apply watermarks to entire directories
- **Multiple Formats**: Supports PNG, JPG, JPEG, BMP, WebP, TIFF

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Single Image - Text Watermark

```bash
python image-watermark.py -i photo.jpg -o watermarked.jpg -t "Copyright 2024"
```

### Single Image - Image Watermark (Logo)

```bash
python image-watermark.py -i photo.jpg -o watermarked.jpg -w logo.png -p center
```

### Position Options

| Position | Description |
|----------|-------------|
| `top-left` | Top left corner |
| `top-center` | Top center |
| `top-right` | Top right corner |
| `center-left` | Left middle |
| `center` | Dead center |
| `center-right` | Right middle |
| `bottom-left` | Bottom left corner |
| `bottom-center` | Bottom center |
| `bottom-right` | Bottom right corner |

### Advanced Options

```bash
# Custom font size
python image-watermark.py -i photo.jpg -o out.jpg -t "DRAFT" --font-size 72

# Custom color (RGB)
python image-watermark.py -i photo.jpg -o out.jpg -t "CONFIDENTIAL" --color 255,0,0

# Adjust opacity (0-255, lower = more transparent)
python image-watermark.py -i photo.jpg -o out.jpg -t "COPY" --opacity 80

# Image watermark scale
python image-watermark.py -i photo.jpg -o out.jpg -w logo.png --scale 0.15
```

### Batch Processing

```bash
# Process entire directory
python image-watermark.py -i ./photos/ -o ./output/ -t "Watermark" -p bottom-right
```

## Command Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `-i, --input` | Input image file or directory | Required |
| `-o, --output` | Output file or directory | Required |
| `-t, --text` | Text for watermark | - |
| `-w, --watermark` | Image file for watermark | - |
| `-p, --position` | Position (see table above) | `bottom-right` |
| `--font-size` | Font size for text | `36` |
| `--color` | Text color (R,G,B) | `255,255,255` |
| `--opacity` | Opacity 0-255 | `128` |
| `--scale` | Image watermark scale | `0.2` |

## Programmatic Usage

```python
from image-watermark import WatermarkTool

tool = WatermarkTool()

# Text watermark
tool.add_text_watermark(
    'input.jpg', 'output.jpg',
    text='Copyright 2024',
    position='bottom-right',
    font_size=48,
    opacity=100
)

# Image watermark
tool.add_image_watermark(
    'input.jpg', 'logo.png', 'output.jpg',
    position='center',
    scale=0.15,
    opacity=150
)

# Batch processing
results = tool.batch_watermark(
    './photos/', './output/',
    text='Watermark',
    position='bottom-right'
)
```

## Notes

- Either `--text` or `--watermark` must be specified (not both required, but one is needed)
- For batch processing, output must be a directory
- Higher opacity values mean less transparent watermarks
- Image watermark scale is relative to the main image width
