const express = require('express');
const cors = require('cors');
const multer = require('multer');
const path = require('path');
const fs = require('fs');

const app = express();
const PORT = process.env.PORT || 3003;
const UPLOAD_DIR = path.join(__dirname, 'uploads');

// Ensure upload directory exists
if (!fs.existsSync(UPLOAD_DIR)) {
  fs.mkdirSync(UPLOAD_DIR, { recursive: true });
}

// Configure multer storage
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, UPLOAD_DIR);
  },
  filename: (req, file, cb) => {
    const uniqueSuffix = Date.now() + '-' + Math.round(Math.random() * 1E9);
    const ext = path.extname(file.originalname);
    cb(null, uniqueSuffix + ext);
  }
});

// File filter
const fileFilter = (req, file, cb) => {
  // Allow all files or restrict to certain types
  const allowedTypes = [
    'image/jpeg', 'image/png', 'image/gif', 'image/webp',
    'application/pdf', 'text/plain', 'text/csv',
    'application/json', 'application/zip',
    'video/mp4', 'video/webm',
    'audio/mpeg', 'audio/wav'
  ];

  // Allow if no restriction or if type is allowed
  const maxSize = 50 * 1024 * 1024; // 50MB default

  if (allowedTypes.includes(file.mimetype)) {
    cb(null, true);
  } else {
    cb(new Error(`File type ${file.mimetype} not allowed`), false);
  }
};

const upload = multer({
  storage,
  fileFilter,
  limits: {
    fileSize: 50 * 1024 * 1024 // 50MB
  }
});

app.use(cors());
app.use('/files', express.static(UPLOAD_DIR));

// Error handler for multer
app.use((err, req, res, next) => {
  if (err instanceof multer.MulterError) {
    if (err.code === 'LIMIT_FILE_SIZE') {
      return res.status(400).json({
        success: false,
        error: 'File too large. Maximum size is 50MB'
      });
    }
    return res.status(400).json({
      success: false,
      error: err.message
    });
  }
  if (err) {
    return res.status(400).json({
      success: false,
      error: err.message
    });
  }
  next();
});

// Helper: Get file list
function getFileList() {
  try {
    const files = fs.readdirSync(UPLOAD_DIR);
    return files.map(filename => {
      const filepath = path.join(UPLOAD_DIR, filename);
      const stats = fs.statSync(filepath);
      return {
        filename,
        size: stats.size,
        uploadedAt: stats.birthtime.toISOString(),
        url: `/files/${filename}`
      };
    });
  } catch (err) {
    return [];
  }
}

// POST /upload - Upload single file
app.post('/upload', upload.single('file'), (req, res) => {
  if (!req.file) {
    return res.status(400).json({ success: false, error: 'No file uploaded' });
  }

  res.json({
    success: true,
    message: 'File uploaded successfully',
    data: {
      filename: req.file.filename,
      originalName: req.file.originalname,
      size: req.file.size,
      mimetype: req.file.mimetype,
      url: `/files/${req.file.filename}`
    }
  });
});

// POST /upload/multiple - Upload multiple files
app.post('/upload/multiple', upload.array('files', 10), (req, res) => {
  if (!req.files || req.files.length === 0) {
    return res.status(400).json({ success: false, error: 'No files uploaded' });
  }

  const files = req.files.map(file => ({
    filename: file.filename,
    originalName: file.originalname,
    size: file.size,
    mimetype: file.mimetype,
    url: `/files/${file.filename}`
  }));

  res.json({
    success: true,
    message: `${files.length} files uploaded successfully`,
    data: files
  });
});

// GET /files - List all files
app.get('/files', (req, res) => {
  const files = getFileList();
  res.json({
    success: true,
    data: files,
    count: files.length
  });
});

// GET /files/:filename - Get file info
app.get('/files/:filename', (req, res) => {
  const { filename } = req.params;
  const filepath = path.join(UPLOAD_DIR, filename);

  if (!fs.existsSync(filepath)) {
    return res.status(404).json({ success: false, error: 'File not found' });
  }

  const stats = fs.statSync(filepath);
  res.json({
    success: true,
    data: {
      filename,
      size: stats.size,
      uploadedAt: stats.birthtime.toISOString(),
      modifiedAt: stats.mtime.toISOString(),
      url: `/files/${filename}`
    }
  });
});

// DELETE /files/:filename - Delete file
app.delete('/files/:filename', (req, res) => {
  const { filename } = req.params;
  const filepath = path.join(UPLOAD_DIR, filename);

  // Security: prevent directory traversal
  if (filename.includes('..') || filename.includes('/') || filename.includes('\\')) {
    return res.status(400).json({ success: false, error: 'Invalid filename' });
  }

  if (!fs.existsSync(filepath)) {
    return res.status(404).json({ success: false, error: 'File not found' });
  }

  fs.unlinkSync(filepath);
  res.json({
    success: true,
    message: 'File deleted successfully'
  });
});

// DELETE /files - Delete all files
app.delete('/files', (req, res) => {
  const files = fs.readdirSync(UPLOAD_DIR);
  let count = 0;

  files.forEach(filename => {
    fs.unlinkSync(path.join(UPLOAD_DIR, filename));
    count++;
  });

  res.json({
    success: true,
    message: `${count} files deleted`
  });
});

app.listen(PORT, () => {
  console.log(`File Upload API running on http://localhost:${PORT}`);
  console.log(`Upload directory: ${UPLOAD_DIR}`);
});
