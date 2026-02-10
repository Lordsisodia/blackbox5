#!/usr/bin/env python3
"""
Generate API documentation from Python source files.

This script scans the codebase for Python files and generates
API documentation in Markdown format.
"""

import ast
import os
import re
from pathlib import Path
from typing import Dict, List


# Configuration
SOURCE_DIRS = [
    Path("/opt/blackbox5/2-engine"),
    Path("/opt/blackbox5/bin"),
]
OUTPUT_DIR = Path("/opt/blackbox5/1-docs/02-implementation/01-core")
OUTPUT_FILE = OUTPUT_DIR / "API-DOCUMENTATION.md"


def parse_python_file(filepath: Path) -> Dict:
    """Parse a Python file and extract docstrings."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        tree = ast.parse(content)
    except Exception as e:
        return None

    docstring = ast.get_docstring(tree)

    functions = []
    classes = []
    constants = []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            func_doc = ast.get_docstring(node)
            args = [arg.arg for arg in node.args.args]
            functions.append({
                'name': node.name,
                'doc': func_doc or 'No docstring',
                'args': args,
                'lineno': node.lineno,
            })
        elif isinstance(node, ast.ClassDef):
            class_doc = ast.get_docstring(node)
            methods = []
            for item in node.body:
                if isinstance(item, ast.FunctionDef):
                    method_doc = ast.get_docstring(item)
                    methods.append({
                        'name': item.name,
                        'doc': method_doc or 'No docstring',
                    })
            classes.append({
                'name': node.name,
                'doc': class_doc or 'No docstring',
                'methods': methods,
                'lineno': node.lineno,
            })

    return {
        'path': str(filepath.relative_to(Path.cwd())),
        'docstring': docstring or 'No module docstring',
        'functions': functions,
        'classes': classes,
        'constants': constants,
    }


def generate_markdown(parsed_data: Dict) -> str:
    """Generate markdown documentation from parsed data."""
    md = f"""## `{parsed_data['path']}`

{parsed_data['docstring']}

"""
    if parsed_data['classes']:
        md += "### Classes\n\n"
        for cls in parsed_data['classes']:
            md += f"#### `{cls['name']}`\n\n"
            md += f"{cls['doc']}\n\n"
            if cls['methods']:
                md += "**Methods:**\n\n"
                for method in cls['methods']:
                    md += f"- `{method['name']}`: {method['doc']}\n"
            md += "\n"

    if parsed_data['functions']:
        md += "### Functions\n\n"
        for func in parsed_data['functions']:
            args_str = ', '.join(func['args']) if func['args'] else ''
            md += f"#### `{func['name']}({args_str})`\n\n"
            md += f"{func['doc']}\n\n"

    md += "---\n\n"
    return md


def main():
    """Main function to generate API documentation."""
    print("🔍 Scanning for Python files...")

    all_docs = []
    for source_dir in SOURCE_DIRS:
        if not source_dir.exists():
            continue

        for py_file in source_dir.rglob("*.py"):
            # Skip test files and __pycache__
            if '__pycache__' in str(py_file) or 'test' in py_file.name:
                continue

            parsed = parse_python_file(py_file)
            if parsed and (parsed['functions'] or parsed['classes']):
                all_docs.append(parsed)

    print(f"📝 Found {len(all_docs)} documented files")

    # Generate output
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write("""# BlackBox5 API Documentation

This documentation is auto-generated from Python source files.

*Last updated: {}

---

""".format(os.popen('date').read().strip()))

        for doc in all_docs:
            f.write(generate_markdown(doc))

    print(f"✅ Documentation generated: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
