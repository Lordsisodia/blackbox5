#!/usr/bin/env python3
"""
Task Completion Hook - Skill Recording

Automatically records skill usage when tasks complete.
Updates skill-metrics.yaml task_outcomes and skill-usage.yaml usage_log.

Usage:
    Called automatically by task completion system or manually:
    python task_completion_skill_recorder.py --task-id TASK-xxx --skill skill-name

Environment Variables:
    BB5_TASK_ID - Task ID that completed
    BB5_SKILL_USED - Skill that was used (if any)
    BB5_OUTCOME - Task outcome (success|failure|partial)
    BB5_DURATION_MINUTES - Time spent on task
    BB5_QUALITY_RATING - Quality rating 1-5
    BB5_TRIGGER_CORRECT - Whether skill trigger was correct (true|false)
    BB5_WOULD_USE_AGAIN - Whether to use skill again (true|false)
    BB5_NOTES - Optional notes about skill usage
"""

import argparse
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml


def load_yaml_file(filepath: Path) -> dict:
    """Load and parse YAML file."""
    try:
        with open(filepath, 'r') as f:
            return yaml.safe_load(f) or {}
    except FileNotFoundError:
        print(f"Error: File not found: {filepath}", file=sys.stderr)
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"Error parsing YAML: {e}", file=sys.stderr)
        sys.exit(2)


def save_yaml_file(filepath: Path, data: dict) -> None:
    """Save data to YAML file."""
    try:
        with open(filepath, 'w') as f:
            yaml.dump(data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
    except Exception as e:
        print(f"Error saving YAML: {e}", file=sys.stderr)
        sys.exit(3)


def record_task_outcome(metrics_data: dict, outcome: dict) -> dict:
    """Record a new task outcome in skill-metrics.yaml."""
    if 'task_outcomes' not in metrics_data:
        metrics_data['task_outcomes'] = []

    # Check if outcome already exists for this task
    existing = None
    for i, o in enumerate(metrics_data['task_outcomes']):
        if o.get('task_id') == outcome['task_id']:
            existing = i
            break

    if existing is not None:
        # Update existing outcome
        metrics_data['task_outcomes'][existing].update(outcome)
        print(f"Updated existing outcome for {outcome['task_id']}")
    else:
        # Add new outcome
        metrics_data['task_outcomes'].append(outcome)
        print(f"Added new outcome for {outcome['task_id']}")

    return metrics_data


def record_usage_log(usage_data: dict, entry: dict) -> dict:
    """Record a new entry in skill-usage.yaml usage_log."""
    if 'usage_log' not in usage_data:
        usage_data['usage_log'] = []

    # Only record if a skill was actually used
    if entry.get('skill'):
        usage_data['usage_log'].append(entry)
        print(f"Added usage log entry for skill: {entry['skill']}")

        # Update skill aggregate stats
        skill_name = entry['skill']
        for skill in usage_data.get('skills', []):
            if skill['name'] == skill_name:
                # Update usage count
                skill['usage_count'] = skill.get('usage_count', 0) + 1

                # Update timestamps
                timestamp = entry.get('timestamp')
                if timestamp:
                    if not skill.get('first_used'):
                        skill['first_used'] = timestamp
                    skill['last_used'] = timestamp

                # Update success/failure counts
                result = entry.get('result')
                if result == 'success':
                    skill['success_count'] = skill.get('success_count', 0) + 1
                elif result == 'failure':
                    skill['failure_count'] = skill.get('failure_count', 0) + 1

                break

    return usage_data


def record_event(events_file: Path, event: dict) -> None:
    """Record skill usage event in events.yaml."""
    try:
        with open(events_file, 'r') as f:
            events = yaml.safe_load(f) or []
    except FileNotFoundError:
        events = []

    events.append(event)

    with open(events_file, 'w') as f:
        yaml.dump(events, f, default_flow_style=False, sort_keys=False, allow_unicode=True)


def get_env_or_default(env_var: str, default: Any = None) -> Any:
    """Get value from environment variable or return default."""
    value = os.environ.get(env_var)
    if value is None:
        return default

    # Convert boolean strings
    if value.lower() in ('true', '1', 'yes'):
        return True
    if value.lower() in ('false', '0', 'no'):
        return False

    # Convert integers
    try:
        return int(value)
    except ValueError:
        pass

    return value


def main():
    parser = argparse.ArgumentParser(description='Record skill usage on task completion')
    parser.add_argument('--task-id', type=str, help='Task ID')
    parser.add_argument('--skill', type=str, help='Skill used (null if none)')
    parser.add_argument('--outcome', type=str, choices=['success', 'failure', 'partial'],
                       help='Task outcome')
    parser.add_argument('--duration', type=int, help='Duration in minutes')
    parser.add_argument('--quality', type=int, choices=[1, 2, 3, 4, 5],
                       help='Quality rating 1-5')
    parser.add_argument('--trigger-correct', type=lambda x: x.lower() == 'true',
                       help='Whether skill trigger was correct')
    parser.add_argument('--would-use-again', type=lambda x: x.lower() == 'true',
                       help='Whether to use skill again')
    parser.add_argument('--notes', type=str, help='Optional notes')
    parser.add_argument('--project-dir', type=str, default='.',
                       help='Project directory')
    args = parser.parse_args()

    # Get values from args or environment
    task_id = args.task_id or get_env_or_default('BB5_TASK_ID')
    skill_used = args.skill or get_env_or_default('BB5_SKILL_USED')
    outcome = args.outcome or get_env_or_default('BB5_OUTCOME', 'success')
    duration = args.duration or get_env_or_default('BB5_DURATION_MINUTES')
    quality = args.quality or get_env_or_default('BB5_QUALITY_RATING')
    trigger_correct = args.trigger_correct if args.trigger_correct is not None else get_env_or_default('BB5_TRIGGER_CORRECT')
    would_use_again = args.would_use_again if args.would_use_again is not None else get_env_or_default('BB5_WOULD_USE_AGAIN')
    notes = args.notes or get_env_or_default('BB5_NOTES', '')

    if not task_id:
        print("Error: Task ID is required", file=sys.stderr)
        sys.exit(1)

    project_dir = Path(args.project_dir).resolve()
    operations_dir = project_dir / 'operations'
    agents_dir = project_dir / '.autonomous' / 'agents' / 'communications'

    # Load data files
    metrics_file = operations_dir / 'skill-metrics.yaml'
    usage_file = operations_dir / 'skill-usage.yaml'
    events_file = agents_dir / 'events.yaml'

    print(f"Recording skill usage for task: {task_id}")

    metrics_data = load_yaml_file(metrics_file)
    usage_data = load_yaml_file(usage_file)

    timestamp = datetime.now().isoformat()

    # Build task outcome entry
    task_outcome = {
        'task_id': task_id,
        'timestamp': timestamp,
        'skill_used': skill_used,
        'outcome': outcome,
    }

    if duration is not None:
        task_outcome['duration_minutes'] = duration
    if quality is not None:
        task_outcome['quality_rating'] = quality
    if trigger_correct is not None:
        task_outcome['trigger_was_correct'] = trigger_correct
    if would_use_again is not None:
        task_outcome['would_use_again'] = would_use_again
    if notes:
        task_outcome['notes'] = notes

    # Build usage log entry
    usage_entry = {
        'timestamp': timestamp,
        'skill': skill_used,
        'task_id': task_id,
        'result': outcome,
    }

    if notes:
        usage_entry['notes'] = notes

    # Build event entry
    event_entry = {
        'timestamp': timestamp,
        'type': 'skill_used' if skill_used else 'no_skill_used',
        'task_id': task_id,
        'data': {
            'skill': skill_used,
            'outcome': outcome,
        },
    }

    # Record in all locations
    metrics_data = record_task_outcome(metrics_data, task_outcome)
    usage_data = record_usage_log(usage_data, usage_entry)

    # Save updates
    save_yaml_file(metrics_file, metrics_data)
    save_yaml_file(usage_file, usage_data)

    # Record event if events file exists
    if events_file.exists():
        record_event(events_file, event_entry)
        print(f"Recorded event in: {events_file}")

    print(f"\nSkill usage recorded successfully!")
    print(f"  Task: {task_id}")
    print(f"  Skill: {skill_used or 'None'}")
    print(f"  Outcome: {outcome}")

    return 0


if __name__ == '__main__':
    sys.exit(main())
