# ARCHITECTURE.md - Cleanup Loop

**Task:** TASK-CLEANUP-LOOP
**Date:** 2026-02-04

---

## Cleanup Architecture

### Pattern: Iterative Consolidation

The cleanup follows an iterative loop pattern:

```
Scan → Identify → Merge/Delete → Document → Repeat
```

### Loop 1: Root Consolidation (Complete)

**Input:** 14 markdown files in root
**Process:**
1. Read all files to understand content
2. Identify overlaps using first principles
3. Merge complementary content into canonical location
4. Delete redundant files
5. Move misplaced files to proper locations

**Output:** 3 markdown files in root

### Directory Structure (Post-Cleanup)

```
blackbox5/
├── README.md                    # Canonical project overview
├── Ralf-context.md             # RALF agent context
├── STATE.yaml                  # Single source of truth
├── timeline.yaml               # Project timeline
├── feature_backlog.yaml        # Feature backlog
├── test_results.yaml           # Test results
│
├── knowledge/
│   └── conventions/            # NEW: Naming and format conventions
│       ├── naming.md           # From _NAMING.md
│       └── yaml-vs-markdown.md # From YAML-vs-MD-EVALUATION.md
│
├── plans/
│   └── active/
│       └── implementation-plan-navigation.md  # From IMPLEMENTATION-PLAN.md
│
└── .archived/
    └── MIGRATION-SUMMARY.md    # Completed migration work
```

---

## Consolidation Strategy

### README.md as Canonical Hub

README.md now serves as the single entry point:

- **Overview** - Project description and purpose
- **Quick Stats** - From ACTIVE.md
- **Directory Structure** - From UNIFIED-STRUCTURE.md
- **Run Structure** - From RUN-STRUCTURE-MAP.md
- **Quick Links** - Navigation to all key areas
- **Project Status** - Current state

### Knowledge/Conventions Pattern

New directory `knowledge/conventions/` for:
- Naming conventions
- Format standards
- Best practices
- Evaluation documents

### Archive Pattern

`.archived/` for:
- Completed migrations
- Historical summaries
- Obsolete but potentially useful docs

---

## Remaining Work

### Loop 2: Knowledge Consolidation (Complete)

**Input:** 30 markdown files in knowledge/analysis/
**Process:**
1. Group files by topic using sub-agent scan
2. Identify overlapping content
3. Merge complementary analyses into comprehensive documents
4. Delete redundant files
5. Update cross-references

**Consolidation Groups:**

| Group | Files | Output |
|-------|-------|--------|
| CLAUDE.md Analysis | 2 files | claude-md-analysis.md |
| Duration Tracking | 2 files | duration-tracking-analysis-and-fix.md |
| Run Analysis | 2 files | run-analysis-47-runs.md |
| Skill System | 5 files | skill-system-analysis.md |

**Output:** 18 markdown files in knowledge/analysis/ (40% reduction)

### Loop 3: Task Naming Standardization (Pending)
- Find all TASK.md (uppercase)
- Rename to task.md (lowercase)
- Update cross-references

---

## Success Metrics

| Metric | Before | After | Target | Status |
|--------|--------|-------|--------|--------|
| Root .md files | 14 | 3 | < 5 | ✅ |
| Structure maps | 3 | 1 | 1 | ✅ |
| Duplicate topics | 5+ | 0 | 0 | ✅ |
| Files in wrong place | 5+ | 0 | 0 | ✅ |
| Knowledge analysis files | 30 | 18 | < 20 | ✅ |

---

## Commit Pattern

```
cleanup: [area] [action]

- Specific changes
- Files affected: [list]
- Rationale: [first principle]
```

Example:
```
cleanup: root consolidation

- Merged ACTIVE.md, RUN-STRUCTURE-MAP.md into README.md
- Deleted 6 redundant files
- Moved 4 files to proper locations
- Rationale: Single source of truth, minimal viable documentation
```
