#!/usr/bin/env python3
"""
Demo of ModelRouter Cost Tracking and Quality Measurement

This script demonstrates the complete workflow:
1. Route tasks to appropriate models
2. Execute tasks (simulated)
3. Record actual costs and quality
4. Analyze routing effectiveness
5. Get actionable insights
"""

import sys
from pathlib import Path
import random
import json

sys.path.insert(0, str(Path(__file__).parent.parent))

from model_router import ModelRouter


def simulate_task_execution(model_config, task):
    """Simulate task execution and return result"""
    # Simulate different outcomes
    success_rate = 0.9 if model_config.model == 'glm-4-plus' else 0.8

    if random.random() < success_rate:
        desc = task.get('description', '')
        return {
            'success': True,
            'error': None,
            'output': f'Successfully processed task: {desc}\nThis is a substantial output with meaningful content.'
        }
    else:
        return {
            'success': False,
            'error': 'Task failed due to complexity',
            'output': 'Error: unable to complete the task'
        }


def main():
    """Demonstrate cost tracking workflow"""

    print("=" * 70)
    print("ModelRouter Cost Tracking & Quality Measurement Demo")
    print("=" * 70)
    print()

    # Initialize router
    router = ModelRouter()

    # Define test tasks
    tasks = [
        {'id': 't1', 'type': 'validation', 'description': 'Validate Python code syntax'},
        {'id': 't2', 'type': 'planning', 'description': 'Plan system architecture for microservices'},
        {'id': 't3', 'type': 'implementation', 'description': 'Implement REST API endpoint'},
        {'id': 't4', 'type': 'validation', 'description': 'Review test coverage'},
        {'id': 't5', 'type': 'simple', 'description': 'List all files in directory'},
        {'id': 't6', 'type': 'architecture', 'description': 'Design database schema'},
        {'id': 't7', 'type': 'validation', 'description': 'Check security vulnerabilities'},
        {'id': 't8', 'type': 'implementation', 'description': 'Add authentication middleware'},
        {'id': 't9', 'type': 'planning', 'description': 'Break down feature into tasks'},
        {'id': 't10', 'type': 'simple', 'description': 'Get file metadata'},
    ]

    print("Step 1: Routing tasks to models")
    print("-" * 70)

    for task in tasks:
        model_config = router.route(task, {})
        print(f"  {task['id']}: {task['type']:15} -> {model_config.model:15} ({router.models[model_config.model]['tier']:8})")

    print()
    print("Step 2: Executing tasks and recording results")
    print("-" * 70)

    for task in tasks:
        # Route task
        model_config = router.route(task, {})

        # Simulate execution
        result = simulate_task_execution(model_config, task)

        # Measure quality
        quality = router.measure_quality(result, task)

        # Record results (simulated token counts)
        router.record_result(
            task_id=task['id'],
            model_config=model_config,
            input_tokens=random.randint(100, 500),
            output_tokens=random.randint(50, 300),
            success=result['success'],
            quality_score=quality
        )

        status = "SUCCESS" if result['success'] else "FAILED"
        print(f"  {task['id']}: {status:8} | Quality: {quality:.2f} | Cost: ${router._cost_history[-1]['actual_cost']:.6f}")

    print()
    print("Step 3: Cost Statistics by Tier")
    print("-" * 70)

    stats = router.get_cost_statistics()

    print(f"  Total Tasks: {stats['total_tasks']}")
    print(f"  Total Cost: ${stats['total_cost']:.6f}")
    print(f"  Total Tokens: {stats['total_tokens']}")
    print(f"  Cost Accuracy: {stats['cost_accuracy']:.1%}")
    print()
    print("  By Model Tier:")

    for tier, tier_stats in stats['by_tier'].items():
        print(f"    {tier:10} | Count: {tier_stats['count']:2} | "
              f"Avg Cost: ${tier_stats['avg_cost']:.6f} | "
              f"Avg Quality: {tier_stats['avg_quality']:.2f}")

    print()
    print("Step 4: Routing Effectiveness Analysis")
    print("-" * 70)

    analysis = router.analyze_routing_effectiveness()

    print("  Insights:")
    for insight in analysis['insights']:
        icon = "⚠️" if insight['severity'] == 'warning' else "ℹ️"
        print(f"    {icon} {insight['message']}")

    if analysis['recommendations']:
        print()
        print("  Recommendations:")
        for i, rec in enumerate(analysis['recommendations'], 1):
            print(f"    {i}. {rec}")

    print()
    print("Step 5: Cost Comparison Scenarios")
    print("-" * 70)

    # Calculate what if all tasks used HQ model
    hq_cost_per_1k = router.models['glm-4-plus']['cost_per_1k_tokens']
    total_tokens = stats['total_tokens']
    all_hq_cost = (total_tokens / 1000) * hq_cost_per_1k

    savings = all_hq_cost - stats['total_cost']
    savings_pct = (savings / all_hq_cost * 100) if all_hq_cost > 0 else 0

    print(f"  If all tasks used HQ model: ${all_hq_cost:.6f}")
    print(f"  Actual cost with routing:  ${stats['total_cost']:.6f}")
    print(f"  Savings:                   ${savings:.6f} ({savings_pct:.1f}%)")

    print()
    print("=" * 70)
    print("Demo completed successfully!")
    print("=" * 70)


if __name__ == '__main__':
    main()
