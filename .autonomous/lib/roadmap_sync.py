#!/usr/bin/env python3
"""
Roadmap Synchronization Library

This module provides functions to automatically synchronize STATE.yaml
with task completion, preventing drift between documented state and actual state.

Functions:
- update_plan_status(plan_id, status): Update plan status
- unblock_dependents(plan_id): Unblock plans that depend on completed plan
- update_next_action(plan_id): Update next_action to next unblocked plan
- update_goal_status(goal_id): Update goal status if all plans complete
- sync_on_task_completion(task_id, plan_id): Main sync function for task completion
"""

import os
import re
import yaml
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple

# Path configuration
BB5_DIR = Path("/opt/blackbox5")
PROJECT_DIR = BB5_DIR / "5-project-memory/blackbox5"
STATE_FILE = PROJECT_DIR / "STATE.yaml"
GOALS_FILE = PROJECT_DIR / "goals.yaml"
PLANS_DIR = PROJECT_DIR / "plans/active"


def load_state() -> Dict:
    """Load STATE.yaml file."""
    if not STATE_FILE.exists():
        return {}

    with open(STATE_FILE, 'r') as f:
        return yaml.safe_load(f) or {}


def save_state(state: Dict):
    """Save STATE.yaml file."""
    # Update metadata
    state['meta'] = {
        'generated': datetime.now(timezone.utc).isoformat(),
        'source': 'derived from task completion via roadmap_sync.py'
    }

    with open(STATE_FILE, 'w') as f:
        yaml.dump(state, f, default_flow_style=False, sort_keys=False)


def load_goals() -> Dict:
    """Load goals.yaml file."""
    if not GOALS_FILE.exists():
        return {}

    with open(GOALS_FILE, 'r') as f:
        return yaml.safe_load(f) or {}


def save_goals(goals: Dict):
    """Save goals.yaml file."""
    with open(GOALS_FILE, 'w') as f:
        yaml.dump(goals, f, default_flow_style=False, sort_keys=False)


def find_plan_metadata(plan_id: str) -> Optional[Dict]:
    """
    Find plan metadata file in plans/active/.

    Args:
        plan_id: Plan ID (e.g., PLAN-001)

    Returns:
        Dict with plan metadata or None if not found
    """
    # Search in plans/active/ subdirectories
    for plan_dir in PLANS_DIR.rglob("*"):
        if plan_dir.is_dir():
            metadata_file = plan_dir / "metadata.yaml"
            if metadata_file.exists():
                with open(metadata_file, 'r') as f:
                    data = yaml.safe_load(f)
                    if data and data.get('plan_id') == plan_id:
                        return data
    return None


def update_plan_status(plan_id: str, status: str) -> bool:
    """
    Update plan status to 'completed' in metadata.yaml.

    Args:
        plan_id: Plan ID (e.g., PLAN-001)
        status: New status (e.g., 'completed', 'in_progress')

    Returns:
        True if updated, False if not found
    """
    # Find plan metadata
    metadata = find_plan_metadata(plan_id)
    if not metadata:
        print(f"  ⚠️  Plan {plan_id} not found in plans/active/")
        return False

    # Update status in metadata file
    for plan_dir in PLANS_DIR.rglob("*"):
        if plan_dir.is_dir():
            metadata_file = plan_dir / "metadata.yaml"
            if metadata_file.exists():
                with open(metadata_file, 'r') as f:
                    data = yaml.safe_load(f)
                    if data and data.get('plan_id') == plan_id:
                        data['status'] = status
                        data['completed_at'] = datetime.now(timezone.utc).isoformat()

                        with open(metadata_file, 'w') as f:
                            yaml.dump(data, f, default_flow_style=False, sort_keys=False)

                        print(f"  ✅ Updated plan {plan_id} status to {status}")
                        return True

    return False


def unblock_dependents(plan_id: str) -> List[str]:
    """
    Unblock plans that depend on the completed plan.

    Args:
        plan_id: Completed plan ID (e.g., PLAN-001)

    Returns:
        List of unblocked plan IDs
    """
    unblocked = []

    # Scan all plan metadata files
    for plan_dir in PLANS_DIR.rglob("*"):
        if plan_dir.is_dir():
            metadata_file = plan_dir / "metadata.yaml"
            if metadata_file.exists():
                with open(metadata_file, 'r') as f:
                    data = yaml.safe_load(f)

                    if data and 'dependencies' in data:
                        dependencies = data['dependencies']

                        # Check if this plan depends on the completed plan
                        if plan_id in dependencies:
                            # Remove plan_id from dependencies
                            remaining_deps = [d for d in dependencies if d != plan_id]

                            if len(remaining_deps) < len(dependencies):
                                # Update metadata
                                data['dependencies'] = remaining_deps

                                # If no more dependencies, mark as unblocked
                                if not remaining_deps:
                                    data['status'] = 'planned'  # Ready to start
                                    print(f"  ✅ Unblocked plan {data.get('plan_id')} (all dependencies complete)")
                                    unblocked.append(data.get('plan_id'))
                                else:
                                    print(f"  ℹ️  Plan {data.get('plan_id')} still has {len(remaining_deps)} dependencies")

                                # Write back
                                with open(metadata_file, 'w') as f:
                                    yaml.dump(data, f, default_flow_style=False, sort_keys=False)

    return unblocked


def update_next_action(completed_plan_id: str) -> Optional[str]:
    """
    Update next_action to the next unblocked plan.

    Args:
        completed_plan_id: The plan that was just completed

    Returns:
        The new next_action plan ID or None
    """
    state = load_state()

    # Find all plans that are ready (no dependencies, status='planned')
    ready_plans = []

    for plan_dir in PLANS_DIR.rglob("*"):
        if plan_dir.is_dir():
            metadata_file = plan_dir / "metadata.yaml"
            if metadata_file.exists():
                with open(metadata_file, 'r') as f:
                    data = yaml.safe_load(f)

                    if data and data.get('status') == 'planned':
                        dependencies = data.get('dependencies', [])
                        if not dependencies:
                            # Plan is ready to start
                            ready_plans.append({
                                'plan_id': data.get('plan_id'),
                                'priority': data.get('priority', 'medium'),
                                'created': data.get('created', '')
                            })

    # Sort by priority (high > medium > low)
    priority_order = {'high': 0, 'medium': 1, 'low': 2}
    ready_plans.sort(key=lambda x: priority_order.get(x['priority'], 3))

    # Update next_action
    if ready_plans:
        next_plan = ready_plans[0]['plan_id']

        # Don't set next_action to the just-completed plan
        if next_plan != completed_plan_id:
            state['next_action'] = next_plan
            save_state(state)
            print(f"  ✅ Updated next_action to {next_plan}")
            return next_plan

    return None


def update_goal_status(goal_id: str) -> bool:
    """
    Update goal status if all its plans are complete.

    Args:
        goal_id: Goal ID (e.g., IG-001)

    Returns:
        True if updated, False if not applicable
    """
    goals = load_goals()

    # Check if goal exists
    if goal_id not in goals:
        print(f"  ⚠️  Goal {goal_id} not found in goals.yaml")
        return False

    current_status = goals[goal_id]
    if current_status == 'completed':
        print(f"  ℹ️  Goal {goal_id} already completed")
        return False

    # Find all plans linked to this goal
    goal_plans = []

    for plan_dir in PLANS_DIR.rglob("*"):
        if plan_dir.is_dir():
            metadata_file = plan_dir / "metadata.yaml"
            if metadata_file.exists():
                with open(metadata_file, 'r') as f:
                    data = yaml.safe_load(f)

                    if data and data.get('linked_goal') == goal_id:
                        goal_plans.append({
                            'plan_id': data.get('plan_id'),
                            'status': data.get('status')
                        })

    # Check if all plans are complete
    if not goal_plans:
        print(f"  ℹ️  No plans found for goal {goal_id}")
        return False

    all_complete = all(p['status'] == 'completed' for p in goal_plans)

    if all_complete:
        goals[goal_id] = 'completed'
        save_goals(goals)
        print(f"  ✅ Goal {goal_id} marked as completed (all plans done)")
        return True
    else:
        incomplete = [p['plan_id'] for p in goal_plans if p['status'] != 'completed']
        print(f"  ℹ️  Goal {goal_id} has {len(incomplete)} incomplete plans: {incomplete}")
        return False


def sync_on_task_completion(task_id: str, plan_id: Optional[str] = None, goal_id: Optional[str] = None) -> Dict:
    """
    Main synchronization function called after task completion.

    Args:
        task_id: Completed task ID (e.g., TASK-001)
        plan_id: Optional plan ID associated with task
        goal_id: Optional goal ID associated with task

    Returns:
        Dict with sync results
    """
    print(f"\n🔄 Syncing roadmap state for task {task_id}...")

    results = {
        'task_id': task_id,
        'plan_updated': False,
        'unblocked_plans': [],
        'next_action_updated': False,
        'goal_updated': False,
        'errors': []
    }

    try:
        # Step 1: Update plan status if plan_id provided
        if plan_id:
            print(f"\n📋 Step 1: Updating plan {plan_id} status...")
            success = update_plan_status(plan_id, 'completed')
            results['plan_updated'] = success
            results['plan_id'] = plan_id
        else:
            print("  ℹ️  No plan_id provided, skipping plan status update")

        # Step 2: Unblock dependent plans
        if plan_id:
            print(f"\n🔓 Step 2: Unblocking dependent plans...")
            unblocked = unblock_dependents(plan_id)
            results['unblocked_plans'] = unblocked
            print(f"  📊 Unblocked {len(unblocked)} plan(s)")
        else:
            print("  ℹ️  No plan_id provided, skipping dependency unblocking")

        # Step 3: Update next_action
        if plan_id:
            print(f"\n➡️  Step 3: Updating next_action...")
            next_plan = update_next_action(plan_id)
            results['next_action_updated'] = next_plan is not None
            results['next_action'] = next_plan
        else:
            print("  ℹ️  No plan_id provided, skipping next_action update")

        # Step 4: Update goal status if goal_id provided
        if goal_id:
            print(f"\n🎯 Step 4: Updating goal {goal_id} status...")
            success = update_goal_status(goal_id)
            results['goal_updated'] = success
            results['goal_id'] = goal_id
        else:
            print("  ℹ️  No goal_id provided, skipping goal status update")

        print(f"\n✅ Roadmap sync complete for task {task_id}")

    except Exception as e:
        error_msg = f"Error during sync: {str(e)}"
        print(f"  ❌ {error_msg}")
        results['errors'].append(error_msg)

    return results


def get_roadmap_status() -> Dict:
    """
    Get current roadmap status summary.

    Returns:
        Dict with roadmap status
    """
    goals = load_goals()
    state = load_state()

    # Count plans by status
    plans_by_status = {}
    plans_by_goal = {}

    for plan_dir in PLANS_DIR.rglob("*"):
        if plan_dir.is_dir():
            metadata_file = plan_dir / "metadata.yaml"
            if metadata_file.exists():
                with open(metadata_file, 'r') as f:
                    data = yaml.safe_load(f)

                    if data:
                        status = data.get('status', 'unknown')
                        plans_by_status[status] = plans_by_status.get(status, 0) + 1

                        goal_id = data.get('linked_goal')
                        if goal_id:
                            if goal_id not in plans_by_goal:
                                plans_by_goal[goal_id] = {'total': 0, 'completed': 0}
                            plans_by_goal[goal_id]['total'] += 1
                            if status == 'completed':
                                plans_by_goal[goal_id]['completed'] += 1

    return {
        'goals': goals,
        'next_action': state.get('next_action'),
        'plans_by_status': plans_by_status,
        'plans_by_goal': plans_by_goal
    }


if __name__ == '__main__':
    # Test the sync function
    import sys

    if len(sys.argv) < 2:
        print("Usage: python roadmap_sync.py <task_id> [plan_id] [goal_id]")
        print("Example: python roadmap_sync.py TASK-001 PLAN-001 IG-001")
        sys.exit(1)

    task_id = sys.argv[1]
    plan_id = sys.argv[2] if len(sys.argv) > 2 else None
    goal_id = sys.argv[3] if len(sys.argv) > 3 else None

    results = sync_on_task_completion(task_id, plan_id, goal_id)

    print(f"\n📊 Sync Results:")
    print(f"  Task: {results['task_id']}")
    print(f"  Plan Updated: {results['plan_updated']}")
    print(f"  Unblocked Plans: {results['unblocked_plans']}")
    print(f"  Next Action Updated: {results['next_action_updated']}")
    print(f"  Goal Updated: {results['goal_updated']}")

    if results['errors']:
        print(f"\n❌ Errors:")
        for error in results['errors']:
            print(f"  - {error}")
