#!/usr/bin/env python3
"""
Generate module index documentation.

This script creates an index of all modules in the BlackBox5 codebase.
"""

import os
from pathlib import Path
from typing import List


# Configuration
SOURCE_DIRS = [
    Path("/opt/blackbox5/2-engine"),
]
OUTPUT_DIR = Path("/opt/blackbox5/1-docs/02-implementation")
OUTPUT_FILE = OUTPUT_DIR / "MODULE-INDEX.md"


def get_module_info(directory: Path, base_path: Path) -> List[Dict]:
    """Get information about all Python modules."""
    modules = []

    for item in directory.rglob("*.py"):
        # Skip test files and __pycache__
        if '__pycache__' in str(item) or 'test' in item.name or item.name == '__init__.py':
            continue

        rel_path = item.relative_to(base_path)
        module_path = str(rel_path.with_suffix('')).replace('/', '.')

        # Try to get docstring
        docstring = "No description"
        try:
            with open(item, 'r', encoding='utf-8') as f:
                content = f.read()
                # Extract first line docstring
                match = re.search(r'"""([^"]*)"""', content[:500])
                if match:
                    docstring = match.group(1).split('\n')[0]
        except:
            pass

        modules.append({
            'name': module_path,
            'path': str(rel_path),
            'description': docstring,
        })

    return sorted(modules, key=lambda x: x['name'])


def generate_markdown(modules: List[Dict]) -> str:
    """Generate markdown from module info."""
    md = """# BlackBox5 Module Index

Complete index of all modules in the BlackBox5 codebase.

## Quick Reference

| Module | Description |
|--------|-------------|
"""
    for mod in modules:
        md += f"| [`{mod['name']}`]({mod['path']}) | {mod['description']} |\n"

    return md


def main():
    """Main function."""
    print("🔍 Building module index...")

    all_modules = []
    for source_dir in SOURCE_DIRS:
        if source_dir.exists():
            modules = get_module_info(source_dir, source_dir)
            all_modules.extend(modules)

    print(f"📝 Found {len(all_modules)} modules")

    # Generate output
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(generate_markdown(all_modules))

    print(f"✅ Module index generated: {OUTPUT_FILE}")


if __name__ == "__main__":
    import re
    main()
