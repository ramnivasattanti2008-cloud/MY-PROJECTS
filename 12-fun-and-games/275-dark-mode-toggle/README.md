# Dark Mode Toggle Component

A beautiful, animated dark/light mode toggle switch with smooth transitions, stars animation, and sun/moon icons.

## Features

- Smooth animated transition between dark and light modes
- Twinkling stars animation in dark mode
- Sun rays animation in light mode
- Persists theme preference to localStorage
- Respects system preference by default
- Accessible with keyboard support
- Multiple sizes (small, medium, large)

## Installation

Copy `DarkModeToggle.tsx` into your React/Next.js project.

## Usage

### Basic Usage

```tsx
import DarkModeToggle from '@/components/DarkModeToggle';

function App() {
  return (
    <div>
      <DarkModeToggle />
    </div>
  );
}
```

### With Callback

```tsx
import DarkModeToggle from '@/components/DarkModeToggle';

function App() {
  const handleToggle = (isDark: boolean) => {
    console.log(`Dark mode: ${isDark}`);
    // Custom logic here
  };

  return (
    <div>
      <DarkModeToggle onToggle={handleToggle} />
    </div>
  );
}
```

### Starting in Dark Mode

```tsx
<DarkModeToggle defaultDark={true} />
```

### Different Sizes

```tsx
// Small
<DarkModeToggle size="small" />

// Medium (default)
<DarkModeToggle size="medium" />

// Large
<DarkModeToggle size="large" />
```

## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `onToggle` | `(isDark: boolean) => void` | - | Callback when toggle changes |
| `defaultDark` | `boolean` | `false` | Initial state |
| `size` | `'small' \| 'medium' \| 'large'` | `'medium'` | Toggle size |

## Theme Integration

The component automatically:
1. Saves theme preference to `localStorage` under key `'theme'`
2. Sets `data-theme` attribute on `document.documentElement`
3. Adds/removes `dark-mode` class on `document.body`

Check the theme in CSS:

```css
/* Light mode styles */
:root {
  --bg-color: #ffffff;
  --text-color: #333333;
}

/* Dark mode styles */
:root[data-theme="dark"],
body.dark-mode {
  --bg-color: #1a1a2e;
  --text-color: #ffffff;
}
```

## Accessibility

- Uses `role="switch"` for semantic meaning
- `aria-checked` reflects current state
- `aria-label` provides context
- Fully keyboard accessible (Tab, Enter, Space)

## Demo

The toggle shows:
- **Light mode**: Golden sun with radiating rays, warm gradient background
- **Dark mode**: Crescent moon icon, starry sky with twinkling animation
