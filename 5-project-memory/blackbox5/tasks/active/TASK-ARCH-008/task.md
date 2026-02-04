# TASK-ARCH-008: Standardize Run Naming Convention

**Status:** completed
**Priority:** HIGH
**Created:** 2026-02-04
**Completed:** 2026-02-04
**Goal:** IG-007
**Plan:** PLAN-ARCH-001

---

## Objective

Establish ISO datetime format (`run-YYYYMMDD-HHMMSS`) as the standard for run folder naming.

---

## Success Criteria

- [x] Inventory all run folders
- [x] Identify naming patterns in use
- [x] Create migration script
- [x] Document the standard
- [x] Establish policy for historical runs

---

## Analysis Results

**Found 198 run folders across the project:**

| Pattern | Count | Example | Action |
|---------|-------|---------|--------|
| Already standard | 13 | `run-20260204-033815` | ✅ Keep |
| Underscore separator | 10 | `run-20260131_192605` | 📝 Standard going forward |
| Unix epoch | 28 | `run-1769861933` | 📝 Standard going forward |
| Sequential | 143 | `run-0016` | 📝 Standard going forward |
| Descriptive | 4 | `run-youtube-automation` | 📝 Standard going forward |

---

## Decision: Don't Rename Historical Runs

**Reasoning:**
- 185 runs would need renaming
- Multiple references in tasks, docs, and STATE.yaml would break
- Risk outweighs benefit for historical data

**Policy Established:**
1. **Historical runs (pre-2026-02-04):** Keep as-is
2. **New runs (post-2026-02-04):** Must use `run-YYYYMMDD-HHMMSS` format
3. **RALF loop and hooks:** Updated to create runs in standard format

---

## Standard Format

**Format:** `run-YYYYMMDD-HHMMSS[-description]`

**Examples:**
- `run-20260204-143052` = Feb 4, 2026, 14:30:52
- `run-20260204-143052-youtube` = With descriptive suffix

**Benefits:**
- Sorts correctly alphabetically
- Human-readable at a glance
- No timezone ambiguity
- Easy to locate runs by date

---

## Deliverable

- ✅ `bin/standardize-run-names.py` - Migration script (for reference)
- ✅ Naming standard documented
- ✅ Policy established for future runs
- ✅ No breaking changes to historical data
