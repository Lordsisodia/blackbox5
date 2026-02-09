#!/usr/bin/env python3
"""
BB5 Task Scanner Module

Scans task directories, parses task.md files, and updates the task queue.
Can be run standalone or imported as a module.
"""

import argparse
import logging
import os
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

import yaml

# Default paths
DEFAULT_TASKS_DIR = Path("/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/tasks/active")
DEFAULT_QUEUE_PATH = Path("/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/.autonomous/agents/communications/queue.yaml")

# Priority weights for scoring
PRIORITY_WEIGHTS = {
    "critical": 4.0,
    "high": 3.0,
    "medium": 2.0,
    "low": 1.0,
}

# Type multipliers for scoring
TYPE_MULTIPLIERS = {
    "implement": 1.2,
    "fix": 1.3,
    "refactor": 1.1,
    "analyze": 1.0,
    "organize": 0.9,
    "research": 1.0,
}


@dataclass
class Task:
    """Represents a parsed task."""
    id: str
    title: str
    status: str = "pending"
    priority: str = "medium"
    type: str = "implement"
    estimated_minutes: int = 30
    estimated_lines: Optional[int] = None
    success_criteria: list[str] = field(default_factory=list)
    files_to_modify: list[str] = field(default_factory=list)
    files_to_create: list[str] = field(default_factory=list)
    context: str = ""
    approach: str = ""
    created: Optional[str] = None
    completed: Optional[str] = None
    priority_score: float = 0.0
    source_path: Optional[Path] = None

    def calculate_priority_score(self, confidence: float = 1.0) -> float:
        """
        Calculate priority score using formula: (impact / effort) * confidence

        Impact is derived from priority level and type.
        Effort is derived from estimated minutes.
        """
        # Get priority weight (default to medium)
        priority_weight = PRIORITY_WEIGHTS.get(self.priority.lower(), 2.0)

        # Get type multiplier
        type_multiplier = TYPE_MULTIPLIERS.get(self.type.lower(), 1.0)

        # Calculate impact (0-10 scale)
        impact = min(10.0, priority_weight * type_multiplier * 2.5)

        # Calculate effort (normalize minutes to 0.5-5.0 scale)
        effort = max(0.5, min(5.0, self.estimated_minutes / 60))

        # Calculate score
        self.priority_score = round((impact / effort) * confidence, 2)
        return self.priority_score

    def to_queue_entry(self) -> dict[str, Any]:
        """Convert task to queue.yaml entry format."""
        return {
            "id": self.id,
            "type": self.type,
            "status": self.status,
            "priority": self.priority.upper(),
            "priority_score": self.priority_score,
            "title": self.title,
            "estimated_minutes": self.estimated_minutes,
            "roi": {
                "impact": self.priority_score,
                "effort": self.estimated_minutes,
                "confidence": 1.0,
            },
            "blockedBy": [],
            "blocks": [],
            "resource_type": "cpu_bound",
            "parallel_group": "wave_1",
        }


def parse_frontmatter(content: str) -> tuple[dict[str, Any], str]:
    """
    Parse YAML frontmatter from markdown content.

    Returns tuple of (frontmatter_dict, remaining_content).
    """
    frontmatter = {}
    body = content

    # Check for YAML frontmatter (--- at start)
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            try:
                frontmatter = yaml.safe_load(parts[1]) or {}
                body = parts[2].strip()
            except yaml.YAMLError as e:
                logging.warning(f"Failed to parse frontmatter: {e}")
                body = content

    return frontmatter, body


def extract_task_metadata(content: str) -> dict[str, Any]:
    """
    Extract metadata from task.md content.

    Parses the header and various sections to build a complete metadata dict.
    """
    metadata = {
        "status": "pending",
        "priority": "medium",
        "type": "implement",
        "estimated_minutes": 30,
        "success_criteria": [],
        "files_to_modify": [],
        "files_to_create": [],
        "context": "",
        "approach": "",
    }

    # Extract title and ID from first header
    title_match = re.search(r"^#\s+([^\n]+)", content, re.MULTILINE)
    if title_match:
        full_title = title_match.group(1).strip()
        metadata["title"] = full_title
        # Try to extract ID from title (e.g., "TASK-001: Title")
        id_match = re.match(r"([A-Z]+-\d+(?:-[\w-]+)?)", full_title)
        if id_match:
            metadata["id"] = id_match.group(1)

    # Extract status
    status_match = re.search(r"\*\*Status:\*\*\s*(\w+)", content, re.IGNORECASE)
    if status_match:
        metadata["status"] = status_match.group(1).lower()

    # Extract priority
    priority_match = re.search(r"\*\*Priority:\*\*\s*(\w+)", content, re.IGNORECASE)
    if priority_match:
        metadata["priority"] = priority_match.group(1).lower()

    # Extract type/category
    type_match = re.search(r"\*\*(?:Type|Category):\*\*\s*(\w+)", content, re.IGNORECASE)
    if type_match:
        metadata["type"] = type_match.group(1).lower()

    # Extract estimated effort (minutes)
    effort_match = re.search(r"\*\*Estimated Effort:\*\*\s*(\d+)\s*minutes", content, re.IGNORECASE)
    if effort_match:
        metadata["estimated_minutes"] = int(effort_match.group(1))
    else:
        # Try to parse "30-45 minutes" format
        range_match = re.search(r"\*\*Estimated Effort:\*\*\s*(\d+)-\d+\s*minutes", content, re.IGNORECASE)
        if range_match:
            metadata["estimated_minutes"] = int(range_match.group(1))
        else:
            # Try to parse "4 hours" format
            hours_match = re.search(r"\*\*Estimated Effort:\*\*\s*(\d+(?:\.\d+)?)\s*hours?", content, re.IGNORECASE)
            if hours_match:
                metadata["estimated_minutes"] = int(float(hours_match.group(1)) * 60)
            else:
                # Try to parse "1-2 hours" format
                hours_range_match = re.search(r"\*\*Estimated Effort:\*\*\s*(\d+(?:\.\d+)?)-\d+(?:\.\d+)?\s*hours?", content, re.IGNORECASE)
                if hours_range_match:
                    metadata["estimated_minutes"] = int(float(hours_range_match.group(1)) * 60)

    # Extract success criteria (also handles "Acceptance Criteria")
    success_section = re.search(
        r"##\s+(?:Success|Acceptance) Criteria\s*\n(.*?)(?=##|$)",
        content,
        re.DOTALL | re.IGNORECASE
    )
    if success_section:
        criteria_text = success_section.group(1)
        # Find checkbox items
        criteria = re.findall(r"- \[([ xX])\]\s*(.+)", criteria_text)
        metadata["success_criteria"] = [c[1].strip() for c in criteria]

    # Extract files to modify/create
    files_section = re.search(
        r"##\s+Files to Modify\s*\n(.*?)(?=##|$)",
        content,
        re.DOTALL | re.IGNORECASE
    )
    if files_section:
        files_text = files_section.group(1)
        # Parse file entries
        for line in files_text.split("\n"):
            line = line.strip()
            if line.startswith("- Create:") or line.startswith("- Create :"):
                file_path = line.split(":", 1)[1].strip()
                metadata["files_to_create"].append(file_path)
            elif line.startswith("- Modify:") or line.startswith("- Modify :"):
                file_path = line.split(":", 1)[1].strip()
                metadata["files_to_modify"].append(file_path)
            elif line.startswith("- Read:") or line.startswith("- Read :"):
                # Read-only files, not modifying
                pass
            elif line.startswith("-") and ":" in line:
                # Generic file entry
                file_path = line.split(":", 1)[1].strip()
                metadata["files_to_modify"].append(file_path)

    # Extract context
    context_section = re.search(
        r"##\s+Context\s*\n(.*?)(?=##|$)",
        content,
        re.DOTALL | re.IGNORECASE
    )
    if context_section:
        metadata["context"] = context_section.group(1).strip()

    # Extract approach
    approach_section = re.search(
        r"##\s+Approach\s*\n(.*?)(?=##|$)",
        content,
        re.DOTALL | re.IGNORECASE
    )
    if approach_section:
        metadata["approach"] = approach_section.group(1).strip()

    # Extract dates
    created_match = re.search(r"\*\*Created:\*\*\s*([\d\-T:Z]+)", content)
    if created_match:
        metadata["created"] = created_match.group(1)

    completed_match = re.search(r"\*\*Completed:\*\*\s*([\d\-T:Z]+)", content)
    if completed_match:
        metadata["completed"] = completed_match.group(1)

    return metadata


def parse_task_file(task_path: Path) -> Optional[Task]:
    """
    Parse a single task.md file and return a Task object.

    Args:
        task_path: Path to the task.md file

    Returns:
        Task object or None if parsing fails
    """
    try:
        content = task_path.read_text(encoding="utf-8")
    except Exception as e:
        logging.error(f"Failed to read {task_path}: {e}")
        return None

    # Extract metadata
    metadata = extract_task_metadata(content)

    # Ensure we have an ID
    if "id" not in metadata:
        # Use directory name as ID
        metadata["id"] = task_path.parent.name

    # Create Task object
    task = Task(
        id=metadata.get("id", "UNKNOWN"),
        title=metadata.get("title", "Untitled Task"),
        status=metadata.get("status", "pending"),
        priority=metadata.get("priority", "medium"),
        type=metadata.get("type", "implement"),
        estimated_minutes=metadata.get("estimated_minutes", 30),
        success_criteria=metadata.get("success_criteria", []),
        files_to_modify=metadata.get("files_to_modify", []),
        files_to_create=metadata.get("files_to_create", []),
        context=metadata.get("context", ""),
        approach=metadata.get("approach", ""),
        created=metadata.get("created"),
        completed=metadata.get("completed"),
        source_path=task_path,
    )

    # Calculate priority score
    task.calculate_priority_score()

    return task


def scan_tasks_directory(tasks_dir: Path) -> list[Task]:
    """
    Scan the tasks directory for all task.md files.

    Args:
        tasks_dir: Path to the tasks/active directory

    Returns:
        List of parsed Task objects
    """
    tasks = []

    if not tasks_dir.exists():
        logging.error(f"Tasks directory does not exist: {tasks_dir}")
        return tasks

    # Find all task.md files
    for task_file in tasks_dir.rglob("task.md"):
        task = parse_task_file(task_file)
        if task:
            tasks.append(task)
            logging.debug(f"Parsed task: {task.id} - {task.title}")

    # Sort by priority score (descending)
    tasks.sort(key=lambda t: t.priority_score, reverse=True)

    return tasks


def load_queue(queue_path: Path) -> dict[str, Any]:
    """
    Load the existing queue.yaml file.

    Args:
        queue_path: Path to queue.yaml

    Returns:
        Queue dictionary
    """
    if not queue_path.exists():
        logging.warning(f"Queue file does not exist: {queue_path}")
        return {"tasks": []}

    try:
        with open(queue_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {"tasks": []}
    except Exception as e:
        logging.error(f"Failed to load queue: {e}")
        return {"tasks": []}


def save_queue(queue_path: Path, queue: dict[str, Any]) -> bool:
    """
    Save the queue to queue.yaml.

    Args:
        queue_path: Path to queue.yaml
        queue: Queue dictionary

    Returns:
        True if successful
    """
    try:
        # Ensure parent directory exists
        queue_path.parent.mkdir(parents=True, exist_ok=True)

        with open(queue_path, "w", encoding="utf-8") as f:
            yaml.dump(queue, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
        return True
    except Exception as e:
        logging.error(f"Failed to save queue: {e}")
        return False


def get_existing_task_ids(queue: dict[str, Any]) -> set[str]:
    """Get set of task IDs already in queue."""
    tasks = queue.get("tasks", [])
    return {t.get("id") for t in tasks if t.get("id")}


def update_queue_with_tasks(
    queue: dict[str, Any],
    tasks: list[Task],
    skip_completed: bool = True
) -> tuple[int, int]:
    """
    Update queue with new tasks.

    Args:
        queue: Existing queue dictionary
        tasks: List of new tasks to add
        skip_completed: Whether to skip completed tasks

    Returns:
        Tuple of (added_count, skipped_count)
    """
    existing_ids = get_existing_task_ids(queue)
    added = 0
    skipped = 0

    for task in tasks:
        # Skip if already in queue
        if task.id in existing_ids:
            logging.debug(f"Skipping {task.id}: already in queue")
            skipped += 1
            continue

        # Skip completed tasks if requested
        if skip_completed and task.status == "completed":
            logging.debug(f"Skipping {task.id}: completed")
            skipped += 1
            continue

        # Add to queue
        queue["tasks"].append(task.to_queue_entry())
        existing_ids.add(task.id)
        added += 1
        logging.info(f"Added task to queue: {task.id} - {task.title}")

    return added, skipped


def scan_and_update(
    tasks_dir: Optional[Path] = None,
    queue_path: Optional[Path] = None,
    dry_run: bool = False,
    skip_completed: bool = True
) -> dict[str, Any]:
    """
    Main function to scan tasks and update queue.

    Args:
        tasks_dir: Path to tasks directory (default: DEFAULT_TASKS_DIR)
        queue_path: Path to queue.yaml (default: DEFAULT_QUEUE_PATH)
        dry_run: If True, don't actually update queue
        skip_completed: If True, skip completed tasks

    Returns:
        Dictionary with scan results
    """
    tasks_dir = tasks_dir or DEFAULT_TASKS_DIR
    queue_path = queue_path or DEFAULT_QUEUE_PATH

    # Scan for tasks
    logging.info(f"Scanning tasks directory: {tasks_dir}")
    tasks = scan_tasks_directory(tasks_dir)
    logging.info(f"Found {len(tasks)} tasks")

    # Load existing queue
    queue = load_queue(queue_path)

    # Update queue
    added, skipped = update_queue_with_tasks(queue, tasks, skip_completed)

    # Save if not dry run
    if not dry_run:
        if save_queue(queue_path, queue):
            logging.info(f"Queue saved to {queue_path}")
        else:
            logging.error("Failed to save queue")
    else:
        logging.info("Dry run - queue not saved")

    return {
        "tasks_found": len(tasks),
        "tasks_added": added,
        "tasks_skipped": skipped,
        "queue_path": str(queue_path),
        "dry_run": dry_run,
    }


def main():
    """Main entry point for CLI usage."""
    parser = argparse.ArgumentParser(
        description="BB5 Task Scanner - Scan tasks and update queue",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                          # Scan and update queue
  %(prog)s --dry-run                # Preview changes without updating
  %(prog)s --verbose                # Show detailed output
  %(prog)s --include-completed      # Include completed tasks
        """
    )

    parser.add_argument(
        "--tasks-dir",
        type=Path,
        default=DEFAULT_TASKS_DIR,
        help=f"Path to tasks directory (default: {DEFAULT_TASKS_DIR})"
    )

    parser.add_argument(
        "--queue-path",
        type=Path,
        default=DEFAULT_QUEUE_PATH,
        help=f"Path to queue.yaml (default: {DEFAULT_QUEUE_PATH})"
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without updating queue"
    )

    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose logging"
    )

    parser.add_argument(
        "--include-completed",
        action="store_true",
        help="Include completed tasks in queue"
    )

    args = parser.parse_args()

    # Setup logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format="%(levelname)s: %(message)s"
    )

    # Run scan
    results = scan_and_update(
        tasks_dir=args.tasks_dir,
        queue_path=args.queue_path,
        dry_run=args.dry_run,
        skip_completed=not args.include_completed
    )

    # Print summary
    print("\n" + "=" * 50)
    print("SCAN SUMMARY")
    print("=" * 50)
    print(f"Tasks found:    {results['tasks_found']}")
    print(f"Tasks added:    {results['tasks_added']}")
    print(f"Tasks skipped:  {results['tasks_skipped']}")
    print(f"Queue path:     {results['queue_path']}")
    print(f"Dry run:        {results['dry_run']}")

    return 0 if not args.dry_run or results['tasks_added'] == 0 else 0


if __name__ == "__main__":
    sys.exit(main())
