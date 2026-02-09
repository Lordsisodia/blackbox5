#!/usr/bin/env python3
"""
Estimation Accuracy Tracker

Tracks and analyzes task estimation accuracy by comparing estimated vs actual
times for completed tasks. Calculates accuracy metrics by category and tracks
trends over time.

Usage:
    python track-estimation-accuracy.py [options]

Options:
    --output PATH       Output file for report (default: stdout)
    --format FORMAT     Output format: text, json, yaml (default: text)
    --days DAYS         Analyze tasks from last N days (default: all)
    --update-guidelines Update estimation-guidelines.yaml with findings
"""

import os
import re
import sys
import json
import yaml
import argparse
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Tuple, Optional

# Configuration
COMPLETED_TASKS_DIR = Path("/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/tasks/completed")
RUNS_DIR = Path("/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/runs")
ESTIMATION_GUIDELINES_PATH = Path("/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/operations/estimation-guidelines.yaml")


def parse_task_file(task_path: Path) -> Optional[Dict]:
    """Parse a task.md file and extract estimation and timing data."""
    try:
        content = task_path.read_text()
    except Exception:
        return None

    task_data = {
        "task_id": task_path.parent.name,
        "estimated_minutes": None,
        "actual_minutes": None,
        "task_type": None,
        "priority": None,
        "created": None,
        "completed": None,
        "status": None,
    }

    # Extract estimated minutes
    est_patterns = [
        r"\*\*Estimated Minutes:\*\*\s*(\d+)",
        r"\*\*Estimated Effort:\*\*\s*(\d+)\s*minutes",
        r"estimated_minutes:\s*(\d+)",
    ]
    for pattern in est_patterns:
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            task_data["estimated_minutes"] = int(match.group(1))
            break

    # Extract task type
    type_patterns = [
        r"\*\*Type:\*\*\s*(\w+)",
        r"^##?\s*(\w+):",
        r"Category:\s*(\w+)",
    ]
    for pattern in type_patterns:
        match = re.search(pattern, content, re.MULTILINE | re.IGNORECASE)
        if match:
            task_type = match.group(1).lower()
            if task_type in ["analyze", "implement", "fix", "organize", "security", "refactor", "bugfix", "test", "docs"]:
                task_data["task_type"] = task_type
                break

    # Extract priority
    priority_match = re.search(r"\*\*Priority:\*\*\s*(\w+)", content, re.IGNORECASE)
    if priority_match:
        task_data["priority"] = priority_match.group(1).lower()

    # Extract status
    status_match = re.search(r"\*\*Status:\*\*\s*(\w+)", content, re.IGNORECASE)
    if status_match:
        task_data["status"] = status_match.group(1).lower()

    # Extract created timestamp
    created_match = re.search(r"\*\*Created:\*\*\s*([\d\-T:.Z]+)", content)
    if created_match:
        task_data["created"] = created_match.group(1)

    # Extract completed timestamp
    completed_match = re.search(r"\*\*Completed:\*\*\s*([\d\-T:.Z]+)", content)
    if completed_match:
        task_data["completed"] = completed_match.group(1)

    # Calculate actual duration if we have both timestamps
    if task_data["created"] and task_data["completed"]:
        try:
            created_dt = parse_datetime(task_data["created"])
            completed_dt = parse_datetime(task_data["completed"])
            if created_dt and completed_dt:
                duration = (completed_dt - created_dt).total_seconds() / 60
                # Filter out unrealistic durations (> 8 hours likely indicates loop issues)
                if 0 < duration < 480:  # 8 hours max
                    task_data["actual_minutes"] = round(duration, 1)
        except Exception:
            pass

    return task_data


def parse_run_metadata(run_path: Path) -> Optional[Dict]:
    """Parse a run metadata.yaml file and extract duration data."""
    metadata_file = run_path / "metadata.yaml"
    if not metadata_file.exists():
        return None

    try:
        with open(metadata_file, 'r') as f:
            metadata = yaml.safe_load(f)
    except Exception:
        return None

    if not metadata:
        return None

    # Handle both 'run' and 'loop' formats
    run_data = metadata.get('run') or metadata.get('loop', {})
    if isinstance(run_data, str) or not run_data:
        return None

    # Extract task ID from run directory name if present
    run_id = run_data.get('id', run_path.name) if isinstance(run_data, dict) else run_path.name
    task_id = None

    # First try state.task_claimed
    state = metadata.get('state', {})
    if state and 'task_claimed' in state:
        task_id = state['task_claimed']

    # If not found, try to extract task ID from run name (e.g., run-20260206-082558-TASK-ARCH-052)
    if not task_id:
        task_match = re.search(r'(TASK-[A-Z0-9\-]+)', run_id)
        if task_match:
            task_id = task_match.group(1)

    if not task_id:
        return None

    duration_seconds = run_data.get('duration_seconds') if isinstance(run_data, dict) else None
    if not duration_seconds:
        # Try to calculate from timestamps
        start = run_data.get('timestamp_start')
        end = run_data.get('timestamp_end')
        if start and end:
            try:
                start_dt = parse_datetime(start.replace('+07:00', ''))
                end_dt = parse_datetime(end.replace('+07:00', ''))
                if start_dt and end_dt:
                    duration_seconds = (end_dt - start_dt).total_seconds()
            except Exception:
                pass

    if not duration_seconds or duration_seconds <= 0:
        return None

    # Filter out unrealistic durations (> 12 hours likely indicates loop issues)
    if duration_seconds > 43200:  # 12 hours in seconds
        return None

    return {
        "task_id": task_id,
        "actual_minutes": round(duration_seconds / 60, 1),
        "run_id": run_id,
        "timestamp_start": run_data.get('timestamp_start'),
        "timestamp_end": run_data.get('timestamp_end'),
    }


def parse_datetime(dt_str: str) -> Optional[datetime]:
    """Parse various datetime formats."""
    formats = [
        "%Y-%m-%dT%H:%M:%S.%fZ",
        "%Y-%m-%dT%H:%M:%SZ",
        "%Y-%m-%dT%H:%M:%S.%f",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%d",
    ]
    for fmt in formats:
        try:
            return datetime.strptime(dt_str, fmt)
        except ValueError:
            continue
    return None


def calculate_accuracy(estimated: float, actual: float) -> float:
    """Calculate estimation accuracy using the formula: 1 - (|actual - estimate| / estimate)."""
    if estimated == 0:
        return 0.0
    accuracy = 1 - (abs(actual - estimated) / estimated)
    return max(0.0, min(1.0, accuracy))


def categorize_accuracy(accuracy: float) -> str:
    """Categorize accuracy score."""
    if accuracy >= 0.8:
        return "good"
    elif accuracy >= 0.6:
        return "acceptable"
    else:
        return "poor"


def analyze_tasks(tasks: List[Dict]) -> Dict:
    """Analyze task estimation accuracy."""
    results = {
        "total_tasks": len(tasks),
        "tasks_with_estimates": 0,
        "tasks_with_actuals": 0,
        "tasks_comparable": 0,
        "overall_accuracy": 0.0,
        "accuracy_by_category": defaultdict(lambda: {"count": 0, "avg_accuracy": 0.0, "tasks": []}),
        "accuracy_by_type": defaultdict(lambda: {"count": 0, "avg_accuracy": 0.0, "total_estimated": 0, "total_actual": 0}),
        "trends": [],
        "underestimation_rate": 0.0,
        "overestimation_rate": 0.0,
        "recommended_multiplier": 1.0,
    }

    comparable_tasks = []
    total_accuracy = 0.0
    underestimation_count = 0
    overestimation_count = 0

    for task in tasks:
        if task["estimated_minutes"] is None:
            continue
        results["tasks_with_estimates"] += 1

        if task["actual_minutes"] is None:
            continue
        results["tasks_with_actuals"] += 1

        if task["estimated_minutes"] > 0 and task["actual_minutes"] > 0:
            results["tasks_comparable"] += 1
            accuracy = calculate_accuracy(task["estimated_minutes"], task["actual_minutes"])
            task["accuracy"] = accuracy
            task["accuracy_category"] = categorize_accuracy(accuracy)
            task["difference"] = task["actual_minutes"] - task["estimated_minutes"]
            task["ratio"] = task["actual_minutes"] / task["estimated_minutes"] if task["estimated_minutes"] > 0 else 0

            comparable_tasks.append(task)
            total_accuracy += accuracy

            if task["actual_minutes"] > task["estimated_minutes"]:
                underestimation_count += 1
            elif task["actual_minutes"] < task["estimated_minutes"]:
                overestimation_count += 1

            # Categorize by accuracy
            cat = task["accuracy_category"]
            results["accuracy_by_category"][cat]["count"] += 1
            results["accuracy_by_category"][cat]["tasks"].append(task)

            # Categorize by task type
            task_type = task.get("task_type") or "unknown"
            results["accuracy_by_type"][task_type]["count"] += 1
            results["accuracy_by_type"][task_type]["total_estimated"] += task["estimated_minutes"]
            results["accuracy_by_type"][task_type]["total_actual"] += task["actual_minutes"]

    # Calculate overall accuracy
    if results["tasks_comparable"] > 0:
        results["overall_accuracy"] = total_accuracy / results["tasks_comparable"]
        results["underestimation_rate"] = underestimation_count / results["tasks_comparable"]
        results["overestimation_rate"] = overestimation_count / results["tasks_comparable"]

    # Calculate average accuracy by category
    for cat_data in results["accuracy_by_category"].values():
        if cat_data["count"] > 0:
            cat_data["avg_accuracy"] = sum(t["accuracy"] for t in cat_data["tasks"]) / cat_data["count"]

    # Calculate average accuracy and recommended multiplier by type
    type_multipliers = []
    for type_name, type_data in results["accuracy_by_type"].items():
        if type_data["count"] > 0:
            type_tasks = [t for t in comparable_tasks if t.get("task_type") == type_name]
            if type_tasks:
                type_data["avg_accuracy"] = sum(t["accuracy"] for t in type_tasks) / len(type_tasks)
                # Calculate recommended multiplier for this type
                avg_ratio = sum(t["ratio"] for t in type_tasks) / len(type_tasks)
                type_data["recommended_multiplier"] = round(avg_ratio, 2)
                type_multipliers.append(avg_ratio)

    # Calculate overall recommended multiplier
    if comparable_tasks:
        avg_ratio = sum(t["ratio"] for t in comparable_tasks) / len(comparable_tasks)
        results["recommended_multiplier"] = round(max(1.0, avg_ratio), 2)
        results["current_multiplier"] = 1.35  # Current documented multiplier
        results["multiplier_delta"] = round(results["recommended_multiplier"] - results["current_multiplier"], 2)

    # Sort trends by date (filter out None values)
    comparable_with_date = [t for t in comparable_tasks if t.get("completed")]
    results["trends"] = sorted(comparable_with_date, key=lambda x: x.get("completed", ""), reverse=True)[:20]

    return results


def generate_text_report(results: Dict) -> str:
    """Generate a text report of estimation accuracy."""
    lines = []
    lines.append("=" * 70)
    lines.append("ESTIMATION ACCURACY ANALYSIS REPORT")
    lines.append("=" * 70)
    lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("")

    # Summary
    lines.append("-" * 70)
    lines.append("SUMMARY")
    lines.append("-" * 70)
    lines.append(f"Total Tasks Analyzed:        {results['total_tasks']}")
    lines.append(f"Tasks with Estimates:        {results['tasks_with_estimates']}")
    lines.append(f"Tasks with Actual Times:     {results['tasks_with_actuals']}")
    lines.append(f"Comparable Tasks:            {results['tasks_comparable']}")
    lines.append("")

    if results['tasks_comparable'] == 0:
        lines.append("No comparable tasks found with both estimates and actual times.")
        return "\n".join(lines)

    # Overall Accuracy
    lines.append("-" * 70)
    lines.append("OVERALL ACCURACY")
    lines.append("-" * 70)
    lines.append(f"Overall Accuracy Rate:       {results['overall_accuracy']:.1%}")
    lines.append(f"Underestimation Rate:        {results['underestimation_rate']:.1%}")
    lines.append(f"Overestimation Rate:         {results['overestimation_rate']:.1%}")
    lines.append("")

    # Multiplier Analysis
    lines.append("-" * 70)
    lines.append("MULTIPLIER ANALYSIS")
    lines.append("-" * 70)
    lines.append(f"Current Multiplier:          {results.get('current_multiplier', 1.35)}x")
    lines.append(f"Recommended Multiplier:      {results['recommended_multiplier']:.2f}x")
    if results.get('multiplier_delta'):
        delta = results['multiplier_delta']
        direction = "increase" if delta > 0 else "decrease"
        lines.append(f"Adjustment Needed:           {abs(delta):.2f}x {direction}")
    lines.append("")

    # Accuracy by Category
    lines.append("-" * 70)
    lines.append("ACCURACY BY CATEGORY")
    lines.append("-" * 70)
    for category in ["good", "acceptable", "poor"]:
        cat_data = results["accuracy_by_category"].get(category, {"count": 0, "avg_accuracy": 0.0})
        count = cat_data["count"]
        pct = count / results['tasks_comparable'] * 100 if results['tasks_comparable'] > 0 else 0
        avg_acc = cat_data["avg_accuracy"]
        lines.append(f"  {category.capitalize():12} ({count:3d} tasks, {pct:5.1f}%): {avg_acc:.1%} avg accuracy")
    lines.append("")

    # Accuracy by Task Type
    lines.append("-" * 70)
    lines.append("ACCURACY BY TASK TYPE")
    lines.append("-" * 70)
    lines.append(f"{'Type':<15} {'Count':>8} {'Avg Acc':>10} {'Est Total':>12} {'Actual Total':>13} {'Multiplier':>11}")
    lines.append("-" * 70)

    for task_type, type_data in sorted(results["accuracy_by_type"].items()):
        count = type_data["count"]
        avg_acc = type_data.get("avg_accuracy", 0)
        total_est = type_data.get("total_estimated", 0)
        total_actual = type_data.get("total_actual", 0)
        multiplier = type_data.get("recommended_multiplier", 1.0)
        lines.append(f"{task_type:<15} {count:>8} {avg_acc:>9.1%} {total_est:>11}m {total_actual:>12}m {multiplier:>10.2f}x")
    lines.append("")

    # Recent Trends
    lines.append("-" * 70)
    lines.append("RECENT TASKS (Last 20)")
    lines.append("-" * 70)
    lines.append(f"{'Task ID':<30} {'Type':<10} {'Est':>6} {'Actual':>7} {'Diff':>7} {'Acc':>6}")
    lines.append("-" * 70)

    for task in results["trends"][:20]:
        task_id = task["task_id"][:28]
        task_type = (task.get("task_type") or "unknown")[:8]
        est = task.get("estimated_minutes", 0) or 0
        actual = task.get("actual_minutes", 0) or 0
        diff = task.get("difference", 0) or 0
        acc = task.get("accuracy", 0) or 0
        diff_str = f"+{diff:.0f}" if diff > 0 else f"{diff:.0f}"
        lines.append(f"{task_id:<30} {task_type:<10} {est:>6}m {actual:>6}m {diff_str:>7} {acc:>5.0%}")
    lines.append("")

    # Recommendations
    lines.append("-" * 70)
    lines.append("RECOMMENDATIONS")
    lines.append("-" * 70)

    if results['recommended_multiplier'] > results.get('current_multiplier', 1.35):
        lines.append(f"1. INCREASE multiplier from {results.get('current_multiplier', 1.35)}x to {results['recommended_multiplier']:.2f}x")
        lines.append("   Tasks are consistently taking longer than estimated.")
    elif results['recommended_multiplier'] < results.get('current_multiplier', 1.35):
        lines.append(f"1. DECREASE multiplier from {results.get('current_multiplier', 1.35)}x to {results['recommended_multiplier']:.2f}x")
        lines.append("   Tasks are completing faster than estimated.")
    else:
        lines.append(f"1. KEEP multiplier at {results.get('current_multiplier', 1.35)}x")
        lines.append("   Current multiplier is well-calibrated.")

    if results["underestimation_rate"] > 0.5:
        lines.append("2. Review estimation process - systematic underestimation detected.")
    if results["overall_accuracy"] < 0.6:
        lines.append("3. Consider adding buffers for unknown complexity tasks.")

    lines.append("")
    lines.append("=" * 70)

    return "\n".join(lines)


def generate_json_report(results: Dict) -> str:
    """Generate a JSON report."""
    # Convert defaultdict to regular dict for JSON serialization
    results_clean = {
        k: (dict(v) if isinstance(v, defaultdict) else v)
        for k, v in results.items()
    }
    return json.dumps(results_clean, indent=2, default=str)


def generate_yaml_report(results: Dict) -> str:
    """Generate a YAML report."""
    # Convert defaultdict to regular dict for YAML serialization
    results_clean = {
        k: (dict(v) if isinstance(v, defaultdict) else v)
        for k, v in results.items()
    }
    return yaml.dump(results_clean, default_flow_style=False, sort_keys=False)


def update_estimation_guidelines(results: Dict) -> bool:
    """Update the estimation guidelines file with new findings."""
    try:
        if not ESTIMATION_GUIDELINES_PATH.exists():
            print(f"Warning: Estimation guidelines not found at {ESTIMATION_GUIDELINES_PATH}")
            return False

        with open(ESTIMATION_GUIDELINES_PATH, 'r') as f:
            guidelines = yaml.safe_load(f)

        # Update version and date
        guidelines["Version"] = "1.2.0"
        guidelines["Last Updated"] = datetime.now().strftime("%Y-%m-%d")
        guidelines["Based On"] = f"Analysis of {results['tasks_comparable']} completed tasks"

        # Update universal multiplier if significantly different
        if abs(results.get('multiplier_delta', 0)) >= 0.1:
            old_multiplier = results.get('current_multiplier', 1.35)
            new_multiplier = results['recommended_multiplier']
            guidelines["Universal Estimation Multiplier"] = f"{new_multiplier:.2f}x"

            # Update the explanation
            for i, line in enumerate(guidelines.get("Historical analysis shows tasks are consistently underestimated by approximately 35%", [])):
                if "35%" in str(line):
                    pct = int((new_multiplier - 1) * 100)
                    guidelines["Historical analysis shows tasks are consistently underestimated by approximately 35%"][i] = \
                        f"Historical analysis shows tasks are consistently underestimated by approximately {pct}%."

        # Update baseline estimates by task type
        if "Baseline Estimates by Task Type" in guidelines:
            for task_type, type_data in results["accuracy_by_type"].items():
                if type_data["count"] >= 3:  # Only update if we have enough data
                    # Find and update the corresponding row in the table
                    pass  # Table updates would require more complex YAML manipulation

        with open(ESTIMATION_GUIDELINES_PATH, 'w') as f:
            yaml.dump(guidelines, f, default_flow_style=False, sort_keys=False)

        return True
    except Exception as e:
        print(f"Error updating guidelines: {e}")
        return False


def collect_run_durations() -> Dict[str, float]:
    """Collect actual durations from run metadata files."""
    durations = {}

    if not RUNS_DIR.exists():
        return durations

    # Search through all run directories
    for run_dir in RUNS_DIR.rglob("*"):
        if not run_dir.is_dir():
            continue

        metadata = parse_run_metadata(run_dir)
        if metadata and metadata["task_id"]:
            task_id = metadata["task_id"]
            # Keep the shortest duration if multiple runs for same task
            if task_id not in durations or metadata["actual_minutes"] < durations[task_id]:
                durations[task_id] = metadata["actual_minutes"]

    return durations


def main():
    parser = argparse.ArgumentParser(description="Track and analyze task estimation accuracy")
    parser.add_argument("--output", "-o", help="Output file path (default: stdout)")
    parser.add_argument("--format", "-f", choices=["text", "json", "yaml"], default="text",
                        help="Output format (default: text)")
    parser.add_argument("--days", "-d", type=int, help="Analyze tasks from last N days")
    parser.add_argument("--update-guidelines", action="store_true",
                        help="Update estimation-guidelines.yaml with findings")
    args = parser.parse_args()

    # Collect actual durations from runs
    run_durations = collect_run_durations()

    # Build a mapping of task IDs to directory names (task dirs may have suffixes)
    task_dir_mapping = {}
    if COMPLETED_TASKS_DIR.exists():
        for task_dir in COMPLETED_TASKS_DIR.iterdir():
            if task_dir.is_dir():
                # Extract task ID from directory name (e.g., TASK-1769910001-executor-dashboard -> TASK-1769910001)
                # Match TASK- followed by alphanumeric, stopping before lowercase suffix
                task_id_match = re.match(r'(TASK-[A-Z0-9]+(?:-[A-Z0-9]+)*)', task_dir.name)
                if task_id_match:
                    task_dir_mapping[task_id_match.group(1)] = task_dir

    # Collect all completed tasks
    tasks = []
    for task_id, task_dir in task_dir_mapping.items():
        task_file = task_dir / "task.md"
        if task_file.exists():
            task_data = parse_task_file(task_file)
            if task_data:
                # Merge with run duration if available
                if task_id in run_durations:
                    task_data["actual_minutes"] = run_durations[task_id]
                    task_data["duration_source"] = "run_metadata"
                tasks.append(task_data)

    # Filter by date if specified
    if args.days:
        cutoff_date = datetime.now() - timedelta(days=args.days)
        tasks = [
            t for t in tasks
            if t.get("completed") and parse_datetime(t["completed"])
            and parse_datetime(t["completed"]) >= cutoff_date
        ]

    # Analyze tasks
    results = analyze_tasks(tasks)

    # Generate report
    if args.format == "json":
        report = generate_json_report(results)
    elif args.format == "yaml":
        report = generate_yaml_report(results)
    else:
        report = generate_text_report(results)

    # Output report
    if args.output:
        with open(args.output, 'w') as f:
            f.write(report)
        print(f"Report written to {args.output}")
    else:
        print(report)

    # Update guidelines if requested
    if args.update_guidelines:
        if update_estimation_guidelines(results):
            print(f"\nUpdated {ESTIMATION_GUIDELINES_PATH}")
        else:
            print(f"\nFailed to update guidelines")

    return 0


if __name__ == "__main__":
    sys.exit(main())
