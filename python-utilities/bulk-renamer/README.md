# Bulk Renamer

A Python command-line tool for batch renaming files with pattern matching, preview support, and undo functionality.

## Features

- **Pattern-based renaming**: Simple text replacement or regex patterns
- **Preview before apply**: See exactly what will be renamed before committing
- **Undo support**: Revert last rename operation with full history
- **Flexible filtering**: Filter by file extensions or exclusion patterns
- **Case-sensitive/insensitive**: Option for case-sensitive or case-insensitive matching

## Installation

```bash
pip install -r requirements.txt
```

Note: This tool uses only Python standard library, no external dependencies required.

## Usage

### Basic text replacement

```bash
python bulk-renamer.py ./documents -s "old_" -r "new_"
```

### Regex-based renaming

```bash
python bulk-renamer.py ./photos -s "IMG_(\d+)" -r "photo_\1" -R
```

### Preview changes only

```bash
python bulk-renamer.py ./files -s "file" -r "doc" -p
```

### Filter by extension

```bash
python bulk-renamer.py ./docs -s "draft" -r "final" -e .txt .md
```

### Skip confirmation

```bash
python bulk-renamer.py ./files -s "temp" -r "backup" -y
```

### Undo last operation

```bash
python bulk-renamer.py . --undo
```

### View rename history

```bash
python bulk-renamer.py . --history
```

## Arguments

| Argument | Short | Description |
|----------|-------|-------------|
| `directory` | - | Target directory containing files |
| `--search` | `-s` | Pattern to search for |
| `--replace` | `-r` | Replacement text |
| `--extensions` | `-e` | Filter by file extensions (space-separated) |
| `--exclude` | `-x` | Exclude files containing patterns |
| `--regex` | `-R` | Use regex patterns (default: simple text) |
| `--case-insensitive` | `-i` | Case insensitive matching |
| `--preview` | `-p` | Preview only, no changes |
| `--yes` | `-y` | Skip confirmation prompt |
| `--undo` | - | Undo last rename operation |
| `--history` | - | Show rename history |

## Examples

### Rename all files with "vacation" to "holiday"

```bash
python bulk-renamer.py ./photos -s "vacation" -r "holiday"
```

### Add prefix to all .txt files

```bash
python bulk-renamer.py ./docs -s "^" -r "backup_" -R -e .txt
```

### Replace spaces with underscores

```bash
python bulk-renamer.py ./files -s " " -r "_"
```

### Remove "backup_" prefix

```bash
python bulk-renamer.py ./files -s "backup_" -r ""
```

## Regex Groups

When using regex, you can use capture groups in the replacement:

- `\1`, `\2`, etc. - Reference captured groups
- `\d` - Match any digit
- `\w` - Match any word character
- `^` / `$` - Start/end of filename

Example: `IMG_20230915_143022.jpg` to `photo_2023-09-15.jpg`

```bash
python bulk-renamer.py ./photos -s "IMG_(\d{4})(\d{2})(\d{2})_(\d{6})" -r "photo_\1-\2-\3.jpg" -R
```

## License

MIT License
