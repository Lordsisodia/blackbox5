#!/usr/bin/env python3
"""
Update table of contents in README files.

This script scans for README files and adds/updates a table of contents.
"""

import re
from pathlib import Path


# Configuration
README_GLOBS = [
    "/opt/blackbox5/README.md",
    "/opt/blackbox5/1-docs/**/*.md",
]
TOC_START = "<!-- TOC START -->"
TOC_END = "<!-- TOC END -->"


def extract_headers(content: str) -> List[tuple]:
    """Extract headers from markdown content."""
    headers = []
    for line in content.split('\n'):
        match = re.match(r'^(#{1,6})\s+(.+)$', line)
        if match:
            level = len(match.group(1))
            title = match.group(2).strip()
            # Skip TOC markers
            if title not in [TOC_START, TOC_END]:
                headers.append((level, title))
    return headers


def generate_toc(headers: List[tuple]) -> str:
    """Generate table of contents from headers."""
    toc = []
    for level, title in headers:
        indent = "  " * (level - 1)
        # Create anchor
        anchor = re.sub(r'[^\w\s-]', '', title).strip().lower().replace(' ', '-')
        toc.append(f"{indent}- [{title}](#{anchor})")
    return '\n'.join(toc)


def update_toc(filepath: Path):
    """Update TOC in a markdown file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    headers = extract_headers(content)
    toc = generate_toc(headers)

    # Check if TOC markers exist
    if TOC_START in content and TOC_END in content:
        # Update existing TOC
        pattern = f"{re.escape(TOC_START)}.*?{re.escape(TOC_END)}"
        new_toc = f"{TOC_START}\n\n{toc}\n\n{TOC_END}"
        content = re.sub(pattern, new_toc, content, flags=re.DOTALL)
    else:
        # Insert TOC after first heading
        first_heading_match = re.search(r'^#{1,6}\s+.+$', content, flags=re.MULTILINE)
        if first_heading_match:
            insert_pos = first_heading_match.end()
            new_toc = f"\n\n{TOC_START}\n\n{toc}\n\n{TOC_END}\n\n"
            content = content[:insert_pos] + new_toc + content[insert_pos:]

    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"  ✅ Updated: {filepath.relative_to(Path.cwd())}")


def main():
    """Main function."""
    print("📝 Updating README TOCs...")

    for pattern in README_GLOBS:
        for filepath in Path("/opt/blackbox5").glob(pattern.lstrip('/')):
            if filepath.name == 'README.md':
                update_toc(filepath)

    print("✅ TOC updates complete")


if __name__ == "__main__":
    main()
