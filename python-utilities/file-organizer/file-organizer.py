"""
File Organizer Script
Automatically organizes files in a directory by their type into categorized subfolders.

Usage:
    python file-organizer.py [source_directory]

If no directory is specified, defaults to user's Downloads folder.
"""

import os
import shutil
from pathlib import Path
from datetime import datetime


# Define file type categories and their extensions
FILE_CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp", ".ico", ".tiff", ".raw"],
    "Videos": [".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv", ".webm", ".m4v"],
    "Documents": [".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".txt", ".rtf", ".odt", ".csv"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz"],
    "Audio": [".mp3", ".wav", ".flac", ".aac", ".ogg", ".wma", ".m4a"],
    "Code": [".py", ".js", ".html", ".css", ".java", ".cpp", ".c", ".h", ".cs", ".php", ".rb", ".go", ".rs"],
    "Executables": [".exe", ".msi", ".dmg", ".app", ".deb", ".rpm"],
}


def get_file_category(file_extension: str) -> str:
    """
    Determine the category for a given file extension.

    Args:
        file_extension: The file extension to categorize

    Returns:
        The category name, or "Others" if no match found
    """
    extension = file_extension.lower()
    for category, extensions in FILE_CATEGORIES.items():
        if extension in extensions:
            return category
    return "Others"


def create_category_folders(base_path: Path) -> dict:
    """
    Create category subfolders if they don't exist.

    Args:
        base_path: The base directory path

    Returns:
        Dictionary mapping category names to their paths
    """
    folders = {}
    for category in FILE_CATEGORIES.keys():
        folder_path = base_path / category
        folder_path.mkdir(exist_ok=True)
        folders[category] = folder_path
    # Also create Others folder
    others_path = base_path / "Others"
    others_path.mkdir(exist_ok=True)
    folders["Others"] = others_path
    return folders


def organize_files(source_dir: str) -> dict:
    """
    Organize files in the source directory by type.

    Args:
        source_dir: Path to the directory to organize

    Returns:
        Dictionary with counts of moved files per category
    """
    source_path = Path(source_dir)

    # Validate source directory
    if not source_path.exists():
        raise FileNotFoundError(f"Directory not found: {source_dir}")
    if not source_path.is_dir():
        raise NotADirectoryError(f"Path is not a directory: {source_dir}")

    # Create category folders
    category_folders = create_category_folders(source_path)

    # Track results
    results = {category: 0 for category in FILE_CATEGORIES.keys()}
    results["Others"] = 0
    results["Skipped"] = 0

    # Get list of files to process
    files = [f for f in source_path.iterdir() if f.is_file()]

    print(f"\nFound {len(files)} files to organize in: {source_path}")
    print("-" * 50)

    for file_path in files:
        try:
            # Get file extension
            extension = file_path.suffix

            # Skip if no extension (likely system/hidden files)
            if not extension:
                results["Skipped"] += 1
                continue

            # Determine category
            category = get_file_category(extension)

            # Destination path
            dest_path = category_folders[category] / file_path.name

            # Handle duplicate filenames
            if dest_path.exists():
                # Add timestamp to filename
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                new_name = f"{file_path.stem}_{timestamp}{file_path.suffix}"
                dest_path = category_folders[category] / new_name
                print(f"  Renamed: {file_path.name} -> {new_name}")

            # Move the file
            shutil.move(str(file_path), str(dest_path))
            results[category] += 1
            print(f"  Moved: {file_path.name} -> {category}/")

        except PermissionError:
            print(f"  Skipped (permission denied): {file_path.name}")
            results["Skipped"] += 1
        except Exception as e:
            print(f"  Error moving {file_path.name}: {str(e)}")
            results["Skipped"] += 1

    return results


def print_summary(results: dict):
    """
    Print a summary of the organization results.

    Args:
        results: Dictionary with file counts per category
    """
    print("\n" + "=" * 50)
    print("ORGANIZATION SUMMARY")
    print("=" * 50)

    total_moved = sum(v for k, v in results.items() if k != "Skipped")

    for category, count in results.items():
        if count > 0:
            print(f"  {category}: {count} files")

    print("-" * 50)
    print(f"  Total files organized: {total_moved}")
    print(f"  Files skipped: {results['Skipped']}")
    print("=" * 50)


def main():
    """Main function to run the file organizer."""
    print("=" * 50)
    print("FILE ORGANIZER")
    print("Automatically organize files by type")
    print("=" * 50)

    # Default to Downloads folder
    default_downloads = Path.home() / "Downloads"

    # Allow command line argument for source directory
    import sys
    source_dir = sys.argv[1] if len(sys.argv) > 1 else str(default_downloads)

    # Validate directory
    if not os.path.exists(source_dir):
        print(f"\nError: Directory not found: {source_dir}")
        print(f"Please provide a valid directory path.")
        return

    try:
        # Run organization
        results = organize_files(source_dir)

        # Print summary
        print_summary(results)

        print("\nFile organization complete!")

    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
    except Exception as e:
        print(f"\nError: {str(e)}")


if __name__ == "__main__":
    main()
