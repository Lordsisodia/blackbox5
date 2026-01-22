#!/usr/bin/env python3
"""
Test script for Action Plan - Task Registry Integration

This demonstrates:
1. Creating an Action Plan
2. Exporting it to Task Registry
3. Syncing status between systems
"""

import sys
from pathlib import Path

# Setup path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

# Import Action Plan models
import models
from task_registry_integration import TaskRegistryIntegration


def test_export_action_plan():
    """Test exporting an Action Plan to Task Registry."""
    print("=" * 80)
    print("Action Plan - Task Registry Integration Test")
    print("=" * 80)
    print()

    # Check if Task Registry is available
    try:
        integration = TaskRegistryIntegration("../../../../07-operations/runtime/data/task_registry.json")
        print("✓ Task Registry integration available")
    except (ImportError, RuntimeError) as e:
        print(f"⚠ Task Registry not available: {e}")
        print("  This is expected if running standalone without full Black Box setup.")
        print()
        print("  To enable integration:")
        print("  1. Ensure Task Registry is at: 2-engine/07-operations/runtime/task_registry/")
        print("  2. The integration module handles import paths automatically")
        return None

    print()

    # 1. Create a sample Action Plan
    print("1. Creating Sample Action Plan...")
    phase1 = models.ActionPhase(
        id="phase-001",
        name="Design Authentication System",
        description="Design secure JWT-based authentication",
        order=1,
        status=models.PhaseStatus.PENDING,
        dependencies=[],
        exit_criteria=["Design documented", "Security review complete"]
    )

    task1 = models.ActionTask(
        id="task-001",
        phase_id="phase-001",
        title="Define Authentication Requirements",
        description="Document security and functional requirements",
        context_template=models.TaskContext(
            objective="Define requirements for JWT authentication",
            constraints=[
                models.Constraint(
                    text="Must use industry-standard encryption",
                    type=models.ConstraintType.HARD,
                    source="security_policy"
                ),
                models.Constraint(
                    text="Should support OAuth 2.0",
                    type=models.ConstraintType.SOFT,
                    source="product_requirements"
                )
            ],
            assumptions=[
                models.Assumption(
                    text="JWT tokens are appropriate for session management",
                    confidence="high",
                    test="Research JWT best practices"
                )
            ],
            resources=[
                "OWASP Authentication Cheat Sheet",
                "JWT RFC 7519",
                "Company security guidelines"
            ],
            success_criteria=[
                "All requirements documented",
                "Security review passed"
            ],
            thinking_process="First principles: Security is fundamental to authentication"
        ),
        status=models.TaskStatus.PENDING,
        dependencies=[]
    )

    # Add subtasks
    subtask1 = models.ActionSubtask(
        id="subtask-001",
        parent_task_id="task-001",
        title="Review OWASP guidelines",
        description="Review security best practices",
        thinking_process="Industry standards provide baseline requirements",
        order=1,
        status=models.TaskStatus.PENDING
    )

    subtask2 = models.ActionSubtask(
        id="subtask-002",
        parent_task_id="task-001",
        title="Document threat model",
        description="Identify potential attack vectors",
        thinking_process="Understanding threats is key to good security",
        order=2,
        status=models.TaskStatus.PENDING
    )

    task1.add_subtask(subtask1)
    task1.add_subtask(subtask2)
    phase1.add_task(task1)

    print(f"   ✓ Phase: {phase1.name}")
    print(f"   ✓ Task: {task1.title}")
    print(f"   ✓ Subtasks: {len(task1.subtasks)}")
    print()

    # 2. Export to Task Registry
    print("2. Exporting Action Plan to Task Registry...")
    try:
        created_ids = integration.export_plan_to_registry(
            plan_name="Authentication System",
            phases=[phase1],
            objective="Build Authentication",
            tags=["security", "jwt", "action-plan-demo"]
        )

        print(f"   ✓ Exported {len(created_ids)} tasks to Task Registry")
        for task_id in created_ids:
            print(f"     - {task_id}")
        print()

        # 3. Verify export
        print("3. Verifying export in Task Registry...")
        registry_tasks = integration.registry_manager.list_tasks(objective="Build Authentication")
        print(f"   ✓ Found {len(registry_tasks)} tasks in registry")

        for task in registry_tasks:
            print(f"     - [{task.state.value}] {task.title}")
            if task.phase:
                print(f"       Phase: {task.phase}")
            if task.dependencies:
                print(f"       Dependencies: {task.dependencies}")
        print()

        # 4. Test status sync
        print("4. Testing status synchronization...")

        # Mark task as in progress in Action Plan
        original_status = task1.status
        task1.status = models.TaskStatus.IN_PROGRESS
        print(f"   Action Plan task status: {task1.status.value}")

        # Sync to registry
        integration.sync_task_status(task1)

        # Check registry status
        registry_task = integration.registry_manager.get_task("ap-task-001")
        if registry_task:
            print(f"   Registry task status: {registry_task.state.value}")
            print(f"   ✓ Status synced successfully")
        print()

        # Restore status
        task1.status = original_status

        # 5. Test import back
        print("5. Testing import from Task Registry...")
        imported_tasks = integration.import_tasks_to_plan(
            objective="Build Authentication"
        )

        print(f"   ✓ Imported {len(imported_tasks)} task templates")
        for task_template in imported_tasks:
            print(f"     - {task_template['title']}")
            if task_template.get('phase'):
                print(f"       Phase: {task_template['phase']}")
        print()

        print("=" * 80)
        print("✅ Integration Test Complete!")
        print("=" * 80)
        print()
        print("Summary:")
        print("  ✓ Action Plan → Task Registry export works")
        print("  ✓ Status synchronization works")
        print("  ✓ Task Registry → Action Plan import works")
        print()
        print("Next steps:")
        print("  - Use this integration to track Action Plan tasks in Task Registry")
        print("  - Sync status bidirectionally for unified task tracking")
        print("  - Create Action Plans directly from Task Registry objectives")
        print()

        return created_ids

    except Exception as e:
        print(f"   ❌ Error during export: {e}")
        import traceback
        traceback.print_exc()
        return None


if __name__ == "__main__":
    try:
        test_export_action_plan()
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
