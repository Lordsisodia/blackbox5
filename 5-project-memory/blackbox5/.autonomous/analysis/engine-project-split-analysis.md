# Engine vs Project Split - Deep Dive Analysis

**Date:** 2026-02-06
**Analysis Type:** Structural Architecture Review
**Status:** Complete

---

## Executive Summary

Based on analysis by 5 specialized sub-agents, the boundary between `2-engine/` (standardized across projects) and `5-project-memory/blackbox5/` (project-specific) is **significantly blurred**.

### Key Metrics
- **47+ hardcoded cross-boundary paths** found
- **18 categories of duplications** identified
- **62 items in engine** that should move to project
- **45 items in project** that could be standardized to engine
- **20 agent scripts/prompts** with overlapping functionality

---

## Guiding Principle (Confirmed)

| Location | Purpose |
|----------|---------|
| **2-engine/** | Anything standardized across ALL projects |
| **5-project-memory/blackbox5/** | Anything specific to BlackBox5 project |

---

## Critical Finding #1: Hardcoded Path Dependencies

**47 distinct cross-boundary path references** across 25+ files.

### Most Critical Issues

1. **Engine scripts hardcode project paths** - All 6 agent scripts in `2-engine/.autonomous/bin/` contain:
   ```python
   PROJECT_DIR = Path.home() / ".blackbox5" / "5-project-memory" / "blackbox5"
   ENGINE_DIR = Path.home() / ".blackbox5" / "2-engine"
   ```
   This violates the engine/project boundary.

2. **routes.yaml has incorrect paths** - Project routes.yaml contains paths like:
   ```yaml
   /Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/2-engine/.autonomous/
   ```
   This incorrectly nests `2-engine` inside `5-project-memory/blackbox5/`.

3. **Shell scripts use fragile relative paths** - Multiple `../../` traversals that break if files move.

### Files with Cross-Boundary Paths

| Category | Count | Examples |
|----------|-------|----------|
| Python scripts (engine) | 7 | scout-intelligent.py, executor-implement.py, etc. |
| Python scripts (project) | 2 | bb5-metrics-collector.py, bb5-health-dashboard.py |
| Shell scripts | 4 | bb5-scout-improve, ralf-improve, ralf-daemon.sh |
| YAML configs | 5 | routes.yaml (both), project-map.yaml |
| Documentation | 15+ | Multiple .md files |

---

## Critical Finding #2: Content Misplacement

### Items in Engine That Should Move to Project (62 items)

| Area | Items | Reason |
|------|-------|--------|
| **bin/ scripts** | 8 | All agent scripts (scout, planner, executor, verifier, improvement-loop) are BlackBox5-specific |
| **prompts/agents/** | 1 | 6-agent pipeline prompts are project-specific |
| **skills/** | 3 | ralf-cloud-control, github-codespaces-control, legacy-cloud-control |
| **lib/** | 1 | roadmap_sync.py is BlackBox5-specific |
| **config/** | 1 | github-config.yaml |
| **.autonomous/ folders** | 7 | communications/, memory/, history/, wip/, vps-deployment/ |
| **.docs/** | 4 | completions/, archive/, CONSOLIDATION-REPORT.md |
| **.config/** | 1 | mcp-servers.json |

### Items in Project That Could Move to Engine (45 items)

| Area | Items | Reason |
|------|-------|--------|
| **bin/ scripts** | 11 | Queue manager, health dashboard, metrics collector are generic patterns |
| **operations/** | 8 | Skill selection, metrics, improvement frameworks are core RALF |
| **.autonomous/agents/** | 9 | 6-agent pipeline patterns (planner, executor, scout, etc.) |
| **.autonomous/prompts/** | 5 | Agent prompts should be consolidated with engine |
| **knowledge/analysis/** | 2 | Analysis frameworks are reusable |
| **.docs/** | 5 | Template system, task system, goals system guides |

---

## Critical Finding #3: Duplications

**18 categories of duplications** found between engine and project.

### High-Priority Merges Needed

| # | Engine Location | Project Location | Action |
|---|-----------------|------------------|--------|
| 1 | routes.yaml | context/routes.yaml | Make engine authoritative, project extends |
| 2 | prompts/agents/scout*.md | prompts/agents/scout-agent-prompt.md | Merge best of both |
| 3 | prompts/agents/planner*.md | prompts/agents/planner-agent-prompt.md | Merge best of both |
| 4 | prompts/agents/executor*.md | prompts/agents/executor-agent-prompt.md | Merge best of both |
| 5 | bin/scout-*.py | agents/scout/scout-agent.sh | Consolidate to engine |
| 6 | bin/planner-*.py | agents/planner/planner-agent.sh | Consolidate to engine |
| 7 | bin/executor-*.py | agents/executor/executor-agent.sh | Consolidate to engine |

### Template vs Implementation

| Component | Engine (Template) | Project (Implementation) |
|-----------|-------------------|--------------------------|
| Queue | 61-line template | 1,975-line full system |
| Events | 66-line template | 2,116-line event log |
| Tasks | 66-line template | 90+ active tasks |
| Memory | Basic structure | Vector store, CLI, models |
| 6-Agent Pipeline | Orchestrator prompt | Full implementation |

**Recommendation:** Engine should have generic templates; Project has active implementations.

---

## Recommended Migration Strategy

### Phase 1: Path Abstraction (Week 1) - CRITICAL

Create a path resolution library that both engine and project use.

```bash
# 2-engine/.autonomous/lib/paths.sh
get_engine_path() { ... }
get_project_path() { ... }
get_routes_path() { ... }
```

Update all 47+ hardcoded paths to use the abstraction.

### Phase 2: Content Migration (Week 2-3)

**Move to Project:**
- All 8 bin/ scripts from engine
- 3 cloud-control skills
- 7 .autonomous/ folders

**Move to Engine:**
- 11 generic bin/ scripts from project
- 8 operations/ frameworks
- 9 agent patterns

### Phase 3: Consolidation (Week 4)

- Merge duplicate prompts
- Make routes.yaml hierarchical (engine = base, project = overlay)
- Remove deprecated templates

### Phase 4: Cleanup (Week 5)

- Archive old scripts
- Update documentation
- Verify no hardcoded paths remain

---

## Immediate Action Items

1. **Fix routes.yaml** - Correct the incorrect path nesting
2. **Create path abstraction library** - Before any migration
3. **Update 6 critical scripts** - scout-intelligent.py, executor-implement.py, etc.
4. **Document the boundary** - Create ENGINE_PROJECT_BOUNDARY.md

---

## Success Criteria

- [ ] Zero hardcoded cross-boundary paths
- [ ] Clear separation: engine = generic, project = specific
- [ ] Path abstraction library used everywhere
- [ ] No duplications (merged or removed)
- [ ] All tests pass after migration

---

## Related Documents

- `STRUCTURAL_ISSUES_MASTER_LIST.md` - All 8 structural issues
- `engine-content-analysis.md` - Detailed engine content review
- `project-content-analysis.md` - Detailed project content review
- `cross-boundary-paths.md` - All 47 hardcoded paths
- `engine-project-duplications.md` - All 18 duplications
- `migration-strategy.md` - Detailed migration plan

---

*Analysis completed by 5 sub-agents on 2026-02-06*
