# File Upload API

Express API for uploading, listing, and managing files.

## Quick Start

```bash
npm install
npm start
```

API runs at `http://localhost:3003`

Files served at `http://localhost:3003/files`

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /upload | Upload single file |
| POST | /upload/multiple | Upload multiple files (max 10) |
| GET | /files | List all files |
| GET | /files/:filename | Get file info |
| DELETE | /files/:filename | Delete file |
| DELETE | /files | Delete all files |

## Examples

```bash
# Upload a file
curl -X POST http://localhost:3003/upload \
  -F "file=@/path/to/file.jpg"

# Upload multiple files
curl -X POST http://localhost:3003/upload/multiple \
  -F "files=@file1.txt" \
  -F "files=@file2.txt"

# List all files
curl http://localhost:3003/files

# Get file info
curl http://localhost:3003/files/abc123-456.jpg

# Delete a file
curl -X DELETE http://localhost:3003/files/abc123-456.jpg

# Delete all files
curl -X DELETE http://localhost:3003/files
```

## Response Format

```json
{
  "success": true,
  "message": "File uploaded successfully",
  "data": {
    "filename": "abc123-456.jpg",
    "originalName": "photo.jpg",
    "size": 102400,
    "mimetype": "image/jpeg",
    "url": "/files/abc123-456.jpg"
  }
}
```

## Allowed File Types

- Images: JPEG, PNG, GIF, WebP
- Documents: PDF, TXT, CSV, JSON
- Archives: ZIP
- Video: MP4, WebM
- Audio: MP3, WAV

## Limits

- Max file size: 50MB
- Max files per multi-upload: 10
- Upload directory: `uploads/`

## Security

- Filenames randomized to prevent collisions
- Directory traversal protection
- File type validation by MIME type
- Size limit enforced by multer
