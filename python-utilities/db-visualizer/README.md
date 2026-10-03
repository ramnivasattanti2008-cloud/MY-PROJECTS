# Database Visualizer

A Python script that generates ASCII ER diagrams from SQLite databases. Visualize your database schema, tables, columns, relationships, and keys in the terminal.

## Features

- ASCII art ER diagrams
- Unicode box-drawing characters (modern terminals)
- ASCII fallback for older terminals
- Foreign key relationship visualization
- Primary and foreign key highlighting
- Row count display
- Compact single-line view option
- HTML output for documentation
- Color-coded output (terminal dependent)

## Installation

No dependencies required. Uses Python standard library only.

```bash
# Just run directly
python db-visualizer.py database.db
```

## Usage

### Basic Usage

View database schema:

```bash
python db-visualizer.py myapp.db
```

### Compact View

Single-line per table for quick overview:

```bash
python db-visualizer.py myapp.db --compact
```

### ASCII Only

Use ASCII characters instead of Unicode:

```bash
python db-visualizer.py myapp.db --no-unicode
```

### Hide Row Counts

For large tables where counting is slow:

```bash
python db-visualizer.py myapp.db --no-row-counts
```

### HTML Output

Generate HTML documentation:

```bash
python db-visualizer.py myapp.db --html > schema.html
```

### Save to File

Redirect output to a file:

```bash
python db-visualizer.py myapp.db -o schema.txt
```

## Example Output

### Full Diagram View

```
 Database: ecommerce.db
 Tables: 5
 Relationships: 4

┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│   users      │    │   orders     │    │  products    │
├──────────────┤    ├──────────────┤    ├──────────────┤
│ id         PK│    │ id         PK│    │ id         PK│
│ name       str│    │ user_id    FK│    │ name       str│
│ email      str│    │ product_id FK│    │ price      dec│
│ created_at   │    │ quantity   int│    │ category_idFK│
└──────────────┘    │ total      dec│    └──────────────┘
                   │ status     str│
                   │ order_date   │
                   └──────────────┘

Relationships (Foreign Keys):
----------------------------------------
  orders.user_id -> users.id (CASCADE/RESTRICT)
  orders.product_id -> products.id (CASCADE/RESTRICT)
  products.category_id -> categories.id (SET NULL/RESTRICT)
```

### Compact View

```
users (150 rows): id, name, email, password, created_at, updated_at
orders (1250 rows): id, user_id, product_id, quantity, total, status, order_date
products (500 rows): id, name, price, category_id, stock, description
categories (25 rows): id, name, description, parent_id
reviews (3000 rows): id, user_id, product_id, rating, comment, created_at
```

## Command Line Options

| Option | Description |
|--------|-------------|
| `database` | Path to SQLite database file |
| `--compact`, `-c` | Show compact single-line view |
| `--html` | Output as HTML for documentation |
| `--no-unicode`, `-a` | Use ASCII characters only |
| `--no-row-counts`, `-n` | Hide row counts |
| `--output`, `-o` | Save output to file |

## Output Format

### Table Box

Each table is displayed as a box showing:
- Table name with row count
- Column names
- Column data types
- Primary key indicator (`PK`)
- Not null indicator (`*`)
- Foreign key relationships (`FK`)

### Relationships Section

Lists all foreign key relationships with:
- Source table and column
- Target table and column
- ON UPDATE / ON DELETE actions

### Detailed Schema

Full breakdown of each table including:
- All columns with types
- Primary keys
- Not null constraints
- Default values
- Foreign key definitions

## Use Cases

### Database Documentation

Generate schema documentation:

```bash
python db-visualizer.py production.db --html > docs/schema.html
```

### Quick Overview

Check database structure without opening a GUI:

```bash
python db-visualizer.py app.db --compact
```

### CI/CD Integration

Include schema visualization in deployment scripts:

```bash
python db-visualizer.py db.sqlite --no-row-counts -o /tmp/schema.txt
```

## Tips

- Use `--no-row-counts` for large databases (faster)
- Use `--html` output for sharing schema with non-technical stakeholders
- Redirect to file for large databases: `python db-visualizer.py db.db > schema.txt`
