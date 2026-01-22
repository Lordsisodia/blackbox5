#!/usr/bin/env python3
"""
Demo script for Action Plan Templates

Shows how to use pre-built templates for common workflows.
"""

import sys
from pathlib import Path

# Setup path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

# Import templates and models
from templates.plan_templates import (
    feature_development_template,
    bug_investigation_template,
    security_review_template,
    performance_optimization_template,
    list_templates,
    get_template
)
import models


def demo_feature_template():
    """Demonstrate the feature development template."""
    print("=" * 80)
    print("Template 1: Feature Development")
    print("=" * 80)
    print()

    template = feature_development_template(
        feature_name="User Authentication System",
        description="Implement JWT-based authentication with OAuth 2.0 support"
    )

    print(f"Plan: {template['plan_name']}")
    print(f"Description: {template['description']}")
    print()

    print(f"Phases: {len(template['phases'])}")
    for i, phase in enumerate(template['phases'], 1):
        print(f"\n{i}. {phase['name']} (Order: {phase['order']})")
        print(f"   Exit Criteria: {', '.join(phase['exit_criteria'])}")
        print(f"   Tasks: {len(phase['tasks'])}")
        for task in phase['tasks']:
            print(f"     - {task['title']}")
            if 'dependencies' in task and task['dependencies']:
                print(f"       Dependencies: {task['dependencies']}")
    print()


def demo_bug_template():
    """Demonstrate the bug investigation template."""
    print("=" * 80)
    print("Template 2: Bug Investigation")
    print("=" * 80)
    print()

    template = bug_investigation_template(
        bug_description="Users cannot log in when using Safari browser",
        severity="high"
    )

    print(f"Plan: {template['plan_name']}")
    print(f"Description: {template['description']}")
    print()

    print(f"Phases: {len(template['phases'])}")
    for i, phase in enumerate(template['phases'], 1):
        print(f"\n{i}. {phase['name']}")
        print(f"   Tasks: {len(phase['tasks'])}")
        for task in phase['tasks']:
            print(f"     - {task['title']}")
    print()


def demo_security_template():
    """Demonstrate the security review template."""
    print("=" * 80)
    print("Template 3: Security Review")
    print("=" * 80)
    print()

    template = security_review_template(
        scope="Payment Processing System"
    )

    print(f"Plan: {template['plan_name']}")
    print()

    print(f"Phases: {len(template['phases'])}")
    for i, phase in enumerate(template['phases'], 1):
        print(f"\n{i}. {phase['name']}")
        print(f"   Tasks: {len(phase['tasks'])}")
        for task in phase['tasks']:
            print(f"     - {task['title']}")
    print()


def demo_performance_template():
    """Demonstrate the performance optimization template."""
    print("=" * 80)
    print("Template 4: Performance Optimization")
    print("=" * 80)
    print()

    template = performance_optimization_template(
        target="API Response Time",
        goal="Reduce average response time from 500ms to <100ms"
    )

    print(f"Plan: {template['plan_name']}")
    print(f"Description: {template['description']}")
    print()

    # Show the first task's thinking process as an example
    if template['phases'] and template['phases'][0]['tasks']:
        first_task = template['phases'][0]['tasks'][0]
        print("Sample Thinking Process from first task:")
        print("-" * 80)
        print(first_task['context_template'].thinking_process)
        print("-" * 80)
        print()

    print(f"Phases: {len(template['phases'])}")
    for i, phase in enumerate(template['phases'], 1):
        print(f"\n{i}. {phase['name']}")
        print(f"   Tasks: {len(phase['tasks'])}")
        for task in phase['tasks']:
            print(f"     - {task['title']}")
    print()


def demo_template_usage():
    """Demonstrate how to use templates with ActionPlan."""
    print("=" * 80)
    print("Using Templates with Action Plan")
    print("=" * 80)
    print()

    # Get a template
    template_data = get_template(
        "bug_investigation",
        bug_description="Memory leak in background worker",
        severity="critical"
    )

    if template_data:
        print("Retrieved template: " + template_data['plan_name'])
        print()

        # Show how to use it
        print("Usage Example:")
        print("-" * 80)
        print("""
# 1. Get the template
from templates.plan_templates import get_template

template_data = get_template(
    "feature_development",
    feature_name="My Feature",
    description="Description of my feature"
)

# 2. Create Action Plan from template
from action_plan import ActionPlan
from models import ActionPhase, ActionTask, TaskContext

plan = ActionPlan(
    name=template_data['plan_name'],
    description=template_data['description']
)

# 3. Add phases and tasks from template
for phase_data in template_data['phases']:
    phase = plan.add_phase(
        name=phase_data['name'],
        description=phase_data['description'],
        order=phase_data['order'],
        exit_criteria=phase_data.get('exit_criteria', [])
    )

    for task_data in phase_data['tasks']:
        task = plan.create_task(
            phase_id=phase.id,
            title=task_data['title'],
            description=task_data['description'],
            context_template=task_data['context_template'],
            dependencies=task_data.get('dependencies', [])
        )

# 4. Execute the plan
print(f"Created plan with {len(plan.phases)} phases")
for phase in plan.phases:
    print(f"  Phase: {phase.name} - {len(phase.tasks)} tasks")
        """)
        print("-" * 80)
        print()


def demo_all_templates():
    """List all available templates."""
    print("=" * 80)
    print("Available Templates")
    print("=" * 80)
    print()

    templates = list_templates()
    print(f"Total templates: {len(templates)}")
    print()

    for i, template_name in enumerate(templates, 1):
        print(f"{i}. {template_name}")

    print()
    print("Usage:")
    print("  template_data = get_template('feature_development', feature_name='...', description='...')")
    print()


def main():
    """Run all template demos."""
    print()
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 15 + "ACTION PLAN TEMPLATES DEMO" + " " * 37 + "║")
    print("╚" + "═" * 78 + "╝")
    print()

    # List all templates
    demo_all_templates()

    # Demo each template
    demo_feature_template()
    demo_bug_template()
    demo_security_template()
    demo_performance_template()

    # Show usage example
    demo_template_usage()

    print("=" * 80)
    print("✅ Templates Demo Complete!")
    print("=" * 80)
    print()
    print("Summary:")
    print("  ✓ Feature Development Template - 6 phases, 12+ tasks")
    print("  ✓ Bug Investigation Template - 5 phases, focused on root cause")
    print("  ✓ Security Review Template - 5 phases, comprehensive approach")
    print("  ✓ Performance Optimization Template - 4 phases, data-driven")
    print()
    print("Key Features:")
    print("  • First principles thinking embedded in each task")
    print("  • Clear dependencies between phases and tasks")
    print("  • Context templates with constraints and assumptions")
    print("  • Success criteria for every task")
    print("  • Exit criteria for every phase")
    print()
    print("Next Steps:")
    print("  1. Use templates as starting points for your Action Plans")
    print("  2. Customize templates for your specific needs")
    print("  3. Create your own templates based on common workflows")
    print("  4. Export template-based plans to Task Registry for tracking")
    print()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
