#!/usr/bin/env python3
"""Collect skill metrics from task outcomes and update skill-metrics.yaml."""

import os
import yaml
from datetime import datetime
from pathlib import Path
from collections import defaultdict

# Get project directory from environment or use default
PROJECT_DIR = Path(os.environ.get('RALF_PROJECT_DIR', Path.home() / '.blackbox5/5-project-memory/blackbox5'))
METRICS_PATH = PROJECT_DIR / 'operations' / 'skill-metrics.yaml'


def load_skill_metrics():
    """Load current skill-metrics.yaml."""
    with open(METRICS_PATH, 'r') as f:
        return yaml.safe_load(f)

def save_skill_metrics(data):
    """Save updated skill-metrics.yaml."""
    with open(METRICS_PATH, 'w') as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False)

def calculate_skill_metrics(task_outcomes, skills_data):
    """Calculate metrics for each skill based on task outcomes."""
    # Group outcomes by skill
    skill_tasks = defaultdict(list)

    for outcome in task_outcomes:
        skill_used = outcome.get('skill_used')
        if skill_used:
            skill_tasks[skill_used].append(outcome)

    # Calculate metrics for each skill
    for skill in skills_data['skills']:
        skill_name = skill['name']
        tasks = skill_tasks.get(skill_name, [])

        if not tasks:
            continue

        # Success rate
        successes = sum(1 for t in tasks if t.get('outcome') == 'success')
        success_rate = (successes / len(tasks)) * 100

        # Time efficiency (compare to baseline)
        baseline = skill.get('baseline_minutes', 30)
        actual_times = [t.get('duration_minutes', baseline) for t in tasks if t.get('duration_minutes')]
        if actual_times:
            avg_time = sum(actual_times) / len(actual_times)
            time_efficiency = ((baseline - avg_time) / baseline) * 100
        else:
            time_efficiency = 0

        # Trigger accuracy
        correct_triggers = sum(1 for t in tasks if t.get('trigger_was_correct', False))
        trigger_accuracy = (correct_triggers / len(tasks)) * 100

        # Quality score
        quality_ratings = [t.get('quality_rating', 3) for t in tasks if t.get('quality_rating')]
        if quality_ratings:
            avg_quality = sum(quality_ratings) / len(quality_ratings)
            quality_score = (avg_quality / 5) * 100
        else:
            quality_score = 60  # Default

        # Reuse rate
        would_reuse = sum(1 for t in tasks if t.get('would_use_again', False))
        reuse_rate = (would_reuse / len(tasks)) * 100

        # Calculate weighted effectiveness score
        effectiveness = (
            success_rate * 0.35 +
            time_efficiency * 0.25 +
            trigger_accuracy * 0.20 +
            quality_score * 0.15 +
            reuse_rate * 0.05
        )

        # Update skill data
        skill['effectiveness_score'] = round(effectiveness, 1)
        skill['metrics'] = {
            'success_rate': round(success_rate, 1),
            'time_efficiency': round(time_efficiency, 1),
            'trigger_accuracy': round(trigger_accuracy, 1),
            'quality_score': round(quality_score, 1),
            'reuse_rate': round(reuse_rate, 1)
        }

        # Update ROI calculation
        if actual_times:
            time_saved = (baseline - avg_time) * len(tasks)
            skill['roi_calculation']['time_saved_minutes'] = round(time_saved, 1)
            skill['roi_calculation']['quality_improvement'] = round(quality_score - 60, 1)  # vs baseline
            skill['roi_calculation']['cost_benefit_ratio'] = round(effectiveness / 100, 2)

        # Update confidence based on data
        if len(tasks) >= 5:
            skill['recommendations']['confidence'] = 'high'
        elif len(tasks) >= 2:
            skill['recommendations']['confidence'] = 'medium'
        else:
            skill['recommendations']['confidence'] = 'low'

    return skills_data

def calculate_category_performance(skills_data):
    """Calculate aggregated performance by category."""
    category_stats = defaultdict(lambda: {'scores': [], 'tasks': 0, 'successes': 0})

    for skill in skills_data['skills']:
        cat = skill['category']
        if skill.get('effectiveness_score'):
            category_stats[cat]['scores'].append(skill['effectiveness_score'])
            # Count tasks (approximate from metrics)
            if skill.get('metrics', {}).get('success_rate'):
                # Estimate task count from data
                category_stats[cat]['tasks'] += 1

    # Update category performance
    for cat_data in skills_data['analysis']['category_performance']:
        cat = cat_data['category']
        if cat in category_stats:
            scores = category_stats[cat]['scores']
            if scores:
                cat_data['avg_effectiveness'] = round(sum(scores) / len(scores), 1)
                cat_data['total_tasks'] = category_stats[cat]['tasks']

    return skills_data

def generate_recommendations(skills_data):
    """Generate skill selection recommendations based on data."""
    # Sort skills by effectiveness
    ranked_skills = sorted(
        [s for s in skills_data['skills'] if s.get('effectiveness_score')],
        key=lambda x: x['effectiveness_score'],
        reverse=True
    )

    # Top skills
    skills_data['analysis']['top_skills'] = [
        {'name': s['name'], 'score': s['effectiveness_score']}
        for s in ranked_skills[:5]
    ]

    # Underperforming skills
    skills_data['analysis']['underperforming_skills'] = [
        {'name': s['name'], 'score': s['effectiveness_score']}
        for s in ranked_skills if s['effectiveness_score'] < 50
    ]

    # Calculate total ROI
    total_time_saved = sum(
        s['roi_calculation'].get('time_saved_minutes', 0) or 0
        for s in skills_data['skills']
    )
    skills_data['analysis']['roi_summary']['total_time_saved_minutes'] = round(total_time_saved, 1)

    # Update timestamp
    skills_data['analysis']['last_calculated'] = datetime.now().isoformat()
    skills_data['metadata']['last_updated'] = datetime.now().isoformat()

    return skills_data

def main():
    print("=" * 60)
    print("Skill Metrics Collection")
    print("=" * 60)

    # Load data
    print("\n[INFO] Loading skill-metrics.yaml...")
    data = load_skill_metrics()

    # Get task outcomes
    task_outcomes = data.get('task_outcomes', [])
    print(f"[INFO] Found {len(task_outcomes)} task outcomes")

    # Calculate metrics
    print("\n[INFO] Calculating skill metrics...")
    data = calculate_skill_metrics(task_outcomes, data)

    # Calculate category performance
    print("[INFO] Calculating category performance...")
    data = calculate_category_performance(data)

    # Generate recommendations
    print("[INFO] Generating recommendations...")
    data = generate_recommendations(data)

    # Count skills with data
    skills_with_data = sum(1 for s in data['skills'] if s.get('effectiveness_score'))
    print(f"\n[INFO] Updated metrics for {skills_with_data} skills")

    # Save
    print("[INFO] Saving skill-metrics.yaml...")
    save_skill_metrics(data)

    print("\n✅ Skill metrics collection complete!")
    print("=" * 60)

    # Print summary
    print("\n📊 Top Skills:")
    for skill in data['analysis']['top_skills'][:3]:
        print(f"  - {skill['name']}: {skill['score']:.1f}")

    if data['analysis']['underperforming_skills']:
        print("\n⚠️  Underperforming:")
        for skill in data['analysis']['underperforming_skills'][:3]:
            print(f"  - {skill['name']}: {skill['score']:.1f}")

if __name__ == '__main__':
    main()
