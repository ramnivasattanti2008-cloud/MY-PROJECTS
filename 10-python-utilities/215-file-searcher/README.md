# File Searcher

A fast Python command-line tool for searching files by name, content, size, and modification date.

## Features

- **Fast traversal**: Uses `os.scandir` for efficient directory walking
- **Multi-criteria search**: Combine name, content, size, and date filters
- **Regex support**: Full regex pattern matching for advanced searches
- **Human-readable output**: Formatted file sizes and dates
- **Content search**: Find text within files with line numbers
- **No dependencies**: Uses only Python standard library

## Installation

```bash
pip install -r requirements.txt
```

Note: No external dependencies required.

## Usage

### Search by filename

```bash
python file-searcher.py ./documents -n "report"
python file-searcher.py . -n "*.py" --regex
python file-searcher.py . -n "file" -i  # case-insensitive
```

### Search by content

```bash
python file-searcher.py . -c "TODO"
python file-searcher.py ./src -c "function main" -e .py .js
python file-searcher.py . -c "password" -R --regex
```

### Search by size

```bash
python file-searcher.py . -s 10mb       # files up to 10 MB
python file-searcher.py . -s 1kb -s 100kb  # files between 1KB and 100KB
python file-searcher.py . --size 1gb    # files up to 1 GB
```

### Search by date

```bash
python file-searcher.py . -d 7        # modified in last 7 days
python file-searcher.py . --start-date 2024-01-01 --end-date 2024-12-31
python file-searcher.py . -d 30 -t created  # created in last 30 days
```

### Combined searches

```bash
python file-searcher.py . -n ".log" -d 7
python file-searcher.py ./logs -c "ERROR" -d 1 -e .log .txt
```

### Output options

```bash
python file-searcher.py . -n "file" --no-path        # filenames only
python file-searcher.py . -n "file" --show-size      # show file sizes
python file-searcher.py . -n "file" --show-date      # show modification dates
python file-searcher.py . -n "file" -v              # verbose mode
```

## Arguments

| Argument | Short | Description |
|----------|-------|-------------|
| `path` | - | Root path to search (default: current directory) |
| `--name` | `-n` | Search by filename pattern |
| `--content` | `-c` | Search by file content |
| `--size` | `-s` | Search by maximum size (e.g., 10mb, 100kb) |
| `--days` | `-d` | Modified within N days |
| `--start-date` | - | Modified after date (YYYY-MM-DD) |
| `--end-date` | - | Modified before date (YYYY-MM-DD) |
| `--date-type` | `-t` | Date type: modified, accessed, or created |
| `--extensions` | `-e` | File extensions to include (space-separated) |
| `--regex` | `-R` | Use regex pattern |
| `--case-insensitive` | `-i` | Case insensitive matching |
| `--no-path` | - | Show filenames only |
| `--show-size` | - | Show file sizes |
| `--show-date` | - | Show modification dates |
| `--max-size` | `-m` | Max file size for content search (MB) |
| `--verbose` | `-v` | Verbose output |

## Examples

### Find all Python files

```bash
python file-searcher.py . -n ".py" --regex
```

### Find large log files

```bash
python file-searcher.py . -n ".log" -s 50mb
```

### Find recently modified documents

```bash
python file-searcher.py ./documents -d 30 -e .pdf .docx .xlsx
```

### Find TODOs and FIXMEs

```bash
python file-searcher.py . -c "TODO" -e .py .js .ts
python file-searcher.py . -c "FIXME" -e .py .js
```

### Find files by regex pattern

```bash
python file-searcher.py . -n "report_\d{4}" -R
python file-searcher.py . -n "IMG_.*\.jpg$" -R
```

### Find empty or very small files

```bash
python file-searcher.py . -s 100b
```

## Performance Tips

1. Use `--extensions` to filter file types when searching content
2. Use `--max-size` to skip large files during content search
3. For large directories, specify a more specific root path
4. Use `--no-path` for cleaner output when you only need filenames

## License

MIT License
