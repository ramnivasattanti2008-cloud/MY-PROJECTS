/**
 * Express.js Notes REST API
 * Stores notes in a JSON file
 */

const express = require("express");
const cors = require("cors");
const fs = require("fs");
const path = require("path");
const { randomUUID } = require("crypto");

const app = express();
const PORT = process.env.PORT || 3000;
const DATA_FILE = path.join(__dirname, "notes.json");

// Middleware
app.use(cors());
app.use(express.json());

// Helper functions
function readNotes() {
  try {
    if (!fs.existsSync(DATA_FILE)) {
      return [];
    }
    const data = fs.readFileSync(DATA_FILE, "utf-8");
    return JSON.parse(data);
  } catch (error) {
    console.error("Error reading notes:", error.message);
    return [];
  }
}

function writeNotes(notes) {
  try {
    fs.writeFileSync(DATA_FILE, JSON.stringify(notes, null, 2));
    return true;
  } catch (error) {
    console.error("Error writing notes:", error.message);
    return false;
  }
}

// Health check
app.get("/health", (req, res) => {
  res.json({ status: "healthy", timestamp: new Date().toISOString() });
});

// Get all notes
app.get("/notes", (req, res) => {
  try {
    const notes = readNotes();
    const { search, tag } = req.query;

    let filtered = notes;

    if (search) {
      const searchLower = search.toLowerCase();
      filtered = filtered.filter(
        (note) =>
          note.title.toLowerCase().includes(searchLower) ||
          note.content.toLowerCase().includes(searchLower)
      );
    }

    if (tag) {
      filtered = filtered.filter((note) => note.tags.includes(tag));
    }

    res.json({ success: true, count: filtered.length, data: filtered });
  } catch (error) {
    res.status(500).json({ success: false, error: "Failed to retrieve notes" });
  }
});

// Get single note
app.get("/notes/:id", (req, res) => {
  try {
    const notes = readNotes();
    const note = notes.find((n) => n.id === req.params.id);

    if (!note) {
      return res.status(404).json({ success: false, error: "Note not found" });
    }

    res.json({ success: true, data: note });
  } catch (error) {
    res.status(500).json({ success: false, error: "Failed to retrieve note" });
  }
});

// Create note
app.post("/notes", (req, res) => {
  try {
    const { title, content, tags = [] } = req.body;

    if (!title) {
      return res.status(400).json({ success: false, error: "Title is required" });
    }

    const notes = readNotes();
    const newNote = {
      id: randomUUID(),
      title: title.trim(),
      content: (content || "").trim(),
      tags: Array.isArray(tags) ? tags : [],
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
    };

    notes.unshift(newNote);
    writeNotes(notes);

    res.status(201).json({ success: true, data: newNote });
  } catch (error) {
    res.status(500).json({ success: false, error: "Failed to create note" });
  }
});

// Update note
app.put("/notes/:id", (req, res) => {
  try {
    const notes = readNotes();
    const index = notes.findIndex((n) => n.id === req.params.id);

    if (index === -1) {
      return res.status(404).json({ success: false, error: "Note not found" });
    }

    const { title, content, tags } = req.body;
    const updatedNote = {
      ...notes[index],
      title: title !== undefined ? title.trim() : notes[index].title,
      content: content !== undefined ? content.trim() : notes[index].content,
      tags: tags !== undefined ? (Array.isArray(tags) ? tags : notes[index].tags) : notes[index].tags,
      updatedAt: new Date().toISOString(),
    };

    notes[index] = updatedNote;
    writeNotes(notes);

    res.json({ success: true, data: updatedNote });
  } catch (error) {
    res.status(500).json({ success: false, error: "Failed to update note" });
  }
});

// Delete note
app.delete("/notes/:id", (req, res) => {
  try {
    const notes = readNotes();
    const index = notes.findIndex((n) => n.id === req.params.id);

    if (index === -1) {
      return res.status(404).json({ success: false, error: "Note not found" });
    }

    const deletedNote = notes.splice(index, 1)[0];
    writeNotes(notes);

    res.json({ success: true, message: "Note deleted", data: deletedNote });
  } catch (error) {
    res.status(500).json({ success: false, error: "Failed to delete note" });
  }
});

// Get all tags
app.get("/tags", (req, res) => {
  try {
    const notes = readNotes();
    const tagCount = {};

    notes.forEach((note) => {
      note.tags.forEach((tag) => {
        tagCount[tag] = (tagCount[tag] || 0) + 1;
      });
    });

    res.json({
      success: true,
      data: Object.entries(tagCount).map(([tag, count]) => ({ tag, count })),
    });
  } catch (error) {
    res.status(500).json({ success: false, error: "Failed to retrieve tags" });
  }
});

// Error handling middleware
app.use((err, req, res, next) => {
  console.error("Unhandled error:", err);
  res.status(500).json({ success: false, error: "Internal server error" });
});

// Start server
app.listen(PORT, () => {
  console.log(`Notes API running at http://localhost:${PORT}`);
  console.log(`API docs: http://localhost:${PORT}/health`);
});
