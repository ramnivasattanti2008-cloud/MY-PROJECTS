const express = require('express');
const Database = require('better-sqlite3');
const { nanoid } = require('nanoid');
const path = require('path');

const app = express();
const db = new Database('urls.db');

// Middleware
app.use(express.json());
app.use(express.static('public'));

// Initialize database
db.exec(`
  CREATE TABLE IF NOT EXISTS urls (
    id TEXT PRIMARY KEY,
    original_url TEXT NOT NULL,
    clicks INTEGER DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
  )
`);

// Create short URL
app.post('/api/shorten', (req, res) => {
  const { url } = req.body;

  if (!url) {
    return res.status(400).json({ error: 'URL is required' });
  }

  try {
    new URL(url);
  } catch {
    return res.status(400).json({ error: 'Invalid URL format' });
  }

  const id = nanoid(8);

  const stmt = db.prepare('INSERT INTO urls (id, original_url) VALUES (?, ?)');
  stmt.run(id, url);

  res.json({
    id,
    short_url: `${req.protocol}://${req.get('host')}/${id}`,
    original_url: url
  });
});

// Redirect to original URL
app.get('/:id', (req, res) => {
  const { id } = req.params;

  const stmt = db.prepare('SELECT original_url FROM urls WHERE id = ?');
  const row = stmt.get(id);

  if (!row) {
    return res.status(404).json({ error: 'URL not found' });
  }

  // Increment click count
  db.prepare('UPDATE urls SET clicks = clicks + 1 WHERE id = ?').run(id);

  res.redirect(row.original_url);
});

// Get URL stats
app.get('/api/urls/:id', (req, res) => {
  const { id } = req.params;

  const stmt = db.prepare('SELECT * FROM urls WHERE id = ?');
  const row = stmt.get(id);

  if (!row) {
    return res.status(404).json({ error: 'URL not found' });
  }

  res.json(row);
});

// List all URLs
app.get('/api/urls', (req, res) => {
  const stmt = db.prepare('SELECT * FROM urls ORDER BY created_at DESC');
  const rows = stmt.all();
  res.json(rows);
});

// Delete URL
app.delete('/api/urls/:id', (req, res) => {
  const { id } = req.params;

  const stmt = db.prepare('DELETE FROM urls WHERE id = ?');
  const result = stmt.run(id);

  if (result.changes === 0) {
    return res.status(404).json({ error: 'URL not found' });
  }

  res.json({ message: 'URL deleted successfully' });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`URL Shortener running on http://localhost:${PORT}`);
});
