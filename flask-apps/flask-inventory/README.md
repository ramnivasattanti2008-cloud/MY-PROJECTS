# Inventory Tracker

A Flask application to track inventory items, quantities, and stock levels.

## Features

- Add items with name, description, category, and location
- Track current quantity and minimum stock threshold
- Low stock alerts when items fall below minimum
- Quick stock adjustment (+/-)
- Search and filter items
- Summary statistics (total items, low stock count)

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python app.py
```

Open http://127.0.0.1:5000 in your browser.

## How to Use

1. Click "Add Item" to add new inventory items
2. Set a minimum quantity for low stock alerts
3. Use "Adjust" to quickly add or remove stock
4. Items highlighted in red need restocking
5. Filter by category or show only low stock items
