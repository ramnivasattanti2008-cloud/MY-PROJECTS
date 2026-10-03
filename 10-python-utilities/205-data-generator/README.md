# Data Generator

A Python CLI tool for generating fake data for testing purposes.

## Features

- Generate realistic fake data
- Multiple field types: names, emails, phones, addresses, companies, dates, etc.
- Multiple locales: US, UK, India
- Output formats: CSV, JSON, or both
- Reproducible results with random seed
- Configurable number of records

## Installation

No external dependencies required - uses Python standard library.

```bash
# Run directly
python data-generator.py [options]
```

## Usage

### Basic Examples

```bash
# Generate 10 records (default)
python data-generator.py

# Generate 100 records
python data-generator.py -n 100

# Generate 50 records and save to file
python data-generator.py -n 50 -o output.csv

# Generate JSON output
python data-generator.py -n 10 --format json -o output.json
```

### Field Selection

```bash
# Generate only names and emails
python data-generator.py --fields name email

# Include additional fields
python data-generator.py --fields name email phone address company date age

# All available fields
python data-generator.py --fields name email phone address company date age salary id username country
```

### Locales

```bash
# US data (default)
python data-generator.py --locale us

# UK data
python data-generator.py --locale uk

# Indian data
python data-generator.py --locale india
```

### Reproducible Data

```bash
# Use a seed for reproducible data
python data-generator.py -n 100 --seed 42

# Same seed produces same data
python data-generator.py -n 100 --seed 42
```

### Output Formats

```bash
# CSV output (default)
python data-generator.py -n 10 -o data.csv

# JSON output
python data-generator.py -n 10 --format json -o data.json

# Both formats
python data-generator.py -n 10 --format both -o data
```

## Options

| Option | Description |
|--------|-------------|
| `-n, --count` | Number of records to generate (default: 10) |
| `-o, --output` | Output file path (CSV or JSON) |
| `--format` | Output format: csv, json, both (default: csv) |
| `--fields` | Fields to generate: name, email, phone, address, company, date, age, salary, id, username, country |
| `--seed` | Random seed for reproducible data |
| `--locale` | Locale: us, uk, india (default: us) |
| `--indent` | JSON indentation spaces (default: 2) |

## Available Fields

| Field | Description |
|-------|-------------|
| `name` | Full name |
| `email` | Email address |
| `phone` | Phone number |
| `address` | Nested address object |
| `company` | Company name |
| `date` | Random date |
| `age` | Random age (18-80) |
| `salary` | Random salary (30k-200k) |
| `id` | Unique ID |
| `username` | Username |
| `country` | Country name |

## License

MIT
