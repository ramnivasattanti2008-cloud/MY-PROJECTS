/**
 * Express.js REST API
 * A simple CRUD API for managing posts with middleware examples.
 */

const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const morgan = require('morgan');
const { v4: uuidv4 } = require('uuid');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(helmet());
app.use(cors());
app.use(morgan('dev'));
app.use(express.json());

// In-memory database
let posts = [
  {
    id: '1',
    title: 'Welcome to Express API',
    content: 'This is a sample post to get you started.',
    author: 'admin',
    tags: ['welcome', 'api'],
    createdAt: new Date('2024-01-01').toISOString(),
    updatedAt: new Date('2024-01-01').toISOString()
  }
];

// Custom middleware: Request logger
app.use((req, res, next) => {
  req.requestTime = new Date().toISOString();
  console.log(`${req.method} ${req.path} - ${req.requestTime}`);
  next();
});

// Custom middleware: Validate post input
const validatePost = (req, res, next) => {
  const { title, content } = req.body;

  if (!title || typeof title !== 'string' || title.trim().length === 0) {
    return res.status(400).json({ error: 'Title is required and must be a non-empty string' });
  }

  if (title.length > 200) {
    return res.status(400).json({ error: 'Title must be 200 characters or less' });
  }

  if (!content || typeof content !== 'string' || content.trim().length === 0) {
    return res.status(400).json({ error: 'Content is required and must be a non-empty string' });
  }

  if (content.length > 10000) {
    return res.status(400).json({ error: 'Content must be 10000 characters or less' });
  }

  next();
};

// Custom middleware: Validate UUID
const validateUUID = (req, res, next) => {
  const { id } = req.params;
  const uuidRegex = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;

  if (!uuidRegex.test(id) && !/^\d+$/.test(id)) {
    return res.status(400).json({ error: 'Invalid ID format' });
  }

  next();
};

// Error handling middleware
const errorHandler = (err, req, res, next) => {
  console.error('Error:', err);
  res.status(500).json({
    error: 'Internal Server Error',
    message: process.env.NODE_ENV === 'development' ? err.message : undefined
  });
};

// Routes

// Health check
app.get('/', (req, res) => {
  res.json({
    status: 'healthy',
    service: 'Express REST API',
    timestamp: new Date().toISOString()
  });
});

// List posts with pagination and filtering
app.get('/api/posts', (req, res) => {
  try {
    let result = [...posts];

    // Filter by author
    if (req.query.author) {
      result = result.filter(post =>
        post.author.toLowerCase().includes(req.query.author.toLowerCase())
      );
    }

    // Filter by tag
    if (req.query.tag) {
      result = result.filter(post =>
        post.tags.some(tag => tag.toLowerCase() === req.query.tag.toLowerCase())
      );
    }

    // Search in title and content
    if (req.query.search) {
      const search = req.query.search.toLowerCase();
      result = result.filter(post =>
        post.title.toLowerCase().includes(search) ||
        post.content.toLowerCase().includes(search)
      );
    }

    // Pagination
    const page = parseInt(req.query.page) || 1;
    const pageSize = parseInt(req.query.pageSize) || 10;
    const startIndex = (page - 1) * pageSize;
    const endIndex = startIndex + pageSize;

    const paginatedResult = result.slice(startIndex, endIndex);

    res.json({
      data: paginatedResult,
      pagination: {
        page,
        pageSize,
        total: result.length,
        totalPages: Math.ceil(result.length / pageSize)
      }
    });
  } catch (error) {
    next(error);
  }
});

// Get single post
app.get('/api/posts/:id', validateUUID, (req, res, next) => {
  try {
    const post = posts.find(p => p.id === req.params.id);

    if (!post) {
      return res.status(404).json({ error: 'Post not found' });
    }

    res.json(post);
  } catch (error) {
    next(error);
  }
});

// Create post
app.post('/api/posts', validatePost, (req, res, next) => {
  try {
    const { title, content, author = 'anonymous', tags = [] } = req.body;

    const newPost = {
      id: uuidv4(),
      title: title.trim(),
      content: content.trim(),
      author: author.trim(),
      tags: Array.isArray(tags) ? tags.map(t => t.trim().toLowerCase()) : [],
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString()
    };

    posts.unshift(newPost);

    res.status(201).json(newPost);
  } catch (error) {
    next(error);
  }
});

// Update post
app.put('/api/posts/:id', validateUUID, validatePost, (req, res, next) => {
  try {
    const index = posts.findIndex(p => p.id === req.params.id);

    if (index === -1) {
      return res.status(404).json({ error: 'Post not found' });
    }

    const { title, content, author, tags } = req.body;

    posts[index] = {
      ...posts[index],
      title: title.trim(),
      content: content.trim(),
      author: author ? author.trim() : posts[index].author,
      tags: tags ? (Array.isArray(tags) ? tags.map(t => t.trim().toLowerCase()) : []) : posts[index].tags,
      updatedAt: new Date().toISOString()
    };

    res.json(posts[index]);
  } catch (error) {
    next(error);
  }
});

// Partial update post
app.patch('/api/posts/:id', validateUUID, (req, res, next) => {
  try {
    const index = posts.findIndex(p => p.id === req.params.id);

    if (index === -1) {
      return res.status(404).json({ error: 'Post not found' });
    }

    const allowedFields = ['title', 'content', 'author', 'tags'];
    const updates = {};

    for (const field of allowedFields) {
      if (req.body[field] !== undefined) {
        if (field === 'tags' && Array.isArray(req.body[field])) {
          updates[field] = req.body[field].map(t => t.trim().toLowerCase());
        } else {
          updates[field] = typeof req.body[field] === 'string'
            ? req.body[field].trim()
            : req.body[field];
        }
      }
    }

    posts[index] = {
      ...posts[index],
      ...updates,
      updatedAt: new Date().toISOString()
    };

    res.json(posts[index]);
  } catch (error) {
    next(error);
  }
});

// Delete post
app.delete('/api/posts/:id', validateUUID, (req, res, next) => {
  try {
    const index = posts.findIndex(p => p.id === req.params.id);

    if (index === -1) {
      return res.status(404).json({ error: 'Post not found' });
    }

    const deleted = posts.splice(index, 1)[0];

    res.json({ message: 'Post deleted', post: deleted });
  } catch (error) {
    next(error);
  }
});

// Get all tags
app.get('/api/tags', (req, res) => {
  const allTags = [...new Set(posts.flatMap(p => p.tags))];
  res.json({ tags: allTags });
});

// Get statistics
app.get('/api/stats', (req, res) => {
  const stats = {
    totalPosts: posts.length,
    authors: [...new Set(posts.map(p => p.author))],
    tagCounts: posts.flatMap(p => p.tags).reduce((acc, tag) => {
      acc[tag] = (acc[tag] || 0) + 1;
      return acc;
    }, {}),
    averageTitleLength: posts.length > 0
      ? Math.round(posts.reduce((sum, p) => sum + p.title.length, 0) / posts.length)
      : 0
  };
  res.json(stats);
});

// 404 handler
app.use((req, res) => {
  res.status(404).json({ error: 'Route not found' });
});

// Error handler
app.use(errorHandler);

// Start server
app.listen(PORT, () => {
  console.log(`Express REST API running on http://localhost:${PORT}`);
  console.log(`Health check: http://localhost:${PORT}/`);
  console.log(`API endpoints: http://localhost:${PORT}/api/posts`);
});

module.exports = app;
