# SSOT Task State: What Scouts Missed - timeline.yaml Deep Dive

**Scout:** Architecture Analysis Agent (Follow-up)
**Date:** 2026-02-06
**Focus:** Timeline corruption and phantom tasks

---

## Critical Finding: Timeline Events for NON-EXISTENT Tasks

The timeline contains **85+ "Task Completed" events** for numeric task IDs (1-61) that **DO NOT EXIST** as task files.

---

## Phantom Task Completions

| Task ID | # Completion Events | File Exists? |
|---------|---------------------|--------------|
| Task 1 | 4 events | NO |
| Tasks 2, 5-10, 12-13, 18, 23 | 3 events each | NO |
| Tasks 3-4, 11, 14-17 | 2 events each | NO |

**Total:** 85+ completion events for phantom tasks.

---

## Tasks in Active/ with Status: completed (28 found)

These tasks have `**Status:** completed` but remain in `tasks/active/`:

| Task | Status in File | Location | Should Be |
|------|---------------|----------|-----------|
| TASK-SSOT-001 | completed | active/ | completed/ |
| TASK-ARCH-017 | completed | active/ | completed/ |
| TASK-ARCH-028 | completed | active/ | completed/ |
| TASK-PROC-008 | completed | active/ | completed/ |
| TASK-SKIL-001 | completed | active/ | completed/ |
| TASK-ARCH-001 through TASK-ARCH-011 | completed | active/ | completed/ |
| (23 more tasks) | completed | active/ | completed/ |

---

## Duplicate Task Directories

Found evidence of duplicate directories:

- `TASK-ARCH-016/`
- `TASK-ARCH-016-agent-execution-flow/` (both exist)

queue.yaml acknowledges 13 duplicate pairs but cleanup hasn't happened.

---

## Timeline Data Corruption

Multiple completion events for same task on same day:

| Task ID | # Completion Events |
|---------|---------------------|
| 1 | 4 events |
| 2, 5, 6, 7, 8, 9, 10, 12, 13, 18, 23 | 3 events each |
| 3, 4, 11, 14, 15, 16, 17 | 2 events each |

**Root cause:** Timeline update mechanism is **not idempotent** - keeps appending instead of checking.

---

## Missing Timeline Events for Real Completed Tasks

- 110+ tasks in `tasks/completed/` folder
- Only numeric phantom tasks appear in timeline completions
- Real completed tasks have NO timeline events

---

## Inconsistent Task ID Formats

Three different ID formats in use:

1. **Numeric IDs** (1, 2, 3...) - used in timeline, don't exist as files
2. **Timestamp IDs** (TASK-1769978192) - older tasks
3. **Semantic IDs** (TASK-ARCH-001) - newer tasks

**Creates confusion** about which ID system is canonical.

---

## What Initial Scouts Missed

| Issue | Severity | Scouts Found? |
|-------|----------|---------------|
| 85+ phantom task completions | CRITICAL | NO |
| 28 tasks in wrong directory | HIGH | Partial (not quantified) |
| Duplicate task directories | MEDIUM | Noted but not detailed |
| Timeline not idempotent | HIGH | NO |
| Real completed tasks missing from timeline | HIGH | NO |
| Three ID formats | MEDIUM | NO |
