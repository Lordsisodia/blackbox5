"""
Operation Tracker - Track operation lifecycle and multi-agent coordination
"""

import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
from enum import Enum

logger = logging.getLogger(__name__)


class OperationStatus(Enum):
    """Status of an operation."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class OperationTracker:
    """
    Tracks operation lifecycle across multiple agents.

    Provides status broadcasting and history persistence.
    """

    def __init__(self):
        self._operations: Dict[str, Dict[str, Any]] = {}
        self._history: List[Dict[str, Any]] = []

    def start_operation(self, operation_id: str, agent: str, description: str) -> Dict[str, Any]:
        """Start tracking an operation."""
        operation = {
            "id": operation_id,
            "agent": agent,
            "description": description,
            "status": OperationStatus.RUNNING,
            "started_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        self._operations[operation_id] = operation
        logger.info(f"Started operation: {operation_id}")
        return operation

    def update_operation(self, operation_id: str, status: OperationStatus, **kwargs):
        """Update operation status."""
        if operation_id not in self._operations:
            logger.warning(f"Operation {operation_id} not found")
            return

        self._operations[operation_id].update({
            "status": status,
            "updated_at": datetime.now().isoformat(),
            **kwargs
        })

        if status in [OperationStatus.COMPLETED, OperationStatus.FAILED, OperationStatus.CANCELLED]:
            self._history.append(self._operations.pop(operation_id))

    def get_operation(self, operation_id: str) -> Optional[Dict[str, Any]]:
        """Get operation by ID."""
        return self._operations.get(operation_id)

    def get_active_operations(self) -> List[Dict[str, Any]]:
        """Get all active operations."""
        return list(self._operations.values())

    def get_history(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get operation history."""
        return self._history[-limit:]
