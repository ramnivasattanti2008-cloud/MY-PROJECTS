# FastAPI File Service

A comprehensive file upload/download service built with FastAPI, featuring metadata management, search, and categorization.

## Features

- File upload with validation
- File download with download counter
- Streaming for video/audio playback
- File metadata management
- Advanced search with multiple filters
- File categorization by type
- Tags and descriptions
- Storage statistics
- Cleanup utilities
- Auto-generated API documentation at `/docs`

## Installation

```bash
cd fastapi-file
pip install -r requirements.txt
```

## Running the API

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### File Upload

```bash
# Upload a file
curl -X POST "http://localhost:8000/files/upload" \
  -F "file=@/path/to/file.pdf" \
  -F "description=Important document" \
  -F "tags=important,work,2024"

# Upload with just the file
curl -X POST "http://localhost:8000/files/upload" \
  -F "file=@/path/to/image.jpg"
```

### File Listing & Search

```bash
# List all files
curl http://localhost:8000/files

# List files with pagination
curl "http://localhost:8000/files?limit=10&offset=0"

# List files by category
curl "http://localhost:8000/files?category=image"

# Search files by name
curl "http://localhost:8000/files/search?q=report"

# Advanced search
curl "http://localhost:8000/files/search?category=document&extension=.pdf&min_size=1000&max_size=5000000"

# Search by tags
curl "http://localhost:8000/files/search?tags=important,work"

# Search with sorting
curl "http://localhost:8000/files/search?sort_by=downloads&order=desc"
```

### File Operations

```bash
# Get file metadata
curl http://localhost:8000/files/{file_id}

# Download file
curl -O "http://localhost:8000/files/{file_id}/download"

# Stream file (for video/audio)
curl "http://localhost:8000/files/{file_id}/stream" -o video.mp4

# Update file metadata
curl -X PATCH "http://localhost:8000/files/{file_id}" \
  -H "Content-Type: application/json" \
  -d '{"description": "Updated description", "tags": ["new", "tags"]}'

# Delete file
curl -X DELETE "http://localhost:8000/files/{file_id}"
```

### Utilities

```bash
# Get storage statistics
curl http://localhost:8000/stats

# Get available categories
curl http://localhost:8000/categories

# Clean up orphaned metadata
curl -X POST "http://localhost:8000/files/cleanup"
```

## File Categories

| Category | Extensions |
|----------|------------|
| image | .jpg, .jpeg, .png, .gif, .webp, .bmp |
| document | .pdf, .doc, .docx, .txt, .md |
| video | .mp4, .webm, .avi, .mov |
| audio | .mp3, .wav, .ogg, .flac |
| archive | .zip, .tar, .gz, .rar |

## File Metadata

```json
{
  "id": "uuid-string",
  "original_name": "document.pdf",
  "stored_name": "uuid.pdf",
  "file_path": "uploads/uuid.pdf",
  "file_size": 1024000,
  "mime_type": "application/pdf",
  "extension": ".pdf",
  "category": "document",
  "hash": "sha256-hash",
  "description": "Optional description",
  "tags": ["work", "important"],
  "downloads": 42,
  "created_at": "2024-01-15T10:30:00"
}
```

## Storage Statistics Response

```json
{
  "total_files": 150,
  "total_size": 524288000,
  "total_size_formatted": "500.00 MB",
  "by_category": {
    "image": 50,
    "document": 80,
    "video": 20
  },
  "max_file_size": 104857600,
  "max_file_size_formatted": "100.00 MB"
}
```

## Limits

- Maximum file size: 100 MB
- Supported file types: Images, Documents, Videos, Audio, Archives

## Project Structure

```
fastapi-file/
├── main.py           # Main application code
├── requirements.txt  # Python dependencies
├── README.md         # This file
└── uploads/          # Uploaded files directory (created on first upload)
```

## License

MIT
