# PLAN.md: BB5 Consolidation Loop

**Task ID:** TASK-CLEANUP-LOOP
**Status:** Planning
**Priority:** MEDIUM
**Created:** 2026-02-04
**Estimated Effort:** 4-6 hours
**Approach:** First Principles + Continuous Iteration

---

## 1. First Principles Analysis

### Why Is Consolidation Necessary?

1. **Documentation Sprawl**: 14 root-level markdown files with overlapping content
2. **Duplicate Information**: Same structure documented in multiple places
3. **Knowledge Fragmentation**: Analysis scattered across 30+ files
4. **Naming Inconsistencies**: Mixed case conventions (TASK.md vs task.md)
5. **Maintenance Burden**: Updates require changes in multiple locations

### What Happens Without Consolidation?

| Problem | Impact | Severity |
|---------|--------|----------|
| Conflicting information | Users don't know which doc is correct | High |
| Wasted storage | 8.6MB+ in backup directories alone | Medium |
| Onboarding friction | New agents overwhelmed by choices | High |
| Update drift | Docs become stale | Medium |
| Search difficulty | Finding information takes longer | Medium |

### How Should Documentation Be Organized?

**First Principles:**
1. **Single Source of Truth**: One canonical doc per topic
2. **Convention over Configuration**: Standard naming, standard locations
3. **Minimal Viable Documentation**: If it's not needed, delete it
4. **Hierarchy of Information**: Project -> Plans -> Tasks (no overlap)

---

## 2. Current State Assessment

### Root Directory Cleanup (Completed)

**Before:** 14 .md files
**After:** 3 .md files (README.md, Ralf-context.md)

**Consolidated:**
- ACTIVE.md -> merged into README.md
- RUN-STRUCTURE-MAP.md -> merged into README.md
- RUN-STRUCTURE-MAP-v2.md -> deleted (redundant)
- UNIFIED-STRUCTURE.md -> deleted (redundant)
- project-structure.md -> deleted (redundant)
- WORK-LOG.md -> deleted (redundant with runs/)
- QUERIES.md -> deleted (too minimal)
- _NAMING.md -> moved to knowledge/conventions/naming.md
- YAML-vs-MD-EVALUATION.md -> moved to knowledge/conventions/yaml-vs-markdown.md
- MIGRATION-SUMMARY.md -> archived
- ARCHITECTURE_DECISIONS.md -> deleted (empty template)
- IMPLEMENTATION-PLAN.md -> moved to plans/active/

### Knowledge Directory Cleanup (Completed)

**Before:** 30 analysis files
**After:** 18 analysis files (40% reduction)

**Consolidated Groups:**
- CLAUDE.md Analysis (2 files -> 1)
- Duration Tracking (2 files -> 1)
- Run Analysis (2 files -> 1)
- Skill System (5 files -> 1)

### Task Naming Standardization (Completed)

**Before:** 2 uppercase TASK.md files
**After:** 0 uppercase (109+ tasks use lowercase task.md)

---

## 3. Proposed Solution

### Consolidation Framework

**Three-Phase Approach:**

```
Phase 1: Identify Duplicates
  - Scan for overlapping content
  - Map document relationships
  - Identify canonical sources

Phase 2: Merge and Redirect
  - Merge content into canonical location
  - Add redirects/notes in old locations
  - Update cross-references

Phase 3: Validate and Clean
  - Verify no information lost
  - Delete redundant files
  - Update indexes
```

### Consolidation Rules

**Keep if:**
- Unique information not found elsewhere
- Actively maintained and referenced
- Follows naming conventions

**Merge if:**
- Overlaps with another document
- Part of a series on same topic
- Complementary content

**Delete if:**
- Completely redundant
- Outdated and superseded
- Empty or placeholder
- Backup/temporary files

---

## 4. Implementation Plan

### Phase 1: Root Consolidation (Completed)

**Actions:**
1. Read all root .md files
2. Identify overlaps using first principles
3. Merge into canonical locations
4. Delete redundant files
5. Update ASSUMPTIONS.md
6. Commit: "cleanup: consolidate root documentation"

**Results:**
- 14 -> 3 root .md files
- 8.6MB freed from backup deletion
- Clear hierarchy established

### Phase 2: Knowledge Consolidation (Completed)

**Actions:**
1. Scan knowledge/ for duplicates
2. Group related analysis files
3. Merge overlapping topics
4. Establish canonical structure
5. Update cross-references
6. Commit: "cleanup: consolidate knowledge base"

**Results:**
- 30 -> 18 analysis files
- 4 consolidated analysis documents created
- Clearer navigation

### Phase 3: Task Naming Standardization (Completed)

**Actions:**
1. Find all TASK.md files (case-sensitive)
2. Rename to task.md
3. Check for references
4. Update any hardcoded paths
5. Commit: "cleanup: standardize task file naming"

**Results:**
- 109+ tasks use consistent naming
- No references broken

### Phase 4: Remaining Consolidation Targets (Pending)

**Target 1: Decisions Directory**
- Move ARCHITECTURE_DECISIONS.md content
- Ensure all decisions in decisions/
- Update decisions/README.md index

**Target 2: Operations Documentation**
- Consolidate operations/.docs/
- Merge overlapping guides
- Create operations/README.md

**Target 3: Agent Documentation**
- Consolidate agent setup guides
- Merge overlapping instructions
- Create .autonomous/agents/README.md

---

## 5. Success Criteria

- [x] Root directory has < 5 .md files (14 -> 3)
- [x] No duplicate structure maps
- [x] No redundant documentation
- [ ] All decisions in decisions/
- [x] All knowledge in knowledge/
- [x] Consistent naming throughout (109+ task files)
- [ ] Operations documentation consolidated
- [ ] Agent documentation consolidated

---

## 6. Estimated Timeline

| Phase | Duration | Status |
|-------|----------|--------|
| Phase 1: Root | 1 hour | Completed |
| Phase 2: Knowledge | 2 hours | Completed |
| Phase 3: Naming | 30 min | Completed |
| Phase 4: Decisions | 1 hour | Pending |
| Phase 5: Operations | 1 hour | Pending |
| Phase 6: Agents | 1 hour | Pending |
| **Total** | **~6 hours** | **50% Complete** |

---

## 7. Rollback Strategy

If changes cause issues:

1. **Immediate:** Restore from git history
2. **Short-term:** Keep backups in .archived/ until verified
3. **Long-term:** Document what was consolidated where

**Recovery Commands:**
```bash
# Restore specific file
git checkout HEAD~1 -- path/to/file.md

# Restore from archived
mv .archived/filename.md original/location/
```

---

## 8. Files Modified/Created

### Deleted Files (Root)

| File | Reason | Size |
|------|--------|------|
| ACTIVE.md | Merged into README.md | 2KB |
| RUN-STRUCTURE-MAP.md | Merged into README.md | 5KB |
| RUN-STRUCTURE-MAP-v2.md | Redundant | 4KB |
| UNIFIED-STRUCTURE.md | Redundant | 3KB |
| project-structure.md | Redundant | 2KB |
| WORK-LOG.md | Redundant with runs/ | 1KB |
| QUERIES.md | Too minimal | 0.5KB |
| ARCHITECTURE_DECISIONS.md | Empty template | 0.5KB |

### Moved Files

| File | From | To |
|------|------|-----|
| _NAMING.md | root | knowledge/conventions/naming.md |
| YAML-vs-MD-EVALUATION.md | root | knowledge/conventions/yaml-vs-markdown.md |
| MIGRATION-SUMMARY.md | root | .archived/ |
| IMPLEMENTATION-PLAN.md | root | plans/active/ |

### Consolidated Files (Knowledge)

| Group | Files | Into |
|-------|-------|------|
| CLAUDE.md | 2 files | claude-md-analysis.md |
| Duration | 2 files | duration-tracking-analysis-and-fix.md |
| Run Analysis | 2 files | run-analysis-47-runs.md |
| Skill System | 5 files | skill-system-analysis.md |

---

## 9. Commit Pattern

```
cleanup: [area] [action]

- Specific changes
- Files affected: [list]
- Rationale: [first principle]
```

**Examples:**
```
cleanup: root consolidate documentation

- Merge ACTIVE.md into README.md
- Delete RUN-STRUCTURE-MAP-v2.md (redundant)
- Move _NAMING.md to knowledge/
- Rationale: Single source of truth

cleanup: knowledge consolidate analysis files

- Merge 5 skill files into skill-system-analysis.md
- Delete duplicate duration tracking files
- Rationale: Convention over configuration
```

---

*Plan created: 2026-02-06*
*50% complete - Phases 1-3 done, 4-6 pending*
