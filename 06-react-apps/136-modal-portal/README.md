# Modal Portal Component

A fully-featured modal component with React Portal, backdrop, focus trap, and keyboard support.

## Features

- **React Portal**: Renders at document body level
- **Focus Trap**: Keeps keyboard focus within modal
- **Backdrop Click**: Closes modal when clicking outside
- **ESC Key**: Closes modal on Escape press
- **Scroll Lock**: Prevents background scrolling
- **Keyboard Navigation**: Tab/Shift+Tab cycle through focusable elements
- **Size Variants**: small, medium, large, fullscreen
- **Customizable**: Header, body, footer slots
- **Animations**: Smooth fade and slide animations

## Installation

Copy the following files into your project:
- `Modal.tsx` - The modal component
- `useModal.ts` - Helper hooks (optional but recommended)

## Usage

### Basic Usage

```tsx
import Modal from '@/components/Modal';
import { useModal } from '@/components/useModal';

function Example() {
  const { isOpen, open, close } = useModal();

  return (
    <>
      <button onClick={open}>Open Modal</button>
      
      <Modal isOpen={isOpen} onClose={close}>
        <p>This is a modal!</p>
      </Modal>
    </>
  );
}
```

### With Title and Footer

```tsx
<Modal
  isOpen={isOpen}
  onClose={close}
  title="Confirm Action"
  footer={
    <>
      <button onClick={close}>Cancel</button>
      <button onClick={handleConfirm}>Confirm</button>
    </>
  }
>
  <p>Are you sure you want to proceed?</p>
</Modal>
```

### Different Sizes

```tsx
// Small (400px)
<Modal isOpen={isOpen} onClose={close} size="small">
  <p>Small modal</p>
</Modal>

// Medium (560px) - default
<Modal isOpen={isOpen} onClose={close} size="medium">
  <p>Medium modal</p>
</Modal>

// Large (720px)
<Modal isOpen={isOpen} onClose={close} size="large">
  <p>Large modal</p>
</Modal>

// Fullscreen
<Modal isOpen={isOpen} onClose={close} size="fullscreen">
  <p>Fullscreen modal</p>
</Modal>
```

### With Form

```tsx
function FormModal() {
  const { isOpen, open, close } = useModal();

  return (
    <>
      <button onClick={open}>Add Item</button>
      
      <Modal
        isOpen={isOpen}
        onClose={close}
        title="Add New Item"
        footer={
          <>
            <button onClick={close}>Cancel</button>
            <button onClick={handleSubmit} style={{ background: '#667eea', color: '#fff' }}>
              Add
            </button>
          </>
        }
      >
        <form onSubmit={handleSubmit}>
          <div style={{ marginBottom: '16px' }}>
            <label style={{ display: 'block', marginBottom: '4px' }}>Name</label>
            <input type="text" required style={inputStyle} />
          </div>
          <div style={{ marginBottom: '16px' }}>
            <label style={{ display: 'block', marginBottom: '4px' }}>Email</label>
            <input type="email" required style={inputStyle} />
          </div>
        </form>
      </Modal>
    </>
  );
}
```

### Multiple Modals (Modal Group)

```tsx
import { useModalGroup } from './useModal';

function MultiModalExample() {
  const { isOpen, open, close } = useModalGroup();

  return (
    <>
      <button onClick={() => open('edit')}>Edit Profile</button>
      <button onClick={() => open('settings')}>Settings</button>
      
      <Modal isOpen={isOpen('edit')} onClose={() => close('edit')} title="Edit Profile">
        {/* Edit form */}
      </Modal>
      
      <Modal isOpen={isOpen('settings')} onClose={() => close('settings')} title="Settings">
        {/* Settings */}
      </Modal>
    </>
  );
}
```

## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `isOpen` | `boolean` | **required** | Whether modal is visible |
| `onClose` | `() => void` | **required** | Close handler |
| `children` | `ReactNode` | - | Modal content |
| `title` | `string` | - | Header title |
| `footer` | `ReactNode` | - | Footer content (buttons) |
| `size` | `'small' \| 'medium' \| 'large' \| 'fullscreen'` | `'medium'` | Modal size |
| `closeOnBackdrop` | `boolean` | `true` | Close on backdrop click |
| `closeOnEscape` | `boolean` | `true` | Close on ESC key |
| `showCloseButton` | `boolean` | `true` | Show X button in header |
| `className` | `string` | - | CSS class for modal |
| `style` | `CSSProperties` | - | Modal container styles |
| `titleStyle` | `CSSProperties` | - | Title styles |
| `bodyStyle` | `CSSProperties` | - | Body styles |
| `footerStyle` | `CSSProperties` | - | Footer styles |
| `backdropStyle` | `CSSProperties` | - | Backdrop styles |

## useModal Hook

```tsx
import { useModal } from '@/components/useModal';

const { isOpen, open, close, toggle } = useModal({
  onOpen: () => console.log('Modal opened'),
  onClose: () => console.log('Modal closed'),
  defaultOpen: false,
});
```

### useModal Options

| Option | Type | Description |
|--------|------|-------------|
| `onOpen` | `() => void` | Callback when modal opens |
| `onClose` | `() => void` | Callback when modal closes |
| `defaultOpen` | `boolean` | Initial state (default: false) |

### useModal Return

| Property | Type | Description |
|----------|------|-------------|
| `isOpen` | `boolean` | Current open state |
| `open` | `() => void` | Open the modal |
| `close` | `() => void` | Close the modal |
| `toggle` | `() => void` | Toggle open/close |

## useModalGroup Hook

For managing multiple modals:

```tsx
const { isOpen, open, close, closeAll, activeModal } = useModalGroup({
  onOpen: (key) => console.log('Opened:', key),
  onClose: (key) => console.log('Closed:', key),
});

// Check if specific modal is open
isOpen('edit') // boolean

// Open/close specific modal
open('edit');
close('settings');
closeAll();
```

## Accessibility

- Uses `role="dialog"` and `aria-modal="true"`
- Focus is trapped within modal
- ESC key closes modal
- Body scroll is locked when open
- Previous focus is restored on close

## How It Works

1. **Portal**: Uses `ReactDOM.createPortal` to render at `document.body`
2. **Focus Trap**: Queries all focusable elements and manages Tab navigation
3. **Scroll Lock**: Sets `overflow: hidden` on body, accounting for scrollbar width
4. **Escape Handler**: Listens for keydown events at document level
5. **Backdrop**: Click handler on backdrop div checks if target equals currentTarget

## Custom Styling

Override any style by passing CSSProperties:

```tsx
<Modal
  isOpen={isOpen}
  onClose={close}
  style={{ backgroundColor: '#f0f0f0' }}
  titleStyle={{ color: '#333' }}
  bodyStyle={{ padding: '32px' }}
  footerStyle={{ backgroundColor: '#e0e0e0' }}
  backdropStyle={{ backgroundColor: 'rgba(0,0,0,0.8)' }}
>
  {children}
</Modal>
```
