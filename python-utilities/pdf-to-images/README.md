# PDF to Images Converter

Convert PDF pages to images with customizable resolution and format.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python pdf-to-images.py input.pdf
python pdf-to-images.py input.pdf -o output_folder
python pdf-to-images.py input.pdf --dpi 300 --format png
python pdf-to-images.py input.pdf --pages 1-5
```

## Options

| Flag | Description | Default |
|------|-------------|---------|
| `-o, --output` | Output directory | `<input>_images/` |
| `--dpi` | Image resolution | 150 |
| `--format` | Image format (png/jpg/webp) | png |
| `--pages` | Page range (e.g., 1-5) | All pages |
| `--engine` | Conversion engine (auto/pymupdf/pdf2image) | auto |

## Requirements

- **PyMuPDF**: Fast, pure Python (recommended)
- **pdf2image**: Alternative, requires poppler-utils on system

## Examples

```bash
# High resolution PNG for printing
python pdf-to-images.py doc.pdf --dpi 300 --format png

# First 10 pages as JPEG
python pdf-to-images.py doc.pdf --pages 1-10 --format jpg

# Use specific engine
python pdf-to-images.py doc.pdf --engine pdf2image
```
