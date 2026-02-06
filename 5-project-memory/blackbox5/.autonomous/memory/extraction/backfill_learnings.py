#!/usr/bin/env python3
"""
Backfill Learnings - Process all historical runs to populate learning index.

This script processes all existing run directories and extracts learnings
to populate the learning-index.yaml file.

Usage:
    python backfill_learnings.py
    python backfill_learnings.py --dry-run
    python backfill_learnings.py --rebuild
"""

import argparse
import sys
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent))

from learning_extractor import LearningExtractor


def main():
    parser = argparse.ArgumentParser(
        description="Backfill learnings from all historical runs"
    )
    parser.add_argument("--dry-run", action="store_true",
                        help="Process but don't save to index")
    parser.add_argument("--rebuild", action="store_true",
                        help="Rebuild index from scratch (clear existing)")
    parser.add_argument("--runs-dir",
                        default="/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/.autonomous/agents/executor/runs",
                        help="Directory containing run directories")

    args = parser.parse_args()

    runs_dir = Path(args.runs_dir)

    if not runs_dir.exists():
        print(f"Error: Runs directory not found: {runs_dir}")
        return 1

    extractor = LearningExtractor()

    if args.rebuild:
        print("Rebuilding index from scratch...")
        extractor.rebuild_index(runs_dir)
    else:
        print("Backfilling learnings from historical runs...")
        new_learnings = extractor.backfill(runs_dir, dry_run=args.dry_run)
        print(f"\nTotal new learnings: {len(new_learnings)}")

    # Run health check
    print("\n" + "=" * 50)
    print("Running health check...")
    results = extractor.health_check()
    print(f"Status: {results['status'].upper()}")
    print(f"Total learnings in index: {results['stats']['total_learnings']}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
