# Data Exporter

A command-line tool for exporting SQLite databases to JSON, CSV, SQL dump, or NDJSON formats.

## Features

- **JSON Export**: Full database export with metadata
- **CSV Export**: Individual CSV files per table
- **SQL Dump**: Standard SQL dump format for migration
- **NDJSON Export**: Streaming-friendly newline-delimited JSON
- **Gzip Compression**: Reduce output file sizes
- **Selective Tables**: Export specific tables only
- **Schema Only / Data Only**: Export options for SQL format

## Installation

No dependencies required. Uses Python standard library only.

```bash
# Python 3.6+ required
python --version
```

## Usage

### JSON Export

Export entire database to JSON:

```bash
python data-exporter.py database.db --format json -o export.json
```

Compressed JSON:

```bash
python data-exporter.py database.db --format json -o export.json.gz --compress
```

### CSV Export

Export all tables to separate CSV files:

```bash
python data-exporter.py database.db --format csv -o ./exports/
```

Custom delimiter:

```bash
python data-exporter.py database.db --format csv -o exports/ --delimiter ";"
```

### SQL Dump

Export as SQL statements (like `mysqldump`):

```bash
python data-exporter.py database.db --format sql -o dump.sql
```

Schema only (no data):

```bash
python data-exporter.py database.db --format sql -o schema.sql --schema-only
```

### NDJSON Export

Newline-delimited JSON for streaming:

```bash
python data-exporter.py database.db --format ndjson -o data.ndjson
```

## Export Specific Tables

```bash
python data-exporter.py database.db --format json -o users_only.json --tables users
python data-exporter.py database.db --format csv -o ./exports/ --tables users orders products
```

## Command Line Options

| Option | Description |
|--------|-------------|
| `database` | Path to SQLite database file |
| `--format`, `-f` | Export format: json, csv, sql, ndjson |
| `--output`, `-o` | Output path (file or directory) |
| `--tables`, `-t` | Specific tables to export |
| `--compress`, `-c` | Compress output with gzip |
| `--delimiter`, `-d` | CSV delimiter (default: ,) |
| `--no-headers` | Omit headers in CSV |
| `--no-drop` | Omit DROP TABLE in SQL |
| `--schema-only` | Export schema only |
| `--data-only` | Export data only |

## Output Formats

### JSON Format

```json
{
  "metadata": {
    "database": "app.db",
    "exported_at": "2024-01-15T10:30:00",
    "table_count": 3,
    "format": "json"
  },
  "tables": {
    "users": {
      "columns": ["id", "name", "email"],
      "row_count": 100,
      "rows": [
        {"id": 1, "name": "Alice", "email": "alice@example.com"}
      ]
    }
  }
}
```

### CSV Format

Each table becomes a separate file:
- `users.csv`
- `orders.csv`
- `products.csv`

### SQL Format

Standard SQL dump with:
- `PRAGMA foreign_keys=OFF`
- `DROP TABLE IF EXISTS` statements
- `CREATE TABLE` statements
- `INSERT INTO` statements
- `COMMIT`

### NDJSON Format

One JSON object per line, ideal for streaming:
```json
{"_table": "users", "_columns": ["id", "name", "email"]}
{"id": 1, "name": "Alice", "email": "alice@example.com"}
{"id": 2, "name": "Bob", "email": "bob@example.com"}
```

## Use Cases

### Database Backup

```bash
# Full backup with compression
python data-exporter.py production.db --format json -o backup_$(date +%Y%m%d).json.gz --compress
```

### Data Analysis

```bash
# Export for pandas analysis
python data-exporter.py analytics.db --format csv -o ./analysis_data/
```

### Migration

```bash
# Export schema for migration
python data-exporter.py old.db --format sql -o migration.sql --schema-only
```

### API Integration

```bash
# Export for JSON API
python data-exporter.py app.db --format json -o api_data.json
```

## File Sizes

Compare output sizes for a typical database:

| Format | Typical Size |
|--------|--------------|
| JSON | 100% (baseline) |
| JSON + gzip | 15-25% |
| CSV | 80-90% |
| SQL | 100-110% |
| NDJSON | Similar to JSON |

## Tips

- Use `--compress` for large databases (75-85% size reduction)
- Use `--no-drop` when appending to existing SQL dump
- Use `NDJSON` for streaming large datasets to other tools
- CSV export creates one file per table in the output directory
