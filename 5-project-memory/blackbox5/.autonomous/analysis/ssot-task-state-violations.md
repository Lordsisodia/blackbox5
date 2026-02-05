# SSOT Task State Violations Report

**Scout:** Architecture Analysis Agent
**Date:** 2026-02-06
**Status:** Complete

---

## Summary

Task state exists in **5 different places** with no clear single source of truth. This creates data inconsistency, race conditions, and confusion about which status is authoritative.

---

## ALL Places Where Task Data is Stored

| Location | Purpose | Data Stored |
|----------|---------|-------------|
| `tasks/active/*/task.md` | Individual task files | Status, Priority, Created date, Estimated time, Goal, Plan, Success Criteria |
| `tasks/completed/*/task.md` | Completed task files | Same as active (Status = completed) |
| `queue.yaml` | Task queue for RALF | Status, Priority, Priority Score, Type, blockedBy, blocks, resource_type, parallel_group, goal |
| `STATE.yaml` | Project state | Active tasks list (id, title, type, priority, started_at), Completed tasks list |
| `timeline.yaml` | Project timeline | Events for "Task Completed", "Task Started", "New Task Created" with task IDs |
| `events.yaml` | Execution events | Task start/in_progress events with task_id, agent, run_id |

---

## Duplicated Data Identified

### Task Status - DUPLICATED in 4+ places:
1. **task.md files** - `**Status:** completed|pending|in_progress`
2. **queue.yaml** - `status: completed|pending|in_progress`
3. **STATE.yaml** - Tasks listed under `tasks.active` vs `tasks.completed`
4. **timeline.yaml** - Events log task status changes
5. **events.yaml** - Task execution events (started, in_progress)

### Task Priority - DUPLICATED:
1. **task.md files** - `**Priority:** HIGH|CRITICAL|MEDIUM|LOW`
2. **queue.yaml** - `priority: HIGH|CRITICAL|MEDIUM|LOW` + `priority_score: 8.5`

### Task Metadata - DUPLICATED:
| Field | task.md | queue.yaml | STATE.yaml |
|-------|---------|------------|------------|
| Task ID | Filename | `id:` | `id:` |
| Title | First line | `title:` | `title:` |
| Created Date | `**Created:**` | - | `started_at` |
| Estimated Time | `**Estimated:**` | `estimated_minutes:` | - |
| Goal | `**Goal:**` | `goal:` | - |

### Task Counts/Statistics - DUPLICATED:
- **queue.yaml**: `total_tasks: 90`, `completed: 25`, `in_progress: 5`, `pending: 60`
- **queue_metadata**: Same counts repeated
- **STATE.yaml**: Lists active and completed tasks separately

---

## Specific Inconsistencies Found

### Inconsistency #1: TASK-ARCH-016 Status Confusion
- **queue.yaml** (line 391): `status: "in_progress"` (placeholder entry)
- **queue.yaml** (line 435): `status: "pending"` (real entry)
- **Same task ID appears twice** in queue.yaml with different statuses

### Inconsistency #2: Duplicate Task Entries
queue.yaml documents 13 duplicate task pairs (lines 49-62):
```
# 1. AGENT-SYSTEM-AUDIT / TASK-AUTO-010 (keep TASK-AUTO-010)
# 2. TASK-1769978192 / TASK-ARCH-016 (keep TASK-ARCH-016)
...
```

### Inconsistency #3: Timeline vs STATE.yaml
- **timeline.yaml** has hundreds of "Task Completed" events
- **STATE.yaml** has only 4 completed tasks listed
- **Major discrepancy** - timeline tracks every completion, STATE.yaml only tracks recent ones

### Inconsistency #4: Task Location vs Status
- Tasks in `tasks/active/` directory have `**Status:** completed` in their task.md
- Tasks in `tasks/completed/` directory also have `status: completed`
- **Location implies status, but file content also has status** - potential for mismatch

---

## Recommendations for SSOT

### Recommended SSOT Hierarchy:

| Data | SSOT Location | Rationale |
|------|---------------|-----------|
| **Task Status** | `tasks/{active,completed}/TASK-XXX/task.md` | Filesystem location + file content |
| **Task Priority** | `queue.yaml` | Centralized for prioritization algorithm |
| **Task Queue/Ordering** | `queue.yaml` | Purpose-built for RALF scheduling |
| **Task History/Events** | `timeline.yaml` | Append-only event log |
| **Project Summary** | `STATE.yaml` | Should be DERIVED, not source |
| **Execution Events** | `events.yaml` | Real-time execution tracking |

### Critical Fixes Needed:

1. **Remove duplicate task entries from queue.yaml** - 13 duplicates documented but not removed
2. **Make STATE.yaml a derived view** - It should aggregate from task.md files, not duplicate
3. **Standardize status transitions** - Use timeline.yaml as audit log, not parallel status storage
4. **Fix TASK-ARCH-016** - Appears twice in queue.yaml with conflicting statuses
5. **Automate sync** - The `sync-state.py` script exists but may not be running consistently

---

## Files Requiring Attention

| File | Issue |
|------|-------|
| `queue.yaml` | 13 duplicate tasks, TASK-ARCH-016 appears twice |
| `STATE.yaml` | Duplicates task data that exists in task.md files |
| `timeline.yaml` | Massive file (1500+ lines) with redundant event entries |
| `events.yaml` | Task events may duplicate timeline.yaml events |
