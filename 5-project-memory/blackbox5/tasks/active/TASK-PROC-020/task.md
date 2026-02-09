# TASK-PROC-020: Duplicate Task Detection

**Status:** completed
**Priority:** MEDIUM
**Category:** process
**Estimated Effort:** 60 minutes
**Created:** 2026-02-05T01:57:10.949971
**Completed:** 2026-02-09
**Source:** Scout opportunity process-006 (Score: 10.5)

---

## Objective

Detect and prevent duplicate tasks being created in the BlackBox5 task management system.

---

## Success Criteria

- [x] Understand the issue completely
- [x] Implement the suggested action
- [x] Validate the fix works
- [x] Document changes in LEARNINGS.md

---

## Context

**Suggested Action:** Implement duplicate detection check in task creation workflow

**The Problem:**
Multiple tasks exist for the same work. For example:
- `TASK-AUTO-021-persistent-memory` and `TASK-MEMORY-001-improve-persistent-memory` have identical content
- `TASK-1769978192` and `TASK-ARCH-016-agent-execution-flow` have exact same titles
- `TASK-1738375000` and `TASK-DEV-010-cli-interface-f016` are duplicates

**Files Created/Modified:**
- `/Users/shaansisodia/.blackbox5/bin/detect-duplicate-tasks.py` - Duplicate detection script
- `/Users/shaansisodia/.blackbox5/bin/bb5-tools/bb5-create` - Added duplicate check to task creation

---

## Implementation

### 1. Duplicate Detection Script

Created `/Users/shaansisodia/.blackbox5/bin/detect-duplicate-tasks.py` with the following features:

**Detection Algorithms:**
- Exact title match (after normalization)
- High title similarity (>=85% using difflib.SequenceMatcher)
- Medium title similarity (>=70%) + objective similarity (>=75%)
- Content similarity for shorter tasks (>=80%)

**Usage:**
```bash
# Check if a new task would be a duplicate
detect-duplicate-tasks.py --check "Task Title"

# Scan all tasks for duplicates
detect-duplicate-tasks.py --scan

# Generate full report
detect-duplicate-tasks.py --report
```

### 2. Integration with bb5 task:create

Modified `bb5-create` to run duplicate detection before creating a new task:
- Automatically checks for duplicates when running `bb5 task:create "Task Name"`
- Shows warning with matching tasks and confidence scores
- Prompts user to confirm before creating potential duplicates

### 3. Detection Report

Generated report showing 225 tasks scanned with 68 potential duplicates found.
See `duplicate-report.txt` for full details.

**Top duplicates by confidence:**
1. 100% - TASK-1769978192 ↔ TASK-ARCH-016-agent-execution-flow (exact title)
2. 100% - TASK-1738375000 ↔ TASK-DEV-010-cli-interface-f016 (exact title)
3. 100% - TASK-AUTO-021-persistent-memory ↔ TASK-MEMORY-001-improve-persistent-memory (exact content)

---

## Rollback Strategy

If changes cause issues:
1. Remove duplicate detection block from bb5-create (lines 232-260)
2. Delete detect-duplicate-tasks.py script
3. Document what went wrong
4. Update this task with learnings

---

## Notes

**Detection Algorithm Summary:**

1. **Title Normalization:**
   - Remove task ID prefixes (TASK-XXX:)
   - Remove common prefixes (ACTION PLAN:, PLAN:, TASK:)
   - Convert to lowercase
   - Remove special characters
   - Normalize whitespace

2. **Similarity Scoring:**
   - Uses Python's difflib.SequenceMatcher for string comparison
   - Weighted combination of title and objective similarity
   - Content comparison for short tasks (<2000 chars)

3. **Thresholds:**
   - Exact match: 100% (normalized titles identical)
   - High confidence: >=85% title similarity
   - Medium confidence: >=70% title + >=75% objective

**Recommendations for Cleaning Up Existing Duplicates:**
1. Review the 68 potential duplicates in duplicate-report.txt
2. For pairs where one is completed: close the pending one as duplicate
3. For pairs where both are pending: merge or pick the more detailed one
4. Consider archiving completed duplicates to reduce noise
