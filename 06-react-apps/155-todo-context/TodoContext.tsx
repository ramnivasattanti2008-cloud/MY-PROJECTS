'use client';

import React, { createContext, useContext, useReducer, useEffect, ReactNode } from 'react';

// Types
export interface Todo {
  id: string;
  text: string;
  completed: boolean;
  createdAt: Date;
  updatedAt: Date;
}

export type TodoFilter = 'all' | 'active' | 'completed';

interface TodoState {
  todos: Todo[];
  filter: TodoFilter;
}

type TodoAction =
  | { type: 'ADD_TODO'; payload: { text: string } }
  | { type: 'DELETE_TODO'; payload: { id: string } }
  | { type: 'TOGGLE_TODO'; payload: { id: string } }
  | { type: 'UPDATE_TODO'; payload: { id: string; text: string } }
  | { type: 'CLEAR_COMPLETED' }
  | { type: 'SET_FILTER'; payload: { filter: TodoFilter } }
  | { type: 'LOAD_TODOS'; payload: { todos: Todo[] } };

// Storage key
const STORAGE_KEY = 'vojas-todos-v1';

// Reducer
const todoReducer = (state: TodoState, action: TodoAction): TodoState => {
  switch (action.type) {
    case 'ADD_TODO': {
      const newTodo: Todo = {
        id: `todo-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
        text: action.payload.text.trim(),
        completed: false,
        createdAt: new Date(),
        updatedAt: new Date(),
      };
      return {
        ...state,
        todos: [newTodo, ...state.todos],
      };
    }

    case 'DELETE_TODO':
      return {
        ...state,
        todos: state.todos.filter((todo) => todo.id !== action.payload.id),
      };

    case 'TOGGLE_TODO':
      return {
        ...state,
        todos: state.todos.map((todo) =>
          todo.id === action.payload.id
            ? { ...todo, completed: !todo.completed, updatedAt: new Date() }
            : todo
        ),
      };

    case 'UPDATE_TODO':
      return {
        ...state,
        todos: state.todos.map((todo) =>
          todo.id === action.payload.id
            ? { ...todo, text: action.payload.text.trim(), updatedAt: new Date() }
            : todo
        ),
      };

    case 'CLEAR_COMPLETED':
      return {
        ...state,
        todos: state.todos.filter((todo) => !todo.completed),
      };

    case 'SET_FILTER':
      return {
        ...state,
        filter: action.payload.filter,
      };

    case 'LOAD_TODOS':
      return {
        ...state,
        todos: action.payload.todos,
      };

    default:
      return state;
  }
};

// Initial state
const initialState: TodoState = {
  todos: [],
  filter: 'all',
};

// Context
interface TodoContextType {
  todos: Todo[];
  filteredTodos: Todo[];
  filter: TodoFilter;
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

const TodoContext = createContext<TodoContextType | undefined>(undefined);

// Provider
interface TodoProviderProps {
  children: ReactNode;
  storageKey?: string;
}

export const TodoProvider: React.FC<TodoProviderProps> = ({
  children,
  storageKey = STORAGE_KEY,
}) => {
  const [state, dispatch] = useReducer(todoReducer, initialState);

  // Load from localStorage on mount
  useEffect(() => {
    try {
      const stored = localStorage.getItem(storageKey);
      if (stored) {
        const parsed = JSON.parse(stored);
        const todos = parsed.todos.map((todo: Todo) => ({
          ...todo,
          createdAt: new Date(todo.createdAt),
          updatedAt: new Date(todo.updatedAt),
        }));
        dispatch({ type: 'LOAD_TODOS', payload: { todos } });
        if (parsed.filter) {
          dispatch({ type: 'SET_FILTER', payload: { filter: parsed.filter } });
        }
      }
    } catch (error) {
      console.warn('Failed to load todos from storage:', error);
    }
  }, [storageKey]);

  // Save to localStorage on change
  useEffect(() => {
    try {
      localStorage.setItem(
        storageKey,
        JSON.stringify({ todos: state.todos, filter: state.filter })
      );
    } catch (error) {
      console.warn('Failed to save todos to storage:', error);
    }
  }, [state, storageKey]);

  // Computed values
  const filteredTodos = state.todos.filter((todo) => {
    switch (state.filter) {
      case 'active':
        return !todo.completed;
      case 'completed':
        return todo.completed;
      default:
        return true;
    }
  });

  const stats = {
    total: state.todos.length,
    active: state.todos.filter((t) => !t.completed).length,
    completed: state.todos.filter((t) => t.completed).length,
  };

  // Actions
  const addTodo = (text: string) => {
    if (text.trim()) {
      dispatch({ type: 'ADD_TODO', payload: { text } });
    }
  };

  const deleteTodo = (id: string) => {
    dispatch({ type: 'DELETE_TODO', payload: { id } });
  };

  const toggleTodo = (id: string) => {
    dispatch({ type: 'TOGGLE_TODO', payload: { id } });
  };

  const updateTodo = (id: string, text: string) => {
    if (text.trim()) {
      dispatch({ type: 'UPDATE_TODO', payload: { id, text } });
    }
  };

  const clearCompleted = () => {
    dispatch({ type: 'CLEAR_COMPLETED' });
  };

  const setFilter = (filter: TodoFilter) => {
    dispatch({ type: 'SET_FILTER', payload: { filter } });
  };

  const value: TodoContextType = {
    todos: state.todos,
    filteredTodos,
    filter: state.filter,
    addTodo,
    deleteTodo,
    toggleTodo,
    updateTodo,
    clearCompleted,
    setFilter,
    stats,
  };

  return <TodoContext.Provider value={value}>{children}</TodoContext.Provider>;
};

// Hook
export const useTodoContext = (): TodoContextType => {
  const context = useContext(TodoContext);
  if (!context) {
    throw new Error('useTodoContext must be used within a TodoProvider');
  }
  return context;
};

export default TodoContext;
