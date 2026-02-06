#!/usr/bin/env python3
"""
Skill Registry Access Module

Unified interface for accessing skill data from skill-registry.yaml.
Replaces multiple file reads with a single registry access.

Usage:
    from skill_registry import SkillRegistry

    registry = SkillRegistry()

    # Get all skills
    skills = registry.get_all_skills()

    # Get specific skill
    skill = registry.get_skill("bmad-dev")

    # Get skills by category
    agents = registry.get_skills_by_category("agent")

    # Get selection criteria for a skill
    criteria = registry.get_selection_criteria("bmad-dev")

    # Get metrics for a skill
    metrics = registry.get_skill_metrics("bmad-dev")

    # Log usage
    registry.log_usage("TASK-001", "bmad-dev", outcome="success")

    # Add task outcome
    registry.add_task_outcome({
        "task_id": "TASK-001",
        "skill_used": "bmad-dev",
        "outcome": "success",
        "quality_rating": 4
    })
"""

import yaml
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

from atomic_io import atomic_write_yaml

# Default path to the unified registry
DEFAULT_REGISTRY_PATH = Path("/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/operations/skill-registry.yaml")


class SkillRegistry:
    """Unified interface for skill registry operations."""

    def __init__(self, registry_path: Optional[Path] = None):
        """Initialize the registry with the given path."""
        self.registry_path = registry_path or DEFAULT_REGISTRY_PATH
        self._data: Optional[dict] = None
        self._load()

    def _load(self) -> None:
        """Load the registry data from file."""
        if not self.registry_path.exists():
            raise FileNotFoundError(f"Registry not found: {self.registry_path}")

        with open(self.registry_path, 'r') as f:
            self._data = yaml.safe_load(f) or {}

    def _save(self) -> None:
        """Save the registry data to file atomically with locking."""
        if self._data is None:
            return

        # Update metadata
        self._data['metadata']['last_updated'] = datetime.now(timezone.utc).isoformat()

        # Atomic write with file locking
        atomic_write_yaml(self._data, self.registry_path, create_backup=True)

    def reload(self) -> None:
        """Reload the registry from disk."""
        self._load()

    # -------------------------------------------------------------------------
    # Skill Queries
    # -------------------------------------------------------------------------

    def get_all_skills(self) -> dict[str, dict]:
        """Get all skills from the registry."""
        return self._data.get('skills', {})

    def get_skill(self, skill_id: str) -> Optional[dict]:
        """Get a specific skill by ID."""
        return self._data.get('skills', {}).get(skill_id)

    def get_skills_by_category(self, category: str) -> dict[str, dict]:
        """Get all skills in a specific category."""
        skills = self._data.get('skills', {})
        return {
            skill_id: skill for skill_id, skill in skills.items()
            if skill.get('category') == category
        }

    def skill_exists(self, skill_id: str) -> bool:
        """Check if a skill exists in the registry."""
        return skill_id in self._data.get('skills', {})

    # -------------------------------------------------------------------------
    # Metrics Queries
    # -------------------------------------------------------------------------

    def get_skill_metrics(self, skill_id: str) -> Optional[dict]:
        """Get metrics for a specific skill."""
        skill = self.get_skill(skill_id)
        if skill:
            return skill.get('metrics')
        return None

    def get_effectiveness_score(self, skill_id: str) -> Optional[float]:
        """Get the effectiveness score for a skill."""
        metrics = self.get_skill_metrics(skill_id)
        if metrics:
            return metrics.get('effectiveness_score')
        return None

    def get_all_metrics(self) -> dict[str, dict]:
        """Get metrics for all skills."""
        return {
            skill_id: skill.get('metrics', {})
            for skill_id, skill in self.get_all_skills().items()
        }

    # -------------------------------------------------------------------------
    # Usage Queries
    # -------------------------------------------------------------------------

    def get_usage_stats(self, skill_id: str) -> Optional[dict]:
        """Get usage statistics for a skill."""
        skill = self.get_skill(skill_id)
        if skill:
            return skill.get('usage')
        return None

    def get_usage_history(self) -> list[dict]:
        """Get the full usage history."""
        return self._data.get('usage_history', [])

    def get_task_outcomes(self, skill_id: Optional[str] = None) -> list[dict]:
        """Get task outcomes, optionally filtered by skill."""
        outcomes = self._data.get('task_outcomes', [])
        if skill_id:
            return [o for o in outcomes if o.get('skill_used') == skill_id]
        return outcomes

    # -------------------------------------------------------------------------
    # Selection Criteria Queries
    # -------------------------------------------------------------------------

    def get_selection_criteria(self, skill_id: str) -> Optional[dict]:
        """Get selection criteria for a skill."""
        skill = self.get_skill(skill_id)
        if skill:
            return skill.get('selection')
        return None

    def get_auto_trigger_rules(self) -> list[dict]:
        """Get all auto-trigger rules."""
        framework = self._data.get('selection_framework', {})
        return framework.get('auto_trigger_rules', [])

    def get_confidence_threshold(self) -> int:
        """Get the global confidence threshold."""
        framework = self._data.get('selection_framework', {})
        return framework.get('confidence_threshold', 70)

    def find_matching_skills(self, task_description: str) -> list[tuple[str, float]]:
        """
        Find skills that match a task description.
        Returns list of (skill_id, confidence) tuples sorted by confidence.
        """
        task_lower = task_description.lower()
        matches = []

        for skill_id, skill in self.get_all_skills().items():
            selection = skill.get('selection', {})
            triggers = selection.get('triggers', [])

            # Calculate simple keyword match score
            match_count = sum(1 for trigger in triggers if trigger.lower() in task_lower)
            if match_count > 0:
                confidence = min(100, match_count * 20)  # 20% per match, max 100%
                matches.append((skill_id, confidence))

        # Sort by confidence descending
        matches.sort(key=lambda x: x[1], reverse=True)
        return matches

    # -------------------------------------------------------------------------
    # Data Modification
    # -------------------------------------------------------------------------

    def log_usage(
        self,
        task_id: str,
        skill_id: Optional[str],
        confidence: Optional[int] = None,
        outcome: Optional[str] = None,
        duration_minutes: Optional[int] = None,
        notes: str = ""
    ) -> None:
        """Log a skill usage entry."""
        entry = {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'task_id': task_id,
            'skill': skill_id,
            'confidence': confidence,
            'result': outcome or 'unknown',
            'notes': notes
        }

        # Remove None values
        entry = {k: v for k, v in entry.items() if v is not None}

        if 'usage_history' not in self._data:
            self._data['usage_history'] = []

        self._data['usage_history'].append(entry)

        # Update skill usage stats if skill specified
        if skill_id and skill_id in self._data.get('skills', {}):
            self._update_skill_usage_stats(skill_id, outcome, duration_minutes)

        self._save()

    def _update_skill_usage_stats(
        self,
        skill_id: str,
        outcome: Optional[str],
        duration_minutes: Optional[int]
    ) -> None:
        """Update usage statistics for a skill."""
        skill = self._data['skills'][skill_id]
        usage = skill.setdefault('usage', {})

        # Update counts
        usage['usage_count'] = usage.get('usage_count', 0) + 1

        if outcome == 'success':
            usage['success_count'] = usage.get('success_count', 0) + 1
        elif outcome == 'failure':
            usage['failure_count'] = usage.get('failure_count', 0) + 1

        # Update timestamps
        now = datetime.now(timezone.utc).isoformat()
        if not usage.get('first_used'):
            usage['first_used'] = now
        usage['last_used'] = now

        # Update average execution time
        if duration_minutes:
            duration_ms = duration_minutes * 60 * 1000
            current_avg = usage.get('avg_execution_time_ms')
            current_count = usage.get('usage_count', 1)

            if current_avg:
                usage['avg_execution_time_ms'] = (
                    (current_avg * (current_count - 1) + duration_ms) // current_count
                )
            else:
                usage['avg_execution_time_ms'] = duration_ms

    def add_task_outcome(self, outcome: dict) -> None:
        """Add a task outcome record."""
        if 'task_outcomes' not in self._data:
            self._data['task_outcomes'] = []

        # Ensure timestamp
        if 'timestamp' not in outcome:
            outcome['timestamp'] = datetime.now(timezone.utc).isoformat()

        self._data['task_outcomes'].append(outcome)
        self._save()

    def update_skill_metrics(self, skill_id: str, metrics: dict) -> None:
        """Update metrics for a skill."""
        if skill_id not in self._data.get('skills', {}):
            raise ValueError(f"Skill not found: {skill_id}")

        self._data['skills'][skill_id]['metrics'] = metrics
        self._save()

    # -------------------------------------------------------------------------
    # Analysis Queries
    # -------------------------------------------------------------------------

    def get_analysis(self) -> dict:
        """Get the analysis section."""
        return self._data.get('analysis', {})

    def get_category_performance(self) -> list[dict]:
        """Get performance by category."""
        analysis = self._data.get('analysis', {})
        return analysis.get('category_performance', [])

    def get_roi_summary(self) -> dict:
        """Get the ROI summary."""
        analysis = self._data.get('analysis', {})
        return analysis.get('roi_summary', {})

    def get_top_skills(self, limit: int = 5) -> list[dict]:
        """Get top performing skills."""
        analysis = self._data.get('analysis', {})
        return analysis.get('top_skills', [])[:limit]


# -------------------------------------------------------------------------
# Backward Compatibility Functions
# -------------------------------------------------------------------------

def load_skill_metrics() -> dict:
    """
    Backward compatible function to load skill metrics.
    Previously loaded from skill-metrics.yaml, now uses unified registry.
    """
    registry = SkillRegistry()
    return {
        'skills': [
            {
                'name': skill_id,
                'category': skill.get('category'),
                'effectiveness_score': skill.get('metrics', {}).get('effectiveness_score'),
                'metrics': skill.get('metrics', {}),
                'baseline_minutes': skill.get('roi', {}).get('baseline_minutes'),
                'roi_calculation': skill.get('roi', {}),
                'recommendations': {
                    'when_to_use': skill.get('selection', {}).get('when_to_use'),
                    'when_to_avoid': skill.get('selection', {}).get('when_to_avoid'),
                    'confidence': skill.get('selection', {}).get('confidence'),
                }
            }
            for skill_id, skill in registry.get_all_skills().items()
        ],
        'task_outcomes': registry.get_task_outcomes(),
        'analysis': registry.get_analysis(),
        'metadata': registry._data.get('metadata', {})
    }


def load_skill_usage() -> dict:
    """
    Backward compatible function to load skill usage.
    Previously loaded from skill-usage.yaml, now uses unified registry.
    """
    registry = SkillRegistry()
    return {
        'skills': [
            {
                'name': skill_id,
                'description': skill.get('description'),
                'category': skill.get('category'),
                'agent': skill.get('agent'),
                **skill.get('usage', {})
            }
            for skill_id, skill in registry.get_all_skills().items()
        ],
        'usage_log': registry.get_usage_history(),
        'metadata': registry._data.get('metadata', {})
    }


def save_skill_metrics(data: dict) -> None:
    """
    Backward compatible function to save skill metrics.
    Updates the unified registry.
    """
    registry = SkillRegistry()

    for skill_data in data.get('skills', []):
        skill_id = skill_data.get('name')
        if skill_id and registry.skill_exists(skill_id):
            if 'metrics' in skill_data:
                registry.update_skill_metrics(skill_id, skill_data['metrics'])


# -------------------------------------------------------------------------
# CLI Interface
# -------------------------------------------------------------------------

if __name__ == '__main__':
    import argparse
    import json

    parser = argparse.ArgumentParser(description='Skill Registry CLI')
    subparsers = parser.add_subparsers(dest='command')

    # List command
    list_parser = subparsers.add_parser('list', help='List all skills')
    list_parser.add_argument('--category', help='Filter by category')
    list_parser.add_argument('--json', action='store_true', help='Output as JSON')

    # Get command
    get_parser = subparsers.add_parser('get', help='Get skill details')
    get_parser.add_argument('skill', help='Skill ID')
    get_parser.add_argument('--json', action='store_true', help='Output as JSON')

    # Metrics command
    metrics_parser = subparsers.add_parser('metrics', help='Show metrics')
    metrics_parser.add_argument('--skill', help='Specific skill (default: all)')

    # Match command
    match_parser = subparsers.add_parser('match', help='Find matching skills for task')
    match_parser.add_argument('description', help='Task description')

    args = parser.parse_args()

    registry = SkillRegistry()

    if args.command == 'list':
        if args.category:
            skills = registry.get_skills_by_category(args.category)
        else:
            skills = registry.get_all_skills()

        if args.json:
            print(json.dumps(skills, indent=2))
        else:
            print(f"{'Skill ID':<30} {'Name':<25} {'Category':<15} {'Usage':<10}")
            print("-" * 80)
            for skill_id, skill in sorted(skills.items()):
                usage = skill.get('usage', {})
                count = usage.get('usage_count', 0)
                print(f"{skill_id:<30} {skill.get('name', 'N/A'):<25} "
                      f"{skill.get('category', 'N/A'):<15} {count:<10}")

    elif args.command == 'get':
        skill = registry.get_skill(args.skill)
        if skill:
            if args.json:
                print(json.dumps(skill, indent=2))
            else:
                print(f"Skill: {args.skill}")
                print(f"Name: {skill.get('name')}")
                print(f"Description: {skill.get('description')}")
                print(f"Category: {skill.get('category')}")
                print(f"Agent: {skill.get('agent') or 'N/A'}")
                print(f"\nMetrics:")
                for key, value in skill.get('metrics', {}).items():
                    print(f"  {key}: {value or 'N/A'}")
                print(f"\nUsage:")
                for key, value in skill.get('usage', {}).items():
                    print(f"  {key}: {value or 'N/A'}")
        else:
            print(f"Skill not found: {args.skill}", file=sys.stderr)
            sys.exit(1)

    elif args.command == 'metrics':
        if args.skill:
            metrics = registry.get_skill_metrics(args.skill)
            if metrics:
                print(f"Metrics for {args.skill}:")
                for key, value in metrics.items():
                    print(f"  {key}: {value or 'N/A'}")
            else:
                print(f"No metrics found for {args.skill}")
        else:
            print("All Skills Metrics:")
            print(f"{'Skill':<30} {'Effectiveness':<15} {'Success Rate':<15} {'Usage Count':<12}")
            print("-" * 75)
            for skill_id in sorted(registry.get_all_skills().keys()):
                metrics = registry.get_skill_metrics(skill_id) or {}
                usage = registry.get_usage_stats(skill_id) or {}
                eff = metrics.get('effectiveness_score')
                sr = metrics.get('success_rate')
                count = usage.get('usage_count', 0)
                print(f"{skill_id:<30} {str(eff) if eff else 'N/A':<15} "
                      f"{str(sr) + '%' if sr else 'N/A':<15} {count:<12}")

    elif args.command == 'match':
        matches = registry.find_matching_skills(args.description)
        print(f"Matching skills for: {args.description}")
        print(f"{'Skill':<30} {'Confidence':<12}")
        print("-" * 45)
        for skill_id, confidence in matches[:10]:
            print(f"{skill_id:<30} {confidence}%")

    else:
        parser.print_help()
