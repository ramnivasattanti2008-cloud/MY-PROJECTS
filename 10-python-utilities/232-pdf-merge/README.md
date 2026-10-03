# PDF Merge Tool

Merge multiple PDF files into a single PDF document with optional bookmarks.

## Features

- **Multiple Input Methods**: Specify files directly or use a file list
- **Bookmarks**: Add named bookmarks for each merged PDF
- **Preview Mode**: Preview files before merging
- **Verbose Output**: Detailed progress information
- **Error Handling**: Gracefully skip missing or corrupted files

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Basic Merge

```bash
python pdf-merge.py file1.pdf file2.pdf file3.pdf -o merged.pdf
```

### Using a File List

Create a text file (`files.txt`):
```
# PDF Files to merge
file1.pdf
file2.pdf
file3.pdf
subfolder/file4.pdf
```

Run:
```bash
python pdf-merge.py -l files.txt -o merged.pdf
```

### Merge with Bookmarks

```bash
python pdf-merge.py cover.pdf content.pdf appendix.pdf \
    -o complete.pdf \
    -b "Cover Page" "Main Content" "Appendix"
```

### Preview Before Merging

```bash
python pdf-merge.py file1.pdf file2.pdf file3.pdf --preview
```

### Verbose Mode

```bash
python pdf-merge.py file1.pdf file2.pdf -o merged.pdf -v
```

## Options

| Option | Description |
|--------|-------------|
| `files` | Input PDF files (positional arguments) |
| `-o, --output` | Output PDF file (required) |
| `-l, --list` | Text file with list of PDFs (one per line) |
| `-b, --bookmarks` | Bookmark titles for each PDF |
| `-v, --verbose` | Show detailed progress |
| `--preview` | Preview files without merging |

## Examples

### Merging All PDFs in a Folder

```bash
# PowerShell
Get-ChildItem *.pdf | ForEach-Object { $_.FullName } > files.txt
python pdf-merge.py -l files.txt -o all_merged.pdf
```

### Creating a Bookmarked Document

```bash
python pdf-merge.py title.pdf chapter1.pdf chapter2.pdf \
    -o book.pdf \
    -b "Title" "Chapter 1" "Chapter 2"
```

## Requirements

- Python 3.8+
- PyPDF2 - PDF manipulation library
