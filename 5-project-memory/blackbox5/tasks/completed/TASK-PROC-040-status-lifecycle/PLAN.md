# PLAN.md: Task Status Lifecycle Automation

**Task ID:** TASK-STATUS-LIFECYCLE-ACTION-PLAN
**Type:** design | implement
**Priority:** CRITICAL
**Status:** Planning
**Created:** 2026-02-03
**Related:** Critical Blocker #2
**Estimated Effort:** 3 hours

---

## 1. First Principles Analysis

### Why is Task Status Lifecycle Automation Critical?

1. **Visibility**: Know what's actually being worked on vs. what's planned
2. **Duplicate Work Prevention**: Prevent multiple executors from picking up same task
3. **Audit Trail**: Complete history of task progression
4. **Feedback Loops**: Planner knows when tasks start/complete
5. **Automation**: No manual status updates (which are forgotten)

### What Happens Without Automated Status Transitions?

| Problem | Impact | Evidence |
|---------|--------|----------|
| Task remains "pending" when being worked on | No visibility | 182-run analysis |
| Multiple executors pick same task | Duplicate work | Critical Blocker #2 |
| No record of task progression | Broken audit trail | Missing events |
| Planner doesn't know task status | Poor prioritization | Queue staleness |
| Manual updates forgotten | Stale data | 0% sync success |

### How Does Hook-Based State Management Help?

By enforcing state transitions through code (hooks/scripts) rather than suggestions (prompts), we achieve:
- **Deterministic transitions** - Status changes when actions occur
- **Zero manual updates** - No reliance on LLM memory
- **Complete audit trail** - Every transition logged
- **Consistent state** - queue.yaml as single source of truth

---

## 2. Current State Assessment

### Existing Infrastructure

| Component | Location | Status |
|-----------|----------|--------|
| queue.yaml | `.autonomous/agents/communications/queue.yaml` | Has status field (pending/completed) |
| Task files | `tasks/active/TASK-XXX/task.md` | Has Status field in frontmatter |
| Events log | `.autonomous/agents/communications/events.yaml` | Logs events but no status linking |
| Working directory | `tasks/working/` | Auto-created on claim (Blocker #1 fixed) |

### What's Missing

| Gap | Impact |
|-----|--------|
| No automated status transition on claim | Status stays pending |
| No in_progress status | Cannot distinguish claimed vs. active |
| No linking between events.yaml and queue.yaml | Inconsistent records |
| No task move from active/ to completed/ | Manual cleanup required |
| No STATE.yaml integration | System state fragmented |

---

## 3. Proposed Solution

### State Machine Design

```
planned → ready → claimed → in_progress → completed → archived
   ↑         ↑        ↑          ↑           ↑
   |         |        |          |           |
 Planner  Planner  Executor   Executor    Stop Hook
 creates  queues   claims     works       archives
```

### States Definition

| State | Meaning | Set By | Next States |
|-------|---------|--------|-------------|
| **planned** | Task exists but not ready for execution | Task creation | ready |
| **ready** | Task is prioritized and in queue | Planner | claimed |
| **claimed** | Executor has claimed task, working dir created | ralf-task-select.sh | in_progress, failed |
| **in_progress** | Executor is actively working | ralf-task-start.sh | completed, failed |
| **completed** | Task finished successfully | Stop hook | archived |
| **failed** | Task failed, needs replanning | Stop hook | ready (replan) |
| **archived** | Task moved to completed/ folder | Stop hook | - |

### queue.yaml Extensions

```yaml
queue:
  - task_id: "TASK-001"
    status: "in_progress"  # Extended: planned, ready, claimed, in_progress, completed, failed
    priority: "HIGH"
    created_at: "2026-02-03T10:00:00Z"
    # New fields:
    claimed_at: "2026-02-03T14:30:00Z"
    claimed_by: "executor-1"
    started_at: "2026-02-03T14:35:00Z"
    completed_at: null
    failed_at: null
    failure_reason: null
```

---

## 4. Implementation Plan

### Phase 1: Extend queue.yaml Schema (15 min)

**1.1 Update queue.yaml structure**
- Add status values: `claimed`, `in_progress`, `failed`
- Add timestamp fields: `claimed_at`, `claimed_by`, `started_at`, `completed_at`, `failed_at`
- Add `failure_reason` field for failed tasks
- Update schema validation

**1.2 Create migration script**
- Update existing tasks to new schema
- Set default values for new fields

### Phase 2: Update Task Selection Script (30 min)

**2.1 Update `bin/ralf-task-select.sh`**
```bash
#!/bin/bash
# ralf-task-select.sh - Claim a task for execution

TASK_ID=$1
CLAIMED_BY=$2

# Update queue.yaml
python3 << EOF
import yaml
from datetime import datetime

with open('.autonomous/agents/communications/queue.yaml', 'r') as f:
    queue = yaml.safe_load(f)

for task in queue['queue']:
    if task['task_id'] == '$TASK_ID':
        task['status'] = 'claimed'
        task['claimed_at'] = datetime.now().isoformat()
        task['claimed_by'] = '$CLAIMED_BY'
        break

with open('.autonomous/agents/communications/queue.yaml', 'w') as f:
    yaml.dump(queue, f)
EOF

# Create event
echo "- timestamp: $(date -Iseconds)
  event: task_claimed
  task_id: $TASK_ID
  claimed_by: $CLAIMED_BY" >> .autonomous/agents/communications/events.yaml

echo "Task $TASK_ID claimed by $CLAIMED_BY"
```

**2.2 Add validation**
- Check task exists before claiming
- Check task is in 'ready' status
- Prevent double-claiming

### Phase 3: Create Task Start Script (30 min)

**3.1 Create `bin/ralf-task-start.sh`**
```bash
#!/bin/bash
# ralf-task-start.sh - Mark task as in_progress

TASK_ID=$1

# Update queue.yaml
python3 << EOF
import yaml
from datetime import datetime

with open('.autonomous/agents/communications/queue.yaml', 'r') as f:
    queue = yaml.safe_load(f)

for task in queue['queue']:
    if task['task_id'] == '$TASK_ID':
        task['status'] = 'in_progress'
        task['started_at'] = datetime.now().isoformat()
        break

with open('.autonomous/agents/communications/queue.yaml', 'w') as f:
    yaml.dump(queue, f)
EOF

# Update STATE.yaml
# Update heartbeat
# Create event

echo "Task $TASK_ID started"
```

**3.2 Add heartbeat mechanism**
- Periodic updates while task is in_progress
- Timeout detection for stalled tasks

### Phase 4: Update Stop Hook (45 min)

**4.1 Update `bin/ralf-stop-hook.sh`**
```bash
#!/bin/bash
# ralf-stop-hook.sh - Handle task completion on session stop

# Check if task was being worked on
if [ -f ".autonomous/tasks/working/.current-task" ]; then
    TASK_ID=$(cat .autonomous/tasks/working/.current-task)

    # Check completion status (passed via environment or file)
    if [ "$TASK_STATUS" == "completed" ]; then
        # Mark as completed
        python3 << EOF
import yaml
from datetime import datetime

with open('.autonomous/agents/communications/queue.yaml', 'r') as f:
    queue = yaml.safe_load(f)

for task in queue['queue']:
    if task['task_id'] == '$TASK_ID':
        task['status'] = 'completed'
        task['completed_at'] = datetime.now().isoformat()
        break

with open('.autonomous/agents/communications/queue.yaml', 'w') as f:
    yaml.dump(queue, f)
EOF

        # Move task to completed/
        mv "tasks/active/$TASK_ID" "tasks/completed/"

        # Update STATE.yaml

        # Create event
        echo "Task $TASK_ID completed and archived"

    elif [ "$TASK_STATUS" == "failed" ]; then
        # Mark as failed
        python3 << EOF
import yaml
from datetime import datetime

with open('.autonomous/agents/communications/queue.yaml', 'r') as f:
    queue = yaml.safe_load(f)

for task in queue['queue']:
    if task['task_id'] == '$TASK_ID':
        task['status'] = 'failed'
        task['failed_at'] = datetime.now().isoformat()
        task['failure_reason'] = '${TASK_FAILURE_REASON:-Unknown}'
        break

with open('.autonomous/agents/communications/queue.yaml', 'w') as f:
    yaml.dump(queue, f)
EOF

        echo "Task $TASK_ID marked as failed"
    fi
fi

# Commit and push if configured
```

**4.2 Add completion validation**
- Verify task completion criteria met
- Check for uncommitted changes
- Require commit message

### Phase 5: Create Status Sync Script (30 min)

**5.1 Create `bin/ralf-task-status.sh`**
```bash
#!/bin/bash
# ralf-task-status.sh - Task status management utility

COMMAND=$1
TASK_ID=$2

 case $COMMAND in
    show)
        # Show current status
        python3 << EOF
import yaml

with open('.autonomous/agents/communications/queue.yaml', 'r') as f:
    queue = yaml.safe_load(f)

for task in queue['queue']:
    if task['task_id'] == '$TASK_ID':
        print(f"Task: {task['task_id']}")
        print(f"Status: {task['status']}")
        print(f"Priority: {task['priority']}")
        print(f"Created: {task.get('created_at', 'N/A')}")
        print(f"Claimed: {task.get('claimed_at', 'N/A')} by {task.get('claimed_by', 'N/A')}")
        print(f"Started: {task.get('started_at', 'N/A')}")
        print(f"Completed: {task.get('completed_at', 'N/A')}")
        break
EOF
        ;;

    sync)
        # Sync queue.yaml with task.md and events.yaml
        python3 << EOF
import yaml
from pathlib import Path

# Load queue
with open('.autonomous/agents/communications/queue.yaml', 'r') as f:
    queue = yaml.safe_load(f)

# Sync each task
for task in queue['queue']:
    task_id = task['task_id']

    # Update task.md if exists
    task_md_path = Path(f"tasks/active/{task_id}/task.md")
    if task_md_path.exists():
        content = task_md_path.read_text()
        # Update status in frontmatter
        # (Implementation depends on frontmatter format)

    # Verify events.yaml has lifecycle events
    # Add missing events

# Save updated queue
with open('.autonomous/agents/communications/queue.yaml', 'w') as f:
    yaml.dump(queue, f)

print("Sync complete")
EOF
        ;;

    list)
        # List tasks by status
        STATUS_FILTER=$3
        python3 << EOF
import yaml

with open('.autonomous/agents/communications/queue.yaml', 'r') as f:
    queue = yaml.safe_load(f)

print(f"{'Task ID':<20} {'Status':<15} {'Priority':<10} {'Claimed By':<15}")
print("-" * 65)

for task in queue['queue']:
    if not '$STATUS_FILTER' or task['status'] == '$STATUS_FILTER':
        print(f"{task['task_id']:<20} {task['status']:<15} {task['priority']:<10} {task.get('claimed_by', 'N/A'):<15}")
EOF
        ;;

    *)
        echo "Usage: ralf-task-status.sh [show|sync|list] [task_id|status]"
        exit 1
        ;;
esac
```

**5.2 Add sync capabilities**
- Ensure queue.yaml, task.md, and events.yaml are consistent
- Can be run periodically or on demand
- Recovery mechanism for out-of-sync states

### Phase 6: Testing (30 min)

**6.1 Status Transition Test**
- Create test task → verify 'planned' status
- Mark ready → verify 'ready' status
- Claim task → verify 'claimed' status with timestamps
- Start task → verify 'in_progress' status
- Complete task → verify 'completed' status and archive

**6.2 Failure Scenario Test**
- Start task → verify 'in_progress'
- Fail task → verify 'failed' status
- Verify failure_reason captured
- Verify can replan from failed

**6.3 Sync Test**
- Manually modify task.md status
- Run sync → verify queue.yaml updated
- Verify events.yaml has complete lifecycle

**6.4 Double-Claim Prevention Test**
- Claim task with executor-1
- Attempt claim with executor-2 → verify blocked

---

## 5. Success Criteria

| Criterion | Verification Method |
|-----------|---------------------|
| When task is claimed, status changes to 'claimed' | Run ralf-task-select.sh, check queue.yaml |
| When work starts, status changes to 'in_progress' | Run ralf-task-start.sh, check queue.yaml |
| When task completes, status changes to 'completed' | Run Stop hook, check queue.yaml |
| Completed tasks are moved to tasks/completed/ | Verify directory move |
| STATE.yaml is updated with task status | Check STATE.yaml |
| events.yaml has complete lifecycle events | Check events.yaml |
| No manual status updates required | Full automation test |
| Sync script recovers out-of-sync states | Test sync command |
| Double-claiming is prevented | Test concurrent claims |

---

## 6. Estimated Timeline

| Phase | Duration | Cumulative |
|-------|----------|------------|
| Phase 1: Extend queue.yaml | 15 min | 15 min |
| Phase 2: Update ralf-task-select.sh | 30 min | 45 min |
| Phase 3: Create ralf-task-start.sh | 30 min | 75 min |
| Phase 4: Update ralf-stop-hook.sh | 45 min | 120 min |
| Phase 5: Create status sync script | 30 min | 150 min |
| Phase 6: Testing | 30 min | 180 min |
| **Total** | **3 hours** | |

---

## 7. First Principles

**Core Principle:** State transitions should be enforced by code (hooks/scripts), not suggested by prompts. Any status change that relies on an LLM remembering to update a file will fail.

**Design Decision:** Keep queue.yaml as the source of truth for task status, sync to other locations (task.md, STATE.yaml) from there.

**Risk Mitigation:** The status sync script (Step 5) provides a recovery mechanism if statuses get out of sync.

---

## 8. Files to Modify

| File | Change |
|------|--------|
| `.autonomous/agents/communications/queue.yaml` | Add status values and timestamps |
| `bin/ralf-task-select.sh` | Set claimed status on claim |
| `bin/ralf-task-start.sh` | **NEW:** Set in_progress status |
| `bin/ralf-stop-hook.sh` | Set completed/failed, move task |
| `bin/ralf-task-status.sh` | **NEW:** Status sync utility |

---

## 9. Dependencies

- **TASK-010-001** (SessionStart Enhanced Hook) - Provides hook infrastructure
- **TASK-1769978192** (Agent Execution Flow) - Defines overall flow

---

*Automated status lifecycle transforms task management from a manual, error-prone process to a deterministic, traceable system.*
