const express = require('express');
const Database = require('better-sqlite3');
const hljs = require('highlight.js');
const { nanoid } = require('nanoid');

const app = express();
const db = new Database('pastes.db');

// Middleware
app.use(express.json());
app.use(express.static('public'));

// Initialize database
db.exec(`
  CREATE TABLE IF NOT EXISTS pastes (
    id TEXT PRIMARY KEY,
    title TEXT,
    content TEXT NOT NULL,
    language TEXT DEFAULT 'plaintext',
    views INTEGER DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
  )
`);

// Supported languages
const supportedLanguages = [
  'javascript', 'typescript', 'python', 'java', 'cpp', 'csharp',
  'go', 'rust', 'ruby', 'php', 'sql', 'html', 'css', 'json',
  'yaml', 'xml', 'markdown', 'bash', 'plaintext'
];

// Create paste
app.post('/api/pastes', (req, res) => {
  const { title, content, language } = req.body;

  if (!content) {
    return res.status(400).json({ error: 'Content is required' });
  }

  const id = nanoid(10);
  const lang = supportedLanguages.includes(language) ? language : 'plaintext';

  const stmt = db.prepare(
    'INSERT INTO pastes (id, title, content, language) VALUES (?, ?, ?, ?)'
  );
  stmt.run(id, title || 'Untitled', content, lang);

  res.json({ id, title: title || 'Untitled', language: lang });
});

// Get paste with syntax highlighting
app.get('/api/pastes/:id', (req, res) => {
  const { id } = req.params;

  const stmt = db.prepare('SELECT * FROM pastes WHERE id = ?');
  const paste = stmt.get(id);

  if (!paste) {
    return res.status(404).json({ error: 'Paste not found' });
  }

  // Increment view count
  db.prepare('UPDATE pastes SET views = views + 1 WHERE id = ?').run(id);
  paste.views++;

  // Highlight code
  try {
    if (paste.language === 'markdown') {
      const marked = require('marked');
      paste.highlighted = marked.parse(paste.content);
    } else {
      paste.highlighted = hljs.highlight(paste.content, {
        language: paste.language
      }).value;
    }
  } catch {
    paste.highlighted = escapeHtml(paste.content);
  }

  res.json(paste);
});

// Get raw paste
app.get('/api/pastes/:id/raw', (req, res) => {
  const { id } = req.params;

  const stmt = db.prepare('SELECT content, language FROM pastes WHERE id = ?');
  const paste = stmt.get(id);

  if (!paste) {
    return res.status(404).json({ error: 'Paste not found' });
  }

  res.set('Content-Type', 'text/plain; charset=utf-8');
  res.send(paste.content);
});

// List all pastes
app.get('/api/pastes', (req, res) => {
  const stmt = db.prepare(
    'SELECT id, title, language, views, created_at FROM pastes ORDER BY created_at DESC LIMIT 50'
  );
  const pastes = stmt.all();
  res.json(pastes);
});

// Delete paste
app.delete('/api/pastes/:id', (req, res) => {
  const { id } = req.params;

  const stmt = db.prepare('DELETE FROM pastes WHERE id = ?');
  const result = stmt.run(id);

  if (result.changes === 0) {
    return res.status(404).json({ error: 'Paste not found' });
  }

  res.json({ message: 'Paste deleted successfully' });
});

// Get supported languages
app.get('/api/languages', (req, res) => {
  res.json(supportedLanguages);
});

// Utility function
function escapeHtml(text) {
  const map = {
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#039;'
  };
  return text.replace(/[&<>"']/g, m => map[m]);
}

const PORT = process.env.PORT || 3001;
app.listen(PORT, () => {
  console.log(`Pastebin running on http://localhost:${PORT}`);
});
