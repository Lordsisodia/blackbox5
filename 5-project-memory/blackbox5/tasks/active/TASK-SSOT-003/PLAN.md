# PLAN.md: Consolidate Run Folders - Single Source of Truth

**Task:** TASK-SSOT-003 - Run folders exist in both engine and project
**Status:** Planning
**Created:** 2026-02-06
**Estimated Effort:** 3-4 hours
**Importance:** 70 (High)

---

## 1. First Principles Analysis

### The Core Problem
Run data is fragmented across two locations:
- `2-engine/runs/` - Engine-level run storage
- `5-project-memory/blackbox5/runs/` - Project-level run storage

This creates:
1. **Data Fragmentation**: Run data split across locations
2. **Query Complexity**: Finding all runs requires checking both locations
3. **Inconsistent Structure**: Different naming conventions
4. **Backup/Archive Issues**: Two places to manage

### Guiding Principle
- **Project-Owned Runs**: Runs are project-specific and should live in project directory
- **Engine as Framework**: Engine provides the runtime, not the storage
- **Clear Boundaries**: Engine = generic runtime, Project = specific data

---

## 2. Current State Analysis

### Directory Structure

```
2-engine/runs/
├── run-20260205_143022/
│   ├── THOUGHTS.md
│   ├── DECISIONS.md
│   └── results.json
└── run-20260205_150145/
    └── ...

5-project-memory/blackbox5/runs/
├── run-20260205_143022/
│   ├── THOUGHTS.md
│   ├── DECISIONS.md
│   └── results.json
└── run-20260205_150145/
    └── ...
```

### Issues

1. **Duplication**: Same runs in both locations
2. **Divergence**: Runs may have different content
3. **Confusion**: Which location is authoritative?
4. **Waste**: Double storage space

---

## 3. Proposed Solution

### Decision: Project-Owned Storage

**Canonical Location:** `5-project-memory/blackbox5/runs/`

**Rationale:**
- Runs are project-specific (contain project decisions, thoughts, results)
- Engine should be stateless/generic
- Projects may have different run retention policies

### Migration Plan

#### Phase 1: Audit (30 min)

1. List all runs in `2-engine/runs/`
2. List all runs in `5-project-memory/blackbox5/runs/`
3. Identify:
   - Runs only in engine (need migration)
   - Runs only in project (already correct)
   - Runs in both (need merge/verification)

#### Phase 2: Migration (2 hours)

1. For each run in engine:
   - Check if exists in project
   - If not exists: Copy to project
   - If exists: Compare, keep most recent/complete
2. Update any engine scripts that write to `2-engine/runs/`

#### Phase 3: Path Updates (1 hour)

**Update Scripts:**
- `2-engine/.autonomous/bin/*.py` - Change run path
- `2-engine/.autonomous/shell/*.sh` - Change run path
- Any hardcoded references to `2-engine/runs/`

**New Pattern:**
```python
# Before
RUN_DIR = "2-engine/runs/"

# After
RUN_DIR = get_project_path() + "/runs/"
```

#### Phase 4: Cleanup (30 min)

1. Remove `2-engine/runs/` directory
2. Add to `.gitignore` to prevent recreation
3. Update documentation

---

## 4. Files to Modify

### Scripts to Update
1. `2-engine/.autonomous/bin/scout-intelligent.py`
2. `2-engine/.autonomous/bin/executor-implement.py`
3. `2-engine/.autonomous/bin/verifier-validate.py`
4. `2-engine/.autonomous/bin/improvement-loop.py`
5. `2-engine/.autonomous/shell/ralf-loop.sh`

### Configuration
1. `5-project-memory/blackbox5/.autonomous/context/routes.yaml` - Add runs path

### Documentation
1. `2-engine/.autonomous/docs/RUN_STRUCTURE.md` - Update paths

---

## 5. Success Criteria

- [ ] All runs consolidated to project directory
- [ ] Zero runs remaining in `2-engine/runs/`
- [ ] All scripts updated to use project path
- [ ] No hardcoded references to `2-engine/runs/`
- [ ] Run creation works correctly in new location
- [ ] Archive/cleanup processes work

---

## 6. Rollback Strategy

If issues arise:

1. **Immediate**: Restore `2-engine/runs/` from backup
2. **Short-term**: Revert script changes
3. **Re-migrate**: Fix issues and re-run migration

---

## 7. Estimated Timeline

| Phase | Duration | Cumulative |
|-------|----------|------------|
| Phase 1: Audit | 30 min | 30 min |
| Phase 2: Migration | 2 hours | 2.5 hours |
| Phase 3: Path Updates | 1 hour | 3.5 hours |
| Phase 4: Cleanup | 30 min | 4 hours |
| **Total** | | **3-4 hours** |

---

*Plan created based on SSOT violation analysis - Run folders in both engine and project*
