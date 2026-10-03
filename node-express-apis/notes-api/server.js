const express = require('express');
const cors = require('cors');
const fs = require('fs');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;
const DATA_FILE = path.join(__dirname, 'notes.json');

app.use(cors());
app.use(express.json());

// Helper: Load notes from file
function loadNotes() {
  try {
    if (!fs.existsSync(DATA_FILE)) {
      fs.writeFileSync(DATA_FILE, '[]');
      return [];
    }
    const data = fs.readFileSync(DATA_FILE, 'utf8');
    return JSON.parse(data);
  } catch (err) {
    return [];
  }
}

// Helper: Save notes to file
function saveNotes(notes) {
  fs.writeFileSync(DATA_FILE, JSON.stringify(notes, null, 2));
}

// Helper: Generate unique ID
function generateId() {
  return Date.now().toString(36) + Math.random().toString(36).substr(2, 9);
}

// GET /notes - List all notes with optional filters
app.get('/notes', (req, res) => {
  try {
    let notes = loadNotes();
    const { search, category, sort } = req.query;

    // Filter by search
    if (search) {
      const term = search.toLowerCase();
      notes = notes.filter(n =>
        n.title.toLowerCase().includes(term) ||
        n.content.toLowerCase().includes(term)
      );
    }

    // Filter by category
    if (category) {
      notes = notes.filter(n => n.category === category);
    }

    // Sort
    if (sort === 'oldest') {
      notes.sort((a, b) => new Date(a.createdAt) - new Date(b.createdAt));
    } else {
      notes.sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt));
    }

    res.json({ success: true, data: notes, count: notes.length });
  } catch (err) {
    res.status(500).json({ success: false, error: 'Failed to fetch notes' });
  }
});

// GET /notes/:id - Get single note
app.get('/notes/:id', (req, res) => {
  try {
    const notes = loadNotes();
    const note = notes.find(n => n.id === req.params.id);

    if (!note) {
      return res.status(404).json({ success: false, error: 'Note not found' });
    }

    res.json({ success: true, data: note });
  } catch (err) {
    res.status(500).json({ success: false, error: 'Failed to fetch note' });
  }
});

// POST /notes - Create new note
app.post('/notes', (req, res) => {
  try {
    const { title, content, category } = req.body;

    if (!title) {
      return res.status(400).json({ success: false, error: 'Title is required' });
    }

    const notes = loadNotes();
    const now = new Date().toISOString();

    const newNote = {
      id: generateId(),
      title,
      content: content || '',
      category: category || 'general',
      createdAt: now,
      updatedAt: now
    };

    notes.push(newNote);
    saveNotes(notes);

    res.status(201).json({ success: true, data: newNote });
  } catch (err) {
    res.status(500).json({ success: false, error: 'Failed to create note' });
  }
});

// PUT /notes/:id - Update note
app.put('/notes/:id', (req, res) => {
  try {
    const notes = loadNotes();
    const index = notes.findIndex(n => n.id === req.params.id);

    if (index === -1) {
      return res.status(404).json({ success: false, error: 'Note not found' });
    }

    const { title, content, category } = req.body;

    notes[index] = {
      ...notes[index],
      title: title !== undefined ? title : notes[index].title,
      content: content !== undefined ? content : notes[index].content,
      category: category !== undefined ? category : notes[index].category,
      updatedAt: new Date().toISOString()
    };

    saveNotes(notes);
    res.json({ success: true, data: notes[index] });
  } catch (err) {
    res.status(500).json({ success: false, error: 'Failed to update note' });
  }
});

// DELETE /notes/:id - Delete note
app.delete('/notes/:id', (req, res) => {
  try {
    const notes = loadNotes();
    const index = notes.findIndex(n => n.id === req.params.id);

    if (index === -1) {
      return res.status(404).json({ success: false, error: 'Note not found' });
    }

    const deleted = notes.splice(index, 1)[0];
    saveNotes(notes);

    res.json({ success: true, message: 'Note deleted', data: deleted });
  } catch (err) {
    res.status(500).json({ success: false, error: 'Failed to delete note' });
  }
});

// GET /categories - List all categories
app.get('/categories', (req, res) => {
  try {
    const notes = loadNotes();
    const categories = [...new Set(notes.map(n => n.category))];
    res.json({ success: true, data: categories });
  } catch (err) {
    res.status(500).json({ success: false, error: 'Failed to fetch categories' });
  }
});

app.listen(PORT, () => {
  console.log(`Notes API running on http://localhost:${PORT}`);
});
