"""
Data Exporter - Export SQLite database to JSON, CSV, or SQL dump formats.

A CLI tool for exporting database tables and data to various formats
for backup, migration, or data analysis purposes.
"""

import argparse
import csv
import json
import os
import sqlite3
import sys
import gzip
from datetime import datetime
from pathlib import Path


class DataExporter:
    """Export SQLite databases to various formats."""

    def __init__(self, database_path):
        """Initialize exporter with database path."""
        self.database_path = database_path

        if not os.path.exists(database_path):
            raise FileNotFoundError(f"Database not found: {database_path}")

    def _get_connection(self):
        """Get SQLite database connection."""
        conn = sqlite3.connect(self.database_path)
        conn.row_factory = sqlite3.Row
        return conn

    def get_tables(self):
        """Get list of all tables in the database."""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT name FROM sqlite_master
            WHERE type='table' AND name NOT LIKE 'sqlite_%'
            ORDER BY name
        """)
        tables = [row[0] for row in cursor.fetchall()]
        conn.close()
        return tables

    def _serialize_value(self, value):
        """Serialize a value for JSON export."""
        if value is None:
            return None
        elif isinstance(value, (int, float, bool)):
            return value
        elif isinstance(value, bytes):
            return value.hex()
        elif isinstance(value, (list, dict)):
            return json.dumps(value)
        elif hasattr(value, 'isoformat'):  # datetime objects
            return value.isoformat()
        else:
            return str(value)

    def export_to_json(self, output_path, tables=None, indent=2, compress=False):
        """
        Export database tables to JSON format.

        Args:
            output_path: Path to output JSON file
            tables: List of tables to export (None for all)
            indent: JSON indentation spaces
            compress: Whether to compress with gzip

        Returns:
            Dictionary with export statistics
        """
        if tables is None:
            tables = self.get_tables()

        conn = self._get_connection()
        cursor = conn.cursor()

        data = {
            'metadata': {
                'database': self.database_path,
                'exported_at': datetime.now().isoformat(),
                'table_count': len(tables),
                'format': 'json'
            },
            'tables': {}
        }

        total_rows = 0

        for table_name in tables:
            cursor.execute(f"SELECT * FROM {table_name}")
            columns = [description[0] for description in cursor.description]
            rows = cursor.fetchall()

            table_data = {
                'columns': columns,
                'row_count': len(rows),
                'rows': [
                    {columns[i]: self._serialize_value(row[i]) for i in range(len(columns))}
                    for row in rows
                ]
            }

            data['tables'][table_name] = table_data
            total_rows += len(rows)

        conn.close()

        # Write output
        json_content = json.dumps(data, indent=indent)

        if compress:
            with gzip.open(output_path, 'wt', encoding='utf-8') as f:
                f.write(json_content)
        else:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(json_content)

        return {
            'format': 'json',
            'tables': len(tables),
            'rows': total_rows,
            'output': output_path,
            'compressed': compress
        }

    def export_to_csv(self, output_dir, tables=None, delimiter=',', include_headers=True):
        """
        Export database tables to separate CSV files.

        Args:
            output_dir: Directory to save CSV files
            tables: List of tables to export (None for all)
            delimiter: CSV delimiter character
            include_headers: Whether to include column headers

        Returns:
            Dictionary with export statistics
        """
        if tables is None:
            tables = self.get_tables()

        os.makedirs(output_dir, exist_ok=True)

        conn = self._get_connection()
        cursor = conn.cursor()

        results = {}
        total_rows = 0

        for table_name in tables:
            cursor.execute(f"SELECT * FROM {table_name}")
            columns = [description[0] for description in cursor.description]
            rows = cursor.fetchall()

            output_file = os.path.join(output_dir, f"{table_name}.csv")

            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f, delimiter=delimiter)

                if include_headers:
                    writer.writerow(columns)

                for row in rows:
                    serialized = [self._serialize_value(v) for v in row]
                    writer.writerow(serialized)

            results[table_name] = len(rows)
            total_rows += len(rows)

        conn.close()

        return {
            'format': 'csv',
            'tables': len(tables),
            'rows': total_rows,
            'output_dir': output_dir,
            'files': results
        }

    def export_to_sql(self, output_path, tables=None, compress=False,
                      include_drop=True, include_schema=True, include_data=True):
        """
        Export database to SQL dump format.

        Args:
            output_path: Path to output SQL file
            tables: List of tables to export (None for all)
            compress: Whether to compress with gzip
            include_drop: Include DROP TABLE statements
            include_schema: Include CREATE TABLE statements
            include_data: Include INSERT statements

        Returns:
            Dictionary with export statistics
        """
        if tables is None:
            tables = self.get_tables()

        conn = self._get_connection()
        cursor = conn.cursor()

        sql_lines = []

        # Header
        sql_lines.append('--' + '=' * 59)
        sql_lines.append(f'-- SQLite Database Dump')
        sql_lines.append(f'-- Database: {self.database_path}')
        sql_lines.append(f'-- Exported: {datetime.now().isoformat()}')
        sql_lines.append('--' + '=' * 59)
        sql_lines.append('')

        # SQLite pragmas for compatibility
        sql_lines.append('PRAGMA foreign_keys=OFF;')
        sql_lines.append('BEGIN TRANSACTION;')
        sql_lines.append('')

        total_rows = 0

        for table_name in tables:
            # Get table info
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = [dict(row) for row in cursor.fetchall()]

            # Get create statement
            cursor.execute(f"SELECT sql FROM sqlite_master WHERE name='{table_name}'")
            create_sql = cursor.fetchone()[0]

            # Get all data
            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()

            # DROP statement
            if include_drop:
                sql_lines.append(f'DROP TABLE IF EXISTS {table_name};')

            # CREATE statement
            if include_schema and create_sql:
                sql_lines.append(create_sql + ';')

            # INSERT statements
            if include_data and rows:
                column_names = ', '.join(col['name'] for col in columns)

                for row in rows:
                    values = []
                    for value in row:
                        if value is None:
                            values.append('NULL')
                        elif isinstance(value, int):
                            values.append(str(value))
                        elif isinstance(value, float):
                            values.append(str(value))
                        elif isinstance(value, bytes):
                            values.append(f"X'{value.hex()}'")
                        elif isinstance(value, str):
                            # Escape single quotes
                            escaped = value.replace("'", "''")
                            values.append(f"'{escaped}'")
                        elif hasattr(value, 'isoformat'):
                            values.append(f"'{value.isoformat()}'")
                        else:
                            values.append(f"'{str(value)}'")

                    values_str = ', '.join(values)
                    sql_lines.append(
                        f"INSERT INTO {table_name} ({column_names}) VALUES ({values_str});"
                    )
                    total_rows += 1

            sql_lines.append('')

        # Footer
        sql_lines.append('COMMIT;')
        sql_lines.append('PRAGMA foreign_keys=ON;')
        sql_lines.append('')
        sql_lines.append('-- End of dump')

        conn.close()

        sql_content = '\n'.join(sql_lines)

        if compress:
            with gzip.open(output_path, 'wt', encoding='utf-8') as f:
                f.write(sql_content)
        else:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(sql_content)

        return {
            'format': 'sql',
            'tables': len(tables),
            'rows': total_rows,
            'output': output_path,
            'compressed': compress
        }

    def export_to_ndjson(self, output_path, tables=None, compress=False):
        """
        Export database to NDJSON (newline-delimited JSON) format.
        One JSON object per line, ideal for streaming and large datasets.

        Args:
            output_path: Path to output NDJSON file
            tables: List of tables to export (None for all)
            compress: Whether to compress with gzip

        Returns:
            Dictionary with export statistics
        """
        if tables is None:
            tables = self.get_tables()

        conn = self._get_connection()
        cursor = conn.cursor()

        if compress:
            f = gzip.open(output_path, 'wt', encoding='utf-8')
        else:
            f = open(output_path, 'w', encoding='utf-8')

        total_rows = 0

        with f:
            for table_name in tables:
                # Write table header as special record
                cursor.execute(f"PRAGMA table_info({table_name})")
                columns = [row[1] for row in cursor.fetchall()]
                f.write(json.dumps({'_table': table_name, '_columns': columns}) + '\n')

                # Write each row
                cursor.execute(f"SELECT * FROM {table_name}")
                for row in cursor:
                    row_dict = {columns[i]: self._serialize_value(row[i])
                               for i in range(len(columns))}
                    f.write(json.dumps(row_dict) + '\n')
                    total_rows += 1

        conn.close()

        return {
            'format': 'ndjson',
            'tables': len(tables),
            'rows': total_rows,
            'output': output_path,
            'compressed': compress
        }


def format_bytes(size):
    """Format bytes as human-readable string."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} {unit}"


def print_results(results):
    """Pretty print export results."""
    print("\nExport Complete!")
    print("-" * 40)
    print(f"Format: {results['format'].upper()}")
    print(f"Tables: {results['tables']}")
    print(f"Rows: {results['rows']}")

    if 'output' in results:
        size = os.path.getsize(results['output'])
        print(f"Output: {results['output']}")
        print(f"Size: {format_bytes(size)}")
        if results.get('compressed'):
            print("Compressed: Yes (gzip)")
    elif 'output_dir' in results:
        print(f"Output: {results['output_dir']}")
        print("Files:")
        for table, count in results['files'].items():
            print(f"  {table}.csv: {count} rows")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Export SQLite database to JSON, CSV, or SQL formats',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Export to JSON
  python data-exporter.py database.db --format json -o export.json

  # Export to CSV
  python data-exporter.py database.db --format csv -o ./exports/

  # Export to SQL dump
  python data-exporter.py database.db --format sql -o dump.sql

  # Export specific tables
  python data-exporter.py database.db --format json -o export.json --tables users orders

  # Compressed export
  python data-exporter.py database.db --format json -o export.json.gz --compress

  # NDJSON format (streaming-friendly)
  python data-exporter.py database.db --format ndjson -o data.ndjson
        """
    )

    parser.add_argument('database', help='Path to SQLite database')
    parser.add_argument('--format', '-f', choices=['json', 'csv', 'sql', 'ndjson'],
                        default='json', help='Export format')
    parser.add_argument('--output', '-o', required=True,
                        help='Output path (file or directory)')
    parser.add_argument('--tables', '-t', nargs='+',
                        help='Specific tables to export (default: all)')
    parser.add_argument('--compress', '-c', action='store_true',
                        help='Compress output with gzip')
    parser.add_argument('--delimiter', '-d', default=',',
                        help='CSV delimiter (default: ,)')
    parser.add_argument('--no-headers', action='store_true',
                        help='Omit headers in CSV export')
    parser.add_argument('--no-drop', action='store_true',
                        help='Omit DROP TABLE in SQL export')
    parser.add_argument('--schema-only', action='store_true',
                        help='Export schema only (no data)')
    parser.add_argument('--data-only', action='store_true',
                        help='Export data only (no schema)')

    args = parser.parse_args()

    try:
        exporter = DataExporter(args.database)

        # Validate tables exist
        if args.tables:
            all_tables = exporter.get_tables()
            invalid = set(args.tables) - set(all_tables)
            if invalid:
                print(f"Warning: Tables not found: {invalid}")
                args.tables = [t for t in args.tables if t in all_tables]

            if not args.tables:
                print("Error: No valid tables specified")
                sys.exit(1)

        # Set output file extension if needed
        output = args.output

        if args.format == 'json' and not output.endswith('.json') and not output.endswith('.gz'):
            output = output.rstrip('/\\') + '.json' if os.path.isdir(output) else output

        # Export based on format
        if args.format == 'json':
            results = exporter.export_to_json(
                output,
                tables=args.tables,
                compress=args.compress
            )
        elif args.format == 'csv':
            results = exporter.export_to_csv(
                output,
                tables=args.tables,
                delimiter=args.delimiter,
                include_headers=not args.no_headers
            )
        elif args.format == 'sql':
            results = exporter.export_to_sql(
                output,
                tables=args.tables,
                compress=args.compress,
                include_drop=not args.no_drop,
                include_schema=not args.data_only,
                include_data=not args.schema_only
            )
        elif args.format == 'ndjson':
            results = exporter.export_to_ndjson(
                output,
                tables=args.tables,
                compress=args.compress
            )

        print_results(results)

    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
