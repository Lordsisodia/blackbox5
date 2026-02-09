#!/usr/bin/env python3
"""Test script for task-scanner module."""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from task_scanner import parse_task_file, scan_tasks_directory

def test_parse_task():
    """Test parsing a specific task file."""
    print("=" * 60)
    print("TEST: Parse TASK-010-001 (4 hours effort)")
    print("=" * 60)

    task = parse_task_file(Path("/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/tasks/active/TASK-010-001-sessionstart-enhanced/task.md"))

    assert task is not None, "Failed to parse task"
    assert task.id == "TASK-010-001", f"Expected TASK-010-001, got {task.id}"
    assert task.status == "pending", f"Expected pending, got {task.status}"
    assert task.priority == "critical", f"Expected critical, got {task.priority}"
    assert task.estimated_minutes == 240, f"Expected 240 minutes (4 hours), got {task.estimated_minutes}"
    # Note: This task file has template placeholders, so criteria may be empty
    print(f"  Success criteria: {len(task.success_criteria)} items (may be template)")

    print(f"  ID: {task.id}")
    print(f"  Title: {task.title}")
    print(f"  Status: {task.status}")
    print(f"  Priority: {task.priority}")
    print(f"  Type: {task.type}")
    print(f"  Estimated minutes: {task.estimated_minutes}")
    print(f"  Priority score: {task.priority_score}")
    print(f"  Success criteria: {len(task.success_criteria)} items")
    print("  PASS")
    print()

def test_parse_task_with_files():
    """Test parsing a task with file modifications."""
    print("=" * 60)
    print("TEST: Parse TASK-FIX-SKIL-007-1 (with files)")
    print("=" * 60)

    task = parse_task_file(Path("/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/tasks/active/TASK-FIX-SKIL-007-1/task.md"))

    assert task is not None, "Failed to parse task"
    assert task.id == "TASK-FIX-SKIL-007-1", f"Expected TASK-FIX-SKIL-007-1, got {task.id}"
    assert task.priority == "high", f"Expected high, got {task.priority}"

    print(f"  ID: {task.id}")
    print(f"  Title: {task.title}")
    print(f"  Status: {task.status}")
    print(f"  Priority: {task.priority}")
    print(f"  Files to create: {task.files_to_create}")
    print(f"  Files to modify: {task.files_to_modify}")
    print("  PASS")
    print()

def test_scan_directory():
    """Test scanning the tasks directory."""
    print("=" * 60)
    print("TEST: Scan tasks directory")
    print("=" * 60)

    tasks = scan_tasks_directory(Path("/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/tasks/active"))

    assert len(tasks) > 0, "Expected to find tasks"

    # Check that tasks are sorted by priority score
    for i in range(len(tasks) - 1):
        assert tasks[i].priority_score >= tasks[i+1].priority_score, \
            f"Tasks not sorted by priority score: {tasks[i].id} ({tasks[i].priority_score}) < {tasks[i+1].id} ({tasks[i+1].priority_score})"

    print(f"  Found {len(tasks)} tasks")
    print(f"  Highest priority: {tasks[0].id} (score: {tasks[0].priority_score})")
    print(f"  Lowest priority: {tasks[-1].id} (score: {tasks[-1].priority_score})")
    print("  PASS")
    print()

def test_queue_entry_format():
    """Test queue entry format."""
    print("=" * 60)
    print("TEST: Queue entry format")
    print("=" * 60)

    task = parse_task_file(Path("/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/tasks/active/TASK-FIX-SKIL-007-1/task.md"))
    entry = task.to_queue_entry()

    required_keys = ["id", "type", "status", "priority", "priority_score", "title", "estimated_minutes", "roi", "blockedBy", "blocks", "resource_type", "parallel_group"]
    for key in required_keys:
        assert key in entry, f"Missing key: {key}"

    print(f"  Entry keys: {list(entry.keys())}")
    print(f"  ROI: {entry['roi']}")
    print("  PASS")
    print()

def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("TASK SCANNER TEST SUITE")
    print("=" * 60 + "\n")

    try:
        test_parse_task()
        test_parse_task_with_files()
        test_scan_directory()
        test_queue_entry_format()

        print("=" * 60)
        print("ALL TESTS PASSED")
        print("=" * 60)
        return 0
    except AssertionError as e:
        print(f"\nTEST FAILED: {e}")
        return 1
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
