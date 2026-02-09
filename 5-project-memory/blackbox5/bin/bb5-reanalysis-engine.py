#!/usr/bin/env python3
"""
BB5 Reanalysis Engine - Task Reanalysis and Priority Management

This script detects trigger conditions from the reanalysis registry and applies
auto-actions (flag, boost, requeue, invalidate) to affected tasks. It integrates
with the queue.yaml to update task priorities and provides git hook integration.

Usage:
    bb5-reanalysis-engine.py detect [--trigger-type TYPE] [--registry-file PATH]
    bb5-reanalysis-engine.py apply [--dry-run] [--registry-file PATH] [--queue-file PATH]
    bb5-reanalysis-engine.py status [--task-id ID] [--registry-file PATH] [--queue-file PATH]
    bb5-reanalysis-engine.py git-hook [--hook-type TYPE] [--registry-file PATH]

Trigger Types:
    structural_change: Monitor git changes for infrastructure modifications
    dependency_complete: Check when tasks complete to unblock dependents
    health_drop: Monitor task success rates
    time_based: Detect stale tasks (>7 days)
    failure_pattern: Detect similar task failures

Exit Codes:
    0: Success
    1: Configuration error
    2: Detection failure
    3: Apply failure
    4: No triggers detected
"""

from __future__ import annotations

import argparse
import hashlib
import json
import logging
import os
import re
import subprocess
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Any, Optional, TypeVar

import yaml

# Add lib directory to path for storage import
sys.path.insert(0, str(Path(__file__).parent.parent / ".autonomous" / "lib"))
from storage import get_storage

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("bb5-reanalysis-engine")

T = TypeVar("T")


# =============================================================================
# Enums and Data Classes
# =============================================================================

class TriggerType(Enum):
    """Types of reanalysis triggers."""
    STRUCTURAL_CHANGE = "structural_change"
    DEPENDENCY_COMPLETE = "dependency_complete"
    HEALTH_DROP = "health_drop"
    TIME_BASED = "time_based"
    FAILURE_PATTERN = "failure_pattern"


class ActionType(Enum):
    """Types of actions that can be applied to tasks."""
    FLAG = "flag"
    BOOST = "boost"
    REQUEUE = "requeue"
    INVALIDATE = "invalidate"
    MARK_OBSOLETE = "mark_obsolete"
    MARK_COMPLETED = "mark_completed"
    ADD_DEPENDENCIES = "add_dependencies"


class TaskStatus(Enum):
    """Task status enumeration."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    BLOCKED = "blocked"
    CANCELLED = "cancelled"
    INVALID = "invalid"
    OBSOLETE = "obsolete"


class Priority(Enum):
    """Priority level enumeration."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    REVIEW = "review"


@dataclass
class Trigger:
    """Represents a detected trigger condition."""
    trigger_type: TriggerType
    source: str
    detected_at: datetime
    metadata: dict[str, Any] = field(default_factory=dict)
    affected_tasks: list[str] = field(default_factory=list)
    confidence: float = 1.0

    def to_dict(self) -> dict[str, Any]:
        """Convert trigger to dictionary."""
        return {
            "trigger_type": self.trigger_type.value,
            "source": self.source,
            "detected_at": self.detected_at.isoformat(),
            "metadata": self.metadata,
            "affected_tasks": self.affected_tasks,
            "confidence": self.confidence,
        }


@dataclass
class Task:
    """Represents a task in the system."""
    task_id: str
    title: str
    status: TaskStatus
    priority: Priority
    created_at: datetime
    updated_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    depends_on: list[str] = field(default_factory=list)
    blocked_by: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    files_referenced: list[str] = field(default_factory=list)
    success_rate: Optional[float] = None
    failure_count: int = 0
    last_failure: Optional[datetime] = None
    notes: Optional[str] = None

    def to_dict(self) -> dict[str, Any]:
        """Convert task to dictionary."""
        result = {
            "task_id": self.task_id,
            "title": self.title,
            "status": self.status.value,
            "priority": self.priority.value,
            "created_at": self.created_at.isoformat(),
            "depends_on": self.depends_on,
            "blocked_by": self.blocked_by,
            "tags": self.tags,
            "files_referenced": self.files_referenced,
            "failure_count": self.failure_count,
        }
        if self.updated_at:
            result["updated_at"] = self.updated_at.isoformat()
        if self.completed_at:
            result["completed_at"] = self.completed_at.isoformat()
        if self.success_rate is not None:
            result["success_rate"] = self.success_rate
        if self.last_failure:
            result["last_failure"] = self.last_failure.isoformat()
        if self.notes:
            result["notes"] = self.notes
        return result

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Task:
        """Create task from dictionary."""
        return cls(
            task_id=data["task_id"],
            title=data.get("title", "Untitled"),
            status=TaskStatus(data.get("status", "pending")),
            priority=Priority(data.get("priority", "medium")),
            created_at=datetime.fromisoformat(data["created_at"]),
            updated_at=datetime.fromisoformat(data["updated_at"]) if "updated_at" in data else None,
            completed_at=datetime.fromisoformat(data["completed_at"]) if "completed_at" in data else None,
            depends_on=data.get("depends_on", []),
            blocked_by=data.get("blocked_by", []),
            tags=data.get("tags", []),
            files_referenced=data.get("files_referenced", []),
            success_rate=data.get("success_rate"),
            failure_count=data.get("failure_count", 0),
            last_failure=datetime.fromisoformat(data["last_failure"]) if "last_failure" in data else None,
            notes=data.get("notes"),
        )


@dataclass
class Action:
    """Represents an action to be applied to a task."""
    action_type: ActionType
    task_id: str
    trigger: Trigger
    reason: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Convert action to dictionary."""
        return {
            "action_type": self.action_type.value,
            "task_id": self.task_id,
            "trigger": self.trigger.to_dict(),
            "reason": self.reason,
            "metadata": self.metadata,
        }


# =============================================================================
# Configuration and Registry
# =============================================================================

class ReanalysisRegistry:
    """Manages the reanalysis registry configuration using storage backend."""

    DEFAULT_REGISTRY_PATH = ".autonomous/agents/reanalysis/reanalysis-registry.yaml"

    def __init__(self, registry_path: Optional[Path] = None):
        self.registry_path = registry_path or self._find_registry()
        self.config: dict[str, Any] = {}
        self._storage = None
        self.load()

    def _get_storage(self):
        """Get or create storage instance."""
        if self._storage is None:
            self._storage = get_storage()
        return self._storage

    def _find_registry(self) -> Path:
        """Find the registry file in the project."""
        # Try to find from BB5_PROJECT_ROOT or current directory
        project_root = Path(os.environ.get("BB5_PROJECT_ROOT", "."))
        path = project_root / self.DEFAULT_REGISTRY_PATH
        if path.exists():
            return path

        # Search up directory tree
        current = Path.cwd()
        for _ in range(5):  # Search up 5 levels
            path = current / self.DEFAULT_REGISTRY_PATH
            if path.exists():
                return path
            current = current.parent

        raise FileNotFoundError(f"Registry file not found: {self.DEFAULT_REGISTRY_PATH}")

    def load(self) -> None:
        """Load the registry configuration using storage backend."""
        try:
            # Try storage backend first for atomic reads
            storage = self._get_storage()
            # Load from storage if registry is stored there
            self.config = self._load_yaml_atomic(self.registry_path)
            if not self.config:
                self.config = {}
            logger.debug(f"Loaded registry from {self.registry_path}")
        except Exception as e:
            logger.error(f"Failed to load registry: {e}")
            raise

    def _load_yaml_atomic(self, path: Path) -> Optional[dict[str, Any]]:
        """Load YAML file with atomic read pattern."""
        if not path.exists():
            return None
        try:
            with open(path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f)
        except Exception as e:
            logger.warning(f"Failed to load {path}: {e}")
            return None

    def _save_yaml_atomic(self, path: Path, data: dict[str, Any]) -> bool:
        """Save YAML file with atomic write pattern."""
        try:
            import tempfile
            import os

            path.parent.mkdir(parents=True, exist_ok=True)

            # Write to temp file first (atomic write pattern)
            with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False, dir=path.parent) as f:
                yaml.dump(data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
                temp_path = f.name

            # Atomic rename
            os.replace(temp_path, path)
            return True
        except Exception as e:
            logger.error(f"Failed to save {path}: {e}")
            return False

    def get_trigger_config(self, trigger_type: TriggerType) -> dict[str, Any]:
        """Get configuration for a specific trigger type."""
        return self.config.get("triggers", {}).get(trigger_type.value, {})

    def get_invalidation_rules(self) -> list[dict[str, Any]]:
        """Get all invalidation rules."""
        return self.config.get("invalidation_rules", [])

    def get_settings(self) -> dict[str, Any]:
        """Get global settings."""
        return self.config.get("settings", {})

    def get_action_config(self, action_type: ActionType) -> dict[str, Any]:
        """Get configuration for a specific action type."""
        return self.config.get("actions", {}).get(action_type.value, {})


# =============================================================================
# Task Registry
# =============================================================================

class TaskRegistry:
    """Manages task data and operations using storage backend."""

    DEFAULT_TASKS_PATH = "tasks/active"
    DEFAULT_QUEUE_PATH = ".autonomous/memory/queue.yaml"

    def __init__(self, tasks_path: Optional[Path] = None, queue_path: Optional[Path] = None):
        self.tasks_path = tasks_path or self._find_tasks_path()
        self.queue_path = queue_path or self._find_queue_path()
        self.tasks: dict[str, Task] = {}
        self._storage = None
        self.load_tasks()

    def _get_storage(self):
        """Get or create storage instance."""
        if self._storage is None:
            self._storage = get_storage()
        return self._storage

    def _find_tasks_path(self) -> Path:
        """Find the tasks directory."""
        project_root = Path(os.environ.get("BB5_PROJECT_ROOT", "."))
        path = project_root / self.DEFAULT_TASKS_PATH
        if path.exists():
            return path

        current = Path.cwd()
        for _ in range(5):
            path = current / self.DEFAULT_TASKS_PATH
            if path.exists():
                return path
            current = current.parent

        return path  # Return default even if not found

    def _find_queue_path(self) -> Path:
        """Find the queue file."""
        project_root = Path(os.environ.get("BB5_PROJECT_ROOT", "."))
        path = project_root / self.DEFAULT_QUEUE_PATH
        if path.exists():
            return path

        current = Path.cwd()
        for _ in range(5):
            path = current / self.DEFAULT_QUEUE_PATH
            if path.exists():
                return path
            current = current.parent

        return path

    def load_tasks(self) -> None:
        """Load all tasks from the storage backend."""
        try:
            storage = self._get_storage()
            task_list = storage.tasks.list()

            for task_data in task_list:
                try:
                    # Convert storage format to Task format
                    converted_data = self._convert_storage_to_task(task_data)
                    task = Task.from_dict(converted_data)
                    self.tasks[task.task_id] = task
                except Exception as e:
                    logger.warning(f"Failed to load task from storage: {e}")

            logger.info(f"Loaded {len(self.tasks)} tasks from storage")
        except Exception as e:
            logger.warning(f"Failed to load from storage, falling back to file system: {e}")
            # Fallback to file system loading
            self._load_tasks_from_filesystem()

    def _load_tasks_from_filesystem(self) -> None:
        """Fallback: Load tasks from file system."""
        if not self.tasks_path.exists():
            logger.warning(f"Tasks path not found: {self.tasks_path}")
            return

        for task_dir in self.tasks_path.iterdir():
            if task_dir.is_dir():
                task_file = task_dir / "task.yaml"
                if not task_file.exists():
                    task_file = task_dir / f"{task_dir.name}.yaml"

                if task_file.exists():
                    try:
                        with open(task_file, "r") as f:
                            data = yaml.safe_load(f)
                        if data:
                            task = Task.from_dict(data)
                            self.tasks[task.task_id] = task
                    except Exception as e:
                        logger.warning(f"Failed to load task from {task_file}: {e}")

        logger.info(f"Loaded {len(self.tasks)} tasks from file system")

    def _convert_storage_to_task(self, task_data: dict[str, Any]) -> dict[str, Any]:
        """Convert storage task format to Task class format."""
        return {
            "task_id": task_data.get("id", "unknown"),
            "title": task_data.get("title", "Untitled"),
            "status": task_data.get("status", "pending"),
            "priority": task_data.get("priority", "medium"),
            "created_at": task_data.get("created_at", datetime.now().isoformat()),
            "updated_at": task_data.get("updated_at"),
            "completed_at": task_data.get("completed_at"),
            "depends_on": task_data.get("depends_on", []),
            "blocked_by": task_data.get("blockedBy", []),
            "tags": task_data.get("tags", []),
            "files_referenced": task_data.get("files_referenced", []),
            "success_rate": task_data.get("success_rate"),
            "failure_count": task_data.get("failure_count", 0),
            "last_failure": task_data.get("last_failure"),
            "notes": task_data.get("notes"),
        }

    def _convert_task_to_storage(self, task: Task) -> dict[str, Any]:
        """Convert Task class to storage format."""
        return {
            "id": task.task_id,
            "title": task.title,
            "status": task.status.value,
            "priority": task.priority.value,
            "created_at": task.created_at.isoformat(),
            "updated_at": task.updated_at.isoformat() if task.updated_at else None,
            "completed_at": task.completed_at.isoformat() if task.completed_at else None,
            "depends_on": task.depends_on,
            "blockedBy": task.blocked_by,
            "tags": task.tags,
            "files_referenced": task.files_referenced,
            "success_rate": task.success_rate,
            "failure_count": task.failure_count,
            "last_failure": task.last_failure.isoformat() if task.last_failure else None,
            "notes": task.notes,
        }

    def get_task(self, task_id: str) -> Optional[Task]:
        """Get a task by ID."""
        # First check local cache
        if task_id in self.tasks:
            return self.tasks[task_id]

        # Try storage backend
        try:
            storage = self._get_storage()
            task_data = storage.tasks.get(task_id)
            if task_data:
                converted_data = self._convert_storage_to_task(task_data)
                return Task.from_dict(converted_data)
        except Exception as e:
            logger.warning(f"Failed to get task from storage: {e}")

        return None

    def get_tasks_by_status(self, status: TaskStatus) -> list[Task]:
        """Get all tasks with a specific status."""
        return [t for t in self.tasks.values() if t.status == status]

    def get_blocked_tasks(self) -> list[Task]:
        """Get all blocked tasks."""
        return [t for t in self.tasks.values() if t.status == TaskStatus.BLOCKED]

    def get_tasks_referencing_file(self, file_path: str) -> list[Task]:
        """Get all tasks that reference a specific file."""
        return [t for t in self.tasks.values() if file_path in t.files_referenced]

    def get_tasks_blocked_by(self, task_id: str) -> list[Task]:
        """Get all tasks blocked by a specific task."""
        return [t for t in self.tasks.values() if task_id in t.blocked_by or task_id in t.depends_on]

    def update_task(self, task: Task) -> None:
        """Update a task in the registry and persist to storage."""
        self.tasks[task.task_id] = task

        # Persist to storage backend
        try:
            storage = self._get_storage()
            task_data = self._convert_task_to_storage(task)
            storage.tasks.save(task_data)
            logger.debug(f"Persisted task {task.task_id} to storage")
        except Exception as e:
            logger.warning(f"Failed to persist task to storage: {e}")

    def load_queue(self) -> dict[str, Any]:
        """Load the queue configuration from storage backend."""
        try:
            storage = self._get_storage()
            queue_tasks = storage.queue.get_all()
            return {"tasks": queue_tasks, "version": "1.0.0"}
        except Exception as e:
            logger.warning(f"Failed to load queue from storage: {e}")

        # Fallback to file system
        if not self.queue_path.exists():
            return {"tasks": [], "version": "1.0.0"}

        try:
            with open(self.queue_path, "r") as f:
                return yaml.safe_load(f) or {"tasks": [], "version": "1.0.0"}
        except Exception as e:
            logger.error(f"Failed to load queue: {e}")
            return {"tasks": [], "version": "1.0.0"}

    def save_queue(self, queue: dict[str, Any]) -> None:
        """Save the queue configuration using atomic writes."""
        try:
            import tempfile
            import os

            self.queue_path.parent.mkdir(parents=True, exist_ok=True)

            # Write to temp file first (atomic write pattern)
            with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False, dir=self.queue_path.parent) as f:
                yaml.dump(queue, f, default_flow_style=False, sort_keys=False)
                temp_path = f.name

            # Atomic rename
            os.replace(temp_path, self.queue_path)
            logger.info(f"Saved queue to {self.queue_path}")
        except Exception as e:
            logger.error(f"Failed to save queue: {e}")
            raise


# =============================================================================
# Trigger Detectors
# =============================================================================

class TriggerDetector:
    """Base class for trigger detectors."""

    def __init__(self, registry: ReanalysisRegistry, task_registry: TaskRegistry):
        self.registry = registry
        self.task_registry = task_registry

    def detect(self) -> list[Trigger]:
        """Detect triggers. Override in subclasses."""
        raise NotImplementedError


class StructuralChangeDetector(TriggerDetector):
    """Detects structural changes in the codebase."""

    SHARED_PATTERNS = [
        r"shared/.*",
        r"core/.*",
        r"api/.*",
        r"models/.*",
        r"config/.*",
        r"\.autonomous/memory/.*",
        r"bin/.*",
    ]

    def detect(self) -> list[Trigger]:
        """Detect structural changes from recent git commits."""
        triggers = []

        try:
            # Get files changed in last commit
            result = subprocess.run(
                ["git", "diff", "HEAD~1", "--name-only"],
                capture_output=True,
                text=True,
                check=True,
            )
            changed_files = result.stdout.strip().split("\n")

            # Filter for shared/infrastructure files
            shared_files = self._filter_shared_files(changed_files)

            if shared_files:
                # Find affected tasks
                affected_tasks = []
                for file_path in shared_files:
                    tasks = self.task_registry.get_tasks_referencing_file(file_path)
                    affected_tasks.extend([t.task_id for t in tasks])

                if affected_tasks:
                    triggers.append(Trigger(
                        trigger_type=TriggerType.STRUCTURAL_CHANGE,
                        source="git:post-commit",
                        detected_at=datetime.now(),
                        metadata={"changed_files": shared_files},
                        affected_tasks=list(set(affected_tasks)),
                        confidence=0.9,
                    ))

        except subprocess.CalledProcessError as e:
            logger.warning(f"Git command failed: {e}")
        except Exception as e:
            logger.error(f"Structural change detection failed: {e}")

        return triggers

    def _filter_shared_files(self, files: list[str]) -> list[str]:
        """Filter files to only include shared/infrastructure files."""
        shared = []
        for file_path in files:
            for pattern in self.SHARED_PATTERNS:
                if re.match(pattern, file_path):
                    shared.append(file_path)
                    break
        return shared


class DependencyCompleteDetector(TriggerDetector):
    """Detects when dependencies are completed."""

    def detect(self) -> list[Trigger]:
        """Detect tasks that have completed and may unblock dependents."""
        triggers = []

        # Find recently completed tasks
        completed_tasks = [
            t for t in self.task_registry.tasks.values()
            if t.status == TaskStatus.COMPLETED and t.completed_at
            and (datetime.now() - t.completed_at).days < 1  # Completed in last day
        ]

        for completed in completed_tasks:
            # Find tasks blocked by this one
            blocked = self.task_registry.get_tasks_blocked_by(completed.task_id)

            if blocked:
                triggers.append(Trigger(
                    trigger_type=TriggerType.DEPENDENCY_COMPLETE,
                    source=f"task:{completed.task_id}",
                    detected_at=datetime.now(),
                    metadata={"completed_task": completed.task_id},
                    affected_tasks=[t.task_id for t in blocked],
                    confidence=1.0,
                ))

        return triggers


class HealthDropDetector(TriggerDetector):
    """Detects tasks with declining health metrics."""

    def detect(self) -> list[Trigger]:
        """Detect tasks with low success rates."""
        triggers = []
        settings = self.registry.get_settings()
        health_settings = settings.get("health", {})
        threshold = health_settings.get("success_rate_threshold", 0.8)

        # Find tasks with low success rates
        failing_tasks = [
            t for t in self.task_registry.tasks.values()
            if t.success_rate is not None and t.success_rate < threshold
        ]

        if failing_tasks:
            triggers.append(Trigger(
                trigger_type=TriggerType.HEALTH_DROP,
                source="health_monitor",
                detected_at=datetime.now(),
                metadata={
                    "threshold": threshold,
                    "failing_count": len(failing_tasks),
                },
                affected_tasks=[t.task_id for t in failing_tasks],
                confidence=0.85,
            ))

        return triggers


class TimeBasedDetector(TriggerDetector):
    """Detects stale tasks based on time."""

    def detect(self) -> list[Trigger]:
        """Detect tasks that have been pending for too long."""
        triggers = []
        settings = self.registry.get_settings()
        time_settings = settings.get("time", {})
        stale_days = time_settings.get("stale_task_days", 7)

        stale_threshold = datetime.now() - timedelta(days=stale_days)

        # Find stale pending tasks
        stale_tasks = [
            t for t in self.task_registry.tasks.values()
            if t.status == TaskStatus.PENDING and t.created_at < stale_threshold
        ]

        if stale_tasks:
            triggers.append(Trigger(
                trigger_type=TriggerType.TIME_BASED,
                source="scheduler",
                detected_at=datetime.now(),
                metadata={
                    "stale_days": stale_days,
                    "stale_count": len(stale_tasks),
                },
                affected_tasks=[t.task_id for t in stale_tasks],
                confidence=0.95,
            ))

        return triggers


class FailurePatternDetector(TriggerDetector):
    """Detects patterns of task failures."""

    def detect(self) -> list[Trigger]:
        """Detect similar failure patterns across tasks."""
        triggers = []
        settings = self.registry.get_settings()
        pattern_settings = settings.get("patterns", {})
        min_failures = pattern_settings.get("min_similar_failures", 3)

        # Group tasks by failure patterns
        failure_groups: dict[str, list[Task]] = defaultdict(list)

        for task in self.task_registry.tasks.values():
            if task.failure_count > 0:
                # Simple pattern: group by tags
                for tag in task.tags:
                    failure_groups[tag].append(task)

        # Find groups with significant failures
        for pattern, tasks in failure_groups.items():
            if len(tasks) >= min_failures:
                total_failures = sum(t.failure_count for t in tasks)
                if total_failures >= min_failures:
                    triggers.append(Trigger(
                        trigger_type=TriggerType.FAILURE_PATTERN,
                        source="pattern_analyzer",
                        detected_at=datetime.now(),
                        metadata={
                            "pattern": pattern,
                            "affected_count": len(tasks),
                            "total_failures": total_failures,
                        },
                        affected_tasks=[t.task_id for t in tasks],
                        confidence=min(0.95, 0.7 + (len(tasks) * 0.05)),
                    ))

        return triggers


# =============================================================================
# Action Executor
# =============================================================================

class ActionExecutor:
    """Executes actions on tasks."""

    def __init__(self, task_registry: TaskRegistry, dry_run: bool = False):
        self.task_registry = task_registry
        self.dry_run = dry_run
        self.executed_actions: list[Action] = []

    def execute(self, action: Action) -> bool:
        """Execute an action on a task."""
        task = self.task_registry.get_task(action.task_id)
        if not task:
            logger.warning(f"Task not found: {action.task_id}")
            return False

        if self.dry_run:
            logger.info(f"[DRY RUN] Would execute {action.action_type.value} on {action.task_id}")
            self.executed_actions.append(action)
            return True

        try:
            handler = getattr(self, f"_execute_{action.action_type.value}", None)
            if handler:
                handler(task, action)
                self.executed_actions.append(action)
                logger.info(f"Executed {action.action_type.value} on {action.task_id}")
                return True
            else:
                logger.error(f"No handler for action type: {action.action_type.value}")
                return False
        except Exception as e:
            logger.error(f"Failed to execute action: {e}")
            return False

    def _execute_flag(self, task: Task, action: Action) -> None:
        """Flag a task for review."""
        if "needs-review" not in task.tags:
            task.tags.append("needs-review")
        if "reanalysis-flagged" not in task.tags:
            task.tags.append("reanalysis-flagged")
        task.priority = Priority.REVIEW
        task.updated_at = datetime.now()
        self.task_registry.update_task(task)

    def _execute_boost(self, task: Task, action: Action) -> None:
        """Boost a task's priority."""
        priority_order = [Priority.LOW, Priority.MEDIUM, Priority.HIGH, Priority.CRITICAL]
        current_idx = priority_order.index(task.priority) if task.priority in priority_order else 1

        if current_idx < len(priority_order) - 1:
            task.priority = priority_order[current_idx + 1]

        if "priority-boosted" not in task.tags:
            task.tags.append("priority-boosted")
        task.updated_at = datetime.now()
        self.task_registry.update_task(task)

    def _execute_requeue(self, task: Task, action: Action) -> None:
        """Requeue a task."""
        task.status = TaskStatus.PENDING
        task.blocked_by = []
        if "requeued" not in task.tags:
            task.tags.append("requeued")
        if "unblocked" not in task.tags:
            task.tags.append("unblocked")
        task.updated_at = datetime.now()
        self.task_registry.update_task(task)

    def _execute_invalidate(self, task: Task, action: Action) -> None:
        """Invalidate a task."""
        task.status = TaskStatus.INVALID
        if "invalidated" not in task.tags:
            task.tags.append("invalidated")
        task.tags.append(action.trigger.trigger_type.value)
        task.updated_at = datetime.now()
        task.notes = f"{task.notes or ''}\nInvalidated: {action.reason}".strip()
        self.task_registry.update_task(task)

    def _execute_mark_obsolete(self, task: Task, action: Action) -> None:
        """Mark a task as obsolete."""
        task.status = TaskStatus.OBSOLETE
        if "obsolete" not in task.tags:
            task.tags.append("obsolete")
        if "auto-detected" not in task.tags:
            task.tags.append("auto-detected")
        task.updated_at = datetime.now()
        self.task_registry.update_task(task)

    def _execute_mark_completed(self, task: Task, action: Action) -> None:
        """Mark a task as completed."""
        task.status = TaskStatus.COMPLETED
        task.completed_at = datetime.now()
        if "auto-completed" not in task.tags:
            task.tags.append("auto-completed")
        if "issue-resolved" not in task.tags:
            task.tags.append("issue-resolved")
        task.updated_at = datetime.now()
        self.task_registry.update_task(task)

    def _execute_add_dependencies(self, task: Task, action: Action) -> None:
        """Add dependencies to a task."""
        new_deps = action.metadata.get("new_dependencies", [])
        for dep in new_deps:
            if dep not in task.depends_on:
                task.depends_on.append(dep)
                task.blocked_by.append(dep)
        task.status = TaskStatus.BLOCKED
        if "dependencies-added" not in task.tags:
            task.tags.append("dependencies-added")
        task.updated_at = datetime.now()
        self.task_registry.update_task(task)


# =============================================================================
# Reanalysis Engine
# =============================================================================

class ReanalysisEngine:
    """Main reanalysis engine that coordinates detection and action execution."""

    def __init__(
        self,
        registry_path: Optional[Path] = None,
        tasks_path: Optional[Path] = None,
        queue_path: Optional[Path] = None,
        dry_run: bool = False,
    ):
        self.registry = ReanalysisRegistry(registry_path)
        self.task_registry = TaskRegistry(tasks_path, queue_path)
        self.dry_run = dry_run
        self.detectors: dict[TriggerType, TriggerDetector] = {
            TriggerType.STRUCTURAL_CHANGE: StructuralChangeDetector(self.registry, self.task_registry),
            TriggerType.DEPENDENCY_COMPLETE: DependencyCompleteDetector(self.registry, self.task_registry),
            TriggerType.HEALTH_DROP: HealthDropDetector(self.registry, self.task_registry),
            TriggerType.TIME_BASED: TimeBasedDetector(self.registry, self.task_registry),
            TriggerType.FAILURE_PATTERN: FailurePatternDetector(self.registry, self.task_registry),
        }
        self.executor = ActionExecutor(self.task_registry, dry_run)

    def detect_triggers(self, trigger_type: Optional[TriggerType] = None) -> list[Trigger]:
        """Detect triggers of a specific type or all types."""
        triggers = []

        if trigger_type:
            detector = self.detectors.get(trigger_type)
            if detector:
                triggers.extend(detector.detect())
        else:
            for detector in self.detectors.values():
                triggers.extend(detector.detect())

        return triggers

    def apply_actions(self, triggers: list[Trigger]) -> list[Action]:
        """Apply actions based on detected triggers."""
        actions = []

        for trigger in triggers:
            actions.extend(self._determine_actions(trigger))

        # Execute actions
        for action in actions:
            self.executor.execute(action)

        return actions

    def _determine_actions(self, trigger: Trigger) -> list[Action]:
        """Determine actions to take based on a trigger."""
        actions = []

        # Get trigger config
        trigger_config = self.registry.get_trigger_config(trigger.trigger_type)
        auto_actions = trigger_config.get("auto_actions", {})

        for task_id in trigger.affected_tasks:
            task = self.task_registry.get_task(task_id)
            if not task:
                continue

            # Determine action based on trigger type and thresholds
            action_type = self._select_action(trigger, task, auto_actions)

            if action_type:
                actions.append(Action(
                    action_type=action_type,
                    task_id=task_id,
                    trigger=trigger,
                    reason=f"Triggered by {trigger.trigger_type.value} from {trigger.source}",
                    metadata=trigger.metadata,
                ))

        return actions

    def _select_action(
        self,
        trigger: Trigger,
        task: Task,
        auto_actions: dict[str, Any],
    ) -> Optional[ActionType]:
        """Select the appropriate action for a task based on trigger."""
        # Check invalidation rules first
        if self._should_invalidate(task, trigger):
            return ActionType.INVALIDATE

        # Apply trigger-specific logic
        if trigger.trigger_type == TriggerType.STRUCTURAL_CHANGE:
            if trigger.metadata.get("breaking_change"):
                return ActionType.INVALIDATE
            return ActionType.FLAG

        elif trigger.trigger_type == TriggerType.DEPENDENCY_COMPLETE:
            # Check if all dependencies are satisfied
            all_deps_completed = all(
                self.task_registry.get_task(dep) and
                self.task_registry.get_task(dep).status == TaskStatus.COMPLETED
                for dep in task.depends_on
            )
            if all_deps_completed and task.status == TaskStatus.BLOCKED:
                return ActionType.REQUEUE
            return ActionType.BOOST

        elif trigger.trigger_type == TriggerType.HEALTH_DROP:
            if task.success_rate and task.success_rate < 0.5:
                return ActionType.INVALIDATE
            return ActionType.FLAG

        elif trigger.trigger_type == TriggerType.TIME_BASED:
            days_pending = (datetime.now() - task.created_at).days
            if days_pending > 30:
                return ActionType.INVALIDATE
            elif days_pending > 14:
                return ActionType.FLAG
            elif task.priority in [Priority.HIGH, Priority.CRITICAL]:
                return ActionType.BOOST
            return ActionType.FLAG

        elif trigger.trigger_type == TriggerType.FAILURE_PATTERN:
            return ActionType.FLAG

        return None

    def _should_invalidate(self, task: Task, trigger: Trigger) -> bool:
        """Check if a task should be invalidated based on rules."""
        rules = self.registry.get_invalidation_rules()

        for rule in rules:
            rule_name = rule.get("name", "")

            if rule_name == "file_no_longer_exists":
                for file_path in task.files_referenced:
                    if not Path(file_path).exists():
                        return True

            elif rule_name == "approach_fundamentally_flawed":
                if task.failure_count > 5:
                    return True

            elif rule_name == "context_changed_significantly":
                # Would need more sophisticated context comparison
                pass

        return False

    def update_queue(self, actions: list[Action]) -> None:
        """Update the queue with new task priorities."""
        queue = self.task_registry.load_queue()

        # Update queue entries based on actions
        for action in actions:
            if action.action_type in [ActionType.BOOST, ActionType.REQUEUE]:
                # Find or create queue entry
                found = False
                for entry in queue.get("tasks", []):
                    if entry.get("task_id") == action.task_id:
                        entry["priority"] = self.task_registry.get_task(action.task_id).priority.value
                        found = True
                        break

                if not found and action.action_type == ActionType.REQUEUE:
                    queue["tasks"].append({
                        "task_id": action.task_id,
                        "priority": self.task_registry.get_task(action.task_id).priority.value,
                        "added_at": datetime.now().isoformat(),
                    })

        if not self.dry_run:
            self.task_registry.save_queue(queue)

    def get_status(self, task_id: Optional[str] = None) -> dict[str, Any]:
        """Get status of tasks and recent triggers."""
        status = {
            "timestamp": datetime.now().isoformat(),
            "total_tasks": len(self.task_registry.tasks),
            "tasks_by_status": {},
        }

        # Count tasks by status
        for task in self.task_registry.tasks.values():
            status_key = task.status.value
            status["tasks_by_status"][status_key] = status["tasks_by_status"].get(status_key, 0) + 1

        if task_id:
            task = self.task_registry.get_task(task_id)
            if task:
                status["task"] = task.to_dict()
            else:
                status["error"] = f"Task not found: {task_id}"

        return status


# =============================================================================
# CLI Commands
# =============================================================================

def cmd_detect(args: argparse.Namespace) -> int:
    """Execute the detect command."""
    engine = ReanalysisEngine(
        registry_path=Path(args.registry_file) if args.registry_file else None,
        tasks_path=Path(args.tasks_path) if args.tasks_path else None,
        queue_path=Path(args.queue_file) if args.queue_file else None,
    )

    trigger_type = None
    if args.trigger_type:
        try:
            trigger_type = TriggerType(args.trigger_type)
        except ValueError:
            logger.error(f"Invalid trigger type: {args.trigger_type}")
            return 1

    triggers = engine.detect_triggers(trigger_type)

    if triggers:
        print(f"Detected {len(triggers)} trigger(s):")
        for trigger in triggers:
            print(f"\n  {trigger.trigger_type.value}")
            print(f"    Source: {trigger.source}")
            print(f"    Affected tasks: {', '.join(trigger.affected_tasks) or 'None'}")
            print(f"    Confidence: {trigger.confidence:.2%}")
    else:
        print("No triggers detected.")
        return 4

    # Save triggers to file if requested
    if args.output:
        output_data = {"triggers": [t.to_dict() for t in triggers]}
        with open(args.output, "w") as f:
            yaml.dump(output_data, f, default_flow_style=False)
        print(f"\nTriggers saved to {args.output}")

    return 0


def cmd_apply(args: argparse.Namespace) -> int:
    """Execute the apply command."""
    engine = ReanalysisEngine(
        registry_path=Path(args.registry_file) if args.registry_file else None,
        tasks_path=Path(args.tasks_path) if args.tasks_path else None,
        queue_path=Path(args.queue_file) if args.queue_file else None,
        dry_run=args.dry_run,
    )

    # Load triggers from file or detect
    triggers = []
    if args.triggers_file:
        with open(args.triggers_file, "r") as f:
            data = yaml.safe_load(f)
            for t_data in data.get("triggers", []):
                triggers.append(Trigger(
                    trigger_type=TriggerType(t_data["trigger_type"]),
                    source=t_data["source"],
                    detected_at=datetime.fromisoformat(t_data["detected_at"]),
                    metadata=t_data.get("metadata", {}),
                    affected_tasks=t_data.get("affected_tasks", []),
                    confidence=t_data.get("confidence", 1.0),
                ))
    else:
        triggers = engine.detect_triggers()

    if not triggers:
        print("No triggers to apply.")
        return 4

    # Apply actions
    actions = engine.apply_actions(triggers)

    print(f"Applied {len(actions)} action(s):")
    for action in actions:
        print(f"  {action.action_type.value}: {action.task_id}")

    # Update queue
    engine.update_queue(actions)

    if args.dry_run:
        print("\n[DRY RUN] No changes were actually made.")

    return 0


def cmd_status(args: argparse.Namespace) -> int:
    """Execute the status command."""
    engine = ReanalysisEngine(
        registry_path=Path(args.registry_file) if args.registry_file else None,
        tasks_path=Path(args.tasks_path) if args.tasks_path else None,
        queue_path=Path(args.queue_file) if args.queue_file else None,
    )

    status = engine.get_status(args.task_id)

    if args.output:
        with open(args.output, "w") as f:
            yaml.dump(status, f, default_flow_style=False)
        print(f"Status saved to {args.output}")
    else:
        print(yaml.dump(status, default_flow_style=False))

    return 0


def cmd_git_hook(args: argparse.Namespace) -> int:
    """Execute git hook integration."""
    engine = ReanalysisEngine(
        registry_path=Path(args.registry_file) if args.registry_file else None,
    )

    hook_type = args.hook_type or "post-commit"

    # Map hook types to trigger types
    hook_trigger_map = {
        "post-commit": [TriggerType.STRUCTURAL_CHANGE, TriggerType.DEPENDENCY_COMPLETE],
        "post-merge": [TriggerType.STRUCTURAL_CHANGE, TriggerType.FAILURE_PATTERN],
    }

    trigger_types = hook_trigger_map.get(hook_type, [TriggerType.STRUCTURAL_CHANGE])

    all_triggers = []
    for trigger_type in trigger_types:
        triggers = engine.detect_triggers(trigger_type)
        all_triggers.extend(triggers)

    if all_triggers:
        actions = engine.apply_actions(all_triggers)
        engine.update_queue(actions)

        print(f"Git hook '{hook_type}' processed {len(all_triggers)} trigger(s), {len(actions)} action(s)")
    else:
        print(f"Git hook '{hook_type}': No triggers detected")

    return 0


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="BB5 Reanalysis Engine - Task reanalysis and priority management",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  bb5-reanalysis-engine.py detect
  bb5-reanalysis-engine.py detect --trigger-type structural_change
  bb5-reanalysis-engine.py apply --dry-run
  bb5-reanalysis-engine.py status --task-id TASK-001
  bb5-reanalysis-engine.py git-hook --hook-type post-commit
        """,
    )

    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose logging",
    )
    parser.add_argument(
        "--registry-file",
        help="Path to reanalysis registry YAML file",
    )
    parser.add_argument(
        "--queue-file",
        help="Path to queue YAML file",
    )
    parser.add_argument(
        "--tasks-path",
        help="Path to tasks directory",
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Detect command
    detect_parser = subparsers.add_parser(
        "detect",
        help="Detect trigger conditions",
    )
    detect_parser.add_argument(
        "--trigger-type",
        choices=[t.value for t in TriggerType],
        help="Specific trigger type to detect",
    )
    detect_parser.add_argument(
        "--output", "-o",
        help="Output file for detected triggers",
    )
    detect_parser.set_defaults(func=cmd_detect)

    # Apply command
    apply_parser = subparsers.add_parser(
        "apply",
        help="Apply actions to affected tasks",
    )
    apply_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without making changes",
    )
    apply_parser.add_argument(
        "--triggers-file",
        help="Load triggers from file instead of detecting",
    )
    apply_parser.set_defaults(func=cmd_apply)

    # Status command
    status_parser = subparsers.add_parser(
        "status",
        help="Show status of tasks and triggers",
    )
    status_parser.add_argument(
        "--task-id",
        help="Show detailed status for specific task",
    )
    status_parser.add_argument(
        "--output", "-o",
        help="Output file for status",
    )
    status_parser.set_defaults(func=cmd_status)

    # Git hook command
    hook_parser = subparsers.add_parser(
        "git-hook",
        help="Git hook integration",
    )
    hook_parser.add_argument(
        "--hook-type",
        choices=["post-commit", "post-merge"],
        help="Type of git hook",
    )
    hook_parser.set_defaults(func=cmd_git_hook)

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    if not args.command:
        parser.print_help()
        return 1

    try:
        return args.func(args)
    except Exception as e:
        logger.error(f"Command failed: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
