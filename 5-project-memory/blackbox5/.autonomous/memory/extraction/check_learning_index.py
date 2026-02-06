#!/usr/bin/env python3
"""
Learning Index Health Check

Validates the integrity and health of the learning index.
Can be run manually or as part of monitoring.

Usage:
    python check_learning_index.py
    python check_learning_index.py --verbose
    python check_learning_index.py --fix
"""

import argparse
import sys
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent))

from learning_extractor import LearningExtractor


def main():
    parser = argparse.ArgumentParser(
        description="Check learning index health"
    )
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Show detailed output")
    parser.add_argument("--fix", action="store_true",
                        help="Attempt to fix issues automatically")

    args = parser.parse_args()

    extractor = LearningExtractor()
    results = extractor.health_check()

    # Print results
    print("=" * 60)
    print("LEARNING INDEX HEALTH CHECK")
    print("=" * 60)
    print(f"Status: {results['status'].upper()}")
    print()

    # Statistics
    print("STATISTICS:")
    print(f"  Total learnings: {results['stats']['total_learnings']}")
    print(f"  Total patterns: {results['stats']['total_patterns']}")

    if 'types' in results['stats']:
        print("\n  By Type:")
        for type_name, count in sorted(results['stats']['types'].items()):
            print(f"    - {type_name}: {count}")

    if 'categories' in results['stats']:
        print("\n  By Category:")
        for cat_name, count in sorted(results['stats']['categories'].items()):
            print(f"    - {cat_name}: {count}")

    # Issues
    if results['issues']:
        print(f"\nISSUES FOUND ({len(results['issues'])}):")
        for issue in results['issues']:
            print(f"  - {issue}")
    else:
        print("\nNo issues found.")

    # Recommendations
    print("\nRECOMMENDATIONS:")
    if results['stats']['total_learnings'] == 0:
        print("  - Run backfill_learnings.py to populate the index")
    elif results['stats']['total_learnings'] < 50:
        print("  - Consider processing more runs to build up the knowledge base")
    else:
        print("  - Learning index is well-populated")

    if 'frequency' in results['stats']:
        freq = results['stats']['frequency']
        if freq.get('recurring', 0) < 5:
            print("  - Look for more recurring patterns across tasks")

    print("=" * 60)

    # Exit code based on status
    if results['status'] == 'healthy':
        return 0
    elif results['status'] == 'warning':
        return 1
    else:
        return 2


if __name__ == "__main__":
    sys.exit(main())
