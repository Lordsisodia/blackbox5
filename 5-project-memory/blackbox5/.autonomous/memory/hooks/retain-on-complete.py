#!/usr/bin/env python3
"""
RETAIN Hook - Task Completion Memory Extraction

Automatically extracts memories when a task is completed.
Called by task completion workflow.

Usage:
    retain-on-complete.py --task-id TASK-XXX --run-dir /path/to/run
    retain-on-complete.py --run-dir /path/to/run  # Auto-detect task from run
"""

import argparse
import asyncio
import os
import sys
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from operations.retain import RetainEngine


async def retain_from_run(run_dir: Path, task_id: str = None):
    """
    Extract memories from a completed run.

    Args:
        run_dir: Path to run directory
        task_id: Optional task ID (auto-detected if not provided)
    """
    print(f"RETAIN Hook: Processing run {run_dir.name}")

    if not run_dir.exists():
        print(f"Error: Run directory not found: {run_dir}")
        return False

    # Auto-detect task ID if not provided
    if not task_id:
        # Try to read from task_state.json
        task_state_file = run_dir / "task_state.json"
        if task_state_file.exists():
            import json
            try:
                with open(task_state_file) as f:
                    state = json.load(f)
                    task_id = state.get("task", {}).get("task_id")
            except Exception as e:
                print(f"  Warning: Could not read task state: {e}")

    # Files to process (in order of importance)
    files_to_process = []

    # Core documentation files
    for filename in ["DECISIONS.md", "THOUGHTS.md", "RESULTS.md", "LEARNINGS.md"]:
        filepath = run_dir / filename
        if filepath.exists():
            files_to_process.append(filepath)

    if not files_to_process:
        print("  No documentation files found to process")
        return False

    print(f"  Task: {task_id or 'unknown'}")
    print(f"  Files to process: {len(files_to_process)}")

    # Initialize RETAIN engine
    engine = RetainEngine()

    # Process each file
    total_memories = 0
    for filepath in files_to_process:
        try:
            memories = await engine.process_file(filepath, dry_run=False)
            total_memories += len(memories)
            print(f"  ✓ {filepath.name}: {len(memories)} memories")
        except Exception as e:
            print(f"  ✗ {filepath.name}: {e}")

    print(f"\n  Total memories extracted: {total_memories}")

    # Save to output for reference
    output_dir = run_dir / ".retain_output"
    engine.save_to_files(output_dir)

    return True


def main():
    parser = argparse.ArgumentParser(
        description="RETAIN hook - extract memories on task completion"
    )
    parser.add_argument("--run-dir", required=True, help="Path to run directory")
    parser.add_argument("--task-id", help="Task ID (auto-detected if not provided)")
    args = parser.parse_args()

    run_dir = Path(args.run_dir)

    success = asyncio.run(retain_from_run(run_dir, args.task_id))

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
