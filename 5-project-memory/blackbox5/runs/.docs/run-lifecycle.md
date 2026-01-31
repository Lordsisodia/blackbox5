# Run Lifecycle Documentation

**Date:** 2026-02-01
**Purpose:** Document the complete lifecycle of RALF execution runs

---

## Overview

RALF execution runs follow a defined lifecycle from creation to archival. This document describes each stage and the criteria for progression.

---

## Lifecycle Stages

### 1. Active

**Location:** `runs/active/`

**Description:**
Runs that are currently being executed by RALF-Executor. These runs are in progress and have not yet completed their task.

**Entry Criteria:**
- Task claimed from `tasks/active/`
- Run directory created with timestamp
- THOUGHTS.md initialized

**Exit Criteria:**
- Task execution completes (success, failure, or partial)
- Required documentation files created
- Changes committed

**Files Present:**
- THOUGHTS.md (execution log)
- DECISIONS.md (decisions made)
- RESULTS.md (outcomes)
- LEARNINGS.md (insights captured)
- ASSUMPTIONS.md (assumptions made)
- State files (JSON/YAML)

---

### 2. Completed

**Location:** `runs/completed/`

**Description:**
Runs that have finished execution but are awaiting analysis. These runs have all required documentation but have not yet been reviewed for patterns or insights.

**Entry Criteria:**
- Task marked complete, failed, partial, or blocked
- All required documentation files present
- Task file moved to `tasks/completed/`
- Changes committed and pushed

**Exit Criteria:**
- Run analyzed for patterns
- Insights extracted and documented
- Ready for archival

**Duration:**
- Typically 1-7 days before archival
- Depends on analysis schedule

---

### 3. Archived

**Location:** `runs/archived/`

**Description:**
Runs that have been analyzed and are preserved for historical reference. These runs contribute to system improvement through pattern analysis.

**Entry Criteria:**
- Run fully documented
- Analysis completed (patterns extracted)
- No longer needed for active reference

**Retention:**
- Indefinite retention for historical analysis
- Used for first principles reviews (every 5 runs)
- Source of continuous improvement insights

---

## State Transitions

```
┌─────────┐    Execution     ┌───────────┐    Analysis     ┌──────────┐
│  Active │ ───────────────→ │ Completed │ ──────────────→ │ Archived │
│         │    Complete      │           │    Complete     │          │
└─────────┘                  └───────────┘                 └──────────┘
     │                            │                            │
     │ Create run dir             │ Verify docs                  │ Store
     │ Write THOUGHTS.md          │ Pattern analysis             │ Historical
     │ Execute task               │ Extract learnings            │ Reference
     │ Write RESULTS.md           │ Update metrics               │
     │ Commit changes             │ Move to archived             │
```

---

## Current State

**As of 2026-02-01:**

| Stage | Count | Location |
|-------|-------|----------|
| Active | 0 | `runs/active/` |
| Completed | 0 | `runs/completed/` |
| Archived | 47 | `runs/archived/` |
| **Total** | **47** | - |

---

## Archival Process

### When to Archive

1. **Time-based:** Runs older than 7 days in completed/
2. **Analysis-based:** After pattern analysis is documented
3. **Volume-based:** When completed/ exceeds 10 runs

### Archival Steps

1. Verify all required files exist:
   ```bash
   for run in runs/completed/*/; do
     [ -f "$run/THOUGHTS.md" ] && \
     [ -f "$run/DECISIONS.md" ] && \
     [ -f "$run/RESULTS.md" ] && \
     [ -f "$run/LEARNINGS.md" ]
   done
   ```

2. Move to archived:
   ```bash
   mv runs/completed/run-name runs/archived/
   ```

3. Update STATE.yaml counts

4. Commit changes:
   ```bash
   git add STATE.yaml
   git commit -m "Archive runs: moved X runs to archived/"
   ```

---

## File Requirements by Stage

### Minimum Required Files

| File | Active | Completed | Archived |
|------|--------|-----------|----------|
| THOUGHTS.md | Required | Required | Required |
| RESULTS.md | Required | Required | Required |
| DECISIONS.md | Required | Required | Required |
| LEARNINGS.md | Optional | Required | Required |
| ASSUMPTIONS.md | Optional | Optional | Optional |
| State files | Required | Required | Required |

---

## Related Documentation

- [Autonomous Runs Analysis](../knowledge/analysis/autonomous-runs-analysis.md)
- [Run Patterns 2026-02-01](../knowledge/analysis/run-patterns-20260201.md)
- [STATE.yaml](../STATE.yaml) - Current run counts
- [DUAL-RALF-ARCHITECTURE.md](../.autonomous/DUAL-RALF-ARCHITECTURE.md) - System architecture

---

## Maintenance

**Review Schedule:**
- Weekly: Check completed/ for runs ready to archive
- Monthly: Verify archived run integrity
- Quarterly: Analyze archived runs for system improvements

**Last Updated:** 2026-02-01
