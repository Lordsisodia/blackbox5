#!/usr/bin/env python3
"""
Sync BlackBox5 tasks to GitHub Issues

This script reads task state files from 5-project-memory/ and creates/updates
corresponding GitHub Issues with proper labels and metadata.
"""

import json
import os
import re
import sys
from pathlib import Path
from datetime import datetime

import requests
import yaml


# Configuration
TASK_MEMORY_DIR = Path("/opt/blackbox5/5-project-memory")
GITHUB_API_BASE = "https://api.github.com"
REPO_OWNER = "Lordsisodia"
REPO_NAME = "blackbox5"
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
TASK_ID = os.environ.get("TASK_ID")
FORCE_SYNC = os.environ.get("FORCE_SYNC", "false").lower() == "true"

# Label mappings
STATUS_LABELS = {
    "pending": "🔄 In Progress",
    "in_progress": "🔄 In Progress",
    "complete": "✅ Done",
    "failed": "❌ Failed",
    "initialized": "📝 Planning",
}

PRIORITY_LABELS = {
    "high": "🔥 High Priority",
    "medium": "⚡ Medium Priority",
    "low": "🌱 Low Priority",
}


def get_github_headers():
    """Get headers for GitHub API requests."""
    return {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json",
    }


def get_existing_issues():
    """Get all existing issues with BlackBox5 metadata."""
    issues = []
    page = 1
    while True:
        response = requests.get(
            f"{GITHUB_API_BASE}/repos/{REPO_OWNER}/{REPO_NAME}/issues",
            headers=get_github_headers(),
            params={"state": "all", "page": page, "per_page": 100},
        )
        response.raise_for_status()
        batch = response.json()
        if not batch:
            break
        issues.extend(batch)
        page += 1
    return issues


def find_issue_for_task(task_id, issues):
    """Find existing GitHub issue for a task."""
    for issue in issues:
        if issue.get("body") and f"Task ID: {task_id}" in issue["body"]:
            return issue
    return None


def format_issue_body(task_data):
    """Format task data into GitHub issue body."""
    body = f"""## BlackBox5 Task

**Task ID:** {task_data.get('id', 'N/A')}
**Status:** {task_data.get('status', 'N/A')}
**Created:** {task_data.get('created_at', 'N/A')}

### Objective

{task_data.get('objective', 'No objective provided')}

### Subtasks

"""

    subtasks = task_data.get('subtasks', [])
    if subtasks:
        for i, subtask in enumerate(subtasks, 1):
            body += f"{i}. **[{subtask.get('status', 'pending').upper()}]** {subtask.get('title', 'Untitled')}\n"
    else:
        body += "No subtasks defined\n"

    body += f"""
### Metadata

- **Current Depth:** {task_data.get('current_depth', 0)}
- **Max Depth:** {task_data.get('max_depth', 3)}
- **Root Path:** `{task_data.get('root_path', 'N/A')}`

---
*This issue is automatically synced from BlackBox5 task system*
"""

    return body


def get_labels_for_task(task_data):
    """Generate labels for a task."""
    labels = ["blackbox5-task"]

    # Status label
    status = task_data.get('status', 'pending')
    if status in STATUS_LABELS:
        labels.append(STATUS_LABELS[status])

    # Check subtasks for priority hints
    subtasks = task_data.get('subtasks', [])
    if len(subtasks) > 10:
        labels.append(PRIORITY_LABELS.get('high', '🔥 High Priority'))
    elif len(subtasks) > 5:
        labels.append(PRIORITY_LABELS.get('medium', '⚡ Medium Priority'))
    else:
        labels.append(PRIORITY_LABELS.get('low', '🌱 Low Priority'))

    return labels


def create_issue(task_data):
    """Create a new GitHub issue for a task."""
    body = format_issue_body(task_data)
    labels = get_labels_for_task(task_data)

    data = {
        "title": f"[Task {task_data.get('id', 'Unknown')}] {task_data.get('objective', 'No objective')[:80]}",
        "body": body,
        "labels": labels,
    }

    response = requests.post(
        f"{GITHUB_API_BASE}/repos/{REPO_OWNER}/{REPO_NAME}/issues",
        headers=get_github_headers(),
        json=data,
    )
    response.raise_for_status()
    return response.json()


def update_issue(issue, task_data):
    """Update an existing GitHub issue."""
    body = format_issue_body(task_data)
    labels = get_labels_for_task(task_data)
    state = "open" if task_data.get('status') not in ['complete', 'failed'] else "closed"

    data = {
        "title": f"[Task {task_data.get('id', 'Unknown')}] {task_data.get('objective', 'No objective')[:80]}",
        "body": body,
        "labels": labels,
        "state": state,
    }

    response = requests.patch(
        f"{GITHUB_API_BASE}/repos/{REPO_OWNER}/{REPO_NAME}/issues/{issue['number']}",
        headers=get_github_headers(),
        json=data,
    )
    response.raise_for_status()
    return response.json()


def find_all_task_files():
    """Find all task state.json files."""
    task_files = []
    for project_dir in TASK_MEMORY_DIR.glob("*/tasks/*"):
        if project_dir.is_dir():
            state_file = project_dir / "state.json"
            if state_file.exists():
                task_files.append(state_file)
    return task_files


def main():
    """Main sync function."""
    if not GITHUB_TOKEN:
        print("ERROR: GITHUB_TOKEN not set")
        sys.exit(1)

    print("🔄 Starting task sync to GitHub...")

    # Get existing issues
    existing_issues = get_existing_issues()
    print(f"📋 Found {len(existing_issues)} existing issues")

    # Find task files
    task_files = find_all_task_files()
    print(f"📁 Found {len(task_files)} task files")

    # Sync each task
    synced = 0
    created = 0
    updated = 0
    errors = 0

    for task_file in task_files:
        try:
            with open(task_file) as f:
                task_data = json.load(f)

            task_id = task_data.get('id')

            # Filter by specific task ID if provided
            if TASK_ID and task_id != TASK_ID:
                continue

            # Find existing issue
            existing_issue = find_issue_for_task(task_id, existing_issues)

            if existing_issue:
                # Update existing issue
                update_issue(existing_issue, task_data)
                updated += 1
                print(f"✅ Updated issue for task {task_id}")
            else:
                # Create new issue
                create_issue(task_data)
                created += 1
                print(f"✨ Created issue for task {task_id}")

            synced += 1

        except Exception as e:
            errors += 1
            print(f"❌ Error syncing task {task_file}: {e}")

    print(f"\n📊 Sync complete:")
    print(f"   Created: {created}")
    print(f"   Updated: {updated}")
    print(f"   Errors: {errors}")
    print(f"   Total synced: {synced}")


if __name__ == "__main__":
    main()
