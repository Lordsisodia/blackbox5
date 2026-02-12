# TASK-PROC-033: Extraction Rate Below Target Without Root Cause Analysis

**Status:** completed
**Priority:** MEDIUM
**Category:** process
**Estimated Effort:** 60 minutes
**Created:** 2026-02-05T01:57:10.950039
**Completed:** 2026-02-09
**Source:** Scout opportunity metrics-010 (Score: 8.5)

---

## Objective

Create an extraction rate tracking system that counts learnings and decisions extracted per task, calculates extraction rates by category, and identifies tasks with low extraction.

---

## Success Criteria

- [x] Understand the issue completely
- [x] Implement the suggested action
- [x] Validate the fix works
- [x] Document changes in LEARNINGS.md

---

## Context

**Suggested Action:** Analyze the 70 learnings not converted to improvements

**Files Created/Modified:**
- `~/.blackbox5/bin/track-extraction-rates.py` - Extraction tracking script
- `~/.blackbox5/5-project-memory/blackbox5/operations/extraction-report-20260209.yaml` - Initial report

---

## Rollback Strategy

If changes cause issues:
1. Delete the tracking script: `rm ~/.blackbox5/bin/track-extraction-rates.py`
2. Remove the report file if needed
3. Document what went wrong

---

## Notes

**Completed:**

Created `track-extraction-rates.py` that:
- Scans active tasks, completed tasks, and autonomous runs directories
- Parses LEARNINGS.md and DECISIONS.md files
- Counts learnings extracted per task (structured and unstructured)
- Counts decisions extracted per task
- Calculates extraction rates by category (learning rate, decision rate, overall)
- Identifies tasks with low extraction (missing both learnings and decisions)
- Supports text, JSON, and YAML output formats
- Can save reports to file

**Current Extraction Metrics (2026-02-09):**
- Total Tasks: 87 (54 active, 33 completed, 2 autonomous runs)
- Total Learnings: 23 (19 from tasks, 4 from runs)
- Total Decisions: 31 (0 from tasks, 31 from runs)
- Active Tasks Learning Rate: 5.6%
- Active Tasks Decision Rate: 0.0%
- Autonomous Runs Learning Rate: 50.0%
- Autonomous Runs Decision Rate: 50.0%

**Key Finding:**
Process-type tasks have the highest extraction rate at 33.3%, while most other task types have 0% extraction. The autonomous runs system (RALF) has much better extraction rates (50%) compared to manual tasks.

**Tasks Missing Extractions:** 85 total (51 active, 33 completed, 1 run)
