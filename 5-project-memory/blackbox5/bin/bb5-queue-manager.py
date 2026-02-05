#!/usr/bin/env python3
"""
BB5 Queue Manager - Task Queue Management and Prioritization

This script manages the BlackBox5 task queue, including:
- Loading queue from queue.yaml
- Calculating priorities using ROI formula: (impact / effort) * confidence
- Sorting tasks by priority score
- Resolving dependencies using topological sort
- Detecting circular dependencies
- Exporting execution-ready state

Usage:
    bb5-queue-manager.py load [--queue-file PATH]
    bb5-queue-manager.py prioritize [--queue-file PATH] [--output PATH]
    bb5-queue-manager.py resolve [--queue-file PATH] [--output PATH]
    bb5-queue-manager.py export [--queue-file PATH] [--output PATH]
    bb5-queue-manager.py status [--queue-file PATH]
"""

import argparse
import logging
import sys
from collections import defaultdict, deque
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Optional

import yaml

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("bb5-queue-manager")


class TaskStatus(Enum):
    """Task status enumeration."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    BLOCKED = "blocked"
    CANCELLED = "cancelled"


class Priority(Enum):
    """Priority level enumeration."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class Task:
    """Represents a task in the queue."""
    task_id: str
    title: str
    priority: Priority
    priority_score: float
    estimated_minutes: int
    status: TaskStatus
    created_at: datetime
    feature_id: Optional[str] = None
    estimated_lines: Optional[int] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    claimed_at: Optional[datetime] = None
    claimed_by: Optional[str] = None
    notes: Optional[str] = None
    blocked_by: list[str] = field(default_factory=list)
    resources: list[str] = field(default_factory=list)
    impact: float = 5.0  # Default impact score (1-10)
    effort: float = 5.0  # Default effort score (1-10)
    confidence: float = 0.8  # Default confidence (0-1)

    def calculate_priority_score(self) -> float:
        """Calculate priority score using ROI formula: (impact / effort) * confidence."""
        if self.effort <= 0:
            logger.warning(f"Task {self.task_id} has invalid effort value: {self.effort}")
            return 0.0
        return (self.impact / self.effort) * self.confidence

    def to_dict(self) -> dict[str, Any]:
        """Convert task to dictionary."""
        result = {
            "task_id": self.task_id,
            "title": self.title,
            "priority": self.priority.value,
            "priority_score": round(self.priority_score, 2),
            "estimated_minutes": self.estimated_minutes,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "impact": self.impact,
            "effort": self.effort,
            "confidence": self.confidence,
        }

        if self.feature_id:
            result["feature_id"] = self.feature_id
        if self.estimated_lines:
            result["estimated_lines"] = self.estimated_lines
        if self.started_at:
            result["started_at"] = self.started_at.isoformat()
        if self.completed_at:
            result["completed_at"] = self.completed_at.isoformat()
        if self.claimed_at:
            result["claimed_at"] = self.claimed_at.isoformat()
        if self.claimed_by:
            result["claimed_by"] = self.claimed_by
        if self.notes:
            result["notes"] = self.notes
        if self.blocked_by:
            result["blocked_by"] = self.blocked_by
        if self.resources:
            result["resources"] = self.resources

        return result

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Task":
        """Create task from dictionary."""
        # Parse datetime fields
        created_at = cls._parse_datetime(data["created_at"])
        started_at = cls._parse_datetime(data.get("started_at"))
        completed_at = cls._parse_datetime(data.get("completed_at"))
        claimed_at = cls._parse_datetime(data.get("claimed_at"))

        # Parse priority and status
        priority = Priority(data.get("priority", "medium").lower())
        status = TaskStatus(data.get("status", "pending").lower())

        # Extract or estimate impact/effort/confidence from notes or defaults
        impact = data.get("impact", 5.0)
        effort = data.get("effort", 5.0)
        confidence = data.get("confidence", 0.8)

        # Get title with fallback to task_id if missing
        title = data.get("title", f"Untitled Task ({data.get('task_id', 'unknown')})")

        return cls(
            task_id=data["task_id"],
            title=title,
            priority=priority,
            priority_score=data.get("priority_score", 0.0),
            estimated_minutes=data.get("estimated_minutes", 0),
            status=status,
            created_at=created_at,
            feature_id=data.get("feature_id"),
            estimated_lines=data.get("estimated_lines"),
            started_at=started_at,
            completed_at=completed_at,
            claimed_at=claimed_at,
            claimed_by=data.get("claimed_by"),
            notes=data.get("notes"),
            blocked_by=data.get("blocked_by", []),
            resources=data.get("resources", []),
            impact=impact,
            effort=effort,
            confidence=confidence,
        )

    @staticmethod
    def _parse_datetime(value: Optional[str]) -> Optional[datetime]:
        """Parse datetime string to datetime object."""
        if not value:
            return None
        try:
            # Try ISO format with timezone
            return datetime.fromisoformat(value.replace("Z", "+00:00"))
        except (ValueError, AttributeError):
            try:
                # Try common formats
                for fmt in ["%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S"]:
                    try:
                        return datetime.strptime(value, fmt)
                    except ValueError:
                        continue
            except Exception:
                pass
            logger.warning(f"Could not parse datetime: {value}")
            return None


@dataclass
class QueueMetadata:
    """Queue metadata."""
    last_updated: datetime
    updated_by: str
    queue_depth_target: tuple[int, int]
    current_depth: int
    last_completed: Optional[str] = None
    lpm_baseline: int = 500
    notes: str = ""

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "QueueMetadata":
        """Create metadata from dictionary."""
        depth_target = data.get("queue_depth_target", "3-5")
        if isinstance(depth_target, str):
            parts = depth_target.split("-")
            depth_target = (int(parts[0]), int(parts[1]) if len(parts) > 1 else int(parts[0]))

        return cls(
            last_updated=Task._parse_datetime(data.get("last_updated", datetime.now().isoformat())) or datetime.now(),
            updated_by=data.get("updated_by", "unknown"),
            queue_depth_target=depth_target,
            current_depth=data.get("current_depth", 0),
            last_completed=data.get("last_completed"),
            lpm_baseline=data.get("lpm_baseline", 500),
            notes=data.get("notes", ""),
        )

    def to_dict(self) -> dict[str, Any]:
        """Convert metadata to dictionary."""
        return {
            "last_updated": self.last_updated.isoformat(),
            "updated_by": self.updated_by,
            "queue_depth_target": f"{self.queue_depth_target[0]}-{self.queue_depth_target[1]}",
            "current_depth": self.current_depth,
            "last_completed": self.last_completed,
            "lpm_baseline": self.lpm_baseline,
            "notes": self.notes,
        }


class QueueManager:
    """Manages the task queue."""

    def __init__(self, queue_file: Path):
        self.queue_file = queue_file
        self.tasks: list[Task] = []
        self.metadata: Optional[QueueMetadata] = None
        self.task_map: dict[str, Task] = {}

    def load(self) -> "QueueManager":
        """Load queue from YAML file."""
        logger.info(f"Loading queue from {self.queue_file}")

        if not self.queue_file.exists():
            raise FileNotFoundError(f"Queue file not found: {self.queue_file}")

        try:
            with open(self.queue_file, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML in queue file: {e}")

        if not data or "tasks" not in data:
            raise ValueError("Queue file missing 'tasks' key")

        # Load tasks
        self.tasks = []
        for task_data in data["tasks"]:
            try:
                # Convert YAML structure to expected format
                converted_data = self._convert_task_data(task_data)
                task = Task.from_dict(converted_data)
                self.tasks.append(task)
                self.task_map[task.task_id] = task
            except Exception as e:
                logger.error(f"Failed to parse task {task_data.get('id', 'unknown')}: {e}")
                continue

        # Load metadata
        if "metadata" in data:
            self.metadata = QueueMetadata.from_dict(data["metadata"])
        else:
            self.metadata = QueueMetadata(
                last_updated=datetime.now(),
                updated_by="queue-manager",
                queue_depth_target=(3, 5),
                current_depth=len([t for t in self.tasks if t.status == TaskStatus.PENDING]),
            )

        logger.info(f"Loaded {len(self.tasks)} tasks")
        return self

    @staticmethod
    def _convert_task_data(task_data: dict[str, Any]) -> dict[str, Any]:
        """Convert YAML task structure to internal format."""
        # Map YAML fields to internal fields
        converted = {
            "task_id": task_data.get("id", "unknown"),
            "title": task_data.get("title", f"Untitled Task ({task_data.get('id', 'unknown')})"),
            "priority": task_data.get("priority", "medium").lower(),
            "priority_score": task_data.get("priority_score", 0.0),
            "estimated_minutes": task_data.get("estimated_minutes", 0),
            "status": task_data.get("status", "pending").lower(),
            "created_at": datetime.now().isoformat(),  # Default to now if not provided
            "impact": 5.0,
            "effort": 5.0,
            "confidence": 0.8,
        }

        # Extract ROI data if available
        if "roi" in task_data:
            roi = task_data["roi"]
            converted["impact"] = roi.get("impact", 5.0)
            converted["effort"] = roi.get("effort", 5.0)
            converted["confidence"] = roi.get("confidence", 0.8)

        # Map blockedBy to blocked_by
        if "blockedBy" in task_data:
            converted["blocked_by"] = task_data["blockedBy"]

        # Map resource_type to resources
        if "resource_type" in task_data:
            converted["resources"] = [task_data["resource_type"]]

        return converted

    def save(self, output_file: Optional[Path] = None) -> None:
        """Save queue to YAML file."""
        target = output_file or self.queue_file
        logger.info(f"Saving queue to {target}")

        data = {
            "queue": [task.to_dict() for task in self.tasks],
        }

        if self.metadata:
            data["metadata"] = self.metadata.to_dict()

        target.parent.mkdir(parents=True, exist_ok=True)
        with open(target, "w", encoding="utf-8") as f:
            yaml.dump(data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

        logger.info(f"Saved {len(self.tasks)} tasks to {target}")

    def prioritize(self) -> list[Task]:
        """
        Sort tasks by priority score (highest first).

        Priority score = (impact / effort) * confidence

        Returns sorted list of pending tasks.
        """
        logger.info("Prioritizing tasks")

        # Filter pending tasks
        pending = [t for t in self.tasks if t.status == TaskStatus.PENDING]

        # Update priority scores
        for task in pending:
            task.priority_score = task.calculate_priority_score()

        # Sort by priority score (descending), then by created_at (ascending)
        sorted_tasks = sorted(
            pending,
            key=lambda t: (-t.priority_score, t.created_at or datetime.min)
        )

        logger.info(f"Prioritized {len(sorted_tasks)} pending tasks")
        return sorted_tasks

    def build_dependency_graph(self) -> dict[str, set[str]]:
        """
        Build dependency graph from blocked_by fields.

        Returns adjacency list where edges point from dependency to dependent.
        """
        graph: dict[str, set[str]] = defaultdict(set)

        for task in self.tasks:
            # Add task to graph even if no dependencies
            if task.task_id not in graph:
                graph[task.task_id] = set()

            # Add blocked_by dependencies
            for blocked_by in task.blocked_by:
                graph[blocked_by].add(task.task_id)

        return dict(graph)

    def detect_cycles(self) -> Optional[list[str]]:
        """
        Detect circular dependencies using DFS.

        Returns cycle path if found, None otherwise.
        """
        graph = self.build_dependency_graph()
        visited: set[str] = set()
        rec_stack: set[str] = set()
        path: list[str] = []

        def dfs(node: str) -> Optional[list[str]]:
            visited.add(node)
            rec_stack.add(node)
            path.append(node)

            for neighbor in graph.get(node, []):
                if neighbor not in visited:
                    result = dfs(neighbor)
                    if result:
                        return result
                elif neighbor in rec_stack:
                    # Found cycle - extract cycle from path
                    cycle_start = path.index(neighbor)
                    return path[cycle_start:] + [neighbor]

            path.pop()
            rec_stack.remove(node)
            return None

        for node in graph:
            if node not in visited:
                cycle = dfs(node)
                if cycle:
                    return cycle

        return None

    def topological_sort(self) -> list[Task]:
        """
        Perform topological sort on tasks based on dependencies.

        Returns tasks in execution order (dependencies first).
        """
        logger.info("Performing topological sort")

        # Check for cycles first
        cycle = self.detect_cycles()
        if cycle:
            raise ValueError(f"Circular dependency detected: {' -> '.join(cycle)}")

        # Build in-degree map
        in_degree: dict[str, int] = {t.task_id: 0 for t in self.tasks}
        graph = self.build_dependency_graph()

        for task in self.tasks:
            for blocked_by in task.blocked_by:
                if blocked_by in in_degree:
                    in_degree[task.task_id] += 1

        # Kahn's algorithm with priority ordering
        queue: deque[str] = deque()
        pending_tasks = [t for t in self.tasks if t.status == TaskStatus.PENDING]

        # Add tasks with no dependencies, sorted by priority
        ready = sorted(
            [t for t in pending_tasks if in_degree[t.task_id] == 0],
            key=lambda t: (-t.priority_score, t.created_at or datetime.min)
        )
        for task in ready:
            queue.append(task.task_id)

        result: list[Task] = []
        processed: set[str] = set()

        while queue:
            task_id = queue.popleft()
            if task_id in processed:
                continue

            task = self.task_map.get(task_id)
            if not task:
                continue

            result.append(task)
            processed.add(task_id)

            # Update in-degrees and add newly ready tasks
            for dependent in graph.get(task_id, []):
                in_degree[dependent] -= 1
                if in_degree[dependent] == 0:
                    dependent_task = self.task_map.get(dependent)
                    if dependent_task and dependent_task.status == TaskStatus.PENDING:
                        # Insert in priority order
                        queue.append(dependent)

        # Sort remaining queue by priority for consistent ordering
        remaining = sorted(
            [t for t in pending_tasks if t.task_id not in processed],
            key=lambda t: (-t.priority_score, t.created_at or datetime.min)
        )
        result.extend(remaining)

        logger.info(f"Topological sort complete: {len(result)} tasks in order")
        return result

    def detect_resource_conflicts(self) -> dict[str, list[Task]]:
        """
        Detect tasks that share resources.

        Returns mapping of resource -> list of tasks using that resource.
        """
        resource_map: dict[str, list[Task]] = defaultdict(list)

        for task in self.tasks:
            if task.status == TaskStatus.PENDING and task.resources:
                for resource in task.resources:
                    resource_map[resource].append(task)

        # Filter to only conflicts (multiple tasks using same resource)
        conflicts = {
            resource: tasks
            for resource, tasks in resource_map.items()
            if len(tasks) > 1
        }

        if conflicts:
            logger.warning(f"Detected {len(conflicts)} resource conflicts")
            for resource, tasks in conflicts.items():
                logger.warning(f"  Resource '{resource}' used by: {[t.task_id for t in tasks]}")

        return conflicts

    def export_execution_state(self, output_file: Path) -> dict[str, Any]:
        """
        Export execution-ready state.

        Creates a YAML file with tasks sorted by dependencies and priority.
        """
        logger.info(f"Exporting execution state to {output_file}")

        # Get topologically sorted tasks
        try:
            sorted_tasks = self.topological_sort()
        except ValueError as e:
            logger.error(f"Cannot export: {e}")
            raise

        # Detect resource conflicts
        conflicts = self.detect_resource_conflicts()

        # Build execution state
        execution_state = {
            "generated_at": datetime.now().isoformat(),
            "queue_file": str(self.queue_file),
            "total_tasks": len(self.tasks),
            "pending_tasks": len([t for t in self.tasks if t.status == TaskStatus.PENDING]),
            "in_progress_tasks": len([t for t in self.tasks if t.status == TaskStatus.IN_PROGRESS]),
            "completed_tasks": len([t for t in self.tasks if t.status == TaskStatus.COMPLETED]),
            "resource_conflicts": {
                resource: [t.task_id for t in tasks]
                for resource, tasks in conflicts.items()
            },
            "execution_order": [task.task_id for task in sorted_tasks],
            "tasks": {task.task_id: task.to_dict() for task in sorted_tasks},
        }

        if self.metadata:
            execution_state["metadata"] = self.metadata.to_dict()

        # Write to file
        output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, "w", encoding="utf-8") as f:
            yaml.dump(execution_state, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

        logger.info(f"Exported execution state: {len(sorted_tasks)} tasks")
        return execution_state

    def get_status(self) -> dict[str, Any]:
        """Get queue status summary."""
        status_counts: dict[str, int] = defaultdict(int)
        for task in self.tasks:
            status_counts[task.status.value] += 1

        total_score = sum(t.priority_score for t in self.tasks if t.status == TaskStatus.PENDING)
        avg_score = total_score / max(1, status_counts.get("pending", 0))

        return {
            "total_tasks": len(self.tasks),
            "status_breakdown": dict(status_counts),
            "pending_priority_score": {
                "total": round(total_score, 2),
                "average": round(avg_score, 2),
            },
            "metadata": self.metadata.to_dict() if self.metadata else None,
        }


def cmd_load(args: argparse.Namespace) -> int:
    """Load and validate queue file."""
    try:
        manager = QueueManager(Path(args.queue_file))
        manager.load()

        print(f"Queue loaded successfully from {args.queue_file}")
        print(f"  Total tasks: {len(manager.tasks)}")
        print(f"  Pending: {len([t for t in manager.tasks if t.status == TaskStatus.PENDING])}")
        print(f"  In Progress: {len([t for t in manager.tasks if t.status == TaskStatus.IN_PROGRESS])}")
        print(f"  Completed: {len([t for t in manager.tasks if t.status == TaskStatus.COMPLETED])}")

        # Check for cycles
        cycle = manager.detect_cycles()
        if cycle:
            print(f"  WARNING: Circular dependency detected: {' -> '.join(cycle)}")
            return 1

        # Check for resource conflicts
        conflicts = manager.detect_resource_conflicts()
        if conflicts:
            print(f"  WARNING: {len(conflicts)} resource conflicts detected")

        return 0

    except Exception as e:
        logger.error(f"Failed to load queue: {e}")
        return 1


def cmd_prioritize(args: argparse.Namespace) -> int:
    """Prioritize tasks and optionally save."""
    try:
        manager = QueueManager(Path(args.queue_file))
        manager.load()

        sorted_tasks = manager.prioritize()

        print("Task Priority Ranking:")
        print("-" * 80)
        for i, task in enumerate(sorted_tasks[:10], 1):
            print(f"{i:2d}. {task.task_id:<20} Score: {task.priority_score:6.2f}  {task.title[:40]}")

        if len(sorted_tasks) > 10:
            print(f"    ... and {len(sorted_tasks) - 10} more tasks")

        if args.output:
            # Reorder tasks in queue by priority
            other_tasks = [t for t in manager.tasks if t.status != TaskStatus.PENDING]
            manager.tasks = sorted_tasks + other_tasks
            manager.save(Path(args.output))
            print(f"\nSaved prioritized queue to {args.output}")

        return 0

    except Exception as e:
        logger.error(f"Failed to prioritize: {e}")
        return 1


def cmd_resolve(args: argparse.Namespace) -> int:
    """Resolve dependencies and check for issues."""
    try:
        manager = QueueManager(Path(args.queue_file))
        manager.load()

        print("Dependency Resolution:")
        print("-" * 80)

        # Check for cycles
        cycle = manager.detect_cycles()
        if cycle:
            print(f"ERROR: Circular dependency detected!")
            print(f"  Cycle: {' -> '.join(cycle)}")
            return 1
        else:
            print("No circular dependencies found.")

        # Build dependency graph
        graph = manager.build_dependency_graph()
        print(f"\nDependency graph: {len(graph)} nodes")

        # Show task dependencies
        tasks_with_deps = [t for t in manager.tasks if t.blocked_by]
        if tasks_with_deps:
            print(f"\nTasks with dependencies ({len(tasks_with_deps)}):")
            for task in tasks_with_deps[:5]:
                print(f"  {task.task_id} blocked by: {', '.join(task.blocked_by)}")
            if len(tasks_with_deps) > 5:
                print(f"  ... and {len(tasks_with_deps) - 5} more")

        # Check for resource conflicts
        conflicts = manager.detect_resource_conflicts()
        if conflicts:
            print(f"\nResource conflicts ({len(conflicts)}):")
            for resource, tasks in list(conflicts.items())[:5]:
                print(f"  '{resource}' used by: {', '.join(t.task_id for t in tasks)}")
        else:
            print("\nNo resource conflicts detected.")

        # Perform topological sort
        try:
            sorted_tasks = manager.topological_sort()
            print(f"\nTopological sort successful: {len(sorted_tasks)} tasks in execution order")
        except ValueError as e:
            print(f"\nTopological sort failed: {e}")
            return 1

        if args.output:
            manager.save(Path(args.output))
            print(f"\nSaved resolved queue to {args.output}")

        return 0

    except Exception as e:
        logger.error(f"Failed to resolve: {e}")
        return 1


def cmd_export(args: argparse.Namespace) -> int:
    """Export execution-ready state."""
    try:
        manager = QueueManager(Path(args.queue_file))
        manager.load()

        output_file = Path(args.output) if args.output else Path("execution-state.yaml")
        state = manager.export_execution_state(output_file)

        print(f"Execution state exported to {output_file}")
        print(f"  Total tasks: {state['total_tasks']}")
        print(f"  Pending: {state['pending_tasks']}")
        print(f"  In Progress: {state['in_progress_tasks']}")
        print(f"  Completed: {state['completed_tasks']}")

        if state['resource_conflicts']:
            print(f"  Resource conflicts: {len(state['resource_conflicts'])}")

        print(f"\nExecution order (first 10):")
        for i, task_id in enumerate(state['execution_order'][:10], 1):
            task = state['tasks'][task_id]
            print(f"  {i:2d}. {task_id} (Score: {task['priority_score']:.2f})")

        if len(state['execution_order']) > 10:
            print(f"  ... and {len(state['execution_order']) - 10} more tasks")

        return 0

    except Exception as e:
        logger.error(f"Failed to export: {e}")
        return 1


def cmd_status(args: argparse.Namespace) -> int:
    """Show queue status."""
    try:
        manager = QueueManager(Path(args.queue_file))
        manager.load()

        status = manager.get_status()

        print("Queue Status")
        print("=" * 80)
        print(f"Total tasks: {status['total_tasks']}")
        print(f"\nStatus breakdown:")
        for status_type, count in status['status_breakdown'].items():
            print(f"  {status_type:15s}: {count:3d}")

        print(f"\nPending task scores:")
        print(f"  Total:   {status['pending_priority_score']['total']}")
        print(f"  Average: {status['pending_priority_score']['average']}")

        if status['metadata']:
            meta = status['metadata']
            print(f"\nMetadata:")
            print(f"  Last updated: {meta['last_updated']}")
            print(f"  Updated by:   {meta['updated_by']}")
            print(f"  Queue depth:  {meta['current_depth']} (target: {meta['queue_depth_target']})")
            print(f"  LPM baseline: {meta['lpm_baseline']}")

        return 0

    except Exception as e:
        logger.error(f"Failed to get status: {e}")
        return 1


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="BB5 Queue Manager - Task Queue Management and Prioritization",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  bb5-queue-manager.py load
  bb5-queue-manager.py prioritize --output prioritized-queue.yaml
  bb5-queue-manager.py resolve
  bb5-queue-manager.py export --output execution-state.yaml
  bb5-queue-manager.py status
        """
    )

    parser.add_argument(
        "--queue-file",
        default=".autonomous/agents/communications/queue.yaml",
        help="Path to queue.yaml file (default: .autonomous/agents/communications/queue.yaml)"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # load command
    load_parser = subparsers.add_parser("load", help="Load and validate queue file")
    load_parser.set_defaults(func=cmd_load)

    # prioritize command
    prioritize_parser = subparsers.add_parser("prioritize", help="Prioritize tasks by ROI")
    prioritize_parser.add_argument("-o", "--output", help="Output file path")
    prioritize_parser.set_defaults(func=cmd_prioritize)

    # resolve command
    resolve_parser = subparsers.add_parser("resolve", help="Resolve dependencies")
    resolve_parser.add_argument("-o", "--output", help="Output file path")
    resolve_parser.set_defaults(func=cmd_resolve)

    # export command
    export_parser = subparsers.add_parser("export", help="Export execution-ready state")
    export_parser.add_argument("-o", "--output", default="execution-state.yaml",
                               help="Output file path (default: execution-state.yaml)")
    export_parser.set_defaults(func=cmd_export)

    # status command
    status_parser = subparsers.add_parser("status", help="Show queue status")
    status_parser.set_defaults(func=cmd_status)

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    if not args.command:
        parser.print_help()
        return 1

    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
