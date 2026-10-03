# ExpenseTracker

A budget tracking application built with Streamlit and Python.

## Features

- Add and categorize expenses
- Import expenses from CSV files
- Interactive charts (bar, pie)
- Monthly spending trends
- Category breakdown analysis
- Delete individual transactions
- Persistent data during session

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run app.py
```

4. Open http://localhost:8501 in your browser

## CSV Import Format

Your CSV file should have these columns:
```csv
Date,Description,Amount,Category
2024-01-15,Groceries,85.50,Food & Dining
2024-01-16,Gas station,45.00,Transportation
2024-01-17,Cinema,25.00,Entertainment
```

### Supported Categories

- Food & Dining
- Transportation
- Shopping
- Entertainment
- Bills & Utilities
- Healthcare
- Travel
- Education
- Personal Care
- Gifts & Donations
- Investments
- Other

## Usage Tips

1. **Adding Expenses**: Use the sidebar form - enter date, description, amount, and category
2. **Viewing Reports**: Charts update automatically as you add data
3. **Deleting**: Expand "All Expenses" section to remove individual entries
4. **Importing**: Upload a CSV file to bulk-import historical data

## Data Storage

Data is stored in the Streamlit session. For persistent storage, you could modify the app to:
- Save to a database (SQLite, PostgreSQL)
- Save to a JSON file
- Connect to cloud storage

## Technologies

- Streamlit 1.29
- Pandas
- Plotly

## Screenshots

The app includes:
- Summary cards (total, monthly, average)
- Monthly spending bar chart
- Category pie chart
- Top categories with progress bars
- Recent transactions table
- All expenses manager
