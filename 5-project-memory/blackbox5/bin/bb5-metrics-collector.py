#!/usr/bin/env python3
"""
BB5 Metrics Collector

Tracks task execution metrics in real-time, calculates time saved vs manual execution,
measures estimate accuracy, and maintains the metrics dashboard.

Usage:
    bb5-metrics-collector.py collect --task-id TASK-001 --event start
    bb5-metrics-collector.py collect --task-id TASK-001 --event complete --duration 45
    bb5-metrics-collector.py report --period weekly
    bb5-metrics-collector.py dashboard --update
"""

import argparse
import json
import logging
import os
import sys
import time
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
import yaml

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('bb5-metrics')


class EventType(Enum):
    """Task event types."""
    START = "start"
    COMPLETE = "complete"
    FAIL = "fail"
    PAUSE = "pause"
    RESUME = "resume"


class TaskStatus(Enum):
    """Task status values."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    PAUSED = "paused"


@dataclass
class TaskEvent:
    """Represents a single task event."""
    task_id: str
    event_type: EventType
    timestamp: datetime
    duration_minutes: Optional[int] = None
    estimated_minutes: Optional[int] = None
    manual_estimate_minutes: Optional[int] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            'task_id': self.task_id,
            'event_type': self.event_type.value,
            'timestamp': self.timestamp.isoformat(),
            'duration_minutes': self.duration_minutes,
            'estimated_minutes': self.estimated_minutes,
            'manual_estimate_minutes': self.manual_estimate_minutes,
            'metadata': self.metadata
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TaskEvent':
        return cls(
            task_id=data['task_id'],
            event_type=EventType(data['event_type']),
            timestamp=datetime.fromisoformat(data['timestamp']),
            duration_minutes=data.get('duration_minutes'),
            estimated_minutes=data.get('estimated_minutes'),
            manual_estimate_minutes=data.get('manual_estimate_minutes'),
            metadata=data.get('metadata', {})
        )


@dataclass
class TaskMetrics:
    """Aggregated metrics for a single task."""
    task_id: str
    status: TaskStatus
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    duration_minutes: Optional[int] = None
    estimated_minutes: Optional[int] = None
    manual_estimate_minutes: Optional[int] = None
    events: List[TaskEvent] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            'task_id': self.task_id,
            'status': self.status.value,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'duration_minutes': self.duration_minutes,
            'estimated_minutes': self.estimated_minutes,
            'manual_estimate_minutes': self.manual_estimate_minutes,
            'events': [e.to_dict() for e in self.events]
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TaskMetrics':
        return cls(
            task_id=data['task_id'],
            status=TaskStatus(data['status']),
            started_at=datetime.fromisoformat(data['started_at']) if data.get('started_at') else None,
            completed_at=datetime.fromisoformat(data['completed_at']) if data.get('completed_at') else None,
            duration_minutes=data.get('duration_minutes'),
            estimated_minutes=data.get('estimated_minutes'),
            manual_estimate_minutes=data.get('manual_estimate_minutes'),
            events=[TaskEvent.from_dict(e) for e in data.get('events', [])]
        )


@dataclass
class PeriodMetrics:
    """Metrics aggregated over a time period."""
    period_start: datetime
    period_end: datetime
    total_tasks: int = 0
    completed_tasks: int = 0
    failed_tasks: int = 0
    pending_tasks: int = 0
    in_progress_tasks: int = 0
    total_duration_minutes: int = 0
    total_estimated_minutes: int = 0
    total_manual_estimate_minutes: int = 0
    estimate_accuracy: float = 0.0  # 0-100%
    time_saved_minutes: int = 0
    avg_completion_time: float = 0.0
    health_score: float = 0.0  # 0-100

    def to_dict(self) -> Dict[str, Any]:
        return {
            'period_start': self.period_start.isoformat(),
            'period_end': self.period_end.isoformat(),
            'total_tasks': self.total_tasks,
            'completed_tasks': self.completed_tasks,
            'failed_tasks': self.failed_tasks,
            'pending_tasks': self.pending_tasks,
            'in_progress_tasks': self.in_progress_tasks,
            'total_duration_minutes': self.total_duration_minutes,
            'total_estimated_minutes': self.total_estimated_minutes,
            'total_manual_estimate_minutes': self.total_manual_estimate_minutes,
            'estimate_accuracy': round(self.estimate_accuracy, 2),
            'time_saved_minutes': self.time_saved_minutes,
            'avg_completion_time': round(self.avg_completion_time, 2),
            'health_score': round(self.health_score, 2)
        }


class MetricsCollector:
    """Main metrics collection and calculation engine."""

    # Baseline assumptions for manual execution (minutes)
    DEFAULT_MANUAL_MULTIPLIER = 3.0  # Manual takes 3x longer than automated
    MIN_MANUAL_TIME = 15  # Minimum manual time in minutes

    def __init__(self, project_path: Optional[Path] = None):
        self.project_path = project_path or self._find_project_path()
        self.metrics_dir = self.project_path / '.autonomous' / 'metrics'
        self.metrics_dir.mkdir(parents=True, exist_ok=True)

        self.events_file = self.metrics_dir / 'events.jsonl'
        self.tasks_file = self.metrics_dir / 'tasks.json'
        self.baseline_file = self.metrics_dir / 'baseline.yaml'
        self.dashboard_file = self.project_path / '.autonomous' / 'metrics-dashboard.yaml'
        self.execution_state_file = self.project_path / '.autonomous' / 'execution-state.yaml'

        self._tasks: Dict[str, TaskMetrics] = {}
        self._load_tasks()

    def _find_project_path(self) -> Path:
        """Find the BlackBox5 project path."""
        # Check environment variable first
        if 'BB5_PROJECT_PATH' in os.environ:
            return Path(os.environ['BB5_PROJECT_PATH'])

        # Look for .autonomous directory in current or parent directories
        current = Path.cwd()
        for path in [current] + list(current.parents):
            if (path / '.autonomous').exists():
                return path

        # Default to blackbox5 project
        default = Path.home() / '.blackbox5' / '5-project-memory' / 'blackbox5'
        if default.exists():
            return default

        raise ValueError("Could not find BlackBox5 project path. Set BB5_PROJECT_PATH environment variable.")

    def _load_tasks(self) -> None:
        """Load existing task metrics from file."""
        if self.tasks_file.exists():
            try:
                with open(self.tasks_file, 'r') as f:
                    data = json.load(f)
                    self._tasks = {
                        k: TaskMetrics.from_dict(v) for k, v in data.items()
                    }
                logger.debug(f"Loaded {len(self._tasks)} tasks from {self.tasks_file}")
            except Exception as e:
                logger.error(f"Error loading tasks: {e}")
                self._tasks = {}

    def _save_tasks(self) -> None:
        """Save task metrics to file."""
        try:
            with open(self.tasks_file, 'w') as f:
                json.dump(
                    {k: v.to_dict() for k, v in self._tasks.items()},
                    f,
                    indent=2
                )
        except Exception as e:
            logger.error(f"Error saving tasks: {e}")

    def _append_event(self, event: TaskEvent) -> None:
        """Append event to events log."""
        try:
            with open(self.events_file, 'a') as f:
                f.write(json.dumps(event.to_dict()) + '\n')
        except Exception as e:
            logger.error(f"Error appending event: {e}")

    def _load_baseline(self) -> Dict[str, Any]:
        """Load baseline metrics."""
        if self.baseline_file.exists():
            try:
                with open(self.baseline_file, 'r') as f:
                    return yaml.safe_load(f) or {}
            except Exception as e:
                logger.error(f"Error loading baseline: {e}")

        # Return default baseline
        return {
            'manual_time_multiplier': self.DEFAULT_MANUAL_MULTIPLIER,
            'min_manual_time_minutes': self.MIN_MANUAL_TIME,
            'established_at': datetime.now().isoformat(),
            'tasks_baseline': {}
        }

    def _save_baseline(self, baseline: Dict[str, Any]) -> None:
        """Save baseline metrics."""
        try:
            with open(self.baseline_file, 'w') as f:
                yaml.dump(baseline, f, default_flow_style=False)
        except Exception as e:
            logger.error(f"Error saving baseline: {e}")

    def record_event(
        self,
        task_id: str,
        event_type: EventType,
        duration_minutes: Optional[int] = None,
        estimated_minutes: Optional[int] = None,
        manual_estimate_minutes: Optional[int] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> TaskMetrics:
        """Record a task event and update metrics."""
        timestamp = datetime.now()

        # Create event
        event = TaskEvent(
            task_id=task_id,
            event_type=event_type,
            timestamp=timestamp,
            duration_minutes=duration_minutes,
            estimated_minutes=estimated_minutes,
            manual_estimate_minutes=manual_estimate_minutes,
            metadata=metadata or {}
        )

        # Append to event log
        self._append_event(event)

        # Update task metrics
        if task_id not in self._tasks:
            self._tasks[task_id] = TaskMetrics(
                task_id=task_id,
                status=TaskStatus.PENDING
            )

        task = self._tasks[task_id]
        task.events.append(event)

        # Update task state based on event
        if event_type == EventType.START:
            task.status = TaskStatus.IN_PROGRESS
            task.started_at = timestamp
            if estimated_minutes:
                task.estimated_minutes = estimated_minutes
            if manual_estimate_minutes:
                task.manual_estimate_minutes = manual_estimate_minutes

        elif event_type == EventType.COMPLETE:
            task.status = TaskStatus.COMPLETED
            task.completed_at = timestamp
            if duration_minutes:
                task.duration_minutes = duration_minutes
            elif task.started_at:
                task.duration_minutes = int((timestamp - task.started_at).total_seconds() / 60)

        elif event_type == EventType.FAIL:
            task.status = TaskStatus.FAILED
            task.completed_at = timestamp

        elif event_type == EventType.PAUSE:
            task.status = TaskStatus.PAUSED

        elif event_type == EventType.RESUME:
            task.status = TaskStatus.IN_PROGRESS

        # Save updated tasks
        self._save_tasks()

        logger.info(f"Recorded {event_type.value} event for task {task_id}")
        return task

    def calculate_manual_estimate(self, estimated_minutes: int, task_type: str = "default") -> int:
        """Calculate estimated manual execution time."""
        baseline = self._load_baseline()
        multiplier = baseline.get('manual_time_multiplier', self.DEFAULT_MANUAL_MULTIPLIER)
        min_time = baseline.get('min_manual_time_minutes', self.MIN_MANUAL_TIME)

        # Check for task-specific baseline
        tasks_baseline = baseline.get('tasks_baseline', {})
        if task_type in tasks_baseline:
            multiplier = tasks_baseline[task_type].get('multiplier', multiplier)
            min_time = tasks_baseline[task_type].get('min_time', min_time)

        manual_estimate = max(int(estimated_minutes * multiplier), min_time)
        return manual_estimate

    def calculate_period_metrics(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> PeriodMetrics:
        """Calculate metrics for a specific time period."""
        if start_date is None:
            start_date = datetime.now() - timedelta(days=7)
        if end_date is None:
            end_date = datetime.now()

        # Filter tasks within period
        period_tasks = []
        for task in self._tasks.values():
            if task.started_at and start_date <= task.started_at <= end_date:
                period_tasks.append(task)
            elif task.completed_at and start_date <= task.completed_at <= end_date:
                period_tasks.append(task)

        metrics = PeriodMetrics(
            period_start=start_date,
            period_end=end_date,
            total_tasks=len(period_tasks)
        )

        completed_tasks = [t for t in period_tasks if t.status == TaskStatus.COMPLETED]
        failed_tasks = [t for t in period_tasks if t.status == TaskStatus.FAILED]
        pending_tasks = [t for t in period_tasks if t.status == TaskStatus.PENDING]
        in_progress_tasks = [t for t in period_tasks if t.status == TaskStatus.IN_PROGRESS]

        metrics.completed_tasks = len(completed_tasks)
        metrics.failed_tasks = len(failed_tasks)
        metrics.pending_tasks = len(pending_tasks)
        metrics.in_progress_tasks = len(in_progress_tasks)

        # Calculate totals
        for task in completed_tasks:
            if task.duration_minutes:
                metrics.total_duration_minutes += task.duration_minutes
            if task.estimated_minutes:
                metrics.total_estimated_minutes += task.estimated_minutes
            if task.manual_estimate_minutes:
                metrics.total_manual_estimate_minutes += task.manual_estimate_minutes
            else:
                # Calculate from baseline
                if task.estimated_minutes:
                    metrics.total_manual_estimate_minutes += self.calculate_manual_estimate(task.estimated_minutes)

        # Calculate averages
        if completed_tasks:
            metrics.avg_completion_time = metrics.total_duration_minutes / len(completed_tasks)

            # Estimate accuracy: how close were estimates to actual
            total_accuracy = 0
            for task in completed_tasks:
                if task.estimated_minutes and task.duration_minutes:
                    # Accuracy is inverse of error percentage
                    error = abs(task.estimated_minutes - task.duration_minutes) / task.estimated_minutes
                    accuracy = max(0, 100 - (error * 100))
                    total_accuracy += accuracy
            metrics.estimate_accuracy = total_accuracy / len(completed_tasks)

            # Time saved vs manual
            metrics.time_saved_minutes = max(0, metrics.total_manual_estimate_minutes - metrics.total_duration_minutes)

        # Calculate health score
        metrics.health_score = self._calculate_health_score(metrics)

        return metrics

    def _calculate_health_score(self, metrics: PeriodMetrics) -> float:
        """
        Calculate overall health score (0-100).

        Formula:
        health_score = (
            throughput * 0.25 +
            quality * 0.25 +
            efficiency * 0.20 +
            reliability * 0.20 +
            roi * 0.10
        )
        """
        # Throughput: tasks completed per day
        days = (metrics.period_end - metrics.period_start).days or 1
        tasks_per_day = metrics.completed_tasks / days
        throughput = min(100, tasks_per_day * 10)  # 10 tasks/day = 100%

        # Quality: completion rate
        completed_plus_failed = metrics.completed_tasks + metrics.failed_tasks
        if completed_plus_failed > 0:
            quality = (metrics.completed_tasks / completed_plus_failed) * 100
        else:
            quality = 100

        # Efficiency: estimate accuracy
        efficiency = metrics.estimate_accuracy

        # Reliability: consistency (low variance in completion times)
        # Simplified: penalize if many failures
        failure_rate = metrics.failed_tasks / max(1, metrics.total_tasks)
        reliability = (1 - failure_rate) * 100

        # ROI: time saved ratio
        if metrics.total_manual_estimate_minutes > 0:
            roi_ratio = metrics.time_saved_minutes / metrics.total_manual_estimate_minutes
            roi = min(100, roi_ratio * 100)
        else:
            roi = 50  # Neutral if no data

        health_score = (
            throughput * 0.25 +
            quality * 0.25 +
            efficiency * 0.20 +
            reliability * 0.20 +
            roi * 0.10
        )

        return round(health_score, 2)

    def establish_baseline(
        self,
        manual_multiplier: float = DEFAULT_MANUAL_MULTIPLIER,
        min_manual_time: int = MIN_MANUAL_TIME,
        task_baselines: Optional[Dict[str, Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """Establish or update baseline metrics."""
        baseline = {
            'manual_time_multiplier': manual_multiplier,
            'min_manual_time_minutes': min_manual_time,
            'established_at': datetime.now().isoformat(),
            'tasks_baseline': task_baselines or {}
        }

        self._save_baseline(baseline)
        logger.info(f"Established baseline with multiplier={manual_multiplier}")
        return baseline

    def update_dashboard(self) -> Dict[str, Any]:
        """Update the metrics dashboard YAML file."""
        # Calculate current period metrics
        current_metrics = self.calculate_period_metrics()

        # Calculate previous period for comparison
        days = (current_metrics.period_end - current_metrics.period_start).days or 7
        prev_start = current_metrics.period_start - timedelta(days=days)
        prev_end = current_metrics.period_start
        previous_metrics = self.calculate_period_metrics(prev_start, prev_end)

        # Build dashboard data
        dashboard = {
            'metadata': {
                'updated_at': datetime.now().isoformat(),
                'version': '1.0.0'
            },
            'current_period': current_metrics.to_dict(),
            'previous_period': previous_metrics.to_dict(),
            'trends': {
                'tasks_delta': current_metrics.completed_tasks - previous_metrics.completed_tasks,
                'health_score_delta': current_metrics.health_score - previous_metrics.health_score,
                'time_saved_delta': current_metrics.time_saved_minutes - previous_metrics.time_saved_minutes,
                'accuracy_delta': current_metrics.estimate_accuracy - previous_metrics.estimate_accuracy
            },
            'all_time': self._calculate_all_time_metrics(),
            'health': {
                'score': current_metrics.health_score,
                'status': self._health_status(current_metrics.health_score),
                'components': {
                    'throughput': self._calculate_throughput_score(current_metrics),
                    'quality': self._calculate_quality_score(current_metrics),
                    'efficiency': current_metrics.estimate_accuracy,
                    'reliability': self._calculate_reliability_score(current_metrics),
                    'roi': self._calculate_roi_score(current_metrics)
                }
            }
        }

        # Save dashboard
        try:
            with open(self.dashboard_file, 'w') as f:
                yaml.dump(dashboard, f, default_flow_style=False, sort_keys=False)
            logger.info(f"Updated dashboard at {self.dashboard_file}")
        except Exception as e:
            logger.error(f"Error saving dashboard: {e}")

        return dashboard

    def _calculate_all_time_metrics(self) -> Dict[str, Any]:
        """Calculate all-time aggregate metrics."""
        all_tasks = list(self._tasks.values())
        completed = [t for t in all_tasks if t.status == TaskStatus.COMPLETED]

        total_time_saved = 0
        for task in completed:
            if task.manual_estimate_minutes and task.duration_minutes:
                total_time_saved += max(0, task.manual_estimate_minutes - task.duration_minutes)

        return {
            'total_tasks': len(all_tasks),
            'completed_tasks': len(completed),
            'failed_tasks': len([t for t in all_tasks if t.status == TaskStatus.FAILED]),
            'total_time_saved_hours': round(total_time_saved / 60, 2),
            'avg_task_duration': round(
                sum(t.duration_minutes or 0 for t in completed) / max(1, len(completed)), 2
            )
        }

    def _health_status(self, score: float) -> str:
        """Convert health score to status string."""
        if score >= 80:
            return 'excellent'
        elif score >= 60:
            return 'good'
        elif score >= 40:
            return 'fair'
        else:
            return 'needs_attention'

    def _calculate_throughput_score(self, metrics: PeriodMetrics) -> float:
        """Calculate throughput component score."""
        days = (metrics.period_end - metrics.period_start).days or 1
        tasks_per_day = metrics.completed_tasks / days
        return round(min(100, tasks_per_day * 10), 2)

    def _calculate_quality_score(self, metrics: PeriodMetrics) -> float:
        """Calculate quality component score."""
        completed_plus_failed = metrics.completed_tasks + metrics.failed_tasks
        if completed_plus_failed > 0:
            return round((metrics.completed_tasks / completed_plus_failed) * 100, 2)
        return 100.0

    def _calculate_reliability_score(self, metrics: PeriodMetrics) -> float:
        """Calculate reliability component score."""
        failure_rate = metrics.failed_tasks / max(1, metrics.total_tasks)
        return round((1 - failure_rate) * 100, 2)

    def _calculate_roi_score(self, metrics: PeriodMetrics) -> float:
        """Calculate ROI component score."""
        if metrics.total_manual_estimate_minutes > 0:
            roi_ratio = metrics.time_saved_minutes / metrics.total_manual_estimate_minutes
            return round(min(100, roi_ratio * 100), 2)
        return 50.0

    def generate_report(self, period: str = 'weekly') -> str:
        """Generate a formatted metrics report."""
        if period == 'weekly':
            start_date = datetime.now() - timedelta(days=7)
        elif period == 'daily':
            start_date = datetime.now() - timedelta(days=1)
        elif period == 'monthly':
            start_date = datetime.now() - timedelta(days=30)
        else:
            start_date = datetime.now() - timedelta(days=7)

        metrics = self.calculate_period_metrics(start_date)

        report_lines = [
            "=" * 60,
            f"BB5 Metrics Report - {period.upper()}",
            f"Period: {metrics.period_start.strftime('%Y-%m-%d')} to {metrics.period_end.strftime('%Y-%m-%d')}",
            "=" * 60,
            "",
            "Task Summary:",
            f"  Total Tasks: {metrics.total_tasks}",
            f"  Completed: {metrics.completed_tasks}",
            f"  Failed: {metrics.failed_tasks}",
            f"  Pending: {metrics.pending_tasks}",
            f"  In Progress: {metrics.in_progress_tasks}",
            "",
            "Performance Metrics:",
            f"  Average Completion Time: {metrics.avg_completion_time:.1f} minutes",
            f"  Estimate Accuracy: {metrics.estimate_accuracy:.1f}%",
            f"  Time Saved vs Manual: {metrics.time_saved_minutes} minutes ({metrics.time_saved_minutes/60:.1f} hours)",
            "",
            "Health Score:",
            f"  Overall: {metrics.health_score:.1f}/100 ({self._health_status(metrics.health_score)})",
            "",
            "Component Breakdown:",
            f"  Throughput: {self._calculate_throughput_score(metrics):.1f}/100",
            f"  Quality: {self._calculate_quality_score(metrics):.1f}/100",
            f"  Efficiency: {metrics.estimate_accuracy:.1f}/100",
            f"  Reliability: {self._calculate_reliability_score(metrics):.1f}/100",
            f"  ROI: {self._calculate_roi_score(metrics):.1f}/100",
            "",
            "=" * 60
        ]

        return '\n'.join(report_lines)

    def sync_with_execution_state(self) -> None:
        """Sync metrics with execution-state.yaml."""
        if not self.execution_state_file.exists():
            logger.warning(f"Execution state file not found: {self.execution_state_file}")
            return

        try:
            with open(self.execution_state_file, 'r') as f:
                state = yaml.safe_load(f) or {}

            # Extract metrics from execution state
            stats = state.get('stats', {})
            current = state.get('current', {})

            # Update metrics if there's an active task
            current_task = current.get('task_id')
            if current_task:
                status = current.get('status', 'pending')
                if status == 'in_progress' and current_task not in self._tasks:
                    # Auto-record start
                    self.record_event(
                        task_id=current_task,
                        event_type=EventType.START,
                        estimated_minutes=current.get('estimated_minutes'),
                        metadata={'source': 'execution_state_sync'}
                    )

            # Update dashboard with latest
            self.update_dashboard()
            logger.info("Synced metrics with execution state")

        except Exception as e:
            logger.error(f"Error syncing with execution state: {e}")


def main():
    """Main entry point for CLI."""
    parser = argparse.ArgumentParser(
        description='BB5 Metrics Collector - Track task execution metrics',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  bb5-metrics-collector.py collect --task-id TASK-001 --event start
  bb5-metrics-collector.py collect --task-id TASK-001 --event complete --duration 45
  bb5-metrics-collector.py report --period weekly
  bb5-metrics-collector.py dashboard --update
  bb5-metrics-collector.py baseline --establish --multiplier 3.0
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Collect command
    collect_parser = subparsers.add_parser('collect', help='Record a task event')
    collect_parser.add_argument('--task-id', required=True, help='Task identifier')
    collect_parser.add_argument(
        '--event',
        required=True,
        choices=['start', 'complete', 'fail', 'pause', 'resume'],
        help='Event type'
    )
    collect_parser.add_argument('--duration', type=int, help='Duration in minutes')
    collect_parser.add_argument('--estimated', type=int, help='Estimated duration in minutes')
    collect_parser.add_argument('--manual-estimate', type=int, help='Manual execution estimate in minutes')
    collect_parser.add_argument('--metadata', type=json.loads, help='JSON metadata dict')
    collect_parser.add_argument('--project-path', help='Path to BlackBox5 project')

    # Report command
    report_parser = subparsers.add_parser('report', help='Generate metrics report')
    report_parser.add_argument(
        '--period',
        choices=['daily', 'weekly', 'monthly'],
        default='weekly',
        help='Report period'
    )
    report_parser.add_argument('--project-path', help='Path to BlackBox5 project')

    # Dashboard command
    dashboard_parser = subparsers.add_parser('dashboard', help='Update metrics dashboard')
    dashboard_parser.add_argument('--update', action='store_true', help='Update dashboard file')
    dashboard_parser.add_argument('--sync', action='store_true', help='Sync with execution state')
    dashboard_parser.add_argument('--project-path', help='Path to BlackBox5 project')

    # Baseline command
    baseline_parser = subparsers.add_parser('baseline', help='Manage baseline metrics')
    baseline_parser.add_argument('--establish', action='store_true', help='Establish new baseline')
    baseline_parser.add_argument('--multiplier', type=float, default=3.0, help='Manual time multiplier')
    baseline_parser.add_argument('--min-time', type=int, default=15, help='Minimum manual time in minutes')
    baseline_parser.add_argument('--project-path', help='Path to BlackBox5 project')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    # Initialize collector
    project_path = Path(args.project_path) if args.project_path else None
    collector = MetricsCollector(project_path)

    # Execute command
    if args.command == 'collect':
        event_type = EventType(args.event)
        task = collector.record_event(
            task_id=args.task_id,
            event_type=event_type,
            duration_minutes=args.duration,
            estimated_minutes=args.estimated,
            manual_estimate_minutes=args.manual_estimate,
            metadata=args.metadata
        )
        print(f"Recorded {args.event} for task {args.task_id}")
        print(f"Status: {task.status.value}")

    elif args.command == 'report':
        report = collector.generate_report(args.period)
        print(report)

    elif args.command == 'dashboard':
        if args.sync:
            collector.sync_with_execution_state()
        if args.update or not args.sync:
            dashboard = collector.update_dashboard()
            print(f"Dashboard updated at {collector.dashboard_file}")
            print(f"Health Score: {dashboard['health']['score']}/100 ({dashboard['health']['status']})")

    elif args.command == 'baseline':
        if args.establish:
            baseline = collector.establish_baseline(
                manual_multiplier=args.multiplier,
                min_manual_time=args.min_time
            )
            print(f"Baseline established:")
            print(f"  Manual multiplier: {baseline['manual_time_multiplier']}x")
            print(f"  Minimum manual time: {baseline['min_manual_time_minutes']} minutes")
        else:
            baseline = collector._load_baseline()
            print(f"Current baseline:")
            print(f"  Manual multiplier: {baseline['manual_time_multiplier']}x")
            print(f"  Minimum manual time: {baseline['min_manual_time_minutes']} minutes")
            print(f"  Established: {baseline['established_at']}")


if __name__ == '__main__':
    main()
