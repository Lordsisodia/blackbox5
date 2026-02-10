# ASSUMPTIONS.md - Cleanup Loop

**Task:** TASK-CLEANUP-LOOP
**Date:** 2026-02-04

---

## First Principles Applied

### 1. Single Source of Truth
- **Assumption:** One canonical document per topic prevents drift
- **Applied:** Merged 6 structure-related files into README.md
- **Rationale:** Multiple structure maps (RUN-STRUCTURE-MAP, UNIFIED-STRUCTURE, project-structure) created confusion

### 2. Convention over Configuration
- **Assumption:** Standard naming reduces cognitive load
- **Applied:** Moved _NAMING.md to knowledge/conventions/naming.md
- **Rationale:** Underscore prefix is non-standard; conventions belong in knowledge/

### 3. Minimal Viable Documentation
- **Assumption:** If not needed, delete it
- **Applied:** Deleted WORK-LOG.md, QUERIES.md, ARCHITECTURE_DECISIONS.md
- **Rationale:** WORK-LOG redundant with runs/, QUERIES too minimal, ADR was empty template

### 4. Hierarchy of Information
- **Assumption:** Project → Plans → Tasks with no overlap
- **Applied:** Moved IMPLEMENTATION-PLAN.md to plans/active/
- **Rationale:** Plans don't belong in root; they go in plans/

---

## Cleanup Decisions

### Deleted Files (10)
| File | Rationale |
|------|-----------|
| ACTIVE.md | Merged into README.md Quick Stats section |
| RUN-STRUCTURE-MAP.md | Merged into README.md Run Structure section |
| RUN-STRUCTURE-MAP-v2.md | Duplicate of RUN-STRUCTURE-MAP |
| UNIFIED-STRUCTURE.md | Overlaps with README.md structure |
| project-structure.md | Overlaps with README.md |
| WORK-LOG.md | Redundant with runs/ directory |
| QUERIES.md | Too minimal (2 lines) |
| ARCHITECTURE_DECISIONS.md | Empty template, no actual decisions |

### Moved Files (4)
| From | To | Rationale |
|------|-----|-----------|
| _NAMING.md | knowledge/conventions/naming.md | Standard location for conventions |
| YAML-vs-MD-EVALUATION.md | knowledge/conventions/yaml-vs-markdown.md | Knowledge belongs in knowledge/ |
| MIGRATION-SUMMARY.md | .archived/migration-summary.md | Completed work goes to archive |
| IMPLEMENTATION-PLAN.md | plans/active/implementation-plan-navigation.md | Plans belong in plans/ |

### Consolidated Files (3 → 1)
- README.md now contains:
  - Original README content
  - ACTIVE.md Quick Stats
  - RUN-STRUCTURE-MAP run structure documentation

---

## Result

**Before:** 14 .md files in root
**After:** 3 .md files in root (README.md, Ralf-context.md)

**Target achieved:** < 5 root .md files
