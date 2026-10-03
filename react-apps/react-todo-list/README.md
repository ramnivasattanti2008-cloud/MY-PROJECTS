# React Todo List

A polished, feature-rich Todo List React component with local storage persistence.

## Features

- Add, edit, and delete tasks
- Mark tasks as complete/incomplete
- Priority levels (Low, Medium, High) with color coding
- Category organization
- Filter by status (All, Active, Completed)
- Filter by category
- Local storage persistence
- Clean, modern UI
- Responsive design

## Installation

```bash
npm install
```

## Usage

### Basic Usage

```tsx
import { TodoList } from './TodoList';

function App() {
  return <TodoList />;
}
```

### With Custom Categories

```tsx
import { TodoList } from './TodoList';

function App() {
  return (
    <TodoList
      categories={['Personal', 'Work', 'Shopping', 'Health']}
      defaultCategory="Work"
      storageKey="my-todos"
    />
  );
}
```

### In Your React App

```tsx
// App.tsx
import { TodoList } from './components/TodoList';

function App() {
  return (
    <div>
      <h1>My App</h1>
      <TodoList />
    </div>
  );
}
```

## API

### Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `storageKey` | `string` | `'react-todo-list'` | Key for localStorage |
| `categories` | `string[]` | `['Personal', 'Work', 'Shopping', 'Health', 'Ideas']` | Available categories |
| `defaultCategory` | `string` | `'Personal'` | Default category for new todos |

### Todo Object Structure

```typescript
interface Todo {
  id: string;           // Unique identifier
  text: string;         // Todo text
  completed: boolean;   // Completion status
  priority: 'low' | 'medium' | 'high';
  category: string;
  createdAt: number;     // Unix timestamp
  completedAt?: number;  // When completed
}
```

## Features Explained

### Adding Tasks
- Type your task in the input field
- Select a category from the dropdown
- Press Enter or click the + button

### Editing Tasks
- Click the pencil icon on any task
- Modify the text
- Press Enter to save, Escape to cancel

### Priority Levels
- **Low** (green) - Non-urgent tasks
- **Medium** (yellow) - Normal priority
- **High** (red) - Urgent tasks

### Filtering
- **All** - Show all tasks
- **Active** - Show incomplete tasks
- **Completed** - Show completed tasks

### Categories
Organize tasks by:
- Personal
- Work
- Shopping
- Health
- Ideas

### Data Persistence
All tasks are saved to localStorage automatically. Data persists across browser sessions.

## Styling

The component uses inline styles for portability. To customize:

```tsx
// Custom container style
<div style={{ maxWidth: '800px', margin: '0 auto', background: '#f0f0f0' }}>
  <TodoList />
</div>
```

## Browser Support

Works in all modern browsers that support:
- React 18+
- localStorage
- ES6+ features
