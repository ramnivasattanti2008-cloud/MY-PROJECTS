import { useState, useEffect, useMemo } from 'react'

type Category = 'all' | 'work' | 'personal' | 'shopping' | 'health'

interface Todo {
  id: string
  text: string
  category: Exclude<Category, 'all'>
  completed: boolean
  createdAt: number
}

const STORAGE_KEY = 'react-todo-todos'

function App() {
  const [todos, setTodos] = useState<Todo[]>([])
  const [input, setInput] = useState('')
  const [category, setCategory] = useState<Exclude<Category, 'all'>>('work')
  const [filter, setFilter] = useState<Category>('all')
  const [isDarkMode, setIsDarkMode] = useState(true)

  // Load from localStorage
  useEffect(() => {
    const saved = localStorage.getItem(STORAGE_KEY)
    if (saved) {
      try {
        setTodos(JSON.parse(saved))
      } catch {
        console.error('Failed to parse saved todos')
      }
    }
  }, [])

  // Save to localStorage
  useEffect(() => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(todos))
  }, [todos])

  const addTodo = () => {
    if (!input.trim()) return
    const newTodo: Todo = {
      id: Date.now().toString(),
      text: input.trim(),
      category,
      completed: false,
      createdAt: Date.now(),
    }
    setTodos((prev) => [newTodo, ...prev])
    setInput('')
  }

  const toggleTodo = (id: string) => {
    setTodos((prev) =>
      prev.map((todo) =>
        todo.id === id ? { ...todo, completed: !todo.completed } : todo
      )
    )
  }

  const deleteTodo = (id: string) => {
    setTodos((prev) => prev.filter((todo) => todo.id !== id))
  }

  const editTodo = (id: string, newText: string) => {
    if (!newText.trim()) return
    setTodos((prev) =>
      prev.map((todo) =>
        todo.id === id ? { ...todo, text: newText.trim() } : todo
      )
    )
  }

  const filteredTodos = useMemo(() => {
    if (filter === 'all') return todos
    return todos.filter((todo) => todo.category === filter)
  }, [todos, filter])

  const completedCount = todos.filter((t) => t.completed).length
  const totalCount = todos.length

  const categoryColors: Record<Exclude<Category, 'all'>, string> = {
    work: '#3b82f6',
    personal: '#8b5cf6',
    shopping: '#f59e0b',
    health: '#10b981',
  }

  const theme = isDarkMode ? darkTheme : lightTheme

  return (
    <div style={theme.container}>
      <div style={theme.card}>
        <div style={theme.header}>
          <h1 style={theme.title}>Todo App</h1>
          <button
            onClick={() => setIsDarkMode(!isDarkMode)}
            style={theme.themeToggle}
          >
            {isDarkMode ? 'Light' : 'Dark'}
          </button>
        </div>

        <div style={theme.inputContainer}>
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && addTodo()}
            placeholder="Add a new todo..."
            style={theme.input}
          />
          <select
            value={category}
            onChange={(e) => setCategory(e.target.value as Exclude<Category, 'all'>)}
            style={theme.select}
          >
            <option value="work">Work</option>
            <option value="personal">Personal</option>
            <option value="shopping">Shopping</option>
            <option value="health">Health</option>
          </select>
          <button onClick={addTodo} style={theme.addButton}>
            Add
          </button>
        </div>

        <div style={theme.filters}>
          {(['all', 'work', 'personal', 'shopping', 'health'] as Category[]).map((cat) => (
            <button
              key={cat}
              onClick={() => setFilter(cat)}
              style={{
                ...theme.filterButton,
                ...(filter === cat ? theme.filterButtonActive : {}),
              }}
            >
              {cat.charAt(0).toUpperCase() + cat.slice(1)}
            </button>
          ))}
        </div>

        <div style={theme.stats}>
          {completedCount} of {totalCount} completed
        </div>

        <div style={theme.todoList}>
          {filteredTodos.length === 0 ? (
            <div style={theme.emptyState}>
              {filter === 'all' ? 'No todos yet. Add one above!' : `No ${filter} todos.`}
            </div>
          ) : (
            filteredTodos.map((todo) => (
              <div
                key={todo.id}
                style={{
                  ...theme.todoItem,
                  ...(todo.completed ? theme.todoItemCompleted : {}),
                }}
              >
                <input
                  type="checkbox"
                  checked={todo.completed}
                  onChange={() => toggleTodo(todo.id)}
                  style={theme.checkbox}
                />
                <span
                  style={{
                    ...theme.todoText,
                    ...(todo.completed ? theme.todoTextCompleted : {}),
                  }}
                  onDoubleClick={() => {
                    const newText = prompt('Edit todo:', todo.text)
                    if (newText) editTodo(todo.id, newText)
                  }}
                >
                  {todo.text}
                </span>
                <span
                  style={{
                    ...theme.categoryBadge,
                    backgroundColor: categoryColors[todo.category],
                  }}
                >
                  {todo.category}
                </span>
                <button
                  onClick={() => deleteTodo(todo.id)}
                  style={theme.deleteButton}
                >
                  Delete
                </button>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  )
}

const darkTheme: Record<string, React.CSSProperties> = {
  container: {
    minHeight: '100vh',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#0f172a',
    fontFamily: "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
    padding: '20px',
  },
  card: {
    backgroundColor: '#1e293b',
    borderRadius: '20px',
    padding: '32px',
    width: '100%',
    maxWidth: '500px',
    boxShadow: '0 20px 60px rgba(0, 0, 0, 0.5)',
  },
  header: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: '24px',
  },
  title: {
    color: '#f1f5f9',
    fontSize: '28px',
    fontWeight: 700,
    margin: 0,
  },
  themeToggle: {
    padding: '8px 16px',
    backgroundColor: '#334155',
    color: '#f1f5f9',
    border: 'none',
    borderRadius: '8px',
    cursor: 'pointer',
    fontSize: '14px',
  },
  inputContainer: {
    display: 'flex',
    gap: '10px',
    marginBottom: '20px',
  },
  input: {
    flex: 1,
    padding: '12px 16px',
    backgroundColor: '#334155',
    color: '#f1f5f9',
    border: '2px solid #475569',
    borderRadius: '10px',
    fontSize: '16px',
    outline: 'none',
  },
  select: {
    padding: '12px 16px',
    backgroundColor: '#334155',
    color: '#f1f5f9',
    border: '2px solid #475569',
    borderRadius: '10px',
    fontSize: '14px',
    cursor: 'pointer',
  },
  addButton: {
    padding: '12px 24px',
    backgroundColor: '#3b82f6',
    color: '#ffffff',
    border: 'none',
    borderRadius: '10px',
    fontSize: '16px',
    fontWeight: 600,
    cursor: 'pointer',
  },
  filters: {
    display: 'flex',
    gap: '8px',
    marginBottom: '16px',
    flexWrap: 'wrap' as const,
  },
  filterButton: {
    padding: '8px 16px',
    backgroundColor: '#334155',
    color: '#94a3b8',
    border: 'none',
    borderRadius: '20px',
    fontSize: '14px',
    cursor: 'pointer',
    transition: 'all 0.2s',
  },
  filterButtonActive: {
    backgroundColor: '#3b82f6',
    color: '#ffffff',
  },
  stats: {
    color: '#64748b',
    fontSize: '14px',
    marginBottom: '16px',
  },
  todoList: {
    display: 'flex',
    flexDirection: 'column' as const,
    gap: '10px',
  },
  emptyState: {
    color: '#64748b',
    textAlign: 'center' as const,
    padding: '40px',
    fontSize: '16px',
  },
  todoItem: {
    display: 'flex',
    alignItems: 'center',
    gap: '12px',
    padding: '16px',
    backgroundColor: '#334155',
    borderRadius: '12px',
    transition: 'opacity 0.2s',
  },
  todoItemCompleted: {
    opacity: 0.6,
  },
  checkbox: {
    width: '20px',
    height: '20px',
    cursor: 'pointer',
  },
  todoText: {
    flex: 1,
    color: '#f1f5f9',
    fontSize: '16px',
  },
  todoTextCompleted: {
    textDecoration: 'line-through',
    color: '#64748b',
  },
  categoryBadge: {
    padding: '4px 12px',
    borderRadius: '12px',
    color: '#ffffff',
    fontSize: '12px',
    fontWeight: 500,
    textTransform: 'capitalize' as const,
  },
  deleteButton: {
    padding: '6px 12px',
    backgroundColor: '#ef4444',
    color: '#ffffff',
    border: 'none',
    borderRadius: '6px',
    fontSize: '12px',
    cursor: 'pointer',
  },
}

const lightTheme: Record<string, React.CSSProperties> = {
  ...darkTheme,
  container: {
    ...darkTheme.container,
    backgroundColor: '#f1f5f9',
  },
  card: {
    ...darkTheme.card,
    backgroundColor: '#ffffff',
  },
  title: {
    ...darkTheme.title,
    color: '#1e293b',
  },
  themeToggle: {
    ...darkTheme.themeToggle,
    backgroundColor: '#e2e8f0',
    color: '#1e293b',
  },
  input: {
    ...darkTheme.input,
    backgroundColor: '#f8fafc',
    color: '#1e293b',
    borderColor: '#cbd5e1',
  },
  select: {
    ...darkTheme.select,
    backgroundColor: '#f8fafc',
    color: '#1e293b',
    borderColor: '#cbd5e1',
  },
  filterButton: {
    ...darkTheme.filterButton,
    backgroundColor: '#e2e8f0',
    color: '#64748b',
  },
  todoItem: {
    ...darkTheme.todoItem,
    backgroundColor: '#f8fafc',
  },
  todoText: {
    ...darkTheme.todoText,
    color: '#1e293b',
  },
}

export default App
