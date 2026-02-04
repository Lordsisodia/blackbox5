#!/usr/bin/env python3
"""Auto-sync STATE.yaml with actual filesystem state."""

import yaml
import os
from datetime import datetime
from pathlib import Path

def get_actual_tasks():
    """Get list of actual tasks from filesystem."""
    tasks_dir = Path("tasks/active")
    if not tasks_dir.exists():
        return []

    tasks = []
    for item in tasks_dir.iterdir():
        if item.is_dir() and item.name.startswith("TASK-"):
            # Try to read task title from task.md
            task_file = item / "task.md"
            title = item.name
            if task_file.exists():
                try:
                    with open(task_file, 'r') as f:
                        first_line = f.readline()
                        if first_line.startswith("# "):
                            title = first_line[2:].strip()
                except:
                    pass
            tasks.append({"id": item.name, "title": title})
    return tasks

def get_actual_goals():
    """Get list of actual goals from filesystem."""
    goals_dir = Path("goals/active")
    if not goals_dir.exists():
        return []

    goals = []
    for item in goals_dir.iterdir():
        if item.is_dir() and item.name.startswith("IG-"):
            goals.append(item.name)
    return sorted(goals)

def main():
    print("=" * 60)
    print("STATE.yaml Auto-Sync")
    print("=" * 60)

    # Load current STATE.yaml
    state_path = Path("STATE.yaml")
    if state_path.exists():
        with open(state_path, 'r') as f:
            state = yaml.safe_load(f) or {}
    else:
        state = {}

    # Get actual filesystem state
    print("\n[INFO] Syncing tasks...")
    actual_tasks = get_actual_tasks()
    print(f"[INFO] Found {len(actual_tasks)} active tasks")

    print("\n[INFO] Syncing goals...")
    actual_goals = get_actual_goals()
    print(f"[INFO] Found {len(actual_goals)} active goals")

    # Update state - preserve existing task data if present
    if "tasks" not in state:
        state["tasks"] = {}

    # Build new active tasks list, preserving metadata from existing
    existing_tasks = {t["id"]: t for t in state["tasks"].get("active", []) if isinstance(t, dict)}
    new_active_tasks = []
    for task in actual_tasks:
        task_id = task["id"]
        if task_id in existing_tasks:
            # Preserve existing metadata
            existing = existing_tasks[task_id].copy()
            existing["id"] = task_id  # Ensure ID is set
            new_active_tasks.append(existing)
        else:
            # New task
            new_active_tasks.append(task)

    state["tasks"]["active"] = new_active_tasks

    # Update metadata
    if "metadata" not in state:
        state["metadata"] = {}
    if "project" not in state:
        state["project"] = {}
    state["project"]["last_sync"] = datetime.now().isoformat()

    # Save
    with open(state_path, 'w') as f:
        yaml.dump(state, f, default_flow_style=False, sort_keys=False)

    print(f"\n[INFO] STATE.yaml updated successfully")
    print(f"[INFO] Active tasks: {len(new_active_tasks)}")
    print("=" * 60)

if __name__ == "__main__":
    main()
