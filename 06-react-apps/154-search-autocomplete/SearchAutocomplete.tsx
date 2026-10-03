'use client';

import React, { useState, useEffect, useRef, useCallback, KeyboardEvent } from 'react';

// Types
export interface AutocompleteItem {
  id: string;
  label: string;
  description?: string;
  icon?: string;
}

interface SearchAutocompleteProps {
  placeholder?: string;
  onSearch: (query: string) => Promise<AutocompleteItem[]>;
  onSelect: (item: AutocompleteItem) => void;
  debounceMs?: number;
  maxResults?: number;
  minQueryLength?: number;
  className?: string;
  style?: React.CSSProperties;
}

// Styles
const styles = {
  container: {
    position: 'relative' as const,
    fontFamily: 'system-ui, -apple-system, sans-serif',
  },
  inputWrapper: {
    position: 'relative' as const,
  },
  input: {
    width: '100%',
    padding: '12px 16px',
    paddingRight: '40px',
    fontSize: '16px',
    border: '2px solid #e5e7eb',
    borderRadius: '12px',
    outline: 'none',
    transition: 'border-color 0.2s, box-shadow 0.2s',
    boxSizing: 'border-box',
  },
  inputFocused: {
    borderColor: '#667eea',
    boxShadow: '0 0 0 3px rgba(102, 126, 234, 0.15)',
  },
  searchIcon: {
    position: 'absolute' as const,
    right: '14px',
    top: '50%',
    transform: 'translateY(-50%)',
    color: '#9ca3af',
    pointerEvents: 'none' as const,
  },
  clearButton: {
    position: 'absolute' as const,
    right: '14px',
    top: '50%',
    transform: 'translateY(-50%)',
    background: 'none',
    border: 'none',
    cursor: 'pointer',
    color: '#9ca3af',
    padding: '4px',
    borderRadius: '4px',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
  },
  dropdown: {
    position: 'absolute' as const,
    top: 'calc(100% + 4px)',
    left: 0,
    right: 0,
    maxHeight: '320px',
    overflowY: 'auto' as const,
    backgroundColor: '#fff',
    border: '1px solid #e5e7eb',
    borderRadius: '12px',
    boxShadow: '0 10px 40px rgba(0,0,0,0.12)',
    zIndex: 1000,
  },
  loadingContainer: {
    padding: '16px',
    textAlign: 'center' as const,
    color: '#6b7280',
  },
  spinner: {
    display: 'inline-block',
    width: '20px',
    height: '20px',
    border: '2px solid #e5e7eb',
    borderTopColor: '#667eea',
    borderRadius: '50%',
    animation: 'spin 0.8s linear infinite',
  },
  noResults: {
    padding: '16px',
    textAlign: 'center' as const,
    color: '#9ca3af',
  },
  list: {
    padding: '4px',
  },
  item: {
    display: 'flex',
    alignItems: 'center',
    gap: '12px',
    padding: '12px 16px',
    cursor: 'pointer',
    borderRadius: '8px',
    transition: 'background-color 0.15s',
  },
  itemHighlighted: {
    backgroundColor: '#f3f4f6',
  },
  itemIcon: {
    fontSize: '20px',
    width: '24px',
    textAlign: 'center' as const,
  },
  itemContent: {
    flex: 1,
    minWidth: 0,
  },
  itemLabel: {
    fontSize: '15px',
    fontWeight: 500,
    color: '#1f2937',
    whiteSpace: 'nowrap' as const,
    overflow: 'hidden',
    textOverflow: 'ellipsis',
  },
  itemDescription: {
    fontSize: '13px',
    color: '#6b7280',
    marginTop: '2px',
    whiteSpace: 'nowrap' as const,
    overflow: 'hidden',
    textOverflow: 'ellipsis',
  },
  keyboardHint: {
    fontSize: '11px',
    color: '#9ca3af',
    backgroundColor: '#f3f4f6',
    padding: '2px 6px',
    borderRadius: '4px',
    marginLeft: '8px',
  },
};

// CSS for spinner animation
const spinnerKeyframes = `
  @keyframes spin {
    to { transform: rotate(360deg); }
  }
`;

const SearchAutocomplete: React.FC<SearchAutocompleteProps> = ({
  placeholder = 'Search...',
  onSearch,
  onSelect,
  debounceMs = 300,
  maxResults = 10,
  minQueryLength = 2,
  className,
  style,
}) => {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<AutocompleteItem[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isOpen, setIsOpen] = useState(false);
  const [highlightedIndex, setHighlightedIndex] = useState(-1);
  const [error, setError] = useState<string | null>(null);

  const containerRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);
  const debounceRef = useRef<number | null>(null);

  // Debounced search
  const performSearch = useCallback(
    async (searchQuery: string) => {
      if (searchQuery.length < minQueryLength) {
        setResults([]);
        setIsOpen(false);
        return;
      }

      setIsLoading(true);
      setError(null);

      try {
        const items = await onSearch(searchQuery);
        setResults(items.slice(0, maxResults));
        setIsOpen(true);
        setHighlightedIndex(-1);
      } catch (err) {
        setError('Search failed. Please try again.');
        setResults([]);
      } finally {
        setIsLoading(false);
      }
    },
    [onSearch, maxResults, minQueryLength]
  );

  // Handle input change with debounce
  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setQuery(value);

    if (debounceRef.current) {
      clearTimeout(debounceRef.current);
    }

    debounceRef.current = window.setTimeout(() => {
      performSearch(value);
    }, debounceMs);
  };

  // Clear search
  const handleClear = () => {
    setQuery('');
    setResults([]);
    setIsOpen(false);
    setHighlightedIndex(-1);
    inputRef.current?.focus();
  };

  // Select item
  const handleSelect = (item: AutocompleteItem) => {
    setQuery(item.label);
    setIsOpen(false);
    setHighlightedIndex(-1);
    onSelect(item);
  };

  // Keyboard navigation
  const handleKeyDown = (e: KeyboardEvent<HTMLInputElement>) => {
    if (!isOpen) {
      if (e.key === 'ArrowDown' && results.length > 0) {
        setIsOpen(true);
        setHighlightedIndex(0);
        e.preventDefault();
      }
      return;
    }

    switch (e.key) {
      case 'ArrowDown':
        e.preventDefault();
        setHighlightedIndex((prev) =>
          prev < results.length - 1 ? prev + 1 : prev
        );
        break;
      case 'ArrowUp':
        e.preventDefault();
        setHighlightedIndex((prev) => (prev > 0 ? prev - 1 : -1));
        break;
      case 'Enter':
        e.preventDefault();
        if (highlightedIndex >= 0 && results[highlightedIndex]) {
          handleSelect(results[highlightedIndex]);
        }
        break;
      case 'Escape':
        e.preventDefault();
        setIsOpen(false);
        setHighlightedIndex(-1);
        break;
      case 'Tab':
        setIsOpen(false);
        setHighlightedIndex(-1);
        break;
    }
  };

  // Click outside to close
  useEffect(() => {
    const handleClickOutside = (e: MouseEvent) => {
      if (containerRef.current && !containerRef.current.contains(e.target as Node)) {
        setIsOpen(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  // Cleanup debounce on unmount
  useEffect(() => {
    return () => {
      if (debounceRef.current) {
        clearTimeout(debounceRef.current);
      }
    };
  }, []);

  const showDropdown = isOpen && (isLoading || results.length > 0 || error);

  return (
    <>
      <style>{spinnerKeyframes}</style>
      <div ref={containerRef} className={className} style={{ ...styles.container, ...style }}>
        <div style={styles.inputWrapper}>
          <input
            ref={inputRef}
            type="text"
            value={query}
            onChange={handleInputChange}
            onKeyDown={handleKeyDown}
            onFocus={() => query.length >= minQueryLength && results.length > 0 && setIsOpen(true)}
            placeholder={placeholder}
            autoComplete="off"
            role="combobox"
            aria-expanded={isOpen}
            aria-haspopup="listbox"
            aria-autocomplete="list"
            style={{
              ...styles.input,
              ...(isOpen ? styles.inputFocused : {}),
            }}
          />

          {query ? (
            <button
              type="button"
              onClick={handleClear}
              style={styles.clearButton}
              aria-label="Clear search"
            >
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <line x1="18" y1="6" x2="6" y2="18" />
                <line x1="6" y1="6" x2="18" y2="18" />
              </svg>
            </button>
          ) : (
            <span style={styles.searchIcon}>
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <circle cx="11" cy="11" r="8" />
                <line x1="21" y1="21" x2="16.65" y2="16.65" />
              </svg>
            </span>
          )}
        </div>

        {showDropdown && (
          <div style={styles.dropdown} role="listbox">
            {isLoading ? (
              <div style={styles.loadingContainer}>
                <div style={styles.spinner} />
                <span style={{ marginLeft: '8px' }}>Searching...</span>
              </div>
            ) : error ? (
              <div style={styles.noResults}>{error}</div>
            ) : results.length === 0 ? (
              <div style={styles.noResults}>No results found for "{query}"</div>
            ) : (
              <div style={styles.list}>
                {results.map((item, index) => (
                  <div
                    key={item.id}
                    role="option"
                    aria-selected={index === highlightedIndex}
                    onClick={() => handleSelect(item)}
                    onMouseEnter={() => setHighlightedIndex(index)}
                    style={{
                      ...styles.item,
                      ...(index === highlightedIndex ? styles.itemHighlighted : {}),
                    }}
                  >
                    {item.icon && <span style={styles.itemIcon}>{item.icon}</span>}
                    <div style={styles.itemContent}>
                      <div style={styles.itemLabel}>
                        {highlightText(item.label, query)}
                        {index === highlightedIndex && (
                          <span style={styles.keyboardHint}>Enter to select</span>
                        )}
                      </div>
                      {item.description && (
                        <div style={styles.itemDescription}>{item.description}</div>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </div>
    </>
  );
};

// Highlight matching text
const highlightText = (text: string, query: string): React.ReactNode => {
  if (!query) return text;

  const parts = text.split(new RegExp(`(${escapeRegExp(query)})`, 'gi'));
  return (
    <>
      {parts.map((part, i) =>
        part.toLowerCase() === query.toLowerCase() ? (
          <mark key={i} style={{ backgroundColor: '#fef08a', padding: '0 2px' }}>
            {part}
          </mark>
        ) : (
          part
        )
      )}
    </>
  );
};

// Helper to escape regex special characters
const escapeRegExp = (string: string): string => {
  return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
};

export default SearchAutocomplete;
