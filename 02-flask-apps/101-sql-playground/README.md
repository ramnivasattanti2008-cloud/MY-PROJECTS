# SQL Playground

A Flask web application for running SQL queries on SQLite databases with a user-friendly interface.

## Features

- **Interactive Query Editor**: Write and execute SQL queries with syntax highlighting
- **Results Table**: View query results in a formatted table
- **Save Queries**: Save frequently used queries for quick access
- **Database Browser**: View all tables and their schema
- **Export Results**: Download query results as CSV files
- **Sample Database**: Comes with pre-loaded sample data for testing

## Installation

```bash
cd sql-playground
pip install -r requirements.txt
```

## Usage

```bash
python app.py
```

Open your browser and navigate to `http://localhost:5000`

## Sample Queries to Try

```sql
-- Get all users with their orders
SELECT u.name, u.email, COUNT(o.id) as order_count
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.id;

-- Products in Electronics category
SELECT name, price, stock FROM products WHERE category = 'Electronics';

-- Order history with user and product details
SELECT 
    u.name as customer,
    p.name as product,
    o.quantity,
    o.order_date
FROM orders o
JOIN users u ON o.user_id = u.id
JOIN products p ON o.product_id = p.id
ORDER BY o.order_date DESC;
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Main interface |
| `/execute` | POST | Execute a SQL query |
| `/save-query` | POST | Save a query |
| `/delete-query` | POST | Delete a saved query |
| `/export` | POST | Export results to CSV |
| `/tables` | GET | List all tables |

## Project Structure

```
sql-playground/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── README.md           # This file
├── playground.db       # SQLite database (created on first run)
└── templates/
    └── index.html      # Main HTML template
```
