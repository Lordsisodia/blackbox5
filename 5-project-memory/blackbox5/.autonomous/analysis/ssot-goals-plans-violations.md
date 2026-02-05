# SSOT Goals/Plans Violations Report

**Scout:** Architecture Analysis Agent
**Date:** 2026-02-06
**Status:** Complete

---

## Summary of Findings

Goal and plan data is duplicated across multiple locations, creating synchronization risks and inconsistencies.

---

## 1. GOAL STATUS DUPLICATION

**Primary Source:** `goals/active/*/goal.yaml` (canonical)

**Duplicated Locations:**

| Location | Duplicated Data | Inconsistency Risk |
|----------|-----------------|-------------------|
| `goals/INDEX.yaml` | status, progress, priority | HIGH - IG-008 shows "in_progress" in INDEX but "draft" in goal.yaml |
| `goals/goals.yaml` | status, priority | MEDIUM - IG-003/IG-005 marked "active" but merged |
| `STATE.yaml` | None directly, but references goals.yaml | LOW |
| `goals/active/*/timeline.yaml` | progress_delta, events | MEDIUM |

**Specific Inconsistencies Found:**

### IG-008 Status Mismatch:
- `goals/active/IG-008/goal.yaml`: `status: draft` (line 12)
- `goals/INDEX.yaml`: `status: in_progress` (line 121)
- `goals/INDEX.yaml`: `progress: 0%` (line 122) vs goal.yaml showing 75%

### IG-009 Status Mismatch:
- `goals/active/IG-009/goal.yaml`: `status: completed` (line 12)
- `goals/INDEX.yaml`: `status: in_progress` (line 130)
- `goals/INDEX.yaml`: `progress: 60%` (line 131) vs goal.yaml showing 100%

### Merged Goals Still Active:
- IG-003 and IG-005 marked as "active" in `goals.yaml` but listed as "merged" in `INDEX.yaml`

---

## 2. PLAN STATUS DUPLICATION

**Primary Source:** `plans/active/*/epic.md`

**Duplicated Locations:**

| Location | Duplicated Data | Risk |
|----------|-----------------|------|
| Plan's own epic.md | Status, progress | Canonical |
| Goal's goal.yaml | linked_plans references | MEDIUM - may be outdated |
| STATE.yaml | features.completed | HIGH - may not reflect actual plan state |

**Example:** `plans/active/hindsight-memory-implementation/epic.md`
- Shows `Status: MVP_COMPLETE`
- Goal IG-008 links to `PLAN-HINDSIGHT-001` but goal.yaml shows inconsistent progress

---

## 3. GOAL/PLAN/TASK LINKAGE DUPLICATION

**Linkage Chain:**
```
Goal (goal.yaml) -> Plan (epic.md) -> Task (task.md)
```

**Duplication Issues:**

### Bidirectional Links Not Synchronized:
- Goal links to plan in `goal.yaml` (e.g., IG-008 links to PLAN-HINDSIGHT-001)
- Plan links back to goal in `epic.md` (e.g., "Goal: IG-008")
- Task links to goal/plan in `task.md` frontmatter
- **Risk:** If one side changes, the other becomes orphaned

### Sub-goal Linkage Duplication:
- Goal has `sub_goals` with status/progress in `goal.yaml`
- Sub-goals may have their own task files
- Progress tracked in both places

### Task Status in Multiple Places:
- Task has its own `status` field in `task.md`
- Goal tracks `linked_tasks` with completion status
- Timeline tracks task events
- STATE.yaml tracks tasks

**Example from IG-008 goal.yaml:**
```yaml
linked_tasks:
  - TASK-HINDSIGHT-001 (completed)
  - TASK-HINDSIGHT-002 (completed)
```

But task file shows:
```yaml
status: pending  # MISMATCH!
```

---

## 4. PROGRESS TRACKING DUPLICATION

**Progress Stored In:**

| File | Progress Field | Example |
|------|----------------|---------|
| goal.yaml | `progress.percentage` | 75% |
| goal.yaml | `progress.by_sub_goal` | SG-006-1: 85% |
| INDEX.yaml | `progress` | 75% |
| timeline.yaml | `progress_delta` in events | Various |
| epic.md | Implementation table status | "COMPLETE" |

**Inconsistency Example - IG-006:**
- goal.yaml: `percentage: 75`
- INDEX.yaml: `progress: 75%`
- But sub-goal SG-006-4 shows 10% in goal.yaml vs potentially different in INDEX

---

## 5. TIMELINE DUPLICATION

**Each goal has its own timeline.yaml:**
- `goals/active/IG-001/timeline.yaml`
- `goals/active/IG-006/timeline.yaml`
- etc.

**Plus root timeline.yaml:**
- `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/timeline.yaml`

**Issue:** Events related to goals are logged in BOTH:
- The goal's specific timeline.yaml
- The root timeline.yaml

This creates synchronization risk.

---

## 6. CORE GOALS DUPLICATION

**Core goals defined in:**
1. `goals/core/core-goals.yaml` (canonical)
2. `goals/INDEX.yaml` (copied with metrics)
3. `goals/goals.yaml` (referenced in core_goals section)

**Inconsistency Risk:** Metrics in INDEX.yaml may not reflect actual core-goal.yaml state.

---

## Recommendations for SSOT

### 1. Goal Status SSOT
**Canonical Source:** `goals/active/{id}/goal.yaml`
- Remove status/progress from INDEX.yaml
- INDEX.yaml should be auto-generated from goal files only
- Add "last_synced" timestamp to show freshness

### 2. Plan Status SSOT
**Canonical Source:** `plans/active/{plan}/epic.md`
- STATE.yaml should reference, not duplicate
- Goals should link to plans but not store plan status

### 3. Task Status SSOT
**Canonical Source:** `tasks/active/{task}/task.md`
- Goals should reference tasks but not duplicate status
- Use a task query system to get actual status

### 4. Progress SSOT
**Canonical Source:** Calculate from sub-goals/tasks, store only in goal.yaml
- Remove progress from INDEX.yaml (generate dynamically)
- Single calculation method used everywhere

### 5. Timeline SSOT
**Canonical Source:** Root `timeline.yaml`
- Goal-specific timelines should be views/filters, not separate stores
- Or: goal timelines are canonical, root is aggregated view

### 6. Linkage Integrity
- Implement bidirectional link validation
- When a goal links to a plan, verify plan links back
- Report orphaned references

### 7. Automation
- Create a `bb5 sync` command that:
  - Reads all canonical sources
  - Detects inconsistencies
  - Updates derived files (INDEX.yaml, STATE.yaml references)
  - Reports mismatches for human review

---

## Critical Files Requiring Immediate Attention

1. `goals/INDEX.yaml` - Contains stale data
2. `goals/active/IG-008/goal.yaml` - Status should be "completed" or "in_progress", not "draft"
3. `goals/active/IG-009/goal.yaml` - Status mismatch with INDEX.yaml
