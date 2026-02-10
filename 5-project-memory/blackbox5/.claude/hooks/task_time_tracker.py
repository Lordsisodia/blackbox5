#!/usr/bin/env python3
"""
Task Time Tracker Hook

Automatically tracks task start/end times and calculates duration.
Stores timestamps in task directory and calculates duration on completion.
Detects skill used from environment variables or THOUGHTS.md.

Integrates with task_completion_skill_recorder.py to include time data
in task outcomes.

Usage:
    Called automatically by OpenClaw hooks:
    - SessionStart: Records task start time
    - SessionEnd: Records task end time, calculates duration, updates outcome

Environment Variables:
    BB5_TASK_ID - Task ID (auto-detected from current directory)
    BB5_SKILL_USED - Skill that was used (optional)
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

import yaml


def get_current_task_id() -> Optional[str]:
    """
    Detect current task ID from directory structure.

    Returns:
        Task ID if in a task directory, None otherwise
    """
    cwd = Path.cwd()

    # Try to find task directory marker
    # BlackBox5 task directories contain task.md
    for parent in [cwd] + list(cwd.parents):
        task_file = parent / 'task.md'
        if task_file.exists():
            # Extract task ID from directory name
            task_name = parent.name
            # Validate it looks like a task ID (starts with TASK- or TEST-)
            if task_name.startswith('TASK-') or task_name.startswith('task-') or task_name.startswith('TEST-') or task_name.startswith('test-'):
                return task_name

    return None


def get_task_dir(task_id: str) -> Path:
    """Get task directory path."""
    # Check if we're already in task directory
    cwd = Path.cwd()
    if cwd.name == task_id or (cwd / 'task.md').exists():
        return cwd

    # Otherwise try to find it in active tasks directory
    bb5_dir = Path('/opt/blackbox5/5-project-memory/blackbox5')
    task_dir = bb5_dir / 'tasks' / 'active' / task_id

    if task_dir.exists():
        return task_dir

    raise FileNotFoundError(f"Task directory not found for: {task_id}")


def load_task_metadata(task_dir: Path) -> dict:
    """Load existing task metadata from .task-timing.json."""
    timing_file = task_dir / '.task-timing.json'
    if timing_file.exists():
        with open(timing_file, 'r') as f:
            return json.load(f)
    return {}


def save_task_metadata(task_dir: Path, metadata: dict) -> None:
    """Save task metadata to .task-timing.json."""
    timing_file = task_dir / '.task-timing.json'
    with open(timing_file, 'w') as f:
        json.dump(metadata, f, indent=2, default=str)


def get_skill_used_from_context(task_id: str, task_dir: Path) -> Optional[str]:
    """
    Try to detect which skill was used for this task.

    Sources (in order of priority):
    1. Environment variable BB5_SKILL_USED
    2. THOUGHTS.md file in task directory (look for skill documentation)
    3. .task-timing.json metadata (if already set)
    """
    # Check environment variable
    skill = os.environ.get('BB5_SKILL_USED')
    if skill:
        return skill if skill.lower() not in ('null', 'none', '') else None

    # Check THOUGHTS.md for skill usage section
    thoughts_file = task_dir / 'THOUGHTS.md'
    if thoughts_file.exists():
        try:
            with open(thoughts_file, 'r') as f:
                content = f.read()
                # Look for "Skill Used: X" pattern
                if 'Skill Used:' in content:
                    for line in content.split('\n'):
                        if 'Skill Used:' in line:
                            skill = line.split('Skill Used:')[-1].strip()
                            return skill if skill.lower() not in ('null', 'none', 'unknown') else None
        except Exception:
            pass

    # Check task metadata
    metadata = load_task_metadata(task_dir)
    skill = metadata.get('skill_used')
    if skill:
        return skill

    return None


def record_task_start(task_id: str) -> None:
    """Record task start time."""
    task_dir = get_task_dir(task_id)
    metadata = load_task_metadata(task_dir)

    metadata['task_id'] = task_id
    metadata['start_time'] = datetime.now().isoformat()
    metadata['start_timestamp'] = datetime.now().timestamp()

    # Initialize other fields
    metadata.setdefault('end_time', None)
    metadata.setdefault('duration_minutes', None)
    metadata.setdefault('sessions', [])

    # Track this session
    session_id = datetime.now().strftime('%Y%m%d_%H%M%S')
    metadata['sessions'].append({
        'session_id': session_id,
        'start_time': metadata['start_time'],
        'end_time': None,
        'duration_minutes': None
    })
    metadata['current_session_id'] = session_id

    save_task_metadata(task_dir, metadata)

    print(f"[Task Time Tracker] Started task: {task_id}")
    print(f"[Task Time Tracker] Start time: {metadata['start_time']}")


def record_task_end(task_id: str) -> None:
    """
    Record task end time and calculate duration.

    Updates .task-timing.json with end time and duration.
    Also attempts to update task outcome in skill-registry.yaml
    """
    task_dir = get_task_dir(task_id)
    metadata = load_task_metadata(task_dir)

    if not metadata.get('start_time'):
        print(f"[Task Time Tracker] Warning: No start time found for task {task_id}")
        return

    end_time = datetime.now()
    end_time_iso = end_time.isoformat()
    end_timestamp = end_time.timestamp()

    metadata['end_time'] = end_time_iso
    metadata['end_timestamp'] = end_timestamp

    # Calculate duration in minutes
    start_timestamp = metadata.get('start_timestamp')
    if start_timestamp:
        duration_seconds = end_timestamp - start_timestamp
        duration_minutes = round(duration_seconds / 60, 2)
        metadata['duration_minutes'] = duration_minutes

        # Update current session
        if metadata.get('current_session_id'):
            session_id = metadata['current_session_id']
            for session in metadata.get('sessions', []):
                if session.get('session_id') == session_id:
                    session['end_time'] = end_time_iso
                    session['duration_minutes'] = duration_minutes
                    break

    save_task_metadata(task_dir, metadata)

    print(f"[Task Time Tracker] Ended task: {task_id}")
    print(f"[Task Time Tracker] End time: {end_time_iso}")
    print(f"[Task Time Tracker] Duration: {metadata.get('duration_minutes')} minutes")

    # Try to update task outcome with time data
    update_task_outcome_with_time(task_id, metadata, task_dir)


def update_task_outcome_with_time(task_id: str, timing_metadata: dict, task_dir: Path) -> None:
    """
    Update existing task outcome with time tracking data and skill attribution.

    Looks for task outcomes in skill-registry.yaml (task_outcomes section).
    Updates the entry with duration_minutes and skill_used if present.
    """
    duration_minutes = timing_metadata.get('duration_minutes')
    if not duration_minutes:
        return

    skill_used = get_skill_used_from_context(task_id, task_dir)

    if skill_used:
        print(f"[Task Time Tracker] Detected skill: {skill_used}")

    bb5_dir = Path('/opt/blackbox5/5-project-memory/blackbox5')
    operations_dir = bb5_dir / 'operations'

    # Try skill-registry.yaml first (unified registry)
    registry_file = operations_dir / 'skill-registry.yaml'
    if registry_file.exists():
        try:
            with open(registry_file, 'r') as f:
                registry_data = yaml.safe_load(f) or {}

            # Find and update task outcome
            task_outcomes = registry_data.get('task_outcomes', [])
            updated = False

            for outcome in task_outcomes:
                if outcome.get('task_id') == task_id:
                    outcome['duration_minutes'] = duration_minutes
                    # If end time wasn't set, use timing metadata
                    if not outcome.get('end_time'):
                        outcome['end_time'] = timing_metadata.get('end_time')
                    # Update skill_used if detected
                    if skill_used and (not outcome.get('skill_used') or outcome.get('skill_used') == 'null'):
                        outcome['skill_used'] = skill_used
                        print(f"[Task Time Tracker] Updated skill_used to: {skill_used}")
                    updated = True
                    print(f"[Task Time Tracker] Updated outcome in skill-registry.yaml")
                    break

            # If no existing outcome, create one
            if not updated:
                new_outcome = {
                    'task_id': task_id,
                    'timestamp': timing_metadata.get('start_time'),
                    'skill_used': skill_used,  # Detected skill or None
                    'task_type': 'unknown',
                    'duration_minutes': duration_minutes,
                    'outcome': 'success',  # Default assumption
                    'quality_rating': None,
                    'trigger_was_correct': None,
                    'would_use_again': None,
                    'notes': 'Time and skill tracked by task_time_tracker.py'
                }
                task_outcomes.append(new_outcome)
                registry_data['task_outcomes'] = task_outcomes
                updated = True
                print(f"[Task Time Tracker] Created new outcome in skill-registry.yaml")

            if updated:
                # Update metadata
                if 'metadata' in registry_data:
                    registry_data['metadata']['last_updated'] = datetime.now().isoformat() + 'Z'

                with open(registry_file, 'w') as f:
                    yaml.dump(registry_data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

        except Exception as e:
            print(f"[Task Time Tracker] Warning: Failed to update skill-registry.yaml: {e}")

    # Try skill-metrics.yaml if it exists (legacy)
    metrics_file = operations_dir / 'skill-metrics.yaml'
    if metrics_file.exists():
        try:
            with open(metrics_file, 'r') as f:
                metrics_data = yaml.safe_load(f) or {}

            if 'task_outcomes' in metrics_data:
                updated = False

                for outcome in metrics_data['task_outcomes']:
                    if outcome.get('task_id') == task_id:
                        outcome['duration_minutes'] = duration_minutes
                        if skill_used and (not outcome.get('skill_used') or outcome.get('skill_used') == 'null'):
                            outcome['skill_used'] = skill_used
                        updated = True
                        print(f"[Task Time Tracker] Updated outcome in skill-metrics.yaml")
                        break

                if updated:
                    with open(metrics_file, 'w') as f:
                        yaml.dump(metrics_data, f, default_flow_style=False, sort_keys=False)
        except Exception as e:
            print(f"[Task Time Tracker] Warning: Failed to update skill-metrics.yaml: {e}")


def main():
    """Main entry point."""
    # Determine action from arguments or environment
    import argparse

    parser = argparse.ArgumentParser(description='Task time tracking hook')
    parser.add_argument('--start', action='store_true', help='Record task start')
    parser.add_argument('--end', action='store_true', help='Record task end')
    parser.add_argument('--task-id', type=str, help='Task ID (auto-detected if not provided)')
    args = parser.parse_args()

    # Get task ID
    task_id = args.task_id or get_current_task_id()

    if not task_id:
        print("[Task Time Tracker] Error: Could not determine task ID")
        print("[Task Time Tracker] Either provide --task-id or run from within a task directory")
        sys.exit(1)

    # Execute action
    if args.start:
        record_task_start(task_id)
    elif args.end:
        record_task_end(task_id)
    else:
        # If no action specified, assume SessionStart (most common use case)
        record_task_start(task_id)

    return 0


if __name__ == '__main__':
    sys.exit(main())
