"""
Auto Backup Script
Creates timestamped compressed backups of important folders.

Usage:
    python auto-backup.py <source_folder> [backup_destination]

The script creates a zip archive of the source folder with a timestamp.
"""

import os
import sys
import shutil
import zipfile
from pathlib import Path
from datetime import datetime


def get_timestamp() -> str:
    """
    Generate a timestamp string for backup filenames.

    Returns:
        Formatted timestamp string (YYYY-MM-DD_HH-MM-SS)
    """
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")


def create_backup_name(source_name: str, timestamp: str) -> str:
    """
    Generate a backup filename from source folder name and timestamp.

    Args:
        source_name: Name of the source folder
        timestamp: Timestamp string

    Returns:
        Generated backup filename
    """
    # Clean the source name for use in filename
    clean_name = "".join(c if c.isalnum() or c in "-_" else "_" for c in source_name)
    return f"backup_{clean_name}_{timestamp}.zip"


def backup_folder(source: str, destination: str = None, compression: int = zipfile.ZIP_DEFLATED) -> str:
    """
    Create a compressed backup of a folder.

    Args:
        source: Path to the folder to backup
        destination: Path to backup destination (default: same as source)
        compression: Compression method (ZIP_STORED, ZIP_DEFLATED, ZIP_BZIP2, ZIP_LZMA)

    Returns:
        Path to the created backup file

    Raises:
        FileNotFoundError: If source folder doesn't exist
        ValueError: If source path is not a directory
    """
    source_path = Path(source).resolve()

    # Validate source
    if not source_path.exists():
        raise FileNotFoundError(f"Source folder not found: {source}")
    if not source_path.is_dir():
        raise NotADirectoryError(f"Source is not a directory: {source}")

    # Determine destination
    if destination is None:
        dest_path = source_path.parent
    else:
        dest_path = Path(destination).resolve()
        dest_path.mkdir(parents=True, exist_ok=True)

    # Generate backup filename
    timestamp = get_timestamp()
    backup_name = create_backup_name(source_path.name, timestamp)
    backup_path = dest_path / backup_name

    # Count files for progress
    total_files = sum(1 for _ in source_path.rglob("*") if _.is_file())

    print(f"\nBackup Details:")
    print(f"  Source: {source_path}")
    print(f"  Destination: {dest_path}")
    print(f"  Files to backup: {total_files}")
    print(f"  Compression: {'Enabled' if compression != zipfile.ZIP_STORED else 'Stored (no compression)'}")
    print("-" * 50)

    # Create the backup
    files_backed_up = 0
    total_size = 0

    try:
        with zipfile.ZipFile(backup_path, "w", compression=compression) as zipf:
            for file_path in source_path.rglob("*"):
                if file_path.is_file():
                    # Calculate relative path to preserve folder structure
                    arcname = file_path.relative_to(source_path)

                    # Add file to archive
                    zipf.write(file_path, arcname)

                    files_backed_up += 1
                    total_size += file_path.stat().st_size

                    # Progress indicator for large folders
                    if files_backed_up % 100 == 0:
                        print(f"  Progress: {files_backed_up}/{total_files} files...")

        # Get backup file size
        backup_size = backup_path.stat().st_size

        print(f"\nBackup created successfully!")
        print(f"  Filename: {backup_name}")
        print(f"  Files backed up: {files_backed_up}")
        print(f"  Original size: {_format_size(total_size)}")
        print(f"  Backup size: {_format_size(backup_size)}")
        print(f"  Compression ratio: {100 - (backup_size / total_size * 100):.1f}%")

        return str(backup_path)

    except Exception as e:
        # Clean up partial backup on error
        if backup_path.exists():
            backup_path.unlink()
        raise Exception(f"Backup failed: {str(e)}")


def _format_size(size_bytes: int) -> str:
    """
    Format byte size to human-readable string.

    Args:
        size_bytes: Size in bytes

    Returns:
        Formatted size string (e.g., "1.5 MB")
    """
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} PB"


def clean_old_backups(backup_dir: str, keep_count: int = 5):
    """
    Remove old backups, keeping only the most recent ones.

    Args:
        backup_dir: Directory containing backup files
        keep_count: Number of recent backups to keep
    """
    backup_path = Path(backup_dir)

    if not backup_path.exists():
        return

    # Find all backup zip files
    backups = sorted(
        backup_path.glob("backup_*.zip"),
        key=lambda x: x.stat().st_mtime,
        reverse=True
    )

    # Remove old backups
    removed = 0
    for old_backup in backups[keep_count:]:
        try:
            old_backup.unlink()
            print(f"  Removed old backup: {old_backup.name}")
            removed += 1
        except Exception as e:
            print(f"  Could not remove {old_backup.name}: {e}")

    if removed > 0:
        print(f"\nCleaned up {removed} old backup(s)")


def main():
    """Main function to run the backup script."""
    print("=" * 50)
    print("AUTO BACKUP TOOL")
    print("Create timestamped compressed backups")
    print("=" * 50)

    # Parse command line arguments
    if len(sys.argv) < 2:
        print("\nUsage: python auto-backup.py <source_folder> [backup_destination]")
        print("\nExample:")
        print("  python auto-backup.py C:\\ImportantFiles")
        print("  python auto-backup.py C:\\ImportantFiles D:\\Backups")
        return

    source_folder = sys.argv[1]
    backup_destination = sys.argv[2] if len(sys.argv) > 2 else None

    try:
        # Create backup
        backup_path = backup.create_backup(source_folder, backup_destination)

        print(f"\nBackup location: {backup_path}")
        print("\nBackup completed successfully!")

        # Optionally clean old backups
        if backup_destination:
            print("\n" + "-" * 50)
            response = input("Clean old backups? (keep 5 most recent) [y/N]: ").strip().lower()
            if response == "y":
                clean_old_backups(backup_destination)

    except FileNotFoundError as e:
        print(f"\nError: {e}")
        print("Please verify the source folder exists.")
    except NotADirectoryError as e:
        print(f"\nError: {e}")
    except KeyboardInterrupt:
        print("\n\nBackup cancelled by user.")
    except Exception as e:
        print(f"\nUnexpected error: {e}")


if __name__ == "__main__":
    main()
