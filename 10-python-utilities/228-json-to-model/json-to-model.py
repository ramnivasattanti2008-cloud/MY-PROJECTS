#!/usr/bin/env python3
"""
JSON to Model Generator - Convert JSON data to typed data models.
Generates Python dataclasses, TypeScript interfaces, or Go structs from JSON input.
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


def infer_type(value: Any) -> tuple[str, str, str]:
    """
    Infer types from JSON value.
    Returns (python_type, typescript_type, go_type).
    """
    if value is None:
        return ("None", "null", "interface{}")
    elif isinstance(value, bool):
        return ("bool", "boolean", "bool")
    elif isinstance(value, int):
        return ("int", "number", "int64")
    elif isinstance(value, float):
        return ("float", "number", "float64")
    elif isinstance(value, str):
        return ("str", "string", "string")
    elif isinstance(value, list):
        if value:
            # Infer from first element
            inner_python, inner_ts, inner_go = infer_type(value[0])
            return (
                f"list[{inner_python}]",
                f"{inner_ts}[]",
                f"[]{inner_go}"
            )
        return ("list[Any]", "unknown[]", "[]interface{}")
    elif isinstance(value, dict):
        if value:
            return ("dict[str, Any]", "Record<string, unknown>", "map[string]interface{}")
        return ("dict[str, Any]", "Record<string, unknown>", "map[string]interface{}")
    return ("Any", "unknown", "interface{}")


def to_pascal_case(name: str) -> str:
    """Convert snake_case to PascalCase."""
    return ''.join(word.title() for word in re.split(r'[_\s]+', name))


def to_camel_case(name: str) -> str:
    """Convert snake_case to camelCase."""
    words = re.split(r'[_\s]+', name)
    return words[0] + ''.join(word.title() for word in words[1:])


def to_snake_case(name: str) -> str:
    """Convert camelCase/PascalCase to snake_case."""
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def generate_python_model(name: str, data: dict, indent: int = 0) -> str:
    """Generate Python dataclass from JSON."""
    lines = []
    base_indent = "    " * indent

    # Collect fields with their types
    fields = []
    nested_classes = []

    for key, value in data.items():
        field_name = to_snake_case(key)
        python_type, _, _ = infer_type(value)

        # Handle nested objects
        if isinstance(value, dict) and value:
            nested_name = to_pascal_case(key)
            nested_code = generate_python_model(nested_name, value, indent + 1)
            nested_classes.append(nested_code)
            fields.append((field_name, nested_name))
        # Handle arrays of objects
        elif isinstance(value, list) and value and isinstance(value[0], dict):
            nested_name = to_pascal_case(to_snake_case(key).rstrip('s'))
            nested_code = generate_python_model(nested_name, value[0], indent + 1)
            nested_classes.append(nested_code)
            fields.append((field_name, f"list[{nested_name}]"))
        else:
            fields.append((field_name, python_type))

    # Generate class
    lines.append(f"{base_indent}@dataclass")
    lines.append(f"{base_indent}class {name}:")
    lines.append(f'{base_indent}    """Data model for {name}."""')

    if fields:
        for field_name, field_type in fields:
            lines.append(f"{base_indent}    {field_name}: {field_type}")
    else:
        lines.append(f"{base_indent}    pass")

    # Add nested classes
    for nested in nested_classes:
        lines.append("")
        lines.append(nested)

    return '\n'.join(lines)


def generate_python_models(name: str, data: dict, root_name: str | None = None) -> str:
    """Generate complete Python module with models."""
    root = root_name or to_pascal_case(name)
    imports = [
        "from dataclasses import dataclass",
        "from typing import Any, Optional"
    ]

    # Check if we need Optional
    has_optional = False
    def check_optional(d):
        for v in d.values():
            if v is None:
                global has_optional
                has_optional = True
            elif isinstance(v, dict):
                check_optional(v)
            elif isinstance(v, list) and v:
                check_optional(v[0]) if isinstance(v[0], dict) else None

    check_optional(data)

    if has_optional:
        imports.append("from typing import Union")

    models = generate_python_model(root, data)

    header = [
        f'"""',
        f'Generated data models from {name}.',
        f'Run: python -c "import json; print(json.dumps(<instance>, indent=2))" to convert.',
        f'"""',
        "",
        "from __future__ import annotations",
        "",
    ] + imports + ["", ""]

    return '\n'.join(header) + models


def generate_typescript_model(name: str, data: dict, indent: int = 0) -> str:
    """Generate TypeScript interface from JSON."""
    lines = []
    base_indent = "    " * indent

    nested_interfaces = []

    for key, value in data.items():
        field_name = to_camel_case(key)

        if isinstance(value, dict) and value:
            # Nested interface
            nested_name = to_pascal_case(key)
            nested_code = generate_typescript_model(nested_name, value, indent + 1)
            nested_interfaces.append(nested_code)

            # Array of objects
            if indent == 0:
                lines.append(f"{base_indent}{field_name}?: {nested_name}[];")
            else:
                lines.append(f"{base_indent}{field_name}: {nested_name};")
        elif isinstance(value, list) and value and isinstance(value[0], dict):
            # Array of objects
            nested_name = to_pascal_case(to_snake_case(key).rstrip('s'))
            nested_code = generate_typescript_model(nested_name, value[0], indent + 1)
            nested_interfaces.append(nested_code)
            lines.append(f"{base_indent}{field_name}?: {nested_name}[];")
        elif isinstance(value, list):
            inner_type, _, _ = infer_type(value)
            lines.append(f"{base_indent}{field_name}?: {inner_type};")
        elif isinstance(value, dict):
            lines.append(f"{base_indent}{field_name}?: Record<string, unknown>;")
        else:
            ts_type, _, _ = infer_type(value)
            lines.append(f"{base_indent}{field_name}?: {ts_type};")

    result = [f"export interface {name} {{"]
    result.extend(lines)
    result.append("}")

    # Add nested interfaces
    if nested_interfaces:
        result.append("")
        result.extend(nested_interfaces)

    return '\n'.join(result)


def generate_typescript_models(name: str, data: dict, root_name: str | None = None) -> str:
    """Generate complete TypeScript module with interfaces."""
    root = root_name or to_pascal_case(name)

    header = [
        f"// Generated from {name}",
        f"// Run: npx ts-node model.ts < instance.json",
        "",
    ]

    models = generate_typescript_model(root, data)

    return '\n'.join(header) + '\n' + models


def generate_go_model(name: str, data: dict, indent: int = 0) -> str:
    """Generate Go struct from JSON."""
    lines = []
    base_indent = "    " * indent

    nested_structs = []

    for key, value in data.items():
        field_name = to_pascal_case(key)
        field_json = to_snake_case(key)
        go_type, _, _ = infer_type(value)

        if isinstance(value, dict) and value:
            # Nested struct
            nested_name = to_pascal_case(key)
            nested_code = generate_go_model(nested_name, value, indent + 1)
            nested_structs.append(nested_code)
            lines.append(f"{base_indent}{field_name} {nested_name} `json:\"{field_json}\"`")
        elif isinstance(value, list) and value and isinstance(value[0], dict):
            # Array of structs
            nested_name = to_pascal_case(to_snake_case(key).rstrip('s'))
            if not any(f"type {nested_name} struct" in s for s in nested_structs):
                nested_code = generate_go_model(nested_name, value[0], indent + 1)
                nested_structs.append(nested_code)
            lines.append(f"{base_indent}{field_name} []*{nested_name} `json:\"{field_json}\"`")
        elif isinstance(value, list):
            lines.append(f"{base_indent}{field_name} {go_type} `json:\"{field_json}\"`")
        elif isinstance(value, dict):
            lines.append(f"{base_indent}{field_name} map[string]interface{} `json:\"{field_json}\"`")
        else:
            lines.append(f"{base_indent}{field_name} {go_type} `json:\"{field_json}\"`")

    result = [f"type {name} struct {{"]
    result.extend(lines)
    result.append("}")

    # Add nested structs
    if nested_structs:
        result.append("")
        result.extend(nested_structs)

    return '\n'.join(result)


def generate_go_models(name: str, data: dict, root_name: str | None = None) -> str:
    """Generate complete Go module with structs."""
    root = root_name or to_pascal_case(name)

    header = [
        f"// Generated from {name}",
        f"// Run: cat model.go | go run",
        "",
        "package models",
        "",
    ]

    models = generate_go_model(root, data)

    return '\n'.join(header) + '\n' + models


def load_json(input_path: str) -> tuple[str, dict]:
    """Load JSON from file or stdin."""
    if input_path == '-':
        content = sys.stdin.read()
        return ('stdin', json.loads(content))
    else:
        path = Path(input_path)
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return (path.stem, data)


def main():
    parser = argparse.ArgumentParser(
        description="JSON to Model Generator - Convert JSON to Python/TypeScript/Go models",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s data.json --python -o models.py
  %(prog)s data.json --typescript -o models.ts
  %(prog)s data.json --go -o models.go
  cat data.json | %(prog)s - --python
  %(prog)s data.json --python --class-name CustomName
        """
    )

    parser.add_argument(
        'input',
        nargs='?',
        default='-',
        help='Input JSON file (or - for stdin)'
    )

    parser.add_argument(
        '-p', '--python',
        action='store_true',
        help='Generate Python dataclasses'
    )

    parser.add_argument(
        '-t', '--typescript',
        action='store_true',
        help='Generate TypeScript interfaces'
    )

    parser.add_argument(
        '-g', '--go',
        action='store_true',
        help='Generate Go structs'
    )

    parser.add_argument(
        '-c', '--class-name',
        help='Custom name for root model (default: inferred from filename)'
    )

    parser.add_argument(
        '-o', '--output',
        help='Output file (default: stdout)'
    )

    parser.add_argument(
        '-a', '--all',
        action='store_true',
        help='Generate all language outputs as separate files'
    )

    args = parser.parse_args()

    # Default to Python if no format specified
    if not any([args.python, args.typescript, args.go, args.all]):
        args.python = True

    # Load JSON
    try:
        name, data = load_json(args.input)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON: {e}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print(f"Error: File not found: {args.input}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error loading JSON: {e}", file=sys.stderr)
        sys.exit(1)

    # Ensure data is a dict (not array)
    if isinstance(data, list):
        if data and isinstance(data[0], dict):
            data = {"items": data[0]}
        else:
            data = {"items": data}

    outputs = {}

    if args.all:
        outputs = {
            'py': ('models.py', generate_python_models(name, data, args.class_name)),
            'ts': ('models.ts', generate_typescript_models(name, data, args.class_name)),
            'go': ('models.go', generate_go_models(name, data, args.class_name))
        }
    else:
        if args.python:
            outputs['py'] = ('models.py', generate_python_models(name, data, args.class_name))
        if args.typescript:
            outputs['ts'] = ('models.ts', generate_typescript_models(name, data, args.class_name))
        if args.go:
            outputs['go'] = ('models.go', generate_go_models(name, data, args.class_name))

    # Write output
    if args.output and not args.all:
        output_name, output_code = list(outputs.values())[0]
        output_path = Path(args.output)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(output_code)
        print(f"Generated: {output_path}")
    else:
        for ext, (filename, code) in outputs.items():
            print(f"\n{'='*60}")
            print(f"=== {filename} ===")
            print('='*60)
            print(code)

        if args.all:
            for ext, (filename, code) in outputs.items():
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(code)
            print(f"\nGenerated {len(outputs)} files.")


if __name__ == '__main__':
    main()
