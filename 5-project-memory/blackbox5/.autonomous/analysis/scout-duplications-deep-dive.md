# Scout Report: Duplications Deep Dive Analysis

**Scout:** Architecture Analysis Agent
**Date:** 2026-02-06
**Status:** Complete

---

## Executive Summary

Comprehensive analysis of the 18 known duplication categories between the engine (`2-engine/.autonomous`) and project (`5-project-memory/blackbox5`).

| Category | Engine Version | Project Version | Recommendation | Priority |
|----------|---------------|-----------------|----------------|----------|
| 1. Routes Configuration | 138 lines, BMAD commands | 96 lines, project paths | **MERGE** - Engine is SSOT for BMAD, Project extends it | HIGH |
| 2. Queue System (YAML) | 61 lines, simple structure | 1975 lines, full task queue | **KEEP PROJECT** - Far more mature | CRITICAL |
| 3. Events System (YAML) | 65 lines, schema definition | 2424 lines, live event log | **KEEP PROJECT** - Active usage | HIGH |
| 4. Communication Protocol | Basic queue/events files | Full agent communications dir | **KEEP PROJECT** - More complete | HIGH |
| 5. Agent Prompts - Scout | `ralf-scout-improve.md` (217 lines) | None found | **KEEP ENGINE** - Only version exists | MEDIUM |
| 6. Agent Prompts - Planner | None found | None found | N/A - Neither has standalone | LOW |
| 7. Agent Prompts - Executor | `ralf-executor.md` (659 lines) | None found | **KEEP ENGINE** - Only version exists | MEDIUM |
| 8. Agent Scripts - Analyzer | `scout-analyze.py` (471 lines) | None found | **KEEP ENGINE** - Only version exists | MEDIUM |
| 9. Agent Scripts - Planner | `planner-prioritize.py` (441 lines) | None found | **KEEP ENGINE** - Only version exists | MEDIUM |
| 10. Agent Scripts - Scout | `scout-intelligent.py`, `scout-task-based.py` | None found | **KEEP ENGINE** - Only version exists | MEDIUM |
| 11. Task Management System | Basic structure | Full task system with 90 tasks | **KEEP PROJECT** - Far more mature | CRITICAL |
| 12. Skills System | `skills/README.md` only | None found | **KEEP ENGINE** - Only version exists | LOW |
| 13. Skill Router | Referenced in routes | None found | **KEEP ENGINE** - Only version exists | LOW |
| 14. Shell Scripts - RALF Loop | `ralf-loop.sh` (521 lines) | None found | **KEEP ENGINE** - Only version exists | MEDIUM |
| 15. Memory System | None found | Full memory system with vector store | **KEEP PROJECT** - Only version exists | HIGH |
| 16. Operations/Skill Metrics | None found | Full operations directory (21 files) | **KEEP PROJECT** - Only version exists | CRITICAL |
| 17. Decision Registry | Referenced in loop | None found | **KEEP ENGINE** - Referenced but not found | LOW |
| 18. 6-Agent Pipeline System | `bin/` has 6 agent scripts | None found | **KEEP ENGINE** - Only version exists | HIGH |

---

## Key Findings

### Single Source of Truth Recommendations

1. **Engine (2-engine/.autonomous)** should be SSOT for:
   - BMAD command routing and skill definitions
   - Agent prompts and execution scripts
   - RALF loop infrastructure
   - Core agent pipeline (Scout, Planner, Executor, Verifier)

2. **Project (5-project-memory/blackbox5)** should be SSOT for:
   - Task queue and task management
   - Event logging and history
   - Operations and skill metrics
   - Memory system (vector store, session memory)
   - Project-specific routes and configuration

3. **Merge Required:**
   - Routes configuration needs unification - Engine has BMAD commands, Project has paths
   - Both should reference each other rather than duplicate

---

## Critical Observations

1. **Massive Asymmetry**: The project version has 1975 lines in queue.yaml vs 61 lines in engine - the project version is the clearly mature implementation.

2. **Missing Duplicates**: Several categories (6, 11, 15, 16) only exist in one location, not both - these aren't true duplications.

3. **Active vs Static**: Engine files appear to be templates/definitions, while project files contain live data (2424 lines of events).

4. **No True Overlap**: Most categories are actually complementary rather than duplicated - the engine provides infrastructure, the project provides data.

---

## Priority Order for Consolidation

1. **CRITICAL**: Unify routes.yaml (engine has BMAD, project has paths - they need to reference each other)
2. **HIGH**: Ensure engine scripts reference project queue/events correctly
3. **MEDIUM**: Move any remaining agent prompts/scripts to engine if they're generic
4. **LOW**: Document the SSOT boundaries clearly

---

## Conclusion

The "duplication" is largely a separation of concerns: **Engine = Infrastructure/Definitions, Project = Data/Operations**. The consolidation needed is primarily about clear referencing and eliminating any actual redundant definitions (like routes.yaml having overlapping concerns).
