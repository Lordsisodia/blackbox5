#!/usr/bin/env python3
"""
Track learning/decision extraction rates from completed tasks.

This script analyzes LEARNINGS.md and DECISIONS.md files across the project
to calculate extraction rates and identify tasks with low extraction.

Usage:
    track-extraction-rates.py [options]

Options:
    --project PATH      Project directory to analyze (default: ~/.blackbox5/5-project-memory/blackbox5)
    --output FORMAT     Output format: text, json, yaml (default: text)
    --save PATH         Save report to file
    --min-learnings N   Minimum learnings threshold (default: 1)
    --min-decisions N   Minimum decisions threshold (default: 1)
"""

import os
import re
import sys
import json
import yaml
import argparse
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from typing import Dict, List, Tuple, Any


def parse_learning_file(filepath: Path) -> List[Dict[str, Any]]:
    """Parse a LEARNINGS.md file and extract individual learnings."""
    learnings = []

    if not filepath.exists():
        return learnings

    content = filepath.read_text(encoding='utf-8')

    # Try to parse structured learnings (## L-XXX format)
    structured_pattern = r'##\s*(L-[\w-]+)\s*\n\*\*Category:\*\*\s*(\w+)\s*\n\*\*Observation:\*\*\s*(.+?)\n\*\*Action Item:\*\*\s*(.+?)(?=\n##|\Z)'
    structured_matches = re.findall(structured_pattern, content, re.DOTALL)

    for match in structured_matches:
        learnings.append({
            'id': match[0].strip(),
            'category': match[1].strip(),
            'observation': match[2].strip(),
            'action_item': match[3].strip(),
            'structured': True
        })

    # Try to parse simple bullet learnings
    if not learnings:
        bullet_pattern = r'[-*]\s*(.+?)(?=\n[-*]|\n##|\Z)'
        bullet_matches = re.findall(bullet_pattern, content, re.DOTALL)

        for i, match in enumerate(bullet_matches):
            text = match.strip()
            if len(text) > 10:  # Filter out very short lines
                learnings.append({
                    'id': f'L-{filepath.stem}-{i+1}',
                    'category': 'unknown',
                    'observation': text,
                    'action_item': '',
                    'structured': False
                })

    return learnings


def parse_decisions_file(filepath: Path) -> List[Dict[str, Any]]:
    """Parse a DECISIONS.md file and extract individual decisions."""
    decisions = []

    if not filepath.exists():
        return decisions

    content = filepath.read_text(encoding='utf-8')

    # Try to parse structured decisions (## D-XXX format)
    structured_pattern = r'##\s*(D-[\w-]+)\s*\n\*\*Context:\*\*\s*(.+?)\n\*\*Decision:\*\*\s*(.+?)\n\*\*Rationale:\*\*\s*(.+?)(?=\n##|\Z)'
    structured_matches = re.findall(structured_pattern, content, re.DOTALL)

    for match in structured_matches:
        decisions.append({
            'id': match[0].strip(),
            'context': match[1].strip(),
            'decision': match[2].strip(),
            'rationale': match[3].strip(),
            'structured': True
        })

    # Try to parse simple bullet decisions
    if not decisions:
        bullet_pattern = r'[-*]\s*(.+?)(?=\n[-*]|\n##|\Z)'
        bullet_matches = re.findall(bullet_pattern, content, re.DOTALL)

        for i, match in enumerate(bullet_matches):
            text = match.strip()
            if len(text) > 10:
                decisions.append({
                    'id': f'D-{filepath.stem}-{i+1}',
                    'context': '',
                    'decision': text,
                    'rationale': '',
                    'structured': False
                })

    return decisions


def get_task_info(task_path: Path) -> Dict[str, Any]:
    """Extract task information from task directory."""
    task_info = {
        'id': task_path.name,
        'path': str(task_path),
        'type': 'unknown',
        'status': 'unknown',
        'has_learnings': False,
        'has_decisions': False,
        'learnings_count': 0,
        'decisions_count': 0,
        'learnings': [],
        'decisions': []
    }

    # Check for task.md
    task_md = task_path / 'task.md'
    if task_md.exists():
        content = task_md.read_text(encoding='utf-8')

        # Extract status
        status_match = re.search(r'\*\*Status:\*\*\s*(\w+)', content)
        if status_match:
            task_info['status'] = status_match.group(1).lower()

        # Extract category/type
        category_match = re.search(r'\*\*Category:\*\*\s*(\w+)', content)
        if category_match:
            task_info['type'] = category_match.group(1).lower()
        else:
            # Try to infer from task ID
            task_id = task_path.name
            if 'PROC' in task_id:
                task_info['type'] = 'process'
            elif 'RESEARCH' in task_id:
                task_info['type'] = 'research'
            elif 'IMP' in task_id:
                task_info['type'] = 'improvement'
            elif 'BUG' in task_id:
                task_info['type'] = 'bugfix'
            elif 'FEAT' in task_id:
                task_info['type'] = 'feature'

    # Parse LEARNINGS.md
    learnings_file = task_path / 'LEARNINGS.md'
    if learnings_file.exists():
        task_info['has_learnings'] = True
        task_info['learnings'] = parse_learning_file(learnings_file)
        task_info['learnings_count'] = len(task_info['learnings'])

    # Parse DECISIONS.md
    decisions_file = task_path / 'DECISIONS.md'
    if decisions_file.exists():
        task_info['has_decisions'] = True
        task_info['decisions'] = parse_decisions_file(decisions_file)
        task_info['decisions_count'] = len(task_info['decisions'])

    return task_info


def scan_autonomous_runs(project_path: Path) -> Tuple[List[Dict], int, int]:
    """Scan .autonomous/runs directory for learnings and decisions."""
    runs_data = []
    total_learnings = 0
    total_decisions = 0

    runs_path = project_path / '.autonomous' / 'runs'
    if runs_path.exists():
        for run_dir in runs_path.iterdir():
            if run_dir.is_dir() and not run_dir.name.startswith('.'):
                run_info = {
                    'id': run_dir.name,
                    'path': str(run_dir),
                    'type': 'run',
                    'status': 'completed',
                    'has_learnings': False,
                    'has_decisions': False,
                    'learnings_count': 0,
                    'decisions_count': 0,
                    'learnings': [],
                    'decisions': []
                }

                # Parse LEARNINGS.md
                learnings_file = run_dir / 'LEARNINGS.md'
                if learnings_file.exists():
                    run_info['has_learnings'] = True
                    run_info['learnings'] = parse_learning_file(learnings_file)
                    run_info['learnings_count'] = len(run_info['learnings'])
                    total_learnings += run_info['learnings_count']

                # Parse DECISIONS.md
                decisions_file = run_dir / 'DECISIONS.md'
                if decisions_file.exists():
                    run_info['has_decisions'] = True
                    run_info['decisions'] = parse_decisions_file(decisions_file)
                    run_info['decisions_count'] = len(run_info['decisions'])
                    total_decisions += run_info['decisions_count']

                runs_data.append(run_info)

    return runs_data, total_learnings, total_decisions


def scan_project(project_path: Path) -> Tuple[List[Dict], List[Dict], List[Dict], int, int]:
    """Scan project for all tasks and their extraction data."""
    active_tasks = []
    completed_tasks = []

    # Scan active tasks
    active_path = project_path / 'tasks' / 'active'
    if active_path.exists():
        for task_dir in active_path.iterdir():
            if task_dir.is_dir() and not task_dir.name.startswith('.'):
                task_info = get_task_info(task_dir)
                active_tasks.append(task_info)

    # Scan completed tasks
    completed_path = project_path / 'tasks' / 'completed'
    if completed_path.exists():
        for date_dir in completed_path.iterdir():
            if date_dir.is_dir() and not date_dir.name.startswith('.'):
                for task_dir in date_dir.iterdir():
                    if task_dir.is_dir() and not task_dir.name.startswith('.'):
                        task_info = get_task_info(task_dir)
                        completed_tasks.append(task_info)

    # Scan autonomous runs
    runs_data, runs_learnings, runs_decisions = scan_autonomous_runs(project_path)

    return active_tasks, completed_tasks, runs_data, runs_learnings, runs_decisions


def calculate_extraction_metrics(tasks: List[Dict]) -> Dict[str, Any]:
    """Calculate extraction rate metrics from tasks."""
    total_tasks = len(tasks)

    if total_tasks == 0:
        return {
            'total_tasks': 0,
            'tasks_with_learnings': 0,
            'tasks_with_decisions': 0,
            'tasks_with_both': 0,
            'tasks_with_neither': 0,
            'total_learnings': 0,
            'total_decisions': 0,
            'learning_extraction_rate': 0.0,
            'decision_extraction_rate': 0.0,
            'overall_extraction_rate': 0.0,
            'by_type': {},
            'low_extraction_tasks': []
        }

    tasks_with_learnings = sum(1 for t in tasks if t['learnings_count'] > 0)
    tasks_with_decisions = sum(1 for t in tasks if t['decisions_count'] > 0)
    tasks_with_both = sum(1 for t in tasks if t['learnings_count'] > 0 and t['decisions_count'] > 0)
    tasks_with_neither = sum(1 for t in tasks if t['learnings_count'] == 0 and t['decisions_count'] == 0)

    total_learnings = sum(t['learnings_count'] for t in tasks)
    total_decisions = sum(t['decisions_count'] for t in tasks)

    # Calculate rates
    learning_extraction_rate = (tasks_with_learnings / total_tasks) * 100
    decision_extraction_rate = (tasks_with_decisions / total_tasks) * 100
    overall_extraction_rate = ((tasks_with_learnings + tasks_with_decisions) / (total_tasks * 2)) * 100

    # Group by type
    by_type = defaultdict(lambda: {
        'count': 0,
        'with_learnings': 0,
        'with_decisions': 0,
        'total_learnings': 0,
        'total_decisions': 0
    })

    for task in tasks:
        task_type = task.get('type', 'unknown')
        by_type[task_type]['count'] += 1
        if task['learnings_count'] > 0:
            by_type[task_type]['with_learnings'] += 1
        if task['decisions_count'] > 0:
            by_type[task_type]['with_decisions'] += 1
        by_type[task_type]['total_learnings'] += task['learnings_count']
        by_type[task_type]['total_decisions'] += task['decisions_count']

    # Find low extraction tasks (missing both learnings and decisions)
    low_extraction_tasks = [
        {
            'id': t['id'],
            'type': t['type'],
            'status': t['status'],
            'learnings_count': t['learnings_count'],
            'decisions_count': t['decisions_count']
        }
        for t in tasks
        if t['learnings_count'] == 0 and t['decisions_count'] == 0
    ]

    return {
        'total_tasks': total_tasks,
        'tasks_with_learnings': tasks_with_learnings,
        'tasks_with_decisions': tasks_with_decisions,
        'tasks_with_both': tasks_with_both,
        'tasks_with_neither': tasks_with_neither,
        'total_learnings': total_learnings,
        'total_decisions': total_decisions,
        'learning_extraction_rate': round(learning_extraction_rate, 1),
        'decision_extraction_rate': round(decision_extraction_rate, 1),
        'overall_extraction_rate': round(overall_extraction_rate, 1),
        'by_type': dict(by_type),
        'low_extraction_tasks': low_extraction_tasks
    }


def format_text_report(active_metrics: Dict, completed_metrics: Dict, runs_metrics: Dict, runs_learnings: int, runs_decisions: int) -> str:
    """Format metrics as a text report."""
    lines = []
    lines.append("=" * 70)
    lines.append("EXTRACTION RATE TRACKING REPORT")
    lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("=" * 70)
    lines.append("")

    # Overall Summary
    lines.append("-" * 70)
    lines.append("OVERALL SUMMARY")
    lines.append("-" * 70)

    total_tasks = active_metrics['total_tasks'] + completed_metrics['total_tasks']
    total_learnings = active_metrics['total_learnings'] + completed_metrics['total_learnings'] + runs_learnings
    total_decisions = active_metrics['total_decisions'] + completed_metrics['total_decisions'] + runs_decisions

    lines.append(f"Total Tasks:           {total_tasks}")
    lines.append(f"  - Active:            {active_metrics['total_tasks']}")
    lines.append(f"  - Completed:         {completed_metrics['total_tasks']}")
    lines.append(f"  - Autonomous Runs:   {runs_metrics['total_tasks']}")
    lines.append("")
    lines.append(f"Total Learnings:       {total_learnings}")
    lines.append(f"  - From Tasks:        {active_metrics['total_learnings'] + completed_metrics['total_learnings']}")
    lines.append(f"  - From Runs:         {runs_learnings}")
    lines.append(f"Total Decisions:       {total_decisions}")
    lines.append(f"  - From Tasks:        {active_metrics['total_decisions'] + completed_metrics['total_decisions']}")
    lines.append(f"  - From Runs:         {runs_decisions}")
    lines.append("")

    # Active Tasks Metrics
    lines.append("-" * 70)
    lines.append("ACTIVE TASKS METRICS")
    lines.append("-" * 70)
    lines.append(f"Tasks with Learnings:  {active_metrics['tasks_with_learnings']} / {active_metrics['total_tasks']} ({active_metrics['learning_extraction_rate']}%)")
    lines.append(f"Tasks with Decisions:  {active_metrics['tasks_with_decisions']} / {active_metrics['total_tasks']} ({active_metrics['decision_extraction_rate']}%)")
    lines.append(f"Tasks with Both:       {active_metrics['tasks_with_both']} / {active_metrics['total_tasks']}")
    lines.append(f"Tasks with Neither:    {active_metrics['tasks_with_neither']} / {active_metrics['total_tasks']}")
    lines.append(f"Overall Extraction:    {active_metrics['overall_extraction_rate']}%")
    lines.append("")

    # Completed Tasks Metrics
    lines.append("-" * 70)
    lines.append("COMPLETED TASKS METRICS")
    lines.append("-" * 70)
    lines.append(f"Tasks with Learnings:  {completed_metrics['tasks_with_learnings']} / {completed_metrics['total_tasks']} ({completed_metrics['learning_extraction_rate']}%)")
    lines.append(f"Tasks with Decisions:  {completed_metrics['tasks_with_decisions']} / {completed_metrics['total_tasks']} ({completed_metrics['decision_extraction_rate']}%)")
    lines.append(f"Tasks with Both:       {completed_metrics['tasks_with_both']} / {completed_metrics['total_tasks']}")
    lines.append(f"Tasks with Neither:    {completed_metrics['tasks_with_neither']} / {completed_metrics['total_tasks']}")
    lines.append(f"Overall Extraction:    {completed_metrics['overall_extraction_rate']}%")
    lines.append("")

    # Autonomous Runs Metrics
    lines.append("-" * 70)
    lines.append("AUTONOMOUS RUNS METRICS")
    lines.append("-" * 70)
    lines.append(f"Runs with Learnings:   {runs_metrics['tasks_with_learnings']} / {runs_metrics['total_tasks']} ({runs_metrics['learning_extraction_rate']}%)")
    lines.append(f"Runs with Decisions:   {runs_metrics['tasks_with_decisions']} / {runs_metrics['total_tasks']} ({runs_metrics['decision_extraction_rate']}%)")
    lines.append(f"Runs with Both:        {runs_metrics['tasks_with_both']} / {runs_metrics['total_tasks']}")
    lines.append(f"Runs with Neither:     {runs_metrics['tasks_with_neither']} / {runs_metrics['total_tasks']}")
    lines.append(f"Overall Extraction:    {runs_metrics['overall_extraction_rate']}%")
    lines.append(f"Total Learnings:       {runs_learnings}")
    lines.append(f"Total Decisions:       {runs_decisions}")
    lines.append("")

    # By Type
    lines.append("-" * 70)
    lines.append("EXTRACTION BY TASK TYPE")
    lines.append("-" * 70)

    all_types = set(active_metrics['by_type'].keys()) | set(completed_metrics['by_type'].keys()) | set(runs_metrics['by_type'].keys())

    for task_type in sorted(all_types):
        lines.append(f"\n{task_type.upper()}:")

        if task_type in active_metrics['by_type']:
            data = active_metrics['by_type'][task_type]
            rate = (data['with_learnings'] / data['count'] * 100) if data['count'] > 0 else 0
            lines.append(f"  Active:    {data['with_learnings']}/{data['count']} learnings ({rate:.1f}%), {data['total_decisions']} decisions")

        if task_type in completed_metrics['by_type']:
            data = completed_metrics['by_type'][task_type]
            rate = (data['with_learnings'] / data['count'] * 100) if data['count'] > 0 else 0
            lines.append(f"  Completed: {data['with_learnings']}/{data['count']} learnings ({rate:.1f}%), {data['total_decisions']} decisions")

        if task_type in runs_metrics['by_type']:
            data = runs_metrics['by_type'][task_type]
            rate = (data['with_learnings'] / data['count'] * 100) if data['count'] > 0 else 0
            lines.append(f"  Runs:      {data['with_learnings']}/{data['count']} learnings ({rate:.1f}%), {data['total_decisions']} decisions")

    lines.append("")

    # Low Extraction Tasks
    lines.append("-" * 70)
    lines.append("TASKS MISSING EXTRACTIONS")
    lines.append("-" * 70)

    all_low = active_metrics['low_extraction_tasks'] + completed_metrics['low_extraction_tasks'] + runs_metrics['low_extraction_tasks']

    if all_low:
        lines.append(f"Total: {len(all_low)} tasks with no learnings or decisions\n")

        # Show active first
        active_low = [t for t in all_low if t['id'] in [a['id'] for a in active_metrics['low_extraction_tasks']]]
        completed_low = [t for t in all_low if t['id'] in [c['id'] for c in completed_metrics['low_extraction_tasks']]]
        runs_low = [t for t in all_low if t['id'] in [r['id'] for r in runs_metrics['low_extraction_tasks']]]

        if active_low:
            lines.append("ACTIVE TASKS:")
            for task in active_low[:10]:  # Show first 10
                lines.append(f"  - {task['id']} ({task['type']})")
            if len(active_low) > 10:
                lines.append(f"  ... and {len(active_low) - 10} more")
            lines.append("")

        if completed_low:
            lines.append("COMPLETED TASKS:")
            for task in completed_low[:10]:
                lines.append(f"  - {task['id']} ({task['type']})")
            if len(completed_low) > 10:
                lines.append(f"  ... and {len(completed_low) - 10} more")
            lines.append("")

        if runs_low:
            lines.append("AUTONOMOUS RUNS:")
            for task in runs_low[:10]:
                lines.append(f"  - {task['id']}")
            if len(runs_low) > 10:
                lines.append(f"  ... and {len(runs_low) - 10} more")
    else:
        lines.append("All tasks have at least one learning or decision recorded!")

    lines.append("")
    lines.append("=" * 70)
    lines.append("END OF REPORT")
    lines.append("=" * 70)

    return "\n".join(lines)


def format_json_report(active_metrics: Dict, completed_metrics: Dict, runs_metrics: Dict, runs_learnings: int, runs_decisions: int) -> str:
    """Format metrics as JSON."""
    report = {
        'generated_at': datetime.now().isoformat(),
        'active_tasks': active_metrics,
        'completed_tasks': completed_metrics,
        'autonomous_runs': runs_metrics,
        'summary': {
            'total_tasks': active_metrics['total_tasks'] + completed_metrics['total_tasks'],
            'total_learnings': active_metrics['total_learnings'] + completed_metrics['total_learnings'] + runs_learnings,
            'total_decisions': active_metrics['total_decisions'] + completed_metrics['total_decisions'] + runs_decisions,
            'overall_extraction_rate': round(
                (active_metrics['overall_extraction_rate'] + completed_metrics['overall_extraction_rate']) / 2, 1
            )
        }
    }
    return json.dumps(report, indent=2)


def format_yaml_report(active_metrics: Dict, completed_metrics: Dict, runs_metrics: Dict, runs_learnings: int, runs_decisions: int) -> str:
    """Format metrics as YAML."""
    report = {
        'generated_at': datetime.now().isoformat(),
        'active_tasks': active_metrics,
        'completed_tasks': completed_metrics,
        'autonomous_runs': runs_metrics,
        'summary': {
            'total_tasks': active_metrics['total_tasks'] + completed_metrics['total_tasks'],
            'total_learnings': active_metrics['total_learnings'] + completed_metrics['total_learnings'] + runs_learnings,
            'total_decisions': active_metrics['total_decisions'] + completed_metrics['total_decisions'] + runs_decisions,
            'overall_extraction_rate': round(
                (active_metrics['overall_extraction_rate'] + completed_metrics['overall_extraction_rate']) / 2, 1
            )
        }
    }
    return yaml.dump(report, default_flow_style=False, sort_keys=False)


def main():
    parser = argparse.ArgumentParser(
        description='Track learning/decision extraction rates from completed tasks'
    )
    parser.add_argument(
        '--project',
        type=str,
        default=os.path.expanduser('~/.blackbox5/5-project-memory/blackbox5'),
        help='Project directory to analyze'
    )
    parser.add_argument(
        '--output',
        type=str,
        choices=['text', 'json', 'yaml'],
        default='text',
        help='Output format'
    )
    parser.add_argument(
        '--save',
        type=str,
        help='Save report to file'
    )
    parser.add_argument(
        '--min-learnings',
        type=int,
        default=1,
        help='Minimum learnings threshold'
    )
    parser.add_argument(
        '--min-decisions',
        type=int,
        default=1,
        help='Minimum decisions threshold'
    )

    args = parser.parse_args()

    project_path = Path(args.project)

    if not project_path.exists():
        print(f"Error: Project path does not exist: {project_path}", file=sys.stderr)
        sys.exit(1)

    # Scan project
    active_tasks, completed_tasks, runs_data, runs_learnings, runs_decisions = scan_project(project_path)

    # Calculate metrics
    active_metrics = calculate_extraction_metrics(active_tasks)
    completed_metrics = calculate_extraction_metrics(completed_tasks)
    runs_metrics = calculate_extraction_metrics(runs_data)

    # Format report
    if args.output == 'json':
        report = format_json_report(active_metrics, completed_metrics, runs_metrics, runs_learnings, runs_decisions)
    elif args.output == 'yaml':
        report = format_yaml_report(active_metrics, completed_metrics, runs_metrics, runs_learnings, runs_decisions)
    else:
        report = format_text_report(active_metrics, completed_metrics, runs_metrics, runs_learnings, runs_decisions)

    # Output
    if args.save:
        save_path = Path(args.save)
        save_path.write_text(report, encoding='utf-8')
        print(f"Report saved to: {save_path}")
    else:
        print(report)


if __name__ == '__main__':
    main()
