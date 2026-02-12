#!/usr/bin/env python3
"""
RALF Task Selection Script

Programmatically selects the highest priority task from the active task list.
Supports priority ordering and task claiming to prevent duplicate execution.

Usage:
    python3 ralf-task-select.py                    # Select highest priority task
    python3 ralf-task-select.py --claim             # Select and claim task
    python3 ralf-task-select.py --list              # List all tasks with scores
    python3 ralf-task-select.py --help              # Show help

Priority Order: critical > HIGH > MEDIUM > LOW
"""

import os
import sys
import re
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# BlackBox5 paths
BLACKBOX5_HOME = os.environ.get("BLACKBOX5_HOME", "/opt/blackbox5")
TASKS_ACTIVE_DIR = Path(BLACKBOX5_HOME) / "5-project-memory/blackbox5/tasks/active"
TASKS_WORKING_DIR = Path(BLACKBOX5_HOME) / "5-project-memory/blackbox5/tasks/working"

# Priority weights (higher = more important)
PRIORITY_WEIGHTS = {
    "critical": 100,
    "HIGH": 90,
    "high": 90,
    "MEDIUM": 50,
    "medium": 50,
    "LOW": 10,
    "low": 10
}


def parse_task_file(task_path: Path) -> Optional[Dict]:
    """
    Parse a task.md file and extract relevant information.

    Returns:
        Dict with task metadata or None if file is invalid
    """
    if not task_path.exists() or not task_path.is_file():
        return None

    task_id = task_path.parent.name
    content = task_path.read_text()

    # Extract metadata using regex
    status_match = re.search(r'\*\*Status:\*\*\s*(\w+)', content)
    priority_match = re.search(r'\*\*Priority:\*\*\s*(\w+)', content)
    created_match = re.search(r'\*\*Created:\*\*\s*([^\n]+)', content)

    # Skip completed tasks
    if status_match and status_match.group(1).lower() in ["completed", "done"]:
        return None

    status = status_match.group(1) if status_match else "pending"
    priority_str = priority_match.group(1) if priority_match else "MEDIUM"
    created = created_match.group(1) if created_match else ""

    # Calculate priority score
    priority_score = PRIORITY_WEIGHTS.get(priority_str, 50)

    return {
        "task_id": task_id,
        "path": task_path.parent,
        "status": status,
        "priority": priority_str,
        "priority_score": priority_score,
        "created": created
    }


def load_all_tasks() -> List[Dict]:
    """
    Load all active tasks from the tasks/active/ directory.

    Returns:
        List of task dictionaries sorted by priority (highest first)
    """
    tasks = []

    if not TASKS_ACTIVE_DIR.exists():
        print(f"Error: Task directory does not exist: {TASKS_ACTIVE_DIR}", file=sys.stderr)
        return tasks

    # Scan for task.md files
    for task_dir in TASKS_ACTIVE_DIR.iterdir():
        if task_dir.is_dir():
            task_file = task_dir / "task.md"
            if task_file.exists():
                task = parse_task_file(task_file)
                if task:
                    tasks.append(task)

    # Sort by priority score (descending)
    tasks.sort(key=lambda x: x["priority_score"], reverse=True)

    return tasks


def select_task(claim: bool = False) -> Optional[Dict]:
    """
    Select the highest priority pending task.

    Args:
        claim: If True, move task to working/ to prevent duplicate execution

    Returns:
        Selected task dict or None if no tasks available
    """
    tasks = load_all_tasks()

    if not tasks:
        return None

    selected = tasks[0]

    if claim:
        # Move task to working/ directory
        working_path = TASKS_WORKING_DIR / selected["task_id"]

        if working_path.exists():
            print(f"Warning: Task {selected['task_id']} already in working/", file=sys.stderr)
        else:
            # Create working directory and move task files
            working_path.mkdir(parents=True, exist_ok=True)

            # Copy all files from active task
            for file in selected["path"].iterdir():
                if file.is_file():
                    import shutil
                    shutil.copy2(file, working_path / file.name)

            # Mark as claimed in task.md
            task_file = working_path / "task.md"
            if task_file.exists():
                content = task_file.read_text()
                content = re.sub(
                    r'\*\*Status:\*\*\s*\w+',
                    '**Status:** claimed',
                    content
                )
                content += f"\n\n**Claimed:** {datetime.now().isoformat()}\n"
                task_file.write_text(content)

            print(f"Claimed task: {selected['task_id']} → {working_path}", file=sys.stderr)
            selected["path"] = working_path

    return selected


def list_tasks(tasks: List[Dict], limit: int = 20):
    """
    Print a formatted list of tasks with their priority scores.

    Args:
        tasks: List of task dictionaries
        limit: Maximum number of tasks to display
    """
    if not tasks:
        print("No active tasks found.")
        return

    print(f"{'Task ID':<30} {'Priority':<10} {'Score':<5} {'Status':<10} {'Created'}")
    print("-" * 100)

    for task in tasks[:limit]:
        print(f"{task['task_id']:<30} {task['priority']:<10} {task['priority_score']:<5} {task['status']:<10} {task['created'][:19]}")

    if len(tasks) > limit:
        print(f"\n... and {len(tasks) - limit} more tasks")


def main():
    parser = argparse.ArgumentParser(
        description="Select the highest priority BlackBox5 task",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 ralf-task-select.py              # Select highest priority task
  python3 ralf-task-select.py --claim     # Select and claim task (move to working/)
  python3 ralf-task-select.py --list      # List all tasks with priority scores
  python3 ralf-task-select.py --list -n 50 # Show 50 tasks

Priority Order: critical (100) > HIGH (90) > MEDIUM (50) > LOW (10)
        """
    )

    parser.add_argument(
        "--claim",
        action="store_true",
        help="Claim the selected task (move to tasks/working/)"
    )
    parser.add_argument(
        "--list",
        "-l",
        action="store_true",
        help="List all tasks with priority scores"
    )
    parser.add_argument(
        "--number",
        "-n",
        type=int,
        default=20,
        help="Number of tasks to list (default: 20)"
    )

    args = parser.parse_args()

    if args.list:
        tasks = load_all_tasks()
        list_tasks(tasks, args.number)
        return 0

    # Select task
    task = select_task(claim=args.claim)

    if not task:
        print("No pending tasks found.", file=sys.stderr)
        return 1

    # Output selected task in a machine-readable format
    # Format: TASK_ID|PATH|PRIORITY|STATUS
    print(f"{task['task_id']}|{task['path']}|{task['priority']}|{task['status']}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
