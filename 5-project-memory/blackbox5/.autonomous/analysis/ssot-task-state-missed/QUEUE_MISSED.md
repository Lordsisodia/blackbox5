# SSOT Task State: What Scouts Missed - queue.yaml Deep Dive

**Scout:** Architecture Analysis Agent (Follow-up)
**Date:** 2026-02-06
**Focus:** Hidden queue.yaml fields and inconsistencies

---

## Critical Findings: 7 Queue-Only Fields

The queue.yaml contains **7 fields that do not exist in task.md files**:

| Field | queue.yaml Location | task.md Equivalent | Issue |
|-------|---------------------|-------------------|-------|
| `priority_score` | All entries (e.g., 8.5, 12.0) | NONE | Calculated score only in queue |
| `roi` (nested object) | Lines 76-82, 96-102 | NONE | ROI metrics only in queue |
| `resource_type` | Lines 85, 105, 125 | NONE | Scheduling hint only in queue |
| `parallel_group` | Lines 86, 106, 126 | NONE | Execution grouping only in queue |
| `blockedBy` | Lines 83, 103, 123 | `**Depends On:**` (sometimes) | Dependency tracking only in queue |
| `blocks` | Lines 84, 104, 124 | NONE | Reverse dependencies only in queue |
| `type` | Lines 70, 90, 110 | `**Category:**` (inconsistent) | Task type only in queue |

**Impact:** These fields create a **shadow task management system** where critical scheduling and dependency data exists ONLY in queue.yaml.

---

## Field Name Mapping Inconsistencies

| Data | queue.yaml Field | task.md Field | Example |
|------|-----------------|---------------|---------|
| Time estimate | `estimated_minutes` | `**Estimated:**` or `**Estimated Effort:**` | "45" vs "45 minutes" |
| Creation date | - (implied) | `**Created:**` | Not in queue |
| Completion date | - (implied) | `**Completed:**` | Not in queue |
| Actual time | - (not tracked) | `**Actual:**` | Task files have this |
| Goal reference | `goal:` | `**Goal:**` | "IG-007" vs "**Goal:** IG-007" |

---

## Status Mismatches (Critical)

| Task ID | queue.yaml Status | task.md Status | Issue |
|---------|------------------|----------------|-------|
| TASK-ARCH-016 | `in_progress` (line 391) AND `pending` (line 435) | `pending` | **Same task appears TWICE** |
| TASK-ARCH-015-status-lifecycle | `in_progress` | No matching file | Orphaned queue entry |
| TASK-ARCH-016-agent-execution-flow | `in_progress` | No matching file | Orphaned queue entry |
| TASK-ARCH-012-mirror-candidates | `completed` | No matching file | Orphaned queue entry |

---

## Orphaned Queue Entries (5 found)

1. **TASK-ARCH-015-status-lifecycle** - Status: in_progress
2. **TASK-ARCH-016-agent-execution-flow** - Status: in_progress
3. **TASK-ARCH-012-mirror-candidates** - Status: completed
4. **TASK-STATUS-LIFECYCLE-ACTION-PLAN** - Status: in_progress
5. **ACTION-PLAN-youtube-pipeline** - Status: in_progress

---

## Data Type Inconsistencies

| Field | queue.yaml Type | task.md Type |
|-------|----------------|--------------|
| `estimated_minutes` | Integer (45) | String ("45 minutes") |
| `priority_score` | Float (8.5) | Not present |
| `blockedBy` | Array | Sometimes string |

---

## Priority Formula Duplication

The priority formula exists in **multiple places**:
- queue.yaml lines 16-24
- operations/skill-selection.yaml
- operations/estimation-guidelines.yaml

Formula: `priority_score = (impact / effort) * confidence`

---

## What Initial Scouts Missed

| Issue | Severity | Scouts Found? |
|-------|----------|---------------|
| 7 queue-only fields | HIGH | NO |
| TASK-ARCH-016 double entry | CRITICAL | Partial |
| Orphaned queue entries | HIGH | NO |
| Field name inconsistencies | MEDIUM | NO |
| Data type mismatches | MEDIUM | NO |
| Priority formula duplication | MEDIUM | NO |
| blockedBy/blocks only in queue | HIGH | NO |
