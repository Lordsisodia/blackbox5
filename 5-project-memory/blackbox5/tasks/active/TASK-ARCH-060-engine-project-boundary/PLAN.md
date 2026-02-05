# PLAN.md: Engine/Project Boundary - Path Abstraction Layer

**Task:** TASK-ARCH-060
**Title:** Fix Engine/Project Boundary - Path Abstraction Layer
**Status:** pending
**Priority:** CRITICAL
**Created:** 2026-02-06

---

## 1. Executive Summary

This is the **master coordination plan** for fixing the engine/project boundary violation affecting the entire BlackBox5 system. The boundary between `2-engine/` (standardized across projects) and `5-project-memory/blackbox5/` (project-specific) is significantly blurred with **47+ hardcoded cross-boundary paths**.

This plan coordinates **7 sub-tasks (ARCH-061 through ARCH-067)** that must execute in a specific order to successfully resolve the boundary issues.

---

## 2. Problem Statement

### Current State
- **47+ hardcoded paths** crossing between engine and project
- **6 agent scripts** in engine contain hardcoded BlackBox5 paths
- **routes.yaml** has incorrect path nesting (engine paths inside project directory)
- **18 categories of duplications** between engine and project
- **62 items** in engine that should be in project
- **45 items** in project that could be standardized to engine

### Impact
- Engine is not reusable across projects
- System is fragile - path changes break multiple components
- Tight coupling prevents independent evolution
- Violates architectural principle: engine = generic, project = specific

---

## 3. Guiding Architecture Principle

| Location | Purpose |
|----------|---------|
| **2-engine/** | Anything standardized across ALL projects |
| **5-project-memory/blackbox5/** | Anything specific to BlackBox5 project |

---

## 4. Sub-Task Coordination Matrix

| Task ID | Title | Priority | Est. Effort | Dependencies | Parallelizable |
|---------|-------|----------|-------------|--------------|----------------|
| **ARCH-064** | Fix routes.yaml Incorrect Paths | CRITICAL | 1-2 hrs | None | Yes (Phase 1) |
| **ARCH-065** | Create Path Resolution Library | CRITICAL | 4-6 hrs | ARCH-064 | No (must follow 064) |
| **ARCH-061** | Migrate Engine Scripts to Project | HIGH | 3-4 hrs | ARCH-065 | Yes (Phase 2) |
| **ARCH-062** | Consolidate Duplicate Prompts | HIGH | 2-3 hrs | ARCH-065 | Yes (Phase 2) |
| **ARCH-066** | Unify Agent Communication | HIGH | 6-8 hrs | ARCH-065 | Yes (Phase 2) |
| **ARCH-067** | Decouple Agents from Project | HIGH | 8-10 hrs | ARCH-065, ARCH-066 | No (Phase 3) |
| **ARCH-063** | Standardize Project Content to Engine | MEDIUM | 6-8 hrs | ARCH-061, ARCH-067 | No (Phase 4) |

---

## 5. Execution Phases

### Phase 1: Foundation (Days 1-2) - CRITICAL PATH

**Goal:** Establish the path abstraction foundation before any migration.

**Tasks:**
1. **ARCH-064: Fix routes.yaml Incorrect Paths**
   - Fix 10+ incorrect engine paths nested inside project directory
   - Fix duplicated path segments (e.g., `5-project-memory/blackbox5/5-project-memory/blackbox5/`)
   - Create validation script to prevent regression
   - **Must complete before ARCH-065**

2. **ARCH-065: Create Path Resolution Library**
   - Create `2-engine/.autonomous/lib/paths.sh` with functions:
     - `get_engine_path()`, `get_project_path()`, `get_routes_path()`
     - `get_runs_path()`, `get_tasks_path()`, `get_memory_path()`
   - Create `2-engine/.autonomous/lib/paths.py` with `PathResolver` class
   - Update all 6 agent scripts to use the library
   - Verify zero hardcoded paths remain with grep
   - **Must complete before any other tasks**

**Phase 1 Success Criteria:**
- [ ] All routes.yaml paths are correct and verified to exist
- [ ] Path resolution libraries created and tested
- [ ] All 6 agent scripts updated to use abstraction
- [ ] `grep -r "5-project-memory/blackbox5" 2-engine/` returns zero results

---

### Phase 2: Parallel Migration (Days 3-5)

**Goal:** Execute independent migrations using the path abstraction layer.

**Tasks (parallel execution possible):**

1. **ARCH-061: Migrate Engine Scripts to Project**
   - Move 8 BlackBox5-specific scripts from `2-engine/.autonomous/bin/` to `5-project-memory/blackbox5/.autonomous/bin/`
   - Scripts: scout-intelligent.py, executor-implement.py, improvement-loop.py, planner-prioritize.py, verifier-validate.py, scout-task-based.py
   - Create thin wrappers in engine for backward compatibility
   - Update all import paths

2. **ARCH-062: Consolidate Duplicate Prompts**
   - Merge 3 prompt pairs:
     - `prompts/agents/deep-repo-scout.md` + `prompts/agents/scout-agent-prompt.md`
     - `prompts/agents/implementation-planner.md` + `prompts/agents/planner-agent-prompt.md`
     - `prompts/ralf-executor.md` + `prompts/agents/executor-agent-prompt.md`
   - Create merged versions in engine location
   - Archive old project prompts

3. **ARCH-066: Unify Agent Communication**
   - Choose unified protocol (recommendation: Event-Driven)
   - Document event schema
   - Create communication library
   - Migrate Python agents (currently use report files)
   - Migrate Bash agents (currently use events.yaml)
   - Test end-to-end workflow

**Phase 2 Success Criteria:**
- [ ] All 8 scripts migrated and tested
- [ ] 3 prompts consolidated, no duplication remaining
- [ ] Single communication protocol implemented
- [ ] All agents use new protocol

---

### Phase 3: Agent Decoupling (Days 6-8)

**Goal:** Make agents project-agnostic.

**Task:**
- **ARCH-067: Decouple Agents from Project Structure**
  - Create `agent-config.yaml` schema
  - Create base `Agent` class
  - Remove hardcoded paths from all agents
  - Remove hardcoded task handlers (e.g., `if task_id == "TASK-SKIL-005"`)
  - Remove hardcoded file references
  - Create project initialization tool
  - Test agents with mock project

**Dependencies:** ARCH-065 (path library), ARCH-066 (communication)

**Phase 3 Success Criteria:**
- [ ] All hardcoded paths removed from agents
- [ ] Agent-config.yaml created and used
- [ ] Agents work with any project directory
- [ ] Base Agent class created
- [ ] Project initialization tool created

---

### Phase 4: Standardization (Days 9-11)

**Goal:** Move generic frameworks to engine for reuse.

**Task:**
- **ARCH-063: Standardize Project Content to Engine**
  - Move 11 generic bin/ scripts (queue manager, health dashboard, metrics collector, etc.)
  - Move 8 operations/ frameworks (skill selection, metrics, improvement frameworks)
  - Move 9 .autonomous/agents/ patterns
  - Move 5 .docs/ guides
  - Create project-specific configuration files
  - Update project to use engine versions

**Dependencies:** ARCH-061 (script migration complete), ARCH-067 (agent decoupling)

**Phase 4 Success Criteria:**
- [ ] All 33 items moved to appropriate engine locations
- [ ] Project uses engine versions via imports/references
- [ ] Thin wrappers created where needed
- [ ] Documentation updated

---

## 6. Integration Testing Plan

### Phase 1 Testing
- [ ] Validate all routes.yaml paths exist (`find` + `ls` verification)
- [ ] Test path library functions return correct paths
- [ ] Run agent scripts with path abstraction (dry-run mode)

### Phase 2 Testing
- [ ] Test each migrated script still works after move
- [ ] Verify backward compatibility wrappers work
- [ ] Test consolidated prompts with actual agent runs
- [ ] Verify unified communication protocol (events flow correctly)

### Phase 3 Testing
- [ ] Create mock project directory structure
- [ ] Run agents against mock project
- [ ] Verify agents work without BlackBox5-specific paths
- [ ] Test project initialization tool

### Phase 4 Testing
- [ ] Test moved scripts from engine location
- [ ] Verify project can still access functionality
- [ ] Run full RALF pipeline end-to-end
- [ ] Performance test (no regression)

### Final Integration Testing
- [ ] Run complete 6-agent pipeline
- [ ] Verify scout → planner → executor → verifier flow
- [ ] Test improvement loop
- [ ] Verify all reports generated correctly
- [ ] Check no hardcoded paths remain (comprehensive grep)

---

## 7. Overall Success Criteria

### Must Have (Critical)
- [ ] Zero hardcoded cross-boundary paths remain
- [ ] Path abstraction library used everywhere
- [ ] routes.yaml paths are correct and verified
- [ ] All 6 agent scripts use path abstraction
- [ ] All tests pass after migration

### Should Have (High)
- [ ] Clear separation: engine = generic, project = specific
- [ ] No duplications (merged or removed)
- [ ] Agents are project-agnostic
- [ ] Unified communication protocol

### Nice to Have (Medium)
- [ ] Documentation updated
- [ ] Performance improved (no path resolution overhead)
- [ ] New project initialization tool working

---

## 8. Rollback Strategy

### Phase 1 Rollback
- Keep backup of original routes.yaml: `routes.yaml.backup.$(date +%Y%m%d_%H%M%S)`
- Keep old path code commented during transition
- One-command restore: `cp routes.yaml.backup.* routes.yaml`

### Phase 2 Rollback
- Keep copies of scripts in engine until verified working
- Archive old prompts before merging (can restore individually)
- Dual-write mode for communication (write to both old and new)

### Phase 3 Rollback
- Keep hardcoded versions as backup
- Feature flag for new config-driven mode
- Can disable new mode to revert to old behavior

### Phase 4 Rollback
- Keep copies in project until verified
- Can restore if issues found
- Engine versions are additive (old project versions still work)

### Emergency Full Rollback
```bash
# Restore routes.yaml
cp /backup/routes.yaml.backup.* /Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/.autonomous/context/routes.yaml

# Restore scripts to engine
cp /backup/engine-bin/* /Users/shaansisodia/.blackbox5/2-engine/.autonomous/bin/

# Remove path library usage (revert to hardcoded)
git checkout HEAD -- 2-engine/.autonomous/bin/*.py
```

---

## 9. Timeline

```
Week 1: Foundation (Critical Path)
Day 1-2:  ARCH-064 (routes.yaml fix) → ARCH-065 (path library)
          [BLOCKING - all other tasks wait]

Week 2: Parallel Migration
Day 3-5:  ARCH-061 (script migration) ─┐
          ARCH-062 (prompt consolidation) ─┼→ [Can run in parallel]
          ARCH-066 (communication unification) ─┘

Week 3: Decoupling & Standardization
Day 6-8:  ARCH-067 (agent decoupling)
          [Depends on 065, 066]

Day 9-11: ARCH-063 (standardization)
          [Depends on 061, 067]

Week 4: Integration & Cleanup
Day 12-14: Integration testing, bug fixes, documentation
```

---

## 10. Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Path library has bugs | Medium | High | Extensive testing, keep backups |
| Scripts break after migration | Medium | High | Test each script individually, wrappers for compatibility |
| Dependencies missed | Medium | Medium | Dependency matrix validation before each phase |
| Timeline slips | Medium | Medium | Parallel execution where possible, buffer time in Week 4 |
| Rollback needed | Low | High | Comprehensive backups at each phase |

---

## 11. Related Documents

- `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/.autonomous/analysis/engine-project-split-analysis.md` - Full analysis
- `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/.autonomous/context/routes.yaml` - Project routes (to fix)
- `/Users/shaansisodia/.blackbox5/2-engine/.autonomous/bin/` - Engine scripts (to migrate)

---

## 12. Sub-Task Quick Reference

| Task | Directory | Key Files |
|------|-----------|-----------|
| ARCH-060 (this) | `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/tasks/active/TASK-ARCH-060-engine-project-boundary/` | PLAN.md, task.md |
| ARCH-061 | `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/tasks/active/TASK-ARCH-061-migrate-engine-scripts/` | task.md |
| ARCH-062 | `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/tasks/active/TASK-ARCH-062-consolidate-prompts/` | task.md |
| ARCH-063 | `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/tasks/active/TASK-ARCH-063-standardize-project-content/` | task.md |
| ARCH-064 | `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/tasks/active/TASK-ARCH-064-fix-routes-yaml/` | task.md |
| ARCH-065 | `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/tasks/active/TASK-ARCH-065-create-path-library/` | task.md |
| ARCH-066 | `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/tasks/active/TASK-ARCH-066-unify-communication/` | task.md |
| ARCH-067 | `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/tasks/active/TASK-ARCH-067-decouple-agents/` | task.md |

---

## 13. Next Steps

1. **Start with ARCH-064** (routes.yaml fix) - no dependencies
2. **Then ARCH-065** (path library) - blocked by 064
3. **Parallel execution** of ARCH-061, ARCH-062, ARCH-066 once 065 complete
4. **Then ARCH-067** (blocked by 065, 066)
5. **Finally ARCH-063** (blocked by 061, 067)

---

*Plan created: 2026-02-06*
*Estimated Total Effort: 30-41 hours across all sub-tasks*
*Critical Path: ARCH-064 → ARCH-065 → (ARCH-061, ARCH-062, ARCH-066) → ARCH-067 → ARCH-063*
