#!/usr/bin/env python3
"""
SQL Query Runner
Run SQL queries against CSV files using pandas SQL backend.
Export results to CSV or JSON.
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Any


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Run SQL queries against CSV files"
    )
    parser.add_argument(
        "query",
        help="SQL query to execute",
    )
    parser.add_argument(
        "-f", "--file",
        help="CSV file to query (alternative to embedding table name in query)",
    )
    parser.add_argument(
        "-t", "--table",
        default="data",
        help="Table name to use in query (default: data)",
    )
    parser.add_argument(
        "-o", "--output",
        help="Output file for results (default: stdout)",
    )
    parser.add_argument(
        "--format",
        choices=["csv", "json", "pretty-json"],
        default="csv",
        help="Output format (default: csv)",
    )
    parser.add_argument(
        "--no-header",
        action="store_true",
        help="CSV output without header row",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show the query without executing",
    )
    parser.add_argument(
        "--encoding",
        default="utf-8",
        help="Input file encoding (default: utf-8)",
    )
    return parser.parse_args()


def check_dependencies() -> bool:
    """Check if required dependencies are installed."""
    try:
        import pandas as pd
        return True
    except ImportError:
        print("Error: pandas is required for SQL query execution", file=sys.stderr)
        print("\nInstall pandas:", file=sys.stderr)
        print("  pip install pandas", file=sys.stderr)
        return False


def read_csv_file(filepath: Path, encoding: str) -> Any:
    """
    Read CSV file using pandas.

    Args:
        filepath: Path to CSV file
        encoding: File encoding

    Returns:
        pandas DataFrame
    """
    try:
        import pandas as pd
        return pd.read_csv(filepath, encoding=encoding)
    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error reading CSV: {e}", file=sys.stderr)
        sys.exit(1)


def execute_query(
    query: str,
    df: Any,
    table_name: str,
    conn: Any,
) -> Any:
    """
    Execute SQL query against DataFrame.

    Args:
        query: SQL query string
        df: pandas DataFrame
        table_name: Name to register table as
        conn: SQL connection

    Returns:
        Query result as DataFrame
    """
    # Register the DataFrame as a table
    conn.register(table_name, df)

    # Execute query
    try:
        result = conn.execute(query)
        return result.df()
    except Exception as e:
        print(f"Error executing query: {e}", file=sys.stderr)
        sys.exit(1)


def output_results(
    result: Any,
    output_path: Path | None,
    output_format: str,
    no_header: bool,
) -> None:
    """
    Output query results.

    Args:
        result: Result DataFrame
        output_path: Output file path or None for stdout
        output_format: Output format (csv, json, pretty-json)
        no_header: Whether to skip header in CSV
    """
    if output_format in ["json", "pretty-json"]:
        # Convert to JSON
        indent = 2 if output_format == "pretty-json" else None

        if output_path:
            result.to_json(output_path, orient="records", indent=indent, force_ascii=False)
        else:
            print(result.to_json(orient="records", indent=indent, force_ascii=False))

    else:  # csv
        if output_path:
            result.to_csv(output_path, index=False, header=not no_header)
        else:
            print(result.to_csv(index=False, header=not no_header))


def main() -> None:
    """Main entry point for SQL query runner."""
    args = parse_args()

    # Check dependencies
    if not check_dependencies():
        sys.exit(1)

    import pandas as pd

    # Try to use duckdb for SQL execution (best experience)
    try:
        import duckdb
        use_duckdb = True
    except ImportError:
        use_duckdb = False

    # If no file provided, check if query contains a table reference
    if not args.file:
        # Query should contain table name
        table_name = args.table
    else:
        # Read the CSV file
        print(f"Reading '{args.file}'...")
        df = read_csv_file(Path(args.file), args.encoding)
        print(f"  Loaded {len(df)} rows with {len(df.columns)} columns")
        print(f"  Columns: {', '.join(df.columns)}")
        table_name = args.table

    # Process query - replace table name placeholder
    query = args.query
    if not use_duckdb and "table_name" not in query.lower():
        # For pandas read_sql, we need to use the table name
        # Just use the query as-is assuming table_name is referenced
        pass

    if args.dry_run:
        print("Query to execute:")
        print(f"  {query}")
        if not args.file:
            print("\nNote: No input file specified. Query will use table name: " + table_name)
        print("\nDry run complete.")
        return

    print(f"Executing query...")

    if use_duckdb:
        # Use DuckDB for full SQL support
        conn = duckdb.connect(database=":memory:")

        if args.file:
            # Register the DataFrame
            conn.register(table_name, df)
        else:
            # Create a sample table for demonstration
            print("Note: No file provided. Creating sample table for demo.")
            print("Use -f option to query your own CSV file.")

        try:
            result = conn.execute(query).df()
        except Exception as e:
            print(f"Error executing query: {e}", file=sys.stderr)
            sys.exit(1)

        conn.close()

    else:
        # Fallback to pandas for basic operations
        # pandas doesn't have full SQL support, so we'll try sqlite3
        try:
            import sqlite3

            if not args.file:
                print("Error: --file is required when duckdb is not installed", file=sys.stderr)
                print("Install duckdb for better SQL support:", file=sys.stderr)
                print("  pip install duckdb", file=sys.stderr)
                sys.exit(1)

            # Create in-memory SQLite database
            conn = sqlite3.connect(":memory:")
            df.to_sql(table_name, conn, index=False, if_exists="replace")

            try:
                result = pd.read_sql_query(query, conn)
            except Exception as e:
                print(f"Error executing query: {e}", file=sys.stderr)
                sys.exit(1)
            finally:
                conn.close()

        except ImportError:
            print("Error: Neither duckdb nor sqlite3 available", file=sys.stderr)
            print("\nInstall duckdb for SQL queries:", file=sys.stderr)
            print("  pip install duckdb", file=sys.stderr)
            sys.exit(1)

    print(f"  Query returned {len(result)} rows")

    # Output results
    output_path = Path(args.output) if args.output else None
    output_results(result, output_path, args.format, args.no_header)

    if output_path:
        print(f"\nResults written to '{output_path}'")

    print("\nDone!")


if __name__ == "__main__":
    main()
