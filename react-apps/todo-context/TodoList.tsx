'use client';

import React, { useState, useRef, useEffect } from 'react';
import { useTodoContext, Todo, TodoFilter } from './TodoContext';

// Styles
const styles = {
  container: {
    fontFamily: 'system-ui, -apple-system, sans-serif',
    maxWidth: '600px',
    margin: '0 auto',
    padding: '20px',
  },
  header: {
    marginBottom: '24px',
  },
  title: {
    fontSize: '28px',
    fontWeight: 700,
    marginBottom: '16px',
    color: '#1f2937',
  },
  inputContainer: {
    display: 'flex',
    gap: '8px',
    marginBottom: '24px',
  },
  input: {
    flex: 1,
    padding: '12px 16px',
    fontSize: '16px',
    border: '2px solid #e5e7eb',
    borderRadius: '12px',
    outline: 'none',
    transition: 'border-color 0.2s',
  },
  addButton: {
    padding: '12px 24px',
    fontSize: '16px',
    fontWeight: 600,
    color: '#fff',
    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    border: 'none',
    borderRadius: '12px',
    cursor: 'pointer',
    transition: 'transform 0.2s, box-shadow 0.2s',
  },
  filterContainer: {
    display: 'flex',
    gap: '8px',
    marginBottom: '16px',
  },
  filterButton: {
    padding: '8px 16px',
    fontSize: '14px',
    fontWeight: 500,
    border: '2px solid transparent',
    borderRadius: '8px',
    cursor: 'pointer',
    transition: 'all 0.2s',
  },
  filterButtonActive: {
    backgroundColor: '#667eea',
    color: '#fff',
  },
  filterButtonInactive: {
    backgroundColor: '#f3f4f6',
    color: '#6b7280',
  },
  statsContainer: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: '12px 16px',
    backgroundColor: '#f9fafb',
    borderRadius: '12px',
    marginBottom: '16px',
    fontSize: '14px',
    color: '#6b7280',
  },
  todoList: {
    display: 'flex',
    flexDirection: 'column',
    gap: '8px',
  },
  todoItem: {
    display: 'flex',
    alignItems: 'center',
    gap: '12px',
    padding: '16px',
    backgroundColor: '#fff',
    border: '1px solid #e5e7eb',
    borderRadius: '12px',
    transition: 'all 0.2s',
  },
  todoItemCompleted: {
    backgroundColor: '#f9fafb',
    borderColor: '#e5e7eb',
  },
  checkbox: {
    width: '22px',
    height: '22px',
    cursor: 'pointer',
    accentColor: '#667eea',
  },
  todoText: {
    flex: 1,
    fontSize: '16px',
    color: '#1f2937',
    wordBreak: 'break-word',
  },
  todoTextCompleted: {
    textDecoration: 'line-through',
    color: '#9ca3af',
  },
  editInput: {
    flex: 1,
    padding: '8px 12px',
    fontSize: '16px',
    border: '2px solid #667eea',
    borderRadius: '8px',
    outline: 'none',
  },
  iconButton: {
    padding: '8px',
    background: 'none',
    border: 'none',
    cursor: 'pointer',
    color: '#9ca3af',
    borderRadius: '8px',
    transition: 'all 0.2s',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
  },
  emptyState: {
    textAlign: 'center',
    padding: '40px 20px',
    color: '#9ca3af',
  },
  emptyIcon: {
    fontSize: '48px',
    marginBottom: '12px',
  },
  emptyText: {
    fontSize: '16px',
  },
};

// TodoItem Component
interface TodoItemProps {
  todo: Todo;
}

const TodoItem: React.FC<TodoItemProps> = ({ todo }) => {
  const { toggleTodo, updateTodo, deleteTodo } = useTodoContext();
  const [isEditing, setIsEditing] = useState(false);
  const [editText, setEditText] = useState(todo.text);
  const editInputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    if (isEditing && editInputRef.current) {
      editInputRef.current.focus();
    }
  }, [isEditing]);

  const handleSave = () => {
    if (editText.trim() && editText !== todo.text) {
      updateTodo(todo.id, editText);
    }
    setIsEditing(false);
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleSave();
    } else if (e.key === 'Escape') {
      setEditText(todo.text);
      setIsEditing(false);
    }
  };

  const formatDate = (date: Date) => {
    return new Date(date).toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  return (
    <div
      style={{
        ...styles.todoItem,
        ...(todo.completed ? styles.todoItemCompleted : {}),
      }}
    >
      <input
        type="checkbox"
        checked={todo.completed}
        onChange={() => toggleTodo(todo.id)}
        style={styles.checkbox}
        aria-label={`Mark "${todo.text}" as ${todo.completed ? 'incomplete' : 'complete'}`}
      />

      {isEditing ? (
        <input
          ref={editInputRef}
          type="text"
          value={editText}
          onChange={(e) => setEditText(e.target.value)}
          onBlur={handleSave}
          onKeyDown={handleKeyDown}
          style={styles.editInput}
          aria-label="Edit todo text"
        />
      ) : (
        <span
          style={{
            ...styles.todoText,
            ...(todo.completed ? styles.todoTextCompleted : {}),
          }}
          onDoubleClick={() => !todo.completed && setIsEditing(true)}
        >
          {todo.text}
        </span>
      )}

      <span style={{ fontSize: '12px', color: '#9ca3af' }}>
        {formatDate(todo.createdAt)}
      </span>

      <button
        onClick={() => setIsEditing(!isEditing)}
        style={styles.iconButton}
        aria-label="Edit todo"
        title="Edit"
      >
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7" />
          <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z" />
        </svg>
      </button>

      <button
        onClick={() => deleteTodo(todo.id)}
        style={styles.iconButton}
        aria-label="Delete todo"
        title="Delete"
      >
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <polyline points="3,6 5,6 21,6" />
          <path d="M19,6v14a2,2,0,0,1-2,2H7a2,2,0,0,1-2-2V6m3,0V4a2,2,0,0,1,2-2h4a2,2,0,0,1,2,2v2" />
        </svg>
      </button>
    </div>
  );
};

// Filter Button Component
interface FilterButtonProps {
  filter: TodoFilter;
  label: string;
  count?: number;
  active: boolean;
  onClick: () => void;
}

const FilterButton: React.FC<FilterButtonProps> = ({
  label,
  count,
  active,
  onClick,
}) => (
  <button
    onClick={onClick}
    style={{
      ...styles.filterButton,
      ...(active ? styles.filterButtonActive : styles.filterButtonInactive),
    }}
  >
    {label} {count !== undefined && `(${count})`}
  </button>
);

// Main TodoList Component
const TodoList: React.FC = () => {
  const {
    filteredTodos,
    filter,
    addTodo,
    setFilter,
    clearCompleted,
    stats,
  } = useTodoContext();
  const [inputText, setInputText] = useState('');
  const inputRef = useRef<HTMLInputElement>(null);

  const handleAddTodo = () => {
    if (inputText.trim()) {
      addTodo(inputText);
      setInputText('');
      inputRef.current?.focus();
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleAddTodo();
    }
  };

  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <h1 style={styles.title}>My Tasks</h1>
      </div>

      <div style={styles.inputContainer}>
        <input
          ref={inputRef}
          type="text"
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="What needs to be done?"
          style={styles.input}
          aria-label="New todo input"
        />
        <button
          onClick={handleAddTodo}
          style={styles.addButton}
          disabled={!inputText.trim()}
        >
          Add
        </button>
      </div>

      {stats.total > 0 && (
        <>
          <div style={styles.filterContainer}>
            <FilterButton
              filter="all"
              label="All"
              count={stats.total}
              active={filter === 'all'}
              onClick={() => setFilter('all')}
            />
            <FilterButton
              filter="active"
              label="Active"
              count={stats.active}
              active={filter === 'active'}
              onClick={() => setFilter('active')}
            />
            <FilterButton
              filter="completed"
              label="Completed"
              count={stats.completed}
              active={filter === 'completed'}
              onClick={() => setFilter('completed')}
            />
          </div>

          <div style={styles.statsContainer}>
            <span>
              {stats.active} item{stats.active !== 1 ? 's' : ''} left
            </span>
            {stats.completed > 0 && (
              <button
                onClick={clearCompleted}
                style={{
                  ...styles.iconButton,
                  color: '#ef4444',
                  fontSize: '14px',
                }}
              >
                Clear completed ({stats.completed})
              </button>
            )}
          </div>
        </>
      )}

      <div style={styles.todoList} role="list">
        {filteredTodos.length > 0 ? (
          filteredTodos.map((todo) => <TodoItem key={todo.id} todo={todo} />)
        ) : (
          <div style={styles.emptyState}>
            <div style={styles.emptyIcon}>
              {filter === 'all' ? '📝' : filter === 'active' ? '✨' : '✅'}
            </div>
            <p style={styles.emptyText}>
              {filter === 'all'
                ? 'No tasks yet. Add one above!'
                : filter === 'active'
                ? 'All tasks completed!'
                : 'No completed tasks'}
            </p>
          </div>
        )}
      </div>
    </div>
  );
};

export default TodoList;
