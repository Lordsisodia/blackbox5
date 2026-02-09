#!/usr/bin/env python3
"""BB5 Commit Compliance Tracker - Track git commit compliance for completed tasks.

Usage:
    track-commit-compliance.py [options]
    track-commit-compliance.py --json
    track-commit-compliance.py --save

Options:
    -j, --json          Output as JSON
    -s, --save          Save report to file
    -d, --days N        Look back N days (default: 30)
    -t, --threshold P   Compliance threshold percentage (default: 75)
    -h, --help          Show this help message
"""

import argparse
import json
import os
import re
import subprocess
import sys
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple


# Configuration
BB5_ROOT = Path(os.environ.get("BB5_ROOT", Path.home() / ".blackbox5"))
COMPLETED_TASKS_DIR = BB5_ROOT / "5-project-memory/blackbox5/tasks/completed"
REPORTS_DIR = BB5_ROOT / "5-project-memory/blackbox5/reports"
DEFAULT_DAYS = 30
DEFAULT_THRESHOLD = 75


class Colors:
    """ANSI color codes."""
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    NC = '\033[0m'  # No Color


def run_git_command(args: List[str]) -> str:
    """Run a git command and return output."""
    try:
        result = subprocess.run(
            ["git"] + args,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        return ""


def get_commits_with_tasks(days: int) -> List[Dict]:
    """Get git commits that reference tasks."""
    since_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")

    # Get commits with TASK- in the message
    output = run_git_command([
        "log", "--all", f"--since={since_date}",
        "--pretty=format:%H|%ci|%s", "--grep=TASK-"
    ])

    commits = []
    for line in output.strip().split('\n'):
        if '|' not in line:
            continue
        parts = line.split('|', 2)
        if len(parts) >= 3:
            commits.append({
                'hash': parts[0],
                'date': parts[1],
                'message': parts[2]
            })

    return commits


def extract_task_ids_from_commits(commits: List[Dict]) -> set:
    """Extract unique task IDs from commit messages."""
    task_ids = set()
    pattern = re.compile(r'TASK-[A-Z0-9-]+')

    for commit in commits:
        matches = pattern.findall(commit['message'])
        task_ids.update(matches)

    return task_ids


def get_completed_tasks() -> List[str]:
    """Get all completed task IDs from filesystem."""
    tasks = []

    if not COMPLETED_TASKS_DIR.exists():
        return tasks

    # Search for TASK-* directories
    for path in COMPLETED_TASKS_DIR.rglob("TASK-*"):
        if path.is_dir():
            tasks.append(path.name)

    return list(set(tasks))


def get_task_metadata(task_id: str) -> Dict:
    """Get metadata for a task from its task.md file."""
    # Find task directory
    task_dir = None
    for path in COMPLETED_TASKS_DIR.rglob(task_id):
        if path.is_dir():
            task_dir = path
            break

    if not task_dir:
        return {
            'category': 'unknown',
            'priority': 'unknown',
            'completed_date': 'unknown'
        }

    task_file = task_dir / 'task.md'

    # Default values
    metadata = {
        'category': 'uncategorized',
        'priority': 'medium',
        'completed_date': 'unknown'
    }

    # Try to get completion date from directory mtime
    try:
        mtime = task_dir.stat().st_mtime
        metadata['completed_date'] = datetime.fromtimestamp(mtime).strftime('%Y-%m-%d')
    except:
        pass

    # Parse task.md if it exists
    if task_file.exists():
        try:
            content = task_file.read_text()

            # Extract category
            cat_match = re.search(r'\*\*Category:\*\*\s*(\S+)', content)
            if cat_match:
                metadata['category'] = cat_match.group(1).strip()

            # Extract priority
            pri_match = re.search(r'\*\*Priority:\*\*\s*(\S+)', content)
            if pri_match:
                metadata['priority'] = pri_match.group(1).strip()

        except Exception:
            pass

    return metadata


def calculate_compliance(total: int, with_commits: int) -> float:
    """Calculate compliance percentage."""
    if total == 0:
        return 0.0
    return (with_commits / total) * 100


def analyze_compliance(days: int, threshold: int) -> Dict:
    """Analyze commit compliance for completed tasks."""
    # Get commits and task IDs
    commits = get_commits_with_tasks(days)
    committed_task_ids = extract_task_ids_from_commits(commits)

    # Get completed tasks
    completed_tasks = get_completed_tasks()

    # Track results
    tasks_with_commits = []
    tasks_without_commits = []

    category_stats = defaultdict(lambda: {'total': 0, 'with_commits': 0})
    monthly_stats = defaultdict(lambda: {'total': 0, 'with_commits': 0})

    # Analyze each task
    for task_id in completed_tasks:
        metadata = get_task_metadata(task_id)
        category = metadata.get('category', 'uncategorized')
        priority = metadata.get('priority', 'medium')
        completed_date = metadata.get('completed_date', 'unknown')

        has_commit = task_id in committed_task_ids

        task_info = {
            'id': task_id,
            'category': category,
            'priority': priority,
            'completed_date': completed_date
        }

        if has_commit:
            tasks_with_commits.append(task_info)
            category_stats[category]['with_commits'] += 1
            if completed_date != 'unknown':
                month = completed_date[:7]  # YYYY-MM
                monthly_stats[month]['with_commits'] += 1
        else:
            tasks_without_commits.append(task_info)

        category_stats[category]['total'] += 1
        if completed_date != 'unknown':
            month = completed_date[:7]
            monthly_stats[month]['total'] += 1

    # Calculate totals
    total_tasks = len(tasks_with_commits) + len(tasks_without_commits)
    compliance_rate = calculate_compliance(total_tasks, len(tasks_with_commits))

    return {
        'summary': {
            'total_tasks': total_tasks,
            'with_commits': len(tasks_with_commits),
            'without_commits': len(tasks_without_commits),
            'compliance_rate': round(compliance_rate, 1),
            'threshold': threshold,
            'meets_threshold': compliance_rate >= threshold,
            'lookback_days': days
        },
        'by_category': {
            cat: {
                'total': stats['total'],
                'with_commits': stats['with_commits'],
                'rate': round(calculate_compliance(stats['total'], stats['with_commits']), 1)
            }
            for cat, stats in category_stats.items()
        },
        'by_month': {
            month: {
                'total': stats['total'],
                'with_commits': stats['with_commits'],
                'rate': round(calculate_compliance(stats['total'], stats['with_commits']), 1)
            }
            for month, stats in sorted(monthly_stats.items())
        },
        'tasks_without_commits': tasks_without_commits
    }


def print_table_report(data: Dict) -> None:
    """Print compliance report as formatted table."""
    summary = data['summary']

    print("")
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║           BB5 Task Commit Compliance Report                  ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print("")

    # Summary
    print(f"{Colors.BLUE}Summary:{Colors.NC}")
    print(f"  Lookback Period:     {summary['lookback_days']} days")
    print(f"  Total Tasks:         {summary['total_tasks']}")
    print(f"  With Commits:        {Colors.GREEN}{summary['with_commits']}{Colors.NC}")
    print(f"  Without Commits:     {Colors.RED}{summary['without_commits']}{Colors.NC}")

    rate = summary['compliance_rate']
    threshold = summary['threshold']
    if rate >= threshold:
        print(f"  Compliance Rate:     {Colors.GREEN}{rate:.1f}%{Colors.NC} (threshold: {threshold}%)")
    else:
        print(f"  Compliance Rate:     {Colors.RED}{rate:.1f}%{Colors.NC} (threshold: {threshold}%)")
    print("")

    # Category breakdown
    if data['by_category']:
        print(f"{Colors.BLUE}Compliance by Category:{Colors.NC}")
        print(f"  {'Category':<20} {'Total':>8} {'Commits':>8} {'Rate':>10}")
        print(f"  {'-'*20} {'-'*8} {'-'*8} {'-'*10}")

        for category, stats in sorted(data['by_category'].items()):
            rate = stats['rate']
            color = Colors.GREEN if rate >= threshold else Colors.RED
            print(f"  {category:<20} {stats['total']:>8} {stats['with_commits']:>8} {color}{rate:>9.1f}%{Colors.NC}")
        print("")

    # Monthly trend
    if data['by_month']:
        print(f"{Colors.BLUE}Compliance Trend by Month:{Colors.NC}")
        print(f"  {'Month':<10} {'Total':>8} {'Commits':>8} {'Rate':>10}")
        print(f"  {'-'*10} {'-'*8} {'-'*8} {'-'*10}")

        for month, stats in data['by_month'].items():
            rate = stats['rate']
            color = Colors.GREEN if rate >= threshold else Colors.RED
            print(f"  {month:<10} {stats['total']:>8} {stats['with_commits']:>8} {color}{rate:>9.1f}%{Colors.NC}")
        print("")

    # Tasks without commits
    if data['tasks_without_commits']:
        print(f"{Colors.YELLOW}Tasks Without Commits ({len(data['tasks_without_commits'])}):{Colors.NC}")
        print(f"  {'Task ID':<30} {'Category':<15} {'Priority':<10} {'Completed':<12}")
        print(f"  {'-'*30} {'-'*15} {'-'*10} {'-'*12}")

        for task in sorted(data['tasks_without_commits'], key=lambda x: x['id']):
            print(f"  {task['id']:<30} {task['category'][:15]:<15} {task['priority']:<10} {task['completed_date']:<12}")
        print("")

    # Recommendations
    print(f"{Colors.BLUE}Recommendations:{Colors.NC}")
    if not summary['meets_threshold']:
        print(f"  {Colors.YELLOW}⚠{Colors.NC}  Compliance ({rate:.1f}%) is below threshold ({threshold}%)")
        print("     Focus on committing for these task types:")
        for category, stats in data['by_category'].items():
            if stats['rate'] < threshold:
                print(f"     - {category} ({stats['rate']:.1f}% compliance)")
    else:
        print(f"  {Colors.GREEN}✓{Colors.NC}  Compliance ({rate:.1f}%) meets threshold ({threshold}%)")
    print("")


def main():
    parser = argparse.ArgumentParser(
        description="BB5 Commit Compliance Tracker",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    track-commit-compliance.py           # Show compliance report
    track-commit-compliance.py --json    # Output as JSON
    track-commit-compliance.py --save    # Save report to file
        """
    )
    parser.add_argument(
        "-j", "--json",
        action="store_true",
        help="Output as JSON"
    )
    parser.add_argument(
        "-s", "--save",
        action="store_true",
        help="Save report to file"
    )
    parser.add_argument(
        "-d", "--days",
        type=int,
        default=DEFAULT_DAYS,
        help=f"Look back N days (default: {DEFAULT_DAYS})"
    )
    parser.add_argument(
        "-t", "--threshold",
        type=int,
        default=DEFAULT_THRESHOLD,
        help=f"Compliance threshold percentage (default: {DEFAULT_THRESHOLD})"
    )

    args = parser.parse_args()

    # Check if we're in a git repo
    try:
        subprocess.run(
            ["git", "rev-parse", "--git-dir"],
            capture_output=True,
            check=True
        )
    except subprocess.CalledProcessError:
        print("Error: Not in a git repository", file=sys.stderr)
        sys.exit(1)

    # Analyze compliance
    data = analyze_compliance(args.days, args.threshold)

    if data['summary']['total_tasks'] == 0:
        if args.json:
            print(json.dumps({"error": "No completed tasks found"}, indent=2))
        else:
            print("No completed tasks found.")
        sys.exit(0)

    # Output
    if args.json:
        print(json.dumps(data, indent=2))
    else:
        print_table_report(data)

    # Save report if requested
    if args.save:
        REPORTS_DIR.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        report_file = REPORTS_DIR / f"commit-compliance-{timestamp}.json"
        report_file.write_text(json.dumps(data, indent=2))
        if not args.json:
            print(f"Report saved to: {report_file}")


if __name__ == "__main__":
    main()
