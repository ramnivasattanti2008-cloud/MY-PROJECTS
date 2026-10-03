# File Splitter

Split large files into manageable chunks and merge them back with verification.

## Features

- Split any file into chunks of specified size
- SHA256 hash verification for all chunks
- Manifest file tracks all chunks and original file info
- Merge chunks with automatic integrity verification
- List chunk information

## Installation

```bash
pip install -r requirements.txt
# (No external dependencies required)
```

## Usage

### Split a File

```bash
python file-splitter.py split large_file.zip --chunk-size 1024 -o chunks/
```

Options:
- `--chunk-size`: Chunk size in KB (default: 1024)
- `-o, --output`: Output directory (default: chunks/)

### Merge Chunks

```bash
python file-splitter.py merge restored_file.zip -i chunks/
```

Options:
- `-i, --input`: Directory containing chunks (default: chunks/)

### List Chunks

```bash
python file-splitter.py list chunks/
```

## How It Works

1. **Split Mode**: Reads the file in chunks, writes each to disk with hash verification
2. **Manifest**: Stores original filename, size, hash, and chunk metadata
3. **Merge Mode**: Reads chunks in order, verifies each hash, writes to output file
4. **Verification**: Final output hash is compared against original

## Example

```bash
# Split a large video file
$ python file-splitter.py split movie.mp4 --chunk-size 5120 -o video_chunks/
Chunk 0: movie.0000.chunk (5,242,880 bytes)
Chunk 1: movie.0001.chunk (5,242,880 bytes)
...
Split complete: 247 chunks created in video_chunks/

# Merge it back
$ python file-splitter.py merge restored_movie.mp4 -i video_chunks/
Merged chunk 0/247
...
Merge complete: restored_movie.mp4
Size: 1,293,487,104 bytes (verified)
```

## File Structure

```
video_chunks/
  manifest.json      # Metadata and chunk info
  movie.0000.chunk   # First chunk
  movie.0001.chunk   # Second chunk
  ...
```
