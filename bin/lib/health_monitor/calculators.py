"""Health calculators for BB5 Health Monitor."""

import logging
import re
import subprocess
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Any, Tuple

from .models import Task, Agent, Event, StuckTask, HealthStatus
from .utils import format_duration, get_bb5_root

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


def calculate_commit_compliance(days: int = 30, threshold: float = 75.0) -> Dict[str, Any]:
    """Calculate commit compliance for completed tasks.

    Returns compliance metrics showing what percentage of completed tasks
    have associated git commits with task ID references.
    """
    bb5_root = get_bb5_root()
    completed_tasks_dir = bb5_root / "5-project-memory/blackbox5/tasks/completed"

    # Get commits with task references
    since_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")

    try:
        result = subprocess.run(
            ["git", "log", "--all", f"--since={since_date}",
             "--pretty=format:%s", "--grep=TASK-"],
            capture_output=True,
            text=True,
            check=True
        )
        commit_messages = result.stdout
    except subprocess.CalledProcessError:
        commit_messages = ""

    # Extract task IDs from commits
    task_pattern = re.compile(r'TASK-[A-Z0-9-]+')
    committed_task_ids = set(task_pattern.findall(commit_messages))

    # Get completed tasks from filesystem
    completed_tasks = []
    if completed_tasks_dir.exists():
        for path in completed_tasks_dir.rglob("TASK-*"):
            if path.is_dir():
                completed_tasks.append(path.name)

    # Categorize tasks
    tasks_with_commits = []
    tasks_without_commits = []

    category_stats = defaultdict(lambda: {'total': 0, 'with_commits': 0})

    for task_id in completed_tasks:
        # Find task directory and read metadata
        task_dir = None
        for path in completed_tasks_dir.rglob(task_id):
            if path.is_dir():
                task_dir = path
                break

        # Default metadata
        category = 'uncategorized'
        priority = 'medium'

        if task_dir and (task_dir / 'task.md').exists():
            try:
                content = (task_dir / 'task.md').read_text()
                cat_match = re.search(r'\*\*Category:\*\*\s*(\S+)', content)
                if cat_match:
                    category = cat_match.group(1).strip()
                pri_match = re.search(r'\*\*Priority:\*\*\s*(\S+)', content)
                if pri_match:
                    priority = pri_match.group(1).strip()
            except Exception:
                pass

        has_commit = task_id in committed_task_ids

        task_info = {
            'id': task_id,
            'category': category,
            'priority': priority,
        }

        if has_commit:
            tasks_with_commits.append(task_info)
            category_stats[category]['with_commits'] += 1
        else:
            tasks_without_commits.append(task_info)

        category_stats[category]['total'] += 1

    # Calculate compliance
    total_tasks = len(tasks_with_commits) + len(tasks_without_commits)
    compliance_rate = (len(tasks_with_commits) / total_tasks * 100) if total_tasks > 0 else 0

    return {
        'total_tasks': total_tasks,
        'with_commits': len(tasks_with_commits),
        'without_commits': len(tasks_without_commits),
        'compliance_rate': round(compliance_rate, 1),
        'threshold': threshold,
        'meets_threshold': compliance_rate >= threshold,
        'by_category': {
            cat: {
                'total': stats['total'],
                'with_commits': stats['with_commits'],
                'rate': round(stats['with_commits'] / stats['total'] * 100, 1) if stats['total'] > 0 else 0
            }
            for cat, stats in category_stats.items()
        },
        'tasks_without_commits': tasks_without_commits[:10]  # Limit to first 10
    }
