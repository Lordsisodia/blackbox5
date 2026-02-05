#!/usr/bin/env python3
"""
Skill Usage Logger for BlackBox5

Parses THOUGHTS.md files for "Skill Usage for This Task" section
and logs entries to skill-usage.yaml

Usage:
    python log-skill-usage.py --run-dir /path/to/run --task-id TASK-XXX
    python log-skill-usage.py --thoughts /path/to/THOUGHTS.md --task-id TASK-XXX
    python log-skill-usage.py --run-metadata /path/to/metadata.yaml

Integration Points:
    - Run completion workflow
    - Task completion hooks
    - Manual execution for backfill
"""

import argparse
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional
import yaml

# Constants
SKILL_USAGE_FILE = Path("/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/operations/skill-usage.yaml")


def parse_thoughts_for_skill_usage(thoughts_path: Path) -> Optional[dict]:
    """
    Parse THOUGHTS.md for Skill Usage section.

    Expected format:
    ## Skill Usage for This Task

    **Applicable skills:** [list or 'None']
    **Skill invoked:** [name or 'None']
    **Confidence:** [percentage or 'N/A']
    **Rationale:** [explanation]
    **Outcome:** [success|failure|partial] (optional)
    **Duration:** [minutes] (optional)
    """
    if not thoughts_path.exists():
        return None

    content = thoughts_path.read_text()

    # Find Skill Usage section
    skill_section_pattern = r'##\s*Skill Usage for This Task\s*\n(.*?)(?=##|\Z)'
    match = re.search(skill_section_pattern, content, re.DOTALL | re.IGNORECASE)

    if not match:
        return None

    section = match.group(1)

    # Parse fields
    result = {
        'applicable_skills': None,
        'skill_invoked': None,
        'confidence': None,
        'rationale': None,
        'outcome': None,
        'duration_minutes': None
    }

    # Extract applicable skills
    skills_match = re.search(r'\*\*Applicable skills:\*\*\s*(.+?)(?=\n\*\*|$)', section, re.DOTALL)
    if skills_match:
        skills_text = skills_match.group(1).strip()
        if skills_text.lower() not in ['none', 'n/a', '']:
            result['applicable_skills'] = [s.strip() for s in skills_text.split(',')]

    # Extract invoked skill
    invoked_match = re.search(r'\*\*Skill invoked:\*\*\s*(.+?)(?=\n\*\*|$)', section, re.DOTALL)
    if invoked_match:
        invoked_text = invoked_match.group(1).strip()
        if invoked_text.lower() not in ['none', 'n/a', '']:
            result['skill_invoked'] = invoked_text

    # Extract confidence
    confidence_match = re.search(r'\*\*Confidence:\*\*\s*(\d+)%?', section)
    if confidence_match:
        result['confidence'] = int(confidence_match.group(1))

    # Extract rationale
    rationale_match = re.search(r'\*\*Rationale:\*\*\s*(.+?)(?=\n\*\*|$)', section, re.DOTALL)
    if rationale_match:
        result['rationale'] = rationale_match.group(1).strip()

    # Extract outcome (optional)
    outcome_match = re.search(r'\*\*Outcome:\*\*\s*(success|failure|partial)', section, re.IGNORECASE)
    if outcome_match:
        result['outcome'] = outcome_match.group(1).lower()

    # Extract duration (optional)
    duration_match = re.search(r'\*\*Duration:\*\*\s*(\d+)\s*min', section, re.IGNORECASE)
    if duration_match:
        result['duration_minutes'] = int(duration_match.group(1))

    return result


def load_skill_usage_yaml() -> dict:
    """Load the skill-usage.yaml file."""
    if not SKILL_USAGE_FILE.exists():
        return {'usage_log': [], 'skills': [], 'metadata': {}}

    with open(SKILL_USAGE_FILE, 'r') as f:
        return yaml.safe_load(f) or {'usage_log': [], 'skills': [], 'metadata': {}}


def save_skill_usage_yaml(data: dict) -> None:
    """Save the skill-usage.yaml file."""
    # Ensure directory exists
    SKILL_USAGE_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(SKILL_USAGE_FILE, 'w') as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)


def update_skill_stats(data: dict, skill_name: str, outcome: str, duration_ms: Optional[int] = None) -> None:
    """Update aggregate stats for a skill."""
    if 'skills' not in data:
        data['skills'] = []

    for skill in data['skills']:
        if skill.get('name') == skill_name:
            # Update usage count
            skill['usage_count'] = skill.get('usage_count', 0) + 1
            skill['last_used'] = datetime.now(timezone.utc).isoformat()

            # Update first_used if not set
            if not skill.get('first_used'):
                skill['first_used'] = skill['last_used']

            # Update success/failure counts
            if outcome == 'success':
                skill['success_count'] = skill.get('success_count', 0) + 1
            elif outcome == 'failure':
                skill['failure_count'] = skill.get('failure_count', 0) + 1

            # Update average execution time
            if duration_ms:
                current_avg = skill.get('avg_execution_time_ms')
                current_count = skill.get('usage_count', 1)
                if current_avg:
                    skill['avg_execution_time_ms'] = (
                        (current_avg * (current_count - 1) + duration_ms) // current_count
                    )
                else:
                    skill['avg_execution_time_ms'] = duration_ms

            break


def log_skill_usage(
    task_id: str,
    skill_data: dict,
    run_id: Optional[str] = None,
    timestamp: Optional[str] = None
) -> bool:
    """
    Log skill usage entry to skill-usage.yaml.

    Returns True if logged successfully, False otherwise.
    """
    try:
        data = load_skill_usage_yaml()

        # Ensure usage_log exists
        if 'usage_log' not in data:
            data['usage_log'] = []

        # Create log entry
        entry = {
            'timestamp': timestamp or datetime.now(timezone.utc).isoformat(),
            'task_id': task_id,
            'skill': skill_data.get('skill_invoked'),
            'applicable_skills': skill_data.get('applicable_skills', []),
            'confidence': skill_data.get('confidence'),
            'trigger_reason': skill_data.get('rationale'),
            'execution_time_ms': skill_data.get('duration_minutes', 0) * 60000 if skill_data.get('duration_minutes') else None,
            'result': skill_data.get('outcome') or 'unknown',
            'notes': f"Logged from task {task_id}"
        }

        # Remove None values
        entry = {k: v for k, v in entry.items() if v is not None}

        # Add to log
        data['usage_log'].append(entry)

        # Update skill stats if a skill was invoked
        if skill_data.get('skill_invoked'):
            update_skill_stats(
                data,
                skill_data['skill_invoked'],
                skill_data.get('outcome', 'unknown'),
                entry.get('execution_time_ms')
            )

        # Update metadata
        if 'metadata' not in data:
            data['metadata'] = {}
        data['metadata']['last_updated'] = datetime.now(timezone.utc).isoformat()
        data['metadata']['total_invocations'] = len(data['usage_log'])

        # Save
        save_skill_usage_yaml(data)

        print(f"[OK] Logged skill usage for task {task_id}")
        if skill_data.get('skill_invoked'):
            print(f"     Skill: {skill_data['skill_invoked']}")
        if skill_data.get('confidence'):
            print(f"     Confidence: {skill_data['confidence']}%")

        return True

    except Exception as e:
        print(f"[ERROR] Failed to log skill usage: {e}", file=sys.stderr)
        return False


def find_thoughts_in_run(run_dir: Path) -> Optional[Path]:
    """Find THOUGHTS.md in a run directory."""
    # Check common locations
    possible_paths = [
        run_dir / "THOUGHTS.md",
        run_dir / "thoughts.md",
        run_dir / "task" / "THOUGHTS.md",
        run_dir / "task" / "thoughts.md",
    ]

    for path in possible_paths:
        if path.exists():
            return path

    # Search recursively
    for path in run_dir.rglob("THOUGHTS.md"):
        return path

    return None


def parse_run_metadata(metadata_path: Path) -> dict:
    """Parse run metadata.yaml for task and run info."""
    with open(metadata_path, 'r') as f:
        data = yaml.safe_load(f) or {}

    result = {
        'run_id': None,
        'task_id': None,
        'status': None
    }

    if 'run' in data:
        result['run_id'] = data['run'].get('id')
        result['task_id'] = data['run'].get('task_claimed')

    if 'results' in data:
        result['status'] = data['results'].get('status')

    return result


def main():
    parser = argparse.ArgumentParser(
        description="Log skill usage from THOUGHTS.md to skill-usage.yaml"
    )
    parser.add_argument(
        "--run-dir",
        type=Path,
        help="Path to run directory containing THOUGHTS.md"
    )
    parser.add_argument(
        "--thoughts",
        type=Path,
        help="Direct path to THOUGHTS.md file"
    )
    parser.add_argument(
        "--run-metadata",
        type=Path,
        help="Path to run metadata.yaml"
    )
    parser.add_argument(
        "--task-id",
        help="Task ID (required if not using --run-metadata)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Parse and display without logging"
    )

    args = parser.parse_args()

    # Determine THOUGHTS.md path
    thoughts_path = None
    task_id = args.task_id
    run_id = None

    if args.thoughts:
        thoughts_path = args.thoughts
    elif args.run_dir:
        thoughts_path = find_thoughts_in_run(args.run_dir)
        # Try to get task_id from run metadata
        metadata_path = args.run_dir / "metadata.yaml"
        if metadata_path.exists():
            meta = parse_run_metadata(metadata_path)
            task_id = task_id or meta.get('task_id')
            run_id = meta.get('run_id')
    elif args.run_metadata:
        meta = parse_run_metadata(args.run_metadata)
        task_id = task_id or meta.get('task_id')
        run_id = meta.get('run_id')
        # Find THOUGHTS.md in same directory
        thoughts_path = find_thoughts_in_run(args.run_metadata.parent)
    else:
        print("[ERROR] Must specify --run-dir, --thoughts, or --run-metadata", file=sys.stderr)
        sys.exit(1)

    if not thoughts_path or not thoughts_path.exists():
        print(f"[WARN] THOUGHTS.md not found")
        sys.exit(0)

    if not task_id:
        print("[ERROR] Task ID required (use --task-id or provide run metadata)", file=sys.stderr)
        sys.exit(1)

    # Parse skill usage
    skill_data = parse_thoughts_for_skill_usage(thoughts_path)

    if not skill_data:
        print(f"[INFO] No 'Skill Usage for This Task' section found in {thoughts_path}")
        sys.exit(0)

    # Display parsed data
    print(f"[INFO] Parsed skill usage from {thoughts_path}")
    print(f"       Task: {task_id}")
    if skill_data.get('skill_invoked'):
        print(f"       Skill invoked: {skill_data['skill_invoked']}")
    if skill_data.get('applicable_skills'):
        print(f"       Applicable skills: {', '.join(skill_data['applicable_skills'])}")
    if skill_data.get('confidence'):
        print(f"       Confidence: {skill_data['confidence']}%")

    if args.dry_run:
        print("[DRY RUN] Not logging to skill-usage.yaml")
        sys.exit(0)

    # Log to skill-usage.yaml
    success = log_skill_usage(task_id, skill_data, run_id)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
