const express = require('express');
const multer = require('multer');
const path = require('path');
const fs = require('fs');
const { v4: uuidv4 } = require('crypto');

const app = express();

// Ensure uploads directory exists
const UPLOAD_DIR = path.join(__dirname, 'uploads');
if (!fs.existsSync(UPLOAD_DIR)) {
  fs.mkdirSync(UPLOAD_DIR, { recursive: true });
}

// Configure multer storage
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, UPLOAD_DIR);
  },
  filename: (req, file, cb) => {
    const uniqueName = `${Date.now()}-${Math.round(Math.random() * 1E9)}${path.extname(file.originalname)}`;
    cb(null, uniqueName);
  }
});

// File filter
const fileFilter = (req, file, cb) => {
  // Allow all file types or restrict as needed
  const allowedTypes = [
    'image/jpeg', 'image/png', 'image/gif', 'image/webp',
    'application/pdf', 'application/msword',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'text/plain', 'text/csv', 'application/json',
    'application/zip', 'application/x-rar-compressed'
  ];

  if (allowedTypes.includes(file.mimetype) || true) {
    cb(null, true);
  } else {
    cb(new Error(`File type ${file.mimetype} not allowed`), false);
  }
};

const upload = multer({
  storage,
  fileFilter,
  limits: {
    fileSize: 10 * 1024 * 1024 // 10MB max
  }
});

// Middleware
app.use(express.json());
app.use(express.static('public'));
app.use('/uploads', express.static(UPLOAD_DIR));

// Store file metadata (in-memory)
const files = [];

// Generate unique ID
function generateId() {
  return `${Date.now().toString(36)}-${Math.random().toString(36).substr(2, 9)}`;
}

// Upload single file
app.post('/api/upload', upload.single('file'), (req, res) => {
  if (!req.file) {
    return res.status(400).json({ error: 'No file uploaded' });
  }

  const fileData = {
    id: generateId(),
    originalName: req.file.originalname,
    filename: req.file.filename,
    size: req.file.size,
    mimetype: req.file.mimetype,
    path: `/uploads/${req.file.filename}`,
    uploadedAt: new Date().toISOString()
  };

  files.push(fileData);
  res.status(201).json(fileData);
});

// Upload multiple files
app.post('/api/upload/multiple', upload.array('files', 10), (req, res) => {
  if (!req.files || req.files.length === 0) {
    return res.status(400).json({ error: 'No files uploaded' });
  }

  const uploadedFiles = req.files.map(file => ({
    id: generateId(),
    originalName: file.originalname,
    filename: file.filename,
    size: file.size,
    mimetype: file.mimetype,
    path: `/uploads/${file.filename}`,
    uploadedAt: new Date().toISOString()
  }));

  files.push(...uploadedFiles);
  res.status(201).json(uploadedFiles);
});

// List all files
app.get('/api/files', (req, res) => {
  res.json(files);
});

// Get file info
app.get('/api/files/:id', (req, res) => {
  const file = files.find(f => f.id === req.params.id);

  if (!file) {
    return res.status(404).json({ error: 'File not found' });
  }

  res.json(file);
});

// Download file
app.get('/api/files/:id/download', (req, res) => {
  const file = files.find(f => f.id === req.params.id);

  if (!file) {
    return res.status(404).json({ error: 'File not found' });
  }

  const filePath = path.join(UPLOAD_DIR, file.filename);

  if (!fs.existsSync(filePath)) {
    return res.status(404).json({ error: 'File not found on disk' });
  }

  res.download(filePath, file.originalName);
});

// Delete file
app.delete('/api/files/:id', (req, res) => {
  const index = files.findIndex(f => f.id === req.params.id);

  if (index === -1) {
    return res.status(404).json({ error: 'File not found' });
  }

  const file = files[index];
  const filePath = path.join(UPLOAD_DIR, file.filename);

  // Delete from disk
  if (fs.existsSync(filePath)) {
    fs.unlinkSync(filePath);
  }

  // Remove from memory
  files.splice(index, 1);

  res.json({ message: 'File deleted successfully' });
});

// Format file size
function formatSize(bytes) {
  if (bytes === 0) return '0 Bytes';
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

// Error handling middleware
app.use((err, req, res, next) => {
  if (err instanceof multer.MulterError) {
    if (err.code === 'LIMIT_FILE_SIZE') {
      return res.status(400).json({ error: 'File too large. Maximum size is 10MB' });
    }
    return res.status(400).json({ error: err.message });
  }

  if (err) {
    return res.status(400).json({ error: err.message });
  }

  next();
});

// Get storage stats
app.get('/api/stats', (req, res) => {
  const totalSize = files.reduce((sum, f) => sum + f.size, 0);

  res.json({
    totalFiles: files.length,
    totalSize,
    totalSizeFormatted: formatSize(totalSize),
    averageSize: files.length > 0 ? Math.round(totalSize / files.length) : 0
  });
});

const PORT = process.env.PORT || 3004;
app.listen(PORT, () => {
  console.log(`File Upload server running on http://localhost:${PORT}`);
  console.log(`Files will be stored in: ${UPLOAD_DIR}`);
});
