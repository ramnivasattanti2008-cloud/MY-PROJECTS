import React, { useState, useEffect, useRef } from 'react';

// Types
interface Todo {
  id: string;
  text: string;
  completed: boolean;
  priority: 'low' | 'medium' | 'high';
  category: string;
  createdAt: number;
  completedAt?: number;
}

interface TodoListProps {
  storageKey?: string;
  categories?: string[];
  defaultCategory?: string;
}

const DEFAULT_CATEGORIES = ['Personal', 'Work', 'Shopping', 'Health', 'Ideas'];

const PRIORITY_CONFIG = {
  low: { label: 'Low', color: '#10b981', bgColor: 'rgba(16, 185, 129, 0.1)' },
  medium: { label: 'Medium', color: '#f59e0b', bgColor: 'rgba(245, 158, 11, 0.1)' },
  high: { label: 'High', color: '#ef4444', bgColor: 'rgba(239, 68, 68, 0.1)' },
};

// Generate unique ID
const generateId = () => Math.random().toString(36).substring(2, 9);

// Icons
const icons = {
  check: '✓',
  trash: '🗑️',
  edit: '✏️',
  add: '+',
  filter: '⚡',
  category: '📁',
};

export const TodoList: React.FC<TodoListProps> = ({
  storageKey = 'react-todo-list',
  categories = DEFAULT_CATEGORIES,
  defaultCategory = 'Personal',
}) => {
  // State
  const [todos, setTodos] = useState<Todo[]>([]);
  const [input, setInput] = useState('');
  const [editingId, setEditingId] = useState<string | null>(null);
  const [editText, setEditText] = useState('');
  const [filter, setFilter] = useState<'all' | 'active' | 'completed'>('all');
  const [selectedCategory, setSelectedCategory] = useState(defaultCategory);
  const [showCompleted, setShowCompleted] = useState(true);
  const inputRef = useRef<HTMLInputElement>(null);

  // Load from localStorage
  useEffect(() => {
    try {
      const saved = localStorage.getItem(storageKey);
      if (saved) {
        setTodos(JSON.parse(saved));
      }
    } catch (e) {
      console.error('Failed to load todos:', e);
    }
  }, [storageKey]);

  // Save to localStorage
  useEffect(() => {
    try {
      localStorage.setItem(storageKey, JSON.stringify(todos));
    } catch (e) {
      console.error('Failed to save todos:', e);
    }
  }, [todos, storageKey]);

  // Add todo
  const addTodo = (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;

    const newTodo: Todo = {
      id: generateId(),
      text: input.trim(),
      completed: false,
      priority: 'medium',
      category: selectedCategory,
      createdAt: Date.now(),
    };

    setTodos((prev) => [newTodo, ...prev]);
    setInput('');
    inputRef.current?.focus();
  };

  // Toggle complete
  const toggleTodo = (id: string) => {
    setTodos((prev) =>
      prev.map((todo) =>
        todo.id === id
          ? { ...todo, completed: !todo.completed, completedAt: !todo.completed ? Date.now() : undefined }
          : todo
      )
    );
  };

  // Delete todo
  const deleteTodo = (id: string) => {
    setTodos((prev) => prev.filter((todo) => todo.id !== id));
  };

  // Start editing
  const startEdit = (todo: Todo) => {
    setEditingId(todo.id);
    setEditText(todo.text);
  };

  // Save edit
  const saveEdit = (id: string) => {
    if (!editText.trim()) return;
    setTodos((prev) =>
      prev.map((todo) => (todo.id === id ? { ...todo, text: editText.trim() } : todo))
    );
    setEditingId(null);
    setEditText('');
  };

  // Cancel edit
  const cancelEdit = () => {
    setEditingId(null);
    setEditText('');
  };

  // Update priority
  const updatePriority = (id: string, priority: Todo['priority']) => {
    setTodos((prev) => prev.map((todo) => (todo.id === id ? { ...todo, priority } : todo)));
  };

  // Filter todos
  const filteredTodos = todos
    .filter((todo) => {
      if (filter === 'active') return !todo.completed;
      if (filter === 'completed') return todo.completed;
      return true;
    })
    .filter((todo) => todo.category === selectedCategory || selectedCategory === 'All');

  // Stats
  const stats = {
    total: todos.length,
    completed: todos.filter((t) => t.completed).length,
    active: todos.filter((t) => !t.completed).length,
    byCategory: categories.reduce((acc, cat) => {
      acc[cat] = todos.filter((t) => t.category === cat && !t.completed).length;
      return acc;
    }, {} as Record<string, number>),
  };

  // Styles
  const styles = {
    container: {
      fontFamily: "'Segoe UI', system-ui, sans-serif",
      maxWidth: '600px',
      margin: '0 auto',
      padding: '24px',
      background: '#f9fafb',
      minHeight: '100vh',
    } as React.CSSProperties,
    header: {
      textAlign: 'center',
      marginBottom: '24px',
    } as React.CSSProperties,
    title: {
      fontSize: '2rem',
      fontWeight: 700,
      color: '#1f2937',
      marginBottom: '8px',
    } as React.CSSProperties,
    statsBar: {
      display: 'flex',
      justifyContent: 'center',
      gap: '24px',
      fontSize: '0.9rem',
      color: '#6b7280',
    } as React.CSSProperties,
    form: {
      display: 'flex',
      gap: '8px',
      marginBottom: '20px',
    } as React.CSSProperties,
    input: {
      flex: 1,
      padding: '12px 16px',
      borderRadius: '8px',
      border: '2px solid #e5e7eb',
      fontSize: '1rem',
      outline: 'none',
      transition: 'border-color 0.2s',
    } as React.CSSProperties,
    select: {
      padding: '12px 16px',
      borderRadius: '8px',
      border: '2px solid #e5e7eb',
      fontSize: '1rem',
      background: '#fff',
      cursor: 'pointer',
      outline: 'none',
    } as React.CSSProperties,
    button: {
      padding: '12px 20px',
      borderRadius: '8px',
      border: 'none',
      background: '#3b82f6',
      color: '#fff',
      fontSize: '1rem',
      fontWeight: 600,
      cursor: 'pointer',
      transition: 'background 0.2s',
    } as React.CSSProperties,
    controls: {
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'center',
      marginBottom: '20px',
      flexWrap: 'wrap' as const,
      gap: '12px',
    } as React.CSSProperties,
    filterButtons: {
      display: 'flex',
      gap: '8px',
    } as React.CSSProperties,
    filterBtn: {
      padding: '8px 16px',
      borderRadius: '20px',
      border: 'none',
      fontSize: '0.9rem',
      cursor: 'pointer',
      transition: 'all 0.2s',
    } as React.CSSProperties,
    categoryTabs: {
      display: 'flex',
      flexWrap: 'wrap' as const,
      gap: '8px',
      marginBottom: '20px',
    } as React.CSSProperties,
    categoryTab: {
      padding: '8px 16px',
      borderRadius: '20px',
      border: 'none',
      fontSize: '0.85rem',
      cursor: 'pointer',
      transition: 'all 0.2s',
    } as React.CSSProperties,
    todoList: {
      display: 'flex',
      flexDirection: 'column' as const,
      gap: '12px',
    } as React.CSSProperties,
    todoItem: {
      display: 'flex',
      alignItems: 'center',
      gap: '12px',
      padding: '16px',
      background: '#fff',
      borderRadius: '12px',
      boxShadow: '0 1px 3px rgba(0, 0, 0, 0.1)',
      transition: 'all 0.2s',
    } as React.CSSProperties,
    checkbox: {
      width: '24px',
      height: '24px',
      borderRadius: '50%',
      border: '2px solid #d1d5db',
      cursor: 'pointer',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      fontSize: '14px',
      transition: 'all 0.2s',
      flexShrink: 0,
    } as React.CSSProperties,
    todoText: {
      flex: 1,
      fontSize: '1rem',
      color: '#374151',
    } as React.CSSProperties,
    priorityBadge: {
      padding: '4px 10px',
      borderRadius: '12px',
      fontSize: '0.75rem',
      fontWeight: 600,
    } as React.CSSProperties,
    actions: {
      display: 'flex',
      gap: '8px',
    } as React.CSSProperties,
    actionBtn: {
      padding: '6px 10px',
      borderRadius: '6px',
      border: 'none',
      background: 'transparent',
      cursor: 'pointer',
      fontSize: '1rem',
      transition: 'background 0.2s',
    } as React.CSSProperties,
    editInput: {
      flex: 1,
      padding: '8px 12px',
      borderRadius: '6px',
      border: '2px solid #3b82f6',
      fontSize: '1rem',
      outline: 'none',
    } as React.CSSProperties,
    emptyState: {
      textAlign: 'center',
      padding: '40px',
      color: '#9ca3af',
    } as React.CSSProperties,
  };

  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <h1 style={styles.title}>My Tasks</h1>
        <div style={styles.statsBar}>
          <span>{stats.active} active</span>
          <span>{stats.completed} completed</span>
          <span>{stats.total} total</span>
        </div>
      </div>

      <form style={styles.form} onSubmit={addTodo}>
        <input
          ref={inputRef}
          type="text"
          placeholder="What needs to be done?"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          style={styles.input}
          onFocus={(e) => (e.target.style.borderColor = '#3b82f6')}
          onBlur={(e) => (e.target.style.borderColor = '#e5e7eb')}
        />
        <select
          value={selectedCategory}
          onChange={(e) => setSelectedCategory(e.target.value)}
          style={styles.select}
        >
          {categories.map((cat) => (
            <option key={cat} value={cat}>{cat}</option>
          ))}
        </select>
        <button
          type="submit"
          style={styles.button}
          onMouseOver={(e) => (e.currentTarget.style.background = '#2563eb')}
          onMouseOut={(e) => (e.currentTarget.style.background = '#3b82f6')}
        >
          {icons.add}
        </button>
      </form>

      <div style={styles.controls}>
        <div style={styles.filterButtons}>
          {(['all', 'active', 'completed'] as const).map((f) => (
            <button
              key={f}
              style={{
                ...styles.filterBtn,
                background: filter === f ? '#3b82f6' : '#e5e7eb',
                color: filter === f ? '#fff' : '#6b7280',
              }}
              onClick={() => setFilter(f)}
            >
              {f.charAt(0).toUpperCase() + f.slice(1)}
            </button>
          ))}
        </div>
        <label style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '0.9rem', color: '#6b7280' }}>
          <input
            type="checkbox"
            checked={showCompleted}
            onChange={(e) => setShowCompleted(e.target.checked)}
          />
          Show completed
        </label>
      </div>

      <div style={styles.categoryTabs}>
        {['All', ...categories].map((cat) => (
          <button
            key={cat}
            style={{
              ...styles.categoryTab,
              background: selectedCategory === cat ? '#8b5cf6' : '#fff',
              color: selectedCategory === cat ? '#fff' : '#6b7280',
            }}
            onClick={() => setSelectedCategory(cat)}
          >
            {cat} {cat !== 'All' && stats.byCategory[cat] > 0 && `(${stats.byCategory[cat]})`}
          </button>
        ))}
      </div>

      <div style={styles.todoList}>
        {filteredTodos.length === 0 ? (
          <div style={styles.emptyState}>
            {todos.length === 0 ? 'No tasks yet. Add one above!' : 'No tasks in this category.'}
          </div>
        ) : (
          filteredTodos
            .filter((todo) => showCompleted || !todo.completed)
            .map((todo) => {
              const priorityConfig = PRIORITY_CONFIG[todo.priority];
              return (
                <div
                  key={todo.id}
                  style={{
                    ...styles.todoItem,
                    opacity: todo.completed ? 0.6 : 1,
                  }}
                >
                  {editingId === todo.id ? (
                    <>
                      <input
                        type="text"
                        value={editText}
                        onChange={(e) => setEditText(e.target.value)}
                        style={styles.editInput}
                        autoFocus
                        onKeyDown={(e) => {
                          if (e.key === 'Enter') saveEdit(todo.id);
                          if (e.key === 'Escape') cancelEdit();
                        }}
                      />
                      <button
                        style={{ ...styles.actionBtn, background: '#dcfce7' }}
                        onClick={() => saveEdit(todo.id)}
                      >
                        ✓
                      </button>
                      <button
                        style={{ ...styles.actionBtn, background: '#fee2e2' }}
                        onClick={cancelEdit}
                      >
                        ✕
                      </button>
                    </>
                  ) : (
                    <>
                      <div
                        style={{
                          ...styles.checkbox,
                          background: todo.completed ? '#10b981' : 'transparent',
                          borderColor: todo.completed ? '#10b981' : '#d1d5db',
                          color: '#fff',
                        }}
                        onClick={() => toggleTodo(todo.id)}
                      >
                        {todo.completed && icons.check}
                      </div>
                      <span
                        style={{
                          ...styles.todoText,
                          textDecoration: todo.completed ? 'line-through' : 'none',
                        }}
                      >
                        {todo.text}
                      </span>
                      <select
                        value={todo.priority}
                        onChange={(e) => updatePriority(todo.id, e.target.value as Todo['priority'])}
                        style={{
                          ...styles.priorityBadge,
                          color: priorityConfig.color,
                          background: priorityConfig.bgColor,
                          border: 'none',
                          cursor: 'pointer',
                        }}
                      >
                        <option value="low">Low</option>
                        <option value="medium">Medium</option>
                        <option value="high">High</option>
                      </select>
                      <div style={styles.actions}>
                        <button
                          style={styles.actionBtn}
                          onClick={() => startEdit(todo)}
                          title="Edit"
                          onMouseOver={(e) => (e.currentTarget.style.background = '#f3f4f6')}
                          onMouseOut={(e) => (e.currentTarget.style.background = 'transparent')}
                        >
                          {icons.edit}
                        </button>
                        <button
                          style={styles.actionBtn}
                          onClick={() => deleteTodo(todo.id)}
                          title="Delete"
                          onMouseOver={(e) => (e.currentTarget.style.background = '#fee2e2')}
                          onMouseOut={(e) => (e.currentTarget.style.background = 'transparent')}
                        >
                          {icons.trash}
                        </button>
                      </div>
                    </>
                  )}
                </div>
              );
            })
        )}
      </div>
    </div>
  );
};

export default TodoList;
