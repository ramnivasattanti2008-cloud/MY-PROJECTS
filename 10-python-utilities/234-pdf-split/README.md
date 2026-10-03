# PDF Split Tool

Split PDF files into separate pages, page ranges, or chunks.

## Features

- **Individual Pages**: Extract each page as a separate PDF
- **Page Ranges**: Split by custom page ranges
- **Fixed Chunks**: Split into chunks of N pages
- **Extract**: Pull specific pages into a single output file
- **Info Mode**: View page structure and ranges

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Extract All Pages as Separate Files

```bash
python pdf-split.py input.pdf -o pages/
```

Creates files like: `page_001.pdf`, `page_002.pdf`, etc.

### Extract Specific Pages

```bash
python pdf-split.py input.pdf -o pages/ --pages "1,3,5,7-10"
```

### Split by Page Ranges

```bash
python pdf-split.py input.pdf -o splits/ --ranges "1-5" "6-10" "11-20"
```

### Split into Chunks

```bash
python pdf-split.py input.pdf -o chunks/ --every 10
```

This creates chunks of 10 pages each.

### Extract Pages to Single File

```bash
python pdf-split.py input.pdf -o output.pdf --pages "1-5"
```

### Show Page Information

```bash
python pdf-split.py input.pdf --info
```

## Options

| Option | Description |
|--------|-------------|
| `input` | Input PDF file (required) |
| `-o, --output` | Output directory or file path |
| `--pages` | Pages to extract (e.g., "1,3,5-10" or "all") |
| `--ranges` | Page ranges for splitting |
| `--every` | Split into chunks of N pages |
| `--prefix` | Output file prefix (default: page) |
| `--info` | Show PDF page information |
| `--extract` | Extract pages to single output file |

## Page Range Syntax

- Single page: `5`
- Multiple pages: `1,3,5`
- Range: `1-10`
- Mixed: `1,3,5-10,15`

## Examples

### Extract First and Last Pages

```bash
python pdf-split.py document.pdf -o pages/ --pages "1,-1"
```

### Split Multi-Chapter Book

```bash
python pdf-split.py book.pdf -o chapters/ \
    --ranges "1-10" "11-50" "51-100" "101-150"
```

### Extract Odd/Even Pages

```bash
# Extract odd pages
python pdf-split.py input.pdf -o odd_pages.pdf --pages "1,3,5,7,9,11,13,15"

# Extract even pages
python pdf-split.py input.pdf -o even_pages.pdf --pages "2,4,6,8,10,12,14,16"
```

## Requirements

- Python 3.8+
- PyPDF2 - PDF manipulation library
