# Search Autocomplete Component

A fully-featured search input with autocomplete dropdown, debounced API calls, keyboard navigation, and highlighted matches.

## Features

- Debounced search (configurable delay)
- Keyboard navigation (Arrow keys, Enter, Escape)
- Highlighted matching text
- Loading states and error handling
- Optional icons and descriptions per result
- Click outside to close
- Fully accessible (ARIA attributes)

## Installation

Copy `SearchAutocomplete.tsx` into your React/Next.js project.

## Usage

### Basic Usage

```tsx
import SearchAutocomplete, { AutocompleteItem } from '@/components/SearchAutocomplete';

function App() {
  const handleSearch = async (query: string): Promise<AutocompleteItem[]> => {
    const response = await fetch(`/api/search?q=${encodeURIComponent(query)}`);
    const data = await response.json();
    return data.results;
  };

  const handleSelect = (item: AutocompleteItem) => {
    console.log('Selected:', item);
    // Navigate or perform action
  };

  return (
    <SearchAutocomplete
      placeholder="Search for anything..."
      onSearch={handleSearch}
      onSelect={handleSelect}
    />
  );
}
```

### With Local Data

```tsx
import SearchAutocomplete, { AutocompleteItem } from '@/components/SearchAutocomplete';

// Sample data
const countries: AutocompleteItem[] = [
  { id: '1', label: 'India', description: 'South Asia', icon: '🇮🇳' },
  { id: '2', label: 'Indonesia', description: 'Southeast Asia', icon: '🇮🇩' },
  { id: '3', label: 'Ireland', description: 'Northern Europe', icon: '🇮🇪' },
];

function CountrySearch() {
  const handleSearch = async (query: string): Promise<AutocompleteItem[]> => {
    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 300));
    
    const filtered = countries.filter(c =>
      c.label.toLowerCase().includes(query.toLowerCase())
    );
    
    return filtered;
  };

  const handleSelect = (item: AutocompleteItem) => {
    alert(`You selected: ${item.label}`);
  };

  return (
    <div style={{ width: '400px' }}>
      <SearchAutocomplete
        placeholder="Search countries..."
        onSearch={handleSearch}
        onSelect={handleSelect}
      />
    </div>
  );
}
```

### With Custom Styling

```tsx
<SearchAutocomplete
  placeholder="Search users..."
  onSearch={handleSearch}
  onSelect={handleSelect}
  style={{ maxWidth: '500px' }}
/>
```

## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `placeholder` | `string` | `'Search...'` | Input placeholder |
| `onSearch` | `(query: string) => Promise<AutocompleteItem[]>` | - | Search function (required) |
| `onSelect` | `(item: AutocompleteItem) => void` | - | Selection callback (required) |
| `debounceMs` | `number` | `300` | Debounce delay in ms |
| `maxResults` | `number` | `10` | Maximum results to show |
| `minQueryLength` | `number` | `2` | Minimum characters before search |
| `className` | `string` | - | CSS class for container |
| `style` | `CSSProperties` | - | Inline styles for container |

## Types

```typescript
interface AutocompleteItem {
  id: string;
  label: string;
  description?: string;
  icon?: string;
}
```

## Keyboard Navigation

| Key | Action |
|-----|--------|
| `Arrow Down` | Move to next result / Open dropdown |
| `Arrow Up` | Move to previous result |
| `Enter` | Select highlighted result |
| `Escape` | Close dropdown |
| `Tab` | Close dropdown |

## Accessibility

- `role="combobox"` on input
- `role="listbox"` on dropdown
- `role="option"` on each item
- `aria-expanded` reflects open state
- `aria-autocomplete="list"` for screen readers
- Focus management

## Example: Wikipedia Search

```tsx
import SearchAutocomplete, { AutocompleteItem } from '@/components/SearchAutocomplete';

function WikipediaSearch() {
  const handleSearch = async (query: string): Promise<AutocompleteItem[]> => {
    const response = await fetch(
      `https://en.wikipedia.org/w/api.php?action=opensearch&search=${encodeURIComponent(query)}&limit=5&format=json`
    );
    const [search, titles, descriptions] = await response.json();
    
    return titles.map((title: string, index: number) => ({
      id: title,
      label: title,
      description: descriptions[index] || '',
      icon: '📖',
    }));
  };

  const handleSelect = (item: AutocompleteItem) => {
    window.open(`https://en.wikipedia.org/wiki/${encodeURIComponent(item.label)}`, '_blank');
  };

  return (
    <div style={{ width: '500px', margin: '50px auto' }}>
      <h2>Search Wikipedia</h2>
      <SearchAutocomplete
        placeholder="Search Wikipedia articles..."
        onSearch={handleSearch}
        onSelect={handleSelect}
        debounceMs={400}
      />
    </div>
  );
}
```

## How Debouncing Works

The component waits for the user to stop typing for `debounceMs` milliseconds before triggering the search. This prevents excessive API calls.

```
User types: "cat"
         │
         │ (300ms debounce)
         ▼
Trigger search("cat")
         │
         ▼
Display results
```

## Custom Item Rendering

To customize how items are displayed, you can modify the component or create a wrapper:

```tsx
const CustomAutocomplete: React.FC<Props> = (props) => {
  // ... existing logic

  return (
    <SearchAutocomplete
      {...props}
      renderItem={(item, isHighlighted) => (
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <Avatar src={item.avatar} />
          <div>
            <div style={{ fontWeight: 600 }}>{item.name}</div>
            <div style={{ fontSize: '12px', color: '#666' }}>{item.email}</div>
          </div>
        </div>
      )}
    />
  );
};
```
