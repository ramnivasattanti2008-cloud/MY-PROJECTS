#!/usr/bin/env python3
"""
CSV Data Visualizer
Generate charts and visualizations from CSV data.
"""

import argparse
import csv
import sys
from pathlib import Path
from typing import Optional


def read_csv_data(file_path: Path) -> tuple[list[str], list[dict]]:
    """Read CSV file and return headers and rows."""
    with open(file_path, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames or []
        rows = list(reader)
    return headers, rows


def detect_column_type(values: list[str]) -> str:
    """Detect if a column is numeric, date, or categorical."""
    numeric_count = 0
    for v in values[:100]:  # Sample first 100
        if v.strip() == "":
            continue
        try:
            float(v.replace(",", ""))
            numeric_count += 1
        except ValueError:
            pass
    if numeric_count > len(values) * 0.7:
        return "numeric"
    return "categorical"


def generate_html_charts(headers: list[str], rows: list[dict], output_path: Path,
                         chart_type: str = "auto"):
    """Generate HTML file with embedded charts using Chart.js."""

    # Detect column types
    column_types = {}
    numeric_cols = []
    categorical_cols = []

    for header in headers:
        values = [row.get(header, "") for row in rows]
        col_type = detect_column_type(values)
        column_types[header] = col_type
        if col_type == "numeric":
            numeric_cols.append(header)
        else:
            categorical_cols.append(header)

    # Build chart data
    labels = [row.get(categorical_cols[0], f"Row {i}") if categorical_cols else f"Row {i}"
              for i, row in enumerate(rows)]

    # Prepare datasets for each numeric column
    datasets = []
    colors = [
        "rgba(54, 162, 235, 0.7)", "rgba(255, 99, 132, 0.7)", "rgba(75, 192, 192, 0.7)",
        "rgba(255, 206, 86, 0.7)", "rgba(153, 102, 255, 0.7)", "rgba(255, 159, 64, 0.7)"
    ]

    for i, col in enumerate(numeric_cols[:6]):  # Limit to 6 datasets
        values = []
        for row in rows:
            try:
                val = row.get(col, "0").replace(",", "")
                values.append(float(val) if val.strip() else 0)
            except ValueError:
                values.append(0)
        datasets.append({
            "label": col,
            "data": values,
            "backgroundColor": colors[i % len(colors)],
            "borderColor": colors[i % len(colors)].replace("0.7", "1"),
            "borderWidth": 1
        })

    # Generate pie/bar data for categorical + numeric
    pie_data = None
    if categorical_cols and numeric_cols:
        cat_col = categorical_cols[0]
        num_col = numeric_cols[0]
        pie_labels = []
        pie_values = []
        for row in rows[:10]:  # Top 10
            pie_labels.append(row.get(cat_col, "Unknown")[:30])
            try:
                pie_values.append(float(row.get(num_col, "0").replace(",", "")))
            except ValueError:
                pie_values.append(0)
        pie_data = {"labels": pie_labels, "values": pie_values}

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CSV Data Visualizer</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #f5f5f5;
            padding: 20px;
        }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        h1 {{ color: #333; margin-bottom: 10px; }}
        .subtitle {{ color: #666; margin-bottom: 20px; }}
        .chart-container {{
            background: white;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .chart-wrapper {{ position: relative; height: 400px; }}
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }}
        .stat-card {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .stat-label {{ color: #666; font-size: 14px; }}
        .stat-value {{ color: #333; font-size: 24px; font-weight: bold; }}
        .grid-2 {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }}
        @media (max-width: 800px) {{ .grid-2 {{ grid-template-columns: 1fr; }} }}
    </style>
</head>
<body>
    <div class="container">
        <h1>CSV Data Visualizer</h1>
        <p class="subtitle">{file_path.name} - {len(rows)} rows, {len(headers)} columns</p>

        <div class="stats">
            <div class="stat-card">
                <div class="stat-label">Total Rows</div>
                <div class="stat-value">{len(rows)}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Columns</div>
                <div class="stat-value">{len(headers)}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Numeric Columns</div>
                <div class="stat-value">{len(numeric_cols)}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Categorical Columns</div>
                <div class="stat-value">{len(categorical_cols)}</div>
            </div>
        </div>
"""

    # Bar chart for line data (first categorical + numeric)
    if categorical_cols and numeric_cols:
        html_content += f"""
        <div class="chart-container">
            <h2>Bar Chart: {numeric_cols[0]} by {categorical_cols[0]}</h2>
            <div class="chart-wrapper">
                <canvas id="barChart"></canvas>
            </div>
        </div>
        <script>
            new Chart(document.getElementById('barChart'), {{
                type: 'bar',
                data: {{
                    labels: {pie_data['labels'] if pie_data else []},
                    datasets: [{{
                        label: '{numeric_cols[0]}',
                        data: {pie_data['values'] if pie_data else []},
                        backgroundColor: 'rgba(54, 162, 235, 0.7)',
                        borderColor: 'rgba(54, 162, 235, 1)',
                        borderWidth: 1
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{ legend: {{ display: false }} }}
                }}
            }});
        </script>
"""

    # Line chart for numeric trends
    if numeric_cols:
        html_content += f"""
        <div class="chart-container">
            <h2>Line Chart: Numeric Trends</h2>
            <div class="chart-wrapper">
                <canvas id="lineChart"></canvas>
            </div>
        </div>
        <script>
            new Chart(document.getElementById('lineChart'), {{
                type: 'line',
                data: {{
                    labels: {list(range(1, len(rows) + 1))},
                    datasets: {json.dumps(datasets)}
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{ legend: {{ position: 'bottom' }} }}
                }}
            }});
        </script>
"""

    # Pie chart
    if pie_data:
        html_content += f"""
        <div class="chart-container">
            <h2>Pie Chart: {numeric_cols[0]} Distribution</h2>
            <div class="chart-wrapper" style="height: 300px;">
                <canvas id="pieChart"></canvas>
            </div>
        </div>
        <script>
            new Chart(document.getElementById('pieChart'), {{
                type: 'pie',
                data: {{
                    labels: {pie_data['labels']},
                    datasets: [{{
                        data: {pie_data['values']},
                        backgroundColor: [
                            'rgba(54, 162, 235, 0.7)', 'rgba(255, 99, 132, 0.7)',
                            'rgba(75, 192, 192, 0.7)', 'rgba(255, 206, 86, 0.7)',
                            'rgba(153, 102, 255, 0.7)', 'rgba(255, 159, 64, 0.7)',
                            'rgba(199, 199, 199, 0.7)', 'rgba(83, 102, 255, 0.7)'
                        ]
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{ legend: {{ position: 'right' }} }}
                }}
            }});
        </script>
"""

    # Data table preview
    html_content += """
        <div class="chart-container">
            <h2>Data Preview</h2>
            <div style="overflow-x: auto;">
                <table style="width: 100%; border-collapse: collapse; font-size: 14px;">
                    <thead>
                        <tr style="background: #4472C4; color: white;">
"""
    for header in headers[:10]:
        html_content += f'                            <th style="padding: 12px; text-align: left; border: 1px solid #ddd;">{header}</th>\n'

    html_content += """                        </tr>
                    </thead>
                    <tbody>
"""
    for i, row in enumerate(rows[:20]):
        bg = "#f9f9f9" if i % 2 == 0 else "white"
        html_content += f'                        <tr style="background: {bg};">\n'
        for header in headers[:10]:
            html_content += f'                            <td style="padding: 10px; border: 1px solid #ddd;">{row.get(header, "")}</td>\n'
        html_content += '                        </tr>\n'

    html_content += """                    </tbody>
                </table>
            </div>
        </div>
    </div>
</body>
</html>"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)


def main():
    parser = argparse.ArgumentParser(
        description="Generate charts from CSV data",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  csv-visualizer.py data.csv
  csv-visualizer.py data.csv -o charts.html
  csv-visualizer.py data.csv --type bar
        """
    )
    parser.add_argument("input", type=Path, help="Input CSV file")
    parser.add_argument("-o", "--output", type=Path, help="Output HTML file (default: <input>_charts.html)")
    parser.add_argument("--type", choices=["auto", "bar", "line", "pie"], default="auto",
                        help="Primary chart type")

    args = parser.parse_args()

    if not args.input.exists():
        print(f"Error: File not found: {args.input}")
        sys.exit(1)

    if args.output:
        output_path = args.output
    else:
        output_path = args.input.with_name(f"{args.input.stem}_charts.html")

    try:
        headers, rows = read_csv_data(args.input)
        if not rows:
            print("Error: CSV file is empty")
            sys.exit(1)

        generate_html_charts(headers, rows, output_path, args.type)
        print(f"Generated visualization: {output_path}")
        print(f"  - {len(rows)} rows analyzed")
        print(f"  - Open in browser to view charts")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
