# File Upload

An Express.js file upload application with Multer.

## Features

- Single and multiple file uploads
- Drag and drop support
- File listing with metadata
- File download
- File deletion
- Storage statistics
- 10MB max file size
- Progress indicator

## Installation

```bash
npm install
```

## Usage

```bash
npm start
```

The server will start on http://localhost:3004

## API Endpoints

### Upload Single File
```bash
POST /api/upload
Content-Type: multipart/form-data

file: <binary>
```

### Upload Multiple Files
```bash
POST /api/upload/multiple
Content-Type: multipart/form-data

files: <binary> (up to 10 files)
```

### List All Files
```bash
GET /api/files
```

### Get File Info
```bash
GET /api/files/:id
```

### Download File
```bash
GET /api/files/:id/download
```

### Delete File
```bash
DELETE /api/files/:id
```

### Get Storage Stats
```bash
GET /api/stats
```

## Example with cURL

```bash
# Upload a single file
curl -X POST http://localhost:3004/api/upload \
  -F "file=@/path/to/file.pdf"

# Upload multiple files
curl -X POST http://localhost:3004/api/upload/multiple \
  -F "files=@file1.jpg" \
  -F "files=@file2.pdf"

# List all files
curl http://localhost:3004/api/files

# Download a file
curl -O http://localhost:3004/api/files/:id/download

# Delete a file
curl -X DELETE http://localhost:3004/api/files/:id
```

## Supported File Types

- Images: JPEG, PNG, GIF, WebP
- Documents: PDF, DOC, DOCX, TXT
- Data: CSV, JSON
- Archives: ZIP, RAR

## Configuration

### Environment Variables

- `PORT` - Server port (default: 3004)

### Limits

- Maximum file size: 10MB
- Maximum files per request: 10

## File Storage

Files are stored in the `uploads/` directory. Each file is renamed with a unique timestamp and random suffix to prevent conflicts.
