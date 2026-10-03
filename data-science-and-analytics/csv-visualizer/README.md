# CSV Data Visualizer

Generate interactive charts and visualizations from CSV data.

## Installation

No external dependencies required - uses Python standard library only.

```bash
pip install -r requirements.txt  # Optional (empty file, no installs needed)
```

## Usage

```bash
python csv-visualizer.py data.csv
python csv-visualizer.py data.csv -o charts.html
```

## Features

- **Auto-detection**: Automatically detects numeric vs categorical columns
- **Interactive charts**: Bar, line, and pie charts using Chart.js
- **Data preview**: Shows first 20 rows as a formatted table
- **Statistics panel**: Row count, column count, data type summary
- **Responsive design**: Works on desktop and mobile

## Output

Generates a self-contained HTML file with:
- Summary statistics cards
- Bar chart (categorical x numeric)
- Line chart (numeric trends over rows)
- Pie chart (distribution)
- Data preview table

## Examples

```bash
# Basic usage
python csv-visualizer.py sales_data.csv

# Custom output file
python csv-visualizer.py data.csv -o report.html

# View in browser
start report.html  # Windows
open report.html   # macOS
xdg-open report.html  # Linux
```

## CSV Format

Expects standard CSV with headers in the first row:
```csv
Month,Revenue,Customers
January,50000,1200
February,65000,1450
March,72000,1600
```

## Requirements

- Python 3.7+
- Chart.js (loaded from CDN, no installation needed)
