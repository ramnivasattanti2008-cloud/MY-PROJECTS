# CSV Analyzer

A Python utility for comprehensive analysis of CSV files with statistical summaries, data quality assessment, and exportable reports.

## Features

- **Automatic Type Detection**: Identifies columns as integer, float, boolean, date, or string
- **Missing Value Analysis**: Reports missing values per column and overall
- **Statistical Summaries**: Mean, median, std dev, quartiles for numeric columns
- **Duplicate Detection**: Finds duplicate rows and potential primary keys
- **Data Quality Scoring**: Overall quality score (0-100) with letter grades
- **Export Reports**: JSON or text format reports

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Basic Analysis

```bash
python csv-analyzer.py data.csv
```

### Export Report

```bash
# JSON format (default)
python csv-analyzer.py data.csv -o report.json

# Text format
python csv-analyzer.py data.csv -o report.txt --format txt
```

### Quick Stats Only

```bash
python csv-analyzer.py data.csv --quick
```

## Output Example

```
📄 FILE INFORMATION
   Name: sales.csv
   Size: 1,234,567 bytes (1.2 MB)
   Memory: 2.45 MB
   Rows: 50,000
   Columns: 12

📋 COLUMN TYPES
   id: integer (e.g., 1, 2, 3)
   date: date (e.g., 2024-01-15, 2024-01-16)
   amount: float (e.g., 99.99, 149.50)
   status: string (e.g., completed, pending)

❓ MISSING VALUES
   email: 234 (0.39%)
   phone: 1,456 (2.43%)
   Overall: 1,690 cells (0.28%)

✅ DATA QUALITY
   Overall Score: 92/100 (Grade: A)
   Completeness: 99.72/100
   Uniqueness: 100/100
   Type Consistency: 100/100
```

## Data Quality Score

The analyzer calculates an overall quality score based on three factors:

| Factor | Weight | Description |
|--------|--------|-------------|
| Completeness | 40% | Percentage of non-null values |
| Uniqueness | 30% | Inverse of duplicate rate |
| Consistency | 30% | Type consistency across columns |

### Grade Scale

| Score | Grade |
|-------|-------|
| 90-100 | A |
| 80-89 | B |
| 70-79 | C |
| 60-69 | D |
| 0-59 | F |

## CSV File Compatibility

The analyzer automatically handles:
- Different encodings (UTF-8, Latin-1, CP1252, ISO-8859-1)
- Different delimiters (comma, semicolon, tab, pipe)
- Missing values (empty, NaN, NA)
- Malformed lines (warns and skips)

## Library Used

- **pandas**: DataFrame operations and statistics
- **openpyxl**: Excel file support (optional)

## License

MIT License - Educational purposes
