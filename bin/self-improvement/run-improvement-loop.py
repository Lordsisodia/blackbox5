#!/usr/bin/env python3
"""
BlackBox5 Autonomous Self-Improvement Loop
Runs every 30 minutes to analyze systems, identify improvements, and execute them.
"""

import os
import sys
import json
import subprocess
import shutil
import re
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Dict, List, Any

# Configuration
BB5_DIR = Path("/opt/blackbox5")
AUTONOMOUS_DIR = BB5_DIR / ".autonomous" / "self-improvement"
LOGS_DIR = AUTONOMOUS_DIR / "logs"
RUNS_DIR = AUTONOMOUS_DIR / "runs"
METRICS_DIR = AUTONOMOUS_DIR / "metrics"
TASKS_DIR = BB5_DIR / "5-project-memory" / "blackbox5" / "tasks"
TASKS_ACTIVE_DIR = TASKS_DIR / "active"
TASKS_IMPROVEMENTS_DIR = TASKS_DIR / "improvements"
TASKS_BLOCKED_DIR = TASKS_DIR / "blocked"
TASKS_COMPLETED_DIR = TASKS_DIR / "completed"

# Ensure directories exist
for d in [AUTONOMOUS_DIR, LOGS_DIR, RUNS_DIR, METRICS_DIR, TASKS_IMPROVEMENTS_DIR]:
    d.mkdir(parents=True, exist_ok=True)

def get_timestamp() -> str:
    """Get current ISO timestamp."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def get_log_file() -> Path:
    """Get today's log file path."""
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    return LOGS_DIR / f"improvement-{today}.log"

def log(message: str, level: str = "INFO"):
    """Write message to log file and stdout."""
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{timestamp}] [{level}] {message}"
    print(log_line, flush=True)

    log_file = get_log_file()
    with open(log_file, "a") as f:
        f.write(log_line + "\n")

def load_metrics() -> Dict[str, Any]:
    """Load historical metrics."""
    metrics_file = METRICS_DIR / "history.json"
    if metrics_file.exists():
        with open(metrics_file, "r") as f:
            return json.load(f)
    return {"runs": [], "summary": {
        "total_runs": 0,
        "total_improvements": 0,
        "success_rate": 1.0,
        "avg_duration": 0,
        "top_improvement_categories": []
    }}

def save_metrics(metrics: Dict[str, Any]):
    """Save metrics to file."""
    metrics_file = METRICS_DIR / "history.json"
    with open(metrics_file, "w") as f:
        json.dump(metrics, f, indent=2)

def scan_system() -> Dict[str, Any]:
    """Phase 1: Scan system health and status."""
    log("Phase 1: System Scan")

    system_state = {
        "active_tasks": 0,
        "stuck_tasks": [],
        "improvement_tasks": 0,
        "error_count": 0,
        "warning_count": 0,
        "log_file_sizes": {},
        "large_log_files": []
    }

    # Scan active tasks
    if TASKS_ACTIVE_DIR.exists():
        task_dirs = list(TASKS_ACTIVE_DIR.rglob("TASK-*/task.md"))
        system_state["active_tasks"] = len(task_dirs)

        # Check for stuck tasks (in_progress > 4 hours)
        now = datetime.now(timezone.utc)
        four_hours_ago = now - timedelta(hours=4)

        for task_file in task_dirs:
            try:
                with open(task_file, "r") as f:
                    content = f.read()
                    if "**Status:** in_progress" in content:
                        mtime = datetime.fromtimestamp(task_file.stat().st_mtime, tz=timezone.utc)
                        if mtime < four_hours_ago:
                            system_state["stuck_tasks"].append(str(task_file))
            except Exception as e:
                log(f"Error reading task {task_file}: {e}", "WARNING")

    # Scan improvement tasks
    if TASKS_IMPROVEMENTS_DIR.exists():
        system_state["improvement_tasks"] = len(list(TASKS_IMPROVEMENTS_DIR.glob("TASK-*/task.md")))

    # Scan log files for errors
    executor_log = BB5_DIR / ".autonomous" / "logs" / "ralf-executor.log"
    if executor_log.exists():
        try:
            with open(executor_log, "r") as f:
                lines = f.readlines()[-100:]  # Last 100 lines
                for line in lines:
                    if "ERROR" in line.upper():
                        system_state["error_count"] += 1
                    elif "WARNING" in line.upper():
                        system_state["warning_count"] += 1
        except Exception as e:
            log(f"Error reading executor log: {e}", "WARNING")

    # Check log file sizes
    for log_file in LOGS_DIR.glob("improvement-*.log"):
        try:
            size_mb = log_file.stat().st_size / (1024 * 1024)
            system_state["log_file_sizes"][log_file.name] = {
                "size_mb": round(size_mb, 2),
                "needs_rotation": size_mb > 10
            }
            if size_mb > 10:
                system_state["large_log_files"].append(str(log_file))
        except Exception:
            pass

    log(f"  - Active tasks: {system_state['active_tasks']}")
    log(f"  - Stuck tasks: {len(system_state['stuck_tasks'])}")
    log(f"  - Improvement tasks: {system_state['improvement_tasks']}")
    log(f"  - Error count: {system_state['error_count']}")
    log(f"  - Warning count: {system_state['warning_count']}")
    log(f"  - Large log files: {len(system_state['large_log_files'])}")

    return system_state

def identify_improvements(system_state: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Phase 2: Identify improvement opportunities."""
    log("Phase 2: Opportunity Identification")

    improvements = []

    # Pattern 1: Task Cleanup
    if system_state["stuck_tasks"]:
        improvements.append({
            "category": "task_cleanup",
            "title": f"Move {len(system_state['stuck_tasks'])} stuck tasks to blocked",
            "description": f"Found {len(system_state['stuck_tasks'])} tasks in_progress for >4 hours",
            "impact": 5,
            "frequency": 8,
            "effort": 2,
            "risk": 1,
            "safe": True,
            "action": "move_stuck_tasks",
            "data": system_state["stuck_tasks"]
        })

    # Pattern 2: Log Rotation
    if system_state["large_log_files"]:
        improvements.append({
            "category": "log_rotation",
            "title": f"Archive {len(system_state['large_log_files'])} large log files",
            "description": f"Log files >10MB: {len(system_state['large_log_files'])} files",
            "impact": 6,
            "frequency": 5,
            "effort": 3,
            "risk": 1,
            "safe": True,
            "action": "rotate_logs",
            "data": system_state["large_log_files"]
        })

    # Pattern 3: Error Detection
    if system_state["error_count"] > 5:
        improvements.append({
            "category": "error_detection",
            "title": f"Investigate {system_state['error_count']} recent errors",
            "description": f"High error rate detected in executor logs",
            "impact": 8,
            "frequency": 6,
            "effort": 6,
            "risk": 3,
            "safe": True,
            "action": "investigate_errors",
            "data": system_state["error_count"]
        })

    # Pattern 4: Warning Trends
    if system_state["warning_count"] > 20:
        improvements.append({
            "category": "warning_trends",
            "title": f"Review {system_state['warning_count']} warnings for patterns",
            "description": "High warning count may indicate systemic issues",
            "impact": 4,
            "frequency": 4,
            "effort": 4,
            "risk": 1,
            "safe": True,
            "action": "review_warnings",
            "data": system_state["warning_count"]
        })

    # Pattern 5: Task Backlog
    if system_state["active_tasks"] > 20:
        improvements.append({
            "category": "task_backlog",
            "title": f"Review {system_state['active_tasks']} active tasks for prioritization",
            "description": "Large task backlog may need triage",
            "impact": 5,
            "frequency": 3,
            "effort": 5,
            "risk": 2,
            "safe": True,
            "action": "review_backlog",
            "data": system_state["active_tasks"]
        })

    log(f"  - Found {len(improvements)} improvement opportunities")

    # Calculate and display scores
    for imp in improvements:
        score = (imp["impact"] * 10) + (imp["frequency"] * 5) - (imp["effort"] * 3) - (imp["risk"] * 5)
        imp["score"] = score
        priority = "HIGH" if score >= 30 else "MEDIUM" if score >= 15 else "LOW"
        imp["priority"] = priority
        log(f"  - {imp['category']}: Score={score} ({priority})")

    return improvements

def prioritize_improvements(improvements: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Phase 3: Prioritize and select improvements."""
    log("Phase 3: Prioritization")

    # Sort by score descending
    improvements.sort(key=lambda x: x["score"], reverse=True)

    # Select high-priority improvements (score >= 30)
    selected = [imp for imp in improvements if imp["score"] >= 30]

    # Also select medium priority if few high priority
    if len(selected) < 3:
        medium = [imp for imp in improvements if 15 <= imp["score"] < 30]
        selected.extend(medium[:3 - len(selected)])

    # Limit to top 3
    selected = selected[:3]

    log(f"  - Selected {len(selected)} improvements (Score >= 15)")
    for imp in selected:
        log(f"    - {imp['title']}")

    return selected

def create_improvement_task(improvement: Dict[str, Any]) -> str:
    """Create a task file for the improvement."""
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    task_id = f"TASK-AUTO-{timestamp}"

    task_dir = TASKS_IMPROVEMENTS_DIR / task_id
    task_dir.mkdir(parents=True, exist_ok=True)

    task_content = f"""# {task_id}: {improvement['title']}

**Status:** in_progress
**Priority:** {improvement['priority']}
**Type:** autonomous_improvement
**Category:** {improvement['category']}
**Created:** {get_timestamp()}
**Agent:** bb5-self-improvement
**Score:** {improvement['score']}

## Objective
{improvement['description']}

## Problem Statement
{improvement['description']}

## Current State
Detected during autonomous self-improvement scan.

## Proposed Improvement
Execute the improvement action to address the identified issue.

## Implementation Plan
1. Analyze the current state
2. Execute the improvement action
3. Verify the change was successful
4. Document results

## Success Criteria
- [ ] Improvement successfully applied
- [ ] No system instability
- [ ] Logs updated with results

## Rollback Strategy
If system becomes unstable, reverse the change immediately.

## Risk Assessment
- **Risk Level:** {"LOW" if improvement['risk'] <= 1 else "MEDIUM" if improvement['risk'] <= 2 else "HIGH"}
- **Impact if Wrong:** System degradation or instability
- **Reversibility:** {"Easy" if improvement['safe'] else "Medium"}
"""

    task_file = task_dir / "task.md"
    with open(task_file, "w") as f:
        f.write(task_content)

    return task_id

def execute_task_cleanup(stuck_tasks: List[str]) -> bool:
    """Execute task cleanup: move stuck tasks to blocked folder."""
    log("    Action: Moving stuck tasks to blocked folder")

    # Ensure blocked folder exists
    TASKS_BLOCKED_DIR.mkdir(parents=True, exist_ok=True)

    moved_count = 0
    for task_path in stuck_tasks:
        try:
            task_file = Path(task_path)
            task_dir = task_file.parent
            task_name = task_dir.name

            # Create blocked task path
            blocked_task_dir = TASKS_BLOCKED_DIR / task_name

            # Move the entire task directory
            if task_dir.exists() and not blocked_task_dir.exists():
                shutil.move(str(task_dir), str(blocked_task_dir))
                moved_count += 1
                log(f"      Moved: {task_name}")

                # Update task status in moved file
                new_task_file = blocked_task_dir / "task.md"
                if new_task_file.exists():
                    with open(new_task_file, "r") as f:
                        content = f.read()
                    content = content.replace("**Status:** in_progress", "**Status:** blocked")
                    with open(new_task_file, "w") as f:
                        f.write(content)

        except Exception as e:
            log(f"      Failed to move {task_path}: {e}", "ERROR")
            return False

    log(f"    → SUCCESS: Moved {moved_count} tasks")
    return True

def execute_log_rotation(log_files: List[str]) -> bool:
    """Execute log rotation: archive large log files."""
    log("    Action: Rotating large log files")

    archive_dir = LOGS_DIR / "archive"
    archive_dir.mkdir(parents=True, exist_ok=True)

    rotated_count = 0
    for log_path in log_files:
        try:
            log_file = Path(log_path)
            archive_name = f"{log_file.stem}-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}{log_file.suffix}"
            archive_path = archive_dir / archive_name

            # Move log to archive
            shutil.move(str(log_file), str(archive_path))
            rotated_count += 1
            log(f"      Archived: {log_file.name} → {archive_name}")

            # Compress if possible
            try:
                subprocess.run(["gzip", str(archive_path)], check=True, capture_output=True)
                log(f"      Compressed: {archive_name}.gz")
            except:
                pass  # Compression is optional

        except Exception as e:
            log(f"      Failed to rotate {log_path}: {e}", "ERROR")
            return False

    log(f"    → SUCCESS: Rotated {rotated_count} log files")
    return True

def execute_improvement(improvement: Dict[str, Any]) -> bool:
    """Execute a single improvement action."""
    action = improvement.get("action", "")
    data = improvement.get("data", [])

    log(f"  Executing: {improvement['category']} - {improvement['title']}")

    if action == "move_stuck_tasks":
        return execute_task_cleanup(data)

    elif action == "rotate_logs":
        return execute_log_rotation(data)

    elif action == "investigate_errors":
        log("    Action: Error investigation (logged for review)")
        # For now, just log it - this would need more sophisticated analysis
        log(f"      Found {data} errors - flagged for human review")
        log("    → SUCCESS: Logged for review")
        return True

    elif action == "review_warnings":
        log("    Action: Warning review (logged for review)")
        log(f"      Found {data} warnings - monitoring trend")
        log("    → SUCCESS: Logged for monitoring")
        return True

    elif action == "review_backlog":
        log("    Action: Backlog review (logged for review)")
        log(f"      Current backlog: {data} tasks")
        log("    → SUCCESS: Logged for monitoring")
        return True

    else:
        log(f"    Unknown action: {action}", "WARNING")
        return False

def execute_improvements(improvements: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Phase 4: Execute selected improvements."""
    log("Phase 4: Execution")

    results = {
        "attempted": len(improvements),
        "succeeded": 0,
        "failed": 0,
        "tasks_created": []
    }

    for improvement in improvements:
        if not improvement.get("safe", False):
            log(f"  Skipping {improvement['category']} (not safe for autonomous execution)")
            continue

        # Create task
        task_id = create_improvement_task(improvement)
        results["tasks_created"].append(task_id)
        log(f"    Created task: {task_id}")

        # Execute improvement
        success = execute_improvement(improvement)

        if success:
            results["succeeded"] += 1

            # Update task status to completed
            task_file = TASKS_IMPROVEMENTS_DIR / task_id / "task.md"
            if task_file.exists():
                with open(task_file, "r") as f:
                    content = f.read()
                content = content.replace("**Status:** in_progress", "**Status:** completed")
                with open(task_file, "w") as f:
                    f.write(content)

            # Move to completed
            task_dir = TASKS_IMPROVEMENTS_DIR / task_id
            completed_dir = TASKS_DIR / "completed" / task_id
            if task_dir.exists():
                shutil.move(str(task_dir), str(completed_dir))

        else:
            results["failed"] += 1

    return results

def update_metrics(start_time: datetime, system_state: Dict[str, Any],
                   results: Dict[str, Any]) -> Dict[str, Any]:
    """Update metrics history."""
    log("Updating metrics...")

    duration = (datetime.now(timezone.utc) - start_time).total_seconds()
    success_rate = results["succeeded"] / results["attempted"] if results["attempted"] > 0 else 1.0

    metrics = load_metrics()

    # Add run record
    run_record = {
        "timestamp": get_timestamp(),
        "duration_seconds": duration,
        "system_checks": system_state,
        "improvements_attempted": results["attempted"],
        "improvements_succeeded": results["succeeded"],
        "improvements_failed": results["failed"],
        "tasks_created": results["tasks_created"],
        "success_rate": success_rate
    }

    metrics["runs"].append(run_record)

    # Update summary
    metrics["summary"]["total_runs"] += 1
    metrics["summary"]["total_improvements"] += results["attempted"]
    metrics["summary"]["avg_duration"] = (
        (metrics["summary"]["avg_duration"] * (metrics["summary"]["total_runs"] - 1) + duration) /
        metrics["summary"]["total_runs"]
    )

    # Calculate rolling success rate (last 20 runs)
    recent_runs = metrics["runs"][-20:]
    if recent_runs:
        metrics["summary"]["success_rate"] = sum(r.get("success_rate", 0) for r in recent_runs) / len(recent_runs)

    save_metrics(metrics)

    return metrics

def main():
    """Main improvement loop."""
    start_time = datetime.now(timezone.utc)
    start_timestamp = get_timestamp()

    log("=" * 60)
    log(f"STARTING SELF-IMPROVEMENT RUN")
    log(f"Timestamp: {start_timestamp}")
    log("=" * 60)

    try:
        # Phase 1: Scan system
        system_state = scan_system()

        # Phase 2: Identify improvements
        improvements = identify_improvements(system_state)

        # Phase 3: Prioritize
        selected_improvements = prioritize_improvements(improvements)

        # Phase 4: Execute
        results = execute_improvements(selected_improvements)

        # Update metrics
        metrics = update_metrics(start_time, system_state, results)

        # Summary
        duration = (datetime.now(timezone.utc) - start_time).total_seconds()

        log("=" * 60)
        log("RUN COMPLETE")
        log(f"Duration: {int(duration)} seconds")
        log(f"Improvements: {results['attempted']} attempted, {results['succeeded']} succeeded, {results['failed']} failed")
        log(f"Success Rate: {metrics['summary']['success_rate']:.1%}")
        log("=" * 60)

        return 0

    except Exception as e:
        log(f"FATAL ERROR: {e}", "ERROR")
        import traceback
        log(traceback.format_exc(), "ERROR")
        return 1

if __name__ == "__main__":
    sys.exit(main())
