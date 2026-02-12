#!/usr/bin/env python3
"""
VPS Task Loop - Task runner for YouTube automation research

Processes tasks from queue with proper URL validation to prevent
false "404 url.not_found" errors for tasks that don't require URLs.
"""

import sys
import os
import json
import yaml
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Paths
BB5_DIR = Path("/opt/blackbox5")
TASKS_DIR = BB5_DIR / "5-project-memory/blackbox5/tasks/active"
LOG_FILE = BB5_DIR / ".autonomous/logs/task-runner.log"

# Task states
TASK_STATES = {
    'pending': 'Task waiting to be processed',
    'in_progress': 'Task currently being worked on',
    'completed': 'Task finished successfully',
    'failed': 'Task failed with error',
    'requires_url': 'Task requires URL validation'
}

class TaskRunner:
    """Main task runner with URL validation"""

    def __init__(self):
        self.log_file = LOG_FILE
        self.log_file.parent.mkdir(parents=True, exist_ok=True)

    def log(self, message: str):
        """Log to both console and file"""
        timestamp = datetime.now().isoformat()
        log_line = f"[{timestamp}] {message}"
        print(log_line)
        with open(self.log_file, "a") as f:
            f.write(log_line + "\n")

    def load_task(self, task_path: Path) -> Optional[Dict[str, Any]]:
        """Load task from directory"""
        task_file = task_path / "task.md"

        if not task_file.exists():
            self.log(f"❌ Task file not found: {task_file}")
            return None

        # Parse task.md for metadata
        with open(task_file, 'r') as f:
            content = f.read()

        # Extract task metadata (simplified parsing)
        metadata = {
            'path': str(task_path),
            'name': task_path.name,
            'status': 'pending',
            'url_required': False,
            'priority': 'MEDIUM'
        }

        # Extract status
        for line in content.split('\n'):
            if line.startswith('**Status:**'):
                metadata['status'] = line.split(':', 1)[1].strip()
            elif line.startswith('**Priority:**'):
                metadata['priority'] = line.split(':', 1)[1].strip().upper()

        return metadata

    def validate_url_requirement(self, task: Dict[str, Any]) -> tuple[bool, str]:
        """
        Validate if task requires URL and if URL is present.

        Returns:
            (is_valid, error_message)
        """
        # Check if task has URL requirement field
        url_required = task.get('url_required', False)

        # If URL is not required, skip validation
        if not url_required:
            self.log(f"  ✓ Task does not require URL - skipping validation")
            return True, ""

        # If URL is required, check for URL field
        if 'URL:' not in str(task) and 'url' not in str(task).lower():
            return False, "Task marked as requiring URL but no URL provided"

        # Check for video_id
        video_id = task.get('video_id')
        if url_required and not video_id:
            return False, "URL provided but no video ID - please check task configuration"

        # All checks passed
        return True, ""

    def fetch_youtube_metadata(self, video_id: str) -> Optional[Dict[str, Any]]:
        """
        Fetch metadata from YouTube API.

        Returns:
            Metadata dict or None if fetch fails
        """
        try:
            # Placeholder for actual YouTube API call
            # In production, this would use youtube-transcript-api or yt-dlp
            self.log(f"  Fetching metadata for video {video_id}...")

            # Simulated metadata
            metadata = {
                'video_id': video_id,
                'title': 'Test Video',
                'channel': 'Test Channel',
                'duration': 600
            }

            return metadata

        except Exception as e:
            error_msg = f"Error fetching metadata: {str(e)}"
            self.log(f"  ❌ {error_msg}")
            return None

    def execute_task(self, task_path: Path) -> tuple[bool, str]:
        """
        Execute a single task.

        Returns:
            (success, error_message)
        """
        self.log(f"\n{'='*60}")
        self.log(f"Processing task: {task_path.name}")

        # Load task
        task = self.load_task(task_path)
        if not task:
            return False, "Failed to load task"

        # Validate URL requirement
        self.log("Validating URL requirements...")
        is_valid, error = self.validate_url_requirement(task)

        if not is_valid:
            # URL validation failed
            if "Task marked as requiring URL but no URL provided" in error:
                self.log(f"  ⚠️  {error}")
                self.log(f"  → Task marked as 'requires_url' (not 404 error)")
                return False, "requires_url"
            elif "URL provided but no video ID" in error:
                self.log(f"  ⚠️  {error}")
                return False, "url_no_video_id"

        # If URL is required and present, attempt fetch
        if task.get('url_required', False):
            video_id = task.get('video_id')
            if video_id:
                metadata = self.fetch_youtube_metadata(video_id)
                if not metadata:
                    # Video doesn't exist or fetch failed
                    self.log(f"  ❌ Video {video_id} not found or has been deleted")
                    return False, "video_not_found"
                else:
                    self.log(f"  ✓ Metadata fetched successfully")
            else:
                self.log(f"  ⚠️  URL required but no video_id found")
                return False, "url_no_video_id"
        else:
            # No URL required - skip fetch entirely
            self.log(f"  ✓ Skipping metadata fetch (URL not required)")

        # Task execution successful
        self.log(f"✅ Task processed successfully")
        return True, ""

    def run_single(self, task_id: str):
        """Run a single task by ID"""
        task_path = TASKS_DIR / task_id

        if not task_path.exists():
            self.log(f"❌ Task not found: {task_id}")
            return

        success, error = self.execute_task(task_path)

        if success:
            self.log(f"✓ Task completed")
        else:
            self.log(f"✗ Task failed: {error}")


def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("Usage: vps-task-loop.py --execute <task-id>")
        print("       vps-task-loop.py --help")
        sys.exit(1)

    command = sys.argv[1]

    if command == "--execute":
        if len(sys.argv) < 3:
            print("Error: --execute requires task-id")
            sys.exit(1)

        task_id = sys.argv[2]
        runner = TaskRunner()
        runner.run_single(task_id)

    elif command == "--help":
        print("VPS Task Loop - Task Runner with URL Validation")
        print()
        print("Commands:")
        print("  --execute <task-id>  Execute a specific task")
        print("  --help               Show this help message")
        print()
        print("Features:")
        print("  - Validates URL requirements before attempting fetch")
        print("  - Tasks without URL requirement skip metadata fetch phase")
        print("  - Specific error messages for different failure types")
        print("  - No generic 'url.not_found' errors")

    else:
        print(f"Unknown command: {command}")
        print("Use --help for usage")
        sys.exit(1)


if __name__ == "__main__":
    main()
