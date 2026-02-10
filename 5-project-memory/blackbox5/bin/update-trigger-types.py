#!/usr/bin/env python3
"""
Update auto-trigger rules in skill-registry.yaml to add trigger_type field.

This adds trigger_type to each rule:
- clear: Exact domain matches, decision questions, PRD + feature definition
- discretionary: General keyword matches
"""

import yaml
from pathlib import Path
import shutil


def load_yaml(file_path):
    with open(file_path, 'r') as f:
        return yaml.safe_load(f)


def save_yaml(file_path, data):
    with open(file_path, 'w') as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False)


# Define trigger types for each rule
TRIGGER_TYPES = {
    'ATR-001': 'discretionary',  # Implementation - general domain keyword match
    'ATR-002': 'discretionary',  # Analysis - general keyword match
    'ATR-003': 'discretionary',  # Architecture - general keyword match
    'ATR-004': 'clear',  # Decision questions - "Should we..." format
    'ATR-005': 'clear',  # PRD - PRD + feature definition
    'ATR-006': 'discretionary',  # QA - general keyword match
    'ATR-007': 'discretionary',  # Multi-file - general indicator
    'ATR-008': 'discretionary',  # Git - general keyword match
    'ATR-009': 'discretionary',  # Database - general keyword match
    'ATR-010': 'discretionary',  # Continuous improvement - general keyword match
}


def main():
    # Set up path
    registry_path = Path('/opt/blackbox5/5-project-memory/blackbox5/operations/skill-registry.yaml')

    # Create backup
    backup_path = registry_path.with_suffix('.yaml.backup')
    shutil.copy2(registry_path, backup_path)
    print(f"Backup created: {backup_path}")

    # Load registry
    print(f"Loading registry from: {registry_path}")
    registry = load_yaml(registry_path)

    # Update auto_trigger_rules
    if 'selection_framework' in registry and 'auto_trigger_rules' in registry['selection_framework']:
        rules = registry['selection_framework']['auto_trigger_rules']

        updated_count = 0
        for rule in rules:
            rule_id = rule.get('rule_id')
            if rule_id in TRIGGER_TYPES:
                if 'trigger_type' not in rule:
                    rule['trigger_type'] = TRIGGER_TYPES[rule_id]
                    updated_count += 1
                    print(f"  ✓ Added trigger_type '{TRIGGER_TYPES[rule_id]}' to {rule_id}")
                elif rule['trigger_type'] != TRIGGER_TYPES[rule_id]:
                    print(f"  ⚠ {rule_id} already has trigger_type '{rule['trigger_type']}' (expected '{TRIGGER_TYPES[rule_id]}')")
                else:
                    print(f"  ✓ {rule_id} already has correct trigger_type")

        print(f"\nTotal rules updated: {updated_count}")
    else:
        print("ERROR: selection_framework or auto_trigger_rules not found")
        return 1

    # Save updated registry
    save_yaml(registry_path, registry)
    print(f"Saved updated registry to: {registry_path}")

    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main())
