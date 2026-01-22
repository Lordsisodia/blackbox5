#!/usr/bin/env python3
"""
Standalone test for Action Plan system
"""

import sys
from pathlib import Path

# Find the 2-engine directory and add to path
current_dir = Path(__file__).parent
engine_dir = current_dir
while engine_dir.name != "2-engine" and engine_dir.parent != engine_dir:
    engine_dir = engine_dir.parent

sys.path.insert(0, str(engine_dir))

# Now import from the action_plan module
from capabilities.skills_cap.action_plan import (
    ActionPlan,
    TaskContext,
    Constraint,
    Assumption,
    ConstraintType,
    TaskResult
)

def test_action_plan():
    """Test the Action Plan system"""
    print("=" * 80)
    print("Action Plan System Test")
    print("=" * 80)
    print()

    # Create an action plan
    print("1. Creating Action Plan...")
    plan = ActionPlan(
        name="Build User Authentication",
        description="Implement JWT-based authentication",
        apply_first_principles=True
    )
    print(f"   ✓ Plan: {plan.name}")
    print(f"   ✓ ID: {plan.id}")
    print(f"   ✓ Workspace: {plan.workspace_path}")
    print()

    # Add Phase 1
    print("2. Adding Phase 1: Requirements Analysis...")
    phase1 = plan.add_phase(
        name="Requirements Analysis",
        description="Analyze requirements",
        exit_criteria=["Requirements documented"]
    )
    print(f"   ✓ Phase: {phase1.name}")
    print()

    # Add Task
    print("3. Creating Task: Identify Security Requirements...")
    task1 = plan.create_task(
        phase_id=phase1.id,
        title="Identify Security Requirements",
        description="Document security requirements",
        context_template=TaskContext(
            objective="Document security requirements",
            constraints=[
                Constraint(
                    text="Must use industry-standard encryption",
                    type=ConstraintType.HARD,
                    source="security_policy"
                )
            ],
            assumptions=[
                Assumption(
                    text="JWT tokens are appropriate",
                    confidence="high",
                    test="Research JWT best practices"
                )
            ],
            resources=["OWASP guidelines"],
            success_criteria=["Requirements documented"],
            thinking_process="First principles: Security is fundamental"
        )
    )
    print(f"   ✓ Task: {task1.title}")
    print(f"   ✓ Constraints: {len(task1.context_template.constraints)}")
    print(f"   ✓ Assumptions: {len(task1.context_template.assumptions)}")
    print()

    # Add subtasks
    print("4. Adding subtasks...")
    plan.add_subtask(
        task_id=task1.id,
        title="Review OWASP guidelines",
        description="Review security guidelines",
        order=1
    )
    plan.add_subtask(
        task_id=task1.id,
        title="Document threat model",
        description="Create threat model",
        order=2
    )
    print(f"   ✓ Added 2 subtasks")
    print()

    # Execute task
    print("5. Executing task...")
    plan.start_task(task1.id)
    result = TaskResult(
        task_id=task1.id,
        success=True,
        output="Security requirements documented in requirements.md",
        artifacts=["requirements.md"],
        thinking_steps=["Reviewed OWASP guidelines", "Created threat model"]
    )
    plan.complete_task(task1.id, result)
    print(f"   ✓ Task completed")
    print()

    # Show progress
    progress = plan.get_progress()
    print("6. Progress Report:")
    print(f"   Tasks: {progress['tasks_completed']}/{progress['total_tasks']}")
    print(f"   Complete: {progress['percent_complete']:.1f}%")
    print()

    # Generate report
    print("7. Plan Report:")
    print("-" * 80)
    print(plan.generate_report())
    print("-" * 80)
    print()

    print("=" * 80)
    print("✅ Action Plan System Test Complete!")
    print("=" * 80)
    print()
    print(f"Workspace: {plan.workspace_path}")
    print()

    return plan


if __name__ == "__main__":
    test_action_plan()
