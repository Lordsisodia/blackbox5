#!/usr/bin/env python3
"""
BB5 Health Dashboard - Real-time system health monitoring for BlackBox5.

Usage:
    bb5-health-dashboard.py show [--format FORMAT]
    bb5-health-dashboard.py watch [--interval SECONDS]
    bb5-health-dashboard.py export [--format FORMAT] [--output FILE]

Options:
    --format FORMAT    Output format: table, json, csv [default: table]
    --interval SECONDS Refresh interval in seconds [default: 5]
    --output FILE      Output file path (for export)
"""

import argparse
import csv
import io
import json
import os
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Optional

# Color codes for terminal output
COLORS = {
    "reset": "\033[0m",
    "bold": "\033[1m",
    "dim": "\033[2m",
    "red": "\033[91m",
    "green": "\033[92m",
    "yellow": "\033[93m",
    "blue": "\033[94m",
    "magenta": "\033[95m",
    "cyan": "\033[96m",
    "white": "\033[97m",
    "bg_red": "\033[41m",
    "bg_green": "\033[42m",
    "bg_yellow": "\033[43m",
}

# Health score thresholds
HEALTH_THRESHOLDS = {
    "critical": (0, 59),
    "warning": (60, 79),
    "healthy": (80, 100),
}


@dataclass
class TaskStats:
    """Statistics for task queue."""
    pending: int = 0
    in_progress: int = 0
    completed: int = 0
    total: int = 0

    @property
    def completion_rate(self) -> float:
        """Calculate completion rate as percentage."""
        if self.total == 0:
            return 0.0
        return (self.completed / self.total) * 100


@dataclass
class ExecutionSlot:
    """Represents an active execution slot."""
    slot_id: int
    status: str = "idle"
    task_id: Optional[str] = None
    task_name: Optional[str] = None
    started_at: Optional[datetime] = None
    progress: int = 0

    @property
    def duration(self) -> Optional[timedelta]:
        """Calculate execution duration."""
        if self.started_at:
            return datetime.now() - self.started_at
        return None


@dataclass
class CompletedTask:
    """Represents a recently completed task."""
    task_id: str
    task_name: str
    completed_at: datetime
    duration: timedelta
    status: str = "completed"


@dataclass
class ROIMetrics:
    """ROI and efficiency metrics."""
    total_time_saved: float = 0.0  # hours
    efficiency_score: float = 0.0  # percentage
    tasks_automated: int = 0
    avg_task_duration: float = 0.0  # minutes
    trend: str = "→"  # ↑ ↓ →


@dataclass
class HealthData:
    """Complete health data snapshot."""
    timestamp: datetime = field(default_factory=datetime.now)
    overall_score: int = 0
    task_stats: TaskStats = field(default_factory=TaskStats)
    execution_slots: list[ExecutionSlot] = field(default_factory=list)
    recent_completions: list[CompletedTask] = field(default_factory=list)
    roi_metrics: ROIMetrics = field(default_factory=ROIMetrics)
    system_status: str = "unknown"


def get_color_for_score(score: int) -> str:
    """Get color code based on health score."""
    if score >= 80:
        return COLORS["green"]
    elif score >= 60:
        return COLORS["yellow"]
    else:
        return COLORS["red"]


def get_bg_color_for_score(score: int) -> str:
    """Get background color code based on health score."""
    if score >= 80:
        return COLORS["bg_green"]
    elif score >= 60:
        return COLORS["bg_yellow"]
    else:
        return COLORS["bg_red"]


def get_status_text(score: int) -> str:
    """Get status text based on health score."""
    if score >= 80:
        return "HEALTHY"
    elif score >= 60:
        return "WARNING"
    else:
        return "CRITICAL"


def render_progress_bar(percentage: float, width: int = 30) -> str:
    """Render a text-based progress bar."""
    filled = int((percentage / 100) * width)
    empty = width - filled
    bar = "█" * filled + "░" * empty
    color = get_color_for_score(int(percentage))
    return f"{color}{bar}{COLORS['reset']} {percentage:.1f}%"


def format_duration(duration: Optional[timedelta]) -> str:
    """Format timedelta for display."""
    if duration is None:
        return "N/A"
    total_seconds = int(duration.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    if hours > 0:
        return f"{hours}h {minutes}m"
    elif minutes > 0:
        return f"{minutes}m {seconds}s"
    else:
        return f"{seconds}s"


def truncate_text(text: str, max_length: int) -> str:
    """Truncate text to max length with ellipsis."""
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."


class HealthDataCollector:
    """Collects health data from the BlackBox5 system."""

    def __init__(self, base_path: Path = None):
        self.base_path = base_path or Path.home() / ".blackbox5" / "5-project-memory" / "blackbox5"
        self.tasks_path = self.base_path / "tasks"
        self.runs_path = self.base_path / ".autonomous" / "runs"

    def collect(self) -> HealthData:
        """Collect current health data from the system."""
        data = HealthData()
        data.task_stats = self._collect_task_stats()
        data.execution_slots = self._collect_execution_slots()
        data.recent_completions = self._collect_recent_completions()
        data.roi_metrics = self._collect_roi_metrics()
        data.overall_score = self._calculate_overall_score(data)
        data.system_status = get_status_text(data.overall_score)
        return data

    def _collect_task_stats(self) -> TaskStats:
        """Collect task queue statistics."""
        stats = TaskStats()

        active_path = self.tasks_path / "active"
        completed_path = self.tasks_path / "completed"

        if active_path.exists():
            for task_dir in active_path.iterdir():
                if task_dir.is_dir():
                    status = self._get_task_status(task_dir)
                    if status == "pending":
                        stats.pending += 1
                    elif status == "in_progress":
                        stats.in_progress += 1

        if completed_path.exists():
            stats.completed = len([d for d in completed_path.iterdir() if d.is_dir()])

        stats.total = stats.pending + stats.in_progress + stats.completed
        return stats

    def _get_task_status(self, task_dir: Path) -> str:
        """Determine task status from task directory."""
        task_file = task_dir / "task.yaml"
        if task_file.exists():
            content = task_file.read_text()
            if "in_progress" in content:
                return "in_progress"
            elif "pending" in content:
                return "pending"
        return "pending"

    def _collect_execution_slots(self) -> list[ExecutionSlot]:
        """Collect active execution slot information."""
        slots = []

        # Check for active runs
        if self.runs_path.exists():
            active_runs = sorted(
                [d for d in self.runs_path.iterdir() if d.is_dir()],
                key=lambda x: x.stat().st_mtime,
                reverse=True
            )[:5]

            for i, run_dir in enumerate(active_runs, 1):
                slot = ExecutionSlot(slot_id=i)
                status_file = run_dir / "status.yaml"

                if status_file.exists():
                    content = status_file.read_text()
                    if "running" in content.lower():
                        slot.status = "running"
                        slot.task_id = run_dir.name
                        slot.task_name = self._extract_task_name(run_dir)
                        slot.started_at = datetime.fromtimestamp(run_dir.stat().st_mtime)
                        slot.progress = self._estimate_progress(run_dir)
                    elif "completed" in content.lower():
                        slot.status = "completed"
                    else:
                        slot.status = "idle"
                else:
                    # Infer status from directory age
                    age = time.time() - run_dir.stat().st_mtime
                    if age < 3600:  # Less than 1 hour old
                        slot.status = "running"
                        slot.task_id = run_dir.name
                        slot.task_name = self._extract_task_name(run_dir)
                        slot.started_at = datetime.fromtimestamp(run_dir.stat().st_mtime)
                        slot.progress = 50  # Unknown, show 50%
                    else:
                        slot.status = "idle"

                slots.append(slot)

        # Fill remaining slots
        while len(slots) < 5:
            slots.append(ExecutionSlot(slot_id=len(slots) + 1))

        return slots[:5]

    def _extract_task_name(self, run_dir: Path) -> str:
        """Extract task name from run directory."""
        # Try to find task reference in run files
        for file in run_dir.glob("*.md"):
            content = file.read_text()
            if "Task:" in content:
                lines = content.split("\n")
                for line in lines:
                    if "Task:" in line:
                        return line.split("Task:")[1].strip()
        return run_dir.name

    def _estimate_progress(self, run_dir: Path) -> int:
        """Estimate progress of a running task."""
        # Look for progress indicators in log files
        log_files = list(run_dir.glob("*.log")) + list(run_dir.glob("*.md"))
        for log_file in log_files:
            try:
                content = log_file.read_text()
                if "progress" in content.lower():
                    # Simple heuristic: count completion indicators
                    total_lines = len(content.split("\n"))
                    completed_lines = content.lower().count("complete") + content.lower().count("done")
                    if total_lines > 0:
                        return min(100, int((completed_lines / total_lines) * 100))
            except Exception:
                pass
        return 50  # Default to 50% if unknown

    def _collect_recent_completions(self) -> list[CompletedTask]:
        """Collect recently completed tasks."""
        completions = []

        completed_path = self.tasks_path / "completed"
        if completed_path.exists():
            completed_tasks = sorted(
                [d for d in completed_path.iterdir() if d.is_dir()],
                key=lambda x: x.stat().st_mtime,
                reverse=True
            )[:5]

            for task_dir in completed_tasks:
                task = CompletedTask(
                    task_id=task_dir.name,
                    task_name=self._extract_task_name(task_dir),
                    completed_at=datetime.fromtimestamp(task_dir.stat().st_mtime),
                    duration=timedelta(minutes=30),  # Default estimate
                )

                # Try to find actual duration
                task_file = task_dir / "task.yaml"
                if task_file.exists():
                    content = task_file.read_text()
                    # Parse duration if available
                    if "duration:" in content:
                        try:
                            duration_str = content.split("duration:")[1].split("\n")[0].strip()
                            task.duration = timedelta(minutes=int(duration_str))
                        except (ValueError, IndexError):
                            pass

                completions.append(task)

        return completions

    def _collect_roi_metrics(self) -> ROIMetrics:
        """Collect ROI and efficiency metrics."""
        roi = ROIMetrics()

        # Calculate based on completed tasks
        stats = self._collect_task_stats()
        roi.tasks_automated = stats.completed

        # Estimate time saved (assuming manual task would take 2x longer)
        avg_duration = 30  # minutes
        roi.total_time_saved = (stats.completed * avg_duration) / 60  # hours

        # Calculate efficiency score
        if stats.total > 0:
            roi.efficiency_score = (stats.completed / stats.total) * 100
        else:
            roi.efficiency_score = 0.0

        roi.avg_task_duration = avg_duration

        # Determine trend (compare to last week)
        roi.trend = self._calculate_trend()

        return roi

    def _calculate_trend(self) -> str:
        """Calculate trend indicator by comparing to historical data."""
        # Simple trend calculation based on recent activity
        completed_path = self.tasks_path / "completed"
        if not completed_path.exists():
            return "→"

        now = time.time()
        one_week_ago = now - (7 * 24 * 3600)
        two_weeks_ago = now - (14 * 24 * 3600)

        recent_count = 0
        previous_count = 0

        for task_dir in completed_path.iterdir():
            if task_dir.is_dir():
                mtime = task_dir.stat().st_mtime
                if mtime > one_week_ago:
                    recent_count += 1
                elif mtime > two_weeks_ago:
                    previous_count += 1

        if recent_count > previous_count:
            return "↑"
        elif recent_count < previous_count:
            return "↓"
        return "→"

    def _calculate_overall_score(self, data: HealthData) -> int:
        """Calculate overall health score."""
        scores = []

        # Task completion score (40% weight)
        if data.task_stats.total > 0:
            completion_score = (data.task_stats.completed / data.task_stats.total) * 100
        else:
            completion_score = 50  # Neutral if no tasks
        scores.append(completion_score * 0.4)

        # Queue health score (30% weight)
        if data.task_stats.pending > 0:
            queue_ratio = data.task_stats.in_progress / data.task_stats.pending
            queue_score = min(100, queue_ratio * 100)
        else:
            queue_score = 100  # Good if no pending tasks
        scores.append(queue_score * 0.3)

        # Execution slot utilization (20% weight)
        active_slots = sum(1 for slot in data.execution_slots if slot.status == "running")
        execution_score = (active_slots / 5) * 100
        scores.append(execution_score * 0.2)

        # ROI efficiency (10% weight)
        scores.append(data.roi_metrics.efficiency_score * 0.1)

        return int(sum(scores))


class DashboardRenderer:
    """Renders health data in various formats."""

    def __init__(self, use_colors: bool = True):
        self.use_colors = use_colors and sys.stdout.isatty()

    def _color(self, color_code: str) -> str:
        """Return color code if colors are enabled."""
        return COLORS.get(color_code, "") if self.use_colors else ""

    def render_table(self, data: HealthData) -> str:
        """Render health data as formatted table."""
        lines = []

        # Header
        lines.append("")
        lines.append(f"{self._color('bold')}{'=' * 70}{self._color('reset')}")
        lines.append(f"{self._color('cyan')}  BB5 HEALTH DASHBOARD{self._color('reset')}  {data.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"{self._color('bold')}{'=' * 70}{self._color('reset')}")

        # Overall Health Score
        score_color = get_color_for_score(data.overall_score)
        bg_color = get_bg_color_for_score(data.overall_score)
        lines.append("")
        lines.append(f"{self._color('bold')}  OVERALL HEALTH{self._color('reset')}")
        lines.append(f"  {self._color('bold')}{bg_color}  {data.overall_score:>3}  {self._color('reset')}  {score_color}{data.system_status}{self._color('reset')}")
        lines.append(f"  {render_progress_bar(data.overall_score, 40)}")

        # Task Queue Status
        lines.append("")
        lines.append(f"{self._color('bold')}  TASK QUEUE STATUS{self._color('reset')}")
        lines.append(f"  ┌─────────────┬────────┐")
        lines.append(f"  │ Pending     │ {self._color('yellow')}{data.task_stats.pending:>6}{self._color('reset')} │")
        lines.append(f"  │ In Progress │ {self._color('blue')}{data.task_stats.in_progress:>6}{self._color('reset')} │")
        lines.append(f"  │ Completed   │ {self._color('green')}{data.task_stats.completed:>6}{self._color('reset')} │")
        lines.append(f"  │ Total       │ {self._color('white')}{data.task_stats.total:>6}{self._color('reset')} │")
        lines.append(f"  └─────────────┴────────┘")
        lines.append(f"  Completion Rate: {render_progress_bar(data.task_stats.completion_rate, 30)}")

        # Active Executions
        lines.append("")
        lines.append(f"{self._color('bold')}  ACTIVE EXECUTIONS (5 Slots){self._color('reset')}")
        lines.append(f"  ┌──────┬──────────┬─────────────────────┬──────────┬──────────┐")
        lines.append(f"  │ Slot │ Status   │ Task                │ Duration │ Progress │")
        lines.append(f"  ├──────┼──────────┼─────────────────────┼──────────┼──────────┤")

        for slot in data.execution_slots:
            status_color = {
                "running": "blue",
                "completed": "green",
                "idle": "dim",
            }.get(slot.status, "white")

            status_display = slot.status.upper() if slot.status != "idle" else "IDLE"
            task_display = truncate_text(slot.task_name or "-", 19)
            duration_display = format_duration(slot.duration)
            progress_bar = "█" * (slot.progress // 10) + "░" * (10 - (slot.progress // 10))

            lines.append(f"  │ {slot.slot_id:>4} │ {self._color(status_color)}{status_display:>8}{self._color('reset')} │ {task_display:<19} │ {duration_display:>8} │ {progress_bar} {slot.progress:>3}% │")

        lines.append(f"  └──────┴──────────┴─────────────────────┴──────────┴──────────┘")

        # Recent Completions
        lines.append("")
        lines.append(f"{self._color('bold')}  RECENT COMPLETIONS (Last 5){self._color('reset')}")
        if data.recent_completions:
            lines.append(f"  ┌─────────────────────┬─────────────────────┬──────────┐")
            lines.append(f"  │ Task ID             │ Completed           │ Duration │")
            lines.append(f"  ├─────────────────────┼─────────────────────┼──────────┤")
            for task in data.recent_completions:
                task_id = truncate_text(task.task_id, 19)
                completed = task.completed_at.strftime("%m-%d %H:%M")
                duration = format_duration(task.duration)
                lines.append(f"  │ {task_id:<19} │ {completed:<19} │ {duration:>8} │")
            lines.append(f"  └─────────────────────┴─────────────────────┴──────────┘")
        else:
            lines.append(f"  {self._color('dim')}No recent completions{self._color('reset')}")

        # ROI Summary
        lines.append("")
        lines.append(f"{self._color('bold')}  ROI SUMMARY{self._color('reset')}  Trend: {self._get_trend_color(data.roi_metrics.trend)}{data.roi_metrics.trend}{self._color('reset')}")
        lines.append(f"  ┌─────────────────────┬─────────────────────┐")
        lines.append(f"  │ Time Saved          │ {self._color('green')}{data.roi_metrics.total_time_saved:>10.1f} hrs{self._color('reset')} │")
        lines.append(f"  │ Efficiency          │ {render_progress_bar(data.roi_metrics.efficiency_score, 20)} │")
        lines.append(f"  │ Tasks Automated     │ {self._color('cyan')}{data.roi_metrics.tasks_automated:>10}{self._color('reset')} │")
        lines.append(f"  │ Avg Task Duration   │ {data.roi_metrics.avg_task_duration:>10.1f} min │")
        lines.append(f"  └─────────────────────┴─────────────────────┘")

        # Footer
        lines.append("")
        lines.append(f"{self._color('bold')}{'=' * 70}{self._color('reset')}")
        lines.append(f"{self._color('dim')}  Use 'bb5-health-dashboard.py watch' for real-time monitoring{self._color('reset')}")
        lines.append("")

        return "\n".join(lines)

    def _get_trend_color(self, trend: str) -> str:
        """Get color for trend indicator."""
        if trend == "↑":
            return self._color("green")
        elif trend == "↓":
            return self._color("red")
        return self._color("yellow")

    def render_json(self, data: HealthData) -> str:
        """Render health data as JSON."""
        export_data = {
            "timestamp": data.timestamp.isoformat(),
            "overall_score": data.overall_score,
            "system_status": data.system_status,
            "task_stats": {
                "pending": data.task_stats.pending,
                "in_progress": data.task_stats.in_progress,
                "completed": data.task_stats.completed,
                "total": data.task_stats.total,
                "completion_rate": round(data.task_stats.completion_rate, 2),
            },
            "execution_slots": [
                {
                    "slot_id": slot.slot_id,
                    "status": slot.status,
                    "task_id": slot.task_id,
                    "task_name": slot.task_name,
                    "started_at": slot.started_at.isoformat() if slot.started_at else None,
                    "progress": slot.progress,
                    "duration_seconds": slot.duration.total_seconds() if slot.duration else None,
                }
                for slot in data.execution_slots
            ],
            "recent_completions": [
                {
                    "task_id": task.task_id,
                    "task_name": task.task_name,
                    "completed_at": task.completed_at.isoformat(),
                    "duration_minutes": task.duration.total_seconds() / 60,
                    "status": task.status,
                }
                for task in data.recent_completions
            ],
            "roi_metrics": {
                "total_time_saved_hours": round(data.roi_metrics.total_time_saved, 2),
                "efficiency_score": round(data.roi_metrics.efficiency_score, 2),
                "tasks_automated": data.roi_metrics.tasks_automated,
                "avg_task_duration_minutes": round(data.roi_metrics.avg_task_duration, 2),
                "trend": data.roi_metrics.trend,
            },
        }
        return json.dumps(export_data, indent=2)

    def render_csv(self, data: HealthData) -> str:
        """Render health data as CSV."""
        output = io.StringIO()
        writer = csv.writer(output)

        # Header
        writer.writerow(["BB5 Health Dashboard", data.timestamp.isoformat()])
        writer.writerow([])

        # Overall Score
        writer.writerow(["Overall Score", data.overall_score, data.system_status])
        writer.writerow([])

        # Task Stats
        writer.writerow(["Task Queue Status"])
        writer.writerow(["Status", "Count"])
        writer.writerow(["Pending", data.task_stats.pending])
        writer.writerow(["In Progress", data.task_stats.in_progress])
        writer.writerow(["Completed", data.task_stats.completed])
        writer.writerow(["Total", data.task_stats.total])
        writer.writerow(["Completion Rate %", round(data.task_stats.completion_rate, 2)])
        writer.writerow([])

        # Execution Slots
        writer.writerow(["Execution Slots"])
        writer.writerow(["Slot ID", "Status", "Task ID", "Task Name", "Progress %"])
        for slot in data.execution_slots:
            writer.writerow([
                slot.slot_id,
                slot.status,
                slot.task_id or "",
                slot.task_name or "",
                slot.progress,
            ])
        writer.writerow([])

        # ROI Metrics
        writer.writerow(["ROI Metrics"])
        writer.writerow(["Metric", "Value"])
        writer.writerow(["Time Saved (hours)", round(data.roi_metrics.total_time_saved, 2)])
        writer.writerow(["Efficiency Score %", round(data.roi_metrics.efficiency_score, 2)])
        writer.writerow(["Tasks Automated", data.roi_metrics.tasks_automated])
        writer.writerow(["Avg Task Duration (min)", round(data.roi_metrics.avg_task_duration, 2)])
        writer.writerow(["Trend", data.roi_metrics.trend])

        return output.getvalue()


def cmd_show(args: argparse.Namespace) -> int:
    """Handle the 'show' command."""
    collector = HealthDataCollector()
    renderer = DashboardRenderer(use_colors=not args.no_color)

    try:
        data = collector.collect()

        if args.format == "json":
            print(renderer.render_json(data))
        elif args.format == "csv":
            print(renderer.render_csv(data))
        else:
            print(renderer.render_table(data))

        return 0
    except Exception as e:
        print(f"Error collecting health data: {e}", file=sys.stderr)
        return 1


def cmd_watch(args: argparse.Namespace) -> int:
    """Handle the 'watch' command with auto-refresh."""
    collector = HealthDataCollector()
    renderer = DashboardRenderer(use_colors=not args.no_color)

    try:
        while True:
            # Clear screen
            os.system("clear" if os.name == "posix" else "cls")

            data = collector.collect()
            print(renderer.render_table(data))
            print(f"{COLORS['dim']}Refreshing every {args.interval} seconds... Press Ctrl+C to exit{COLORS['reset']}")

            time.sleep(args.interval)
    except KeyboardInterrupt:
        print("\nExiting...")
        return 0
    except Exception as e:
        print(f"Error in watch mode: {e}", file=sys.stderr)
        return 1


def cmd_export(args: argparse.Namespace) -> int:
    """Handle the 'export' command."""
    collector = HealthDataCollector()
    renderer = DashboardRenderer(use_colors=False)

    try:
        data = collector.collect()

        if args.format == "json":
            output = renderer.render_json(data)
        elif args.format == "csv":
            output = renderer.render_csv(data)
        else:
            print(f"Unsupported export format: {args.format}", file=sys.stderr)
            return 1

        if args.output:
            output_path = Path(args.output)
            output_path.write_text(output)
            print(f"Exported to {output_path}")
        else:
            print(output)

        return 0
    except Exception as e:
        print(f"Error exporting data: {e}", file=sys.stderr)
        return 1


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="BB5 Health Dashboard - Monitor BlackBox5 system health",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    bb5-health-dashboard.py show                    # Display current health
    bb5-health-dashboard.py show --format json      # Output as JSON
    bb5-health-dashboard.py watch                   # Real-time monitoring
    bb5-health-dashboard.py watch --interval 10     # Refresh every 10 seconds
    bb5-health-dashboard.py export --output health.json
        """,
    )

    parser.add_argument(
        "--no-color",
        action="store_true",
        help="Disable colored output",
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Show command
    show_parser = subparsers.add_parser("show", help="Display current health status")
    show_parser.add_argument(
        "--format",
        choices=["table", "json", "csv"],
        default="table",
        help="Output format (default: table)",
    )
    show_parser.set_defaults(func=cmd_show)

    # Watch command
    watch_parser = subparsers.add_parser("watch", help="Monitor health in real-time")
    watch_parser.add_argument(
        "--interval",
        type=int,
        default=5,
        help="Refresh interval in seconds (default: 5)",
    )
    watch_parser.set_defaults(func=cmd_watch)

    # Export command
    export_parser = subparsers.add_parser("export", help="Export health data")
    export_parser.add_argument(
        "--format",
        choices=["json", "csv"],
        default="json",
        help="Export format (default: json)",
    )
    export_parser.add_argument(
        "--output",
        type=str,
        help="Output file path (default: stdout)",
    )
    export_parser.set_defaults(func=cmd_export)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
