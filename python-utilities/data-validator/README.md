# Data Validator

A Python CLI tool for validating data against common rules and reporting errors.

## Features

- Email format validation
- Phone number validation (international, US, India formats)
- Date format validation with custom formats
- URL validation
- Number validation
- Required field validation
- String length validation
- Auto-detection of field types (email, phone, date, etc.)
- CSV error report export

## Installation

No external dependencies required - uses Python standard library.

```bash
# Run directly
python data-validator.py input.csv [options]
```

## Usage

### Basic Examples

```bash
# Validate all inferred rules based on field names
python data-validator.py input.csv --verbose

# Validate specific rules
python data-validator.py input.csv --rules email phone

# Mark specific fields as required
python data-validator.py input.csv --required-fields email phone name

# Export errors to CSV
python data-validator.py input.csv --output errors.csv
```

### Date and Phone Formats

```bash
# Custom date format
python data-validator.py input.csv --rules date --date-format "%d/%m/%Y"

# US phone format
python data-validator.py input.csv --rules phone --phone-format us

# India phone format
python data-validator.py input.csv --rules phone --phone-format india
```

### Combined Validation

```bash
# Full validation with custom rules
python data-validator.py input.csv \
  --rules email phone date url number \
  --required-fields email phone \
  --date-format "%Y-%m-%d" \
  --phone-format international \
  --output validation_errors.csv \
  --verbose
```

## Options

| Option | Description |
|--------|-------------|
| `input` | Input CSV file path (required) |
| `--rules` | Validation rules to apply: email, phone, date, url, number, required, length |
| `--required-fields` | List of field names that cannot be empty |
| `--date-format` | Expected date format (default: %Y-%m-%d) |
| `--phone-format` | Phone format: international, us, india, any |
| `--output` | Output file for error report (CSV) |
| `--verbose` | Show detailed error output |
| `--encoding` | Input file encoding (default: utf-8) |

## Auto-Detection

The validator automatically detects field types based on column names:

| Field Name Pattern | Validation Rule |
|-------------------|-----------------|
| `*email*` | Email format |
| `*phone*`, `*mobile*`, `*tel*` | Phone format |
| `*date*`, `*dob*`, `*birth*` | Date format |
| `*url*`, `*website*`, `*link*` | URL format |
| `*id*`, `*count*`, `*amount*`, `*price*` | Number format |

## Exit Codes

- `0` - Validation passed, no errors
- `1` - Validation failed, errors found

## License

MIT
