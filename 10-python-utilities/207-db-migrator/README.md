# Database Migrator

A Python script for converting data between SQLite databases and CSV files.

## Features

- Export entire SQLite database to CSV files
- Export individual tables to CSV
- Import CSV files to create new SQLite tables
- Auto-detect column types from data
- Custom CSV delimiters
- List all tables in a database

## Installation

No dependencies required. Uses Python standard library only.

```bash
# Python 3.6+ required
python --version  # Should be 3.6 or higher
```

## Usage

### Export Database to CSV

Export all tables from a SQLite database:

```bash
python db-migrator.py export database.db output_directory/
```

Export a single table:

```bash
python db-migrator.py export database.db users.csv --table users
```

### Import CSV to Database

Import all CSV files from a directory:

```bash
python db-migrator.py import database.db input_directory/
```

Import a single CSV file:

```bash
python db-migrator.py import database.db data.csv --table my_table
```

### List Database Tables

View all tables and their schemas:

```bash
python db-migrator.py list database.db
```

### Custom Delimiters

Use semicolon or tab as delimiter:

```bash
python db-migrator.py export database.db output/ --delimiter ";"
python db-migrator.py import database.db input/ --delimiter $'\t'
```

## Command Reference

| Command | Description |
|---------|-------------|
| `export` | Convert SQLite tables to CSV files |
| `import` | Convert CSV files to SQLite tables |
| `list` | Display database schema |

## Examples

### Complete Workflow

```bash
# 1. Export existing database
$ python db-migrator.py export production.db ./backup/
Exported users: 1000 rows -> ./backup/users.csv
Exported orders: 5000 rows -> ./backup/orders.csv
Exported products: 200 rows -> ./backup/products.csv

Export complete! 3 tables exported.
Total rows: 6200

# 2. Make changes to CSV files in Excel/LibreOffice
# (editing happens externally)

# 3. Import modified data to new database
$ python db-migrator.py import new_database.db ./backup/
Imported users.csv: 1000 rows -> users
Imported orders.csv: 5000 rows -> orders
Imported products.csv: 200 rows -> products

Import complete! 3 tables imported.
Total rows: 6200

# 4. Verify tables
$ python db-migrator.py list new_database.db
Tables in 'new_database.db':
----------------------------------------
users (1000 rows)
  - id: INTEGER [PK]
  - name: TEXT
  - email: TEXT

orders (5000 rows)
  - id: INTEGER [PK]
  - user_id: INTEGER
  - total: REAL

products (200 rows)
  - id: INTEGER [PK]
  - name: TEXT
  - price: REAL
```

## Type Inference

When importing CSV files, the migrator automatically detects column types:

| Detected Pattern | SQLite Type |
|------------------|-------------|
| All values are integers | INTEGER |
| All values are decimals | REAL |
| Mixed or text content | TEXT |

## Notes

- NULL values in CSV are represented as empty strings
- Binary data (BLOB) is exported as hex strings
- Table names are derived from CSV filenames (without extension)
- Existing tables are replaced on import (DROP + CREATE)
