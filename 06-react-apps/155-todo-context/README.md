# Todo App with Context API

A complete React todo application with CRUD operations, localStorage persistence, and filter functionality.

## Features

- **Create**: Add new todos with a text input
- **Read**: View all todos with filter support
- **Update**: Edit todo text inline (double-click)
- **Delete**: Remove individual todos or clear all completed
- **Toggle**: Mark todos as complete/incomplete
- **Filter**: View all, active, or completed todos
- **Persistence**: All data saved to localStorage
- **Stats**: Shows count of total, active, and completed items

## Installation

Copy the following files into your project:
- `TodoContext.tsx` - Context provider and state management
- `TodoList.tsx` - UI components
- `useTodo.ts` - Hook-based API (optional alternative)

## Usage

### Basic Setup with Context Provider

```tsx
import { TodoProvider } from './TodoContext';
import TodoList from './TodoList';

function App() {
  return (
    <TodoProvider>
      <TodoList />
    </TodoProvider>
  );
}
```

### Using the Hook (Alternative)

```tsx
import useTodo from './useTodo';

function CustomTodoView() {
  const { todos, addTodo, toggleTodo, stats } = useTodo();
  
  return (
    <div>
      <p>Total todos: {stats.total}</p>
      {/* ...custom UI */}
    </div>
  );
}
```

### Custom Storage Key

```tsx
<TodoProvider storageKey="my-custom-todos">
  <TodoList />
</TodoProvider>
```

## Components

### TodoProvider

Wraps your app and provides todo state globally.

```tsx
<TodoProvider storageKey="optional-key">
  {children}
</TodoProvider>
```

### TodoList

The complete todo UI with input, filters, and list.

```tsx
<TodoList />
```

### useTodoContext / useTodo

Hook to access todo state and actions.

```tsx
const {
  todos,
  filteredTodos,
  filter,
  addTodo,
  deleteTodo,
  toggleTodo,
  updateTodo,
  clearCompleted,
  setFilter,
  stats,
} = useTodoContext();
```

## API

### Todo Type

```typescript
interface Todo {
  id: string;
  text: string;
  completed: boolean;
  createdAt: Date;
  updatedAt: Date;
}
```

### TodoFilter

```typescript
type TodoFilter = 'all' | 'active' | 'completed';
```

### Stats Type

```typescript
interface Stats {
  total: number;
  active: number;
  completed: number;
}
```

## Props

### TodoProvider

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `children` | `ReactNode` | - | Child components |
| `storageKey` | `string` | `'vojas-todos-v1'` | localStorage key |

## Styling

The component uses inline styles. To customize, modify the `styles` object in `TodoList.tsx` or create your own styled components using the provided structure.

### Custom Styling Example

```tsx
// Create your own styled list
const MyTodoItem = ({ todo }) => (
  <div style={{
    padding: '16px',
    borderBottom: '1px solid #eee',
    backgroundColor: todo.completed ? '#f5f5f5' : '#fff',
  }}>
    <input type="checkbox" checked={todo.completed} />
    <span>{todo.text}</span>
  </div>
);
```

## Accessibility

- Semantic HTML elements
- ARIA labels on interactive elements
- Keyboard navigation support
- Focus management for editing

## File Structure

```
todo-context/
├── TodoContext.tsx   # Context provider, reducer, types
├── TodoList.tsx     # UI components
├── useTodo.ts       # Hook-based alternative API
└── README.md        # This file
```
