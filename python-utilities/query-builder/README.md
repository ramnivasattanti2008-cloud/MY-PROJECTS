# SQL Query Builder

A visual tool for building SQL queries without writing code. Point and click to select tables, columns, conditions, joins, and generate SQL statements.

## Features

- **Visual Table Selection**: Click to select tables from your database schema
- **Column Picker**: Choose specific columns or select all with *
- **WHERE Builder**: Add conditions with multiple operators
- **JOIN Builder**: Create INNER, LEFT, RIGHT, and FULL joins
- **ORDER BY & GROUP BY**: Sort and group results
- **LIMIT Control**: Restrict result set size
- **Copy to Clipboard**: One-click copy of generated SQL
- **Syntax Highlighting**: Keywords, columns, and strings are color-coded

## Usage

Simply open `query-builder.html` in any modern web browser. No server or installation required.

```bash
# Open in default browser
start query-builder.html        # Windows
open query-builder.html        # macOS
xdg-open query-builder.html    # Linux
```

## How to Use

### 1. Select Tables
Click on table names in the sidebar to add them to your query. Multiple tables can be selected.

### 2. Choose Columns
After selecting tables, check the columns you want in your output. Leave blank for all columns (*).

### 3. Add Conditions
Click "+ Add Condition" to add WHERE clauses. Choose column, operator, and value.

### 4. Add JOINs
Click "+ Add JOIN" to connect related tables. Select join type, table, and columns to join on.

### 5. Set Ordering
Choose a column for ORDER BY and select ASC or DESC.

### 6. Group Results
Check "GROUP BY" and select a column to group results.

### 7. Limit Results
Enter a number in the LIMIT field to restrict output.

### 8. Copy SQL
Click "Copy to Clipboard" to copy the generated SQL to your clipboard.

## Operators Available

| Operator | Description |
|----------|-------------|
| `=` | Equal to |
| `!=` | Not equal to |
| `>` | Greater than |
| `<` | Less than |
| `>=` | Greater than or equal |
| `<=` | Less than or equal |
| `LIKE` | Pattern matching |
| `IN` | Value in list |
| `IS NULL` | Is empty |
| `IS NOT NULL` | Is not empty |

## Join Types

| Type | Description |
|------|-------------|
| INNER | Only matching rows from both tables |
| LEFT | All rows from left table, matching from right |
| RIGHT | All rows from right table, matching from left |
| FULL | All rows from both tables |

## Helper Panel

The helper panel on the right provides:
- **Snippets**: Common SQL patterns
- **Functions**: Aggregate and string functions
- **Keywords**: SQL keyword reference

## Example Queries

### Basic SELECT
```sql
SELECT users.name, users.email
FROM users
```

### With WHERE
```sql
SELECT *
FROM users
WHERE age >= 18
```

### With JOIN
```sql
SELECT users.name, orders.total
FROM users
INNER JOIN orders ON users.id = orders.user_id
```

### Complex Query
```sql
SELECT 
    products.name,
    COUNT(orders.id) as order_count
FROM products
LEFT JOIN orders ON products.id = orders.product_id
WHERE products.price > 50
GROUP BY products.name
ORDER BY order_count DESC
LIMIT 10
```

## Customization

The tool uses a sample schema. To customize for your own database, modify the `schema` object in the JavaScript:

```javascript
const schema = {
    your_table: {
        columns: [
            { name: 'id', type: 'INTEGER' },
            { name: 'name', type: 'TEXT' },
            // ... more columns
        ]
    },
    // ... more tables
};
```

## Browser Compatibility

Works in all modern browsers:
- Chrome 80+
- Firefox 75+
- Safari 13+
- Edge 80+
