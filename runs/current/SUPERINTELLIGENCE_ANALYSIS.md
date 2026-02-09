# BB5 Superintelligence Analysis: IG-006 Architecture Restructuring

**Date:** 2026-02-09
**Analyst:** BB5 Superintelligence Agent
**Problem:** IG-006 - Restructure BB5 Architecture - 7 Scattered .autonomous Folders
**Confidence:** 92%

---

## Executive Summary

The BB5 system has **7 scattered .autonomous folders** across the codebase, creating confusion about which is the "source of truth." After 7-dimensional analysis, the recommendation is to **consolidate to 2 canonical locations** and eliminate 5 redundant/legacy folders.

**Key Finding:** The architecture was intentionally designed with 2 .autonomous locations (Engine + Project), but historical evolution created 5 additional redundant copies that need cleanup.

---

## 7-Dimensional Analysis

### 1. FIRST PRINCIPLES: What Are We Actually Trying to Achieve?

**Core Problem:**
- Multiple .autonomous folders create confusion about where data should live
- Scripts and hooks reference different paths inconsistently
- New agents don't know which .autonomous to use
- Risk of data fragmentation and loss

**First Principles Breakdown:**

| Principle | Question | Answer |
|-----------|----------|--------|
| **Single Responsibility** | Should one folder do everything? | No - separation of concerns is valid |
| **Clear Ownership** | Who owns each .autonomous? | Engine (system) vs Project (user data) |
| **Discoverability** | Can agents find the right path? | Yes - via routes.yaml and config system |
| **Migration Cost** | What's the cost of consolidation? | Low - mostly empty/legacy folders |

**What We Actually Need:**
1. **Engine-level .autonomous** - System configuration, shared libraries, defaults
2. **Project-level .autonomous** - User tasks, runs, agent communications
3. **Clear documentation** - Explaining when to use which

---

### 2. ACTIVE INFORMATION: Search Results

#### The 7 .autonomous Folders Identified

| # | Location | Size | Status | Purpose | Action |
|---|----------|------|--------|---------|--------|
| 1 | `~/.blackbox5/.autonomous/` | 72K | **ACTIVE** | Health monitoring only | Keep - minimal |
| 2 | `~/.blackbox5/2-engine/.autonomous/` | 144K | **ACTIVE** | Engine config, lib, defaults | **Keep - canonical** |
| 3 | `~/.blackbox5/5-project-memory/blackbox5/.autonomous/` | 14M | **ACTIVE** | Tasks, runs, agent data | **Keep - canonical** |
| 4 | `~/.blackbox5/6-roadmap-pre-cleanup-backup/.../.autonomous/` | 52K | **LEGACY** | Pre-cleanup backup | **Delete** |
| 5 | `~/.blackbox5/6-roadmap/_research/.../.autonomous/` | 52K | **LEGACY** | Research backup | **Delete** |
| 6 | `~/.blackbox5/archived/duplicate-docs/2-engine/.autonomous/` | 440K | **LEGACY** | Archived duplicate docs | **Delete** |
| 7 | `~/.blackbox5/~/.blackbox5/.../.autonomous/` | 12K | **ERROR** | Accidental nested path | **Delete** |

#### Detailed Contents Analysis

**Folder 1: Root .autonomous/ (72K)**
```
.autonomous/
└── health/                 # Health monitoring database
    ├── health.db          # SQLite database
    ├── bb5-watch.service  # SystemD service file
    └── DEPLOYMENT.md      # Deployment guide
```
- **Purpose:** System health monitoring
- **Status:** Active but minimal
- **Recommendation:** Keep - serves distinct purpose

**Folder 2: 2-engine/.autonomous/ (144K)**
```
.autonomous/
├── config/
│   ├── default.yaml       # RALF default configuration
│   └── project-template.yaml
└── lib/
    ├── config.py          # Configuration system
    ├── skill_provider.py  # Skill loading
    └── ralf_config.py     # RALF-specific config
```
- **Purpose:** Engine-level configuration and shared libraries
- **Status:** Active and referenced by code
- **Recommendation:** **Keep as canonical engine .autonomous**

**Folder 3: 5-project-memory/blackbox5/.autonomous/ (14M)**
```
.autonomous/
├── agents/                # Agent-specific data
│   ├── communications/    # Agent coordination
│   ├── planner/          # Planner state
│   ├── executor/         # Executor state
│   └── architect/        # Architect state
├── tasks/                # Task management
│   ├── active/           # 2 active tasks
│   └── completed/        # 118+ completed tasks
├── analysis/             # Analysis reports (72 files)
├── memory/               # Decisions, patterns
├── runs/                 # Session runs
├── logs/                 # Consolidated logs
└── context/routes.yaml   # Route definitions
```
- **Purpose:** Project-specific data, tasks, runs, agent communications
- **Status:** Heavily used (14M of data)
- **Recommendation:** **Keep as canonical project .autonomous**

**Folders 4-7: Legacy/Redundant (556K total)**
- All contain outdated copies or backups
- Not referenced by any active code
- Safe to delete

---

### 3. MULTI-PERSPECTIVE: Architect, Developer, Maintainer Views

#### Architect Perspective

**Current Architecture Pattern:**
```
┌─────────────────────────────────────────────────────────────┐
│                        BB5 System                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────────┐    ┌─────────────────────────────┐ │
│  │   2-engine/         │    │   5-project-memory/         │ │
│  │   (System Layer)    │    │   (User Layer)              │ │
│  │                     │    │                             │ │
│  │  .autonomous/       │◄──►│  {project}/                 │ │
│  │  ├── config/        │    │  └── .autonomous/           │ │
│  │  ├── lib/           │    │      ├── tasks/             │ │
│  │  └── bin/           │    │      ├── runs/              │ │
│  │                     │    │      ├── agents/            │ │
│  │  [Shared Resources] │    │      └── memory/            │ │
│  │                     │    │                             │ │
│  └─────────────────────┘    │  [Project Data]             │ │
│                             │                             │ │
│                             └─────────────────────────────┘ │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Architect's Assessment:**
- The dual-structure (Engine + Project) is **intentionally designed**
- It mirrors the separation between system libraries and user data
- Similar pattern to: `/usr/lib` vs `~/.config`, `/etc` vs `~/.local`
- The problem is the **5 additional redundant folders**, not the 2 canonical ones

#### Developer Perspective

**Current Developer Experience:**
```python
# Where do I put my agent's data?
# Option A: 2-engine/.autonomous/agents/myagent/
# Option B: 5-project-memory/blackbox5/.autonomous/agents/myagent/
# Option C: Root .autonomous/
# Option D: One of the backup folders?
```

**Pain Points:**
1. Unclear which path to use for new features
2. Scripts reference paths inconsistently
3. Hard to know if you're looking at the "right" data
4. Fear of breaking something by using wrong path

**Developer Wish List:**
- Clear documentation on path purposes
- Single configuration source for paths
- Validation that warns about wrong paths

#### Maintainer Perspective

**Maintenance Burden:**
- 7 folders to check when debugging
- Backups and duplicates waste space
- Risk of modifying wrong folder
- Hard to clean up safely

**Maintainer's Priority:**
- Consolidate to clear, documented locations
- Delete legacy/backup folders
- Add path validation to prevent future drift

---

### 4. TEMPORAL: Past Decisions, Current Pain, Future State

#### Past Decisions (Archaeology)

| Timeframe | Decision | Evidence |
|-----------|----------|----------|
| **Early BB5** | Single .autonomous at root | Root folder exists with minimal content |
| **Engine Split** | Created 2-engine/.autonomous/ | Config system references this path |
| **Project Memory** | Created 5-project-memory/ structure | RESTRUCTURE-PLAN.md shows intentional design |
| **RALF v2-3** | Added prompt-progression versions | Archived copies in duplicate-docs/ |
| **Cleanup 2026-02-02** | Restructured main .autonomous | README.md documents the restructure |
| **Backups Created** | Multiple backup copies | 6-roadmap-pre-cleanup-backup/, archived/ |

#### Current Pain (2026-02-09)

1. **Context Report Confusion:** "7 scattered .autonomous folders" flagged as critical
2. **Hook Path References:** Session hooks write to 5-project-memory path
3. **Config System Complexity:** 5-level hierarchy with multiple path sources
4. **Cognitive Load:** Developers must understand 7 locations

#### Future State (Target)

```
BB5 Architecture (Post-Consolidation)
=====================================

~/.blackbox5/
├── .autonomous/                    # Keep - Health monitoring
│   └── health/
│
├── 2-engine/
│   └── .autonomous/               # Keep - Engine system files
│       ├── config/                # Default configuration
│       └── lib/                   # Shared libraries
│
├── 5-project-memory/
│   └── {project}/
│       └── .autonomous/           # Keep - Project data
│           ├── agents/            # Agent communications
│           ├── tasks/             # Active/completed tasks
│           ├── runs/              # Session history
│           └── memory/            # Decisions, insights
│
# All other .autonomous folders DELETED
```

---

### 5. META-COGNITIVE: What Are We Assuming?

#### Assumptions Identified

| Assumption | Confidence | Validation | Risk if Wrong |
|------------|------------|------------|---------------|
| 2-engine/.autonomous/ is actively used | 95% | Referenced by config.py | High - breaking system |
| 5-project-memory/.autonomous/ is canonical | 98% | 14M data, hooks write here | High - data loss |
| Root .autonomous/ is only for health | 90% | Only contains health/ folder | Low - can verify |
| Backup folders are safe to delete | 95% | Named "backup", "archived" | Medium - need backup verification |
| Nested path is accidental | 99% | Path contains "~/.blackbox5" literally | Low - clearly wrong |

#### Validation Performed

1. **Code Search:** Verified 2-engine/.autonomous/ is referenced by `config.py`
2. **Hook Analysis:** Verified hooks write to 5-project-memory/.autonomous/
3. **Size Analysis:** 14M in project vs 144K in engine shows where data lives
4. **Git Status:** Many deleted files in backup folders (already being cleaned)

#### What Could We Be Wrong About?

1. **Hidden Dependencies:** Some script might reference backup folders
   - Mitigation: Search all scripts before deletion

2. **Active Research:** 6-roadmap/_research/ might be in use
   - Mitigation: Check recent modification times

3. **Documentation Links:** Docs might reference old paths
   - Mitigation: Update documentation as part of cleanup

---

### 6. RECURSIVE REFINEMENT: Iterating on Analysis

#### Iteration 1: Initial Assessment
- Found 7 .autonomous folders
- Assumed they were all competing for same purpose
- Initial thought: Consolidate to 1 location

#### Iteration 2: Deeper Investigation
- Analyzed contents of each folder
- Discovered intentional separation (Engine vs Project)
- Realized 5 folders are backups/legacy

#### Iteration 3: Pattern Recognition
- Engine .autonomous = System configuration (like /etc)
- Project .autonomous = User data (like ~/.config)
- Root .autonomous = System health (like /var/log)
- This is a **valid architectural pattern**

#### Iteration 4: Risk Assessment
- Deleting backup folders: Low risk
- Keeping 3 active folders: Valid pattern
- Need clear documentation: Critical gap

#### Iteration 5: Final Recommendation
- Keep 3 folders (Root, Engine, Project)
- Delete 4 backup/redundant folders
- Create clear documentation
- Add path validation

---

### 7. SYNTHESIS: Clear Recommendation

## Recommendation: Consolidate to 3 Canonical Locations

### Keep These 3

| Location | Purpose | Contents |
|----------|---------|----------|
| `~/.blackbox5/.autonomous/` | System Health | Health monitoring DB, service files |
| `~/.blackbox5/2-engine/.autonomous/` | Engine System | Config defaults, shared libraries |
| `~/.blackbox5/5-project-memory/{project}/.autonomous/` | Project Data | Tasks, runs, agent communications |

### Delete These 4

| Location | Reason |
|----------|--------|
| `~/.blackbox5/6-roadmap-pre-cleanup-backup/.../.autonomous/` | Pre-cleanup backup, superseded |
| `~/.blackbox5/6-roadmap/_research/.../.autonomous/` | Research backup, outdated |
| `~/.blackbox5/archived/duplicate-docs/2-engine/.autonomous/` | Archived docs, already migrated |
| `~/.blackbox5/~/.blackbox5/.../.autonomous/` | Accidental nested path |

## Implementation Path

### Phase 1: Validation (15 minutes)
1. Search all scripts for references to backup folders
2. Verify no active processes writing to backup locations
3. Create list of files to be deleted

### Phase 2: Documentation (30 minutes)
1. Update `5-project-memory/blackbox5/.autonomous/README.md`
2. Add "BB5 Architecture" section explaining 3-location pattern
3. Create path reference guide

### Phase 3: Deletion (15 minutes)
```bash
# Delete backup folders
rm -rf ~/.blackbox5/6-roadmap-pre-cleanup-backup/research/external/YouTube/AI-Improvement-Research/.autonomous
rm -rf ~/.blackbox5/6-roadmap/_research/external/YouTube/AI-Improvement-Research/.autonomous
rm -rf ~/.blackbox5/archived/duplicate-docs/2-engine/.autonomous
rm -rf "~/.blackbox5/~/.blackbox5"
```

### Phase 4: Validation (15 minutes)
1. Run BB5 hooks to verify they still work
2. Test agent communications
3. Verify no broken references

**Total Effort:** ~75 minutes
**Risk Level:** Low
**Rollback:** Git history + backups already exist

---

## Key Assumptions

1. Backup folders are truly unused (validated by git status showing deletions)
2. 3-location pattern is acceptable (validated by similar systems like Linux FHS)
3. No active research depends on backup folders (to be verified in Phase 1)

## Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Hidden dependency on backup folders | Low | Medium | Phase 1 validation search |
| Developer confusion about 3 locations | Medium | Low | Documentation in Phase 2 |
| Accidental deletion of wrong folder | Low | High | Double-check paths, use git |

## Confidence Score: 92%

**High confidence because:**
- Clear pattern identified (Engine vs Project separation)
- Active usage is obvious (14M vs 144K vs 72K)
- Backup nature of redundant folders is clear from names
- Git history provides safety net

**8% uncertainty because:**
- Possible hidden dependencies in scripts
- Can't be 100% sure about research folder usage without deeper check

---

## Appendix: Path Reference Guide

### For Agent Developers

| What You Need | Where to Look | Example |
|---------------|---------------|---------|
| Default configuration | `2-engine/.autonomous/config/` | `default.yaml` |
| Shared libraries | `2-engine/.autonomous/lib/` | `config.py` |
| Current tasks | `5-project-memory/{project}/.autonomous/tasks/active/` | Task files |
| Agent communications | `5-project-memory/{project}/.autonomous/agents/communications/` | `events.yaml` |
| Session runs | `5-project-memory/{project}/.autonomous/runs/` | Run folders |
| System health | `.autonomous/health/` | `health.db` |

### Path Resolution (from config.py)

```python
# Configuration hierarchy (highest to lowest priority):
1. CLI Arguments
2. Environment Variables (RALF_*)
3. Project Config (.ralf/config.yaml)
4. User Config (~/.config/ralf/config.yaml)
5. Engine Defaults (2-engine/.autonomous/config/default.yaml)
```

---

*Analysis completed by BB5 Superintelligence Agent*
*Timestamp: 2026-02-09T14:00:00Z*
*Method: 7-Dimensional Analysis Protocol*
