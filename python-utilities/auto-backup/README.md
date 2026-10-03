# Auto Backup Tool

A Python script that creates timestamped compressed backups of important folders.

## Features

- Creates compressed zip archives of any folder
- Automatic timestamp naming (backup_FolderName_2024-01-15_14-30-00.zip)
- Configurable compression level (deflate/bzip2/lzma)
- Preserves folder structure in backup
- Shows progress for large folders
- Displays compression statistics
- Option to clean old backups automatically

## Usage

### Basic Backup (saves in same directory as source)
```bash
python auto-backup.py C:\ImportantFiles
```

### Backup to specific location
```bash
python auto-backup.py C:\ImportantFiles D:\Backups
```

## Requirements

- Python 3.6 or higher
- No external packages required (uses standard library only)

## Example Output

```
==================================================
AUTO BACKUP TOOL
Create timestamped compressed backups
==================================================

Backup Details:
  Source: C:\ImportantFiles
  Destination: D:\Backups
  Files to backup: 156
  Compression: Enabled
--------------------------------------------------
  Progress: 100/156 files...
  Progress: 200/156 files...

Backup created successfully!
  Filename: backup_ImportantFiles_2024-01-15_14-30-00.zip
  Files backed up: 156
  Original size: 245.6 MB
  Backup size: 89.3 MB
  Compression ratio: 63.6%

Backup location: D:\Backups\backup_ImportantFiles_2024-01-15_14-30-00.zip

Backup completed successfully!
```

## Tips

- Schedule regular backups using Windows Task Scheduler
- Keep backups on external drives or cloud storage
- Use the cleanup option to manage disk space
