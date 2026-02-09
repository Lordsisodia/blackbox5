#!/usr/bin/env python3
"""
Sync skills from skill-registry.yaml to Claude Code native skills.

This script converts BlackBox5 skill definitions into Claude Code skill files
that can be used across any Claude Code instance.

Usage:
    sync-skills-to-claude.py [--output-dir ~/.claude/skills]
"""

import argparse
import yaml
import os
from pathlib import Path
from datetime import datetime


def load_skill_registry(registry_path: Path) -> dict:
    """Load the skill registry YAML file."""
    with open(registry_path, 'r') as f:
        return yaml.safe_load(f)


def convert_skill_to_claude_format(skill_def: dict, skill_id: str) -> str:
    """Convert a skill definition to Claude Code skill format."""

    # Extract key info
    name = skill_def.get('name', skill_id)
    description = skill_def.get('description', '')
    triggers = skill_def.get('triggers', {}).get('keywords', [])
    confidence = skill_def.get('triggers', {}).get('confidence_threshold', 0.7)
    invocation = skill_def.get('invocation', {})
    content = invocation.get('content', '')
    examples = invocation.get('examples', [])

    # Build the skill content
    skill_content = f"""# {name}

## Description
{description}

## Triggers
- **Keywords:** {', '.join(triggers) if triggers else 'None defined'}
- **Confidence Threshold:** {confidence}

## When to Use
"""

    # Add trigger contexts
    contexts = skill_def.get('triggers', {}).get('contexts', [])
    if contexts:
        for ctx in contexts:
            skill_content += f"- {ctx}\n"
    else:
        skill_content += "- When task matches skill domain\n"

    # Add invocation content
    if content:
        skill_content += f"""
## Invocation
{content}
"""

    # Add examples
    if examples:
        skill_content += "\n## Examples\n"
        for i, example in enumerate(examples, 1):
            skill_content += f"\n### Example {i}\n"
            skill_content += f"**Task:** {example.get('task', 'N/A')}\n\n"
            skill_content += f"**Skill Applied:** {example.get('application', 'N/A')}\n"

    # Add metadata
    skill_content += f"""
## Metadata
- **ID:** {skill_id}
- **Category:** {skill_def.get('category', 'uncategorized')}
- **Version:** {skill_def.get('version', '1.0.0')}
- **Auto-Invoke:** {skill_def.get('triggers', {}).get('auto_invoke', False)}
- **Last Synced:** {datetime.now().isoformat()}

---
*This skill was auto-generated from skill-registry.yaml*
"""

    return skill_content


def sync_skills(registry_path: Path, output_dir: Path, dry_run: bool = False):
    """Sync all skills from registry to Claude skills directory."""

    print(f"Loading skill registry from: {registry_path}")
    registry = load_skill_registry(registry_path)

    skills = registry.get('skills', [])
    total = len(skills)
    created = 0
    updated = 0
    skipped = 0

    print(f"Found {total} skills to sync\n")

    for skill_id, skill_def in skills.items():
        if not skill_id or not isinstance(skill_def, dict):
            print(f"⚠️  Skipping invalid skill entry")
            skipped += 1
            continue

        # Create skill directory
        skill_dir = output_dir / skill_id
        skill_file = skill_dir / 'SKILL.md'

        # Check if already exists
        exists = skill_file.exists()

        if not dry_run:
            skill_dir.mkdir(parents=True, exist_ok=True)

            # Generate skill content
            content = convert_skill_to_claude_format(skill_def, skill_id)

            # Write skill file
            with open(skill_file, 'w') as f:
                f.write(content)

        if exists:
            print(f"🔄 Updated: {skill_id}")
            updated += 1
        else:
            print(f"✅ Created: {skill_id}")
            created += 1

    # Create index file
    index_content = generate_index(skills)
    index_file = output_dir / 'INDEX.md'

    if not dry_run:
        with open(index_file, 'w') as f:
            f.write(index_content)

    print(f"\n{'='*50}")
    print(f"Sync Summary:")
    print(f"  Created: {created}")
    print(f"  Updated: {updated}")
    print(f"  Skipped: {skipped}")
    print(f"  Total: {total}")
    print(f"{'='*50}")

    if dry_run:
        print("\n⚠️  DRY RUN - No files were written")
    else:
        print(f"\n✅ Skills synced to: {output_dir}")
        print(f"📋 Index written to: {index_file}")


def generate_index(skills: dict) -> str:
    """Generate an index of all skills."""

    content = """# Claude Skills Index

Auto-generated index of all available skills.

## Quick Reference

| Skill | Category | Description | Auto-Invoke |
|-------|----------|-------------|-------------|
"""

    for skill_id, skill in skills.items():
        if not isinstance(skill, dict):
            continue
        name = skill.get('name', skill_id)
        category = skill.get('category', 'uncategorized')
        description = skill.get('description', '')[:50] + '...' if len(skill.get('description', '')) > 50 else skill.get('description', '')
        auto_invoke = skill.get('triggers', {}).get('auto_invoke', False)

        content += f"| [{name}](./{skill_id}/SKILL.md) | {category} | {description} | {'✅' if auto_invoke else '❌'} |\n"

    content += """
## Categories

"""

    # Group by category
    by_category = {}
    for skill_id, skill in skills.items():
        if not isinstance(skill, dict):
            continue
        cat = skill.get('category', 'uncategorized')
        if cat not in by_category:
            by_category[cat] = []
        by_category[cat].append((skill_id, skill))

    for category, cat_skills in sorted(by_category.items()):
        content += f"\n### {category.title()}\n\n"
        for skill_id, skill in cat_skills:
            name = skill.get('name', skill_id)
            content += f"- [{name}](./{skill_id}/SKILL.md)\n"

    content += f"""
---
*Last updated: {datetime.now().isoformat()}*
*Source: skill-registry.yaml*
"""

    return content


def main():
    parser = argparse.ArgumentParser(
        description='Sync skills from skill-registry.yaml to Claude Code native skills'
    )
    parser.add_argument(
        '--registry',
        type=Path,
        default=Path.home() / '.blackbox5' / '5-project-memory' / 'blackbox5' / 'operations' / 'skill-registry.yaml',
        help='Path to skill-registry.yaml'
    )
    parser.add_argument(
        '--output-dir',
        type=Path,
        default=Path.home() / '.claude' / 'skills',
        help='Output directory for Claude skills'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be done without writing files'
    )

    args = parser.parse_args()

    if not args.registry.exists():
        print(f"❌ Error: Registry not found at {args.registry}")
        return 1

    # Create output directory if needed
    if not args.dry_run:
        args.output_dir.mkdir(parents=True, exist_ok=True)

    sync_skills(args.registry, args.output_dir, args.dry_run)

    return 0


if __name__ == '__main__':
    exit(main())
