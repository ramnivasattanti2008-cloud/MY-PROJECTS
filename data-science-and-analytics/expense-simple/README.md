# Expense Tracker

A Streamlit application for tracking personal expenses with visual analytics.

## Features

- Add expenses with date, amount, category, and description
- View recent expenses with delete functionality
- Monthly spending trend with bar and line charts
- Category breakdown with pie and bar charts
- Total, count, and average statistics
- SQLite database for persistent storage

## Installation

```bash
cd expense-simple
pip install -r requirements.txt
streamlit run app.py
```

## Usage

1. Run the app with `streamlit run app.py`
2. Opens at `http://localhost:8501`
3. Add expenses using the form on the left
4. View analytics in the three tabs

## Categories

- Food & Dining
- Transportation
- Shopping
- Entertainment
- Bills & Utilities
- Healthcare
- Education
- Travel
- Groceries
- Personal Care
- Other

## Database

SQLite database (`expenses.db`) created automatically.

## Project Structure

```
expense-simple/
├── app.py          # Main Streamlit application
├── requirements.txt
└── README.md
```
