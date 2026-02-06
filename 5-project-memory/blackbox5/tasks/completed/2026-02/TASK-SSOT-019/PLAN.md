# PLAN.md: Derive STATE.yaml from Source Files

**Task:** TASK-SSOT-019 - STATE.yaml is manually maintained instead of derived
**Status:** Planning
**Created:** 2026-02-06
**Estimated Effort:** 4-6 hours
**Importance:** 70 (High)

---

## 1. First Principles Analysis

### The Core Problem
STATE.yaml is manually maintained but should be derived from:
- `tasks/active/` directory
- `goals/active/` directory
- `runs/` directory
- Other source files

This creates:
1. **Manual Updates**: Must remember to update STATE.yaml
2. **Staleness**: STATE.yaml often out of date
3. **Inconsistency**: STATE.yaml doesn't match actual state
4. **Maintenance Burden**: Extra work for every change

### First Principles Solution
- **Derived Data**: STATE.yaml generated from source
- **Single Source of Truth**: Source directories are canonical
- **Automated Generation**: Script to regenerate STATE.yaml
- **Validation**: Check that derived matches expected

---

## 2. Current State Analysis

### STATE.yaml Structure

```yaml
version: "1.0"
last_updated: "2026-02-05T10:00:00Z"

project:
  name: "blackbox5"
  status: "active"

metrics:
  active_tasks: 45
  active_goals: 3
  completed_tasks: 120
  total_runs: 200

tasks:
  active:
    - id: "TASK-001"
      title: "Fix bug"
      status: "in_progress"
  # ... more tasks

goals:
  active:
    - id: "IG-001"
      title: "Improve system"
      status: "in_progress"
  # ... more goals
```

### Source Directories

| Source | STATE.yaml Section |
|--------|-------------------|
| `tasks/active/` | `tasks.active` |
| `goals/active/` | `goals.active` |
| `runs/` | `metrics.total_runs` |
| `tasks/completed/` | `metrics.completed_tasks` |

---

## 3. Proposed Solution

### Decision: Generated STATE.yaml

**Generator Script:** `2-engine/.autonomous/bin/generate-state.py`

```python
#!/usr/bin/env python3
"""Generate STATE.yaml from source directories."""

import yaml
from pathlib import Path
from datetime import datetime

def generate_state(project_path: Path) -> dict:
    """Generate STATE.yaml from source files."""
    state = {
        'version': '1.0',
        'last_updated': datetime.now().isoformat(),
        'project': {
            'name': 'blackbox5',
            'status': 'active'
        },
        'metrics': {},
        'tasks': {'active': []},
        'goals': {'active': []}
    }

    # Derive tasks from tasks/active/
    tasks_dir = project_path / 'tasks' / 'active'
    for task_dir in sorted(tasks_dir.iterdir()):
        if task_dir.is_dir() and task_dir.name.startswith('TASK-'):
            task = load_task(task_dir)
            state['tasks']['active'].append(task)

    # Derive goals from goals/active/
    goals_dir = project_path / 'goals' / 'active'
    for goal_dir in sorted(goals_dir.iterdir()):
        if goal_dir.is_dir() and goal_dir.name.startswith('IG-'):
            goal = load_goal(goal_dir)
            state['goals']['active'].append(goal)

    # Calculate metrics
    state['metrics']['active_tasks'] = len(state['tasks']['active'])
    state['metrics']['active_goals'] = len(state['goals']['active'])

    completed_dir = project_path / 'tasks' / 'completed'
    if completed_dir.exists():
        state['metrics']['completed_tasks'] = len(list(completed_dir.iterdir()))

    runs_dir = project_path / 'runs'
    if runs_dir.exists():
        state['metrics']['total_runs'] = len(list(runs_dir.iterdir()))

    return state

def load_task(task_dir: Path) -> dict:
    """Load task data from task directory."""
    task_file = task_dir / 'task.md'
    if not task_file.exists():
        return {'id': task_dir.name, 'error': 'No task.md'}

    content = task_file.read_text()

    # Parse task.md
    task = {
        'id': task_dir.name,
        'title': extract_title(content),
        'status': extract_status(content),
        'priority': extract_priority(content)
    }

    return task

def load_goal(goal_dir: Path) -> dict:
    """Load goal data from goal directory."""
    goal_file = goal_dir / 'goal.yaml'
    if not goal_file.exists():
        return {'id': goal_dir.name, 'error': 'No goal.yaml'}

    with open(goal_file) as f:
        return yaml.safe_load(f)

def main():
    project_path = Path('5-project-memory/blackbox5')
    state = generate_state(project_path)

    output_path = project_path / 'STATE.yaml'
    with open(output_path, 'w') as f:
        yaml.dump(state, f, default_flow_style=False)

    print(f"Generated {output_path}")
    print(f"  Active tasks: {state['metrics']['active_tasks']}")
    print(f"  Active goals: {state['metrics']['active_goals']}")

if __name__ == '__main__':
    main()
```

### Implementation Plan

#### Phase 1: Create Generator Script (2 hours)

1. Implement state generation logic
2. Parse task files
3. Parse goal files
4. Calculate metrics

#### Phase 2: Add Validation (1 hour)

```python
def validate_state(state: dict) -> list:
    """Validate generated state."""
    errors = []

    # Check required fields
    if 'metrics' not in state:
        errors.append("Missing metrics section")

    # Check consistency
    if len(state.get('tasks', {}).get('active', [])) != state.get('metrics', {}).get('active_tasks'):
        errors.append("Task count mismatch")

    return errors
```

#### Phase 3: Add Hook Integration (1 hour)

**Hook:** `post-task.sh`

```bash
#!/bin/bash
# Regenerate STATE.yaml after task changes

~/.blackbox5/2-engine/.autonomous/bin/generate-state.py
```

#### Phase 4: Documentation (1 hour)

1. Document that STATE.yaml is generated
2. Explain source directories
3. Add generation command to documentation

---

## 4. Files to Modify

### New Files
1. `2-engine/.autonomous/bin/generate-state.py` - State generator

### Modified Files
1. `5-project-memory/blackbox5/STATE.yaml` - Replace with generated version
2. Add hook to regenerate on changes

---

## 5. Success Criteria

- [ ] State generator script created
- [ ] STATE.yaml accurately reflects source directories
- [ ] Validation passes
- [ ] Hook regenerates state automatically
- [ ] Documentation updated
- [ ] No manual STATE.yaml edits needed

---

## 6. Rollback Strategy

If issues arise:

1. **Immediate**: Restore manual STATE.yaml
2. **Fix**: Debug generator script
3. **Re-apply**: Once fixed

---

## 7. Estimated Timeline

| Phase | Duration | Cumulative |
|-------|----------|------------|
| Phase 1: Generator | 2 hours | 2 hours |
| Phase 2: Validation | 1 hour | 3 hours |
| Phase 3: Hook | 1 hour | 4 hours |
| Phase 4: Documentation | 1 hour | 5 hours |
| **Total** | | **4-6 hours** |

---

*Plan created based on SSOT violation analysis - STATE.yaml manually maintained*
