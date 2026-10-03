# Disk Usage Analyzer

Analyze disk usage and visualize largest files and folders with bar charts.

## Features

- Recursive directory scanning
- Visual bar charts of largest items
- Directory tree view
- File type breakdown by extension
- Human-readable sizes (B, KB, MB, GB, TB)
- Symlink-safe scanning
- Permission error handling

## Installation

```bash
pip install -r requirements.txt
# (No external dependencies required)
```

## Usage

### Basic Analysis

```bash
python disk-usage.py
python disk-usage.py /path/to/directory
```

### Show More Items

```bash
python disk-usage.py . -n 50
```

### Directory Tree View

```bash
python disk-usage.py . --tree
python disk-usage.py /home -d 5  # Max depth 5
```

### File Type Breakdown

```bash
python disk-usage.py . --extensions
```

### Without Chart

```bash
python disk-usage.py . --no-chart
```

## Example Output

### Summary View

```
Analyzing: /photos
Scanning...
================================================================================
SUMMARY
================================================================================
Directory:     /photos
Total size:    45.67 GB
Files:         12,847
Directories:   456
================================================================================

LARGEST ITEMS
--------------------------------------------------------------------------------
     4.52 GB  DIR      /photos/vacation/2024
     3.21 GB  DIR      /photos/backups
     2.87 GB  FILE     /photos/video/concert.mp4
     ...
```

### Bar Chart

```
================================================================================
DISK USAGE BAR CHART
================================================================================
     4.52 GB  [D] ██████████████████████████████████████████████ /photos/vacation/2024
     3.21 GB  [D] ███████████████████████████████ /photos/backups
     2.87 GB  [F] █████████████████████████ /photos/video/concert.mp4
```

### Tree View

```
================================================================================
DIRECTORY TREE
================================================================================
/photos  45.67 GB
  +-- vacation  8.45 GB
    +-- 2023  3.93 GB
    +-- 2024  4.52 GB
  +-- backups  3.21 GB
  +-- video  12.87 GB
    +-- raw  10.00 GB
    +-- edited  2.87 GB
```

### Extension Breakdown

```
================================================================================
BREAKDOWN BY FILE TYPE
================================================================================
    12.45 GB  .mp4               ████████████████████████████████
     8.32 GB  .jpg               █████████████████████
     5.67 GB  .raw               ███████████████
     3.21 GB  .png               █████████
```

## Visual Elements

- `[D]` indicates a directory
- `[F]` indicates a file
- `█` blocks represent relative size
- `▓` blocks used in tree view
- `+--` prefix for directory entries in tree

## Performance

- Handles large directories efficiently
- Symlinks are skipped to avoid loops
- Permission errors are logged but don't stop scan
- Progress updates for large scans
