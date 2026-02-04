#!/usr/bin/env python3
"""Standardize run folder naming to ISO datetime format.

Converts:
- Sequential: run-0001 -> run-20260204-143052 (using folder mtime)
- Epoch: run-1769862398 -> run-20251031-120638 (converting timestamp)
- Underscore: run-20260131_192605 -> run-20260131-192605 (standardizing separator)
- Descriptive: run-youtube-automation -> run-20260204-143052-youtube (using mtime + preserving name)

Target format: run-YYYYMMDD-HHMMSS[-description]
"""

import os
import re
import shutil
from datetime import datetime
from pathlib import Path

def get_folder_mtime(path):
    """Get folder modification time as datetime."""
    try:
        mtime = os.path.getmtime(path)
        return datetime.fromtimestamp(mtime)
    except:
        return datetime.now()

def convert_epoch_to_datetime(epoch_str):
    """Convert Unix epoch string to datetime."""
    try:
        epoch = int(epoch_str)
        return datetime.fromtimestamp(epoch)
    except:
        return None

def generate_new_name(old_name, folder_path):
    """Generate standardized name based on old name pattern."""
    # Pattern: run-YYYYMMDD-HHMMSS (already standard)
    if re.match(r'^run-\d{8}-\d{6}$', old_name):
        return old_name, "already_standard"

    # Pattern: run-YYYYMMDD_HHMMSS (underscore separator)
    match = re.match(r'^run-(\d{4})(\d{2})(\d{2})_(\d{2})(\d{2})(\d{2})$', old_name)
    if match:
        new_name = f"run-{match.group(1)}{match.group(2)}{match.group(3)}-{match.group(4)}{match.group(5)}{match.group(6)}"
        return new_name, "underscore_to_dash"

    # Pattern: run-<10+digits> (Unix epoch)
    match = re.match(r'^run-(\d{10,})$', old_name)
    if match:
        dt = convert_epoch_to_datetime(match.group(1))
        if dt:
            new_name = dt.strftime("run-%Y%m%d-%H%M%S")
            return new_name, "epoch_to_datetime"

    # Pattern: run-<4 digits> (sequential)
    match = re.match(r'^run-(\d{1,4})$', old_name)
    if match:
        dt = get_folder_mtime(folder_path)
        new_name = dt.strftime("run-%Y%m%d-%H%M%S")
        return new_name, "sequential_to_datetime"

    # Pattern: run-<descriptive-name> (descriptive)
    match = re.match(r'^run-(.+)$', old_name)
    if match:
        desc = match.group(1)
        dt = get_folder_mtime(folder_path)
        new_name = dt.strftime("run-%Y%m%d-%H%M%S") + f"-{desc}"
        return new_name, "descriptive_preserved"

    return None, "unknown_pattern"

def main():
    print("=" * 60)
    print("Run Naming Standardization")
    print("=" * 60)

    # Find all run folders
    base_path = Path(".autonomous")
    if not base_path.exists():
        base_path = Path(".")

    run_folders = []
    for root, dirs, files in os.walk(base_path):
        for d in dirs:
            if d.startswith("run-"):
                run_folders.append(Path(root) / d)

    print(f"\nFound {len(run_folders)} run folders")

    # Categorize
    categories = {
        "already_standard": [],
        "underscore_to_dash": [],
        "epoch_to_datetime": [],
        "sequential_to_datetime": [],
        "descriptive_preserved": [],
        "unknown_pattern": []
    }

    for folder in run_folders:
        new_name, category = generate_new_name(folder.name, folder)
        if new_name:
            categories[category].append({
                "old": str(folder),
                "new": str(folder.parent / new_name),
                "category": category
            })

    # Print summary
    print("\nCategories:")
    for cat, items in categories.items():
        if items:
            print(f"  {cat}: {len(items)}")

    # Show samples
    print("\nSample conversions:")
    for cat, items in categories.items():
        if items and cat != "already_standard":
            sample = items[0]
            print(f"  {cat}:")
            print(f"    {Path(sample['old']).name}")
            print(f"    -> {Path(sample['new']).name}")

    # Ask for confirmation
    total_to_rename = sum(len(items) for cat, items in categories.items() if cat != "already_standard")
    print(f"\n{total_to_rename} folders need renaming")
    print("\nDry run complete. To actually rename, run with --execute flag")

    return categories

if __name__ == "__main__":
    import sys
    if "--execute" in sys.argv:
        print("\nExecuting renames...")
        categories = main()
        for cat, items in categories.items():
            if cat != "already_standard":
                for item in items:
                    try:
                        shutil.move(item["old"], item["new"])
                        print(f"Renamed: {Path(item['old']).name} -> {Path(item['new']).name}")
                    except Exception as e:
                        print(f"Error renaming {item['old']}: {e}")
        print("\nDone!")
    else:
        main()
