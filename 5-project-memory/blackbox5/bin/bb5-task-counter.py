#!/usr/bin/env python3
"""
BB5 Task Counter - Dynamically count tasks from filesystem

This script scans the tasks/active/ and tasks/completed/ directories
to derive accurate task counts instead of relying on hardcoded values.

Usage:
    bb5-task-counter.py [--tasks-dir PATH] [--output-format yaml|json|shell]
    bb5-task-counter.py validate [--tasks-dir PATH] [--queue-file PATH]
"""

import argparse
import json
import logging
import re
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

import yaml

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("bb5-task-counter")


class TaskCounter:
    """Counts tasks by scanning task directories."""

    def __init__(self, tasks_dir: Path):
        self.tasks_dir = tasks_dir
        self.active_dir = tasks_dir / "active"
        self.completed_dir = tasks_dir / "completed"
        self.cancelled_dir = tasks_dir / "cancelled"

    def count_tasks(self) -> dict[str, Any]:
        """Scan task directories and count tasks by status."""
        counts = {
            "generated_at": datetime.now().isoformat(),
            "tasks_dir": str(self.tasks_dir),
            "by_location": {},
            "by_status": {
                "pending": 0,
                "in_progress": 0,
                "completed": 0,
                "cancelled": 0,
                "unknown": 0,
            },
            "by_priority": defaultdict(int),
            "by_type": defaultdict(int),
            "total": 0,
            "details": [],
        }

        # Scan active directory
        if self.active_dir.exists():
            active_counts = self._scan_directory(self.active_dir, "active", counts)
            counts["by_location"]["active"] = active_counts

        # Scan completed directory
        if self.completed_dir.exists():
            completed_counts = self._scan_directory(self.completed_dir, "completed", counts)
            counts["by_location"]["completed"] = completed_counts

        # Scan cancelled directory
        if self.cancelled_dir.exists():
            cancelled_counts = self._scan_directory(self.cancelled_dir, "cancelled", counts)
            counts["by_location"]["cancelled"] = cancelled_counts

        # Calculate totals
        counts["total"] = sum(counts["by_status"].values())

        # Convert defaultdict to regular dict for serialization
        counts["by_priority"] = dict(counts["by_priority"])
        counts["by_type"] = dict(counts["by_type"])

        return counts

    def _scan_directory(self, directory: Path, location: str, counts: dict[str, Any]) -> dict[str, Any]:
        """Scan a task directory and extract task information."""
        result = {
            "total_dirs": 0,
            "with_task_md": 0,
            "task_dirs": [],
        }

        if not directory.exists():
            return result

        for task_dir in directory.iterdir():
            if not task_dir.is_dir():
                continue

            result["total_dirs"] += 1
            task_md = task_dir / "task.md"

            if task_md.exists():
                result["with_task_md"] += 1
                task_info = self._parse_task_file(task_md, task_dir.name)
                result["task_dirs"].append(task_info)

                # Aggregate counts
                status = task_info.get("status", "unknown")
                if status in counts["by_status"]:
                    counts["by_status"][status] += 1
                else:
                    counts["by_status"]["unknown"] += 1

                priority = task_info.get("priority", "unknown")
                if priority != "unknown":
                    counts["by_priority"][priority] += 1

                task_type = task_info.get("type", "unknown")
                if task_type != "unknown":
                    counts["by_type"][task_type] += 1

        return result

    def _parse_task_file(self, task_file: Path, task_dir_name: str) -> dict[str, Any]:
        """Parse a task.md file to extract status and metadata."""
        info = {
            "dir_name": task_dir_name,
            "task_id": task_dir_name,
            "status": "unknown",
            "priority": "unknown",
            "type": "unknown",
            "title": "",
        }

        try:
            content = task_file.read_text(encoding="utf-8")

            # Extract task ID from first line
            first_line = content.split("\n")[0] if content else ""
            task_id_match = re.search(r"(TASK-[A-Z]+-\d+|TASK-\d+|ACTION-[A-Z]+-[^\s]+)", first_line)
            if task_id_match:
                info["task_id"] = task_id_match.group(1)

            # Extract title
            title_match = re.search(r"^#\s+\S+:\s+(.+)$", content, re.MULTILINE)
            if title_match:
                info["title"] = title_match.group(1).strip()

            # Extract status
            status_match = re.search(r"\*\*Status:\*\*\s*(\w+)", content, re.IGNORECASE)
            if status_match:
                info["status"] = status_match.group(1).lower()

            # Extract priority
            priority_match = re.search(r"\*\*Priority:\*\*\s*(\w+)", content, re.IGNORECASE)
            if priority_match:
                info["priority"] = priority_match.group(1).upper()

            # Extract type (if present)
            type_match = re.search(r"\*\*Type:\*\*\s*(\w+)", content, re.IGNORECASE)
            if type_match:
                info["type"] = type_match.group(1).lower()

        except Exception as e:
            logger.warning(f"Failed to parse {task_file}: {e}")

        return info

    def update_queue_file(self, queue_file: Path, dry_run: bool = False) -> dict[str, Any]:
        """Update queue.yaml with dynamically calculated counts."""
        counts = self.count_tasks()

        if not queue_file.exists():
            logger.error(f"Queue file not found: {queue_file}")
            return counts

        try:
            with open(queue_file, "r", encoding="utf-8") as f:
                queue_data = yaml.safe_load(f) or {}
        except yaml.YAMLError as e:
            logger.error(f"Invalid YAML in queue file: {e}")
            return counts

        # Calculate derived counts
        active_tasks = counts["by_location"].get("active", {}).get("task_dirs", [])
        completed_tasks = counts["by_location"].get("completed", {}).get("task_dirs", [])

        pending = len([t for t in active_tasks if t["status"] == "pending"])
        in_progress = len([t for t in active_tasks if t["status"] == "in_progress"])
        completed = len(completed_tasks)

        # Update schema section
        if "schema" not in queue_data:
            queue_data["schema"] = {}

        queue_data["schema"]["generated"] = datetime.now().strftime("%Y-%m-%d")
        queue_data["schema"]["total_tasks"] = pending + in_progress + completed
        queue_data["schema"]["completed"] = completed
        queue_data["schema"]["in_progress"] = in_progress
        queue_data["schema"]["pending"] = pending

        # Update queue_metadata section
        if "queue_metadata" not in queue_data:
            queue_data["queue_metadata"] = {}

        queue_data["queue_metadata"]["total_tasks"] = pending + in_progress + completed
        queue_data["queue_metadata"]["by_status"] = {
            "completed": completed,
            "in_progress": in_progress,
            "pending": pending,
        }

        # Add derived_from_filesystem flag
        queue_data["queue_metadata"]["derived_from_filesystem"] = True
        queue_data["queue_metadata"]["last_counted_at"] = datetime.now().isoformat()

        if dry_run:
            logger.info("Dry run - would update queue.yaml with:")
            logger.info(f"  Total: {pending + in_progress + completed}")
            logger.info(f"  Pending: {pending}")
            logger.info(f"  In Progress: {in_progress}")
            logger.info(f"  Completed: {completed}")
        else:
            with open(queue_file, "w", encoding="utf-8") as f:
                yaml.dump(queue_data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
            logger.info(f"Updated {queue_file} with dynamic counts")

        return counts


def cmd_count(args: argparse.Namespace) -> int:
    """Count tasks and output results."""
    try:
        counter = TaskCounter(Path(args.tasks_dir))
        counts = counter.count_tasks()

        if args.output_format == "json":
            print(json.dumps(counts, indent=2))
        elif args.output_format == "yaml":
            print(yaml.dump(counts, default_flow_style=False, sort_keys=False, allow_unicode=True))
        elif args.output_format == "shell":
            print(f"BB5_TASKS_TOTAL={counts['total']}")
            print(f"BB5_TASKS_PENDING={counts['by_status']['pending']}")
            print(f"BB5_TASKS_IN_PROGRESS={counts['by_status']['in_progress']}")
            print(f"BB5_TASKS_COMPLETED={counts['by_status']['completed']}")
            print(f"BB5_TASKS_CANCELLED={counts['by_status']['cancelled']}")
        else:
            # Default table output
            print("Task Counts (from filesystem)")
            print("=" * 50)
            print(f"Total:        {counts['total']}")
            print(f"Pending:      {counts['by_status']['pending']}")
            print(f"In Progress:  {counts['by_status']['in_progress']}")
            print(f"Completed:    {counts['by_status']['completed']}")
            print(f"Cancelled:    {counts['by_status']['cancelled']}")
            print(f"Unknown:      {counts['by_status']['unknown']}")
            print("")
            print("By Location:")
            for location, data in counts["by_location"].items():
                task_dirs = data.get("task_dirs", [])
                print(f"  {location:12s}: {len(task_dirs)} tasks")

        return 0

    except Exception as e:
        logger.error(f"Failed to count tasks: {e}")
        return 1


def cmd_update(args: argparse.Namespace) -> int:
    """Update queue.yaml with dynamic counts."""
    try:
        counter = TaskCounter(Path(args.tasks_dir))
        counts = counter.update_queue_file(Path(args.queue_file), dry_run=args.dry_run)

        if not args.dry_run:
            print("Queue file updated successfully")
            print(f"  Total: {counts['total']}")
            print(f"  Pending: {counts['by_status']['pending']}")
            print(f"  In Progress: {counts['by_status']['in_progress']}")
            print(f"  Completed: {counts['by_status']['completed']}")

        return 0

    except Exception as e:
        logger.error(f"Failed to update queue: {e}")
        return 1


def cmd_validate(args: argparse.Namespace) -> int:
    """Validate queue.yaml counts match filesystem."""
    try:
        counter = TaskCounter(Path(args.tasks_dir))
        counts = counter.count_tasks()

        queue_file = Path(args.queue_file)
        if not queue_file.exists():
            logger.error(f"Queue file not found: {queue_file}")
            return 1

        with open(queue_file, "r", encoding="utf-8") as f:
            queue_data = yaml.safe_load(f) or {}

        # Get queue.yaml counts
        schema = queue_data.get("schema", {})
        queue_total = schema.get("total_tasks", 0)
        queue_completed = schema.get("completed", 0)
        queue_in_progress = schema.get("in_progress", 0)
        queue_pending = schema.get("pending", 0)

        # Get filesystem counts
        active_tasks = counts["by_location"].get("active", {}).get("task_dirs", [])
        completed_tasks = counts["by_location"].get("completed", {}).get("task_dirs", [])

        fs_pending = len([t for t in active_tasks if t["status"] == "pending"])
        fs_in_progress = len([t for t in active_tasks if t["status"] == "in_progress"])
        fs_completed = len(completed_tasks)
        fs_total = fs_pending + fs_in_progress + fs_completed

        # Validate
        errors = []
        if queue_total != fs_total:
            errors.append(f"Total mismatch: queue={queue_total}, filesystem={fs_total}")
        if queue_completed != fs_completed:
            errors.append(f"Completed mismatch: queue={queue_completed}, filesystem={fs_completed}")
        if queue_in_progress != fs_in_progress:
            errors.append(f"In Progress mismatch: queue={queue_in_progress}, filesystem={fs_in_progress}")
        if queue_pending != fs_pending:
            errors.append(f"Pending mismatch: queue={queue_pending}, filesystem={fs_pending}")

        if errors:
            print("VALIDATION FAILED:")
            for error in errors:
                print(f"  - {error}")
            return 1
        else:
            print("VALIDATION PASSED: Queue counts match filesystem")
            return 0

    except Exception as e:
        logger.error(f"Failed to validate: {e}")
        return 1


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="BB5 Task Counter - Dynamic task counting from filesystem",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  bb5-task-counter.py count
  bb5-task-counter.py count --output-format json
  bb5-task-counter.py update --queue-file .autonomous/agents/communications/queue.yaml
  bb5-task-counter.py validate
        """
    )

    parser.add_argument(
        "--tasks-dir",
        default="tasks",
        help="Path to tasks directory (default: tasks)"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # count command
    count_parser = subparsers.add_parser("count", help="Count tasks from filesystem")
    count_parser.add_argument(
        "--output-format",
        choices=["table", "json", "yaml", "shell"],
        default="table",
        help="Output format (default: table)"
    )
    count_parser.set_defaults(func=cmd_count)

    # update command
    update_parser = subparsers.add_parser("update", help="Update queue.yaml with dynamic counts")
    update_parser.add_argument(
        "--queue-file",
        default=".autonomous/agents/communications/queue.yaml",
        help="Path to queue.yaml file"
    )
    update_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be updated without making changes"
    )
    update_parser.set_defaults(func=cmd_update)

    # validate command
    validate_parser = subparsers.add_parser("validate", help="Validate queue.yaml matches filesystem")
    validate_parser.add_argument(
        "--queue-file",
        default=".autonomous/agents/communications/queue.yaml",
        help="Path to queue.yaml file"
    )
    validate_parser.set_defaults(func=cmd_validate)

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    if not args.command:
        parser.print_help()
        return 1

    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
