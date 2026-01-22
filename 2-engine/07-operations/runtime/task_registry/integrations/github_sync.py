"""GitHub sync integration for the Task Registry."""

import subprocess
import json
from pathlib import Path
from typing import Optional


class GitHubSync:
    """Synchronizes tasks with GitHub issues."""
    
    def __init__(self, registry_path: str | Path = "data/task_registry.json"):
        self.registry_path = Path(registry_path)
    
    def run_gh_command(self, args: list[str]) -> str:
        """Run a GitHub CLI command and return the output."""
        result = subprocess.run(
            ["gh"] + args,
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout
    
    def create_issue_for_task(self, task: dict) -> Optional[int]:
        """Create a GitHub issue for a task.
        
        Returns:
            The issue number if successful, None otherwise
        """
        if task.get("github_issue"):
            return task["github_issue"]
        
        # Build issue body
        body = f"""**Task ID**: {task['id']}

**Description**: {task.get('description', 'No description')}

**Objective**: {task.get('objective')}
**Phase**: {task.get('phase', 'N/A')}
**Priority**: {task.get('priority', 'medium')}

**Dependencies**: {', '.join(task.get('dependencies', [])) or 'None'}
**Blocks**: {', '.join(task.get('blocks', [])) or 'None'}

**Tags**: {', '.join(task.get('tags', [])) or 'None'}

---
*This issue was automatically created from the Task Registry.*
"""
        
        try:
            # Create the issue
            output = self.run_gh_command([
                "issue", "create",
                "--title", f"[Task] {task['title']}",
                "--body", body,
                "--label", "task", task.get('objective', ''),
            ])
            
            # Parse issue number from output
            # Output format: "https://github.com/owner/repo/issues/123"
            issue_url = output.strip()
            issue_number = int(issue_url.split('/')[-1])
            
            return issue_number
        
        except subprocess.CalledProcessError as e:
            print(f"Failed to create GitHub issue: {e.stderr}")
            return None
    
    def update_issue_state(self, task: dict):
        """Update the state of a GitHub issue based on task state."""
        if not task.get("github_issue"):
            return
        
        issue_number = task["github_issue"]
        task_state = task.get("state")
        
        # Map task states to GitHub issue states
        if task_state in ["BACKLOG", "ASSIGNED", "ACTIVE"]:
            gh_state = "open"
        elif task_state == "DONE":
            gh_state = "closed"
        else:  # FAILED or other
            gh_state = "open"
        
        try:
            self.run_gh_command([
                "issue", "edit", str(issue_number),
                "--state", gh_state,
            ])
        except subprocess.CalledProcessError as e:
            print(f"Failed to update GitHub issue #{issue_number}: {e.stderr}")
    
    def close_issue(self, task: dict):
        """Close a GitHub issue when a task is complete."""
        if not task.get("github_issue"):
            return
        
        issue_number = task["github_issue"]
        
        try:
            self.run_gh_command([
                "issue", "close", str(issue_number),
                "--comment", f"Task completed at {task.get('completed_at', 'unknown')}",
            ])
        except subprocess.CalledProcessError as e:
            print(f"Failed to close GitHub issue #{issue_number}: {e.stderr}")
    
    def sync_task_to_github(self, task_id: str, registry_data: dict) -> dict:
        """Sync a single task to GitHub.
        
        Returns:
            Updated task data with GitHub issue number
        """
        tasks = registry_data.get("tasks", {})
        task = tasks.get(task_id)
        
        if not task:
            print(f"Task {task_id} not found")
            return task
        
        # Create issue if it doesn't exist
        if not task.get("github_issue"):
            issue_number = self.create_issue_for_task(task)
            if issue_number:
                task["github_issue"] = issue_number
                task["github_url"] = f"https://github.com/siso-agency-internal/issues/{issue_number}"
        
        # Update issue state based on task state
        self.update_issue_state(task)
        
        return task
    
    def sync_all_to_github(self, registry_data: dict) -> dict:
        """Sync all tasks to GitHub.
        
        Returns:
            Updated registry data with GitHub issue numbers
        """
        tasks = registry_data.get("tasks", {})
        
        for task_id, task in tasks.items():
            self.sync_task_to_github(task_id, registry_data)
        
        return registry_data
    
    def sync_from_github(self, task_id: str, registry_data: dict) -> dict:
        """Sync task state from GitHub (for bidirectional sync).
        
        This checks if a GitHub issue is closed and updates the task state accordingly.
        
        Returns:
            Updated registry data
        """
        tasks = registry_data.get("tasks", {})
        task = tasks.get(task_id)
        
        if not task or not task.get("github_issue"):
            return registry_data
        
        issue_number = task["github_issue"]
        
        try:
            # Get issue state from GitHub
            output = self.run_gh_command([
                "issue", "view", str(issue_number),
                "--json", "state,closedAt",
            ])
            
            issue_data = json.loads(output)
            
            # If issue is closed and task is not done, update task
            if issue_data.get("state") == "CLOSED" and task.get("state") != "DONE":
                task["state"] = "DONE"
                task["completed_at"] = issue_data.get("closedAt")
        
        except subprocess.CalledProcessError as e:
            print(f"Failed to sync from GitHub for issue #{issue_number}: {e.stderr}")
        
        return registry_data


# CLI command for manual sync
def sync_github_command(registry_path: str = "data/task_registry.json"):
    """Sync all tasks to GitHub (CLI command)."""
    sync = GitHubSync(registry_path)
    
    with open(registry_path, "r") as f:
        registry_data = json.load(f)
    
    print("Syncing tasks to GitHub...")
    updated_data = sync.sync_all_to_github(registry_data)
    
    # Save updated registry
    with open(registry_path, "w") as f:
        json.dump(updated_data, f, indent=2)
    
    print("Sync complete.")


if __name__ == "__main__":
    import sys
    registry_path = sys.argv[1] if len(sys.argv) > 1 else "data/task_registry.json"
    sync_github_command(registry_path)
