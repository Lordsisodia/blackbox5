# PLAN.md: Consolidate Run Folders

**Task:** TASK-SSOT-033 - Run folders scattered in multiple locations
**Status:** Planning
**Created:** 2026-02-06
**Estimated Effort:** 2-3 hours
**Importance:** 60 (Medium)

---

## 1. First Principles Analysis

### The Core Problem
Run folders exist in multiple locations:
- `2-engine/runs/` - Engine runs
- `5-project-memory/blackbox5/runs/` - Project runs

This creates:
1. **Data Fragmentation**: Run data split across locations
2. **Query Complexity**: Finding runs requires checking both
3. **Inconsistent Structure**: Different naming conventions
4. **Backup Issues**: Two places to manage

### First Principles Solution
- **Project-Owned**: Runs are project-specific
- **Single Location**: All runs in project directory
- **Clear Structure**: Consistent naming
- **Migration**: Move engine runs to project

---

## 2. Proposed Solution

### Consolidation Plan

**Canonical Location:** `5-project-memory/blackbox5/runs/`

#### Phase 1: Audit (30 min)

1. List all runs in engine
2. List all runs in project
3. Identify duplicates and unique runs

#### Phase 2: Migration (1 hour)

```bash
#!/bin/bash
# migrate-runs.sh

ENGINE_RUNS="$HOME/.blackbox5/2-engine/runs"
PROJECT_RUNS="$HOME/.blackbox5/5-project-memory/blackbox5/runs"

for run in "$ENGINE_RUNS"/run-*; do
    if [ -d "$run" ]; then
        run_name=$(basename "$run")
        if [ ! -d "$PROJECT_RUNS/$run_name" ]; then
            cp -r "$run" "$PROJECT_RUNS/"
            echo "Migrated: $run_name"
        fi
    fi
done
```

#### Phase 3: Update Scripts (1 hour)

Update all scripts that reference run paths:
```python
# Before
RUN_DIR = "2-engine/runs/"

# After
RUN_DIR = get_project_path() + "/runs/"
```

#### Phase 4: Cleanup (30 min)

1. Remove `2-engine/runs/`
2. Update .gitignore
3. Update documentation

---

## 3. Success Criteria

- [ ] All runs in project directory
- [ ] Engine runs directory removed
- [ ] All scripts updated
- [ ] No broken references

---

## 4. Estimated Timeline

| Phase | Duration |
|-------|----------|
| Audit | 30 min |
| Migration | 1 hour |
| Script Updates | 1 hour |
| Cleanup | 30 min |
| **Total** | **2-3 hours** |

---

*Plan created based on SSOT violation analysis*
