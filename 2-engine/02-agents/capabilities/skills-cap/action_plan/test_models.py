#!/usr/bin/env python3
"""
Simple standalone test for Action Plan models
Tests that the data models work correctly
"""

import sys
from pathlib import Path

# Add parent directories to path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))
sys.path.insert(0, str(current_dir.parent.parent))

# Import models directly
from models import (
    PhaseStatus,
    TaskStatus,
    ConstraintType,
    Constraint,
    Assumption,
    TaskContext,
    ActionPhase,
    ActionTask,
    ActionSubtask,
    TaskResult,
    Checkpoint
)


def test_models():
    """Test that all models can be created"""
    print("=" * 80)
    print("Action Plan Models Test")
    print("=" * 80)
    print()

    # Test enums
    print("Testing enums...")
    assert PhaseStatus.PENDING.value == "pending"
    assert TaskStatus.IN_PROGRESS.value == "in_progress"
    assert ConstraintType.HARD.value == "hard"
    print("✓ Enums work")
    print()

    # Test Constraint
    print("Testing Constraint...")
    constraint = Constraint(
        text="Must use encryption",
        type=ConstraintType.HARD,
        source="security_policy"
    )
    assert constraint.text == "Must use encryption"
    assert constraint.type == ConstraintType.HARD
    print(f"✓ Constraint: {constraint.text}")
    print()

    # Test Assumption
    print("Testing Assumption...")
    assumption = Assumption(
        text="JWT is appropriate",
        confidence="high",
        test="Research best practices"
    )
    assert assumption.text == "JWT is appropriate"
    print(f"✓ Assumption: {assumption.text}")
    print()

    # Test TaskContext
    print("Testing TaskContext...")
    context = TaskContext(
        objective="Test objective",
        constraints=[constraint],
        assumptions=[assumption],
        resources=["OWASP"],
        success_criteria=["Done"],
        thinking_process="Test thinking"
    )
    assert context.objective == "Test objective"
    assert len(context.constraints) == 1
    assert len(context.assumptions) == 1
    print(f"✓ TaskContext created with {len(context.resources)} resources")
    print()

    # Test ActionPhase
    print("Testing ActionPhase...")
    phase = ActionPhase(
        id="phase-001",
        name="Test Phase",
        description="A test phase",
        order=1,
        status=PhaseStatus.PENDING,
        dependencies=[],
        exit_criteria=["Done"]
    )
    assert phase.name == "Test Phase"
    assert phase.status == PhaseStatus.PENDING
    print(f"✓ ActionPhase: {phase.name}")
    print()

    # Test ActionTask
    print("Testing ActionTask...")
    task = ActionTask(
        id="task-001",
        phase_id="phase-001",
        title="Test Task",
        description="A test task",
        status=TaskStatus.PENDING,
        context_template=context
    )
    assert task.title == "Test Task"
    assert task.status == TaskStatus.PENDING
    print(f"✓ ActionTask: {task.title}")
    print()

    # Test ActionSubtask
    print("Testing ActionSubtask...")
    subtask = ActionSubtask(
        id="subtask-001",
        parent_task_id="task-001",
        title="Test Subtask",
        description="A test subtask",
        thinking_process="Test thinking process",
        status=TaskStatus.PENDING,
        order=1
    )
    assert subtask.title == "Test Subtask"
    print(f"✓ ActionSubtask: {subtask.title}")
    print()

    # Test TaskResult
    print("Testing TaskResult...")
    result = TaskResult(
        task_id="task-001",
        success=True,
        output="Test output",
        artifacts=["test.md"],
        thinking_steps=["Step 1", "Step 2"]
    )
    assert result.success == True
    print(f"✓ TaskResult: Success={result.success}")
    print()

    # Test Checkpoint
    print("Testing Checkpoint...")
    checkpoint = Checkpoint(
        checkpoint_id="checkpoint-001",
        timestamp="2024-01-01T00:00:00Z",
        plan_state={},
        context={}
    )
    assert checkpoint.checkpoint_id == "checkpoint-001"
    print(f"✓ Checkpoint: {checkpoint.checkpoint_id}")
    print()

    print("=" * 80)
    print("✅ All models work correctly!")
    print("=" * 80)
    return True


if __name__ == "__main__":
    try:
        test_models()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
