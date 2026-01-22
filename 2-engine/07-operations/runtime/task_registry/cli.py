"""Task Registry System CLI."""

import click
from pathlib import Path
from typing import Optional

from .registry import TaskRegistryManager
from .state_machine import TaskStateMachine, StateTransitionError
from .workspace import WorkspaceFactory
from .models import TaskState


# Global instances
def get_registry_manager() -> TaskRegistryManager:
    """Get or create the registry manager."""
    return TaskRegistryManager()


def get_state_machine() -> TaskStateMachine:
    """Get or create the state machine."""
    registry = get_registry_manager()
    return TaskStateMachine(registry)


def get_workspace_factory() -> WorkspaceFactory:
    """Get or create the workspace factory."""
    return WorkspaceFactory()


@click.group()
@click.version_option(version="1.0")
def task():
    """Task Registry CLI - Manage hierarchical task execution."""
    pass


@task.command()
@click.option("--state", type=click.Choice([s.value for s in TaskState]), help="Filter by state")
@click.option("--objective", help="Filter by objective")
@click.option("--assignee", help="Filter by assignee")
def list(state, objective, assignee):
    """List all tasks."""
    registry = get_registry_manager()
    
    state_filter = TaskState(state) if state else None
    tasks = registry.list_tasks(
        state=state_filter,
        objective=objective,
        assignee=assignee,
    )
    
    if not tasks:
        click.echo("No tasks found.")
        return
    
    click.echo(f"Found {len(tasks)} task(s):\n")
    
    for t in tasks:
        click.echo(f"📋 {t.id}: {t.title}")
        click.echo(f"   State: {t.state.value}")
        click.echo(f"   Objective: {t.objective}")
        if t.phase:
            click.echo(f"   Phase: {t.phase}")
        if t.assignee:
            click.echo(f"   Assignee: {t.assignee}")
        if t.dependencies:
            click.echo(f"   Dependencies: {', '.join(t.dependencies)}")
        click.echo()


@task.command()
def available():
    """Show tasks that are ready to be assigned."""
    registry = get_registry_manager()
    tasks = registry.get_available_tasks()
    
    if not tasks:
        click.echo("No tasks available for assignment.")
        return
    
    click.echo(f"Found {len(tasks)} available task(s):\n")
    
    for t in tasks:
        click.echo(f"✅ {t.id}: {t.title}")
        click.echo(f"   Priority: {t.priority.value}")
        if t.dependencies:
            click.echo(f"   Dependencies: {', '.join(t.dependencies)} (all complete)")
        click.echo()


@task.command()
@click.argument("task_id")
def status(task_id):
    """Show detailed status of a task."""
    registry = get_registry_manager()
    task = registry.get_task(task_id)
    
    if not task:
        click.echo(f"Task {task_id} not found.")
        return
    
    click.echo(f"📋 {task.id}: {task.title}")
    click.echo(f"   Description: {task.description}")
    click.echo(f"   State: {task.state.value}")
    click.echo(f"   Objective: {task.objective}")
    if task.phase:
        click.echo(f"   Phase: {task.phase}")
    click.echo(f"   Priority: {task.priority.value}")
    
    if task.assignee:
        click.echo(f"   Assignee: {task.assignee}")
    if task.assigned_at:
        click.echo(f"   Assigned: {task.assigned_at}")
    if task.started_at:
        click.echo(f"   Started: {task.started_at}")
    if task.completed_at:
        click.echo(f"   Completed: {task.completed_at}")
    
    if task.dependencies:
        click.echo(f"   Dependencies: {', '.join(task.dependencies)}")
    if task.blocks:
        click.echo(f"   Blocks: {', '.join(task.blocks)}")
    
    if task.workspace:
        click.echo(f"   Workspace: {task.workspace}")
    if task.github_issue:
        click.echo(f"   GitHub Issue: #{task.github_issue}")
    
    if task.tags:
        click.echo(f"   Tags: {', '.join(task.tags)}")


@task.command()
@click.argument("task_id")
@click.option("--agent", default="claude-agent", help="Agent name")
def take(task_id, agent):
    """Assign a task to yourself."""
    state_machine = get_state_machine()
    
    try:
        task = state_machine.transition(task_id, TaskState.ASSIGNED, assignee=agent)
        
        # Create workspace if it doesn't exist
        workspace_factory = get_workspace_factory()
        if not workspace_factory.workspace_exists(task_id):
            workspace_path = workspace_factory.create_workspace(task_id, task.title)
            
            # Update task with workspace path
            registry = get_registry_manager()
            registry.update_task(task_id, workspace=str(workspace_path))
            
            # Add timeline entry
            workspace_factory.add_timeline_entry(
                task_id,
                "assigned",
                {"agent": agent, "workspace": str(workspace_path)}
            )
        
        click.echo(f"✅ Assigned {task_id} to {agent}")
        
    except StateTransitionError as e:
        click.echo(f"❌ {e}")
    except ValueError as e:
        click.echo(f"❌ {e}")


@task.command()
@click.argument("task_id")
def start(task_id):
    """Mark a task as started (ACTIVE)."""
    state_machine = get_state_machine()
    
    try:
        task = state_machine.transition(task_id, TaskState.ACTIVE)
        
        # Add timeline entry
        workspace_factory = get_workspace_factory()
        workspace_factory.add_timeline_entry(
            task_id,
            "started",
            {"assignee": task.assignee}
        )
        
        click.echo(f"🚀 Started {task_id}")
        
    except StateTransitionError as e:
        click.echo(f"❌ {e}")


@task.command()
@click.argument("task_id")
@click.option("--result", help="Path to result file")
def complete(task_id, result):
    """Mark a task as complete."""
    state_machine = get_state_machine()
    registry = get_registry_manager()
    
    try:
        task = state_machine.transition(task_id, TaskState.DONE)
        
        # Add timeline entry
        workspace_factory = get_workspace_factory()
        workspace_factory.add_timeline_entry(
            task_id,
            "completed",
            {"assignee": task.assignee}
        )
        
        # Update result.json if provided
        if result:
            import json
            with open(result) as f:
                result_data = json.load(f)
            workspace_factory.update_result(task_id, result_data)
        
        click.echo(f"✅ Completed {task_id}")
        
        # TODO: Sync with GitHub (close issue)
        
    except StateTransitionError as e:
        click.echo(f"❌ {e}")


@task.command()
@click.argument("task_id")
@click.argument("reason")
def fail(task_id, reason):
    """Mark a task as failed."""
    state_machine = get_state_machine()
    
    try:
        state_machine.transition(task_id, TaskState.FAILED, failure_reason=reason)
        
        # Add timeline entry
        workspace_factory = get_workspace_factory()
        workspace_factory.add_timeline_entry(
            task_id,
            "failed",
            {"reason": reason}
        )
        
        click.echo(f"❌ Failed {task_id}: {reason}")
        
    except StateTransitionError as e:
        click.echo(f"❌ {e}")


@task.command()
@click.argument("task_id")
def what_is_blocking(task_id):
    """Show what's blocking a task."""
    state_machine = get_state_machine()
    blocking = state_machine.get_blocking_tasks(task_id)
    
    if not blocking:
        click.echo(f"✅ {task_id} is not blocked by anything.")
        return
    
    click.echo(f"🚧 {task_id} is blocked by:\n")
    for task in blocking:
        click.echo(f"   • {task.id}: {task.title} ({task.state.value})")


@task.command()
@click.argument("task_id")
def workspace(task_id):
    """Print the path to a task's workspace."""
    workspace_factory = get_workspace_factory()
    workspace_path = workspace_factory.get_workspace_path(task_id)
    
    if not workspace_path.exists():
        click.echo(f"❌ Workspace for {task_id} does not exist.")
        return
    
    click.echo(str(workspace_path))


@task.command()
def stats():
    """Show task statistics."""
    registry = get_registry_manager()
    stats = registry.get_statistics()
    
    click.echo("📊 Task Statistics\n")
    click.echo(f"Total tasks: {stats.total}")
    click.echo("\nBy state:")
    for state, count in stats.by_state.items():
        click.echo(f"   {state.value}: {count}")
    
    if stats.by_objective:
        click.echo("\nBy objective:")
        for objective, count in stats.by_objective.items():
            click.echo(f"   {objective}: {count}")
    
    if stats.by_assignee:
        click.echo("\nBy assignee:")
        for assignee, count in stats.by_assignee.items():
            click.echo(f"   {assignee}: {count}")


@task.command()
@click.argument("epic_path", type=click.Path(exists=True))
@click.option("--breakdown", type=click.Path(exists=True), help="Path to TASK-BREAKDOWN.md")
@click.option("--objective", help="Objective name (defaults to epic name)")
def import_epic(epic_path, breakdown, objective):
    """Import tasks from an epic.md file."""
    from .epic_import import import_epic_command

    import_epic_command(
        epic_path=epic_path,
        breakdown_path=breakdown,
        objective=objective,
    )


@task.command()
@click.option("--message", help="Commit message")
def sync_github(message):
    """Sync all tasks to GitHub issues."""
    from .integrations.github_sync import sync_github_command

    registry_path = "data/task_registry.json"
    sync_github_command(registry_path)


if __name__ == "__main__":
    task()
