"""
FastAPI File Service - Upload, Download, Metadata, Search
"""

import os
import uuid
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Optional, List

from fastapi import FastAPI, HTTPException, UploadFile, File, Form, Query, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field, ConfigDict
import aiofiles

# Configuration
UPLOAD_DIR = Path("uploads")
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100 MB
ALLOWED_EXTENSIONS = {
    "image": [".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp"],
    "document": [".pdf", ".doc", ".docx", ".txt", ".md"],
    "video": [".mp4", ".webm", ".avi", ".mov"],
    "audio": [".mp3", ".wav", ".ogg", ".flac"],
    "archive": [".zip", ".tar", ".gz", ".rar"],
}

ALLOWED_MIME_TYPES = {
    "image/jpeg", "image/png", "image/gif", "image/webp", "image/bmp",
    "application/pdf",
    "application/msword",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "text/plain", "text/markdown",
    "video/mp4", "video/webm", "video/x-msvideo",
    "audio/mpeg", "audio/wav", "audio/ogg", "audio/flac",
    "application/zip", "application/x-tar", "application/gzip",
}

# In-memory file metadata store (in production, use a database)
file_metadata = {}

# FastAPI App
app = FastAPI(
    title="File Service API",
    description="Upload, download, manage file metadata, and search files",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create upload directory
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# Pydantic Models
class FileMetadata(BaseModel):
    id: str
    original_name: str
    stored_name: str
    file_path: str
    file_size: int
    mime_type: str
    extension: str
    category: str
    hash: Optional[str] = None
    description: Optional[str] = None
    tags: List[str] = []
    downloads: int = 0
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class FileSearchQuery(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    mime_type: Optional[str] = None
    tags: Optional[List[str]] = None
    min_size: Optional[int] = None
    max_size: Optional[int] = None
    from_date: Optional[datetime] = None
    to_date: Optional[datetime] = None

class FileUpdate(BaseModel):
    description: Optional[str] = None
    tags: Optional[List[str]] = None

# Helper functions
def get_file_category(extension: str) -> str:
    extension = extension.lower()
    for category, extensions in ALLOWED_EXTENSIONS.items():
        if extension in extensions:
            return category
    return "other"

def calculate_hash(file_path: Path) -> str:
    hasher = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            hasher.update(chunk)
    return hasher.hexdigest()

def format_file_size(size_bytes: int) -> str:
    for unit in ["B", "KB", "MB", "GB"]:
        if size_bytes < 1024:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.2f} TB"

# ==================== FILE OPERATIONS ====================

@app.post("/files/upload", response_model=FileMetadata, status_code=status.HTTP_201_CREATED)
async def upload_file(
    file: UploadFile = File(...),
    description: Optional[str] = Form(None),
    tags: Optional[str] = Form(None),  # Comma-separated tags
):
    # Validate file size
    file.file.seek(0, 2)
    size = file.file.tell()
    file.file.seek(0)
    if size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File too large. Maximum size is {format_file_size(MAX_FILE_SIZE)}"
        )

    # Validate content type
    if file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"File type '{file.content_type}' not allowed"
        )

    # Generate unique ID and filename
    file_id = str(uuid.uuid4())
    extension = Path(file.filename).suffix.lower()
    stored_name = f"{file_id}{extension}"

    # Save file
    file_path = UPLOAD_DIR / stored_name
    async with aiofiles.open(file_path, "wb") as f:
        content = await file.read()
        await f.write(content)

    # Calculate hash
    file_hash = calculate_hash(file_path)

    # Parse tags
    tag_list = [t.strip() for t in tags.split(",") if t.strip()] if tags else []

    # Store metadata
    metadata = FileMetadata(
        id=file_id,
        original_name=file.filename,
        stored_name=stored_name,
        file_path=str(file_path),
        file_size=size,
        mime_type=file.content_type,
        extension=extension,
        category=get_file_category(extension),
        hash=file_hash,
        description=description,
        tags=tag_list,
        downloads=0,
        created_at=datetime.utcnow()
    )
    file_metadata[file_id] = metadata

    return metadata

@app.get("/files", response_model=List[FileMetadata])
async def list_files(
    category: Optional[str] = Query(None, description="Filter by category"),
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0)
):
    files = list(file_metadata.values())

    if category:
        files = [f for f in files if f.category == category]

    files.sort(key=lambda x: x.created_at, reverse=True)
    return files[offset:offset + limit]

@app.get("/files/search", response_model=List[FileMetadata])
async def search_files(
    q: Optional[str] = Query(None, description="Search in filename"),
    category: Optional[str] = Query(None, description="Filter by category"),
    extension: Optional[str] = Query(None, description="Filter by extension (.pdf, .jpg)"),
    tags: Optional[str] = Query(None, description="Comma-separated tags to filter"),
    min_size: Optional[int] = Query(None, ge=0, description="Minimum file size in bytes"),
    max_size: Optional[int] = Query(None, ge=0, description="Maximum file size in bytes"),
    sort_by: str = Query("created_at", enum=["created_at", "file_size", "downloads", "original_name"]),
    order: str = Query("desc", enum=["asc", "desc"]),
):
    results = list(file_metadata.values())

    # Filter by search query
    if q:
        q_lower = q.lower()
        results = [f for f in results if q_lower in f.original_name.lower()]

    # Filter by category
    if category:
        results = [f for f in results if f.category == category]

    # Filter by extension
    if extension:
        ext = extension if extension.startswith(".") else f".{extension}"
        results = [f for f in results if f.extension.lower() == ext.lower()]

    # Filter by tags
    if tags:
        filter_tags = [t.strip().lower() for t in tags.split(",")]
        results = [f for f in results if any(tag.lower() in f.tags for tag in filter_tags)]

    # Filter by size
    if min_size is not None:
        results = [f for f in results if f.file_size >= min_size]
    if max_size is not None:
        results = [f for f in results if f.file_size <= max_size]

    # Sort
    reverse = order == "desc"
    if sort_by == "file_size":
        results.sort(key=lambda x: x.file_size, reverse=reverse)
    elif sort_by == "downloads":
        results.sort(key=lambda x: x.downloads, reverse=reverse)
    elif sort_by == "original_name":
        results.sort(key=lambda x: x.original_name.lower(), reverse=reverse)
    else:
        results.sort(key=lambda x: x.created_at, reverse=reverse)

    return results

@app.get("/files/{file_id}", response_model=FileMetadata)
async def get_file_metadata(file_id: str):
    if file_id not in file_metadata:
        raise HTTPException(status_code=404, detail="File not found")
    return file_metadata[file_id]

@app.get("/files/{file_id}/download")
async def download_file(file_id: str):
    if file_id not in file_metadata:
        raise HTTPException(status_code=404, detail="File not found")

    metadata = file_metadata[file_id]
    file_path = Path(metadata.file_path)

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found on disk")

    # Increment download count
    metadata.downloads += 1

    return FileResponse(
        path=file_path,
        filename=metadata.original_name,
        media_type=metadata.mime_type
    )

@app.get("/files/{file_id}/stream")
async def stream_file(file_id: str):
    """Stream file for video/audio playback"""
    if file_id not in file_metadata:
        raise HTTPException(status_code=404, detail="File not found")

    metadata = file_metadata[file_id]
    file_path = Path(metadata.file_path)

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found on disk")

    # Increment download count
    metadata.downloads += 1

    async def iterfile():
        async with aiofiles.open(file_path, "rb") as f:
            while chunk := await f.read(65536):  # 64KB chunks
                yield chunk

    return StreamingResponse(
        iterfile(),
        media_type=metadata.mime_type,
        headers={
            "Content-Disposition": f'inline; filename="{metadata.original_name}"',
            "Accept-Ranges": "bytes"
        }
    )

@app.patch("/files/{file_id}", response_model=FileMetadata)
async def update_file_metadata(file_id: str, update: FileUpdate):
    if file_id not in file_metadata:
        raise HTTPException(status_code=404, detail="File not found")

    metadata = file_metadata[file_id]

    if update.description is not None:
        metadata.description = update.description
    if update.tags is not None:
        metadata.tags = update.tags

    return metadata

@app.delete("/files/{file_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_file(file_id: str):
    if file_id not in file_metadata:
        raise HTTPException(status_code=404, detail="File not found")

    metadata = file_metadata[file_id]
    file_path = Path(metadata.file_path)

    # Delete from disk
    if file_path.exists():
        file_path.unlink()

    # Remove from metadata
    del file_metadata[file_id]

# ==================== UTILITY ENDPOINTS ====================

@app.get("/stats")
async def get_stats():
    """Get storage statistics"""
    total_files = len(file_metadata)
    total_size = sum(f.file_size for f in file_metadata.values())
    by_category = {}

    for f in file_metadata.values():
        by_category[f.category] = by_category.get(f.category, 0) + 1

    return {
        "total_files": total_files,
        "total_size": total_size,
        "total_size_formatted": format_file_size(total_size),
        "by_category": by_category,
        "max_file_size": MAX_FILE_SIZE,
        "max_file_size_formatted": format_file_size(MAX_FILE_SIZE)
    }

@app.get("/categories")
async def get_categories():
    """Get available file categories"""
    return [
        {"name": name, "extensions": exts}
        for name, exts in ALLOWED_EXTENSIONS.items()
    ]

@app.post("/files/cleanup", status_code=status.HTTP_200_OK)
async def cleanup_orphaned_files():
    """Remove metadata entries for files that no longer exist on disk"""
    removed = 0
    for file_id in list(file_metadata.keys()):
        file_path = Path(file_metadata[file_id].file_path)
        if not file_path.exists():
            del file_metadata[file_id]
            removed += 1
    return {"removed_entries": removed, "remaining_files": len(file_metadata)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
