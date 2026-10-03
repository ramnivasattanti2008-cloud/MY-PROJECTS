# PDF to Text Extractor

A Python CLI tool to extract text content from PDF files with support for tables and metadata.

## Features

- Extract text from single or multiple PDF files
- Batch processing from directory
- Extract specific page ranges
- Extract tables as TSV format
- Show PDF metadata (title, author, etc.)
- Save output to file or stdout
- Supports both pdfplumber for better accuracy

## Installation

```bash
pip install -r requirements/pdf-to-text-requirements.txt
```

## Usage

### Basic usage

```bash
# Extract all text from a PDF
python pdf-to-text.py document.pdf

# Save output to file
python pdf-to-text.py document.pdf -o output.txt
```

### Multiple files

```bash
# Process multiple PDFs
python pdf-to-text.py file1.pdf file2.pdf file3.pdf

# Process all PDFs in a directory
python pdf-to-text.py /path/to/pdfs/
```

### Page range

```bash
# Extract specific pages
python pdf-to-text.py document.pdf --pages 1-5

# Extract single page
python pdf-to-text.py document.pdf --pages 3

# Extract multiple page ranges
python pdf-to-text.py document.pdf --pages 1,3,5
```

### Metadata only

```bash
# Show PDF metadata
python pdf-to-text.py document.pdf --metadata
```

### Extract tables

```bash
# Extract text and tables
python pdf-to-text.py document.pdf --tables -o output.txt
```

### Options

| Option | Description |
|--------|-------------|
| `files` | PDF file(s) or directory |
| `--output`, `-o` | Output file path |
| `--pages`, `-p` | Page range (e.g., '1-5', '3', '1,3,5') |
| `--metadata`, `-m` | Show PDF metadata only |
| `--tables`, `-t` | Extract tables along with text |
| `--silent` | Suppress progress messages |

## Example Output

### Text Extraction

```
--- Page 1 ---
This is the first page of the document.
It contains some text content.

--- Page 2 ---
This is the second page.
More text here.
```

### Metadata Output

```
  PDF Information: document.pdf
  ───────────────────────────────────────────────────
  Pages:          42
  Size:           2.3 MB

  Metadata
  ───────────────────────────────────────────────────
  Title:         Project Report 2024
  Author:        John Doe
  Subject:       Annual Review
  Creator:       Microsoft Word
  Producer:      Adobe PDF Library
  Created:       D:20240115103000
```

### Table Extraction

```
--- Page 5 ---
Regular text content on the page.

--- Page 5, Table 1 ---
Name    Age     City
John    30      New York
Jane    25      London
```

## Error Handling

The tool will report errors for:
- Files that are not valid PDFs
- Password-protected PDFs
- Corrupted or unreadable files
- Non-existent files

Exit code is 0 for success, 1 if any errors occurred.

## Performance

- Large PDFs are processed page by page
- Memory efficient for very large documents
- Tables may require additional processing time
