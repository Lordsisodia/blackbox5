"""Vibe Kanban integration for the Task Registry."""

import json
from pathlib import Path
from typing import List, Dict
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class VibeKanbanHandler(FileSystemEventHandler):
    """File system event handler for task registry changes."""
    
    def __init__(self, callback):
        self.callback = callback
        self.registry_path = None
    
    def on_modified(self, event):
        """Called when task_registry.json is modified."""
        if event.src_path.endswith("task_registry.json"):
            self.callback()


class VibeKanbanIntegration:
    """Integrates the Task Registry with Vibe Kanban."""
    
    def __init__(self, registry_path: str | Path = "data/task_registry.json"):
        self.registry_path = Path(registry_path)
        self.observer = None
    
    def get_active_tasks(self) -> List[Dict]:
        """Get all active tasks for display in Vibe Kanban.
        
        Vibe Kanban only shows tasks where state == "ACTIVE".
        """
        if not self.registry_path.exists():
            return []
        
        with open(self.registry_path, "r") as f:
            registry = json.load(f)
        
        active_tasks = []
        for task_id, task_data in registry.get("tasks", {}).items():
            if task_data.get("state") == "ACTIVE":
                active_tasks.append({
                    "id": task_id,
                    "title": task_data.get("title"),
                    "description": task_data.get("description"),
                    "assignee": task_data.get("assignee"),
                    "started_at": task_data.get("started_at"),
                    "objective": task_data.get("objective"),
                    "phase": task_data.get("phase"),
                })
        
        return active_tasks
    
    def start_watching(self, callback):
        """Start watching the task registry file for changes.
        
        Args:
            callback: Function to call when registry changes
        """
        handler = VibeKanbanHandler(callback)
        handler.registry_path = str(self.registry_path)
        
        self.observer = Observer()
        # Watch the directory containing the registry file
        self.observer.schedule(
            handler,
            path=str(self.registry_path.parent),
            recursive=False
        )
        self.observer.start()
    
    def stop_watching(self):
        """Stop watching the task registry file."""
        if self.observer:
            self.observer.stop()
            self.observer.join()
            self.observer = None


# Example usage for Vibe Kanban frontend:
def refresh_kanban_display(active_tasks: List[Dict]):
    """Callback function to refresh the Kanban display."""
    print(f"Refreshing Vibe Kanban with {len(active_tasks)} active tasks")
    for task in active_tasks:
        print(f"  📋 {task['id']}: {task['title']} ({task['assignee']})")


def main():
    """Example usage of the Vibe Kanban integration."""
    integration = VibeKanbanIntegration()
    
    # Initial load
    active_tasks = integration.get_active_tasks()
    refresh_kanban_display(active_tasks)
    
    # Start watching for changes
    integration.start_watching(lambda: refresh_kanban_display(integration.get_active_tasks()))
    
    print("Watching task_registry.json for changes...")
    print("Press Ctrl+C to stop.")
    
    try:
        import time
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        integration.stop_watching()
        print("\nStopped watching.")


if __name__ == "__main__":
    main()
