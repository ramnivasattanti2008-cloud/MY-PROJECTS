#!/usr/bin/env python3
"""
CSV Analyzer - Analyze and summarize CSV files.

This script provides comprehensive analysis of CSV files including:
- Column type detection (string, integer, float, date, boolean)
- Missing value analysis
- Statistical summaries for numeric columns
- Duplicate row detection
- Data quality scoring

Educational Purpose:
- Demonstrates pandas data analysis fundamentals
- Shows type inference techniques
- Illustrates descriptive statistics calculations
- Teaches data quality assessment

Author: Educational Example
License: MIT
"""

import argparse
import csv
import json
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    import pandas as pd
except ImportError:
    print("Error: pandas library not installed.")
    print("Run: pip install pandas openpyxl")
    sys.exit(1)


class CSVAnalyzer:
    """
    Comprehensive CSV file analyzer.

    Provides statistical analysis, data quality metrics, and exportable reports
    for any CSV file.
    """

    def __init__(self, file_path: str):
        """
        Initialize the analyzer with a CSV file.

        Args:
            file_path: Path to the CSV file to analyze
        """
        self.file_path = Path(file_path)

        if not self.file_path.exists():
            raise FileNotFoundError(f"File not found: {self.file_path}")

        try:
            # Try different encodings and delimiters
            self.df = self._read_csv()
        except Exception as e:
            raise ValueError(f"Error reading CSV file: {e}")

        self.analysis = {}

    def _read_csv(self) -> pd.DataFrame:
        """Attempt to read CSV with various encodings and delimiters."""
        encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
        delimiters = [',', ';', '\t', '|']

        for encoding in encodings:
            for delimiter in delimiters:
                try:
                    return pd.read_csv(
                        self.file_path,
                        encoding=encoding,
                        delimiter=delimiter,
                        on_bad_lines='warn'
                    )
                except (UnicodeDecodeError, pd.errors.ParserError):
                    continue

        raise ValueError("Could not read CSV with any encoding/delimiter combination")

    def analyze(self) -> dict:
        """
        Perform complete analysis of the CSV file.

        Returns:
            Dictionary containing all analysis results
        """
        print("Analyzing CSV file...")
        print(f"  File: {self.file_path.name}")
        print(f"  Rows: {len(self.df):,}")
        print(f"  Columns: {len(self.df.columns)}")

        self.analysis = {
            'file_info': self._analyze_file_info(),
            'column_types': self._analyze_column_types(),
            'missing_values': self._analyze_missing_values(),
            'statistics': self._analyze_statistics(),
            'duplicates': self._analyze_duplicates(),
            'unique_values': self._analyze_unique_values(),
            'data_quality': self._calculate_quality_score(),
        }

        return self.analysis

    def _analyze_file_info(self) -> dict:
        """Get basic file information."""
        return {
            'file_name': self.file_path.name,
            'file_size_bytes': self.file_path.stat().st_size,
            'total_rows': len(self.df),
            'total_columns': len(self.df.columns),
            'column_names': list(self.df.columns),
            'memory_usage_mb': self.df.memory_usage(deep=True).sum() / 1024 / 1024,
        }

    def _analyze_column_types(self) -> dict:
        """
        Detect and classify column types.

        Type hierarchy: date > float > integer > boolean > datetime > string
        """
        type_mapping = {}

        for col in self.df.columns:
            dtype = self.df[col].dtype

            # Try to infer the best type
            inferred_type = self._infer_column_type(self.df[col])

            type_mapping[col] = {
                'pandas_dtype': str(dtype),
                'inferred_type': inferred_type,
                'sample_values': self.df[col].dropna().head(3).tolist(),
            }

        return type_mapping

    def _infer_column_type(self, series: pd.Series) -> str:
        """Infer the logical type of a column."""
        non_null = series.dropna()

        if len(non_null) == 0:
            return 'empty'

        # Check for boolean
        unique_vals = non_null.unique()
        if set(str(v).lower() for v in unique_vals).issubset({'true', 'false', '1', '0', 'yes', 'no'}):
            if len(unique_vals) <= 2:
                return 'boolean'

        # Check for integer
        try:
            non_null.astype(int)
            if all(float(v).is_integer() for v in non_null if pd.notna(v)):
                return 'integer'
        except (ValueError, TypeError):
            pass

        # Check for float
        try:
            non_null.astype(float)
            return 'float'
        except (ValueError, TypeError):
            pass

        # Check for date/datetime
        if self._looks_like_date(series):
            return 'date'

        return 'string'

    def _looks_like_date(self, series: pd.Series) -> bool:
        """Check if a column looks like dates."""
        date_patterns = [
            '%Y-%m-%d', '%d/%m/%Y', '%m/%d/%Y', '%Y/%m/%d',
            '%d-%m-%Y', '%m-%d-%Y', '%Y%m%d', '%d.%m.%Y',
        ]

        sample = series.dropna().head(20)
        date_count = 0

        for val in sample:
            val_str = str(val)
            for pattern in date_patterns:
                try:
                    datetime.strptime(val_str, pattern)
                    date_count += 1
                    break
                except ValueError:
                    continue

        return date_count >= len(sample) * 0.8

    def _analyze_missing_values(self) -> dict:
        """Analyze missing values in each column."""
        missing_info = {}

        for col in self.df.columns:
            total = len(self.df)
            missing = self.df[col].isna().sum()
            empty_strings = (self.df[col] == '').sum() if self.df[col].dtype == 'object' else 0

            missing_info[col] = {
                'missing_count': int(missing),
                'missing_percent': round(missing / total * 100, 2),
                'empty_string_count': int(empty_strings),
                'present_count': int(total - missing),
                'data_type': str(self.df[col].dtype),
            }

        # Overall missing data summary
        total_cells = self.df.shape[0] * self.df.shape[1]
        total_missing = self.df.isna().sum().sum()

        missing_info['_summary'] = {
            'total_cells': total_cells,
            'total_missing': int(total_missing),
            'overall_missing_percent': round(total_missing / total_cells * 100, 2),
            'columns_with_missing': sum(1 for c in self.df.columns if self.df[c].isna().any()),
        }

        return missing_info

    def _analyze_statistics(self) -> dict:
        """Calculate statistics for all columns."""
        stats = {}

        for col in self.df.columns:
            col_stats = {
                'count': int(self.df[col].count()),
                'unique_count': int(self.df[col].nunique()),
            }

            # Numeric statistics
            if pd.api.types.is_numeric_dtype(self.df[col]):
                numeric_data = self.df[col].dropna()
                if len(numeric_data) > 0:
                    col_stats.update({
                        'mean': round(float(numeric_data.mean()), 4),
                        'median': round(float(numeric_data.median()), 4),
                        'std': round(float(numeric_data.std()), 4),
                        'min': float(numeric_data.min()),
                        'max': float(numeric_data.max()),
                        'q25': float(numeric_data.quantile(0.25)),
                        'q75': float(numeric_data.quantile(0.75)),
                    })

            # String statistics
            elif self.df[col].dtype == 'object':
                str_data = self.df[col].dropna().astype(str)
                if len(str_data) > 0:
                    lengths = str_data.str.len()
                    col_stats.update({
                        'min_length': int(lengths.min()),
                        'max_length': int(lengths.max()),
                        'avg_length': round(float(lengths.mean()), 2),
                        'most_common': dict(Counter(str_data).most_common(5)),
                    })

            stats[col] = col_stats

        return stats

    def _analyze_duplicates(self) -> dict:
        """Analyze duplicate rows."""
        total_rows = len(self.df)
        duplicate_rows = self.df.duplicated().sum()
        duplicate_cols = self.df.duplicated(subset=list(self.df.columns)).sum()

        # Find columns that uniquely identify rows
        potential_keys = []
        for col in self.df.columns:
            if self.df[col].nunique() == total_rows:
                potential_keys.append(col)

        return {
            'total_rows': total_rows,
            'duplicate_rows': int(duplicate_rows),
            'duplicate_percent': round(duplicate_rows / total_rows * 100, 2),
            'potential_primary_keys': potential_keys,
            'first_duplicate_index': int(self.df.duplicated().idxmax()) if duplicate_rows > 0 else None,
        }

    def _analyze_unique_values(self) -> dict:
        """Analyze unique values for categorical columns."""
        unique_info = {}

        for col in self.df.columns:
            unique_count = self.df[col].nunique()
            total = len(self.df)

            # Only show details for low-cardinality columns
            if unique_count <= 50 and unique_count > 0:
                value_counts = self.df[col].value_counts().head(20)
                unique_info[col] = {
                    'unique_count': int(unique_count),
                    'cardinality_percent': round(unique_count / total * 100, 2),
                    'top_values': {
                        str(k): int(v) for k, v in value_counts.items()
                    },
                    'is_low_cardinality': True,
                }
            else:
                unique_info[col] = {
                    'unique_count': int(unique_count),
                    'cardinality_percent': round(unique_count / total * 100, 2),
                    'is_low_cardinality': False,
                }

        return unique_info

    def _calculate_quality_score(self) -> dict:
        """
        Calculate an overall data quality score (0-100).

        Factors:
        - Completeness (missing values)
        - Uniqueness (duplicates)
        - Consistency (type consistency)
        """
        scores = {}
        issues = []

        # Completeness score (40% weight)
        total_cells = self.df.shape[0] * self.df.shape[1]
        missing_cells = self.df.isna().sum().sum()
        completeness = (1 - missing_cells / total_cells) * 100
        scores['completeness'] = round(completeness, 2)
        if completeness < 80:
            issues.append(f"High missing value rate: {100 - completeness:.1f}%")

        # Uniqueness score (30% weight)
        dup_percent = self.df.duplicated().sum() / len(self.df) * 100
        uniqueness = max(0, 100 - dup_percent)
        scores['uniqueness'] = round(uniqueness, 2)
        if dup_percent > 10:
            issues.append(f"High duplicate rate: {dup_percent:.1f}%")

        # Type consistency score (30% weight)
        # Check if columns have consistent types
        type_consistency = 100
        for col in self.df.columns:
            sample = self.df[col].dropna().head(100)
            # Simple check: can all values be converted to same type
            if len(sample) > 0:
                try:
                    sample.astype(float)
                except (ValueError, TypeError):
                    try:
                        len(sample.astype(str).str.len().unique()) / len(sample)
                    except:
                        pass

        scores['type_consistency'] = round(type_consistency, 2)

        # Overall score
        overall = (
            scores['completeness'] * 0.4 +
            scores['uniqueness'] * 0.3 +
            scores['type_consistency'] * 0.3
        )
        scores['overall'] = round(overall, 2)
        scores['grade'] = self._get_grade(overall)
        scores['issues'] = issues

        return scores

    def _get_grade(self, score: float) -> str:
        """Convert numeric score to letter grade."""
        if score >= 90:
            return 'A'
        elif score >= 80:
            return 'B'
        elif score >= 70:
            return 'C'
        elif score >= 60:
            return 'D'
        else:
            return 'F'

    def print_report(self):
        """Print a formatted analysis report to console."""
        if not self.analysis:
            self.analyze()

        a = self.analysis
        fi = a['file_info']
        mv = a['missing_values']
        dup = a['duplicates']
        dq = a['data_quality']

        print("\n" + "=" * 60)
        print("CSV ANALYSIS REPORT")
        print("=" * 60)

        # File Info
        print(f"\n📄 FILE INFORMATION")
        print(f"   Name: {fi['file_name']}")
        print(f"   Size: {fi['file_size_bytes']:,} bytes ({fi['file_size_bytes']/1024:.1f} KB)")
        print(f"   Memory: {fi['memory_usage_mb']:.2f} MB")
        print(f"   Rows: {fi['total_rows']:,}")
        print(f"   Columns: {fi['total_columns']}")

        # Columns
        print(f"\n📊 COLUMNS")
        print(f"   {', '.join(fi['column_names'])}")

        # Data Types
        print(f"\n📋 COLUMN TYPES")
        for col, info in a['column_types'].items():
            sample = info['sample_values'][:2]
            sample_str = ', '.join(str(s)[:20] for s in sample)
            print(f"   {col}: {info['inferred_type']} (e.g., {sample_str})")

        # Missing Values
        print(f"\n❓ MISSING VALUES")
        cols_with_missing = [c for c in mv if c != '_summary' and mv[c]['missing_count'] > 0]
        if cols_with_missing:
            for col in cols_with_missing:
                m = mv[col]
                print(f"   {col}: {m['missing_count']:,} ({m['missing_percent']}%)")
        else:
            print("   No missing values found!")

        summary = mv['_summary']
        print(f"   Overall: {summary['total_missing']:,} cells ({summary['overall_missing_percent']}%)")

        # Duplicates
        print(f"\n🔄 DUPLICATES")
        print(f"   Total duplicates: {dup['duplicate_rows']:,} ({dup['duplicate_percent']}%)")
        if dup['potential_primary_keys']:
            print(f"   Unique identifiers: {', '.join(dup['potential_primary_keys'])}")

        # Data Quality
        print(f"\n✅ DATA QUALITY")
        print(f"   Overall Score: {dq['overall']}/100 (Grade: {dq['grade']})")
        print(f"   Completeness: {dq['completeness']}/100")
        print(f"   Uniqueness: {dq['uniqueness']}/100")
        print(f"   Type Consistency: {dq['type_consistency']}/100")

        if dq['issues']:
            print(f"\n⚠️  ISSUES FOUND:")
            for issue in dq['issues']:
                print(f"   - {issue}")

        # Statistics
        print(f"\n📈 STATISTICS (Numeric Columns)")
        for col, stats in a['statistics'].items():
            if 'mean' in stats:
                print(f"\n   {col}:")
                print(f"      Mean: {stats['mean']}, Median: {stats['median']}")
                print(f"      Std Dev: {stats['std']}")
                print(f"      Range: [{stats['min']}, {stats['max']}]")
                print(f"      IQR: [{stats['q25']}, {stats['q75']}]")

        print("\n" + "=" * 60)

    def export_report(self, output_path: str, format: str = 'json'):
        """
        Export analysis report to file.

        Args:
            output_path: Path for the output file
            format: 'json' or 'txt'
        """
        if not self.analysis:
            self.analyze()

        output_path = Path(output_path)

        if format == 'json':
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(self.analysis, f, indent=2, default=str)
        else:
            # Export as text report
            self._export_text_report(output_path)

        print(f"Report exported: {output_path}")

    def _export_text_report(self, output_path: Path):
        """Export analysis as formatted text."""
        import io
        from contextlib import redirect_stdout

        buffer = io.StringIO()
        with redirect_stdout(buffer):
            self.print_report()

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(buffer.getvalue())


def main():
    """Main entry point with CLI argument parsing."""
    parser = argparse.ArgumentParser(
        description='Analyze and summarize CSV files.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Analyze a CSV file and print report:
    python csv-analyzer.py data.csv

  Export report as JSON:
    python csv-analyzer.py data.csv -o report.json

  Export report as text:
    python csv-analyzer.py data.csv -o report.txt --format txt

  Quick stats only:
    python csv-analyzer.py data.csv --quick
        """
    )

    parser.add_argument('file', help='Path to the CSV file')
    parser.add_argument('-o', '--output', help='Output file for the report')
    parser.add_argument('--format', choices=['json', 'txt'], default='json',
                        help='Output format (default: json)')
    parser.add_argument('--quick', action='store_true',
                        help='Show quick stats only (skip detailed analysis)')

    args = parser.parse_args()

    try:
        analyzer = CSVAnalyzer(args.file)

        if args.quick:
            # Quick analysis
            print(f"\n📊 Quick Stats for: {analyzer.file_path.name}")
            print(f"   Rows: {len(analyzer.df):,}")
            print(f"   Columns: {len(analyzer.df.columns)}")
            print(f"   Missing: {analyzer.df.isna().sum().sum():,}")
            print(f"   Duplicates: {analyzer.df.duplicated().sum():,}")
        else:
            analyzer.analyze()
            analyzer.print_report()

            if args.output:
                analyzer.export_report(args.output, args.format)

    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
