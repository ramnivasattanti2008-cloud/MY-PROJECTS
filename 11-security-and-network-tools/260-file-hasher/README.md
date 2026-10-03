# File Hasher

Calculate cryptographic hashes (MD5, SHA1, SHA256, SHA512) for any file.

## Features

- Calculate multiple hash types for any file
- GUI mode with drag & drop support
- CLI mode for scripting and automation
- Verify files against known hashes
- Copy all hashes to clipboard (GUI)
- Human-readable file sizes

## Installation

No installation required. Requires Python 3.7+.

```bash
# Just run directly
python file-hasher.py
```

## Usage

### GUI Mode (Default when no arguments)

```bash
python file-hasher.py
```

- Drag and drop files onto the window
- Click "Browse Files" to select files
- Click "Copy All" to copy hashes to clipboard

### CLI Mode

```bash
# Hash single file (default SHA256)
python file-hasher.py document.pdf

# Hash multiple files
python file-hasher.py file1.txt file2.pdf image.jpg

# Use specific algorithm
python file-hasher.py -a md5 document.pdf

# Show all hash types
python file-hasher.py -v document.pdf

# Verify against known hash
python file-hasher.py --verify 5d41402abc4b2a76b9719d911017c592 document.pdf
python file-hasher.py --verify abc123 -a sha1 document.pdf
```

## Hash Algorithms

| Algorithm | Length | Use Case |
|-----------|--------|----------|
| MD5 | 32 chars | Legacy checksums (not secure) |
| SHA1 | 40 chars | Git commits, legacy systems |
| SHA256 | 64 chars | Default, recommended for most uses |
| SHA512 | 128 chars | High-security applications |

## Examples

### Verify Download Integrity

```bash
# Download a file, then verify its hash
python file-hasher.py -a sha256 downloaded_file.zip

# Compare with the published hash
python file-hasher.py --verify PUBLISHED_HASH_HERE downloaded_file.zip
```

### Batch Processing

```bash
# Hash all files in a directory
for f in *.iso; do python file-hasher.py -a sha256 "$f"; done
```

## Troubleshooting

**GUI doesn't start on Linux?**
```bash
sudo apt install python3-tk
```

**Need faster hashing for large files?**
The tool uses 64KB chunks for memory efficiency while maintaining speed. This is optimal for most use cases.
