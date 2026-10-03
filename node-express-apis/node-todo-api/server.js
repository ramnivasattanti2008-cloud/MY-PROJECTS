const express = require('express');
const Database = require('better-sqlite3');
const jwt = require('jsonwebtoken');
const bcrypt = require('bcryptjs');

const app = express();
const db = new Database('todos.db');
const JWT_SECRET = process.env.JWT_SECRET || 'your-secret-key-change-in-production';

// Middleware
app.use(express.json());

// Initialize database
db.exec(`
  CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
  );

  CREATE TABLE IF NOT EXISTS todos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    completed INTEGER DEFAULT 0,
    priority TEXT DEFAULT 'medium',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
  )
`);

// Auth middleware
function authenticate(req, res, next) {
  const authHeader = req.headers.authorization;

  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    return res.status(401).json({ error: 'No token provided' });
  }

  const token = authHeader.split(' ')[1];

  try {
    const decoded = jwt.verify(token, JWT_SECRET);
    req.userId = decoded.userId;
    next();
  } catch {
    return res.status(401).json({ error: 'Invalid token' });
  }
}

// ==================== AUTH ROUTES ====================

// Register
app.post('/api/auth/register', async (req, res) => {
  const { email, password } = req.body;

  if (!email || !password) {
    return res.status(400).json({ error: 'Email and password are required' });
  }

  if (password.length < 6) {
    return res.status(400).json({ error: 'Password must be at least 6 characters' });
  }

  const hashedPassword = await bcrypt.hash(password, 10);

  try {
    const stmt = db.prepare('INSERT INTO users (email, password) VALUES (?, ?)');
    const result = stmt.run(email, hashedPassword);

    const token = jwt.sign({ userId: result.lastInsertRowid }, JWT_SECRET, { expiresIn: '7d' });

    res.status(201).json({
      message: 'User registered successfully',
      token,
      user: { id: result.lastInsertRowid, email }
    });
  } catch (error) {
    if (error.message.includes('UNIQUE constraint')) {
      return res.status(409).json({ error: 'Email already exists' });
    }
    res.status(500).json({ error: 'Registration failed' });
  }
});

// Login
app.post('/api/auth/login', async (req, res) => {
  const { email, password } = req.body;

  if (!email || !password) {
    return res.status(400).json({ error: 'Email and password are required' });
  }

  const stmt = db.prepare('SELECT * FROM users WHERE email = ?');
  const user = stmt.get(email);

  if (!user) {
    return res.status(401).json({ error: 'Invalid credentials' });
  }

  const validPassword = await bcrypt.compare(password, user.password);

  if (!validPassword) {
    return res.status(401).json({ error: 'Invalid credentials' });
  }

  const token = jwt.sign({ userId: user.id }, JWT_SECRET, { expiresIn: '7d' });

  res.json({
    message: 'Login successful',
    token,
    user: { id: user.id, email: user.email }
  });
});

// ==================== TODO ROUTES ====================

// Create todo
app.post('/api/todos', authenticate, (req, res) => {
  const { title, description, priority } = req.body;

  if (!title) {
    return res.status(400).json({ error: 'Title is required' });
  }

  const validPriorities = ['low', 'medium', 'high'];
  const todoPriority = validPriorities.includes(priority) ? priority : 'medium';

  const stmt = db.prepare(
    'INSERT INTO todos (user_id, title, description, priority) VALUES (?, ?, ?, ?)'
  );
  const result = stmt.run(req.userId, title, description || null, todoPriority);

  const newTodo = db.prepare('SELECT * FROM todos WHERE id = ?').get(result.lastInsertRowid);
  res.status(201).json(newTodo);
});

// Get all todos for user
app.get('/api/todos', authenticate, (req, res) => {
  const { completed, priority } = req.query;

  let query = 'SELECT * FROM todos WHERE user_id = ?';
  const params = [req.userId];

  if (completed !== undefined) {
    query += ' AND completed = ?';
    params.push(completed === 'true' ? 1 : 0);
  }

  if (priority) {
    query += ' AND priority = ?';
    params.push(priority);
  }

  query += ' ORDER BY created_at DESC';

  const stmt = db.prepare(query);
  const todos = stmt.all(...params);
  res.json(todos);
});

// Get single todo
app.get('/api/todos/:id', authenticate, (req, res) => {
  const { id } = req.params;

  const stmt = db.prepare('SELECT * FROM todos WHERE id = ? AND user_id = ?');
  const todo = stmt.get(id, req.userId);

  if (!todo) {
    return res.status(404).json({ error: 'Todo not found' });
  }

  res.json(todo);
});

// Update todo
app.put('/api/todos/:id', authenticate, (req, res) => {
  const { id } = req.params;
  const { title, description, completed, priority } = req.body;

  const existing = db.prepare('SELECT * FROM todos WHERE id = ? AND user_id = ?').get(id, req.userId);
  if (!existing) {
    return res.status(404).json({ error: 'Todo not found' });
  }

  const validPriorities = ['low', 'medium', 'high'];

  const updatedTodo = {
    title: title || existing.title,
    description: description !== undefined ? description : existing.description,
    completed: completed !== undefined ? (completed ? 1 : 0) : existing.completed,
    priority: validPriorities.includes(priority) ? priority : existing.priority,
    updated_at: new Date().toISOString()
  };

  const stmt = db.prepare(`
    UPDATE todos
    SET title = ?, description = ?, completed = ?, priority = ?, updated_at = ?
    WHERE id = ? AND user_id = ?
  `);
  stmt.run(
    updatedTodo.title,
    updatedTodo.description,
    updatedTodo.completed,
    updatedTodo.priority,
    updatedTodo.updated_at,
    id,
    req.userId
  );

  const todo = db.prepare('SELECT * FROM todos WHERE id = ?').get(id);
  res.json(todo);
});

// Delete todo
app.delete('/api/todos/:id', authenticate, (req, res) => {
  const { id } = req.params;

  const stmt = db.prepare('DELETE FROM todos WHERE id = ? AND user_id = ?');
  const result = stmt.run(id, req.userId);

  if (result.changes === 0) {
    return res.status(404).json({ error: 'Todo not found' });
  }

  res.json({ message: 'Todo deleted successfully' });
});

// Toggle todo completion
app.patch('/api/todos/:id/toggle', authenticate, (req, res) => {
  const { id } = req.params;

  const existing = db.prepare('SELECT * FROM todos WHERE id = ? AND user_id = ?').get(id, req.userId);
  if (!existing) {
    return res.status(404).json({ error: 'Todo not found' });
  }

  const newCompleted = existing.completed ? 0 : 1;
  db.prepare('UPDATE todos SET completed = ?, updated_at = ? WHERE id = ?')
    .run(newCompleted, new Date().toISOString(), id);

  const todo = db.prepare('SELECT * FROM todos WHERE id = ?').get(id);
  res.json(todo);
});

const PORT = process.env.PORT || 3002;
app.listen(PORT, () => {
  console.log(`Todo API running on http://localhost:${PORT}`);
});
