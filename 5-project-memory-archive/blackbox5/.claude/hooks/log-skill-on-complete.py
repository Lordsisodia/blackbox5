#!/usr/bin/env python3
"""
Skill Usage Logging Hook - Task Completion Integration

Automatically logs skill usage when a task is completed.
Called by task completion workflow.

Usage:
    log-skill-on-complete.py --task-id TASK-XXX --run-dir /path/to/run
    log-skill-on-complete.py --run-dir /path/to/run  # Auto-detect from run metadata

Integration:
    - Called by task completion workflow
    - Parses THOUGHTS.md for "Skill Usage for This Task" section
    - Logs entries to operations/skill-usage.yaml
    - Updates skill aggregate statistics
"""

import argparse
import os
import sys
from pathlib import Path

# Add project root to path for imports
PROJECT_ROOT = Path("/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5")
sys.path.insert(0, str(PROJECT_ROOT / "bin"))

# Import the log-skill-usage functionality
import importlib.util
spec = importlib.util.spec_from_file_location(
    "log_skill_usage",
    PROJECT_ROOT / "bin" / "log-skill-usage.py"
)
log_skill_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(log_skill_module)

# Get functions from module
parse_thoughts_for_skill_usage = log_skill_module.parse_thoughts_for_skill_usage
log_skill_usage = log_skill_module.log_skill_usage
find_thoughts_in_run = log_skill_module.find_thoughts_in_run
parse_run_metadata = log_skill_module.parse_run_metadata


def log_skill_from_run(run_dir: Path, task_id: str = None) -> bool:
    """
    Log skill usage from a completed run.

    Args:
        run_dir: Path to run directory
        task_id: Optional task ID (auto-detected from metadata if not provided)

    Returns:
        True if skill usage was logged, False otherwise
    """
    print(f"[SKILL-LOG] Processing run: {run_dir.name}")

    if not run_dir.exists():
        print(f"[ERROR] Run directory not found: {run_dir}")
        return False

    # Auto-detect task ID and run info from metadata
    run_id = None
    metadata_path = run_dir / "metadata.yaml"
    if metadata_path.exists():
        meta = parse_run_metadata(metadata_path)
        task_id = task_id or meta.get('task_id')
        run_id = meta.get('run_id')

    if not task_id:
        print("[WARN] No task ID found, skipping skill logging")
        return False

    # Find THOUGHTS.md
    thoughts_path = find_thoughts_in_run(run_dir)

    if not thoughts_path or not thoughts_path.exists():
        print(f"[WARN] THOUGHTS.md not found in {run_dir}")
        return False

    # Parse skill usage
    skill_data = parse_thoughts_for_skill_usage(thoughts_path)

    if not skill_data:
        print(f"[INFO] No 'Skill Usage for This Task' section in {thoughts_path.name}")
        # Log a "no skill" entry to track that skill checking was skipped
        skill_data = {
            'skill_invoked': None,
            'applicable_skills': [],
            'confidence': None,
            'rationale': 'No skill usage section found in THOUGHTS.md',
            'outcome': 'unknown'
        }

    # Log to skill-usage.yaml
    success = log_skill_usage(task_id, skill_data, run_id)

    if success:
        print(f"[OK] Skill usage logged for {task_id}")
    else:
        print(f"[ERROR] Failed to log skill usage for {task_id}")

    return success


def main():
    parser = argparse.ArgumentParser(
        description="Log skill usage on task completion"
    )
    parser.add_argument(
        "--run-dir",
        required=True,
        type=Path,
        help="Path to run directory"
    )
    parser.add_argument(
        "--task-id",
        help="Task ID (auto-detected from metadata if not provided)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Parse and display without logging"
    )

    args = parser.parse_args()

    success = log_skill_from_run(args.run_dir, args.task_id)

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
