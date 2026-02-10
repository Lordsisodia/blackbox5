"""
Alert Manager - Manages alerts and notifications
"""

import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
from dataclasses import dataclass

from ..core.models import Task

logger = logging.getLogger(__name__)


@dataclass
class Alert:
    """Alert data structure"""
    alert_id: str
    task_id: str
    alert_type: str  # 'stalled', 'overdue', 'failed', 'critical'
    severity: str  # 'info', 'warning', 'error', 'critical'
    message: str
    timestamp: str
    acknowledged: bool = False
    resolved: bool = False


class AlertManager:
    """Manages alerts for task queue events"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.alerts: List[Alert] = []
        self.alert_counter = 0

        monitoring_config = config.get('monitoring', {})
        self.enabled = monitoring_config.get('enabled', True)

    def create_stalled_alert(self, task: Task, threshold_minutes: int) -> Alert:
        """Create an alert for a stalled task"""
        alert_id = f"ALERT-{self.alert_counter}"
        self.alert_counter += 1

        alert = Alert(
            alert_id=alert_id,
            task_id=task.task_id,
            alert_type='stalled',
            severity='warning',
            message=f"Task {task.task_id} has been in-progress for {threshold_minutes}+ minutes",
            timestamp=datetime.now().isoformat()
        )

        self.alerts.append(alert)
        logger.warning(f"Alert created: {alert_id} - {alert.message}")
        return alert

    def create_overdue_alert(self, task: Task) -> Alert:
        """Create an alert for an overdue task"""
        alert_id = f"ALERT-{self.alert_counter}"
        self.alert_counter += 1

        alert = Alert(
            alert_id=alert_id,
            task_id=task.task_id,
            alert_type='overdue',
            severity='error',
            message=f"Task {task.task_id} is overdue (deadline: {task.deadline_at})",
            timestamp=datetime.now().isoformat()
        )

        self.alerts.append(alert)
        logger.error(f"Alert created: {alert_id} - {alert.message}")
        return alert

    def create_failed_alert(self, task: Task, error: str) -> Alert:
        """Create an alert for a failed task"""
        alert_id = f"ALERT-{self.alert_counter}"
        self.alert_counter += 1

        alert = Alert(
            alert_id=alert_id,
            task_id=task.task_id,
            alert_type='failed',
            severity='error' if task.priority.value in ['critical', 'high'] else 'warning',
            message=f"Task {task.task_id} failed: {error}",
            timestamp=datetime.now().isoformat()
        )

        self.alerts.append(alert)
        logger.error(f"Alert created: {alert_id} - {alert.message}")
        return alert

    def create_critical_alert(self, task: Task, reason: str) -> Alert:
        """Create a critical alert"""
        alert_id = f"ALERT-{self.alert_counter}"
        self.alert_counter += 1

        alert = Alert(
            alert_id=alert_id,
            task_id=task.task_id,
            alert_type='critical',
            severity='critical',
            message=f"CRITICAL: Task {task.task_id} - {reason}",
            timestamp=datetime.now().isoformat()
        )

        self.alerts.append(alert)
        logger.critical(f"Alert created: {alert_id} - {alert.message}")
        return alert

    def acknowledge_alert(self, alert_id: str) -> bool:
        """Acknowledge an alert"""
        for alert in self.alerts:
            if alert.alert_id == alert_id:
                alert.acknowledged = True
                logger.info(f"Alert {alert_id} acknowledged")
                return True
        return False

    def resolve_alert(self, alert_id: str) -> bool:
        """Resolve an alert"""
        for alert in self.alerts:
            if alert.alert_id == alert_id:
                alert.resolved = True
                logger.info(f"Alert {alert_id} resolved")
                return True
        return False

    def get_active_alerts(self) -> List[Alert]:
        """Get all unacknowledged and unresolved alerts"""
        return [a for a in self.alerts if not a.acknowledged and not a.resolved]

    def get_alerts_by_task(self, task_id: str) -> List[Alert]:
        """Get all alerts for a specific task"""
        return [a for a in self.alerts if a.task_id == task_id]

    def get_alerts_by_severity(self, severity: str) -> List[Alert]:
        """Get all alerts of a specific severity"""
        return [a for a in self.alerts if a.severity == severity]

    def get_summary(self) -> Dict[str, Any]:
        """Get alert summary"""
        active = self.get_active_alerts()
        return {
            'total_alerts': len(self.alerts),
            'active_alerts': len(active),
            'acknowledged': len([a for a in self.alerts if a.acknowledged]),
            'resolved': len([a for a in self.alerts if a.resolved]),
            'by_severity': {
                'critical': len([a for a in active if a.severity == 'critical']),
                'error': len([a for a in active if a.severity == 'error']),
                'warning': len([a for a in active if a.severity == 'warning']),
                'info': len([a for a in active if a.severity == 'info']),
            },
            'by_type': {
                'stalled': len([a for a in active if a.alert_type == 'stalled']),
                'overdue': len([a for a in active if a.alert_type == 'overdue']),
                'failed': len([a for a in active if a.alert_type == 'failed']),
                'critical': len([a for a in active if a.alert_type == 'critical']),
            }
        }

    def clear_old_alerts(self, hours_old: int = 24):
        """Clear old resolved alerts"""
        cutoff = datetime.now().timestamp() - (hours_old * 3600)
        self.alerts = [
            a for a in self.alerts
            if not a.resolved or datetime.fromisoformat(a.timestamp).timestamp() > cutoff
        ]
        logger.info(f"Cleared old alerts (older than {hours_old}h)")
