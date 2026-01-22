"""
Tests for Action Plan System
"""

import unittest
import tempfile
import shutil
from pathlib import Path
from datetime import datetime

from action_plan import (
    create_action_plan,
    TaskContext,
    TaskResult,
    Constraint,
    Assumption,
    ConstraintType,
    FirstPrinciplesIntegration,
    WorkspaceManager
)


class TestActionPlan(unittest.TestCase):
    """Test cases for ActionPlan class."""

    def setUp(self):
        """Set up test fixtures."""
        # Create temporary workspace for testing
        self.temp_dir = tempfile.mkdtemp()
        self.workspace_path = Path(self.temp_dir) / "test_workspace"

    def tearDown(self):
        """Clean up test fixtures."""
        if Path(self.temp_dir).exists():
            shutil.rmtree(self.temp_dir)

    def test_create_action_plan(self):
        """Test creating an action plan."""
        plan = create_action_plan(
            name="Test Plan",
            description="A test plan for validation",
            workspace_path=str(self.workspace_path),
            apply_first_principles=True
        )

        self.assertIsNotNone(plan)
        self.assertEqual(plan.name, "Test Plan")
        self.assertEqual(plan.description, "A test plan for validation")
        self.assertTrue(plan.workspace_path == str(self.workspace_path))
        self.assertIsNotNone(plan.overall_fp_analysis)

    def test_add_phase(self):
        """Test adding a phase to the plan."""
        plan = create_action_plan(
            name="Test Plan",
            description="Test",
            workspace_path=str(self.workspace_path),
            apply_first_principles=False
        )

        phase = plan.add_phase(
            name="Phase 1",
            description="First phase",
            exit_criteria=["Task 1 complete", "Task 2 complete"]
        )

        self.assertEqual(len(plan.phases), 1)
        self.assertEqual(phase.name, "Phase 1")
        self.assertEqual(phase.status.value, "pending")
        self.assertEqual(len(phase.exit_criteria), 2)

    def test_create_task(self):
        """Test creating a task in a phase."""
        plan = create_action_plan(
            name="Test Plan",
            description="Test",
            workspace_path=str(self.workspace_path),
            apply_first_principles=False
        )

        phase = plan.add_phase(
            name="Phase 1",
            description="First phase"
        )

        task = plan.create_task(
            phase_id=phase.id,
            title="Task 1",
            description="First task",
            context_template=TaskContext(
                objective="Complete task 1",
                constraints=[],
                assumptions=[],
                resources=["Resource 1"],
                success_criteria=["Task 1 done"]
            )
        )

        self.assertEqual(len(phase.tasks), 1)
        self.assertEqual(task.title, "Task 1")
        self.assertEqual(task.status.value, "pending")

    def test_add_subtask(self):
        """Test adding subtasks to a task."""
        plan = create_action_plan(
            name="Test Plan",
            description="Test",
            workspace_path=str(self.workspace_path),
            apply_first_principles=False
        )

        phase = plan.add_phase(name="Phase 1", description="First phase")
        task = plan.create_task(
            phase_id=phase.id,
            title="Task 1",
            description="First task",
            context_template=TaskContext(
                objective="Complete task 1",
                constraints=[],
                assumptions=[],
                resources=[],
                success_criteria=[]
            )
        )

        subtask1 = plan.add_subtask(
            task_id=task.id,
            title="Subtask 1",
            description="First subtask",
            thinking_process="Thinking about subtask 1",
            order=1
        )

        subtask2 = plan.add_subtask(
            task_id=task.id,
            title="Subtask 2",
            description="Second subtask",
            thinking_process="Thinking about subtask 2",
            order=2
        )

        self.assertEqual(len(task.subtasks), 2)
        self.assertEqual(task.subtasks[0].title, "Subtask 1")
        self.assertEqual(task.subtasks[1].title, "Subtask 2")

    def test_get_next_task(self):
        """Test getting the next task to execute."""
        plan = create_action_plan(
            name="Test Plan",
            description="Test",
            workspace_path=str(self.workspace_path),
            apply_first_principles=False
        )

        phase1 = plan.add_phase(name="Phase 1", description="First phase")
        phase2 = plan.add_phase(
            name="Phase 2",
            description="Second phase",
            dependencies=[phase1.id]
        )

        task1 = plan.create_task(
            phase_id=phase1.id,
            title="Task 1",
            description="First task",
            context_template=TaskContext(
                objective="Complete task 1",
                constraints=[],
                assumptions=[],
                resources=[],
                success_criteria=[]
            )
        )

        # Should return task1 (first task in first phase)
        next_task = plan.get_next_task()
        self.assertIsNotNone(next_task)
        self.assertEqual(next_task.id, task1.id)

    def test_task_completion(self):
        """Test marking a task as complete."""
        plan = create_action_plan(
            name="Test Plan",
            description="Test",
            workspace_path=str(self.workspace_path),
            apply_first_principles=False
        )

        phase = plan.add_phase(name="Phase 1", description="First phase")
        task = plan.create_task(
            phase_id=phase.id,
            title="Task 1",
            description="First task",
            context_template=TaskContext(
                objective="Complete task 1",
                constraints=[],
                assumptions=[],
                resources=[],
                success_criteria=[]
            )
        )

        # Start and complete task
        plan.start_task(task)
        result = TaskResult(
            task_id=task.id,
            success=True,
            output="Task completed successfully",
            thinking_steps=["Step 1", "Step 2"]
        )
        plan.complete_task(task.id, result)

        # Verify task is complete
        self.assertEqual(task.status.value, "completed")
        self.assertIn(task.id, plan.completed_task_ids)

    def test_checkpoint_save_and_load(self):
        """Test saving and loading checkpoints."""
        plan = create_action_plan(
            name="Test Plan",
            description="Test",
            workspace_path=str(self.workspace_path),
            apply_first_principles=False
        )

        phase = plan.add_phase(name="Phase 1", description="First phase")
        task = plan.create_task(
            phase_id=phase.id,
            title="Task 1",
            description="First task",
            context_template=TaskContext(
                objective="Complete task 1",
                constraints=[],
                assumptions=[],
                resources=[],
                success_criteria=[]
            )
        )

        # Start and complete task
        plan.start_task(task)
        result = TaskResult(
            task_id=task.id,
            success=True,
            output="Task completed"
        )
        plan.complete_task(task.id, result)

        # Save checkpoint
        checkpoint_id = plan.create_checkpoint()
        self.assertIsNotNone(checkpoint_id)

        # Create new plan and load checkpoint
        new_plan = create_action_plan(
            name=plan.name,
            description=plan.description,
            workspace_path=plan.workspace_path,
            apply_first_principles=False
        )

        loaded = new_plan.load_checkpoint(checkpoint_id)
        self.assertTrue(loaded)
        self.assertEqual(len(new_plan.completed_task_ids), 1)

    def test_generate_report(self):
        """Test generating a progress report."""
        plan = create_action_plan(
            name="Test Plan",
            description="Test",
            workspace_path=str(self.workspace_path),
            apply_first_principles=True
        )

        phase = plan.add_phase(name="Phase 1", description="First phase")
        task = plan.create_task(
            phase_id=phase.id,
            title="Task 1",
            description="First task",
            context_template=TaskContext(
                objective="Complete task 1",
                constraints=[],
                assumptions=[],
                resources=[],
                success_criteria=[]
            )
        )

        report = plan.generate_report()

        self.assertIn("Test Plan", report)
        self.assertIn("Phase 1", report)
        self.assertIn("Task 1", report)
        self.assertIn("Progress", report)

    def test_get_progress(self):
        """Test getting progress information."""
        plan = create_action_plan(
            name="Test Plan",
            description="Test",
            workspace_path=str(self.workspace_path),
            apply_first_principles=False
        )

        phase = plan.add_phase(name="Phase 1", description="First phase")
        task = plan.create_task(
            phase_id=phase.id,
            title="Task 1",
            description="First task",
            context_template=TaskContext(
                objective="Complete task 1",
                constraints=[],
                assumptions=[],
                resources=[],
                success_criteria=[]
            )
        )

        progress = plan.get_progress()

        self.assertEqual(progress['total_phases'], 1)
        self.assertEqual(progress['total_tasks'], 1)
        self.assertEqual(progress['completed_tasks'], 0)
        self.assertEqual(progress['percent_complete'], 0.0)


class TestFirstPrinciplesIntegration(unittest.TestCase):
    """Test cases for FirstPrinciplesIntegration."""

    def setUp(self):
        """Set up test fixtures."""
        self.fp = FirstPrinciplesIntegration()

    def test_analyze_problem(self):
        """Test analyzing a problem using first principles."""
        problem = "Build a user authentication system"
        analysis = self.fp.analyze_problem(problem)

        self.assertIsNotNone(analysis)
        self.assertIsNotNone(analysis.true_problem)
        self.assertIsInstance(analysis.fundamental_truths, list)
        self.assertIsInstance(analysis.assumptions, list)
        self.assertIsInstance(analysis.essential_requirements, list)

    def test_analyze_phase(self):
        """Test analyzing a phase."""
        analysis = self.fp.analyze_phase(
            phase_name="Implementation",
            phase_description="Implement the authentication system"
        )

        self.assertIsNotNone(analysis)
        self.assertIn("Implementation", analysis.true_problem)

    def test_analyze_task(self):
        """Test analyzing a task."""
        analysis = self.fp.analyze_task(
            task_title="Implement Login",
            task_description="Create login endpoint"
        )

        self.assertIsNotNone(analysis)
        self.assertIn("login", analysis.true_problem.lower())


class TestWorkspaceManager(unittest.TestCase):
    """Test cases for WorkspaceManager."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.manager = WorkspaceManager(base_path=Path(self.temp_dir))

    def tearDown(self):
        """Clean up test fixtures."""
        if Path(self.temp_dir).exists():
            shutil.rmtree(self.temp_dir)

    def test_create_workspace(self):
        """Test creating a workspace."""
        plan_id = "test_plan_001"
        workspace_path = self.manager.create_workspace(plan_id)

        self.assertTrue(Path(workspace_path).exists())
        self.assertTrue((Path(workspace_path) / "checkpoints").exists())
        self.assertTrue((Path(workspace_path) / "tasks").exists())
        self.assertTrue((Path(workspace_path) / "phases").exists())
        self.assertTrue((Path(workspace_path) / "artifacts").exists())
        self.assertTrue((Path(workspace_path) / "logs").exists())

    def test_save_and_load_plan_state(self):
        """Test saving and loading plan state."""
        plan_id = "test_plan_002"
        self.manager.create_workspace(plan_id)

        state = {
            "plan_id": plan_id,
            "name": "Test Plan",
            "phases": []
        }

        self.manager.save_plan_state(plan_id, state)
        loaded_state = self.manager.load_plan_state(plan_id)

        self.assertEqual(loaded_state["plan_id"], plan_id)
        self.assertEqual(loaded_state["name"], "Test Plan")

    def test_save_and_load_task_context(self):
        """Test saving and loading task context."""
        plan_id = "test_plan_003"
        task_id = "task_001"

        self.manager.create_workspace(plan_id)

        context = {
            "objective": "Test objective",
            "constraints": [],
            "resources": []
        }

        self.manager.save_task_context(plan_id, task_id, context)
        loaded_context = self.manager.load_task_context(plan_id, task_id)

        self.assertEqual(loaded_context["objective"], "Test objective")

    def test_checkpoint_operations(self):
        """Test checkpoint operations."""
        plan_id = "test_plan_004"
        self.manager.create_workspace(plan_id)

        checkpoint_data = {
            "checkpoint_id": "checkpoint_001",
            "timestamp": datetime.now().isoformat(),
            "plan_state": {}
        }

        self.manager.save_checkpoint(plan_id, "checkpoint_001", checkpoint_data)
        loaded_checkpoint = self.manager.load_checkpoint(plan_id, "checkpoint_001")

        self.assertEqual(loaded_checkpoint["checkpoint_id"], "checkpoint_001")

        checkpoints = self.manager.list_checkpoints(plan_id)
        self.assertEqual(len(checkpoints), 1)

    def test_cleanup_workspace(self):
        """Test cleaning up a workspace."""
        plan_id = "test_plan_005"
        workspace_path = self.manager.create_workspace(plan_id)

        self.assertTrue(Path(workspace_path).exists())

        self.manager.cleanup_workspace(plan_id)
        self.assertFalse(Path(workspace_path).exists())


if __name__ == '__main__':
    unittest.main()
