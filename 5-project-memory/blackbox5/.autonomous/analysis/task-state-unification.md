# Task State Unification (SSOT-032)

## Canonical Source of Truth

**Primary Source:** Filesystem task directories
- Location: `~/.blackbox5/5-project-memory/blackbox5/tasks/active/TASK-*/task.md`
- Status field in task.md is the authoritative source

**Derived Sources:**
1. **queue.yaml** - Runtime queue for task selection (derived from filesystem)
2. **STATE.yaml** - High-level summary (derived from queue.yaml)

## State Hierarchy

```
Filesystem (task.md)
    |
    v
queue.yaml (runtime queue)
    |
    v
STATE.yaml (summary)
```

## Status Values

| Status | Meaning | Location |
|--------|---------|----------|
| pending | Ready to be queued | task.md, queue.yaml |
| claimed | Executor has claimed task | queue.yaml |
| in_progress | Currently being worked | task.md, queue.yaml |
| completed | Done | task.md, queue.yaml |
| blocked | Has unmet dependencies | task.md |

## Sync Rules

1. **Filesystem is master** - Always read task.md first
2. **queue.yaml is runtime cache** - Updated by planner/executor
3. **STATE.yaml is summary** - Generated from queue.yaml
4. **Never edit task.md status directly in queue.yaml** - Use task promotion workflow

## Validation Checklist

- [ ] task.md status matches queue.yaml status
- [ ] queue.yaml pending count matches STATE.yaml active count
- [ ] No duplicate task IDs in queue.yaml
- [ ] No self-blocking dependencies (task blocks itself)

## Fixed Issues (SSOT-010)

- Removed duplicate TASK-ARCH-016-agent-execution-flow (was self-blocking)
- Removed duplicate TASK-ARCH-012-mirror-candidates
- Updated schema version to 1.0.1
