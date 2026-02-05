# PLAN.md: Consolidate Hook Scripts - Single Source of Truth

**Task:** TASK-SSOT-011 - Hook scripts in both engine and project
**Status:** Planning
**Created:** 2026-02-06
**Estimated Effort:** 3-4 hours
**Importance:** 70 (High)

---

## 1. First Principles Analysis

### The Core Problem
Hook scripts are duplicated across:
- `2-engine/.autonomous/hooks/` - Engine hooks
- `5-project-memory/blackbox5/.autonomous/hooks/` - Project hooks

This creates:
1. **Execution Confusion**: Which hook runs first? Both?
2. **Maintenance Overhead**: Updates needed in multiple places
3. **Inconsistent Behavior**: Same hook behaving differently
4. **Debugging Difficulty**: Hard to trace which hook is running

### Guiding Principle
- **Engine = Framework Hooks**: Generic hooks for all projects
- **Project = Specific Hooks**: Project-specific extensions
- **Clear Precedence**: Well-defined execution order
- **No Duplication**: Each hook exists in exactly one location

---

## 2. Current State Analysis

### Directory Structure

```
2-engine/.autonomous/hooks/
├── pre-task.sh
├── post-task.sh
└── on-error.sh

5-project-memory/blackbox5/.autonomous/hooks/
├── pre-task.sh
├── post-task.sh
├── on-error.sh
└── custom-hook.sh
```

### Issues

1. **Duplicate Hooks**: Same hook name in both locations
2. **Unclear Order**: Which runs first?
3. **Conflict Potential**: Hooks may interfere with each other

---

## 3. Proposed Solution

### Decision: Hierarchical Hook System

**Execution Order:**
1. Engine pre-hooks (framework-level)
2. Project pre-hooks (project-level)
3. Task execution
4. Project post-hooks
5. Engine post-hooks

**Naming Convention:**
- Engine hooks: `engine-*`
- Project hooks: `project-*` or custom names

### Implementation Plan

#### Phase 1: Audit (30 min)

1. List all engine hooks
2. List all project hooks
3. Identify:
   - True duplicates (same purpose)
   - Project-specific hooks
   - Engine hooks that should be generic

#### Phase 2: Rename and Consolidate (2 hours)

1. **For duplicates:**
   - Keep engine version as base
   - Rename project version to `project-*`
   - Or remove if truly duplicate

2. **For project-specific:**
   - Keep with clear naming
   - Document purpose

#### Phase 3: Update Hook Loader (1 hour)

**Update:** Hook execution system

```bash
#!/bin/bash
# Hook execution with clear precedence

run_hooks() {
    local hook_type=$1  # pre-task, post-task, on-error

    # Run engine hooks first
    if [ -d "$ENGINE_DIR/.autonomous/hooks" ]; then
        for hook in "$ENGINE_DIR/.autonomous/hooks"/${hook_type}*.sh; do
            [ -f "$hook" ] && source "$hook"
        done
    fi

    # Run project hooks second
    if [ -d "$PROJECT_DIR/.autonomous/hooks" ]; then
        for hook in "$PROJECT_DIR/.autonomous/hooks"/${hook_type}*.sh; do
            [ -f "$hook" ] && source "$hook"
        done
    fi
}
```

#### Phase 4: Documentation (30 min)

1. Document hook execution order
2. Document naming conventions
3. Add examples for common use cases

---

## 4. Files to Modify

### Renamed Files
1. Project hooks renamed to `project-*` or removed if duplicate

### Modified Files
1. Hook loading scripts
2. Hook execution documentation

---

## 5. Success Criteria

- [ ] No duplicate hook names between engine and project
- [ ] Clear execution order documented
- [ ] Hook loader updated with precedence
- [ ] All hooks run correctly
- [ ] Documentation updated

---

## 6. Rollback Strategy

If issues arise:

1. **Immediate**: Restore original hook names
2. **Fix**: Debug hook loading
3. **Re-apply**: Once fixed

---

## 7. Estimated Timeline

| Phase | Duration | Cumulative |
|-------|----------|------------|
| Phase 1: Audit | 30 min | 30 min |
| Phase 2: Rename/Consolidate | 2 hours | 2.5 hours |
| Phase 3: Hook Loader | 1 hour | 3.5 hours |
| Phase 4: Documentation | 30 min | 4 hours |
| **Total** | | **3-4 hours** |

---

*Plan created based on SSOT violation analysis - Hook scripts duplicated*
