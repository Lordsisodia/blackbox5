"""State machine for task lifecycle management."""

from datetime import datetime
from typing import Tuple, Optional, List, Union

from .models import Task, TaskState
from .registry import TaskRegistryManager


class StateTransitionError(Exception):
    """Raised when an invalid state transition is attempted."""
    
    def __init__(self, task_id: str, current_state: TaskState, desired_state: TaskState, reason: str):
        self.task_id = task_id
        self.current_state = current_state
        self.desired_state = desired_state
        self.reason = reason
        super().__init__(f"Cannot transition {task_id} from {current_state.value} to {desired_state.value}: {reason}")


class TaskStateMachine:
    """Manages task state transitions and validation."""
    
    # Valid state transitions
    VALID_TRANSITIONS = {
        TaskState.BACKLOG: [TaskState.ASSIGNED, TaskState.FAILED],
        TaskState.ASSIGNED: [TaskState.ACTIVE, TaskState.BACKLOG, TaskState.FAILED],
        TaskState.ACTIVE: [TaskState.DONE, TaskState.FAILED],
        TaskState.DONE: [],  # Terminal state
        TaskState.FAILED: [TaskState.BACKLOG],  # Can retry
    }
    
    def __init__(self, registry_manager: TaskRegistryManager):
        self.registry = registry_manager
    
    def can_transition(self, task: Task, new_state: TaskState) -> Tuple[bool, Optional[str]]:
        """Check if a state transition is valid.
        
        Returns:
            (can_transition, reason_if_not)
        """
        # Check if transition is valid
        valid_next_states = self.VALID_TRANSITIONS.get(task.state, [])
        if new_state not in valid_next_states:
            return False, f"Cannot transition from {task.state.value} to {new_state.value}"
        
        # State-specific validation
        if new_state == TaskState.ASSIGNED:
            can_assign, reason = task.can_assign()
            if not can_assign:
                return False, reason
            
            # Check dependencies
            deps_met, dep_reason = self._check_dependencies(task)
            if not deps_met:
                return False, dep_reason
        
        if new_state == TaskState.ACTIVE:
            can_start, reason = task.can_start()
            if not can_start:
                return False, reason
        
        if new_state == TaskState.DONE:
            can_complete, reason = task.can_complete()
            if not can_complete:
                return False, reason
        
        return True, None
    
    def transition(
        self,
        task_id: str,
        new_state: TaskState,
        assignee: Optional[str] = None,
        failure_reason: Optional[str] = None,
    ) -> Task:
        """Transition a task to a new state.
        
        Args:
            task_id: ID of the task to transition
            new_state: The desired new state
            assignee: Agent name (required when transitioning to ASSIGNED)
            failure_reason: Reason for failure (required when transitioning to FAILED)
        
        Returns:
            The updated task
        
        Raises:
            StateTransitionError: If the transition is invalid
        """
        task = self.registry.get_task(task_id)
        if not task:
            raise ValueError(f"Task {task_id} not found")
        
        # Validate transition
        can_transition, reason = self.can_transition(task, new_state)
        if not can_transition:
            raise StateTransitionError(task_id, task.state, new_state, reason or "Unknown reason")
        
        # Apply transition
        updates: dict = {"state": new_state}
        
        if new_state == TaskState.ASSIGNED:
            if not assignee:
                raise StateTransitionError(task_id, task.state, new_state, "assignee is required")
            updates["assignee"] = assignee
            updates["assigned_at"] = datetime.utcnow()
        
        if new_state == TaskState.ACTIVE:
            updates["started_at"] = datetime.utcnow()
        
        if new_state == TaskState.DONE:
            updates["completed_at"] = datetime.utcnow()
            # Clear assignee - task is complete
            updates["assignee"] = None
        
        if new_state == TaskState.BACKLOG:
            # Reset fields when going back to backlog
            updates["assignee"] = None
            updates["assigned_at"] = None
            updates["started_at"] = None
            updates["completed_at"] = None
        
        if new_state == TaskState.FAILED:
            if not failure_reason:
                raise StateTransitionError(task_id, task.state, new_state, "failure_reason is required")
            # Add failure reason to tags for tracking
            updates["tags"] = task.tags + [f"failed: {failure_reason}"]
            updates["assignee"] = None
        
        # Update task
        updated_task = self.registry.update_task(task_id, **updates)
        
        # Propagate state to dependent tasks
        self._propagate_state(updated_task)
        
        return updated_task
    
    def _check_dependencies(self, task: Task) -> Tuple[bool, Optional[str]]:
        """Check if all dependencies are met."""
        for dep_id in task.dependencies:
            dep_task = self.registry.get_task(dep_id)
            if not dep_task:
                return False, f"Dependency {dep_id} not found"
            if dep_task.state != TaskState.DONE:
                return False, f"Dependency {dep_id} is {dep_task.state.value}, not DONE"
        return True, None
    
    def _propagate_state(self, task: Task):
        """Propagate state changes to dependent tasks.
        
        When a task completes, check if any tasks that depend on it
        can now be assigned (all their dependencies are done).
        """
        if task.state != TaskState.DONE:
            return
        
        # Find tasks that depend on this one
        for other_task in self.registry.list_tasks():
            if task.id in other_task.dependencies:
                # Check if all dependencies are now met
                all_deps_done = True
                for dep_id in other_task.dependencies:
                    dep_task = self.registry.get_task(dep_id)
                    if not dep_task or dep_task.state != TaskState.DONE:
                        all_deps_done = False
                        break
                
                # If all dependencies are done and task is in backlog, make it assignable
                if all_deps_done and other_task.state == TaskState.BACKLOG:
                    # Note: We don't auto-assign, just mark as ready
                    # The agent still needs to explicitly take the task
                    pass
    
    def get_blocking_tasks(self, task_id: str) -> List[Task]:
        """Get tasks that are blocking this task."""
        task = self.registry.get_task(task_id)
        if not task:
            return []
        
        blocking = []
        for dep_id in task.dependencies:
            dep_task = self.registry.get_task(dep_id)
            if dep_task and dep_task.state != TaskState.DONE:
                blocking.append(dep_task)
        
        return blocking
    
    def get_blocked_tasks(self, task_id: str) -> List[Task]:
        """Get tasks that are blocked by this task."""
        blocking = []
        for task in self.registry.list_tasks():
            if task_id in task.dependencies and task.state != TaskState.DONE:
                blocking.append(task)
        return blocking
