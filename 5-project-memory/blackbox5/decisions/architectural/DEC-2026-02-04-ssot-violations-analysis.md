# DEC-2026-02-04: Single Source of Truth Violations Analysis

**Status:** Proposed
**Date:** 2026-02-04
**Context:** IG-007 Continuous Architecture Evolution
**Impact:** High - affects all autonomous agent operations

---

## Problem Statement

BlackBox5 claims to follow "Single Source of Truth" but has multiple sources for the same information, causing:
- Agents reading outdated data
- Conflicting instructions
- Maintenance burden (update N files instead of 1)
- Trust erosion (which source is correct?)

---

## Violations Catalog

### VIOLATION-1: Project Identity Fragmentation

**Severity:** Critical
**Impact:** Agents don't know which project version/identity to trust

| Source | Version | Description | Last Updated |
|--------|---------|-------------|--------------|
| STATE.yaml | 5.1.0 | "Global AI Infrastructure..." | 2026-02-04 |
| project/context.yaml | 5.0.0 | "Next-generation autonomous agent..." | 2026-01-20 |
| README.md | 5.0.0 | "Autonomous Agent Framework" | 2026-02-04 |

**Conflict:** Version numbers differ (5.1.0 vs 5.0.0)
**Risk:** Agent confusion about capabilities and maturity

---

### VIOLATION-2: Active Work Tracking - Multiple Sources

**Severity:** High
**Impact:** Agents can't determine what to work on

| Source | Claims Active | Type |
|--------|---------------|------|
| STATE.yaml tasks.active | TASK-1769978192 (Design Agent Flow) | Single task |
| Ralf-context.md | 5 features (F-013, F-014, F-016, F-017, F-018) | Feature specs |
| goals/active/IG-007/ | TASK-ARCH-001 (Architecture Framework) | Goal task |
| .autonomous/communications/queue.yaml | Unknown | Queue |

**Conflict:** Four different "active work" sources with no cross-references
**Risk:** Parallel work on conflicting tasks, duplicate effort

---

### VIOLATION-3: Outdated References in STATE.yaml

**Severity:** High
**Impact:** STATE.yaml claims authority but references deleted files

**Files Listed But Don't Exist:**
- ACTIVE.md (deleted in cleanup)
- WORK-LOG.md (deleted in cleanup)
- _NAMING.md (moved to knowledge/conventions/)
- QUERIES.md (deleted in cleanup)
- UNIFIED-STRUCTURE.md (deleted in cleanup)

**Files Listed But Moved:**
- _NAMING.md → knowledge/conventions/naming.md

**Risk:** Agents following STATE.yaml references fail

---

### VIOLATION-4: Decision Records Scattered

**Severity:** Medium
**Impact:** Can't trace why architecture choices were made

| Location | Count | Status |
|----------|-------|--------|
| STATE.yaml decisions section | 7 decisions | Listed inline |
| decisions/architectural/ | 2 files | Actual files |
| decisions/scope/ | 0 files | Empty directory |
| decisions/technical/ | 1 file | Exists |

**Conflict:** STATE.yaml lists decisions not in decisions/ folder
**Risk:** Decisions lost, rationale forgotten, repeated mistakes

---

### VIOLATION-5: Project Description Duplication

**Severity:** Low
**Impact:** Minor confusion, maintenance burden

| File | Description |
|------|-------------|
| STATE.yaml | "Global AI Infrastructure for multi-agent orchestration" |
| project/context.yaml | "Next-generation autonomous agent system with hierarchical memory..." |
| README.md | Consolidated description |

**Conflict:** Three different descriptions of same project
**Risk:** Inconsistent messaging, outdated descriptions

---

## Special Case: Ralf-context.md

**Status:** Required for RALF Loop Operation
**Constraint:** CANNOT be eliminated
**Purpose:** Session-specific context injection for RALF agents

**Characteristics:**
- Updated every RALF loop (frequently changing)
- Contains loop-specific data (what was worked on, what's next)
- Injected via SessionStart hook
- Format optimized for RALF consumption

**Implication:** Ralf-context.md is a **derived view**, not a source of truth. It aggregates from canonical sources.

---

## Root Cause Analysis

```
STATE.yaml tried to be EVERYTHING:
├── Project identity (should be project/context.yaml)
├── Active tasks (should be tasks/active/)
├── Active goals (should be goals/active/)
├── Decisions (should be decisions/)
├── Structure (legitimate)
├── Templates (legitimate)
└── System status (legitimate)

Result: STATE.yaml duplicates + becomes outdated
```

**The Pattern:** Convenience vs. Correctness
- It's convenient to have one file with everything
- But it violates SSOT when that info lives elsewhere
- STATE.yaml became a "cache" that doesn't invalidate

---

## Solution Options

### Option A: STATE.yaml as Aggregator (Recommended)

**Approach:** STATE.yaml references, doesn't duplicate

**Canonical Sources:**
| Concern | Canonical Location | STATE.yaml Role |
|---------|-------------------|-----------------|
| Project identity | project/context.yaml | Reference + cache |
| Active goals | goals/active/ | List with symlinks |
| Active tasks | tasks/active/ | Reference only |
| Decisions | decisions/ | Index, not content |
| Structure | STATE.yaml | **Canonical** |
| Templates | .templates/ | **Canonical** |
| System config | STATE.yaml | **Canonical** |

**Ralf-context.md:** Derived from canonical sources, updated per loop

**Pros:**
- Clear separation of concerns
- Each source has single responsibility
- STATE.yaml stays focused
- Automation possible

**Cons:**
- More files to read
- Need cross-reference validation

**First Principles Alignment:**
- ✅ Single Source: Each concern has one owner
- ✅ Convention: Clear where each type lives
- ✅ Minimal: STATE.yaml only owns structure
- ✅ Hierarchy: Project → Goals → Tasks clear

---

### Option B: STATE.yaml as Supreme Source

**Approach:** Everything lives in STATE.yaml, other files are views

**Structure:**
- STATE.yaml = Canonical everything
- project/context.yaml = Generated from STATE.yaml
- goals/ = Generated from STATE.yaml
- tasks/ = Source of truth (too big to inline)

**Pros:**
- One file to rule them all
- Easy to get complete picture

**Cons:**
- STATE.yaml becomes massive
- Hard to edit (YAML complexity)
- Doesn't scale
- Violates "Minimal Viable Documentation"

**First Principles Alignment:**
- ❌ Single Source: Technically yes, but impractical
- ❌ Convention: Non-standard (everything in one file)
- ❌ Minimal: File becomes bloated
- ❌ Hierarchy: Flattened into one level

---

### Option C: Event-Driven Sync

**Approach:** Changes propagate via events, all sources stay in sync

**Mechanism:**
- Change project/context.yaml → Event fired
- STATE.yaml subscribes → Updates reference
- Ralf-context.md subscribes → Updates for next loop

**Pros:**
- Eventually consistent
- Multiple views possible
- Real-time updates

**Cons:**
- Complex infrastructure
- Overkill for current scale
- Debugging sync issues hard

**First Principles Alignment:**
- ✅ Single Source: Each change has one origin
- ⚠️ Convention: Complex, non-obvious
- ❌ Minimal: Heavy infrastructure
- ✅ Hierarchy: Preserved

---

## Recommendation

**Option A: STATE.yaml as Aggregator**

**Rationale:**
1. **Autonomous Agent Friendly:** Clear where to find what
2. **Scalable:** Each concern can grow independently
3. **Maintainable:** Change one file, not N
4. **Validatable:** Can check references vs. reality
5. **RALF Compatible:** Ralf-context.md derived from clear sources

**Implementation:**
1. Strip STATE.yaml of duplicated content
2. Add reference pointers to canonical sources
3. Create validation script (check references exist)
4. Update Ralf-context.md generation to pull from canonical sources
5. Document the pattern: "Reference, Don't Duplicate"

---

## Acceptance Criteria

- [ ] STATE.yaml contains no duplicated project identity info
- [ ] STATE.yaml references project/context.yaml for identity
- [ ] STATE.yaml lists active goals with symlinks
- [ ] STATE.yaml references tasks/active/ for task details
- [ ] All references in STATE.yaml validated (no broken links)
- [ ] Ralf-context.md generation documented
- [ ] Validation script created and tested

---

## Next Steps

1. **DECISION REQUIRED:** Accept Option A approach?
2. Create TASK-ARCH-003: Implement SSOT Fix
3. Execute: Strip duplicates, add references, validate
4. Test: Run validation, check RALF loop still works
5. Document: Update knowledge/architecture/ssot-pattern.md

---

**Proposed By:** Claude (Architecture Analysis)
**Date:** 2026-02-04
**Decision Due:** Next session
