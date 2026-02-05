#!/usr/bin/env python3
"""
Skill Metrics Calculator

Calculates effectiveness metrics for all skills based on task outcomes data.
Updates skill-metrics.yaml with calculated values.

Usage:
    python calculate-skill-metrics.py [--dry-run]

Exit Codes:
    0 - Success
    1 - Data file not found
    2 - YAML parsing error
    3 - Calculation error
"""

import argparse
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml


def load_yaml_file(filepath: Path) -> dict:
    """Load and parse YAML file."""
    try:
        with open(filepath, 'r') as f:
            return yaml.safe_load(f) or {}
    except FileNotFoundError:
        print(f"Error: File not found: {filepath}", file=sys.stderr)
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"Error parsing YAML: {e}", file=sys.stderr)
        sys.exit(2)


def save_yaml_file(filepath: Path, data: dict) -> None:
    """Save data to YAML file."""
    try:
        with open(filepath, 'w') as f:
            yaml.dump(data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
    except Exception as e:
        print(f"Error saving YAML: {e}", file=sys.stderr)
        sys.exit(3)


def calculate_success_rate(outcomes: list[dict]) -> float | None:
    """
    Calculate success rate from task outcomes.
    Formula: (success_count / total_invocations) * 100
    """
    if not outcomes:
        return None

    total = len(outcomes)
    success_count = sum(1 for o in outcomes if o.get('outcome') == 'success')
    return round((success_count / total) * 100, 2)


def calculate_time_efficiency(outcomes: list[dict], baseline_minutes: int) -> float | None:
    """
    Calculate time efficiency.
    Formula: (baseline_time - actual_time) / baseline_time * 100
    Positive values indicate time saved (faster than baseline).
    """
    if not outcomes or baseline_minutes <= 0:
        return None

    durations = [o.get('duration_minutes', 0) for o in outcomes if o.get('duration_minutes')]
    if not durations:
        return None

    avg_duration = sum(durations) / len(durations)
    efficiency = ((baseline_minutes - avg_duration) / baseline_minutes) * 100
    return round(efficiency, 2)


def calculate_trigger_accuracy(outcomes: list[dict]) -> float | None:
    """
    Calculate trigger accuracy.
    Formula: correct_selections / total_selections * 100
    """
    if not outcomes:
        return None

    # Only count outcomes where trigger_was_correct is explicitly set
    valid_outcomes = [o for o in outcomes if 'trigger_was_correct' in o]
    if not valid_outcomes:
        return None

    correct = sum(1 for o in valid_outcomes if o.get('trigger_was_correct') is True)
    return round((correct / len(valid_outcomes)) * 100, 2)


def calculate_quality_score(outcomes: list[dict]) -> float | None:
    """
    Calculate quality score.
    Formula: sum(quality_ratings) / count(quality_ratings) * 20
    Converts 1-5 scale to 0-100 scale.
    """
    if not outcomes:
        return None

    ratings = [o.get('quality_rating') for o in outcomes if o.get('quality_rating') is not None]
    if not ratings:
        return None

    avg_rating = sum(ratings) / len(ratings)
    return round(avg_rating * 20, 2)


def calculate_reuse_rate(outcomes: list[dict]) -> float | None:
    """
    Calculate reuse rate.
    Formula: reuse_count / total_invocations * 100
    """
    if not outcomes:
        return None

    total = len(outcomes)
    reuse_count = sum(1 for o in outcomes if o.get('would_use_again') is True)
    return round((reuse_count / total) * 100, 2)


def calculate_effectiveness_score(metrics: dict[str, float | None]) -> float | None:
    """
    Calculate weighted composite effectiveness score.
    Weights from metrics_schema:
    - success_rate: 0.35
    - time_efficiency: 0.25
    - trigger_accuracy: 0.20
    - quality_score: 0.15
    - reuse_rate: 0.05
    """
    weights = {
        'success_rate': 0.35,
        'time_efficiency': 0.25,
        'trigger_accuracy': 0.20,
        'quality_score': 0.15,
        'reuse_rate': 0.05,
    }

    total_weight = 0
    weighted_sum = 0

    for metric_name, weight in weights.items():
        value = metrics.get(metric_name)
        if value is not None:
            weighted_sum += value * weight
            total_weight += weight

    if total_weight == 0:
        return None

    # Normalize to account for missing metrics
    return round(weighted_sum / total_weight, 2)


def calculate_time_saved(outcomes: list[dict], baseline_minutes: int) -> int | None:
    """Calculate total time saved in minutes."""
    if not outcomes or baseline_minutes <= 0:
        return None

    total_saved = 0
    for outcome in outcomes:
        actual = outcome.get('duration_minutes')
        if actual is not None and actual < baseline_minutes:
            total_saved += (baseline_minutes - actual)

    return int(total_saved)


def calculate_quality_improvement(outcomes: list[dict]) -> float | None:
    """Calculate average quality improvement (baseline 3.0 = 60%)."""
    if not outcomes:
        return None

    ratings = [o.get('quality_rating') for o in outcomes if o.get('quality_rating') is not None]
    if not ratings:
        return None

    avg_rating = sum(ratings) / len(ratings)
    baseline = 3.0  # Neutral rating
    improvement = ((avg_rating - baseline) / baseline) * 100
    return round(improvement, 2)


def calculate_cost_benefit_ratio(outcomes: list[dict], baseline_minutes: int) -> float | None:
    """
    Calculate cost-benefit ratio.
    Simple model: time saved / time invested in skill development
    Assumes 30 min initial skill setup cost.
    """
    time_saved = calculate_time_saved(outcomes, baseline_minutes)
    if time_saved is None:
        return None

    setup_cost = 30  # minutes
    if time_saved <= 0:
        return 0.0

    return round(time_saved / setup_cost, 2)


def get_outcomes_for_skill(outcomes: list[dict], skill_name: str) -> list[dict]:
    """Filter task outcomes for a specific skill."""
    return [o for o in outcomes if o.get('skill_used') == skill_name]


def determine_confidence_level(effectiveness_score: float | None) -> str:
    """Determine confidence level based on effectiveness score."""
    if effectiveness_score is None:
        return 'low'
    if effectiveness_score >= 80:
        return 'high'
    if effectiveness_score >= 60:
        return 'medium'
    return 'low'


def calculate_category_performance(skills: list[dict], outcomes: list[dict]) -> list[dict]:
    """Calculate performance metrics by category."""
    categories = {}

    for skill in skills:
        cat = skill.get('category', 'unknown')
        if cat not in categories:
            categories[cat] = {'skills': [], 'outcomes': []}
        categories[cat]['skills'].append(skill)

    # Map outcomes to categories based on skill_used
    skill_names = {s['name'] for s in skills}
    for outcome in outcomes:
        skill_used = outcome.get('skill_used')
        if skill_used:
            for cat, data in categories.items():
                if any(s['name'] == skill_used for s in data['skills']):
                    data['outcomes'].append(outcome)
                    break

    results = []
    for cat_name, data in sorted(categories.items()):
        cat_outcomes = data['outcomes']
        results.append({
            'category': cat_name,
            'avg_effectiveness': calculate_effectiveness_score({
                'success_rate': calculate_success_rate(cat_outcomes),
                'time_efficiency': None,
                'trigger_accuracy': calculate_trigger_accuracy(cat_outcomes),
                'quality_score': calculate_quality_score(cat_outcomes),
                'reuse_rate': calculate_reuse_rate(cat_outcomes),
            }),
            'total_tasks': len(cat_outcomes),
            'success_rate': calculate_success_rate(cat_outcomes),
        })

    return results


def calculate_roi_summary(skills: list[dict], outcomes: list[dict]) -> dict:
    """Calculate overall ROI summary."""
    total_time_saved = 0
    all_ratings = []

    for skill in skills:
        skill_outcomes = get_outcomes_for_skill(outcomes, skill['name'])
        baseline = skill.get('baseline_minutes', 30)

        saved = calculate_time_saved(skill_outcomes, baseline)
        if saved:
            total_time_saved += saved

        ratings = [o.get('quality_rating') for o in skill_outcomes if o.get('quality_rating')]
        all_ratings.extend(ratings)

    avg_quality = None
    if all_ratings:
        avg_quality = round((sum(all_ratings) / len(all_ratings)) * 20, 2)

    # Overall cost-benefit: total time saved / total setup costs
    total_setup_cost = len(skills) * 30  # 30 min per skill
    cost_benefit = None
    if total_time_saved > 0 and total_setup_cost > 0:
        cost_benefit = round(total_time_saved / total_setup_cost, 2)

    return {
        'total_time_saved_minutes': total_time_saved,
        'avg_quality_improvement': avg_quality,
        'cost_benefit_ratio': cost_benefit,
    }


def update_skill_metrics(metrics_data: dict, outcomes: list[dict]) -> dict:
    """Update all skill metrics based on task outcomes."""
    skills = metrics_data.get('skills', [])

    for skill in skills:
        skill_name = skill['name']
        skill_outcomes = get_outcomes_for_skill(outcomes, skill_name)
        baseline = skill.get('baseline_minutes', 30)

        # Calculate individual metrics
        metrics = {
            'success_rate': calculate_success_rate(skill_outcomes),
            'time_efficiency': calculate_time_efficiency(skill_outcomes, baseline),
            'trigger_accuracy': calculate_trigger_accuracy(skill_outcomes),
            'quality_score': calculate_quality_score(skill_outcomes),
            'reuse_rate': calculate_reuse_rate(skill_outcomes),
        }

        # Calculate effectiveness score
        effectiveness = calculate_effectiveness_score(metrics)

        # Update skill data
        skill['effectiveness_score'] = effectiveness
        skill['metrics'] = metrics

        # Update ROI calculations
        skill['roi_calculation'] = {
            'time_saved_minutes': calculate_time_saved(skill_outcomes, baseline),
            'quality_improvement': calculate_quality_improvement(skill_outcomes),
            'cost_benefit_ratio': calculate_cost_benefit_ratio(skill_outcomes, baseline),
        }

        # Update recommendation confidence
        skill['recommendations']['confidence'] = determine_confidence_level(effectiveness)

    # Update analysis section
    metrics_data['analysis'] = {
        'last_calculated': datetime.now().isoformat(),
        'top_skills': get_top_skills(skills),
        'underperforming_skills': get_underperforming_skills(skills),
        'category_performance': calculate_category_performance(skills, outcomes),
        'roi_summary': calculate_roi_summary(skills, outcomes),
        'skill_selection_recommendations': generate_recommendations(skills),
        'trigger_insights': generate_trigger_insights(outcomes),
    }

    # Update metadata
    metrics_data['metadata']['last_updated'] = datetime.now().isoformat()
    metrics_data['metadata']['total_tasks_tracked'] = len(outcomes)

    return metrics_data


def get_top_skills(skills: list[dict], limit: int = 5) -> list[dict]:
    """Get top performing skills by effectiveness score."""
    scored = [(s, s.get('effectiveness_score') or 0) for s in skills]
    scored.sort(key=lambda x: x[1], reverse=True)

    return [
        {
            'name': s['name'],
            'effectiveness_score': s['effectiveness_score'],
            'category': s.get('category', 'unknown'),
        }
        for s, _ in scored[:limit] if s['effectiveness_score'] is not None
    ]


def get_underperforming_skills(skills: list[dict], threshold: float = 50) -> list[dict]:
    """Get skills with effectiveness below threshold."""
    underperforming = []
    for skill in skills:
        score = skill.get('effectiveness_score')
        if score is not None and score < threshold:
            underperforming.append({
                'name': skill['name'],
                'effectiveness_score': score,
                'category': skill.get('category', 'unknown'),
            })
    return underperforming


def generate_recommendations(skills: list[dict]) -> list[dict]:
    """Generate skill selection recommendations."""
    recommendations = []

    # Quick fixes recommendation
    quick_flow = next((s for s in skills if s['name'] == 'bmad-quick-flow'), None)
    if quick_flow:
        recommendations.append({
            'scenario': 'Quick fixes (< 30 min)',
            'recommended_skill': 'bmad-quick-flow',
            'confidence': quick_flow['recommendations']['confidence'],
        })

    # Architecture recommendation
    architect = next((s for s in skills if s['name'] == 'bmad-architect'), None)
    if architect:
        recommendations.append({
            'scenario': 'Architecture decisions',
            'recommended_skill': 'bmad-architect',
            'confidence': architect['recommendations']['confidence'],
        })

    # Research recommendation
    analyst = next((s for s in skills if s['name'] == 'bmad-analyst'), None)
    if analyst:
        recommendations.append({
            'scenario': 'Research and analysis',
            'recommended_skill': 'bmad-analyst',
            'confidence': analyst['recommendations']['confidence'],
        })

    # Complex problems recommendation
    superintel = next((s for s in skills if s['name'] == 'superintelligence-protocol'), None)
    if superintel:
        recommendations.append({
            'scenario': 'Complex multi-step problems',
            'recommended_skill': 'superintelligence-protocol',
            'confidence': superintel['recommendations']['confidence'],
        })

    return recommendations


def generate_trigger_insights(outcomes: list[dict]) -> dict:
    """Generate insights about trigger accuracy."""
    false_positives = []
    missed_opportunities = []
    working_keywords = []

    for outcome in outcomes:
        notes = outcome.get('notes', '')
        trigger_correct = outcome.get('trigger_was_correct')

        if trigger_correct is False:
            false_positives.append({
                'task_id': outcome.get('task_id'),
                'reason': notes[:100] if notes else 'Unknown',
            })

        if 'would have added value' in notes.lower():
            missed_opportunities.append({
                'task_id': outcome.get('task_id'),
                'skill': outcome.get('skill_used') or 'unknown',
            })

    return {
        'common_false_positives': false_positives,
        'common_missed_opportunities': missed_opportunities,
        'trigger_keywords_that_work': working_keywords,
    }


def update_skill_usage(usage_data: dict, outcomes: list[dict]) -> dict:
    """Update skill usage statistics based on task outcomes."""
    skills = usage_data.get('skills', [])

    for skill in skills:
        skill_name = skill['name']
        skill_outcomes = get_outcomes_for_skill(outcomes, skill_name)

        if not skill_outcomes:
            continue

        # Update usage counts
        skill['usage_count'] = len(skill_outcomes)
        skill['success_count'] = sum(1 for o in skill_outcomes if o.get('outcome') == 'success')
        skill['failure_count'] = sum(1 for o in skill_outcomes if o.get('outcome') == 'failure')

        # Update timestamps
        timestamps = [o.get('timestamp') for o in skill_outcomes if o.get('timestamp')]
        if timestamps:
            skill['first_used'] = min(timestamps)
            skill['last_used'] = max(timestamps)

        # Calculate average execution time
        durations = [o.get('duration_minutes') for o in skill_outcomes if o.get('duration_minutes')]
        if durations:
            avg_minutes = sum(durations) / len(durations)
            skill['avg_execution_time_ms'] = int(avg_minutes * 60 * 1000)

        # Update trigger accuracy
        valid_outcomes = [o for o in skill_outcomes if 'trigger_was_correct' in o]
        if valid_outcomes:
            correct = sum(1 for o in valid_outcomes if o.get('trigger_was_correct') is True)
            accuracy = (correct / len(valid_outcomes)) * 100
            skill['trigger_accuracy'] = f"{accuracy:.1f}%"

    # Update metadata
    usage_data['metadata']['last_updated'] = datetime.now().isoformat()
    usage_data['metadata']['total_invocations'] = len(outcomes)

    return usage_data


def main():
    parser = argparse.ArgumentParser(description='Calculate skill metrics from task outcomes')
    parser.add_argument('--dry-run', action='store_true', help='Print results without saving')
    parser.add_argument('--project-dir', type=str, default='.',
                       help='Project directory containing operations/ folder')
    args = parser.parse_args()

    project_dir = Path(args.project_dir).resolve()
    operations_dir = project_dir / 'operations'

    # Load data files
    metrics_file = operations_dir / 'skill-metrics.yaml'
    usage_file = operations_dir / 'skill-usage.yaml'

    print(f"Loading metrics from: {metrics_file}")
    metrics_data = load_yaml_file(metrics_file)

    print(f"Loading usage data from: {usage_file}")
    usage_data = load_yaml_file(usage_file)

    # Get task outcomes
    outcomes = metrics_data.get('task_outcomes', [])
    print(f"Found {len(outcomes)} task outcomes")

    if not outcomes:
        print("Warning: No task outcomes found. Metrics will be null.")

    # Calculate and update metrics
    print("\nCalculating skill metrics...")
    updated_metrics = update_skill_metrics(metrics_data, outcomes)

    print("Updating skill usage statistics...")
    updated_usage = update_skill_usage(usage_data, outcomes)

    # Print summary
    print("\n" + "=" * 60)
    print("CALCULATION SUMMARY")
    print("=" * 60)

    for skill in updated_metrics.get('skills', []):
        name = skill['name']
        score = skill['effectiveness_score']
        metrics = skill['metrics']

        print(f"\n{name}:")
        print(f"  Effectiveness Score: {score if score is not None else 'N/A'}")
        print(f"  Success Rate: {metrics.get('success_rate') if metrics.get('success_rate') is not None else 'N/A'}%")
        print(f"  Time Efficiency: {metrics.get('time_efficiency') if metrics.get('time_efficiency') is not None else 'N/A'}%")
        print(f"  Trigger Accuracy: {metrics.get('trigger_accuracy') if metrics.get('trigger_accuracy') is not None else 'N/A'}%")
        print(f"  Quality Score: {metrics.get('quality_score') if metrics.get('quality_score') is not None else 'N/A'}")
        print(f"  Reuse Rate: {metrics.get('reuse_rate') if metrics.get('reuse_rate') is not None else 'N/A'}%")

    # Category performance
    print("\n" + "-" * 60)
    print("CATEGORY PERFORMANCE")
    print("-" * 60)
    for cat in updated_metrics.get('analysis', {}).get('category_performance', []):
        print(f"\n{cat['category']}:")
        print(f"  Avg Effectiveness: {cat['avg_effectiveness'] if cat['avg_effectiveness'] is not None else 'N/A'}")
        print(f"  Total Tasks: {cat['total_tasks']}")
        print(f"  Success Rate: {cat['success_rate'] if cat['success_rate'] is not None else 'N/A'}%")

    # ROI Summary
    roi = updated_metrics.get('analysis', {}).get('roi_summary', {})
    print("\n" + "-" * 60)
    print("ROI SUMMARY")
    print("-" * 60)
    print(f"Total Time Saved: {roi.get('total_time_saved_minutes', 'N/A')} minutes")
    print(f"Avg Quality Improvement: {roi.get('avg_quality_improvement', 'N/A')}")
    print(f"Cost-Benefit Ratio: {roi.get('cost_benefit_ratio', 'N/A')}")

    if args.dry_run:
        print("\n[DRY RUN - No files modified]")
        return 0

    # Save updated files
    print(f"\nSaving updated metrics to: {metrics_file}")
    save_yaml_file(metrics_file, updated_metrics)

    print(f"Saving updated usage to: {usage_file}")
    save_yaml_file(usage_file, updated_usage)

    print("\nSkill metrics calculation complete!")
    return 0


if __name__ == '__main__':
    sys.exit(main())
