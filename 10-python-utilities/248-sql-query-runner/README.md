# SQL Query Runner

A Python CLI tool for running SQL queries against CSV files.

## Features

- Run SQL queries against CSV files
- Full SQL support via DuckDB
- Export results to CSV or JSON
- Dry-run mode for testing queries
- Multiple output formats

## Installation

```bash
# Install dependencies
pip install -r sql-query-runner-requirements.txt

# Or minimal installation
pip install pandas duckdb
```

## Usage

### Basic Examples

```bash
# Query a CSV file
python sql-query-runner.py "SELECT * FROM data LIMIT 10" -f data.csv

# Filter and select columns
python sql-query-runner.py "SELECT name, email FROM data WHERE age > 30" -f data.csv

# Aggregate queries
python sql-query-runner.py "SELECT department, COUNT(*) as count FROM data GROUP BY department" -f data.csv

# Order and limit
python sql-query-runner.py "SELECT * FROM data ORDER BY salary DESC LIMIT 5" -f data.csv
```

### Output Options

```bash
# Output to file (CSV)
python sql-query-runner.py "SELECT * FROM data" -f data.csv -o results.csv

# JSON output
python sql-query-runner.py "SELECT * FROM data" -f data.csv --format json -o results.json

# Pretty JSON output
python sql-query-runner.py "SELECT * FROM data" -f data.csv --format pretty-json -o results.json

# CSV without header
python sql-query-runner.py "SELECT * FROM data" -f data.csv --no-header -o results.csv
```

### Custom Table Name

```bash
# Use custom table name in query
python sql-query-runner.py "SELECT * FROM my_table WHERE id > 100" -f data.csv --table my_table
```

### Dry Run Mode

```bash
# Test query without executing
python sql-query-runner.py "SELECT * FROM data WHERE name = 'John'" -f data.csv --dry-run
```

### Common SQL Operations

```bash
# Join tables (requires loading both files first)
python sql-query-runner.py "SELECT * FROM a JOIN b ON a.id = b.id" -f a.csv

# Subqueries
python sql-query-runner.py "SELECT * FROM data WHERE id IN (SELECT id FROM other)" -f data.csv

# Aggregations with HAVING
python sql-query-runner.py "SELECT city, COUNT(*) as cnt FROM data GROUP BY city HAVING cnt > 5" -f data.csv

# CASE statements
python sql-query-runner.py "SELECT name, CASE WHEN salary > 100000 THEN 'High' ELSE 'Low' END as tier FROM data" -f data.csv
```

## Options

| Option | Description |
|--------|-------------|
| `query` | SQL query to execute (required) |
| `-f, --file` | Input CSV file |
| `-t, --table` | Table name for query (default: data) |
| `-o, --output` | Output file for results |
| `--format` | Output format: csv, json, pretty-json |
| `--no-header` | CSV output without header row |
| `--dry-run` | Show query without executing |
| `--encoding` | Input file encoding (default: utf-8) |

## SQL Features

The tool uses DuckDB for SQL execution, which supports:

- SELECT, WHERE, GROUP BY, ORDER BY, LIMIT
- JOINs (INNER, LEFT, RIGHT, FULL)
- Subqueries
- Aggregate functions (COUNT, SUM, AVG, MIN, MAX)
- String functions (LIKE, SUBSTR, CONCAT)
- Date/time functions
- CASE statements
- Window functions

## Examples by Use Case

### Data Filtering
```bash
# Find records with missing values
python sql-query-runner.py "SELECT * FROM data WHERE email IS NULL" -f data.csv

# Date range filter
python sql-query-runner.py "SELECT * FROM data WHERE date > '2024-01-01'" -f data.csv

# Multiple conditions
python sql-query-runner.py "SELECT * FROM data WHERE age > 25 AND city = 'New York'" -f data.csv
```

### Data Analysis
```bash
# Statistics
python sql-query-runner.py "SELECT AVG(salary), MIN(salary), MAX(salary) FROM data" -f data.csv

# Group statistics
python sql-query-runner.py "SELECT city, AVG(age) as avg_age FROM data GROUP BY city" -f data.csv

# Percentiles
python sql-query-runner.py "SELECT PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY salary) FROM data" -f data.csv
```

## License

MIT
