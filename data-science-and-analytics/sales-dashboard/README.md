# Sales Dashboard 📈

A comprehensive Streamlit application for analyzing sales data with interactive visualizations and KPIs.

## Features

- **Overview Dashboard**: Key metrics, top products, regional distribution
- **Revenue Analysis**: Detailed revenue breakdown with filters
- **Product Analysis**: Product performance, comparison, and heatmaps
- **Regional Analysis**: Regional performance comparison
- **Time Analysis**: Trend analysis by month, week, quarter

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
streamlit run app.py
```

## CSV Format

Your CSV file should have the following columns:

```csv
date,region,product,category,quantity,unit_price
2024-01-15,North,Laptop,Electronics,5,1200.00
2024-01-16,South,Phone,Electronics,10,800.00
```

### Optional columns:
- `customer_type`: Individual, Business, Government
- `salesperson`: Name of salesperson

## KPIs Tracked

- Total Revenue
- Total Orders
- Average Order Value
- Units Sold
- Revenue by Region
- Revenue by Product
- Revenue by Category

## Tech Stack

- Streamlit - Web framework
- Pandas - Data manipulation
- Plotly - Interactive visualizations
- NumPy - Numerical computing

## License

MIT License
