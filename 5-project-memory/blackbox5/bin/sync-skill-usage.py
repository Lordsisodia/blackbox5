#!/usr/bin/env python3
"""
Sync skill-usage.yaml to skill-registry.yaml

This script reads usage data from skill-usage.yaml and updates the unified
skill-registry.yaml with current usage statistics and history.
"""

import yaml
from pathlib import Path
from datetime import datetime
import shutil
import sys


def load_yaml_file(file_path):
    """Load a YAML file safely."""
    try:
        with open(file_path, 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"Error: File not found: {file_path}")
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"Error: Invalid YAML in {file_path}: {e}")
        sys.exit(1)


def save_yaml_file(file_path, data):
    """Save data to a YAML file."""
    with open(file_path, 'w') as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False)


def backup_file(file_path):
    """Create a backup of the file."""
    backup_path = file_path.with_suffix('.yaml.backup')
    shutil.copy2(file_path, backup_path)
    print(f"Created backup: {backup_path}")
    return backup_path


def sync_skill_usage(registry_file, usage_file):
    """
    Sync usage data from skill-usage.yaml to skill-registry.yaml.

    This updates:
    1. usage section for each skill (usage_count, success_count, etc.)
    2. usage_history with new log entries
    3. metadata with updated counts
    """
    print(f"Loading registry from: {registry_file}")
    print(f"Loading usage data from: {usage_file}")

    registry = load_yaml_file(registry_file)
    usage_data = load_yaml_file(usage_file)

    # Initialize skills section if it doesn't exist
    if 'skills' not in registry:
        registry['skills'] = {}

    # Initialize usage_history if it doesn't exist
    if 'usage_history' not in registry:
        registry['usage_history'] = []

    # Track new entries to add
    new_history_entries = []
    skills_updated = set()

    # Process each skill from usage_data
    for skill_usage in usage_data.get('skills', []):
        skill_name = skill_usage['name']

        if skill_name in registry['skills']:
            # Update skill usage section in registry
            skill_entry = registry['skills'][skill_name]

            if 'usage' not in skill_entry:
                skill_entry['usage'] = {}

            skill_entry['usage']['usage_count'] = skill_usage.get('usage_count', 0)
            skill_entry['usage']['success_count'] = skill_usage.get('success_count', 0)
            skill_entry['usage']['failure_count'] = skill_usage.get('failure_count', 0)
            skill_entry['usage']['first_used'] = skill_usage.get('first_used')
            skill_entry['usage']['last_used'] = skill_usage.get('last_used')

            print(f"  ✓ Updated usage for: {skill_name}")
            skills_updated.add(skill_name)
        else:
            print(f"  ⚠ Skill not found in registry: {skill_name}")

    # Process usage log entries
    existing_timestamps = {entry.get('timestamp') for entry in registry['usage_history']}

    for log_entry in usage_data.get('usage_log', []):
        timestamp = log_entry.get('timestamp')
        if timestamp and timestamp not in existing_timestamps:
            new_history_entries.append(log_entry)

    if new_history_entries:
        registry['usage_history'].extend(new_history_entries)
        print(f"  ✓ Added {len(new_history_entries)} new usage history entries")

    # Update metadata
    if 'metadata' not in registry:
        registry['metadata'] = {}

    registry['metadata']['last_updated'] = datetime.now().isoformat() + 'Z'
    registry['metadata']['total_usage_records'] = len(registry['usage_history'])
    registry['metadata']['total_invocations'] = sum(
        skill.get('usage', {}).get('usage_count', 0)
        for skill in registry['skills'].values()
    )

    # Update task_outcomes if there are new usage entries with task results
    if 'task_outcomes' not in registry:
        registry['task_outcomes'] = []

    for log_entry in usage_data.get('usage_log', []):
        task_id = log_entry.get('task_id')
        if task_id:
            # Check if task outcome already exists
            existing = [
                t for t in registry['task_outcomes']
                if t.get('task_id') == task_id
            ]

            if not existing:
                # Create new task outcome entry
                new_outcome = {
                    'task_id': task_id,
                    'timestamp': log_entry.get('timestamp'),
                    'skill_used': log_entry.get('skill'),
                    'task_type': 'unknown',
                    'duration_minutes': None,
                    'outcome': log_entry.get('result', 'unknown'),
                    'quality_rating': None,
                    'trigger_was_correct': None,
                    'would_use_again': None,
                    'notes': log_entry.get('notes', '')
                }
                registry['task_outcomes'].append(new_outcome)

    return registry, len(skills_updated), len(new_history_entries)


def main():
    """Main sync function."""
    # Set up paths - support both /opt/blackbox5 and ~/.blackbox5 locations
    home_path = Path.home() / '.blackbox5' / '5-project-memory' / 'blackbox5'
    opt_path = Path('/opt/blackbox5/5-project-memory/blackbox5')

    # Use opt_path if it exists, otherwise fall back to home_path
    if opt_path.exists():
        bb5_dir = opt_path
    else:
        bb5_dir = home_path

    registry_file = bb5_dir / 'operations' / 'skill-registry.yaml'
    usage_file = bb5_dir / '.autonomous' / 'operations' / 'skill-usage.yaml'

    # Verify files exist
    if not registry_file.exists():
        print(f"Error: Registry file not found: {registry_file}")
        sys.exit(1)

    if not usage_file.exists():
        print(f"Error: Usage file not found: {usage_file}")
        sys.exit(1)

    # Create backup
    backup_file(registry_file)

    # Perform sync
    updated_registry, skills_updated, history_added = sync_skill_usage(
        registry_file, usage_file
    )

    # Save updated registry
    save_yaml_file(registry_file, updated_registry)

    # Summary
    print("\n" + "=" * 60)
    print("SYNC COMPLETE")
    print("=" * 60)
    print(f"Skills updated: {skills_updated}")
    print(f"History entries added: {history_added}")
    print(f"Total invocations: {updated_registry['metadata']['total_invocations']}")
    print(f"Last updated: {updated_registry['metadata']['last_updated']}")
    print("=" * 60)

    return 0


if __name__ == '__main__':
    sys.exit(main())
