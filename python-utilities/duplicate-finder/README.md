# Duplicate Finder

Find duplicate files by content hash and optionally remove them.

## Features

- Fast two-pass algorithm (groups by size first, then hashes)
- SHA256 hash verification for accurate detection
- Filter by file extensions
- Minimum/maximum size filters
- Multiple keep strategies (first, last, smallest, newest)
- Detailed report with wasted space calculations
- Safe deletion with confirmation

## Installation

```bash
pip install -r requirements.txt
# (No external dependencies required)
```

## Usage

### Basic Scan

```bash
python duplicate-finder.py /path/to/scan
```

### Filter by Extension

```bash
# Only scan images
python duplicate-finder.py . --extensions .jpg .png .gif

# Only scan videos
python duplicate-finder.py . --extensions mp4 avi mkv
```

### Filter by Size

```bash
# Only files larger than 1MB
python duplicate-finder.py . --min-size 1048576

# Files between 1MB and 100MB
python duplicate-finder.py . --min-size 1048576 --max-size 104857600
```

### Show File Hashes

```bash
python duplicate-finder.py . --show-hashes
```

### Delete Duplicates

```bash
# Keep the first file found (default)
python duplicate-finder.py . --delete

# Keep the newest file
python duplicate-finder.py . --delete --keep newest

# Keep the smallest filename
python duplicate-finder.py . --delete --keep smallest
```

## How It Works

1. **Size Grouping**: Files are grouped by size first (files with unique sizes can't be duplicates)
2. **Hash Calculation**: Only files with duplicate sizes are hashed
3. **Duplicate Detection**: Files with matching hashes are identified as duplicates
4. **Report**: Shows all duplicate groups with space calculations
5. **Delete**: Removes duplicates based on keep strategy

## Example Output

```
Scanning: /photos
Found 1,234 files in 45 directories
Grouping by size...
Computed 89 hashes

==============================================================
DUPLICATE FILES REPORT
==============================================================
Found 12 groups of duplicates
Total duplicate files: 28
Wasted space: 847.32 MB
==============================================================

[1] Duplicate Group - 3 files
    Size per file: 15.2 MB
    Wasted space: 30.4 MB (66.7%)
    Files:
      1. /photos/vacation/DSC_0001.jpg [KEEP]
      2. /photos/vacation/DSC_0001_copy.jpg
      3. /photos/backups/DSC_0001.jpg

[2] Duplicate Group - 2 files
    Size per file: 8.5 MB
    Wasted space: 8.5 MB (50.0%)
    Files:
      1. /photos/screenshot.png [KEEP]
      2. /photos/Downloads/screenshot.png
```

## Performance

- Uses SHA256 for reliable duplicate detection
- Optimized with size pre-filtering
- Progress indicator for large scans
- Handles permission errors gracefully

## Safety

- Deletion requires explicit `--delete` flag
- Always keeps at least one copy of each file
- Reports errors for inaccessible files
- Shows what will be deleted before action
