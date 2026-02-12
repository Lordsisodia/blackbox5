#!/usr/bin/env python3
"""
Skill Comparison Report Generator

Generates A/B comparison reports for skill effectiveness by comparing
tasks completed with skills vs without skills.

Usage:
    python3 skill-comparison-report.py
    python3 skill-comparison-report.py --skill git-automation
    python3 skill-comparison-report.py --output /tmp/report.md
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional


class SkillComparisonReport:
    """Generate comparison reports for skill effectiveness."""

    def __init__(self, registry_path: str = None):
        """
        Initialize comparison report generator.

        Args:
            registry_path: Path to skill-registry.yaml file
        """
        if registry_path is None:
            # Default path relative to BlackBox5 project root
            bb5_root = Path(__file__).parent.parent
            registry_path = bb5_root / "5-project-memory/blackbox5/operations/skill-registry.yaml"

        self.registry_path = Path(registry_path)
        self.registry = self._load_registry()

    def _load_registry(self) -> Dict[str, Any]:
        """Load skill registry from YAML file."""
        try:
            import yaml
            with open(self.registry_path, 'r') as f:
                return yaml.safe_load(f)
        except ImportError:
            print("Error: PyYAML not installed. Run: pip install pyyaml", file=sys.stderr)
            sys.exit(1)
        except FileNotFoundError:
            print(f"Error: Registry file not found: {self.registry_path}", file=sys.stderr)
            sys.exit(1)

    def generate_summary(self) -> str:
        """Generate a summary of comparison data."""
        comparison_pairs = self.registry.get('comparison_pairs', [])

        if not comparison_pairs:
            return "# No comparison data available\n\nAdd comparison pairs to skill-registry.yaml to generate reports."

        report_lines = [
            "# Skill Comparison Report\n",
            f"Generated: {datetime.now().isoformat()}",
            f"Total comparisons: {len(comparison_pairs)}",
            "",
            "## Summary Statistics\n",
            ""

        ]

        # Calculate overall statistics
        total_time_saved = 0
        total_percent_saved = 0
        task_types = set()

        for pair in comparison_pairs:
            task_type = pair.get('task_type', 'unknown')
            time_saved = pair.get('time_saved_minutes', 0)
            percent_saved = pair.get('time_saved_percent', 0)

            total_time_saved += time_saved
            total_percent_saved += percent_saved
            task_types.add(task_type)

        if comparison_pairs:
            avg_time_saved = total_time_saved / len(comparison_pairs)
            avg_percent_saved = total_percent_saved / len(comparison_pairs)

            report_lines.extend([
                f"- **Total Time Saved:** {total_time_saved} minutes",
                f"- **Average Time Saved:** {avg_time_saved:.1f} minutes per task",
                f"- **Average Percent Saved:** {avg_percent_saved:.1f}% per task",
                f"- **Task Types Analyzed:** {len(task_types)}",
                ""
            ])

        # Generate per-skill breakdown
        report_lines.append("## Per-Skill Breakdown\n")
        report_lines.append("")

        skills_reported = {}
        for pair in comparison_pairs:
            for skill_task in pair.get('skill_tasks', []):
                skill = skill_task.get('skill_used', 'unknown')
                if skill not in skills_reported:
                    skills_reported[skill] = {
                        'time_saved': 0,
                        'percent_saved': 0,
                        'count': 0
                    }

                skills_reported[skill]['time_saved'] += pair.get('time_saved_minutes', 0)
                skills_reported[skill]['percent_saved'] += pair.get('time_saved_percent', 0)
                skills_reported[skill]['count'] += 1

        for skill, stats in sorted(skills_reported.items()):
            avg_time = stats['time_saved'] / stats['count'] if stats['count'] > 0 else 0
            avg_percent = stats['percent_saved'] / stats['count'] if stats['count'] > 0 else 0

            report_lines.extend([
                f"### {skill}",
                f"- **Comparisons:** {stats['count']}",
                f"- **Total Time Saved:** {stats['time_saved']} minutes",
                f"- **Avg Time Saved:** {avg_time:.1f} minutes",
                f"- **Avg Percent Saved:** {avg_percent:.1f}%",
                ""
            ])

        # Generate detailed breakdown by task type
        report_lines.append("## Detailed Comparison by Task Type\n")
        report_lines.append("")

        for pair in comparison_pairs:
            task_type = pair.get('task_type', 'unknown')
            report_lines.append(f"### {task_type}")
            report_lines.append("")

            # Baseline tasks
            report_lines.append("**Baseline Tasks (no skill):**")
            for baseline in pair.get('baseline_tasks', []):
                duration = baseline.get('duration_minutes', 0)
                report_lines.append(f"- {baseline.get('task_id')}: {duration} minutes")

            report_lines.append("")

            # Skill tasks
            report_lines.append("**Skill-Enhanced Tasks:**")
            for skill_task in pair.get('skill_tasks', []):
                skill = skill_task.get('skill_used', 'unknown')
                duration = skill_task.get('duration_minutes', 0)
                report_lines.append(f"- {skill_task.get('task_id')}: {duration} minutes (skill: {skill})")

            report_lines.append("")
            report_lines.extend([
                f"**Results:**",
                f"- Time Saved: {pair.get('time_saved_minutes', 0)} minutes",
                f"- Percent Saved: {pair.get('time_saved_percent', 0)}%",
                f"- Sample Size: {pair.get('sample_size', 0)}",
                f"- Confidence: {pair.get('confidence', 'unknown')}",
                ""
            ])

        return "\n".join(report_lines)

    def generate_skill_report(self, skill_name: str) -> str:
        """Generate report for a specific skill."""
        comparison_pairs = self.registry.get('comparison_pairs', [])

        # Filter comparisons for the specific skill
        skill_pairs = []
        for pair in comparison_pairs:
            for skill_task in pair.get('skill_tasks', []):
                if skill_task.get('skill_used', '').lower() == skill_name.lower():
                    skill_pairs.append(pair)
                    break

        if not skill_pairs:
            return f"# Skill Report: {skill_name}\n\nNo comparison data available for this skill."

        report_lines = [
            f"# Skill Report: {skill_name}",
            f"Generated: {datetime.now().isoformat()}",
            f"Comparisons found: {len(skill_pairs)}",
            "",
            "## Summary\n",
            ""
        ]

        total_time_saved = sum(p.get('time_saved_minutes', 0) for p in skill_pairs)
        total_percent_saved = sum(p.get('time_saved_percent', 0) for p in skill_pairs)
        avg_time_saved = total_time_saved / len(skill_pairs) if skill_pairs else 0
        avg_percent_saved = total_percent_saved / len(skill_pairs) if skill_pairs else 0

        report_lines.extend([
            f"- **Total Comparisons:** {len(skill_pairs)}",
            f"- **Total Time Saved:** {total_time_saved} minutes",
            f"- **Average Time Saved:** {avg_time_saved:.1f} minutes",
            f"- **Average Percent Saved:** {avg_percent_saved:.1f}%",
            ""
        ])

        report_lines.append("## Detailed Comparisons\n")
        report_lines.append("")

        for pair in skill_pairs:
            task_type = pair.get('task_type', 'unknown')
            report_lines.extend([
                f"### {task_type}",
                "",
                f"- **Time Saved:** {pair.get('time_saved_minutes', 0)} minutes",
                f"- **Percent Saved:** {pair.get('time_saved_percent', 0)}%",
                f"- **Sample Size:** {pair.get('sample_size', 0)}",
                f"- **Confidence:** {pair.get('confidence', 'unknown')}",
                ""
            ])

        return "\n".join(report_lines)

    def calculate_time_savings(self, baseline_minutes: int, skill_minutes: int) -> Dict[str, Any]:
        """
        Calculate time savings between baseline and skill-enhanced task.

        Args:
            baseline_minutes: Duration of baseline task (no skill)
            skill_minutes: Duration of skill-enhanced task

        Returns:
            Dictionary with time_saved_minutes and time_saved_percent
        """
        time_saved = baseline_minutes - skill_minutes
        percent_saved = (time_saved / baseline_minutes * 100) if baseline_minutes > 0 else 0

        return {
            'time_saved_minutes': max(0, time_saved),  # Don't show negative savings
            'time_saved_percent': round(max(0, percent_saved), 1)
        }


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Generate skill comparison reports',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate summary report
  python3 skill-comparison-report.py

  # Generate report for specific skill
  python3 skill-comparison-report.py --skill git-automation

  # Save report to file
  python3 skill-comparison-report.py --output /tmp/report.md

  # Calculate time savings
  python3 skill-comparison-report.py --calculate 30 15
        """
    )

    parser.add_argument(
        '--skill',
        help='Generate report for specific skill only'
    )

    parser.add_argument(
        '--output',
        help='Output file path (default: stdout)'
    )

    parser.add_argument(
        '--calculate',
        nargs=2,
        metavar=('BASELINE', 'SKILL'),
        type=int,
        help='Calculate time savings: baseline_minutes skill_minutes'
    )

    parser.add_argument(
        '--registry',
        help='Path to skill-registry.yaml (default: auto-detect)'
    )

    args = parser.parse_args()

    report = SkillComparisonReport(registry_path=args.registry)

    # Handle calculation mode
    if args.calculate:
        baseline, skill = args.calculate
        savings = report.calculate_time_savings(baseline, skill)
        print(f"Time Saved: {savings['time_saved_minutes']} minutes")
        print(f"Percent Saved: {savings['time_saved_percent']}%")
        return

    # Generate report
    if args.skill:
        report_text = report.generate_skill_report(args.skill)
    else:
        report_text = report.generate_summary()

    # Output
    if args.output:
        with open(args.output, 'w') as f:
            f.write(report_text)
        print(f"Report saved to: {args.output}")
    else:
        print(report_text)


if __name__ == '__main__':
    main()
