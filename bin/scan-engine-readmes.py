#!/usr/bin/env python3
"""
Engine-Wide README Scanner

Scans the entire Blackbox5 engine for:
- Directories without READMEs
- READMEs that don't match directory structure
- Orphaned documentation
- Inconsistent naming

Usage:
    ./bin/scan-engine-readmes.py              # Full scan
    ./bin/scan-engine-readmes.py --missing    # Only missing READMEs
    ./bin/scan-engine-readmes.py --orphaned   # Only orphaned files
    ./bin/scan-engine-readmes.py --fixable    # Show what can be auto-fixed
"""

import os
import re
import argparse
from pathlib import Path
from typing import List, Dict, Set, Tuple
from dataclasses import dataclass, field
from collections import defaultdict

BB5_ROOT = Path("/Users/shaansisodia/.blackbox5")

# Directories to skip
SKIP_DIRS = {
    '.git', '.archive', 'node_modules', '__pycache__', '.pytest_cache',
    '.mypy_cache', 'venv', '.venv', 'env', 'dist', 'build', '.egg-info',
    '.tox', '.coverage', 'htmlcov', '.DS_Store', '.claude', '.autonomous'
}

@dataclass
class DirectoryInfo:
    """Information about a directory"""
    path: Path
    has_readme: bool
    has_subdirs: bool
    file_count: int
    subdirs_without_readmes: List[Path] = field(default_factory=list)
    orphaned_files: List[Path] = field(default_factory=list)

class EngineReadmeScanner:
    """Scans entire engine for README issues"""

    def __init__(self, root: Path):
        self.root = root
        self.dirs_info: List[DirectoryInfo] = []
        self.missing_readmes: List[Path] = []
        self.orphaned_files: List[Tuple[Path, Path]] = []  # (file, parent_readme)
        self.readme_mismatches: List[Tuple[Path, str]] = []  # (readme, issue)

    def should_skip(self, path: Path) -> bool:
        """Check if path should be skipped"""
        for part in path.parts:
            if part in SKIP_DIRS:
                return True
        return False

    def scan_directory(self, path: Path = None, depth: int = 0) -> DirectoryInfo:
        """Recursively scan directory"""
        if path is None:
            path = self.root

        if self.should_skip(path):
            return None

        has_readme = (path / "README.md").exists()
        subdirs = []
        files = []

        try:
            for item in path.iterdir():
                if item.is_dir() and not self.should_skip(item):
                    subdirs.append(item)
                elif item.is_file():
                    files.append(item)
        except PermissionError:
            pass

        info = DirectoryInfo(
            path=path,
            has_readme=has_readme,
            has_subdirs=len(subdirs) > 0,
            file_count=len(files)
        )

        # Check for missing READMEs in subdirs
        for subdir in subdirs:
            if not (subdir / "README.md").exists():
                info.subdirs_without_readmes.append(subdir)
                if depth < 4:  # Only track first few levels
                    self.missing_readmes.append(subdir)

        # Check for orphaned files
        if has_readme:
            readme_content = (path / "README.md").read_text(encoding='utf-8', errors='ignore')
            for f in files:
                if f.name == "README.md":
                    continue
                if f.suffix == '.md':
                    if not self.is_file_linked(f, readme_content):
                        info.orphaned_files.append(f)
                        self.orphaned_files.append((f, path / "README.md"))

        # Recurse
        for subdir in subdirs:
            sub_info = self.scan_directory(subdir, depth + 1)
            if sub_info:
                self.dirs_info.append(sub_info)

        return info

    def is_file_linked(self, file_path: Path, readme_content: str) -> bool:
        """Check if file is linked from README"""
        patterns = [
            rf"\[.*?\]\({re.escape(file_path.name)}",
            rf"\[.*?\]\({re.escape(file_path.name.lower())}",
            rf"\[.*?{re.escape(file_path.stem)}.*?\]\(",
        ]
        for pattern in patterns:
            if re.search(pattern, readme_content, re.IGNORECASE):
                return True
        return False

    def analyze(self):
        """Run full analysis"""
        print("🔍 Scanning entire Blackbox5 engine...")
        self.scan_directory()

    def print_report(self):
        """Print comprehensive report"""
        print("\n" + "="*80)
        print("BLACKBOX5 ENGINE README ANALYSIS")
        print("="*80)

        # Summary
        total_dirs = len(self.dirs_info)
        dirs_with_readme = sum(1 for d in self.dirs_info if d.has_readme)
        dirs_without_readme = total_dirs - dirs_with_readme

        print(f"\n📊 SUMMARY")
        print(f"   Total directories scanned: {total_dirs}")
        print(f"   Directories with README: {dirs_with_readme}")
        print(f"   Directories without README: {dirs_without_readme}")
        print(f"   Orphaned markdown files: {len(self.orphaned_files)}")

        # Missing READMEs by area
        if self.missing_readmes:
            print(f"\n❌ DIRECTORIES WITHOUT README ({len(self.missing_readmes)})")
            print("-" * 80)

            by_area = defaultdict(list)
            for path in self.missing_readmes:
                rel = path.relative_to(self.root)
                area = rel.parts[0] if rel.parts else "root"
                by_area[area].append(rel)

            for area, paths in sorted(by_area.items()):
                print(f"\n   📁 {area}/")
                for p in paths[:10]:
                    print(f"      - {p}")
                if len(paths) > 10:
                    print(f"      ... and {len(paths) - 10} more")

        # Critical missing READMEs (directories with files)
        critical_missing = [d for d in self.dirs_info if not d.has_readme and d.file_count > 0]
        if critical_missing:
            print(f"\n🚨 CRITICAL: Directories with files but no README ({len(critical_missing)})")
            print("-" * 80)
            for info in critical_missing[:15]:
                rel = info.path.relative_to(self.root)
                print(f"   - {rel}/ ({info.file_count} files)")

        # Orphaned files by area
        if self.orphaned_files:
            print(f"\n📄 ORPHANED FILES (not linked from parent README)")
            print("-" * 80)

            by_area = defaultdict(list)
            for file_path, readme_path in self.orphaned_files:
                rel = file_path.relative_to(self.root)
                area = rel.parts[0] if rel.parts else "root"
                by_area[area].append(rel)

            for area, files in sorted(by_area.items()):
                print(f"\n   📁 {area}/ ({len(files)} files)")
                for f in files[:5]:
                    print(f"      - {f.name}")
                if len(files) > 5:
                    print(f"      ... and {len(files) - 5} more")

        # Recommendations
        print(f"\n💡 RECOMMENDATIONS")
        print("-" * 80)

        if dirs_without_readme > 50:
            print("   🔴 HIGH PRIORITY: Many directories lack READMEs")
            print("      → Focus on directories with files first")
        elif dirs_without_readme > 20:
            print("   🟡 MEDIUM PRIORITY: Some directories lack READMEs")
        else:
            print("   🟢 LOW PRIORITY: Most directories have READMEs")

        if len(self.orphaned_files) > 100:
            print(f"   🔴 HIGH PRIORITY: {len(self.orphaned_files)} orphaned files")
            print("      → Run ./bin/fix-docs-links.py --fix-orphans")
        elif len(self.orphaned_files) > 50:
            print(f"   🟡 MEDIUM PRIORITY: {len(self.orphaned_files)} orphaned files")

        print("\n" + "="*80)

    def generate_readme_template(self, dir_path: Path) -> str:
        """Generate a README template for a directory"""
        dir_name = dir_path.name.replace('-', ' ').replace('_', ' ').title()

        # List files in directory
        files = []
        subdirs = []
        try:
            for item in sorted(dir_path.iterdir()):
                if item.is_dir():
                    subdirs.append(item.name)
                elif item.is_file() and item.suffix == '.md':
                    files.append(item.name)
        except:
            pass

        lines = [
            f"# {dir_name}",
            "",
            f"Brief description of {dir_name}.",
            "",
        ]

        if subdirs:
            lines.extend(["## Subdirectories", ""])
            for subdir in subdirs:
                lines.append(f"- [{subdir}/](./{subdir}/)")
            lines.append("")

        if files:
            lines.extend(["## Files", ""])
            for f in files:
                if f != "README.md":
                    name = f.replace('.md', '').replace('-', ' ').title()
                    lines.append(f"- [{name}](./{f})")
            lines.append("")

        lines.extend([
            "## Purpose",
            "",
            "What this directory contains and why.",
            "",
        ])

        return '\n'.join(lines)

    def create_missing_readmes(self, dry_run: bool = True):
        """Create READMEs for directories that need them"""
        created = 0
        skipped = 0

        # Prioritize directories with files
        candidates = sorted(
            [d for d in self.dirs_info if not d.has_readme and d.file_count > 0],
            key=lambda x: x.file_count,
            reverse=True
        )

        print(f"\n{'='*80}")
        print("CREATING MISSING READMEs")
        print(f"{'='*80}")
        print(f"Found {len(candidates)} directories that need READMEs")
        print(f"Mode: {'DRY RUN' if dry_run else 'LIVE'}")
        print()

        for info in candidates[:20]:  # Limit to first 20
            rel_path = info.path.relative_to(self.root)
            readme_path = info.path / "README.md"

            print(f"📁 {rel_path}/")
            print(f"   Files: {info.file_count}")

            if dry_run:
                print(f"   Would create: {readme_path}")
            else:
                template = self.generate_readme_template(info.path)
                readme_path.write_text(template, encoding='utf-8')
                print(f"   ✅ Created: {readme_path}")
                created += 1

            print()

        if not dry_run:
            print(f"Created {created} READMEs")

def main():
    parser = argparse.ArgumentParser(
        description="Scan Blackbox5 engine for README issues"
    )
    parser.add_argument(
        '--missing',
        action='store_true',
        help='Only show missing READMEs'
    )
    parser.add_argument(
        '--orphaned',
        action='store_true',
        help='Only show orphaned files'
    )
    parser.add_argument(
        '--create',
        action='store_true',
        help='Create missing READMEs (not dry run)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        default=True,
        help='Show what would be created (default)'
    )

    args = parser.parse_args()

    scanner = EngineReadmeScanner(BB5_ROOT)
    scanner.analyze()

    if args.create:
        scanner.create_missing_readmes(dry_run=False)
    else:
        scanner.print_report()

if __name__ == "__main__":
    main()
