#!/usr/bin/env python3
"""
Documentation Extract Script
Processes fetched pages and creates agent-friendly summaries
"""

import argparse
import json
import re
from pathlib import Path
from datetime import datetime


def extract_code_examples(content: str) -> list:
    """Extract code blocks from markdown"""
    # Match fenced code blocks
    pattern = r'```(\w+)?\n(.*?)```'
    matches = re.findall(pattern, content, re.DOTALL)

    examples = []
    for lang, code in matches:
        examples.append({
            'language': lang or 'text',
            'code': code.strip()
        })

    return examples


def extract_commands(content: str) -> list:
    """Extract CLI commands from content"""
    # Match commands like `claude --flag` or claude subcommand
    pattern = r'`?(claude[\s\w\-]+)`?'
    matches = re.findall(pattern, content, re.IGNORECASE)

    return list(set(matches))  # Deduplicate


def extract_tables(content: str) -> list:
    """Extract markdown tables"""
    tables = []

    # Simple table detection
    lines = content.split('\n')
    in_table = False
    table_lines = []

    for line in lines:
        if '|' in line:
            table_lines.append(line)
            in_table = True
        elif in_table:
            if table_lines:
                tables.append('\n'.join(table_lines))
            table_lines = []
            in_table = False

    return tables


def create_quick_reference(pages_dir: Path) -> str:
    """Create quick-reference.md from all fetched pages"""

    sections = []

    for page_file in sorted(pages_dir.glob('*.md')):
        with open(page_file) as f:
            content = f.read()

        # Parse frontmatter
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                try:
                    frontmatter = json.loads(parts[1])
                    body = parts[2]
                except:
                    frontmatter = {}
                    body = content
        else:
            frontmatter = {}
            body = content

        title = frontmatter.get('metadata', {}).get('title', '')
        section = frontmatter.get('metadata', {}).get('section', '')

        # Extract key information based on section
        section_content = f"## {title or section}\n\n"

        # Look for command examples
        commands = extract_commands(body)
        if commands:
            section_content += "### Commands\n\n"
            for cmd in commands[:10]:  # Limit to first 10
                section_content += f"- `{cmd}`\n"
            section_content += "\n"

        # Look for tables (often contain reference data)
        tables = extract_tables(body)
        if tables:
            section_content += "### Key Reference\n\n"
            section_content += tables[0] + "\n\n"

        sections.append(section_content)

    # Assemble quick reference
    output = "---\n"
    output += f"source: claude-code\n"
    output += f"generated_at: {datetime.now().isoformat()}\n"
    output += f"pages_processed: {len(sections)}\n"
    output += "---\n\n"
    output += "# Quick Reference\n\n"
    output += "Key facts extracted for fast agent lookup.\n\n"

    for section in sections:
        output += section + "\n"

    return output


def create_search_index(pages_dir: Path) -> dict:
    """Create search-index.json for programmatic access"""

    index = {
        'concepts': [],
        'commands': [],
        'pages': []
    }

    for page_file in pages_dir.glob('*.md'):
        with open(page_file) as f:
            content = f.read()

        # Parse frontmatter
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                try:
                    frontmatter = json.loads(parts[1])
                    body = parts[2]
                except:
                    frontmatter = {}
                    body = content
        else:
            frontmatter = {}
            body = content

        page_info = {
            'path': str(page_file.name),
            'title': frontmatter.get('metadata', {}).get('title', ''),
            'section': frontmatter.get('metadata', {}).get('section', ''),
            'tier': frontmatter.get('metadata', {}).get('tier', 3)
        }

        index['pages'].append(page_info)

        # Extract commands
        commands = extract_commands(body)
        for cmd in commands:
            index['commands'].append({
                'command': cmd,
                'source_page': page_file.name
            })

    return index


def main():
    parser = argparse.ArgumentParser(description='Extract insights from docs')
    parser.add_argument('--input', '-i', required=True,
                        help='Directory with fetched pages')
    parser.add_argument('--output', '-o', required=True,
                        help='Output directory for extracted content')

    args = parser.parse_args()

    pages_dir = Path(args.input)
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    if not pages_dir.exists():
        print(f"Error: Input directory not found: {pages_dir}")
        return

    print(f"Processing pages from: {pages_dir}")

    # Create quick reference
    print("Creating quick-reference.md...")
    quick_ref = create_quick_reference(pages_dir)
    with open(output_dir / 'quick-reference.md', 'w') as f:
        f.write(quick_ref)

    # Create search index
    print("Creating search-index.json...")
    search_index = create_search_index(pages_dir)
    with open(output_dir / 'search-index.json', 'w') as f:
        json.dump(search_index, f, indent=2)

    print()
    print(f"Extraction complete:")
    print(f"  - quick-reference.md")
    print(f"  - search-index.json")
    print(f"  - {len(search_index['pages'])} pages indexed")
    print(f"  - {len(search_index['commands'])} commands extracted")


if __name__ == '__main__':
    main()
