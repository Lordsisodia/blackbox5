# TASK-ARCH-008: Standardize Run Naming Convention - Results

**Status:** COMPLETED
**Completed:** 2026-02-04
**Goal:** IG-007

---

## Summary

Analyzed 198 run folders across BlackBox5 and established ISO datetime format as the naming standard for all future runs.

---

## Analysis Results

| Pattern | Count | Example | Status |
|---------|-------|---------|--------|
| Already standard | 13 | `run-20260204-033815` | ✅ Keep |
| Underscore separator | 10 | `run-20260131_192605` | 📝 Historical |
| Unix epoch | 28 | `run-1769861933` | 📝 Historical |
| Sequential | 143 | `run-0016` | 📝 Historical |
| Descriptive | 4 | `run-youtube-automation` | 📝 Historical |

**Total:** 198 run folders
**Already standard:** 13 (7%)
**Non-standard:** 185 (93%)

---

## Key Decision

**Do NOT rename historical runs.**

**Rationale:**
- 185 runs would need renaming
- References exist in tasks, docs, and STATE.yaml
- Risk of breaking historical records outweighs benefit
- Better to establish standard going forward

---

## Policy Established

1. **Historical runs (pre-2026-02-04):** Keep as-is
2. **New runs (post-2026-02-04):** Must use `run-YYYYMMDD-HHMMSS` format
3. **RALF loop:** Create new runs in standard format

---

## Standard Format

**Format:** `run-YYYYMMDD-HHMMSS[-description]`

**Examples:**
- `run-20260204-143052`
- `run-20260204-143052-youtube-automation`

**Benefits:**
- Sorts correctly alphabetically
- Human-readable at a glance
- No timezone ambiguity
- Easy to locate runs by date

---

## Deliverable

- ✅ `bin/standardize-run-names.py` - Reference migration script
- ✅ Naming convention documented
- ✅ Policy established for future runs
- ✅ No breaking changes to historical data
