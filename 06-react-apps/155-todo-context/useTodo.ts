/**
 * useTodo Hook - Alternative hook-based API for Todo functionality
 *
 * This is an alternative API if you prefer hooks over Context.
 * You can import either the hook or the context - they provide the same functionality.
 */

import { useState, useEffect, useCallback, useMemo } from 'react';
import { Todo, TodoFilter } from './TodoContext';

const STORAGE_KEY = 'vojas-todos-v1';

interface UseTodoReturn {
  todos: Todo[];
  filteredTodos: Todo[];
  filter: TodoFilter;
  isLoading: boolean;
  addTodo: (text: string) => void;
  deleteTodo: (id: string) => void;
  toggleTodo: (id: string) => void;
  updateTodo: (id: string, text: string) => void;
  clearCompleted: () => void;
  setFilter: (filter: TodoFilter) => void;
  stats: {
    total: number;
    active: number;
    completed: number;
  };
}

export function useTodo(storageKey: string = STORAGE_KEY): UseTodoReturn {
  const [todos, setTodos] = useState<Todo[]>([]);
  const [filter, setFilter] = useState<TodoFilter>('all');
  const [isLoading, setIsLoading] = useState(true);

  // Load from localStorage
  useEffect(() => {
    try {
      const stored = localStorage.getItem(storageKey);
      if (stored) {
        const parsed = JSON.parse(stored);
        const loadedTodos = parsed.todos.map((todo: Todo) => ({
          ...todo,
          createdAt: new Date(todo.createdAt),
          updatedAt: new Date(todo.updatedAt),
        }));
        setTodos(loadedTodos);
        if (parsed.filter) {
          setFilter(parsed.filter);
        }
      }
    } catch (error) {
      console.warn('Failed to load todos:', error);
    } finally {
      setIsLoading(false);
    }
  }, [storageKey]);

  // Save to localStorage
  useEffect(() => {
    if (!isLoading) {
      try {
        localStorage.setItem(storageKey, JSON.stringify({ todos, filter }));
      } catch (error) {
        console.warn('Failed to save todos:', error);
      }
    }
  }, [todos, filter, storageKey, isLoading]);

  // Computed values
  const filteredTodos = useMemo(() => {
    return todos.filter((todo) => {
      switch (filter) {
        case 'active':
          return !todo.completed;
        case 'completed':
          return todo.completed;
        default:
          return true;
      }
    });
  }, [todos, filter]);

  const stats = useMemo(() => ({
    total: todos.length,
    active: todos.filter((t) => !t.completed).length,
    completed: todos.filter((t) => t.completed).length,
  }), [todos]);

  // Actions
  const addTodo = useCallback((text: string) => {
    if (!text.trim()) return;

    const newTodo: Todo = {
      id: `todo-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
      text: text.trim(),
      completed: false,
      createdAt: new Date(),
      updatedAt: new Date(),
    };

    setTodos((prev) => [newTodo, ...prev]);
  }, []);

  const deleteTodo = useCallback((id: string) => {
    setTodos((prev) => prev.filter((todo) => todo.id !== id));
  }, []);

  const toggleTodo = useCallback((id: string) => {
    setTodos((prev) =>
      prev.map((todo) =>
        todo.id === id
          ? { ...todo, completed: !todo.completed, updatedAt: new Date() }
          : todo
      )
    );
  }, []);

  const updateTodo = useCallback((id: string, text: string) => {
    if (!text.trim()) return;

    setTodos((prev) =>
      prev.map((todo) =>
        todo.id === id
          ? { ...todo, text: text.trim(), updatedAt: new Date() }
          : todo
      )
    );
  }, []);

  const clearCompleted = useCallback(() => {
    setTodos((prev) => prev.filter((todo) => !todo.completed));
  }, []);

  return {
    todos,
    filteredTodos,
    filter,
    isLoading,
    addTodo,
    deleteTodo,
    toggleTodo,
    updateTodo,
    clearCompleted,
    setFilter,
    stats,
  };
}

export default useTodo;
