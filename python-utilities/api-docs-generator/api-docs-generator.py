#!/usr/bin/env python3
"""
API Documentation Generator - Scan Python files and auto-generate API docs from docstrings.
Extracts function signatures, docstrings, and type hints to create comprehensive documentation.
"""

import argparse
import ast
import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class FunctionDoc:
    """Represents a documented function."""
    name: str
    signature: str
    docstring: str
    decorators: list[str] = field(default_factory=list)
    decorators_doc: dict[str, str] = field(default_factory=dict)
    line_number: int = 0


@dataclass
class ClassDoc:
    """Represents a documented class."""
    name: str
    docstring: str
    methods: list[FunctionDoc] = field(default_factory=list)
    decorators: list[str] = field(default_factory=list)
    line_number: int = 0


@dataclass
class ModuleDoc:
    """Represents a documented module."""
    path: Path
    module_name: str
    docstring: str
    classes: list[ClassDoc] = field(default_factory=list)
    functions: list[FunctionDoc] = field(default_factory=list)


def parse_decorator(decorator: ast.expr) -> str | None:
    """Extract decorator name from AST node."""
    if isinstance(decorator, ast.Name):
        return decorator.id
    elif isinstance(decorator, ast.Call):
        if isinstance(decorator.func, ast.Name):
            return decorator.func.id
        elif isinstance(decorator.func, ast.Attribute):
            return decorator.func.attr
    elif isinstance(decorator, ast.Attribute):
        return decorator.attr
    return None


def get_decorator_signature(decorator: ast.expr) -> str:
    """Get decorator signature as string."""
    try:
        return ast.unparse(decorator)
    except Exception:
        if isinstance(decorator, ast.Call):
            func = decorator.func
            if isinstance(func, ast.Name):
                args = [ast.unparse(a) for a in decorator.args]
                kwargs = [f"{kw.arg}={ast.unparse(kw.value)}" for kw in decorator.keywords]
                all_args = args + kwargs
                return f"@{func.id}({', '.join(all_args)})"
        return "@decorator"
    return "@decorator"


def get_function_signature(func: ast.FunctionDef | ast.AsyncFunctionDef) -> str:
    """Generate function signature string."""
    args = func.args

    # Get argument names with defaults
    arg_parts = []

    # Positional args
    pos_args = list(args.args)
    defaults = list(args.defaults)

    # Calculate offset for defaults
    num_defaults = len(defaults)
    num_args = len(pos_args)

    for i, arg in enumerate(pos_args):
        arg_name = arg.arg

        # Add annotation if present
        if arg.annotation:
            try:
                annotation = ast.unparse(arg.annotation)
                arg_name = f"{arg_name}: {annotation}"
            except Exception:
                pass

        # Add default value if present
        default_idx = i - (num_args - num_defaults)
        if default_idx >= 0 and default_idx < len(defaults):
            try:
                default = ast.unparse(defaults[default_idx])
                arg_name = f"{arg_name}={default}"
            except Exception:
                pass

        arg_parts.append(arg_name)

    # *args
    if args.vararg:
        vararg = f"*{args.vararg.arg}"
        if args.vararg.annotation:
            try:
                vararg += f": {ast.unparse(args.vararg.annotation)}"
            except Exception:
                pass
        arg_parts.append(vararg)

    # **kwargs
    if args.kwarg:
        kwarg = f"**{args.kwarg.arg}"
        if args.kwarg.annotation:
            try:
                kwarg += f": {ast.unparse(args.kwarg.annotation)}"
            except Exception:
                pass
        arg_parts.append(kwarg)

    # Keyword-only args
    for kw in args.kwonlyargs:
        kw_name = kw.arg
        if kw.annotation:
            try:
                kw_name += f": {ast.unparse(kw.annotation)}"
            except Exception:
                pass
        if kw in args.kw_defaults:
            default = args.kw_defaults[args.kw_defaults.index(kw)]
            if default:
                try:
                    kw_name += f"={ast.unparse(default)}"
                except Exception:
                    pass
        arg_parts.append(kw_name)

    return f"({', '.join(arg_parts)})"


def parse_docstring(docstring: str) -> dict[str, str]:
    """Parse docstring into sections."""
    if not docstring:
        return {'description': '', 'params': {}, 'returns': '', 'raises': []}

    sections = {
        'description': '',
        'params': {},
        'returns': '',
        'raises': [],
        'examples': []
    }

    lines = docstring.split('\n')
    current_section = 'description'
    current_param = None
    param_desc_lines = []

    for line in lines:
        stripped = line.strip()

        # Section headers
        if stripped.lower().startswith('args:') or stripped.lower().startswith('parameters:'):
            current_section = 'params'
            continue
        elif stripped.lower().startswith('returns:') or stripped.lower().startswith('return:'):
            current_section = 'returns'
            sections['returns'] = stripped.split(':', 1)[1].strip() if ':' in stripped else ''
            continue
        elif stripped.lower().startswith('raises:'):
            current_section = 'raises'
            continue
        elif stripped.lower().startswith('example:'):
            current_section = 'examples'
            continue

        # Param parsing
        if current_section == 'params':
            # Check for param name: pattern
            param_match = re.match(r'^\s*(\w+):\s*(.*)$', stripped)
            if param_match:
                if current_param:
                    sections['params'][current_param] = ' '.join(param_desc_lines).strip()
                current_param = param_match.group(1)
                param_desc_lines = [param_match.group(2)]
            elif current_param and stripped:
                param_desc_lines.append(stripped)
        elif current_section in ('description', 'returns', 'raises'):
            if stripped:
                if current_section == 'raises':
                    if not sections[current_section]:
                        sections[current_section] = []
                    sections[current_section].append(stripped)
                elif sections[current_section]:
                    sections[current_section] += ' ' + stripped
                else:
                    sections[current_section] = stripped
        elif current_section == 'examples':
            if stripped:
                sections['examples'].append(stripped)

    # Last param
    if current_param:
        sections['params'][current_param] = ' '.join(param_desc_lines).strip()

    return sections


def format_docstring_sections(sections: dict) -> str:
    """Format parsed docstring sections for output."""
    parts = []

    if sections['description']:
        parts.append(sections['description'])

    if sections['params']:
        parts.append("\n**Parameters:**")
        for name, desc in sections['params'].items():
            parts.append(f"  - `{name}` — {desc}")

    if sections['returns']:
        parts.append(f"\n**Returns:** {sections['returns']}")

    if sections['raises']:
        parts.append(f"\n**Raises:** {', '.join(sections['raises'])}")

    return '\n'.join(parts)


class APIDocVisitor(ast.NodeVisitor):
    """AST visitor to extract API documentation."""

    def __init__(self, source: str, module_path: Path):
        self.source = source
        self.module_path = module_path
        self.module_doc = ModuleDoc(
            path=module_path,
            module_name=module_path.stem,
            docstring=''
        )
        self.current_class: ClassDoc | None = None

    def visit_Module(self, node: ast.Module):
        """Visit module-level docstring."""
        if ast.get_docstring(node):
            self.module_doc.docstring = ast.get_docstring(node)
        self.generic_visit(node)

    def visit_ClassDef(self, node: ast.ClassDef):
        """Visit class definitions."""
        decorators = [parse_decorator(d) for d in node.decorator_list]
        decorators_signatures = [get_decorator_signature(d) for d in node.decorator_list]

        class_doc = ClassDoc(
            name=node.name,
            docstring=ast.get_docstring(node) or '',
            decorators=decorators,
            line_number=node.lineno
        )

        # Track decorators with documentation
        for i, dec in enumerate(node.decorator_list):
            dec_sig = get_decorator_signature(dec)
            if dec_sig != '@decorator':
                class_doc.decorators_doc[decorators[i] or 'decorator'] = dec_sig

        old_class = self.current_class
        self.current_class = class_doc

        # Visit methods
        for child in node.body:
            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                self.visit_FunctionDef(child, is_method=True)

        # Also visit inner classes
        for child in node.body:
            if isinstance(child, ast.ClassDef):
                self.visit_ClassDef(child)

        self.current_class = old_class
        self.module_doc.classes.append(class_doc)

    def visit_FunctionDef(self, node: ast.FunctionDef | ast.AsyncFunctionDef, is_method: bool = False):
        """Visit function definitions."""
        func_name = node.name

        # Skip private methods for basic output
        if is_method and func_name.startswith('_') and not func_name.startswith('__'):
            return

        decorators = [parse_decorator(d) for d in node.decorator_list]

        func_doc = FunctionDoc(
            name=func_name,
            signature=get_function_signature(node),
            docstring=ast.get_docstring(node) or '',
            decorators=decorators,
            line_number=node.lineno
        )

        if is_method and self.current_class:
            self.current_class.methods.append(func_doc)
        else:
            self.module_doc.functions.append(func_doc)


def scan_file(file_path: Path) -> ModuleDoc | None:
    """Scan a Python file and extract API documentation."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            source = f.read()

        tree = ast.parse(source, filename=str(file_path))
        visitor = APIDocVisitor(source, file_path)
        visitor.visit(tree)
        return visitor.module_doc

    except SyntaxError as e:
        print(f"Syntax error in {file_path}: {e}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"Error parsing {file_path}: {e}", file=sys.stderr)
        return None


def scan_directory(directory: Path, pattern: str = "*.py") -> list[ModuleDoc]:
    """Scan directory for Python files and extract documentation."""
    modules = []

    for file_path in sorted(directory.rglob(pattern)):
        # Skip __pycache__ and hidden directories
        if '__pycache__' in str(file_path):
            continue

        module = scan_file(file_path)
        if module:
            modules.append(module)

    return modules


def generate_markdown(modules: list[ModuleDoc], title: str = "API Documentation") -> str:
    """Generate Markdown documentation."""
    lines = [
        f"# {title}",
        "",
        "## Table of Contents",
        ""
    ]

    # Build TOC
    for module in modules:
        rel_path = module.path.relative_to(module.path.parents[0]) if module.path.parent != module.path else module.path
        lines.append(f"- [{module.module_name}](#{module.module_name.lower().replace('.', '-')})")

        for cls in module.classes:
            lines.append(f"  - [{cls.name}](#{cls.name.lower()})")
            for method in cls.methods:
                lines.append(f"    - [{method.name}()](#{method.name.lower()})")

        for func in module.functions:
            lines.append(f"  - [{func.name}()](#{func.name.lower()})")

    lines.append("")

    # Generate sections
    for module in modules:
        lines.append(f"## {module.module_name}")
        lines.append("")

        if module.path.exists():
            lines.append(f"**File:** `{module.path}`")
            lines.append("")

        if module.docstring:
            lines.append(module.docstring)
            lines.append("")

        # Classes
        for cls in module.classes:
            lines.append(f"### {cls.name}")
            lines.append("")

            if cls.docstring:
                sections = parse_docstring(cls.docstring)
                lines.append(format_docstring_sections(sections))
                lines.append("")

            if cls.decorators:
                lines.append(f"**Decorators:** `{', '.join(filter(None, cls.decorators))}`")
                lines.append("")

            for method in cls.methods:
                lines.append(f"#### `{method.name}{method.signature}`")
                lines.append("")

                if method.docstring:
                    sections = parse_docstring(method.docstring)
                    lines.append(format_docstring_sections(sections))
                    lines.append("")

                if method.decorators:
                    lines.append(f"**Decorators:** `{', '.join(filter(None, method.decorators))}`")
                    lines.append("")

                lines.append("---")
                lines.append("")

        # Standalone functions
        for func in module.functions:
            lines.append(f"### `{func.name}{func.signature}`")
            lines.append("")

            if func.docstring:
                sections = parse_docstring(func.docstring)
                lines.append(format_docstring_sections(sections))
                lines.append("")

            if func.decorators:
                lines.append(f"**Decorators:** `{', '.join(filter(None, func.decorators))}`")
                lines.append("")

            lines.append("---")
            lines.append("")

    return '\n'.join(lines)


def generate_openapi(modules: list[ModuleDoc]) -> dict[str, Any]:
    """Generate OpenAPI-compatible documentation."""
    spec = {
        "openapi": "3.1.0",
        "info": {
            "title": "API Documentation",
            "version": "1.0.0"
        },
        "paths": {}
    }

    for module in modules:
        for func in module.functions:
            # Check if it's a route function
            if any(d in (func.decorators or []) for d in ('get', 'post', 'put', 'delete', 'route', 'api_view')):
                path = f"/{module.module_name}/{func.name}"
                method = 'get'

                for dec in (func.decorators or []):
                    if dec in ('get', 'post', 'put', 'delete', 'patch'):
                        method = dec
                    elif dec == 'route':
                        # Extract path from decorator
                        pass

                sections = parse_docstring(func.docstring)

                if path not in spec['paths']:
                    spec['paths'][path] = {}

                spec['paths'][path][method] = {
                    "summary": sections['description'] or func.name,
                    "parameters": [
                        {"name": p, "description": d}
                        for p, d in sections['params'].items()
                    ],
                    "responses": {
                        "200": {
                            "description": sections['returns'] or "Successful response"
                        }
                    }
                }

    return spec


def main():
    parser = argparse.ArgumentParser(
        description="API Documentation Generator - Scan Python files and generate API docs",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        'path',
        help='Python file or directory to scan'
    )

    parser.add_argument(
        '-o', '--output',
        help='Output file (default: stdout)'
    )

    parser.add_argument(
        '-f', '--format',
        choices=['markdown', 'openapi', 'json'],
        default='markdown',
        help='Output format (default: markdown)'
    )

    parser.add_argument(
        '-t', '--title',
        default='API Documentation',
        help='Documentation title'
    )

    parser.add_argument(
        '-p', '--pattern',
        default='*.py',
        help='File pattern to match (default: *.py)'
    )

    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Verbose output'
    )

    args = parser.parse_args()

    # Resolve path
    path = Path(args.path).resolve()

    if not path.exists():
        print(f"Error: Path not found: {path}", file=sys.stderr)
        sys.exit(1)

    # Scan files
    if path.is_file():
        module = scan_file(path)
        modules = [module] if module else []
    else:
        modules = scan_directory(path, args.pattern)

    if not modules:
        print("No modules found.", file=sys.stderr)
        sys.exit(1)

    if args.verbose:
        print(f"Scanned {len(modules)} module(s)")

    # Generate output
    if args.format == 'markdown':
        output = generate_markdown(modules, args.title)
    elif args.format == 'openapi':
        spec = generate_openapi(modules)
        output = json.dumps(spec, indent=2)
    else:  # json
        output = json.dumps([{
            'path': str(m.path),
            'module': m.module_name,
            'docstring': m.docstring,
            'classes': [{
                'name': c.name,
                'docstring': c.docstring,
                'methods': [{
                    'name': f.name,
                    'signature': f.signature,
                    'docstring': f.docstring
                } for f in c.methods]
            } for c in m.classes],
            'functions': [{
                'name': f.name,
                'signature': f.signature,
                'docstring': f.docstring
            } for f in m.functions]
        } for m in modules], indent=2)

    # Write output
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output)
        print(f"Documentation written to: {args.output}")
    else:
        print(output)


if __name__ == '__main__':
    main()
