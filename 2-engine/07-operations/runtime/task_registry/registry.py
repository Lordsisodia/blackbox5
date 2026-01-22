"""Task Registry - Single source of truth for task execution tracking."""

import json
from pathlib import Path
from datetime import datetime
from typing import Optional, Union, List

from .models import Task, TaskState, TaskPriority, TaskRegistry


class TaskRegistryManager:
    """Manages the task registry file."""

    def __init__(self, registry_path: Union[str, Path] = "data/task_registry.json"):
        self.registry_path = Path(registry_path)
        self.registry_path.parent.mkdir(parents=True, exist_ok=True)
        self._registry: Optional[TaskRegistry] = None
    
    def load(self) -> TaskRegistry:
        """Load the task registry from disk."""
        if not self.registry_path.exists():
            # Create new empty registry
            self._registry = TaskRegistry()
            self.save()
            return self._registry
        
        with open(self.registry_path, "r") as f:
            data = json.load(f)
        
        # Parse tasks
        tasks = {}
        for task_id, task_data in data.get("tasks", {}).items():
            tasks[task_id] = Task.from_dict(task_data)
        
        self._registry = TaskRegistry(
            version=data.get("version", "1.0"),
            last_updated=datetime.fromisoformat(data["last_updated"]),
            tasks=tasks,
        )
        
        return self._registry
    
    @property
    def registry(self) -> TaskRegistry:
        """Get the registry, loading if necessary."""
        if self._registry is None:
            self._registry = self.load()
        return self._registry
    
    def save(self):
        """Save the task registry to disk."""
        if self._registry is None:
            raise ValueError("No registry to save")
        
        self._registry.last_updated = datetime.utcnow()
        
        with open(self.registry_path, "w") as f:
            json.dump(self._registry.to_dict(), f, indent=2)
    
    def get_task(self, task_id: str) -> Optional[Task]:
        """Get a task by ID."""
        return self.registry.get_task(task_id)
    
    def list_tasks(
        self,
        state: Optional[TaskState] = None,
        objective: Optional[str] = None,
        assignee: Optional[str] = None,
    ) -> List[Task]:
        """List tasks with optional filters."""
        return self.registry.list_tasks(state=state, objective=objective, assignee=assignee)
    
    def create_task(
        self,
        task_id: str,
        title: str,
        description: str,
        objective: str,
        phase: Optional[str] = None,
        dependencies: Optional[List[str]] = None,
        blocks: Optional[List[str]] = None,
        priority: Union[str, TaskPriority] = "medium",
        tags: Optional[List[str]] = None,
    ) -> Task:
        """Create a new task."""
        if dependencies is None:
            dependencies = []
        if blocks is None:
            blocks = []
        if tags is None:
            tags = []

        # Convert priority string to TaskPriority enum if needed
        if isinstance(priority, str):
            priority = TaskPriority(priority)

        task = Task(
            id=task_id,
            title=title,
            description=description,
            objective=objective,
            phase=phase,
            dependencies=dependencies,
            blocks=blocks,
            priority=priority,
            tags=tags,
        )
        
        self.registry.tasks[task_id] = task
        self.save()
        
        return task
    
    def update_task(self, task_id: str, **updates) -> Optional[Task]:
        """Update a task."""
        task = self.registry.get_task(task_id)
        if not task:
            return None
        
        for key, value in updates.items():
            if hasattr(task, key):
                # Convert string to TaskState if needed
                if key == "state" and isinstance(value, str):
                    value = TaskState(value)
                setattr(task, key, value)
        
        task.updated_at = datetime.utcnow()
        self.save()
        
        return task
    
    def delete_task(self, task_id: str) -> bool:
        """Delete a task."""
        if task_id in self.registry.tasks:
            del self.registry.tasks[task_id]
            self.save()
            return True
        return False
    
    def get_available_tasks(self) -> List[Task]:
        """Get tasks that are ready to be assigned."""
        return self.registry.get_available_tasks()
    
    def get_statistics(self):
        """Get task statistics."""
        return self.registry.calculate_statistics()
