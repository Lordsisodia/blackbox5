#!/usr/bin/env python3
"""
Automated Skill Detection Script
Analyzes task input and returns recommended skills with confidence scores.
"""

import argparse
import json
import sys
import re
from pathlib import Path
from typing import List, Dict, Tuple

try:
    import yaml
except ImportError:
    print("Error: PyYAML not installed. Run: pip install pyyaml", file=sys.stderr)
    sys.exit(3)


def load_skill_registry(registry_path: str) -> Dict:
    """Load skill registry from YAML file."""
    try:
        with open(registry_path, 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"Error: Skill registry not found at {registry_path}", file=sys.stderr)
        sys.exit(3)
    except yaml.YAMLError as e:
        print(f"Error parsing skill registry: {e}", file=sys.stderr)
        sys.exit(3)


def calculate_keyword_score(task: str, triggers: List[str]) -> Tuple[float, List[str]]:
    """
    Calculate keyword matching score and return matched keywords.
    - Exact match: +40 points
    - Partial match (word boundary): +25 points
    """
    task_lower = task.lower()
    matched_keywords = []
    score = 0

    for trigger in triggers:
        trigger_lower = trigger.lower()

        # Exact match (whole word)
        if re.search(rf'\b{re.escape(trigger_lower)}\b', task_lower):
            score += 40
            matched_keywords.append(trigger)
        # Partial match (substring)
        elif trigger_lower in task_lower:
            score += 25
            matched_keywords.append(trigger)

    # Normalize to 0-100 scale (direct proportion)
    # Base score is already high enough with 40 points per match
    normalized_score = min(score, 100)

    return normalized_score, matched_keywords


def calculate_confidence(task: str, skill_data: Dict) -> float:
    """
    Calculate confidence score for a skill.
    Formula: (keyword_match_score * 0.5 +
              domain_match_score * 0.2 +
              task_type_match_score * 0.2 +
              context_match_score * 0.1)
    """
    triggers = skill_data.get('selection', {}).get('triggers', [])

    # Keyword matching (50% - most important)
    keyword_score, matched = calculate_keyword_score(task, triggers)

    # Domain matching (20%) - Check if task contains domain-relevant terms
    category = skill_data.get('category', '')
    domain_score = 0
    if category in ['agent', 'core']:
        # High relevance category
        domain_score = 80
    elif category in ['testing', 'documentation']:
        # Medium relevance
        domain_score = 60
    else:
        domain_score = 40

    # Task type matching (20%) - Check task patterns
    task_type_score = 50  # Default middle score
    task_lower = task.lower()

    # Identify task type patterns
    if any(word in task_lower for word in ['implement', 'create', 'build', 'develop']):
        task_type_score = 80
    elif any(word in task_lower for word in ['fix', 'bug', 'error', 'issue']):
        task_type_score = 70
    elif any(word in task_lower for word in ['analyze', 'review', 'audit', 'check']):
        task_type_score = 60
    elif any(word in task_lower for word in ['document', 'write', 'readme', 'guide']):
        task_type_score = 50

    # Context matching (10%) - Check confidence from registry
    current_confidence = skill_data.get('selection', {}).get('confidence', 'medium')
    context_scores = {'high': 90, 'medium': 60, 'low': 30}
    context_score = context_scores.get(current_confidence, 50)

    # Calculate weighted composite score
    confidence = (
        keyword_score * 0.5 +
        domain_score * 0.2 +
        task_type_score * 0.2 +
        context_score * 0.1
    )

    return confidence


def determine_trigger_type(confidence: float, threshold: float) -> str:
    """
    Determine trigger type based on confidence and threshold.

    Logic:
    - confidence >= 85: Clear trigger - MUST invoke regardless of threshold
    - threshold <= confidence < 85: Discretionary - SHOULD invoke
    - confidence < threshold: None - MAY check
    """
    if confidence >= 85:
        return "clear"
    elif confidence >= threshold:
        return "discretionary"
    else:
        return "none"


def detect_skills(task: str, registry: Dict, limit: int = 10) -> List[Dict]:
    """Detect recommended skills for a task."""
    results = []

    for skill_id, skill_data in registry.get('skills', {}).items():
        # Skip infrastructure skills (local-dev only)
        if skill_data.get('category') == 'infrastructure':
            continue

        confidence = calculate_confidence(task, skill_data)
        threshold = skill_data.get('selection', {}).get('confidence_threshold', 70)
        trigger_type = determine_trigger_type(confidence, threshold)
        triggers = skill_data.get('selection', {}).get('triggers', [])

        # Get matched keywords
        keyword_score, matched = calculate_keyword_score(task, triggers)

        results.append({
            'id': skill_id,
            'name': skill_data.get('name', skill_id),
            'confidence': round(confidence, 1),
            'trigger_type': trigger_type,
            'matched_keywords': matched
        })

    # Sort by confidence descending
    results.sort(key=lambda x: x['confidence'], reverse=True)

    return results[:limit]


def main():
    parser = argparse.ArgumentParser(
        description='Detect recommended skills for a task',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  detect-skill.py "Implement git commit workflow"
  echo "Create PRD for user authentication" | detect-skill.py --stdin
  detect-skill.py --task-file /path/to/task.md

Exit Codes:
  0: Clear trigger (>=85% confidence) - MUST invoke
  1: Discretionary (70-84% confidence) - SHOULD invoke
  2: No match (<70% confidence) - MAY check
  3: Error
        """
    )

    parser.add_argument('task', nargs='?', help='Task description')
    parser.add_argument('--stdin', action='store_true', help='Read task from stdin')
    parser.add_argument('--task-file', type=str, help='Read task from file')
    parser.add_argument('--registry', type=str,
                       default='/opt/blackbox5/5-project-memory/blackbox5/operations/skill-registry.yaml',
                       help='Path to skill registry YAML')
    parser.add_argument('--limit', type=int, default=10,
                       help='Maximum number of skills to return (default: 10)')

    args = parser.parse_args()

    # Get task text
    if args.stdin:
        task_text = sys.stdin.read().strip()
    elif args.task_file:
        try:
            with open(args.task_file, 'r') as f:
                task_text = f.read().strip()
        except FileNotFoundError:
            print(f"Error: Task file not found: {args.task_file}", file=sys.stderr)
            sys.exit(3)
    elif args.task:
        task_text = args.task.strip()
    else:
        parser.print_help()
        sys.exit(3)

    if not task_text:
        print("Error: No task text provided", file=sys.stderr)
        sys.exit(3)

    # Load skill registry
    registry = load_skill_registry(args.registry)

    # Detect skills
    skills = detect_skills(task_text, registry, limit=args.limit)

    # Determine overall action
    if not skills:
        action_required = "MAY check (no matches)"
        exit_code = 2
    else:
        top_skill = skills[0]
        if top_skill['trigger_type'] == 'clear':
            action_required = "MUST invoke"
            exit_code = 0
        elif top_skill['trigger_type'] == 'discretionary':
            action_required = "SHOULD invoke"
            exit_code = 1
        else:
            action_required = "MAY check"
            exit_code = 2

    # Create output
    output = {
        'task_summary': task_text[:200] + ('...' if len(task_text) > 200 else ''),
        'recommended_skills': skills[:3],  # Top 3 as primary recommendations
        'action_required': action_required,
        'all_matches': skills  # All matches for reference
    }

    # Output JSON
    print(json.dumps(output, indent=2))

    # Return exit code
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
