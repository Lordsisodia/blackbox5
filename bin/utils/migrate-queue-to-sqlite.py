#!/usr/bin/env python3
"""
Queue.yaml to SQLite Migration Script
======================================

Migrates task queue from YAML to SQLite database using the storage abstraction layer.

Usage:
    python migrate-queue-to-sqlite.py [--project PROJECT] [--dry-run] [--backup]

Options:
    --project PROJECT  Project name (default: blackbox5)
    --dry-run          Show what would be migrated without making changes
    --backup           Create backup of queue.yaml before migration
    --verbose          Show detailed output
"""

import argparse
import os
import sys
from datetime import datetime
from pathlib import Path

# Add lib to path
LIB_PATH = Path(__file__).parent.parent / "5-project-memory" / "blackbox5" / ".autonomous" / "lib"
sys.path.insert(0, str(LIB_PATH))

try:
    from storage import Storage
    from backends.yaml_backend import YAMLStorageBackend
    from backends.sqlite_backend import SQLiteStorageBackend
except ImportError as e:
    print(f"[ERROR] Failed to import storage modules: {e}")
    print(f"[INFO] Make sure {LIB_PATH} exists and contains storage.py")
    sys.exit(1)


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Migrate BlackBox5 queue from YAML to SQLite"
    )
    parser.add_argument(
        "--project",
        default="blackbox5",
        help="Project name (default: blackbox5)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be migrated without making changes"
    )
    parser.add_argument(
        "--backup",
        action="store_true",
        help="Create backup of queue.yaml before migration"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show detailed output"
    )
    return parser.parse_args()


def create_backup(project_name: str) -> Path:
    """Create a backup of queue.yaml."""
    from paths import get_path_resolver

    resolver = get_path_resolver(project_name)
    project_path = resolver.get_project_path(project_name)
    queue_path = project_path / ".autonomous" / "agents" / "communications" / "queue.yaml"

    if not queue_path.exists():
        raise FileNotFoundError(f"queue.yaml not found at {queue_path}")

    backup_name = f"queue.yaml.backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    backup_path = queue_path.parent / backup_name

    import shutil
    shutil.copy2(queue_path, backup_path)
    return backup_path


def migrate_tasks(
    yaml_backend: YAMLStorageBackend,
    sqlite_backend: SQLiteStorageBackend,
    dry_run: bool = False,
    verbose: bool = False
) -> dict:
    """Migrate tasks from YAML to SQLite."""
    stats = {
        "tasks_migrated": 0,
        "tasks_failed": 0,
        "queue_items_migrated": 0,
        "errors": []
    }

    # Get all tasks from YAML
    yaml_tasks = yaml_backend.list_tasks()
    print(f"[OK] Found {len(yaml_tasks)} tasks in YAML backend")

    # Get queue from YAML
    yaml_queue = yaml_backend.get_queue()
    print(f"[OK] Found {len(yaml_queue)} items in YAML queue")

    if dry_run:
        print("\n[DRY RUN] Would migrate:")
        print(f"  - {len(yaml_tasks)} tasks")
        print(f"  - {len(yaml_queue)} queue items")
        return stats

    # Migrate tasks
    print("\n[OK] Migrating tasks...")
    for task in yaml_tasks:
        task_id = task.get("id", "unknown")
        try:
            if verbose:
                print(f"  Migrating: {task_id}")
            sqlite_backend.save_task(task)
            stats["tasks_migrated"] += 1
        except Exception as e:
            stats["tasks_failed"] += 1
            error_msg = f"Task {task_id}: {str(e)}"
            stats["errors"].append(error_msg)
            if verbose:
                print(f"    ERROR: {e}")

    # Migrate queue
    print("[OK] Migrating queue...")
    for queue_item in yaml_queue:
        task_id = queue_item.get("id")
        if not task_id:
            continue

        try:
            if verbose:
                print(f"  Enqueueing: {task_id}")

            # Get full task from SQLite
            task = sqlite_backend.get_task(task_id)
            if task:
                sqlite_backend.enqueue(task)
            else:
                # Use queue data if full task not found
                sqlite_backend.enqueue(queue_item)
            stats["queue_items_migrated"] += 1
        except Exception as e:
            error_msg = f"Queue item {task_id}: {str(e)}"
            stats["errors"].append(error_msg)
            if verbose:
                print(f"    ERROR: {e}")

    return stats


def verify_migration(
    yaml_backend: YAMLStorageBackend,
    sqlite_backend: SQLiteStorageBackend
) -> bool:
    """Verify the migration was successful."""
    yaml_tasks = yaml_backend.list_tasks()
    sqlite_tasks = sqlite_backend.list_tasks()

    yaml_queue = yaml_backend.get_queue()
    sqlite_queue = sqlite_backend.get_queue()

    success = True

    print("\n=== Verification ===")

    # Check task counts
    if len(yaml_tasks) != len(sqlite_tasks):
        print(f"[WARN] Task count mismatch - YAML: {len(yaml_tasks)}, SQLite: {len(sqlite_tasks)}")
        success = False
    else:
        print(f"[OK] Tasks: {len(sqlite_tasks)}")

    # Check queue counts
    if len(yaml_queue) != len(sqlite_queue):
        print(f"[WARN] Queue count mismatch - YAML: {len(yaml_queue)}, SQLite: {len(sqlite_queue)}")
        success = False
    else:
        print(f"[OK] Queue: {len(sqlite_queue)}")

    # Check specific tasks
    yaml_ids = {t.get("id") for t in yaml_tasks}
    sqlite_ids = {t.get("id") for t in sqlite_tasks}

    missing_in_sqlite = yaml_ids - sqlite_ids
    extra_in_sqlite = sqlite_ids - yaml_ids

    if missing_in_sqlite:
        print(f"[WARN] Missing in SQLite: {missing_in_sqlite}")
        success = False

    if extra_in_sqlite:
        print(f"[WARN] Extra in SQLite: {extra_in_sqlite}")
        success = False

    if not missing_in_sqlite and not extra_in_sqlite:
        print("[OK] All task IDs match")

    # Check statistics
    stats = sqlite_backend.get_statistics()
    print(f"\n--- Statistics ---")
    print(f"  By status: {stats.get('by_status', {})}")
    print(f"  By type: {stats.get('by_type', {})}")
    print(f"  By priority: {stats.get('by_priority', {})}")

    return success


def test_operations(sqlite_backend: SQLiteStorageBackend) -> bool:
    """Test basic CRUD operations."""
    print("\n=== Testing Operations ===")

    try:
        # Test 1: Read
        tasks = sqlite_backend.list_tasks(status="pending")
        if tasks:
            print(f"[OK] Read: Found {len(tasks)} pending tasks")
        else:
            print("[WARN] Read: No pending tasks found")

        # Test 2: Get specific task
        all_tasks = sqlite_backend.list_tasks()
        if all_tasks:
            test_task = all_tasks[0]
            task_id = test_task["id"]
            retrieved = sqlite_backend.get_task(task_id)
            if retrieved and retrieved["id"] == task_id:
                print(f"[OK] Get: Retrieved task {task_id}")
            else:
                print(f"[FAIL] Get: Could not retrieve task {task_id}")
                return False

        # Test 3: Queue operations
        queue = sqlite_backend.get_queue()
        print(f"[OK] Queue: Retrieved {len(queue)} items")

        return True

    except Exception as e:
        print(f"[FAIL] Operation test failed: {e}")
        return False


def main():
    """Main migration function."""
    args = parse_args()

    print("=" * 60)
    print("BlackBox5 Queue Migration: YAML to SQLite")
    print("=" * 60)
    print(f"Project: {args.project}")
    print(f"Dry run: {args.dry_run}")
    print()

    # Initialize backends
    try:
        yaml_backend = YAMLStorageBackend(project_name=args.project)
        sqlite_backend = SQLiteStorageBackend(project_name=args.project)
    except Exception as e:
        print(f"[ERROR] Failed to initialize backends: {e}")
        sys.exit(1)

    print(f"[OK] Source: YAML backend")
    print(f"[OK] Destination: {sqlite_backend._db_path}")
    print()

    # Create backup if requested
    if args.backup and not args.dry_run:
        try:
            backup_path = create_backup(args.project)
            print(f"[OK] Backup: {backup_path}")
            print()
        except Exception as e:
            print(f"[WARN] Backup failed: {e}")
            print()

    # Perform migration
    stats = migrate_tasks(
        yaml_backend,
        sqlite_backend,
        dry_run=args.dry_run,
        verbose=args.verbose
    )

    if args.dry_run:
        print("\n[DRY RUN] No changes made.")
        yaml_backend.close()
        sqlite_backend.close()
        return 0

    # Print results
    print("\n" + "=" * 60)
    print("Migration Results")
    print("=" * 60)
    print(f"Tasks migrated: {stats['tasks_migrated']}")
    print(f"Tasks failed: {stats['tasks_failed']}")
    print(f"Queue items: {stats['queue_items_migrated']}")

    if stats["errors"]:
        print(f"\n[WARN] {len(stats['errors'])} errors:")
        for error in stats["errors"][:5]:
            print(f"  - {error}")

    # Verify
    print()
    success = verify_migration(yaml_backend, sqlite_backend)

    # Test operations
    test_operations(sqlite_backend)

    # Summary
    print("\n" + "=" * 60)
    if success and stats["tasks_failed"] == 0:
        print("Migration completed successfully!")
        print()
        print("Next steps:")
        print("  1. Test applications with new SQLite backend")
        print("  2. Update configuration to use 'sqlite' backend")
        print("  3. Archive queue.yaml when ready")
    else:
        print("Migration completed with issues.")
        print("Please review the output above.")
    print("=" * 60)

    # Cleanup
    yaml_backend.close()
    sqlite_backend.close()

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
