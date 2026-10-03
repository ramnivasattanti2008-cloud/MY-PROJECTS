#!/usr/bin/env python3
"""
File Splitter - Split large files into chunks and merge them back.
Usage:
    Split:  python file-splitter.py split <file> [--chunk-size KB]
    Merge:  python file-splitter.py merge <output_file>
    List:   python file-splitter.py list <folder>
"""

import argparse
import hashlib
import os
import sys
from pathlib import Path
from typing import Optional


CHUNK_EXT = ".chunk"
MANIFEST_FILE = "manifest.json"


def calculate_hash(data: bytes) -> str:
    """Calculate SHA256 hash of data."""
    return hashlib.sha256(data).hexdigest()


def get_file_hash(filepath: Path) -> str:
    """Calculate SHA256 hash of entire file."""
    sha256 = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256.update(chunk)
    return sha256.hexdigest()


def split_file(input_path: Path, chunk_size_kb: int, output_dir: Path) -> dict:
    """
    Split a file into chunks.
    Returns manifest with file info and chunk hashes.
    """
    chunk_size = chunk_size_kb * 1024
    output_dir.mkdir(parents=True, exist_ok=True)

    file_size = input_path.stat().st_size
    original_hash = get_file_hash(input_path)

    chunks = []
    with open(input_path, "rb") as f:
        chunk_index = 0
        while True:
            chunk_data = f.read(chunk_size)
            if not chunk_data:
                break

            chunk_hash = calculate_hash(chunk_data)
            chunk_filename = f"{input_path.stem}.{chunk_index:04d}{CHUNK_EXT}"
            chunk_path = output_dir / chunk_filename

            with open(chunk_path, "wb") as chunk_file:
                chunk_file.write(chunk_data)

            chunks.append({
                "index": chunk_index,
                "filename": chunk_filename,
                "hash": chunk_hash,
                "size": len(chunk_data)
            })

            print(f"  Chunk {chunk_index}: {chunk_filename} ({len(chunk_data):,} bytes)")
            chunk_index += 1

    manifest = {
        "original_filename": input_path.name,
        "original_size": file_size,
        "original_hash": original_hash,
        "chunk_size_kb": chunk_size_kb,
        "total_chunks": chunk_index,
        "chunks": chunks
    }

    manifest_path = output_dir / MANIFEST_FILE
    import json
    with open(manifest_path, "w") as m:
        json.dump(manifest, m, indent=2)

    print(f"\nSplit complete: {chunk_index} chunks created in {output_dir}")
    print(f"Original size: {file_size:,} bytes")
    print(f"Manifest saved: {manifest_path}")

    return manifest


def merge_files(output_path: Path, chunks_dir: Path) -> bool:
    """
    Merge chunks back into original file.
    Verifies hashes before merging.
    """
    manifest_path = chunks_dir / MANIFEST_FILE
    if not manifest_path.exists():
        print(f"Error: Manifest not found in {chunks_dir}")
        return False

    import json
    with open(manifest_path, "r") as m:
        manifest = json.load(m)

    print(f"Merging: {manifest['original_filename']}")
    print(f"Total chunks expected: {manifest['total_chunks']}")

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "wb") as out_file:
        for i, chunk_info in enumerate(manifest["chunks"]):
            chunk_path = chunks_dir / chunk_info["filename"]

            if not chunk_path.exists():
                print(f"Error: Missing chunk {chunk_info['filename']}")
                return False

            with open(chunk_path, "rb") as chunk_file:
                chunk_data = chunk_file.read()

            actual_hash = calculate_hash(chunk_data)
            if actual_hash != chunk_info["hash"]:
                print(f"Error: Hash mismatch for {chunk_info['filename']}")
                print(f"  Expected: {chunk_info['hash']}")
                print(f"  Got:      {actual_hash}")
                return False

            out_file.write(chunk_data)
            print(f"  Merged chunk {i}/{manifest['total_chunks']}")

    merged_hash = get_file_hash(output_path)
    if merged_hash != manifest["original_hash"]:
        print(f"Error: Final hash mismatch!")
        return False

    print(f"\nMerge complete: {output_path}")
    print(f"Size: {output_path.stat().st_size:,} bytes (verified)")
    return True


def list_chunks(chunks_dir: Path) -> None:
    """List all chunk files in a directory."""
    manifest_path = chunks_dir / MANIFEST_FILE

    if manifest_path.exists():
        import json
        with open(manifest_path, "r") as m:
            manifest = json.load(m)
        print(f"Manifest for: {manifest['original_filename']}")
        print(f"Original size: {manifest['original_size']:,} bytes")
        print(f"Chunk size: {manifest['chunk_size_kb']} KB")
        print(f"Total chunks: {manifest['total_chunks']}")
        print(f"Original hash: {manifest['original_hash']}")
        print(f"\nChunks:")
        for chunk in manifest["chunks"]:
            print(f"  {chunk['filename']}: {chunk['size']:,} bytes")

        total = sum(c["size"] for c in manifest["chunks"])
        print(f"\nTotal data: {total:,} bytes")
    else:
        print("No manifest found. Listing .chunk files:")
        for chunk_file in sorted(chunks_dir.glob(f"*{CHUNK_EXT}")):
            print(f"  {chunk_file.name}: {chunk_file.stat().st_size:,} bytes")


def main():
    parser = argparse.ArgumentParser(
        description="Split large files into chunks and merge them back.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Split a file:
    python file-splitter.py split large_file.zip --chunk-size 1024

  Merge chunks:
    python file-splitter.py merge output/restored_file.zip

  List chunk info:
    python file-splitter.py list chunks_folder/
        """
    )

    subparsers = parser.add_subparsers(dest="command", help="Commands")

    split_parser = subparsers.add_parser("split", help="Split a file into chunks")
    split_parser.add_argument("file", type=Path, help="File to split")
    split_parser.add_argument("-o", "--output", type=Path, default=Path("chunks"),
                              help="Output directory (default: chunks)")
    split_parser.add_argument("-s", "--chunk-size", type=int, default=1024,
                              help="Chunk size in KB (default: 1024)")

    merge_parser = subparsers.add_parser("merge", help="Merge chunks back into file")
    merge_parser.add_argument("output", type=Path, help="Output file path")
    merge_parser.add_argument("-i", "--input", type=Path, default=Path("chunks"),
                              help="Directory containing chunks (default: chunks)")

    list_parser = subparsers.add_parser("list", help="List chunks in a directory")
    list_parser.add_argument("directory", type=Path, help="Directory containing chunks")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    if args.command == "split":
        if not args.file.exists():
            print(f"Error: File not found: {args.file}")
            sys.exit(1)
        split_file(args.file, args.chunk_size, args.output)

    elif args.command == "merge":
        if not args.input.exists():
            print(f"Error: Directory not found: {args.input}")
            sys.exit(1)
        if not merge_files(args.output, args.input):
            sys.exit(1)

    elif args.command == "list":
        if not args.directory.exists():
            print(f"Error: Directory not found: {args.directory}")
            sys.exit(1)
        list_chunks(args.directory)


if __name__ == "__main__":
    main()
