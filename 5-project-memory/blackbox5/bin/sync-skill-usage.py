#!/usr/bin/env python3
"""
Sync skill usage data from skill-usage.yaml to skill-registry.yaml

This script reads usage statistics from the deprecated skill-usage.yaml file
and syncs them to the unified skill-registry.yaml file.
"""

import sys
import os
from pathlib import Path
from datetime import datetime
import json
import shutil
import yaml

# Add lib directory to path
lib_dir = Path(__file__).parent.parent / '.autonomous' / 'lib'
sys.path.insert(0, str(lib_dir))

# Paths
PROJECT_DIR = Path(__file__).parent.parent
operations_dir = PROJECT_DIR / 'operations'
autonomous_ops_dir = PROJECT_DIR / '.autonomous' / 'operations'

SOURCE_FILE = autonomous_ops_dir / 'skill-usage.yaml'
TARGET_FILE = operations_dir / 'skill-registry.yaml'
BACKUP_FILE = operations_dir / f'skill-registry.yaml.backup.{datetime.now().strftime("%Y%m%d_%H%M%S")}'

def load_yaml_file(file_path):
    """Load YAML file with error handling."""
    try:
        with open(file_path, 'r') as f:
            return yaml.safe_load(f) or {}
    except FileNotFoundError:
        print(f"⚠️  Warning: File not found: {file_path}")
        return {}
    except yaml.YAMLError as e:
        print(f"❌ Error parsing YAML file {file_path}: {e}")
        return {}

def save_yaml_file(data, file_path):
    """Save data to YAML file."""
    with open(file_path, 'w') as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False)
    print(f"✅ Saved: {file_path}")

def sync_skill_usage():
    """Sync skill usage data from source to target."""
    print("=" * 60)
    print("Skill Usage Sync Script")
    print("=" * 60)

    # Load source and target files
    print(f"\n📖 Loading source file: {SOURCE_FILE}")
    source_data = load_yaml_file(SOURCE_FILE)
    if not source_data:
        print("❌ No data found in source file. Aborting.")
        return False

    print(f"📖 Loading target file: {TARGET_FILE}")
    target_data = load_yaml_file(TARGET_FILE)
    if not target_data:
        print("❌ No data found in target file. Aborting.")
        return False

    # Create backup
    print(f"\n💾 Creating backup: {BACKUP_FILE}")
    shutil.copy2(TARGET_FILE, BACKUP_FILE)
    print("✅ Backup created")

    # Get skills sections
    source_skills = source_data.get('skills', [])
    target_skills = target_data.get('skills', {})

    print(f"\n📊 Source skills: {len(source_skills)} entries")
    print(f"📊 Target skills: {len(target_skills)} entries")

    # Sync usage data
    sync_count = 0
    for source_skill in source_skills:
        skill_name = source_skill.get('name')
        if not skill_name:
            continue

        if skill_name not in target_skills:
            print(f"⚠️  Warning: Skill '{skill_name}' not found in target registry. Skipping.")
            continue

        # Update usage data
        target_skill = target_skills[skill_name]
        usage = target_skill.get('usage', {})

        # Sync usage fields
        updates = {}
        if source_skill.get('usage_count', 0) > usage.get('usage_count', 0):
            updates['usage_count'] = source_skill['usage_count']
        if source_skill.get('success_count', 0) > usage.get('success_count', 0):
            updates['success_count'] = source_skill['success_count']
        if source_skill.get('failure_count', 0) > usage.get('failure_count', 0):
            updates['failure_count'] = source_skill['failure_count']
        if source_skill.get('last_used'):
            if not usage.get('last_used') or source_skill['last_used'] > usage['last_used']:
                updates['last_used'] = source_skill['last_used']
        if source_skill.get('first_used'):
            if not usage.get('first_used') or source_skill['first_used'] < usage['first_used']:
                updates['first_used'] = source_skill['first_used']

        if updates:
            usage.update(updates)
            target_skill['usage'] = usage
            target_skills[skill_name] = target_skill
            sync_count += 1
            print(f"✅ Updated '{skill_name}': {updates}")

    # Update total usage records in metadata
    total_usage_records = source_data.get('metadata', {}).get('total_invocations', 0)
    target_data.setdefault('metadata', {})['total_usage_records'] = total_usage_records

    # Sync usage_log to task_outcomes if not present OR backfill null skill_used
    usage_log = source_data.get('usage_log', [])
    if usage_log:
        task_outcomes = target_data.get('task_outcomes', [])
        # Create a mapping of task_id to index for O(1) lookups
        task_id_to_index = {o.get('task_id'): i for i, o in enumerate(task_outcomes)}

        for log_entry in usage_log:
            task_id = log_entry.get('task_id')
            skill = log_entry.get('skill')

            if not task_id or not skill:
                continue

            if task_id not in task_id_to_index:
                # Create task outcome entry from usage log
                outcome = {
                    'task_id': task_id,
                    'timestamp': log_entry.get('timestamp'),
                    'skill_used': skill,
                    'task_type': log_entry.get('result', 'unknown'),
                    'duration_minutes': None,
                    'outcome': log_entry.get('result', 'unknown'),
                    'quality_rating': None,
                    'trigger_was_correct': None,
                    'would_use_again': None,
                    'notes': log_entry.get('notes', '')
                }
                task_outcomes.append(outcome)
                sync_count += 1
                print(f"✅ Added task outcome: {task_id}")
            else:
                # Backfill existing task outcome if skill_used is null
                existing_outcome = task_outcomes[task_id_to_index[task_id]]
                if existing_outcome.get('skill_used') is None:
                    existing_outcome['skill_used'] = skill
                    # Update task_type from result if unknown
                    if existing_outcome.get('task_type') == 'unknown' and log_entry.get('result'):
                        existing_outcome['task_type'] = log_entry.get('result')
                    # Update outcome from result if unknown
                    if existing_outcome.get('outcome') == 'unknown' and log_entry.get('result'):
                        existing_outcome['outcome'] = log_entry.get('result')
                    # Add notes if not present
                    if not existing_outcome.get('notes') and log_entry.get('notes'):
                        existing_outcome['notes'] = log_entry.get('notes')
                    sync_count += 1
                    print(f"✅ Backfilled skill_used for {task_id}: {skill}")

        target_data['task_outcomes'] = task_outcomes

    # Save updated target file
    target_data['skills'] = target_skills
    print(f"\n💾 Saving updated target file...")
    save_yaml_file(target_data, TARGET_FILE)

    # Summary
    print("\n" + "=" * 60)
    print("Sync Summary")
    print("=" * 60)
    print(f"✅ Skills updated: {sync_count}")
    print(f"✅ Total usage records: {total_usage_records}")
    print(f"✅ Target file updated: {TARGET_FILE}")
    print(f"✅ Backup saved: {BACKUP_FILE}")

    # Validation
    print("\n🔍 Validating sync...")
    target_data_check = load_yaml_file(TARGET_FILE)
    if target_data_check:
        print("✅ Target file is valid YAML")
        updated_skills = [s for s in target_data_check.get('skills', {}).values()
                         if s.get('usage', {}).get('usage_count', 0) > 0]
        print(f"✅ Skills with usage data: {len(updated_skills)}")

    return True

def main():
    """Main entry point."""
    dry_run = '--dry-run' in sys.argv

    if dry_run:
        print("🔍 DRY RUN MODE - No changes will be made\n")

    try:
        if not dry_run:
            result = sync_skill_usage()
            if result:
                print("\n✅ Sync completed successfully!")
                return 0
            else:
                print("\n❌ Sync failed!")
                return 1
        else:
            print("Dry run complete. No files modified.")
            return 0
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    sys.exit(main())
