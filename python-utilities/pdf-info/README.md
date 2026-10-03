# PDF Info Tool

Extract metadata and information from PDF files including page count, title, author, and more.

## Features

- **Metadata Extraction**: Title, author, subject, keywords, creation date, etc.
- **Page Information**: Page count and dimensions
- **Encryption Status**: Check if PDF is password protected
- **Text Extraction**: Extract text content from pages
- **Image Extraction**: Pull images from PDF pages
- **PDF Comparison**: Compare multiple PDFs side by side
- **Directory Listing**: List all PDFs in a folder
- **JSON Output**: Machine-readable output format

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Get PDF Information

```bash
python pdf-info.py document.pdf
```

### Verbose Output

```bash
python pdf-info.py document.pdf -v
```

### JSON Output

```bash
python pdf-info.py document.pdf --json
```

### Extract Text

```bash
python pdf-info.py document.pdf --text
```

Extract from specific pages:
```bash
python pdf-info.py document.pdf --text --pages "1-3,5"
```

### Extract Images

```bash
python pdf-info.py document.pdf --extract-images -o images/
```

### Compare PDFs

```bash
python pdf-info.py file1.pdf file2.pdf file3.pdf --compare
```

### List PDFs in Directory

```bash
python pdf-info.py -l ./documents
```

Recursive search:
```bash
python pdf-info.py -l ./documents -r
```

## Options

| Option | Description |
|--------|-------------|
| `input` | Input PDF file path |
| `-v, --verbose` | Verbose output with page details |
| `--json` | Output in JSON format |
| `-t, --text` | Extract text content |
| `--pages` | Pages to extract (e.g., "1,3,5-10") |
| `-i, --extract-images` | Extract images from PDF |
| `-o, --output-dir` | Output directory |
| `--compare` | Compare multiple PDFs |
| `-l, --list-dir` | List PDFs in directory |
| `-r, --recursive` | Recursive search |

## Metadata Fields

The tool extracts these metadata fields when available:

| Field | Description |
|-------|-------------|
| Title | Document title |
| Author | Document author |
| Subject | Document subject |
| Keywords | Document keywords |
| Creator | Application that created the PDF |
| Producer | Application that produced the PDF |
| CreationDate | When the PDF was created |
| ModDate | When the PDF was last modified |

## Examples

### Batch Information Extraction

```bash
for file in *.pdf; do
    echo "=== $file ==="
    python pdf-info.py "$file" --json
done
```

### Find Largest PDFs

```bash
python pdf-info.py -l . | sort -k3 -h
```

### Check for Encrypted PDFs

```bash
python pdf-info.py -l ./documents -r | grep "Yes"
```

## Requirements

- Python 3.8+
- PyPDF2 - PDF manipulation library
- Pillow - Image processing (for image extraction)
