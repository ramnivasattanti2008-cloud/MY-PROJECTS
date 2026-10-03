"""
Database Migrator - Convert data between SQLite and CSV formats.

Usage:
    # Export SQLite tables to CSV
    python db-migrator.py export database.db output_dir/

    # Import CSV files to SQLite
    python db-migrator.py import database.db input_dir/

    # Export specific table
    python db-migrator.py export database.db output_dir/ --table users

    # Import with custom delimiter
    python db-migrator.py import database.db input_dir/ --delimiter ","
"""

import argparse
import csv
import os
import sqlite3
import sys
from pathlib import Path
from datetime import datetime


class DatabaseMigrator:
    """Handles migration between SQLite databases and CSV files."""

    def __init__(self, database_path):
        """Initialize migrator with database path."""
        self.database_path = database_path
        self._ensure_database_exists()

    def _ensure_database_exists(self):
        """Create database file if it doesn't exist."""
        if not os.path.exists(self.database_path):
            Path(self.database_path).touch()

    def _get_connection(self):
        """Get SQLite database connection."""
        conn = sqlite3.connect(self.database_path)
        conn.row_factory = sqlite3.Row
        return conn

    def get_tables(self):
        """Get list of all tables in the database."""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        tables = [row[0] for row in cursor.fetchall()]
        conn.close()
        return tables

    def get_table_schema(self, table_name):
        """Get schema information for a table."""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(f"PRAGMA table_info({table_name})")
        schema = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return schema

    def export_table_to_csv(self, table_name, csv_path, delimiter=',', include_headers=True):
        """
        Export a single table to CSV file.

        Args:
            table_name: Name of the table to export
            csv_path: Path to the output CSV file
            delimiter: CSV delimiter character
            include_headers: Whether to include column headers

        Returns:
            Number of rows exported
        """
        conn = self._get_connection()
        cursor = conn.cursor()

        # Get all data from table
        cursor.execute(f"SELECT * FROM {table_name}")
        columns = [description[0] for description in cursor.description]
        rows = cursor.fetchall()

        # Write to CSV
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter=delimiter)

            if include_headers:
                writer.writerow(columns)

            for row in rows:
                # Convert various types to strings
                row_data = []
                for value in row:
                    if value is None:
                        row_data.append('')
                    elif isinstance(value, (int, float)):
                        row_data.append(value)
                    elif isinstance(value, bytes):
                        row_data.append(value.hex())
                    else:
                        row_data.append(str(value))
                writer.writerow(row_data)

        conn.close()
        return len(rows)

    def import_csv_to_table(self, csv_path, table_name, delimiter=',', create_table=True):
        """
        Import CSV file to a database table.

        Args:
            csv_path: Path to the input CSV file
            table_name: Name of the table to create/append to
            delimiter: CSV delimiter character
            create_table: Whether to create the table if it doesn't exist

        Returns:
            Number of rows imported
        """
        # Read CSV file
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter=delimiter)

            # First row is headers
            headers = next(reader)

            # Read all data
            rows = list(reader)

        conn = self._get_connection()
        cursor = conn.cursor()

        if create_table:
            # Drop existing table
            cursor.execute(f"DROP TABLE IF EXISTS {table_name}")

            # Infer column types from data
            column_defs = []
            for i, header in enumerate(headers):
                safe_header = self._sanitize_column_name(header)
                # Sample first few values to guess type
                sample_values = [row[i] for row in rows[:10] if i < len(row) and row[i]]

                if all(self._is_int(v) for v in sample_values):
                    col_type = 'INTEGER'
                elif all(self._is_float(v) for v in sample_values):
                    col_type = 'REAL'
                else:
                    col_type = 'TEXT'

                column_defs.append(f"{safe_header} {col_type}")

            create_sql = f"CREATE TABLE {table_name} ({', '.join(column_defs)})"
            cursor.execute(create_sql)

        # Insert data
        placeholders = ', '.join(['?' for _ in headers])
        insert_sql = f"INSERT INTO {table_name} VALUES ({placeholders})"

        for row in rows:
            # Pad row if necessary
            while len(row) < len(headers):
                row.append(None)
            cursor.execute(insert_sql, row)

        conn.commit()
        conn.close()

        return len(rows)

    def export_all_tables(self, output_dir, delimiter=',', include_headers=True):
        """
        Export all tables in the database to separate CSV files.

        Args:
            output_dir: Directory to save CSV files
            delimiter: CSV delimiter character
            include_headers: Whether to include column headers

        Returns:
            Dictionary mapping table names to row counts
        """
        os.makedirs(output_dir, exist_ok=True)

        tables = self.get_tables()
        results = {}

        for table in tables:
            csv_path = os.path.join(output_dir, f"{table}.csv")
            row_count = self.export_table_to_csv(table, csv_path, delimiter, include_headers)
            results[table] = row_count
            print(f"Exported {table}: {row_count} rows -> {csv_path}")

        return results

    def import_all_csv(self, input_dir, delimiter=',', create_tables=True):
        """
        Import all CSV files from a directory to the database.

        Args:
            input_dir: Directory containing CSV files
            delimiter: CSV delimiter character
            create_tables: Whether to create tables if they don't exist

        Returns:
            Dictionary mapping table names to row counts
        """
        results = {}

        for csv_file in Path(input_dir).glob('*.csv'):
            table_name = csv_file.stem
            row_count = self.import_csv_to_table(str(csv_file), table_name, delimiter, create_tables)
            results[table_name] = row_count
            print(f"Imported {csv_file.name}: {row_count} rows -> {table_name}")

        return results

    def _sanitize_column_name(self, name):
        """Sanitize column name for SQL."""
        # Remove invalid characters, replace with underscore
        import re
        safe = re.sub(r'[^a-zA-Z0-9_]', '_', name.strip())
        if safe and safe[0].isdigit():
            safe = 'col_' + safe
        return safe or 'column'

    def _is_int(self, value):
        """Check if value can be converted to integer."""
        try:
            int(value)
            return True
        except (ValueError, TypeError):
            return False

    def _is_float(self, value):
        """Check if value can be converted to float."""
        try:
            float(value)
            return '.' in value
        except (ValueError, TypeError):
            return False


def export_command(args):
    """Handle export command."""
    migrator = DatabaseMigrator(args.database)

    if args.table:
        # Export single table
        output_path = args.output or f"{args.table}.csv"
        count = migrator.export_table_to_csv(args.table, output_path, args.delimiter)
        print(f"Exported {count} rows from '{args.table}' to '{output_path}'")
    else:
        # Export all tables
        results = migrator.export_all_tables(args.output, args.delimiter)
        print(f"\nExport complete! {len(results)} tables exported.")
        print(f"Total rows: {sum(results.values())}")


def import_command(args):
    """Handle import command."""
    migrator = DatabaseMigrator(args.database)

    if args.csv_file:
        # Import single file
        table_name = args.table or Path(args.csv_file).stem
        count = migrator.import_csv_to_table(args.csv_file, table_name, args.delimiter)
        print(f"Imported {count} rows from '{args.csv_file}' to table '{table_name}'")
    else:
        # Import all files from directory
        results = migrator.import_all_csv(args.input, args.delimiter)
        print(f"\nImport complete! {len(results)} tables imported.")
        print(f"Total rows: {sum(results.values())}")


def list_command(args):
    """Handle list command."""
    migrator = DatabaseMigrator(args.database)
    tables = migrator.get_tables()

    if not tables:
        print("No tables found in database.")
        return

    print(f"Tables in '{args.database}':")
    print("-" * 40)

    for table in tables:
        schema = migrator.get_table_schema(table)
        cursor = migrator._get_connection().cursor()
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        migrator._get_connection().close()

        print(f"\n{table} ({count} rows)")
        for col in schema:
            pk = " [PK]" if col['pk'] else ""
            nullable = "" if col['notnull'] else " NULL"
            print(f"  - {col['name']}: {col['type'] or 'TEXT'}{pk}{nullable}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Database Migrator - Convert between SQLite and CSV formats',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Export all tables to CSV
  python db-migrator.py export data.db ./exports/

  # Export single table
  python db-migrator.py export data.db ./exports/ --table users

  # Import CSV files
  python db-migrator.py import data.db ./imports/

  # List tables in database
  python db-migrator.py list data.db

  # Import with custom delimiter
  python db-migrator.py import data.db ./imports/ --delimiter ";"
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Export subcommand
    export_parser = subparsers.add_parser('export', help='Export SQLite tables to CSV')
    export_parser.add_argument('database', help='Path to SQLite database')
    export_parser.add_argument('output', help='Output directory or file path')
    export_parser.add_argument('--table', help='Export specific table only')
    export_parser.add_argument('--delimiter', default=',', help='CSV delimiter (default: ,)')

    # Import subcommand
    import_parser = subparsers.add_parser('import', help='Import CSV files to SQLite')
    import_parser.add_argument('database', help='Path to SQLite database')
    import_parser.add_argument('input', nargs='?', help='Input directory or file path')
    import_parser.add_argument('--csv-file', '--file', dest='csv_file', help='Import specific CSV file')
    import_parser.add_argument('--table', help='Target table name for single file import')
    import_parser.add_argument('--delimiter', default=',', help='CSV delimiter (default: ,)')

    # List subcommand
    list_parser = subparsers.add_parser('list', help='List tables in database')
    list_parser.add_argument('database', help='Path to SQLite database')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    # Route to appropriate command handler
    if args.command == 'export':
        export_command(args)
    elif args.command == 'import':
        import_command(args)
    elif args.command == 'list':
        list_command(args)


if __name__ == '__main__':
    main()
