#!/usr/bin/env python3
"""
Documentation Link Fixer - Safe, Incremental Improvements

Analyzes docs structure and SUGGESTS fixes without making changes.
Only fixes things when you explicitly approve.

Usage:
    ./bin/fix-docs-links.py --analyze          # Show what needs fixing
    ./bin/fix-docs-links.py --fix-orphans      # Interactive fix orphaned files
    ./bin/fix-docs-links.py --fix-readmes      # Fix README mismatches
    ./bin/fix-docs-links.py --dry-run          # Preview all changes
"""

import os
import re
import argparse
from pathlib import Path
from typing import List, Tuple, Optional
from dataclasses import dataclass

DOCS_ROOT = Path("/Users/shaansisodia/.blackbox5/1-docs")

@dataclass
class OrphanedFile:
    """A file not linked from its parent README"""
    path: Path
    rel_path: Path
    parent_readme: Path
    suggested_section: str = ""

@dataclass
class ReadmeMismatch:
    """A directory not mentioned in parent README"""
    dir_path: Path
    dir_name: str
    parent_readme: Path
    readme_content: str

class DocsLinkFixer:
    """Analyzes and fixes documentation link issues"""

    def __init__(self, docs_root: Path):
        self.docs_root = docs_root
        self.orphaned_files: List[OrphanedFile] = []
        self.readme_mismatches: List[ReadmeMismatch] = []
        self.changes_made: List[str] = []

    def find_all_md_files(self) -> List[Path]:
        """Find all markdown files"""
        files = []
        for path in self.docs_root.rglob("*.md"):
            if path.name == "INDEX.md":
                continue
            files.append(path)
        return sorted(files)

    def is_linked_in_readme(self, file_path: Path, readme_content: str) -> bool:
        """Check if file is linked from README"""
        file_name = file_path.name
        file_stem = file_path.stem

        # Various link patterns to check
        patterns = [
            rf"\[.*?\]\({re.escape(file_name)}",
            rf"\[.*?\]\({re.escape(file_name.lower())}",
            rf"\[.*?\]\({re.escape(file_stem)}",
            rf"\[.*?\]\({re.escape(file_stem.lower())}",
            rf"\[.*?{re.escape(file_stem)}.*?\]\(",
        ]

        for pattern in patterns:
            if re.search(pattern, readme_content, re.IGNORECASE):
                return True
        return False

    def find_orphaned_files(self):
        """Find files not linked from their parent README"""
        all_files = self.find_all_md_files()

        for file_path in all_files:
            if file_path.name == "README.md":
                continue

            parent_dir = file_path.parent
            readme_path = parent_dir / "README.md"

            if not readme_path.exists():
                continue

            readme_content = readme_path.read_text(encoding='utf-8', errors='ignore')

            if not self.is_linked_in_readme(file_path, readme_content):
                # Suggest a section based on filename
                suggested = self.suggest_section(file_path)

                self.orphaned_files.append(OrphanedFile(
                    path=file_path,
                    rel_path=file_path.relative_to(self.docs_root),
                    parent_readme=readme_path,
                    suggested_section=suggested
                ))

    def suggest_section(self, file_path: Path) -> str:
        """Suggest which README section a file should go in"""
        name = file_path.name.lower()

        if any(x in name for x in ['quickstart', 'quick-start', 'start', 'setup']):
            return "Getting Started"
        elif any(x in name for x in ['guide', 'tutorial', 'howto', 'how-to']):
            return "Guides"
        elif any(x in name for x in ['design', 'architecture', 'pattern']):
            return "Design"
        elif any(x in name for x in ['impl', 'code', 'dev']):
            return "Implementation"
        elif any(x in name for x in ['ref', 'summary', 'cheatsheet']):
            return "Reference"
        else:
            return "Other Files"

    def find_readme_mismatches(self):
        """Find directories not mentioned in parent README"""
        for dir_path in sorted(self.docs_root.rglob("*")):
            if not dir_path.is_dir():
                continue
            if dir_path.name.startswith('.'):
                continue

            parent_dir = dir_path.parent
            if parent_dir == self.docs_root:
                continue  # Skip root level

            readme_path = parent_dir / "README.md"
            if not readme_path.exists():
                continue

            readme_content = readme_path.read_text(encoding='utf-8', errors='ignore')
            dir_name = dir_path.name

            # Check if directory is mentioned
            if dir_name not in readme_content:
                self.readme_mismatches.append(ReadmeMismatch(
                    dir_path=dir_path,
                    dir_name=dir_name,
                    parent_readme=readme_path,
                    readme_content=readme_content
                ))

    def analyze(self):
        """Run all analysis"""
        print("🔍 Analyzing documentation structure...")
        self.find_orphaned_files()
        self.find_readme_mismatches()

    def print_report(self):
        """Print analysis report"""
        print("\n" + "="*70)
        print("DOCUMENTATION LINK ANALYSIS REPORT")
        print("="*70)

        print(f"\n📊 SUMMARY")
        print(f"   Orphaned files: {len(self.orphaned_files)}")
        print(f"   README mismatches: {len(self.readme_mismatches)}")

        if self.orphaned_files:
            print(f"\n📄 ORPHANED FILES (not linked from parent README)")
            print("-" * 70)

            # Group by parent README
            by_readme = {}
            for orphan in self.orphaned_files:
                key = str(orphan.parent_readme.relative_to(self.docs_root))
                if key not in by_readme:
                    by_readme[key] = []
                by_readme[key].append(orphan)

            for readme, orphans in sorted(by_readme.items()):
                print(f"\n   In: {readme}")
                for orphan in orphans:
                    print(f"      - {orphan.rel_path.name}")
                    print(f"        Suggested section: {orphan.suggested_section}")

        if self.readme_mismatches:
            print(f"\n📁 DIRECTORIES NOT IN PARENT README")
            print("-" * 70)

            # Group by parent README
            by_parent = {}
            for mismatch in self.readme_mismatches:
                key = str(mismatch.parent_readme.relative_to(self.docs_root))
                if key not in by_parent:
                    by_parent[key] = []
                by_parent[key].append(mismatch)

            for readme, mismatches in sorted(by_parent.items()):
                print(f"\n   Parent README: {readme}")
                for m in mismatches:
                    print(f"      - {m.dir_name}/")

        print("\n" + "="*70)

    def interactive_fix_orphans(self):
        """Interactively fix orphaned files"""
        if not self.orphaned_files:
            print("✅ No orphaned files found!")
            return

        print(f"\n🔧 FIXING ORPHANED FILES ({len(self.orphaned_files)} found)")
        print("-" * 70)

        fixed = 0
        skipped = 0

        for orphan in self.orphaned_files:
            print(f"\n📄 {orphan.rel_path}")
            print(f"   Parent README: {orphan.parent_readme.relative_to(self.docs_root)}")
            print(f"   Suggested section: {orphan.suggested_section}")

            # Show current README sections
            readme_content = orphan.parent_readme.read_text(encoding='utf-8', errors='ignore')
            sections = re.findall(r'^##+ (.+)$', readme_content, re.MULTILINE)

            if sections:
                print(f"\n   Existing sections in README:")
                for i, section in enumerate(sections[:5], 1):
                    print(f"      {i}. {section}")
                if len(sections) > 5:
                    print(f"      ... and {len(sections) - 5} more")

            response = input(f"\n   Add link to this file? (y/n/q/skip-all): ").lower().strip()

            if response == 'q':
                break
            elif response == 'skip-all':
                skipped += len(self.orphaned_files) - fixed
                break
            elif response in ('y', 'yes'):
                self._add_link_to_readme(orphan)
                fixed += 1
            else:
                skipped += 1

        print(f"\n✅ Fixed: {fixed}, Skipped: {skipped}")

    def _add_link_to_readme(self, orphan: OrphanedFile):
        """Add a link to the parent README"""
        readme_path = orphan.parent_readme
        content = readme_path.read_text(encoding='utf-8', errors='ignore')

        # Create link text
        file_name = orphan.path.stem.replace('-', ' ').replace('_', ' ').title()
        link_text = f"- [{file_name}](./{orphan.path.name})"

        # Try to find appropriate section
        section_pattern = rf"(##+ {orphan.suggested_section}.*?)(\n##+ |\Z)"
        match = re.search(section_pattern, content, re.DOTALL | re.IGNORECASE)

        if match:
            # Add to existing section
            insert_pos = match.end(1)
            new_content = content[:insert_pos] + "\n" + link_text + content[insert_pos:]
        else:
            # Add to end of file
            new_content = content.rstrip() + f"\n\n## {orphan.suggested_section}\n\n{link_text}\n"

        # Write back
        readme_path.write_text(new_content, encoding='utf-8')
        print(f"   ✅ Added link to {readme_path.name}")
        self.changes_made.append(f"Added link to {orphan.rel_path} in {readme_path.relative_to(self.docs_root)}")

    def generate_fix_plan(self) -> str:
        """Generate a fix plan markdown file"""
        lines = [
            "# Documentation Link Fix Plan",
            "",
            f"Generated: {__import__('datetime').datetime.now().isoformat()}",
            "",
            "## Issues Found",
            "",
            f"- **Orphaned Files**: {len(self.orphaned_files)}",
            f"- **README Mismatches**: {len(self.readme_mismatches)}",
            "",
            "## Orphaned Files to Link",
            "",
        ]

        # Group by parent README
        by_readme = {}
        for orphan in self.orphaned_files:
            key = str(orphan.parent_readme.relative_to(self.docs_root))
            if key not in by_readme:
                by_readme[key] = []
            by_readme[key].append(orphan)

        for readme, orphans in sorted(by_readme.items()):
            lines.append(f"\n### {readme}\n")
            for orphan in orphans:
                file_name = orphan.path.stem.replace('-', ' ').replace('_', ' ').title()
                lines.append(f"- [ ] Add: `[{file_name}](./{orphan.path.name})`")
                lines.append(f"  - Section: {orphan.suggested_section}")
                lines.append(f"  - File: `{orphan.rel_path}`")
                lines.append("")

        lines.extend([
            "",
            "## Directories to Add to READMEs",
            "",
        ])

        by_parent = {}
        for mismatch in self.readme_mismatches:
            key = str(mismatch.parent_readme.relative_to(self.docs_root))
            if key not in by_parent:
                by_parent[key] = []
            by_parent[key].append(mismatch)

        for readme, mismatches in sorted(by_parent.items()):
            lines.append(f"\n### {readme}\n")
            for m in mismatches:
                lines.append(f"- [ ] Add directory: `{m.dir_name}/`")
                lines.append("")

        lines.extend([
            "",
            "## How to Fix",
            "",
            "1. Review this plan",
            "2. Edit each README to add the suggested links",
            "3. Run `./bin/fix-docs-links.py --analyze` to verify",
            "",
            "Or run `./bin/fix-docs-links.py --fix-orphans` for interactive fixing.",
            "",
        ])

        return '\n'.join(lines)

    def save_fix_plan(self):
        """Save fix plan to file"""
        plan = self.generate_fix_plan()
        plan_path = self.docs_root / "FIX_PLAN.md"
        plan_path.write_text(plan, encoding='utf-8')
        print(f"\n📝 Fix plan saved to: {plan_path}")
        print("   Review and edit, or run with --fix-orphans for interactive mode")

def main():
    parser = argparse.ArgumentParser(
        description="Fix documentation link issues safely"
    )
    parser.add_argument(
        '--analyze',
        '-a',
        action='store_true',
        help='Analyze and show report (default)'
    )
    parser.add_argument(
        '--fix-orphans',
        action='store_true',
        help='Interactively fix orphaned files'
    )
    parser.add_argument(
        '--fix-readmes',
        action='store_true',
        help='Fix README mismatches'
    )
    parser.add_argument(
        '--save-plan',
        action='store_true',
        help='Save fix plan to FIX_PLAN.md'
    )

    args = parser.parse_args()

    fixer = DocsLinkFixer(DOCS_ROOT)
    fixer.analyze()

    if args.fix_orphans:
        fixer.interactive_fix_orphans()
    elif args.fix_readmes:
        print("README fix not yet implemented. Use --save-plan to generate fix list.")
    elif args.save_plan:
        fixer.save_fix_plan()
    else:
        fixer.print_report()
        print("\n💡 Next steps:")
        print("   --save-plan     Save detailed fix plan to FIX_PLAN.md")
        print("   --fix-orphans   Interactive fix mode")

if __name__ == "__main__":
    main()
