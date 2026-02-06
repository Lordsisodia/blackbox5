# TASK-ARCH-007: Consolidate Task Systems

**Status:** completed
**Priority:** CRITICAL
**Created:** 2026-02-04
**Estimated:** 90 minutes
**Actual:** 60 minutes
**Goal:** IG-007
**Plan:** PLAN-ARCH-001

---

## Objective

Standardize task naming across BlackBox5 by migrating non-standard task names to the `TASK-{PREFIX}-{NUMBER}` format.

---

## Success Criteria

- [x] Inventory all task naming patterns
- [x] Rename active non-standard tasks
- [x] Update goal references
- [x] Document naming standard
- [x] Validation passes

---

## Naming Patterns Found

| Pattern | Format | Action |
|---------|--------|--------|
| Standard | `TASK-{PREFIX}-{NUMBER}` | Keep |
| Timestamp | `TASK-{timestamp}` | Migrated |
| Descriptive | `{NAME}` | Migrated |
| Sequential | `TASK-{001-006}` | Keep (historical) |

---

## Migrations Completed

24 tasks renamed to standard format:
- `AGENT-SYSTEM-AUDIT` → `TASK-AUTO-010-agent-system-audit`
- `TASK-1769978192` → `TASK-ARCH-011-agent-execution-flow`
- etc.

---

## Standard Naming Convention

**Format:** `TASK-{PREFIX}-{NUMBER}-{description}`

**Prefixes:**
- `ARCH` - Architecture
- `DEV` - Development
- `AUTO` - Autonomous system
- `DOCS` - Documentation

---

## Deliverable

- 24 tasks renamed
- Goal references updated
- Validation passes
- Naming convention documented
