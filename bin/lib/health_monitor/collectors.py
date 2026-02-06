"""Data collectors for BB5 Health Monitor."""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional

import yaml

from .config import get_config
from .models import Task, Agent, Event, TaskStatus, Metric
from .utils import parse_timestamp

logger = logging.getLogger(__name__)


def _safe_read_yaml(path: Path) -> Optional[Dict[str, Any]]:
    """Safely read a YAML file, returning None on error."""
    if not path.exists():
        logger.debug(f"File not found: {path}")
        return None
    try:
        with open(path, 'r') as f:
            return yaml.safe_load(f) or {}
    except Exception as e:
        logger.error(f"Error reading {path}: {e}")
        return None


def _safe_read_json(path: Path) -> Optional[Dict[str, Any]]:
    """Safely read a JSON file, returning None on error."""
    if not path.exists():
        logger.debug(f"File not found: {path}")
        return None
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error reading {path}: {e}")
        return None


def collect_queue() -> List[Task]:
    """Collect tasks from queue.yaml."""
    config = get_config()
    data = _safe_read_yaml(config.queue_path)

    if not data:
        return []

    tasks = []
    for item in data.get('tasks', []):
        try:
            task = Task(
                id=item.get('id', 'unknown'),
                title=item.get('title', 'Untitled'),
                status=TaskStatus(item.get('status', 'pending')),
                priority=item.get('priority', 'medium'),
                estimated_minutes=item.get('estimated_minutes', 60),
                created_at=parse_timestamp(item.get('created_at')) or datetime.now(),
                updated_at=parse_timestamp(item.get('updated_at')),
                started_at=parse_timestamp(item.get('started_at')),
                completed_at=parse_timestamp(item.get('completed_at')),
                agent=item.get('agent'),
                blocked_by=item.get('blocked_by', []),
                tags=item.get('tags', []),
            )
            tasks.append(task)
        except Exception as e:
            logger.warning(f"Error parsing task {item.get('id')}: {e}")

    return tasks


def collect_heartbeat() -> List[Agent]:
    """Collect agent heartbeats from heartbeat.yaml."""
    config = get_config()
    data = _safe_read_yaml(config.heartbeat_path)

    if not data:
        return []

    agents = []
    for name, info in data.get('agents', {}).items():
        try:
            agent = Agent(
                name=name,
                last_seen=parse_timestamp(info.get('last_seen')) or datetime.now(),
                status=info.get('status', 'unknown'),
                loop_number=info.get('loop_number', 0),
                current_task=info.get('current_task'),
                version=info.get('version'),
            )
            agents.append(agent)
        except Exception as e:
            logger.warning(f"Error parsing agent {name}: {e}")

    return agents


def collect_events(limit: int = 100) -> List[Event]:
    """Collect events from events.yaml."""
    config = get_config()
    data = _safe_read_yaml(config.events_path)

    if not data:
        return []

    events = []
    for item in data.get('events', [])[-limit:]:
        try:
            event = Event(
                timestamp=parse_timestamp(item.get('timestamp')) or datetime.now(),
                event_type=item.get('type', 'unknown'),
                task_id=item.get('task_id'),
                agent=item.get('agent'),
                message=item.get('message'),
                data=item.get('data', {}),
            )
            events.append(event)
        except Exception as e:
            logger.warning(f"Error parsing event: {e}")

    return events


def collect_metrics() -> Dict[str, Any]:
    """Collect metrics from metrics-dashboard.yaml."""
    config = get_config()
    data = _safe_read_yaml(config.metrics_path)
    return data or {}


def collect_skills() -> Dict[str, Any]:
    """Collect skills from skill-registry.yaml."""
    config = get_config()
    data = _safe_read_yaml(config.skills_path)
    return data or {}


def collect_run_metrics() -> List[Dict[str, Any]]:
    """Collect metrics from run directories."""
    config = get_config()
    metrics = []

    if not config.runs_dir.exists():
        return metrics

    for run_dir in config.runs_dir.iterdir():
        if not run_dir.is_dir():
            continue

        metrics_file = run_dir / 'metrics.json'
        if metrics_file.exists():
            data = _safe_read_json(metrics_file)
            if data:
                data['run_id'] = run_dir.name
                metrics.append(data)

    return metrics


def collect_all() -> Dict[str, Any]:
    """Collect all health data sources."""
    return {
        'tasks': collect_queue(),
        'agents': collect_heartbeat(),
        'events': collect_events(),
        'metrics': collect_metrics(),
        'skills': collect_skills(),
        'run_metrics': collect_run_metrics(),
        'timestamp': datetime.now().isoformat(),
    }
