# PDF Merger Tool

Merge multiple PDF files into one with support for drag & drop and CLI usage.

## Features

- **Interactive Mode**: User-friendly menu for selecting files
- **CLI Mode**: Quick command-line merging
- **Drag & Drop**: Simply pass files as arguments
- **Directory Mode**: Merge all PDFs in a folder
- **Natural Sorting**: Intelligent file ordering (file1, file2, file10 instead of file1, file10, file2)
- **Reversal Option**: Merge files in reverse order

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Interactive Mode

```bash
python pdf-merger.py
```

Navigate the menu to:
- Add individual PDF files
- Add all PDFs from a directory
- View/manage file list
- Merge and save

### Command Line Mode

```bash
# Merge specific files
python pdf-merger.py file1.pdf file2.pdf file3.pdf -o merged.pdf

# Merge all PDFs from a directory
python pdf-merger.py -d ./documents/ -o output.pdf

# With natural sorting (recommended for numbered files)
python pdf-merger.py -d ./chapters/ -o book.pdf --sort

# Reverse order
python pdf-merger.py *.pdf -o reversed.pdf --reverse
```

### Drag & Drop Support

On Windows, you can drag PDF files onto the script or use quoted wildcards:

```bash
python pdf-merger.py "report*.pdf" "appendix*.pdf" -o final.pdf
```

## Command Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `files` | PDF files to merge | - |
| `-d, --directory` | Directory containing PDFs | - |
| `-o, --output` | Output filename | `merged.pdf` |
| `-s, --sort` | Natural sort before merging | False |
| `-i, --interactive` | Force interactive mode | False |
| `--reverse` | Reverse file order | False |

## Programmatic Usage

```python
from pdf_merger import PDFMerger

merger = PDFMerger()

# Method 1: Add files individually
merger.add_pdf('file1.pdf')
merger.add_pdf('file2.pdf')
merger.add_pdf('file3.pdf')
merger.merge('output.pdf')

# Method 2: Add all from directory
merger.add_pdfs_from_directory('./pdfs/')
merger.merge('output.pdf')

# Method 3: Direct merge
merger.merge_files(['file1.pdf', 'file2.pdf'], 'output.pdf')
```

## Natural Sorting

Natural sorting handles numbered filenames correctly:

| Standard Sort | Natural Sort |
|--------------|--------------|
| file1.pdf | file1.pdf |
| file10.pdf | file2.pdf |
| file2.pdf | file10.pdf |
| file3.pdf | file3.pdf |

This is especially useful when merging chapters or sections of a document.

## Tips

- Use `--sort` when merging numbered documents to ensure correct order
- Specify full paths if files are in different directories
- The tool preserves PDF bookmarks when possible
- Large PDFs may take a moment to merge
