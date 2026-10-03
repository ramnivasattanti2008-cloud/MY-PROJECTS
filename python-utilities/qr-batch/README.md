# QR Batch Generator

Generate multiple QR codes from CSV data. Perfect for batch processing URLs, contacts, WiFi credentials, and more.

## Features

- **Batch Processing**: Generate hundreds of QR codes from a single CSV file
- **Auto-Detection**: Automatically detects data and name columns
- **Customizable**: Adjust size, error correction, and format
- **GUI Mode**: Visual interface for easy operation
- **CLI Mode**: Script-friendly for automation

## Installation

```bash
pip install qrcode[pil]
```

## Usage

### GUI Mode (Recommended)

```bash
python qr-batch.py
```

- Click "Create Sample CSV" to see the format
- Select your CSV file
- Choose output folder and settings
- Click "Generate QR Codes"

### CLI Mode

```bash
# Basic usage with auto-detected columns
qr-batch.py data.csv

# Specify columns
qr-batch.py data.csv -d url -n name

# Custom output and settings
qr-batch.py links.csv -o ./qrcodes -s 15 -e H -f PNG
```

## CSV Format

Your CSV file should have at least one column with the data to encode:

```csv
name,url,description
Google,https://www.google.com,Search engine
GitHub,https://github.com,Code hosting
Python,https://www.python.org,Programming language
```

### Column Detection

The tool automatically detects:
- **Data column**: Looks for `url`, `link`, `data`, `content`, `text`, `value`, or `code`
- **Name column**: Looks for `name`, `id`, `title`, `filename`, or `label`

Or specify manually with `-d` and `-n` flags.

## Options

| Option | Short | Default | Description |
|--------|-------|---------|-------------|
| `--output` | `-o` | `./qr-output` | Output directory |
| `--data-column` | `-d` | auto | Column with QR data |
| `--name-column` | `-n` | auto | Column for filenames |
| `--size` | `-s` | 10 | Module size (pixels) |
| `--error-level` | `-e` | M | L/M/Q/H error correction |
| `--format` | `-f` | PNG | Image format |
| `--sample` | | | Create sample CSV |

### Error Correction Levels

| Level | Recovery | Best For |
|-------|----------|----------|
| L | 7% | High volume, clean environment |
| M | 15% | Default, balanced |
| Q | 25% | Industrial/scanned codes |
| H | 30% | Damaged codes, small sizes |

Higher error correction creates larger QR codes but can be read even if partially damaged.

## Examples

### WiFi Credentials

```csv
name,ssid,password,type
HomeNetwork,MyWiFi,password123,WPA
OfficeNet,Office_5G,securepass456,WPA2
```

Encode as: `WIFI:T:WPA;S:MyWiFi;P:password123;;`

### Business Cards (vCard)

```csv
name,email,phone,company
John Doe,john@example.com,+1234567890,Acme Corp
```

### Product Codes

```csv
id,url,sku
PROD001,https://shop.com/p/PROD001,SKU-001
PROD002,https://shop.com/p/PROD002,SKU-002
```

### Event Tickets

```csv
ticket_id,event,date,seat
ABC123,Concert 2024,2024-06-15,A12
DEF456,Concert 2024,2024-06-15,B7
```

## Output

Generated QR codes are saved to the output directory with names based on the name column:

```
qr-output/
  Google.png
  GitHub.png
  Python.png
  StackOverflow.png
```

## Troubleshooting

**"qrcode library required" error?**
```bash
pip install qrcode[pil]
```

**QR codes won't scan?**
- Increase error correction level (`-e H`)
- Increase module size (`-s 15` or higher)
- Ensure sufficient quiet zone (white border)

**Output folder already exists?**
Files are overwritten by default. Use a different `--output` path.

**Large CSV processing slow?**
The tool processes sequentially. For very large batches, consider splitting the CSV.
