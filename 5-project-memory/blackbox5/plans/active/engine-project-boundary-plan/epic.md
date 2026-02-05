# Plan: Engine/Project Boundary Restructuring

**Plan ID:** PLAN-ARCH-ENGINE-001
**Goal:** IG-006 - Restructure BlackBox5 Architecture for Clarity
**Sub-Goal:** SG-006-1 - Consolidate .autonomous folders
**Status:** in_progress
**Created:** 2026-02-06
**Target Completion:** 2026-02-20

---

## Overview

This plan addresses the structural issue where the boundary between `2-engine/` (standardized across all projects) and `5-project-memory/blackbox5/` (project-specific) is significantly blurred. Analysis found 47+ hardcoded cross-boundary paths, 18 categories of duplications, and 62+ items misplaced.

---

## Guiding Principle

| Location | Purpose |
|----------|---------|
| **2-engine/** | Anything standardized across ALL projects |
| **5-project-memory/blackbox5/** | Anything specific to BlackBox5 project |

---

## Problem Statement

### Current State
- 47+ hardcoded paths crossing engine/project boundary
- 18 categories of duplications between locations
- 62 items in engine that are BlackBox5-specific
- 45 items in project that should be standardized
- No path abstraction layer
- routes.yaml has incorrect path nesting

### Impact
- Violates separation of concerns
- Makes engine non-reusable for other projects
- Creates maintenance burden
- Fragile relative paths break when files move

### Desired State
- Clear boundary: engine = generic, project = specific
- Zero hardcoded cross-boundary paths
- Path abstraction layer used everywhere
- No duplications
- Engine is fully reusable across projects

---

## The Scout-Planner-Executor Workflow

```
┌─────────────────────────────────────────────────────────────┐
│              ARCHITECTURE IMPROVEMENT LOOP                  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐                │
│  │  SCOUT  │───▶│ PLANNER │───▶│ EXECUTOR│                │
│  │         │    │         │    │         │                │
│  │ Analyze │    │ Validate│    │ Implement│               │
│  │  Area   │    │  Plan   │    │   Fix    │                │
│  └─────────┘    └─────────┘    └─────────┘                │
│       ▲                              │                      │
│       └──────────────────────────────┘                      │
│              (feedback loop)                                │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Scout Phase
- Analyze specific area (directory structure, data flow, etc.)
- Identify issues and opportunities
- Document findings
- Create detailed analysis report

### Planner Phase
- Review scout findings
- Validate issues are real and worth fixing
- Create detailed implementation plan
- Define acceptance criteria
- Estimate effort

### Executor Phase
- Implement the fix
- Update all references
- Test thoroughly
- Document changes
- Mark task complete

---

## Analysis Areas (Scout Tasks)

### Area 1: Path Dependencies ✓ (COMPLETED)
**Status:** Analysis complete
**Findings:** 47 hardcoded paths, 25+ files affected
**Report:** `engine-project-split-analysis.md`

### Area 2: Content Misplacement
**Status:** Pending scout analysis
**Focus:** Which items belong in engine vs project
**Expected:** Detailed inventory of 62+ misplaced items

### Area 3: Duplications
**Status:** Partially analyzed
**Findings:** 18 categories identified
**Next:** Deep dive on each category

### Area 4: routes.yaml Structure
**Status:** Critical issue identified
**Problem:** Incorrect path nesting
**Next:** Design proper hierarchical structure

### Area 5: Agent Script Architecture
**Status:** Pending analysis
**Focus:** 6-agent pipeline coupling
**Next:** Analyze dependencies and boundaries

---

## Implementation Phases

### Phase 1: Foundation (Week 1)
**Goal:** Create path abstraction layer

**Tasks:**
- TASK-ARCH-060: Create path abstraction library
- TASK-ARCH-064: Fix routes.yaml structure
- TASK-ARCH-065: Update critical agent scripts

**Deliverables:**
- paths.sh and paths.py libraries
- Fixed routes.yaml
- 6 agent scripts using abstraction

### Phase 2: Migration (Week 2)
**Goal:** Move misplaced content

**Tasks:**
- TASK-ARCH-061: Migrate engine scripts to project
- TASK-ARCH-063: Standardize project content to engine

**Deliverables:**
- 8 scripts moved to project
- 33 items standardized to engine
- Backward compatibility maintained

### Phase 3: Consolidation (Week 3)
**Goal:** Eliminate duplications

**Tasks:**
- TASK-ARCH-062: Consolidate duplicate prompts
- TASK-ARCH-066: Merge queue systems
- TASK-ARCH-067: Unify event systems

**Deliverables:**
- 3 merged prompts
- Single queue system
- Single event system

### Phase 4: Validation (Week 4)
**Goal:** Verify and cleanup

**Tasks:**
- TASK-ARCH-068: Verify zero hardcoded paths
- TASK-ARCH-069: Test all systems
- TASK-ARCH-070: Update documentation

**Deliverables:**
- Verification report
- All tests passing
- Updated architecture docs

---

## Success Criteria

- [ ] Zero hardcoded cross-boundary paths (verified by grep)
- [ ] Path abstraction library used everywhere
- [ ] All 62 misplaced items in correct location
- [ ] All 18 duplications eliminated
- [ ] routes.yaml has correct structure
- [ ] Engine is reusable (no project-specific code)
- [ ] All tests pass
- [ ] Documentation updated

---

## Related Documents

- Analysis: `.autonomous/analysis/engine-project-split-analysis.md`
- Structural Issues: `.autonomous/analysis/STRUCTURAL_ISSUES_MASTER_LIST.md`
- Cross-boundary paths: `.autonomous/analysis/cross-boundary-paths.md`
- Duplications: `.autonomous/analysis/engine-project-duplications.md`
- Migration strategy: `.autonomous/analysis/migration-strategy.md`

---

*Plan Version: 1.0*
*Last Updated: 2026-02-06*
