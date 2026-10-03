# PDF Watermark Tool

Add text or image watermarks to PDF documents with customizable options.

## Features

- **Text Watermarks**: Add custom text with configurable font size, opacity, rotation, and color
- **Image Watermarks**: Add image overlays with positioning and scaling options
- **Page Selection**: Apply watermarks to specific pages or all pages
- **Batch Processing**: Process single or multiple PDFs

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Text Watermark

```bash
python pdf-watermark.py input.pdf output.pdf -t "CONFIDENTIAL"
```

With custom options:
```bash
python pdf-watermark.py input.pdf output.pdf -t "DRAFT" \
    --font-size 60 \
    --opacity 0.2 \
    --rotation -30 \
    --color FF0000
```

### Image Watermark

```bash
python pdf-watermark.py input.pdf output.pdf -i logo.png
```

With positioning and scaling:
```bash
python pdf-watermark.py input.pdf output.pdf -i logo.png \
    --position top-right \
    --scale 0.5 \
    --opacity 0.3
```

### Specific Pages Only

```bash
python pdf-watermark.py input.pdf output.pdf -t "DRAFT" --pages "1,3,5"
```

## Options

### Text Watermark Options

| Option | Description | Default |
|--------|-------------|---------|
| `-t, --text` | Watermark text | Required |
| `--font-size` | Font size | 40 |
| `--opacity` | Opacity (0.0-1.0) | 0.3 |
| `--rotation` | Rotation angle (degrees) | 45 |
| `--color` | Hex color code | 808080 (gray) |
| `--pages` | Pages to watermark | all |

### Image Watermark Options

| Option | Description | Default |
|--------|-------------|---------|
| `-i, --image` | Image file path | Required |
| `--position` | Position on page | center |
| `--scale` | Scale factor | 1.0 |
| `--opacity` | Opacity (0.0-1.0) | 0.3 |
| `--pages` | Pages to watermark | all |

### Position Options

- `center` - Center of page (default)
- `top` - Top center
- `bottom` - Bottom center
- `top-left` - Top left corner
- `top-right` - Top right corner
- `bottom-left` - Bottom left corner
- `bottom-right` - Bottom right corner

## Requirements

- Python 3.8+
- PyPDF2 - PDF reading/writing
- reportlab - PDF generation and image support
- Pillow - Image processing
