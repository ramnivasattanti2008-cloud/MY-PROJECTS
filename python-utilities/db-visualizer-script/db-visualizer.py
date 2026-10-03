"""
Database Visualizer - Generate ASCII ER diagrams from SQLite databases.

Displays database schema as an ASCII art diagram showing tables, columns,
data types, keys, and relationships (foreign keys).
"""

import argparse
import sqlite3
import sys
from collections import defaultdict


class DatabaseVisualizer:
    """Generates ASCII ER diagrams from SQLite databases."""

    # Box drawing characters
    CHARS = {
        'top_left': '+',
        'top_right': '+',
        'bottom_left': '+',
        'bottom_right': '+',
        'horizontal': '-',
        'vertical': '|',
        'left_tee': '+',
        'right_tee': '+',
        'top_tee': '+',
        'bottom_tee': '+',
        'cross': '+',
        'plus': '+',
        'minus': '-',
        'arrow_left': '<',
        'arrow_right': '>',
    }

    # Box drawing with unicode characters (modern terminals)
    UNICODE_CHARS = {
        'top_left': '┌',
        'top_right': '┐',
        'bottom_left': '└',
        'bottom_right': '┘',
        'horizontal': '─',
        'vertical': '│',
        'left_tee': '├',
        'right_tee': '┤',
        'top_tee': '┬',
        'bottom_tee': '┘',  # Using close approximation
        'cross': '┼',
        'plus': '┼',
        'minus': '─',
        'arrow_left': '◀',
        'arrow_right': '▶',
    }

    def __init__(self, database_path, use_unicode=True, show_row_counts=True):
        """Initialize visualizer with database path."""
        self.database_path = database_path
        self.use_unicode = use_unicode and self._supports_unicode()
        self.show_row_counts = show_row_counts
        self.chars = self.UNICODE_CHARS if self.use_unicode else self.CHARS
        self.tables = {}
        self.foreign_keys = []
        self.relationships = []

    def _supports_unicode(self):
        """Check if terminal supports unicode."""
        try:
            return sys.stdout.encoding.lower().startswith('utf')
        except:
            return False

    def _connect(self):
        """Get database connection."""
        return sqlite3.connect(self.database_path)

    def load_schema(self):
        """Load all schema information from the database."""
        conn = self._connect()
        cursor = conn.cursor()

        # Get all tables
        cursor.execute("""
            SELECT name FROM sqlite_master
            WHERE type='table' AND name NOT LIKE 'sqlite_%'
            ORDER BY name
        """)
        table_names = [row[0] for row in cursor.fetchall()]

        for table_name in table_names:
            # Get table info
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = [dict(row) for row in cursor.fetchall()]

            # Get foreign keys
            cursor.execute(f"PRAGMA foreign_key_list({table_name})")
            fks = [dict(row) for row in cursor.fetchall()]

            # Get row count
            if self.show_row_counts:
                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                row_count = cursor.fetchone()[0]
            else:
                row_count = None

            self.tables[table_name] = {
                'columns': columns,
                'foreign_keys': fks,
                'row_count': row_count
            }

            # Store relationships
            for fk in fks:
                self.relationships.append({
                    'from_table': table_name,
                    'from_column': fk['from'],
                    'to_table': fk['table'],
                    'to_column': fk['to'],
                    'on_update': fk['on_update'],
                    'on_delete': fk['on_delete']
                })

        conn.close()

    def _get_column_width(self, column):
        """Calculate display width for a column."""
        name = column['name']
        col_type = column['type'] or 'TEXT'

        # Account for type, null indicator, and key indicator
        extra = 0
        if column['notnull']:
            extra += 1  # asterisk
        if column['pk']:
            extra += 4  # [PK]

        return max(len(name), len(col_type) + extra)

    def _draw_table(self, table_name, max_width):
        """Draw a single table as ASCII box."""
        table = self.tables[table_name]
        columns = table['columns']

        lines = []
        h = self.chars['horizontal']

        # Table header
        header = f" {table_name} "
        if table['row_count'] is not None:
            header += f"({table['row_count']} rows)"

        lines.append(self.chars['top_left'] + h * (max_width + 2) + self.chars['top_right'])
        lines.append(f"{self.chars['vertical']}{header.center(max_width + 2)}{self.chars['vertical']}")
        lines.append(self.chars['left_tee'] + h * (max_width + 2) + self.chars['right_tee'])

        # Columns
        for col in columns:
            name = col['name']
            col_type = col['type'] or 'TEXT'
            flags = ''

            if col['pk']:
                flags = ' [PK]'
            elif col['notnull']:
                flags = ' *'

            line = f"{self.chars['vertical']} {name.ljust(max_width)}{col_type[-10:].rjust(10)}{flags}{self.chars['vertical']}"
            lines.append(line)

        lines.append(self.chars['bottom_left'] + h * (max_width + 2) + self.chars['bottom_right'])

        return lines

    def _calculate_max_width(self):
        """Calculate maximum column name width across all tables."""
        max_width = 0
        for table_name, table in self.tables.items():
            for col in table['columns']:
                width = self._get_column_width(col)
                max_width = max(max_width, width)

        # Include table name width
        max_width = max(max_width, max(len(name) for name in self.tables.keys()))

        return max_width

    def _draw_relationships(self, table_positions):
        """Draw relationship lines between tables."""
        if not self.relationships:
            return []

        lines = []

        for rel in self.relationships:
            from_pos = table_positions.get(rel['from_table'])
            to_pos = table_positions.get(rel['to_table'])

            if not from_pos or not to_pos:
                continue

            # Draw connection
            lines.append(f"{' '*from_pos['x']}\\  FK: {rel['from_column']} -> {rel['to_table']}.{rel['to_column']}")

        return lines

    def render(self):
        """Render the complete ER diagram."""
        if not self.tables:
            self.load_schema()

        if not self.tables:
            return "No tables found in database."

        output = []

        # Title
        output.append("")
        output.append(f" Database: {self.database_path}")
        output.append(f" Tables: {len(self.tables)}")
        output.append(f" Relationships: {len(self.relationships)}")
        output.append("")

        # Draw each table
        max_width = self._calculate_max_width()

        table_positions = {}
        current_x = 0

        # Calculate positions for relationship lines
        for table_name in self.tables.keys():
            table_lines = self._draw_table(table_name, max_width)
            table_positions[table_name] = {
                'x': current_x,
                'height': len(table_lines)
            }
            current_x += max_width + 10

        # Draw all tables side by side
        table_heights = {name: len(self._draw_table(name, max_width))
                        for name in self.tables.keys()}
        max_height = max(table_heights.values()) if table_heights else 0

        for row_idx in range(max_height):
            line_parts = []
            for table_name in self.tables.keys():
                table_lines = self._draw_table(table_name, max_width)
                if row_idx < len(table_lines):
                    line_parts.append(table_lines[row_idx])
                else:
                    line_parts.append(' ' * (max_width + 20))

                # Add spacing between tables
                if self.use_unicode:
                    line_parts.append('    ')
                else:
                    line_parts.append('    ')

            output.append(''.join(line_parts))

        # Draw relationships legend
        if self.relationships:
            output.append("")
            output.append("Relationships (Foreign Keys):")
            output.append("-" * 40)

            for rel in self.relationships:
                action = f"ON {rel['on_update']}/{rel['on_delete']}"
                output.append(
                    f"  {rel['from_table']}.{rel['from_column']} "
                    f"-> {rel['to_table']}.{rel['to_column']} [{action}]"
                )

        # Draw full schema
        output.append("")
        output.append("=" * 60)
        output.append("DETAILED SCHEMA")
        output.append("=" * 60)
        output.append("")

        for table_name in sorted(self.tables.keys()):
            table = self.tables[table_name]
            output.append(f"TABLE: {table_name}")

            if table['row_count'] is not None:
                output.append(f"  Rows: {table['row_count']}")

            output.append("  Columns:")

            for col in table['columns']:
                flags = []
                if col['pk']:
                    flags.append('PRIMARY KEY')
                if col['notnull']:
                    flags.append('NOT NULL')
                if col['dflt_value'] is not None:
                    flags.append(f'DEFAULT: {col["dflt_value"]}')

                flag_str = f" ({', '.join(flags)})" if flags else ""
                output.append(f"    {col['name']}: {col['type'] or 'TEXT'}{flag_str}")

            if table['foreign_keys']:
                output.append("  Foreign Keys:")
                for fk in table['foreign_keys']:
                    output.append(
                        f"    {fk['from']} -> {fk['table']}.{fk['to']} "
                        f"({fk['on_update']}/{fk['on_delete']})"
                    )

            output.append("")

        return '\n'.join(output)

    def render_compact(self):
        """Render a compact single-line per table view."""
        if not self.tables:
            self.load_schema()

        if not self.tables:
            return "No tables found in database."

        output = []
        output.append("")

        for table_name in sorted(self.tables.keys()):
            table = self.tables[table_name]
            columns = [col['name'] for col in table['columns']]

            row_info = f" ({table['row_count']} rows)" if table['row_count'] else ""
            cols_str = ', '.join(columns)

            output.append(f"{table_name}{row_info}: {cols_str}")

        return '\n'.join(output)

    def render_html(self):
        """Generate HTML representation of the schema."""
        if not self.tables:
            self.load_schema()

        html = ['<html><head><style>']
        html.append('body { font-family: monospace; background: #1a1a1a; color: #e0e0e0; padding: 20px; }')
        html.append('table { border-collapse: collapse; margin: 20px 0; }')
        html.append('th, td { border: 1px solid #444; padding: 8px 12px; text-align: left; }')
        html.append('th { background: #333; color: #fff; }')
        html.append('tr:hover { background: #2a2a2a; }')
        html.append('.pk { color: #ffd700; }')
        html.append('.fk { color: #00bfff; }')
        html.append('.null { color: #888; }')
        html.append('</style></head><body>')

        html.append(f'<h2>Database: {self.database_path}</h2>')
        html.append(f'<p>Tables: {len(self.tables)} | Relationships: {len(self.relationships)}</p>')

        for table_name in sorted(self.tables.keys()):
            table = self.tables[table_name]

            html.append(f'<h3>{table_name}')
            if table['row_count'] is not None:
                html.append(f' <small>({table["row_count"]} rows)</small>')
            html.append('</h3>')

            html.append('<table>')
            html.append('<thead><tr><th>Column</th><th>Type</th><th>Constraints</th></tr></thead>')
            html.append('<tbody>')

            for col in table['columns']:
                constraints = []
                if col['pk']:
                    constraints.append('<span class="pk">PK</span>')
                if col['notnull']:
                    constraints.append('<span class="null">NOT NULL</span>')
                if col['dflt_value']:
                    constraints.append(f'DEFAULT: {col["dflt_value"]}')

                # Check if this is a foreign key
                for fk in table['foreign_keys']:
                    if fk['from'] == col['name']:
                        constraints.append(
                            f'<span class="fk">FK -> {fk["table"]}.{fk["to"]}</span>'
                        )

                html.append(f'<tr>')
                html.append(f'<td>{col["name"]}</td>')
                html.append(f'<td>{col["type"] or "TEXT"}</td>')
                html.append(f'<td>{" ".join(constraints)}</td>')
                html.append(f'</tr>')

            html.append('</tbody></table>')

        html.append('</body></html>')
        return '\n'.join(html)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Visualize SQLite database schema as ASCII ER diagram',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument('database', help='Path to SQLite database')
    parser.add_argument('--compact', '-c', action='store_true',
                        help='Show compact single-line view')
    parser.add_argument('--html', action='store_true',
                        help='Output as HTML')
    parser.add_argument('--no-unicode', '-a', action='store_true',
                        help='Use ASCII characters only (no Unicode)')
    parser.add_argument('--no-row-counts', '-n', action='store_true',
                        help='Hide row counts')
    parser.add_argument('--output', '-o',
                        help='Save output to file')

    args = parser.parse_args()

    visualizer = DatabaseVisualizer(
        args.database,
        use_unicode=not args.no_unicode,
        show_row_counts=not args.no_row_counts
    )

    if args.html:
        output = visualizer.render_html()
    elif args.compact:
        output = visualizer.render_compact()
    else:
        output = visualizer.render()

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output)
        print(f"Output saved to {args.output}")
    else:
        print(output)


if __name__ == '__main__':
    main()
