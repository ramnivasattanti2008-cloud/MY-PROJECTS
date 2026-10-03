# Clipboard Manager

Manage clipboard history with save, search, and paste functionality.

## Features

- Save clipboard content to persistent history
- Search through clipboard history
- Paste from any history entry
- Watch mode for automatic clipboard capture
- Persistent storage across sessions
- Human-readable timestamps
- Duplicate removal (keeps most recent)

## Installation

```bash
pip install -r requirements.txt
```

### Platform Requirements

- **Windows**: Works with PowerShell (default) or pyperclip
- **Linux**: Requires `xclip` or pyperclip
- **macOS**: Requires pyperclip

For pyperclip:
```bash
pip install pyperclip
```

## Usage

### Save to History

```bash
# Save current clipboard
python clipboard-manager.py save

# Save specific text
python clipboard-manager.py save --text "Hello, World!"
```

### List History

```bash
# List recent entries
python clipboard-manager.py list

# List more entries
python clipboard-manager.py list -n 50
```

### Search History

```bash
# Search for text
python clipboard-manager.py search "error"

# Case-insensitive search
python clipboard-manager.py search "TODO" -i
```

### Paste from History

```bash
# Paste entry at index 5
python clipboard-manager.py paste 5
```

### Clear History

```bash
# Clear all history (with confirmation)
python clipboard-manager.py clear

# Clear without confirmation
python clipboard-manager.py clear --force
```

### Watch Mode

```bash
# Watch clipboard and auto-save
python clipboard-manager.py watch

# Faster check interval
python clipboard-manager.py watch -i 0.5
```

### Default Behavior

```bash
# Just show history (default)
python clipboard-manager.py
```

## Example Output

```
Clipboard History (20 of 156 entries)

--------------------------------------------------------------------------------
[  1]      2 mins ago      245 chars  SELECT * FROM users WHERE...
       SELECT * FROM users WHERE active = 1 ORDER BY...
[  2]     15 mins ago      128 chars  Error: Connection timeout at...
       Error: Connection timeout at line 42 in...
[  3]      1 hour ago       89 chars  # TODO: Fix authentication...
       # TODO: Fix authentication bug in...
```

## Storage

History is stored in `~/.clipboard_history.json` (JSON format).

- Maximum 1000 entries
- Duplicates are automatically removed
- Entries include: content, timestamp, length

## Notes

- The watch mode requires clipboard access; ensure proper permissions
- On Linux without pyperclip, install xclip: `sudo apt install xclip`
- History persists across sessions and reboots
