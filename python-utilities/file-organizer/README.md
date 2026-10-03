# File Organizer

A Python script that automatically organizes files in a directory by their type into categorized subfolders.

## Features

- Automatically sorts files into appropriate categories:
  - **Images**: jpg, png, gif, svg, webp, etc.
  - **Videos**: mp4, avi, mkv, mov, etc.
  - **Documents**: pdf, doc, docx, xls, txt, etc.
  - **Archives**: zip, rar, 7z, tar, gz, etc.
  - **Audio**: mp3, wav, flac, ogg, etc.
  - **Code**: py, js, html, css, java, etc.
  - **Executables**: exe, msi, dmg, etc.
  - **Others**: Everything else

- Handles duplicate filenames by adding timestamps
- Skips hidden/system files
- Shows progress as files are moved
- Provides a summary of organized files

## Usage

### Basic Usage (organizes Downloads folder)
```bash
python file-organizer.py
```

### Specify a custom directory
```bash
python file-organizer.py /path/to/folder
```

## Requirements

- Python 3.6 or higher
- No external packages required (uses standard library only)

## Example Output

```
==================================================
FILE ORGANIZER
Automatically organize files by type
==================================================

Found 25 files to organize in: C:\Users\Username\Downloads
--------------------------------------------------
  Moved: photo.jpg -> Images/
  Moved: document.pdf -> Documents/
  Moved: video.mp4 -> Videos/
  ...

==================================================
ORGANIZATION SUMMARY
==================================================
  Images: 5 files
  Documents: 8 files
  Videos: 3 files
  Archives: 2 files
  Others: 1 files
--------------------------------------------------
  Total files organized: 19
  Files skipped: 6
==================================================

File organization complete!
```
