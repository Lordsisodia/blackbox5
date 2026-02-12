# TASK-INFR-010: Learning Index Shows Zero Learnings Despite 80+ Claimed

**Status:** completed
**Priority:** HIGH
**Category:** infrastructure
**Estimated Effort:** 60 minutes
**Created:** 2026-02-05T01:57:10.949919
**Completed:** 2026-02-12T16:21:00.000000Z
**Source:** Scout opportunity metrics-003 (Score: 13.5)

---

## Objective

Debug and fix the learning_extractor.py to properly extract and index learnings from task runs.

---

## Success Criteria

- [x] Understand the issue completely
- [x] Implement the suggested action
- [x] Validate the fix works
- [x] Document changes in LEARNINGS.md

---

## Root Cause Analysis

**Issue:** Learning index showed 0 learnings despite 5,193 run directories existing.

**Root Causes:**

1. **Hardcoded macOS path in learning_extractor.py:**
   - Line 87: `/Users/shaansisodia/.blackbox5/...`
   - Line 817: Default runs directory also hardcoded to macOS path
   - Script was trying to save to non-existent path on VPS

2. **Missing LEARNINGS.md extraction:**
   - Script only parsed THOUGHTS.md, DECISIONS.md, and RESULTS.md
   - LEARNINGS.md files contained actual learnings (e.g., run-20260210_041851 had 12 learnings)
   - Most structured learnings are stored in LEARNINGS.md format

---

## Solution Implemented

### Fix 1: Environment-Aware Path Resolution

**File:** `/opt/blackbox5/5-project-memory/blackbox5/.autonomous/memory/extraction/learning_extractor.py`

**Changes:**
1. Updated `__init__()` to detect environment and use correct paths
2. Updated main() backfill to use environment-aware defaults

**Before:**
```python
if index_path is None:
    self.index_path = Path("/Users/shaansisodia/.blackbox5/...")
```

**After:**
```python
if index_path is None:
    bb5_path = Path("/opt/blackbox5")
    if bb5_path.exists():
        self.index_path = bb5_path / "5-project-memory/blackbox5/memory/insights/learning-index.yaml"
    else:
        # Fallback to macOS dev path
        self.index_path = Path("/Users/shaansisodia/.blackbox5/...")
```

### Fix 2: LEARNINGS.md Extraction

**Added Method:** `_extract_from_learnings()`

**Features:**
- Extracts numbered sections (## N. Title)
- Parses "Finding:" and "Details:" fields
- Auto-detects learning type (pattern, bugfix, optimization, insight)
- Auto-detects category (technical, process, architectural, operational)
- Handles alternative unnumbered section format
- Extracts relevant tags

**Pattern Example:**
```markdown
## 1. Hook Development Pattern

**Finding:** BB5 hooks follow a consistent pattern for JSON input/output.

**Details:**
- Read JSON from stdin using `json.load(sys.stdin)`
- Add fields to input dict (e.g., `logged_at`)
- ...
```

### Fix 3: Backfill All Runs

**Command:**
```bash
cd /opt/blackbox5
python3 5-project-memory/blackbox5/.autonomous/memory/extraction/learning_extractor.py --backfill
```

**Results:**
- Processed 5,193 run directories
- Extracted 26 new learnings
- Total index: 37 learnings (11 test + 26 new)

---

## Validation

**Health Check Before Fix:**
```
Status: WARNING
Total learnings: 0
Issues: No learnings in index
```

**Health Check After Fix:**
```
Status: HEALTHY
Total learnings: 37
Types:
  - insight: 22
  - decision: 12
  - pattern: 2
  - bugfix: 1
Categories:
  - technical: 33
  - process: 2
  - architectural: 2
```

---

## Context

**Suggested Action:** Debug learning_extractor.py to identify why learnings are not being indexed

**Files to Check/Modify:**
- `/opt/blackbox5/5-project-memory/blackbox5/.autonomous/memory/extraction/learning_extractor.py` (FIXED)
- `/opt/blackbox5/5-project-memory/blackbox5/memory/insights/learning-index.yaml` (POPULATED)

---

## Rollback Strategy

If changes cause issues:
1. Revert to previous state using git
2. Document what went wrong
3. Update this task with learnings

---

## Notes

_Add notes as you work on this task_
