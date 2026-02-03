# BlackBox5 Complete File Inventory

**Date:** 2026-02-02
**Total Files:** 1,171
**Status:** Architecture analysis in progress

---

## Top-Level Directory Structure

```
5-project-memory/blackbox5/
├── .analysis/              # Analysis workspace
├── .archived/              # Archived items
├── .autonomous/            # Agent data (DEPRECATED - see autonomous/)
├── .docs/                  # Documentation templates
├── .templates/             # File templates
├── architecture/           # Architecture documentation
├── autonomous/             # Project agent data (ACTIVE)
├── decisions/              # Decision records
├── knowledge/              # Knowledge base
├── memory/                 # Project memory
├── operations/             # Operations docs
├── plans/                  # Project plans
├── project/                # Project metadata
├── runs/                   # Run history
├── tasks/                  # Legacy tasks (DEPRECATED)
├── _NAMING.md              # Naming conventions
├── ACTIVE.md               # Current work dashboard
├── ARCHITECTURE_DECISIONS.md  # Moving to architecture/
├── goals.yaml              # Project goals
├── MAP.yaml                # Complete file map
├── QUERIES.md              # Project queries
├── README.md               # Project overview
├── STATE.yaml              # Project state
└── timeline.yaml           # Timeline data
```

---

## Directory Analysis

### 1. ROOT LEVEL FILES (9 files)

| File | Purpose | Status |
|------|---------|--------|
| _NAMING.md | Naming conventions | Active |
| ACTIVE.md | Work dashboard | Active |
| ARCHITECTURE_DECISIONS.md | Arch decisions (migrating) | Migrating |
| goals.yaml | Project goals | Active |
| MAP.yaml | File map | Active |
| QUERIES.md | Queries | Active |
| README.md | Overview | Active |
| STATE.yaml | State | Active |
| timeline.yaml | Timeline | Active |

### 2. DOT-FOLDERS (Hidden/System)

#### .analysis/
- **Purpose:** Analysis workspace
- **Status:** Unknown usage
- **Needs audit:** Check if actually used

#### .archived/
- **Purpose:** Archived items
- **Status:** Check contents
- **Needs audit:** Verify still needed

#### .autonomous/ (DEPRECATED)
- **Purpose:** Old agent data location
- **Status:** DEPRECATED - superseded by `autonomous/`
- **Issue:** Duplicate of `autonomous/` folder
- **Subfolders:** 16 total
  - approvals/
  - communications/
  - data/
  - feedback/
  - goals/
  - LOGS/
  - memory/
  - operations/
  - planner-tracking/
  - reviews/
  - runs/
  - tasks/
  - timeline/
  - validations/
  - workspaces/

#### .docs/
- **Purpose:** Documentation templates/guides
- **Status:** Active
- **Files:** 6 guides
  - ai-template-usage-guide.md
  - dot-docs-system.md
  - learning-extraction-guide.md
  - migration-plan.md
  - siso-internal-patterns.md
  - template-system-guide.md

#### .templates/
- **Purpose:** File templates
- **Status:** Active
- **Subfolders:** 7
  - agents/
  - decisions/
  - epic/
  - research/
  - reviews/
  - root/
  - tasks/

### 3. REGULAR FOLDERS

#### architecture/ (NEW)
- **Purpose:** Architecture documentation
- **Status:** Active (created 2026-02-02)
- **Subfolders:**
  - context/ - Current system state
  - decisions/ - Architecture decisions
  - knowledge/ - Architectural patterns
  - plans/ - Future improvements

#### autonomous/ (ACTIVE)
- **Purpose:** Project agent data
- **Status:** Active
- **Subfolders:** 4
  - communications/
  - runs/
  - tasks/
  - context/

#### decisions/
- **Purpose:** Decision records
- **Status:** Active
- **Subfolders:** 4
  - .docs/
  - infrastructure/
  - scope/
  - technical/
- **Note:** architectural/ moved to architecture/decisions/

#### knowledge/
- **Purpose:** Knowledge base
- **Status:** Active
- **Subfolders:** 10
  - .docs/
  - analysis/
  - architecture/ (moving to architecture/knowledge/)
  - archives/
  - codebase/
  - first-principles/
  - frameworks/
  - ralf-patterns/
  - ralph-integration/
  - ralph-loop/
  - research/
  - validation/

#### memory/
- **Purpose:** Project memory
- **Status:** Active
- **Subfolders:** 1
  - insights/

#### operations/
- **Purpose:** Operations docs
- **Status:** Active
- **Subfolders:** 7
  - .docs/
  - agents/
  - architecture/ (empty?)
  - dashboard/
  - docs/
  - logs/
  - sessions/
  - workflows/

#### plans/
- **Purpose:** Project plans
- **Status:** Active
- **Subfolders:** 6
  - .docs/
  - active/
  - archived/
  - briefs/
  - features/
  - prds/

#### project/
- **Purpose:** Project metadata
- **Status:** Active
- **Subfolders:** 2
  - .docs/
  - context.yaml

#### runs/
- **Purpose:** Run history
- **Status:** Active
- **Subfolders:** 8
  - .docs/
  - archived/
  - assets/
  - completed/
  - executor/
  - planner/
  - timeline/

#### tasks/ (DEPRECATED)
- **Purpose:** Legacy task system
- **Status:** DEPRECATED
- **Subfolders:** 5
  - .docs/
  - backlog/
  - completed/
  - FG-1769138998/
  - working/

---

## Critical Architecture Issues Found

### Issue 1: Duplicate .autonomous Folders
```
.autonomous/     - 16 subfolders, contains old data
autonomous/      - 4 subfolders, new clean structure
```
**Problem:** Two folders with same purpose
**Impact:** Confusion about which to use
**Action:** Migrate data from `.autonomous/` to `autonomous/`, then delete

### Issue 2: Duplicate Task Systems
```
tasks/                    - Legacy (backlog/, working/, completed/)
.autonomous/tasks/        - Old system (48 completed tasks)
autonomous/tasks/         - New system (empty)
```
**Problem:** Three task locations
**Impact:** Agents don't know which to use
**Action:** Consolidate all into `autonomous/tasks/`

### Issue 3: Duplicate Run Systems
```
.autonomous/runs/         - 8 old runs
runs/archived/            - Archived runs
runs/completed/           - Completed runs
runs/executor/            - 61 executor runs
runs/planner/             - 77 planner runs
runs/timeline/            - Timeline data
```
**Problem:** Run data scattered across 6 locations
**Impact:** Run history fragmented
**Action:** Consolidate all into `runs/`

### Issue 4: Scattered Architecture Docs
```
ARCHITECTURE_DECISIONS.md (root)     - Moving
decisions/architectural/             - Moved to architecture/decisions/
knowledge/architecture/              - Moving to architecture/knowledge/
architecture/                        - New consolidated location
```
**Problem:** Architecture docs in 4 places
**Action:** Consolidate into `architecture/`

### Issue 5: Empty/Underused Folders
Potentially empty (need verification):
- `.analysis/`
- `.archived/`
- `operations/architecture/`
- `.autonomous/validations/`
- `.autonomous/workspaces/`

---

## File Count by Category

| Category | Count | Notes |
|----------|-------|-------|
| Root files | 9 | Includes 1 migrating |
| Dot-folders | 5 | 1 deprecated |
| Regular folders | 10 | 1 deprecated |
| Total directories | ~80 | Including nested |
| Total files | 1,171 | Across all folders |

---

## Next Steps

1. **Verify empty folders** - Check which are actually empty
2. **Audit .autonomous/ content** - See what needs migrating
3. **Consolidate task systems** - Pick one location
4. **Consolidate run systems** - Unify run storage
5. **Complete architecture migration** - Move remaining docs
6. **Delete deprecated folders** - After migration complete

---

## Questions

1. Is `.analysis/` used for anything?
2. What's in `.archived/` - can it be deleted?
3. Are there active tasks in `.autonomous/tasks/`?
4. Is `operations/architecture/` empty?
5. What's the difference between `.docs/` and `.templates/`?
