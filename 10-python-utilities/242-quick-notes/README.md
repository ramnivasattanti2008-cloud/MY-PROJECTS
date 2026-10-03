# Quick Notes

A fast, terminal-based note-taking application with tagging and search capabilities.

## Features

- **Add notes** with title, content, and multiple tags
- **List notes** with optional filtering by tag or search query
- **View individual notes** in full detail
- **Update notes** - change title, content, or tags
- **Delete notes** by ID
- **List all tags** used across your notes
- **Persistent storage** in JSON format

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Add a Note
```bash
python quick-notes.py add "Meeting Notes" "Discussed project timeline and deliverables" --tags work important
```

### List All Notes
```bash
python quick-notes.py list
```

### Filter by Tag
```bash
python quick-notes.py list --tag work
```

### Search Notes
```bash
python quick-notes.py list --search "timeline"
```

### View a Note
```bash
python quick-notes.py view 20231015123456789012
```

### Update a Note
```bash
python quick-notes.py update 20231015123456789012 --title "Updated Title" --tags newtag
```

### Delete a Note
```bash
python quick-notes.py delete 20231015123456789012
```

### List All Tags
```bash
python quick-notes.py tags
```

## Data Storage

Notes are stored in `~/.quick-notes.json` (your home directory).

## Color Output

The app uses colorama for colored terminal output:
- Green: Success messages and note titles
- Cyan: Headers and metadata
- Yellow: Tags
- Red: Error messages
- Dim: Secondary information
