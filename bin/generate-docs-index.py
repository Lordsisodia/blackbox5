#!/usr/bin/env python3
"""
Blackbox5 Documentation Index Generator

Auto-generates INDEX.md from actual directory structure.
Detects orphaned files, duplicates, and README mismatches.

Usage:
    ./bin/generate-docs-index.py              # Generate INDEX.md
    ./bin/generate-docs-index.py --check      # Verify INDEX.md is current (CI mode)
    ./bin/generate-docs-index.py --watch      # Watch for changes and auto-regenerate
"""

import os
import sys
import re
import argparse
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Tuple, Optional

DOCS_ROOT = Path("/Users/shaansisodia/.blackbox5/1-docs")
INDEX_PATH = DOCS_ROOT / "INDEX.md"

# Files to ignore in indexing
IGNORE_PATTERNS = [
    ".*",           # Hidden files
    "INDEX.md",     # This file
    "*.pyc",
    "__pycache__",
    "*.tmp",
]

class DocEntry:
    """Represents a documentation file or directory"""
    def __init__(self, path: Path, root: Path):
        self.path = path
        self.root = root
        self.rel_path = path.relative_to(root)
        self.name = path.name
        self.is_dir = path.is_dir()
        self.has_readme = (path / "README.md").exists() if self.is_dir else False
        self.readme_content = self._read_readme() if self.has_readme else None

    def _read_readme(self) -> Optional[str]:
        """Read README content for analysis"""
        try:
            return (self.path / "README.md").read_text(encoding='utf-8', errors='ignore')
        except:
            return None

    def get_description(self) -> str:
        """Extract description from README or return default"""
        if self.readme_content:
            # Try to extract first paragraph after title
            lines = self.readme_content.split('\n')
            for i, line in enumerate(lines):
                if line.startswith('# ') and i + 1 < len(lines):
                    # Skip empty lines and take next non-empty
                    for j in range(i + 1, min(i + 5, len(lines))):
                        desc = lines[j].strip()
                        if desc and not desc.startswith('#') and not desc.startswith('['):
                            return desc[:100] + '...' if len(desc) > 100 else desc
        return ""

class DocsIndexGenerator:
    """Generates the documentation index"""

    def __init__(self, docs_root: Path):
        self.docs_root = docs_root
        self.entries: List[DocEntry] = []
        self.orphaned_files: List[Path] = []
        self.duplicate_warnings: List[Tuple[str, List[Path]]] = []
        self.readme_mismatches: List[Tuple[Path, str]] = []

    def should_ignore(self, path: Path) -> bool:
        """Check if path should be ignored"""
        name = path.name
        for pattern in IGNORE_PATTERNS:
            if pattern.startswith('*'):
                if name.endswith(pattern[1:]):
                    return True
            elif pattern.startswith('.'):
                if name.startswith('.'):
                    return True
            elif name == pattern:
                return True
        return False

    def scan_directory(self, path: Path = None, depth: int = 0) -> List[DocEntry]:
        """Recursively scan directory structure"""
        if path is None:
            path = self.docs_root

        entries = []

        try:
            for item in sorted(path.iterdir()):
                if self.should_ignore(item):
                    continue

                entry = DocEntry(item, self.docs_root)
                entries.append(entry)

                if entry.is_dir and depth < 5:
                    entry.children = self.scan_directory(item, depth + 1)

        except PermissionError:
            pass

        return entries

    def find_orphaned_files(self, entries: List[DocEntry], parent_readme: Optional[str] = None):
        """Find files not linked from parent README"""
        for entry in entries:
            if entry.is_dir:
                # Check if directory is mentioned in parent README
                if parent_readme and entry.name not in parent_readme:
                    if not entry.name.startswith('.'):
                        self.readme_mismatches.append((
                            entry.path,
                            f"Directory '{entry.name}' not mentioned in parent README"
                        ))

                # Recurse into directory
                readme_content = entry.readme_content or ""
                if hasattr(entry, 'children'):
                    self.find_orphaned_files(entry.children, readme_content)
            else:
                # Check if file is linked from parent README
                if parent_readme and entry.name != "README.md":
                    # Check various link patterns
                    link_patterns = [
                        f"]({entry.name})",
                        f"]({entry.name}#",
                        f"]({entry.name.lower()})",
                        f"]({entry.name.replace('-', '_')})",
                    ]
                    if not any(pattern in parent_readme for pattern in link_patterns):
                        if entry.name.endswith('.md'):
                            self.orphaned_files.append(entry.rel_path)

    def detect_duplicates(self, entries: List[DocEntry]):
        """Detect potentially duplicate content"""
        topic_map: Dict[str, List[Path]] = {}

        # Common topics that might be duplicated
        duplicate_keywords = [
            'quick-start', 'quickstart', 'getting-started',
            'state-management', 'state',
            'skills', 'skill-registry',
            'mcp', 'integration',
            'orchestrator', 'orchestration',
            'checkpoint', 'atomic',
        ]

        for entry in entries:
            name_lower = entry.name.lower().replace('_', '-')
            for keyword in duplicate_keywords:
                if keyword in name_lower:
                    if keyword not in topic_map:
                        topic_map[keyword] = []
                    topic_map[keyword].append(entry.rel_path)

        # Find topics with multiple locations
        for topic, paths in topic_map.items():
            if len(paths) > 1:
                self.duplicate_warnings.append((topic, paths))

    def count_files(self, entries: List[DocEntry]) -> int:
        """Count total markdown files"""
        count = 0
        for entry in entries:
            if entry.is_dir:
                if hasattr(entry, 'children'):
                    count += self.count_files(entry.children)
            elif entry.name.endswith('.md'):
                count += 1
        return count

    def generate_markdown(self, entries: List[DocEntry]) -> str:
        """Generate the INDEX.md content"""
        lines = []

        # Header
        lines.extend([
            "# Blackbox5 Documentation Index",
            "",
            "**Auto-generated from actual directory structure**",
            f"*Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*",
            "",
            "> **Note:** This index reflects the ACTUAL structure, not the intended structure.",
            "> Run `./bin/generate-docs-index.py` to regenerate.",
            "",
            "---",
            "",
        ])

        # Quick Navigation
        lines.extend([
            "## Quick Navigation",
            "",
            "| I want to... | Go to |",
            "|--------------|-------|",
        ])

        nav_map = [
            ("Understand concepts", "01-theory"),
            ("Build/extend the system", "02-implementation"),
            ("Use the system", "03-guides"),
            ("Manage the project", "04-project"),
            ("See examples", "05-examples"),
            ("Understand decisions", "decisions"),
        ]

        for label, path in nav_map:
            lines.append(f"| {label} | [{path}/](#{path.replace('-', '')}) |")

        lines.append("")
        lines.append("---")
        lines.append("")

        # Statistics
        total_files = self.count_files(entries)
        total_dirs = sum(1 for e in entries if e.is_dir)

        lines.extend([
            "## Statistics",
            "",
            f"- **Total Markdown Files:** {total_files}",
            f"- **Total Directories:** {total_dirs}",
            f"- **Orphaned Files:** {len(self.orphaned_files)}",
            f"- **Duplicate Warnings:** {len(self.duplicate_warnings)}",
            f"- **README Mismatches:** {len(self.readme_mismatches)}",
            "",
            "---",
            "",
        ])

        # Main sections
        for entry in entries:
            if entry.is_dir:
                lines.extend(self._generate_section(entry))

        # Warnings section
        if self.orphaned_files or self.duplicate_warnings or self.readme_mismatches:
            lines.extend([
                "",
                "---",
                "",
                "## Warnings",
                "",
            ])

            if self.orphaned_files:
                lines.extend([
                    "### Orphaned Files (Not Linked from Parent README)",
                    "",
                ])
                for f in self.orphaned_files[:20]:  # Limit to 20
                    lines.append(f"- `{f}`")
                if len(self.orphaned_files) > 20:
                    lines.append(f"- ... and {len(self.orphaned_files) - 20} more")
                lines.append("")

            if self.duplicate_warnings:
                lines.extend([
                    "### Potential Duplicate Content",
                    "",
                ])
                for topic, paths in self.duplicate_warnings[:10]:
                    lines.append(f"**{topic}:**")
                    for p in paths:
                        lines.append(f"  - `{p}`")
                    lines.append("")

            if self.readme_mismatches:
                lines.extend([
                    "### README/Structure Mismatches",
                    "",
                ])
                for path, issue in self.readme_mismatches[:10]:
                    rel = path.relative_to(self.docs_root)
                    lines.append(f"- `{rel}`: {issue}")
                lines.append("")

        # Footer
        lines.extend([
            "",
            "---",
            "",
            "## For Agents",
            "",
            "**Navigation Strategy:**",
            "1. Start here (INDEX.md) for overview",
            "2. Use section READMEs for details",
            "3. Watch for warnings about structural issues",
            "4. When in doubt, this index is the source of truth",
            "",
            "**Search Tips:**",
            '- Use `find 1-docs -name "*topic*"` for file names',
            '- Use `grep -r "topic" 1-docs/` for content',
            "- Check this index first for known locations",
            "",
            "---",
            "",
            "*This index is auto-generated. To regenerate: Run `./bin/generate-docs-index.py`*",
            "",
        ])

        return '\n'.join(lines)

    def _generate_section(self, entry: DocEntry, depth: int = 0) -> List[str]:
        """Generate markdown for a section"""
        lines = []
        indent = "  " * depth

        # Section header
        anchor = str(entry.rel_path).replace('/', '').replace('-', '').lower()
        file_count = self._count_md_files(entry)

        lines.extend([
            "",
            f"## {str(entry.rel_path)}/ ({file_count} files)",
            "",
        ])

        if entry.has_readme:
            desc = entry.get_description()
            if desc:
                lines.append(f"**Description:** {desc}")
                lines.append("")
            lines.append(f"**README:** [{entry.name}/README.md](./{entry.rel_path}/README.md)")
            lines.append("")

        # Table of contents for subdirectory
        if hasattr(entry, 'children') and entry.children:
            subdirs = [e for e in entry.children if e.is_dir]
            files = [e for e in entry.children if not e.is_dir and e.name.endswith('.md')]

            if subdirs:
                lines.append("| Subdirectory | Files | README | Description |")
                lines.append("|--------------|-------|--------|-------------|")

                for sub in subdirs:
                    sub_count = self._count_md_files(sub)
                    readme_badge = "✅" if sub.has_readme else "❌"
                    desc = sub.get_description()[:50] if sub.get_description() else ""
                    lines.append(
                        f"| [{sub.name}/](./{sub.rel_path}/) | ~{sub_count} | "
                        f"{readme_badge} | {desc} |"
                    )
                lines.append("")

            # List key files
            key_files = [f for f in files if f.name != "README.md" and not f.name.startswith('.')]
            if key_files:
                lines.append("**Key Files:**")
                lines.append("")
                for f in key_files[:10]:  # Limit to 10
                    lines.append(f"- [{f.name}](./{f.rel_path})")
                if len(key_files) > 10:
                    lines.append(f"- ... and {len(key_files) - 10} more files")
                lines.append("")

            # Recurse for subsections (limited depth)
            if depth < 1:
                for sub in subdirs:
                    lines.extend(self._generate_section(sub, depth + 1))

        return lines

    def _count_md_files(self, entry: DocEntry) -> int:
        """Count markdown files in entry"""
        if not entry.is_dir:
            return 1 if entry.name.endswith('.md') else 0

        count = 0
        if hasattr(entry, 'children'):
            for child in entry.children:
                count += self._count_md_files(child)
        return count

    def generate(self) -> str:
        """Main generation method"""
        print("🔍 Scanning documentation structure...")
        entries = self.scan_directory()

        print("🔍 Finding orphaned files...")
        self.find_orphaned_files(entries)

        print("🔍 Detecting duplicate content...")
        self.detect_duplicates(entries)

        print("📝 Generating INDEX.md...")
        content = self.generate_markdown(entries)

        return content

    def write(self, content: str):
        """Write index to file"""
        INDEX_PATH.write_text(content, encoding='utf-8')
        print(f"✅ INDEX.md generated: {INDEX_PATH}")
        print(f"   - Total entries: {self.count_files(self.scan_directory())}")
        print(f"   - Orphaned files: {len(self.orphaned_files)}")
        print(f"   - Duplicate warnings: {len(self.duplicate_warnings)}")
        print(f"   - README mismatches: {len(self.readme_mismatches)}")

    def check(self) -> bool:
        """Check if INDEX.md is current (for CI)"""
        if not INDEX_PATH.exists():
            print("❌ INDEX.md does not exist")
            return False

        current_content = INDEX_PATH.read_text(encoding='utf-8')
        new_content = self.generate()

        if current_content == new_content:
            print("✅ INDEX.md is up to date")
            return True
        else:
            print("❌ INDEX.md is out of date")
            print("   Run `./bin/generate-docs-index.py` to regenerate")
            return False

def watch_mode():
    """Watch for changes and auto-regenerate"""
    try:
        from watchdog.observers import Observer
        from watchdog.events import FileSystemEventHandler
    except ImportError:
        print("⚠️  Watch mode requires watchdog: pip install watchdog")
        sys.exit(1)

    class DocsHandler(FileSystemEventHandler):
        def __init__(self, generator):
            self.generator = generator
            self.last_run = 0

        def on_modified(self, event):
            if event.is_directory:
                return
            if event.src_path.endswith('INDEX.md'):
                return
            if event.src_path.endswith('.md'):
                import time
                now = time.time()
                if now - self.last_run > 2:  # Debounce
                    print(f"\n📝 Change detected: {event.src_path}")
                    print("Regenerating INDEX.md...")
                    content = self.generator.generate()
                    self.generator.write(content)
                    self.last_run = now

    generator = DocsIndexGenerator(DOCS_ROOT)
    event_handler = DocsHandler(generator)
    observer = Observer()
    observer.schedule(event_handler, str(DOCS_ROOT), recursive=True)
    observer.start()

    print(f"👁️  Watching {DOCS_ROOT} for changes...")
    print("Press Ctrl+C to stop")

    try:
        while True:
            import time
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

def main():
    parser = argparse.ArgumentParser(
        description="Generate documentation index for Blackbox5"
    )
    parser.add_argument(
        '--check',
        action='store_true',
        help='Check if INDEX.md is current (CI mode)'
    )
    parser.add_argument(
        '--watch',
        action='store_true',
        help='Watch for changes and auto-regenerate'
    )
    parser.add_argument(
        '--output',
        '-o',
        type=str,
        help='Output file (default: 1-docs/INDEX.md)'
    )

    args = parser.parse_args()

    generator = DocsIndexGenerator(DOCS_ROOT)

    if args.watch:
        watch_mode()
    elif args.check:
        success = generator.check()
        sys.exit(0 if success else 1)
    else:
        content = generator.generate()
        if args.output:
            Path(args.output).write_text(content, encoding='utf-8')
            print(f"✅ Index written to: {args.output}")
        else:
            generator.write(content)

if __name__ == "__main__":
    main()
