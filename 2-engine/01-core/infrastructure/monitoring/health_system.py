"""
Health System - Component health checks and dependency verification
"""

import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
from enum import Enum

logger = logging.getLogger(__name__)


class HealthStatus(Enum):
    """Health status."""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"


class HealthSystem:
    """
    Monitors component health and verifies dependencies.

    Provides alert generation and resource monitoring.
    """

    def __init__(self):
        self._components: Dict[str, Dict[str, Any]] = {}
        self._alerts: List[Dict[str, Any]] = []

    def register_component(self, name: str, check_func=None):
        """Register a component for health checking."""
        self._components[name] = {
            "name": name,
            "status": HealthStatus.UNKNOWN,
            "check_func": check_func,
            "last_check": None
        }

    def check_health(self, component_name: str) -> HealthStatus:
        """Check health of a specific component."""
        if component_name not in self._components:
            logger.warning(f"Component {component_name} not registered")
            return HealthStatus.UNKNOWN

        component = self._components[component_name]
        if component["check_func"]:
            try:
                is_healthy = component["check_func"]()
                component["status"] = HealthStatus.HEALTHY if is_healthy else HealthStatus.UNHEALTHY
            except Exception as e:
                logger.error(f"Health check failed for {component_name}: {e}")
                component["status"] = HealthStatus.UNHEALTHY

        component["last_check"] = datetime.now().isoformat()
        return component["status"]

    def check_all(self) -> Dict[str, HealthStatus]:
        """Check health of all components."""
        results = {}
        for name in self._components:
            results[name] = self.check_health(name)
        return results

    def get_alerts(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get recent alerts."""
        return self._alerts[-limit:]

    def create_alert(self, component: str, severity: str, message: str):
        """Create a health alert."""
        alert = {
            "component": component,
            "severity": severity,
            "message": message,
            "created_at": datetime.now().isoformat()
        }
        self._alerts.append(alert)
        logger.warning(f"Alert: {component} - {message}")
