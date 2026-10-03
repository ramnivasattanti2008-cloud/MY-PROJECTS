const express = require('express');
const cors = require('cors');
const Database = require('better-sqlite3');
const path = require('path');
const crypto = require('crypto');

const app = express();
const PORT = process.env.PORT || 3004;
const BASE_URL = process.env.BASE_URL || `http://localhost:${PORT}`;
const DB_PATH = path.join(__dirname, 'urls.db');

app.use(cors());
app.use(express.json());

// Initialize SQLite database
const db = new Database(DB_PATH);
db.exec(`
  CREATE TABLE IF NOT EXISTS urls (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    shortCode TEXT UNIQUE NOT NULL,
    originalUrl TEXT NOT NULL,
    title TEXT,
    createdAt TEXT DEFAULT CURRENT_TIMESTAMP,
    visitCount INTEGER DEFAULT 0,
    lastVisitedAt TEXT
  );
  CREATE TABLE IF NOT EXISTS visits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    urlId INTEGER NOT NULL,
    visitedAt TEXT DEFAULT CURRENT_TIMESTAMP,
    referer TEXT,
    userAgent TEXT,
    ipAddress TEXT,
    country TEXT,
    FOREIGN KEY (urlId) REFERENCES urls(id) ON DELETE CASCADE
  );
`);

// Helper: Generate short code
function generateShortCode(length = 6) {
  const chars = 'ABCDEFGHJKLMNPQRSTUVWXYZabcdefghjkmnpqrstuvwxyz23456789';
  let code = '';
  const bytes = crypto.randomBytes(length);
  for (let i = 0; i < length; i++) {
    code += chars[bytes[i] % chars.length];
  }
  return code;
}

// Helper: Validate URL
function isValidUrl(string) {
  try {
    new URL(string);
    return true;
  } catch (_) {
    return false;
  }
}

// POST /urls - Create short URL
app.post('/urls', (req, res) => {
  try {
    const { url, title, customCode } = req.body;

    if (!url) {
      return res.status(400).json({
        success: false,
        error: 'URL is required'
      });
    }

    if (!isValidUrl(url)) {
      return res.status(400).json({
        success: false,
        error: 'Invalid URL format'
      });
    }

    // Check for custom code
    let shortCode = customCode || generateShortCode();

    // Check if code already exists
    const existing = db.prepare('SELECT id FROM urls WHERE shortCode = ?').get(shortCode);
    if (existing) {
      if (customCode) {
        return res.status(409).json({
          success: false,
          error: 'Custom code already in use'
        });
      }
      // Generate new code
      shortCode = generateShortCode();
    }

    // Insert URL
    const result = db.prepare(
      'INSERT INTO urls (shortCode, originalUrl, title) VALUES (?, ?, ?)'
    ).run(shortCode, url, title || '');

    const fullUrl = `${BASE_URL}/${shortCode}`;

    res.status(201).json({
      success: true,
      data: {
        id: result.lastInsertRowid,
        shortCode,
        shortUrl: fullUrl,
        originalUrl: url,
        title: title || ''
      }
    });
  } catch (err) {
    console.error(err);
    res.status(500).json({ success: false, error: 'Failed to create short URL' });
  }
});

// GET /urls - List all URLs
app.get('/urls', (req, res) => {
  try {
    const urls = db.prepare(`
      SELECT id, shortCode, originalUrl, title, visitCount, lastVisitedAt, createdAt
      FROM urls ORDER BY createdAt DESC
    `).all();

    const result = urls.map(row => ({
      ...row,
      shortUrl: `${BASE_URL}/${row.shortCode}`
    }));

    res.json({
      success: true,
      data: result,
      count: result.length
    });
  } catch (err) {
    res.status(500).json({ success: false, error: 'Failed to fetch URLs' });
  }
});

// GET /urls/:shortCode - Get URL info
app.get('/urls/:shortCode', (req, res) => {
  try {
    const { shortCode } = req.params;

    const url = db.prepare(`
      SELECT id, shortCode, originalUrl, title, visitCount, lastVisitedAt, createdAt
      FROM urls WHERE shortCode = ?
    `).get(shortCode);

    if (!url) {
      return res.status(404).json({ success: false, error: 'URL not found' });
    }

    // Get recent visits
    const recentVisits = db.prepare(`
      SELECT visitedAt, referer, country
      FROM visits WHERE urlId = ? ORDER BY visitedAt DESC LIMIT 10
    `).all(url.id);

    res.json({
      success: true,
      data: {
        ...url,
        shortUrl: `${BASE_URL}/${shortCode}`,
        recentVisits
      }
    });
  } catch (err) {
    res.status(500).json({ success: false, error: 'Failed to fetch URL' });
  }
});

// GET /:shortCode - Redirect to original URL
app.get('/:shortCode', (req, res) => {
  try {
    const { shortCode } = req.params;

    const url = db.prepare('SELECT * FROM urls WHERE shortCode = ?').get(shortCode);

    if (!url) {
      return res.status(404).json({ success: false, error: 'Short URL not found' });
    }

    // Record visit
    const now = new Date().toISOString();
    db.prepare(`
      UPDATE urls SET visitCount = visitCount + 1, lastVisitedAt = ? WHERE id = ?
    `).run(now, url.id);

    db.prepare(`
      INSERT INTO visits (urlId, referer, userAgent, ipAddress)
      VALUES (?, ?, ?, ?)
    `).run(
      url.id,
      req.headers.referer || '',
      req.headers['user-agent'] || '',
      req.ip || req.connection.remoteAddress || ''
    );

    // Redirect to original URL
    res.redirect(url.originalUrl);
  } catch (err) {
    console.error(err);
    res.status(500).json({ success: false, error: 'Failed to redirect' });
  }
});

// DELETE /urls/:shortCode - Delete URL
app.delete('/urls/:shortCode', (req, res) => {
  try {
    const { shortCode } = req.params;

    const url = db.prepare('SELECT * FROM urls WHERE shortCode = ?').get(shortCode);

    if (!url) {
      return res.status(404).json({ success: false, error: 'URL not found' });
    }

    db.prepare('DELETE FROM urls WHERE shortCode = ?').run(shortCode);

    res.json({
      success: true,
      message: 'URL deleted successfully'
    });
  } catch (err) {
    res.status(500).json({ success: false, error: 'Failed to delete URL' });
  }
});

// GET /urls/:shortCode/clicks - Get click statistics
app.get('/urls/:shortCode/clicks', (req, res) => {
  try {
    const { shortCode } = req.params;

    const url = db.prepare('SELECT * FROM urls WHERE shortCode = ?').get(shortCode);

    if (!url) {
      return res.status(404).json({ success: false, error: 'URL not found' });
    }

    const clicksByDay = db.prepare(`
      SELECT DATE(visitedAt) as date, COUNT(*) as clicks
      FROM visits WHERE urlId = ?
      GROUP BY DATE(visitedAt) ORDER BY date DESC LIMIT 30
    `).all(url.id);

    const topReferers = db.prepare(`
      SELECT referer, COUNT(*) as count
      FROM visits WHERE urlId = ? AND referer != ''
      GROUP BY referer ORDER BY count DESC LIMIT 10
    `).all(url.id);

    res.json({
      success: true,
      data: {
        totalClicks: url.visitCount,
        clicksByDay,
        topReferers,
        lastVisited: url.lastVisitedAt
      }
    });
  } catch (err) {
    res.status(500).json({ success: false, error: 'Failed to fetch statistics' });
  }
});

app.listen(PORT, () => {
  console.log(`URL Shortener API running on http://localhost:${PORT}`);
});
