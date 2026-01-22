#!/usr/bin/env python3
"""
Standalone test script for Action Plan system
Run this directly to test the Action Plan functionality
"""

import sys
from pathlib import Path

# Add the action_plan directory to the Python path
action_plan_dir = Path(__file__).parent
sys.path.insert(0, str(action_plan_dir))

# Now we can import from the modules
from models import (
    ActionPhase,
    ActionTask,
    ActionSubtask,
    TaskContext,
    TaskResult,
    Constraint,
    Assumption,
    ConstraintType
)
from action_plan import ActionPlan
from workspace_manager import WorkspaceManager


def main():
    """Test the Action Plan system"""
    print("=" * 80)
    print("Action Plan System Test")
    print("=" * 80)
    print()

    # Create an action plan
    print("Creating Action Plan...")
    plan = ActionPlan(
        name="Build User Authentication",
        description="Implement JWT-based authentication",
        apply_first_principles=True
    )
    print(f"✓ Created plan: {plan.name}")
    print(f"  Plan ID: {plan.id}")
    print(f"  Workspace: {plan.workspace_path}")
    print()

    # Add Phase 1
    print("Adding Phase 1: Requirements Analysis...")
    phase1 = plan.add_phase(
        name="Requirements Analysis",
        description="Analyze requirements",
        exit_criteria=["Requirements documented"]
    )
    print(f"✓ Created phase: {phase1.name} (ID: {phase1.id})")
    print()

    # Add Task to Phase 1
    print("Adding Task: Identify Security Requirements...")
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
    print(f"✓ Created task: {task1.title} (ID: {task1.id})")
    print(f"  Context template created with:")
    print(f"    - {len(task1.context_template.constraints)} constraint(s)")
    print(f"    - {len(task1.context_template.assumptions)} assumption(s)")
    print(f"    - {len(task1.context_template.resources)} resource(s)")
    print()

    # Add subtasks
    print("Adding subtasks...")
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
    print(f"✓ Added 2 subtasks to {task1.title}")
    print()

    # Start the task
    print("Starting task...")
    plan.start_task(task1.id)
    print(f"✓ Task {task1.id} is now {task1.status.value}")
    print()

    # Show next task
    next_task = plan.get_next_task()
    print(f"Next task to execute: {next_task.title if next_task else 'None'}")
    print()

    # Complete the task
    print("Completing task...")
    result = TaskResult(
        task_id=task1.id,
        success=True,
        output="Security requirements documented",
        artifacts=["requirements.md"],
        thinking_steps=["Reviewed OWASP", "Created threat model"]
    )
    plan.complete_task(task1.id, result)
    print(f"✓ Task {task1.id} completed")
    print()

    # Show progress
    progress = plan.get_progress()
    print("Progress:")
    print(f"  Tasks completed: {progress['tasks_completed']}/{progress['total_tasks']}")
    print(f"  Percent complete: {progress['percent_complete']:.1f}%")
    print()

    # Generate report
    print("Generating report...")
    report = plan.generate_report()
    print(report)
    print()

    # Save checkpoint
    print("Saving checkpoint...")
    checkpoint_id = plan.create_checkpoint()
    print(f"✓ Checkpoint saved: {checkpoint_id}")
    print()

    # Show workspace structure
    print("Workspace structure:")
    workspace = WorkspaceManager(plan.workspace_path)
    structure = workspace.get_workspace_structure()
    for item in structure:
        print(f"  {item}")
    print()

    print("=" * 80)
    print("Action Plan System Test Complete!")
    print("=" * 80)


if __name__ == "__main__":
    main()
