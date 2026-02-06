"""Health calculators for BB5 Health Monitor."""

import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any, Tuple

from .models import Task, Agent, Event, StuckTask, HealthStatus
from .utils import format_duration

logger = logging.getLogger(__name__)


def calculate_throughput(tasks: List[Task], days: int = 7) -> float:
    """Calculate tasks completed per day over the given period."""
    cutoff = datetime.now() - timedelta(days=days)
    completed = [
        t for t in tasks
        if t.is_completed and t.completed_at and t.completed_at > cutoff
    ]
    return len(completed) / days if days > 0 else 0


def calculate_queue_health(tasks: List[Task]) -> Tuple[float, str]:
    """Calculate queue health score (0-100) and status."""
    if not tasks:
        return 100.0, "healthy"

    pending = sum(1 for t in tasks if t.is_pending)
    in_progress = sum(1 for t in tasks if t.is_in_progress)
    completed = sum(1 for t in tasks if t.is_completed)
    total = len(tasks)

    if total == 0:
        return 100.0, "healthy"

    # Score based on completion ratio and pending backlog
    completion_ratio = completed / total

    # Penalize large pending backlog
    pending_penalty = min(30, pending * 0.5)

    score = max(0, (completion_ratio * 100) - pending_penalty)

    if score >= 80:
        return score, "healthy"
    elif score >= 60:
        return score, "warning"
    return score, "critical"


def calculate_agent_health(agents: List[Agent], timeout_seconds: int = 120) -> Tuple[float, str]:
    """Calculate agent health score (0-100) and status."""
    if not agents:
        return 0.0, "critical"

    online = sum(1 for a in agents if a.is_online(timeout_seconds))
    stale = sum(1 for a in agents if a.is_stale(timeout_seconds) and not a.seconds_since_seen() > timeout_seconds * 2)
    offline = len(agents) - online - stale

    # Score: online = 100, stale = 50, offline = 0
    score = ((online * 100) + (stale * 50)) / len(agents)

    if offline > 0:
        return score, "critical"
    elif stale > 0:
        return score, "warning"
    return score, "healthy"


def detect_stuck_tasks(tasks: List[Task], events: List[Event], multiplier: float = 2.0) -> List[StuckTask]:
    """Detect tasks that appear stuck based on elapsed time vs estimate."""
    stuck = []

    for task in tasks:
        if not task.is_in_progress or not task.started_at:
            continue

        elapsed = task.elapsed_minutes()
        if not elapsed:
            continue

        threshold = task.estimated_minutes * multiplier

        if elapsed > threshold:
            # Find last event for this task
            task_events = [e for e in events if e.task_id == task.id]
            last_event = max(task_events, key=lambda e: e.timestamp) if task_events else None

            if last_event:
                time_since_event = datetime.now() - last_event.timestamp
                if time_since_event.total_seconds() > 3600:  # No activity for 1 hour
                    stuck.append(StuckTask(
                        task=task,
                        reason=f">{multiplier}x estimate, no activity for {format_duration(int(time_since_event.total_seconds()))}",
                        stuck_duration=format_duration(int((datetime.now() - task.started_at).total_seconds())),
                        stuck_minutes=elapsed,
                    ))
            else:
                # No events at all for this task
                stuck.append(StuckTask(
                    task=task,
                    reason=f">{multiplier}x estimate, no events recorded",
                    stuck_duration=format_duration(int((datetime.now() - task.started_at).total_seconds())),
                    stuck_minutes=elapsed,
                ))

    return stuck


def calculate_health_score(
    tasks: List[Task],
    agents: List[Agent],
    events: List[Event],
    metrics: Dict[str, Any],
    timeout_seconds: int = 120
) -> Tuple[int, HealthStatus, Dict[str, Any]]:
    """Calculate overall health score (0-100) and status.

    Weights:
    - throughput: 25% (tasks/day vs target)
    - quality: 25% (success rate from metrics)
    - efficiency: 20% (time saved from metrics)
    - reliability: 15% (agent uptime)
    - queue_health: 15% (queue status)
    """
    # Get component scores
    throughput = calculate_throughput(tasks)
    queue_score, queue_status = calculate_queue_health(tasks)
    agent_score, agent_status = calculate_agent_health(agents, timeout_seconds)

    # Extract metrics from dashboard data
    dashboard_metrics = metrics.get('metrics', {})

    # Quality: success rate (default to 100 if not available)
    quality_score = dashboard_metrics.get('quality', {}).get('value', 100)

    # Efficiency: time saved metric
    efficiency_score = dashboard_metrics.get('efficiency', {}).get('value', 100)

    # Normalize throughput (target: 5 tasks/day = 100%)
    throughput_score = min(100, (throughput / 5) * 100)

    # Calculate weighted score
    score = int(
        (throughput_score * 0.25) +
        (quality_score * 0.25) +
        (efficiency_score * 0.20) +
        (agent_score * 0.15) +
        (queue_score * 0.15)
    )

    # Determine status
    if agent_status == "critical" or score < 40:
        status = HealthStatus.CRITICAL
    elif score < 60 or queue_status == "critical":
        status = HealthStatus.WARNING
    else:
        status = HealthStatus.HEALTHY

    details = {
        'throughput': {
            'score': throughput_score,
            'value': throughput,
            'target': 5,
            'weight': 0.25,
        },
        'quality': {
            'score': quality_score,
            'weight': 0.25,
        },
        'efficiency': {
            'score': efficiency_score,
            'weight': 0.20,
        },
        'reliability': {
            'score': agent_score,
            'status': agent_status,
            'weight': 0.15,
        },
        'queue': {
            'score': queue_score,
            'status': queue_status,
            'weight': 0.15,
        },
    }

    return score, status, details
