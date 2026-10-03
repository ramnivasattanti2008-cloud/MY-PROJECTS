# Folder Sync

Synchronize two folders by copying new and modified files from source to destination.

## Features

- One-way sync (source -> destination)
- Smart change detection (by size and modification time)
- Preview mode (dry run) to see what would be copied
- Delete orphans option (remove files in destination not in source)
- GUI mode with visual progress
- CLI mode for automation and scripts

## Installation

No installation required. Requires Python 3.7+.

```bash
python folder-sync.py
```

## Usage

### GUI Mode (Default)

```bash
python folder-sync.py
```

- Select source and destination folders
- Choose options (delete orphans, preview/execute)
- Preview changes before syncing
- Click "Start Sync" to execute

### CLI Mode

```bash
# Basic sync
folder-sync.py ./source ./destination

# Preview what would be copied
folder-sync.py ./source ./destination --dry-run

# Delete orphaned files in destination
folder-sync.py ./source ./destination --delete

# Quiet mode (minimal output)
folder-sync.py ./source ./destination -q
```

## How It Works

1. Scans the source folder recursively
2. For each file, compares with destination:
   - Copy if file doesn't exist in destination
   - Copy if source file is newer
   - Copy if file size differs
   - Skip if identical
3. Optionally deletes orphaned files in destination

## Options

| Option | Description |
|--------|-------------|
| `--dry-run` | Preview changes without copying |
| `-d, --delete` | Delete files in destination not in source |
| `-q, --quiet` | Suppress verbose output |

## Examples

### Backup to USB Drive

```bash
# Preview what will be backed up
folder-sync.py ./Documents /mnt/usb/backups --dry-run

# Execute backup
folder-sync.py ./Documents /mnt/usb/backups
```

### Mirror a Website Folder

```bash
# Keep public folder in sync with source
folder-sync.py ./src /var/www/public --delete
```

### Automated Nightly Backup

```bash
# Add to crontab for automated backups
0 2 * * * /path/to/folder-sync.py /data /backup --delete -q
```

## Troubleshooting

**GUI doesn't start on Linux?**
```bash
sudo apt install python3-tk
```

**Want to sync both directions?**
This tool does one-way sync only. For two-way sync, consider `unison` or `rsync`.

**Symlinks and special files?**
Currently only regular files are synced. Hidden files (starting with `.`) are included.
