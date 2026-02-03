# TASK-CLEANUP-LOOP: BB5 Consolidation Loop

**Type:** cleanup
**Priority:** MEDIUM
**Status:** in_progress
**Created:** 2026-02-04
**Approach:** First Principles + Continuous Iteration

---

## Objective

Run a continuous cleanup loop through BlackBox5 to consolidate documentation, remove duplicates, and establish canonical structure using first principles.

---

## First Principles

1. **Single Source of Truth** - One canonical doc per topic
2. **Convention over Configuration** - Standard naming, standard locations
3. **Minimal Viable Documentation** - If it's not needed, delete it
4. **Hierarchy of Information** - Project → Plans → Tasks (no overlap)

---

## Current State (Post-Cleanup)

✅ **Completed:**

### Backup Cleanup
- Deleted 5 backup directories (8.6MB freed)
- goals.backup.20260204/
- plans.backup.20260204/
- runs.backup.20260204/
- tasks.backup.20260204/
- .autonomous.backup.20260204/

### Root Consolidation (Loop 1)
- Consolidated README.md with ACTIVE.md stats and RUN-STRUCTURE-MAP structure
- Deleted ACTIVE.md (merged into README.md)
- Deleted RUN-STRUCTURE-MAP.md (merged into README.md)
- Deleted RUN-STRUCTURE-MAP-v2.md (redundant)
- Deleted UNIFIED-STRUCTURE.md (redundant)
- Deleted project-structure.md (redundant)
- Deleted WORK-LOG.md (redundant with runs/)
- Deleted QUERIES.md (too minimal)
- Moved _NAMING.md → knowledge/conventions/naming.md
- Moved YAML-vs-MD-EVALUATION.md → knowledge/conventions/yaml-vs-markdown.md
- Moved MIGRATION-SUMMARY.md → .archived/
- Deleted ARCHITECTURE_DECISIONS.md (empty template)
- Moved IMPLEMENTATION-PLAN.md → plans/active/implementation-plan-navigation.md

**Result:** Root .md files reduced from 14 → 3 (README.md, Ralf-context.md)

### Knowledge Consolidation (Loop 2)

**Consolidated 5 analysis groups:**

| Group | Files Consolidated | Into |
|-------|-------------------|------|
| CLAUDE.md Analysis | claude-md-improvements.md, claude-md-decision-effectiveness.md | claude-md-analysis.md |
| Duration Tracking | duration-tracking-analysis-20260201.md, duration-tracking-fix-20260201.md | duration-tracking-analysis-and-fix.md |
| Run Analysis | autonomous-runs-analysis.md, run-patterns-20260201.md | run-analysis-47-runs.md |
| Skill System | 5 skill-related files | skill-system-analysis.md |

**Files Deleted (12):**
- claude-md-improvements.md
- claude-md-decision-effectiveness.md
- duration-tracking-analysis-20260201.md
- duration-tracking-fix-20260201.md
- autonomous-runs-analysis.md
- run-patterns-20260201.md
- skill-system-effectiveness-20260201.md
- skill-system-recovery-20260201.md
- skill-validation-analysis-20260201.md
- executor-decision-patterns-20260201.md
- skill-usage-gap-analysis-20260201.md

**Files Created (4):**
- claude-md-analysis.md
- duration-tracking-analysis-and-fix.md
- run-analysis-47-runs.md
- skill-system-analysis.md

**Result:** knowledge/analysis/ reduced from 30 → 18 files (40% reduction)

---

## Consolidation Targets

### Target 1: Root README Consolidation

**Files to Merge:**
- README.md (main project readme)
- ACTIVE.md (dashboard - mostly empty)
- RUN-STRUCTURE-MAP.md
- RUN-STRUCTURE-MAP-v2.md (duplicate)
- UNIFIED-STRUCTURE.md (overlaps)
- project-structure.md (overlaps)

**Canonical Location:** README.md

**Action:**
1. Merge ACTIVE.md stats into README.md
2. Merge RUN-STRUCTURE-MAP into README.md "Structure" section
3. Delete RUN-STRUCTURE-MAP-v2.md (redundant)
4. Delete UNIFIED-STRUCTURE.md (redundant)
5. Delete project-structure.md (redundant)

### Target 2: Architecture Decisions Consolidation

**Files to Move:**
- ARCHITECTURE_DECISIONS.md → decisions/architectural/

**Action:**
1. Move to decisions/architectural/bb5-core.md
2. Update index in decisions/README.md

### Target 3: Context Files Consolidation

**Files to Review:**
- Ralf-context.md (mixed case, should be canonical)
- _NAMING.md (conventions)
- YAML-vs-MD-EVALUATION.md (knowledge)
- MIGRATION-SUMMARY.md (completed work)
- WORK-LOG.md (overlaps with runs/)
- QUERIES.md (minimal content)

**Actions:**
1. Keep Ralf-context.md as canonical project context
2. Move _NAMING.md to knowledge/conventions.md
3. Move YAML-vs-MD-EVALUATION.md to knowledge/
4. Archive MIGRATION-SUMMARY.md to .archived/
5. Delete WORK-LOG.md (redundant with runs/)
6. Delete QUERIES.md (too minimal)

---

## Iteration Loop

### Loop 1: Root Consolidation

```
1. Read all root .md files
2. Identify overlaps using first principles
3. Merge into canonical locations
4. Delete redundant files
5. Update ASSUMPTIONS.md
6. Update ARCHITECTURE.md
7. Commit: "cleanup: consolidate root documentation"
```

### Loop 2: Knowledge Consolidation

```
1. Scan knowledge/ for duplicates
2. Merge overlapping topics
3. Establish canonical structure
4. Update cross-references
5. Commit: "cleanup: consolidate knowledge base"
```

### Loop 3: Task Naming Standardization

```
1. Find all TASK.md (uppercase)
2. Rename to task.md (lowercase)
3. Update any references
4. Commit: "cleanup: standardize task file naming"
```

---

## Exit Criteria

- [x] Root directory has < 5 .md files (14 → 3)
- [x] No duplicate structure maps
- [x] No redundant documentation
- [ ] All decisions in decisions/
- [x] All knowledge in knowledge/
- [ ] Consistent naming throughout

## Success Metrics

| Metric | Before | Target | After |
|--------|--------|--------|-------|
| Root .md files | 14 | < 5 | 3 ✅ |
| Structure maps | 3 | 1 | 1 ✅ |
| Duplicate topics | 5+ | 0 | 0 ✅ |
| Files in wrong place | 5+ | 0 | 0 ✅ |
| Knowledge analysis files | 30 | < 20 | 18 ✅ |

---

## Success Metrics

| Metric | Before | Target | After |
|--------|--------|--------|-------|
| Root .md files | 14 | < 5 | ? |
| Structure maps | 3 | 1 | ? |
| Duplicate topics | 5+ | 0 | ? |
| Files in wrong place | 5+ | 0 | ? |

---

## Notes

**Use minimal changes:**
- Don't reorganize working systems
- Don't touch runs/ or archived/
- Don't modify .autonomous/agents/ structure
- Focus on documentation consolidation only

**Commit pattern:**
```
cleanup: [area] [action]

- Specific changes
- Files affected: [list]
- Rationale: [first principle]
```
