#!/usr/bin/env python3
"""Generate STATE.yaml from actual task and goal files."""
import yaml
from pathlib import Path
from datetime import datetime

def count_tasks(tasks_dir):
    """Count tasks in directory."""
    if not tasks_dir.exists():
        return 0
    return len([d for d in tasks_dir.iterdir() if d.is_dir() and d.name.startswith('TASK-')])

def get_goal_statuses(goals_dir):
    """Read goal statuses from goal.yaml files (supports both YAML and markdown formats)."""
    statuses = {}
    if not goals_dir.exists():
        return statuses
    for goal_dir in goals_dir.iterdir():
        if not goal_dir.is_dir():
            continue
        goal_yaml = goal_dir / 'goal.yaml'
        if goal_yaml.exists():
            try:
                with open(goal_yaml) as f:
                    content = f.read()
                    # Try YAML first
                    try:
                        data = yaml.safe_load(content)
                        if data and isinstance(data, dict):
                            # Check for status at root level
                            if 'status' in data:
                                statuses[goal_dir.name] = data['status']
                                continue
                            # Check for status in meta section
                            if 'meta' in data and isinstance(data['meta'], dict):
                                if 'status' in data['meta']:
                                    statuses[goal_dir.name] = data['meta']['status']
                                    continue
                    except yaml.YAMLError:
                        pass
                    # Fallback: parse markdown-style **Status:** field
                    for line in content.split('\n'):
                        if '**Status:**' in line or 'Status:' in line:
                            status = line.split(':', 1)[1].strip()
                            status = status.strip('*').strip()
                            statuses[goal_dir.name] = status
                            break
                    else:
                        statuses[goal_dir.name] = 'unknown'
            except Exception as e:
                statuses[goal_dir.name] = f'error: {e}'
    return statuses

def generate_state():
    bb5_root = Path.home() / '.blackbox5'
    project_dir = bb5_root / '5-project-memory/blackbox5'

    # Count tasks
    active_count = count_tasks(project_dir / 'tasks/active')
    completed_count = count_tasks(project_dir / 'tasks/completed')

    # Get goal statuses
    goal_statuses = get_goal_statuses(project_dir / 'goals/active')

    # Generate STATE.yaml content
    state = {
        'meta': {
            'generated': datetime.now().isoformat(),
            'source': 'derived from filesystem'
        },
        'tasks': {
            'active': active_count,
            'completed': completed_count,
            'total': active_count + completed_count
        },
        'goals': goal_statuses
    }

    # Write STATE.yaml
    output_path = project_dir / 'STATE.yaml'
    with open(output_path, 'w') as f:
        yaml.dump(state, f, default_flow_style=False, sort_keys=False)

    print(f"Generated STATE.yaml: {active_count} active, {completed_count} completed tasks")
    print(f"Goals tracked: {len(goal_statuses)}")
    print(f"Output: {output_path}")

if __name__ == '__main__':
    generate_state()
