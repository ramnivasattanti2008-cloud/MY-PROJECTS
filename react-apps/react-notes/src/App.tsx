import { useState, useEffect } from 'react';
import { v4 as uuid } from 'uuid';

interface Note {
  id: string;
  title: string;
  content: string;
  createdAt: string;
}

const STORAGE_KEY = 'react-notes-data';

export default function App() {
  const [notes, setNotes] = useState<Note[]>([]);
  const [selected, setSelected] = useState<Note | null>(null);
  const [editTitle, setEditTitle] = useState('');
  const [editContent, setEditContent] = useState('');

  useEffect(() => {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved) setNotes(JSON.parse(saved));
  }, []);

  useEffect(() => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(notes));
  }, [notes]);

  const createNote = () => {
    const note: Note = { id: uuid(), title: 'Untitled', content: '', createdAt: new Date().toISOString() };
    setNotes((prev) => [note, ...prev]);
    setSelected(note);
    setEditTitle(note.title);
    setEditContent(note.content);
  };

  const selectNote = (note: Note) => {
    setSelected(note);
    setEditTitle(note.title);
    setEditContent(note.content);
  };

  const saveNote = () => {
    if (!selected) return;
    const updated = { ...selected, title: editTitle || 'Untitled', content: editContent };
    setNotes((prev) => prev.map((n) => (n.id === selected.id ? updated : n)));
    setSelected(updated);
  };

  const deleteNote = (id: string) => {
    setNotes((prev) => prev.filter((n) => n.id !== id));
    if (selected?.id === id) {
      setSelected(null);
      setEditTitle('');
      setEditContent('');
    }
  };

  return (
    <div style={styles.container}>
      <div style={styles.sidebar}>
        <div style={styles.sidebarHeader}>
          <h1 style={styles.title}>Notes</h1>
          <button style={styles.addBtn} onClick={createNote}>+ New</button>
        </div>
        <div style={styles.list}>
          {notes.map((note) => (
            <div
              key={note.id}
              style={{ ...styles.noteItem, ...(selected?.id === note.id ? styles.noteItemActive : {}) }}
              onClick={() => selectNote(note)}
            >
              <div style={styles.noteTitle}>{note.title}</div>
              <div style={styles.notePreview}>{note.content.slice(0, 60) || 'Empty note'}</div>
              <button
                style={styles.deleteBtn}
                onClick={(e) => { e.stopPropagation(); deleteNote(note.id); }}
              >
                ×
              </button>
            </div>
          ))}
          {notes.length === 0 && (
            <div style={styles.empty}>No notes yet. Click + New to create one.</div>
          )}
        </div>
      </div>
      <div style={styles.editor}>
        {selected ? (
          <>
            <input
              style={styles.titleInput}
              value={editTitle}
              onChange={(e) => setEditTitle(e.target.value)}
              onBlur={saveNote}
              placeholder="Note title..."
            />
            <textarea
              style={styles.contentInput}
              value={editContent}
              onChange={(e) => setEditContent(e.target.value)}
              onBlur={saveNote}
              placeholder="Start typing..."
            />
            <div style={styles.saveHint}>Changes saved automatically</div>
          </>
        ) : (
          <div style={styles.placeholder}>Select a note or create a new one</div>
        )}
      </div>
    </div>
  );
}

const styles: Record<string, React.CSSProperties> = {
  container: {
    display: 'flex',
    minHeight: '100vh',
    background: '#0f0f0f',
    fontFamily: 'system-ui, sans-serif',
    color: '#fff',
  },
  sidebar: { width: 280, background: '#141414', borderRight: '1px solid #222', display: 'flex', flexDirection: 'column' },
  sidebarHeader: { padding: 20, display: 'flex', justifyContent: 'space-between', alignItems: 'center' },
  title: { fontSize: 20, fontWeight: 700, color: '#e0e0e0' },
  addBtn: {
    padding: '8px 16px',
    fontSize: 14,
    fontWeight: 600,
    border: 'none',
    borderRadius: 6,
    cursor: 'pointer',
    background: '#22c55e',
    color: '#0f0f0f',
  },
  list: { flex: 1, overflowY: 'auto', padding: '0 12px 12px' },
  noteItem: {
    padding: 12,
    borderRadius: 8,
    marginBottom: 8,
    cursor: 'pointer',
    background: '#1a1a1a',
    position: 'relative',
    transition: 'background 0.15s',
  },
  noteItemActive: { background: '#222' },
  noteTitle: { fontSize: 14, fontWeight: 600, marginBottom: 4, color: '#e0e0e0' },
  notePreview: { fontSize: 12, color: '#666', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' },
  deleteBtn: {
    position: 'absolute',
    top: 8,
    right: 8,
    width: 20,
    height: 20,
    border: 'none',
    borderRadius: 4,
    cursor: 'pointer',
    background: '#333',
    color: '#888',
    fontSize: 14,
    lineHeight: 1,
  },
  empty: { padding: 20, textAlign: 'center', color: '#555', fontSize: 14 },
  editor: { flex: 1, display: 'flex', flexDirection: 'column', padding: 32 },
  titleInput: {
    fontSize: 28,
    fontWeight: 700,
    border: 'none',
    background: 'transparent',
    color: '#e0e0e0',
    outline: 'none',
    marginBottom: 16,
  },
  contentInput: {
    flex: 1,
    fontSize: 16,
    lineHeight: 1.7,
    border: 'none',
    background: 'transparent',
    color: '#ccc',
    outline: 'none',
    resize: 'none',
  },
  saveHint: { fontSize: 12, color: '#555', marginTop: 8 },
  placeholder: { display: 'flex', alignItems: 'center', justifyContent: 'center', height: '100%', color: '#444', fontSize: 16 },
};
