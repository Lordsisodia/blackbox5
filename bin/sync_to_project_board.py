#!/usr/bin/env python3
"""
Sync GitHub Issues to Project Board.

This script adds issues to the appropriate columns in a GitHub Project board.
"""

import json
import os
from pathlib import Path


# Configuration
PROJECT_NUMBER = 1  # Update with your project number
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN") or os.environ.get("PROJECT_TOKEN")
REPO_OWNER = os.environ.get("GITHUB_REPOSITORY_OWNER", "Lordsisodia")
REPO_NAME = os.environ.get("GITHUB_REPOSITORY_NAME", "blackbox5")
ISSUE_NUMBER = int(os.environ.get("ISSUE_NUMBER", "0")) if os.environ.get("ISSUE_NUMBER") else None
ISSUE_TITLE = os.environ.get("ISSUE_TITLE", "")
ISSUE_STATE = os.environ.get("ISSUE_STATE", "open")

# Mapping from issue state/labels to project column
COLUMN_MAPPING = {
    "open": "To Do",
    "closed": "Done",
    "in_progress": "In Progress",
}

# Label-based column mapping
LABEL_COLUMN_MAPPING = {
    "🔄 In Progress": "In Progress",
    "✅ Done": "Done",
    "📝 Planning": "Planning",
    "🔥 High Priority": "To Do",
    "⚡ Medium Priority": "To Do",
    "🌱 Low Priority": "Backlog",
}


def get_github_headers():
    """Get headers for GitHub API requests."""
    return {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json",
    }


def get_project_board():
    """Get the project board details."""
    import requests

    # Get all projects for the repository
    response = requests.get(
        f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/projects",
        headers=get_github_headers(),
    )
    response.raise_for_status()
    projects = response.json()

    if not projects:
        print("No projects found")
        return None

    # Use the first project
    return projects[0]


def get_project_columns(project_id):
    """Get all columns in a project."""
    import requests

    response = requests.get(
        f"https://api.github.com/projects/{project_id}/columns",
        headers=get_github_headers(),
    )
    response.raise_for_status()
    return response.json()


def get_column_id(columns, column_name):
    """Get column ID by name."""
    for column in columns:
        if column['name'].lower() == column_name.lower():
            return column['id']
    return None


def add_issue_to_column(issue_number, column_id):
    """Add issue to a project column."""
    import requests

    # Create a card for the issue
    response = requests.post(
        f"https://api.github.com/projects/columns/{column_id}/cards",
        headers=get_github_headers(),
        json={"content_id": issue_number, "content_type": "Issue"},
    )
    response.raise_for_status()
    return response.json()


def get_issue_labels(issue_number):
    """Get labels for an issue."""
    import requests

    response = requests.get(
        f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/issues/{issue_number}",
        headers=get_github_headers(),
    )
    response.raise_for_status()
    issue = response.json()

    return [label['name'] for label in issue.get('labels', [])]


def determine_target_column(issue_state, labels):
    """Determine which column to place the issue in."""
    # Check for label-based mapping first
    for label in labels:
        if label in LABEL_COLUMN_MAPPING:
            return LABEL_COLUMN_MAPPING[label]

    # Fall back to state-based mapping
    return COLUMN_MAPPING.get(issue_state, "To Do")


def main():
    """Main sync function."""
    if not GITHUB_TOKEN:
        print("ERROR: GITHUB_TOKEN or PROJECT_TOKEN not set")
        return

    if not ISSUE_NUMBER:
        print("ERROR: ISSUE_NUMBER not set")
        return

    print(f"🔄 Syncing issue #{ISSUE_NUMBER} to project board...")

    # Get project board
    project = get_project_board()
    if not project:
        return

    project_id = project['id']
    print(f"📋 Using project: {project['name']}")

    # Get project columns
    columns = get_project_columns(project_id)
    print(f"📁 Found {len(columns)} columns")

    # Get issue labels
    labels = get_issue_labels(ISSUE_NUMBER)
    print(f"🏷️  Labels: {', '.join(labels)}")

    # Determine target column
    target_column = determine_target_column(ISSUE_STATE, labels)
    print(f"📌 Target column: {target_column}")

    # Get column ID
    column_id = get_column_id(columns, target_column)
    if not column_id:
        print(f"ERROR: Column '{target_column}' not found")
        return

    # Add issue to column
    try:
        card = add_issue_to_column(ISSUE_NUMBER, column_id)
        print(f"✅ Issue added to column: {target_column}")
    except Exception as e:
        # Card might already exist, which is fine
        if "already exists" in str(e):
            print(f"ℹ️  Issue already in project board")
        else:
            print(f"WARNING: {e}")


if __name__ == "__main__":
    main()
