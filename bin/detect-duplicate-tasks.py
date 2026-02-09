#!/usr/bin/env python3
"""
detect-duplicate-tasks.py - Detect and prevent duplicate tasks in BlackBox5

This script compares task titles and objectives to identify potential duplicates.
It uses multiple similarity algorithms to catch duplicates even with wording variations.

Usage:
    detect-duplicate-tasks.py --check "New Task Title"    # Check for duplicates of new task
    detect-duplicate-tasks.py --scan                      # Scan all tasks for duplicates
    detect-duplicate-tasks.py --report                    # Generate duplicate report

Exit codes:
    0 - No duplicates found
    1 - Duplicates detected (when used with --check)
    2 - Error
"""

import os
import sys
import re
import argparse
import difflib
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Task:
    """Represents a task with its metadata."""
    task_id: str
    title: str
    objective: str
    status: str
    priority: str
    file_path: Path
    content: str

    def __hash__(self):
        return hash(self.task_id)


class DuplicateDetector:
    """Detects duplicate tasks using multiple similarity algorithms."""

    # Similarity thresholds
    TITLE_EXACT_MATCH = 1.0
    TITLE_HIGH_SIMILARITY = 0.85
    TITLE_MEDIUM_SIMILARITY = 0.70
    OBJECTIVE_SIMILARITY = 0.75
    CONTENT_SIMILARITY = 0.80

    def __init__(self, tasks_dir: Path):
        self.tasks_dir = tasks_dir
        self.tasks: List[Task] = []
        self.duplicates: List[Tuple[Task, Task, float, str]] = []

    def load_all_tasks(self) -> List[Task]:
        """Load all tasks from the tasks directory."""
        tasks = []

        # Load from active tasks
        active_dir = self.tasks_dir / "active"
        if active_dir.exists():
            tasks.extend(self._load_tasks_from_dir(active_dir))

        # Load from completed tasks
        completed_dir = self.tasks_dir / "completed"
        if completed_dir.exists():
            tasks.extend(self._load_tasks_from_dir(completed_dir))

        self.tasks = tasks
        return tasks

    def _load_tasks_from_dir(self, directory: Path) -> List[Task]:
        """Load tasks from a specific directory."""
        tasks = []

        for task_dir in directory.iterdir():
            if not task_dir.is_dir():
                continue

            task_file = task_dir / "task.md"
            if not task_file.exists():
                # Try to find any .md file
                md_files = list(task_dir.glob("*.md"))
                if md_files:
                    task_file = md_files[0]
                else:
                    continue

            try:
                task = self._parse_task_file(task_file, task_dir.name)
                if task:
                    tasks.append(task)
            except Exception as e:
                print(f"Warning: Could not parse {task_file}: {e}", file=sys.stderr)

        return tasks

    def _parse_task_file(self, file_path: Path, task_id: str) -> Optional[Task]:
        """Parse a task.md file and extract metadata."""
        content = file_path.read_text(encoding='utf-8')

        # Extract title (first # heading)
        title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        title = title_match.group(1) if title_match else task_id

        # Extract objective
        objective = self._extract_objective(content)

        # Extract status
        status_match = re.search(r'\*\*Status:\*\*\s*(\w+)', content, re.IGNORECASE)
        status = status_match.group(1).lower() if status_match else "unknown"

        # Extract priority
        priority_match = re.search(r'\*\*Priority:\*\*\s*(\w+)', content, re.IGNORECASE)
        priority = priority_match.group(1).lower() if priority_match else "unknown"

        return Task(
            task_id=task_id,
            title=title.strip(),
            objective=objective.strip(),
            status=status,
            priority=priority,
            file_path=file_path,
            content=content
        )

    def _extract_objective(self, content: str) -> str:
        """Extract the objective section from task content."""
        # Try to find Objective section
        objective_match = re.search(
            r'##?\s*(?:Objective|Description)\s*\n\s*\n?(.+?)(?:\n##|\n\n##|$)',
            content,
            re.DOTALL | re.IGNORECASE
        )

        if objective_match:
            objective = objective_match.group(1).strip()
            # Limit length
            if len(objective) > 500:
                objective = objective[:500] + "..."
            return objective

        # Fallback: use first paragraph after title
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if line.startswith('# ') and i + 1 < len(lines):
                # Skip empty lines and find first content
                for j in range(i + 1, min(i + 10, len(lines))):
                    if lines[j].strip() and not lines[j].startswith('**'):
                        return lines[j].strip()[:200]

        return ""

    def normalize_title(self, title: str) -> str:
        """Normalize a title for comparison."""
        # Remove task ID prefix
        title = re.sub(r'^TASK-[A-Z0-9-]+:\s*', '', title, flags=re.IGNORECASE)
        # Remove common prefixes
        title = re.sub(r'^(ACTION PLAN|PLAN|TASK):\s*', '', title, flags=re.IGNORECASE)
        # Convert to lowercase
        title = title.lower()
        # Remove special characters
        title = re.sub(r'[^\w\s]', ' ', title)
        # Normalize whitespace
        title = ' '.join(title.split())
        return title.strip()

    def calculate_similarity(self, str1: str, str2: str) -> float:
        """Calculate similarity ratio between two strings."""
        if not str1 or not str2:
            return 0.0

        # Use difflib's SequenceMatcher
        return difflib.SequenceMatcher(None, str1.lower(), str2.lower()).ratio()

    def are_duplicates(self, task1: Task, task2: Task) -> Tuple[bool, float, str]:
        """
        Check if two tasks are potential duplicates.
        Returns (is_duplicate, confidence_score, reason)
        """
        if task1.task_id == task2.task_id:
            return False, 0.0, ""

        norm_title1 = self.normalize_title(task1.title)
        norm_title2 = self.normalize_title(task2.title)

        # Check for exact title match (after normalization)
        if norm_title1 == norm_title2 and len(norm_title1) > 5:
            return True, 1.0, f"Exact title match: '{norm_title1}'"

        # Calculate title similarity
        title_sim = self.calculate_similarity(norm_title1, norm_title2)

        # High title similarity
        if title_sim >= self.TITLE_HIGH_SIMILARITY:
            return True, title_sim, f"High title similarity ({title_sim:.0%})"

        # Medium title similarity + objective similarity
        if title_sim >= self.TITLE_MEDIUM_SIMILARITY:
            obj_sim = self.calculate_similarity(task1.objective, task2.objective)
            if obj_sim >= self.OBJECTIVE_SIMILARITY:
                combined_score = (title_sim + obj_sim) / 2
                return True, combined_score, f"Title ({title_sim:.0%}) + Objective ({obj_sim:.0%}) similarity"

        # Check content similarity for shorter tasks
        if len(task1.content) < 2000 and len(task2.content) < 2000:
            content_sim = self.calculate_similarity(task1.content, task2.content)
            if content_sim >= self.CONTENT_SIMILARITY:
                return True, content_sim, f"High content similarity ({content_sim:.0%})"

        return False, 0.0, ""

    def find_duplicates(self) -> List[Tuple[Task, Task, float, str]]:
        """Find all duplicate task pairs."""
        self.duplicates = []
        checked_pairs = set()

        for i, task1 in enumerate(self.tasks):
            for task2 in self.tasks[i + 1:]:
                pair_key = tuple(sorted([task1.task_id, task2.task_id]))
                if pair_key in checked_pairs:
                    continue
                checked_pairs.add(pair_key)

                is_dup, score, reason = self.are_duplicates(task1, task2)
                if is_dup:
                    self.duplicates.append((task1, task2, score, reason))

        # Sort by confidence score (descending)
        self.duplicates.sort(key=lambda x: x[2], reverse=True)
        return self.duplicates

    def check_new_task(self, new_title: str, new_objective: str = "") -> List[Tuple[Task, float, str]]:
        """Check if a new task would be a duplicate of existing tasks."""
        matches = []

        norm_new_title = self.normalize_title(new_title)

        for task in self.tasks:
            norm_task_title = self.normalize_title(task.title)

            # Check exact match
            if norm_new_title == norm_task_title and len(norm_new_title) > 5:
                matches.append((task, 1.0, f"Exact title match"))
                continue

            # Check title similarity
            title_sim = self.calculate_similarity(norm_new_title, norm_task_title)

            if title_sim >= self.TITLE_HIGH_SIMILARITY:
                matches.append((task, title_sim, f"High title similarity ({title_sim:.0%})"))
                continue

            if title_sim >= self.TITLE_MEDIUM_SIMILARITY:
                obj_sim = self.calculate_similarity(new_objective, task.objective)
                if obj_sim >= self.OBJECTIVE_SIMILARITY:
                    combined = (title_sim + obj_sim) / 2
                    matches.append((task, combined, f"Title ({title_sim:.0%}) + Objective ({obj_sim:.0%})"))

        # Sort by confidence
        matches.sort(key=lambda x: x[1], reverse=True)
        return matches

    def generate_report(self) -> str:
        """Generate a detailed duplicate detection report."""
        lines = []
        lines.append("=" * 80)
        lines.append("BLACKBOX5 TASK DUPLICATE DETECTION REPORT")
        lines.append(f"Generated: {datetime.now().isoformat()}")
        lines.append("=" * 80)
        lines.append("")

        lines.append(f"Total tasks scanned: {len(self.tasks)}")
        lines.append(f"Potential duplicates found: {len(self.duplicates)}")
        lines.append("")

        if not self.duplicates:
            lines.append("✓ No duplicate tasks detected!")
        else:
            lines.append("-" * 80)
            lines.append("POTENTIAL DUPLICATES (sorted by confidence)")
            lines.append("-" * 80)
            lines.append("")

            for i, (task1, task2, score, reason) in enumerate(self.duplicates, 1):
                lines.append(f"{i}. Confidence: {score:.0%}")
                lines.append(f"   Reason: {reason}")
                lines.append("")
                lines.append(f"   Task A: {task1.task_id}")
                lines.append(f"   Title:  {task1.title}")
                lines.append(f"   Status: {task1.status} | Priority: {task1.priority}")
                lines.append(f"   Path:   {task1.file_path}")
                lines.append("")
                lines.append(f"   Task B: {task2.task_id}")
                lines.append(f"   Title:  {task2.title}")
                lines.append(f"   Status: {task2.status} | Priority: {task2.priority}")
                lines.append(f"   Path:   {task2.file_path}")
                lines.append("")

                # Suggest action
                if task1.status == "completed" and task2.status != "completed":
                    lines.append(f"   → Suggestion: Task A is completed. Consider closing Task B as duplicate.")
                elif task2.status == "completed" and task1.status != "completed":
                    lines.append(f"   → Suggestion: Task B is completed. Consider closing Task A as duplicate.")
                else:
                    lines.append(f"   → Suggestion: Review and merge or close one of these tasks.")

                lines.append("")
                lines.append("-" * 80)
                lines.append("")

        return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Detect duplicate tasks in BlackBox5",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    %(prog)s --scan                           # Scan all tasks for duplicates
    %(prog)s --check "Fix authentication bug" # Check if task already exists
    %(prog)s --report                         # Generate full duplicate report
    %(prog)s --report --output duplicates.txt # Save report to file
        """
    )

    parser.add_argument(
        "--scan",
        action="store_true",
        help="Scan all tasks for duplicates"
    )

    parser.add_argument(
        "--check",
        metavar="TITLE",
        help="Check if a new task title would be a duplicate"
    )

    parser.add_argument(
        "--objective",
        metavar="TEXT",
        default="",
        help="Objective/description for the new task (used with --check)"
    )

    parser.add_argument(
        "--report",
        action="store_true",
        help="Generate a detailed duplicate detection report"
    )

    parser.add_argument(
        "--output",
        "-o",
        metavar="FILE",
        help="Save report to file instead of stdout"
    )

    parser.add_argument(
        "--tasks-dir",
        metavar="PATH",
        default=os.environ.get("BB5_TASKS_DIR", "~/.blackbox5/5-project-memory/blackbox5/tasks"),
        help="Path to tasks directory (default: ~/.blackbox5/5-project-memory/blackbox5/tasks)"
    )

    parser.add_argument(
        "--threshold",
        type=float,
        default=0.70,
        help="Similarity threshold for duplicates (default: 0.70)"
    )

    args = parser.parse_args()

    # Expand path
    tasks_dir = Path(args.tasks_dir).expanduser()

    if not tasks_dir.exists():
        print(f"Error: Tasks directory not found: {tasks_dir}", file=sys.stderr)
        sys.exit(2)

    # Initialize detector
    detector = DuplicateDetector(tasks_dir)
    detector.TITLE_MEDIUM_SIMILARITY = args.threshold

    # Load all tasks
    print(f"Loading tasks from {tasks_dir}...", file=sys.stderr)
    detector.load_all_tasks()
    print(f"Loaded {len(detector.tasks)} tasks", file=sys.stderr)

    if args.check:
        # Check for duplicates of new task
        matches = detector.check_new_task(args.check, args.objective)

        if matches:
            print(f"\n⚠ WARNING: Potential duplicates found for '{args.check}':\n")
            for task, score, reason in matches[:5]:  # Show top 5
                print(f"  • {task.task_id} (confidence: {score:.0%})")
                print(f"    Title: {task.title}")
                print(f"    Status: {task.status}")
                print(f"    Reason: {reason}")
                print()
            sys.exit(1)
        else:
            print(f"\n✓ No duplicates found for '{args.check}'")
            sys.exit(0)

    elif args.scan or args.report:
        # Find all duplicates
        duplicates = detector.find_duplicates()

        if args.report:
            report = detector.generate_report()
            if args.output:
                Path(args.output).write_text(report)
                print(f"Report saved to {args.output}")
            else:
                print(report)
        else:
            # Simple scan output
            if duplicates:
                print(f"\nFound {len(duplicates)} potential duplicate(s):")
                for task1, task2, score, reason in duplicates:
                    print(f"\n  • {task1.task_id} ↔ {task2.task_id}")
                    print(f"    Confidence: {score:.0%}")
                    print(f"    Reason: {reason}")
                sys.exit(1)
            else:
                print("\n✓ No duplicates found")
                sys.exit(0)

    else:
        parser.print_help()
        sys.exit(0)


if __name__ == "__main__":
    main()
