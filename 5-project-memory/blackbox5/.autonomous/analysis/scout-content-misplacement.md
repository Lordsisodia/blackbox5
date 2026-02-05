# Scout Report: Content Misplacement Analysis

**Scout:** Architecture Analysis Agent
**Date:** 2026-02-06
**Status:** Complete

---

## Summary

Analyzed content distribution between Engine (2-engine/) and Project (5-project-memory/blackbox5/) to identify misplacement issues.

| Category | Count |
|----------|-------|
| Engine items to move to project | 8 |
| Project items to standardize (move to engine) | 11 |
| Correctly placed engine items | 25+ |
| Correctly placed project items | 15+ |

---

## Engine Items That Should Move to Project

| Item | Current Location | What It Does | Classification | Recommended Location | Migration Complexity |
|------|-----------------|--------------|----------------|---------------------|---------------------|
| **scout-intelligent.py** | 2-engine/.autonomous/bin/ | AI-powered improvement discovery using Claude Code subagents to analyze BlackBox5 specifically | **PROJECT-SPECIFIC** - Hardcoded paths to blackbox5 project directory, analyzes skill-metrics.yaml, operations/ files | 5-project-memory/blackbox5/bin/ | Low |
| **executor-implement.py** | 2-engine/.autonomous/bin/ | Implements quick wins for BlackBox5 improvements; references PROJECT_DIR as blackbox5 | **PROJECT-SPECIFIC** - Executes threshold fixes for skill-selection.yaml in blackbox5 | 5-project-memory/blackbox5/bin/ | Low |
| **improvement-loop.py** | 2-engine/.autonomous/bin/ | Master orchestrator for Scout->Planner->Executor->Verifier loop; hardcoded to blackbox5 | **PROJECT-SPECIFIC** - All paths point to blackbox5 project | 5-project-memory/blackbox5/bin/ | Low |
| **planner-prioritize.py** | 2-engine/.autonomous/bin/ | Prioritizes improvement opportunities from scout reports for blackbox5 | **PROJECT-SPECIFIC** - Uses blackbox5 paths exclusively | 5-project-memory/blackbox5/bin/ | Low |
| **verifier-validate.py** | 2-engine/.autonomous/bin/ | Validates improvement implementations in blackbox5 | **PROJECT-SPECIFIC** - Validates skill-selection.yaml changes in blackbox5 | 5-project-memory/blackbox5/bin/ | Low |
| **scout-task-based.py** | 2-engine/.autonomous/bin/ | Task-based scout using Claude Code Task tool for blackbox5 analysis | **PROJECT-SPECIFIC** - Hardcoded blackbox5 project paths | 5-project-memory/blackbox5/bin/ | Low |
| **ralf-improvement-loop.md** | 2-engine/.autonomous/prompts/ | Prompt for improvement loop specifically referencing BlackBox5 structure | **PROJECT-SPECIFIC** - Mentions blackbox5-specific files | 5-project-memory/blackbox5/.autonomous/prompts/ | Low |
| **ralf-scout-improve.md** | 2-engine/.autonomous/prompts/ | Scout prompt for finding improvements in BlackBox5 | **PROJECT-SPECIFIC** - References blackbox5-specific paths | 5-project-memory/blackbox5/.autonomous/prompts/ | Low |

---

## Project Items That Could Be Standardized

| Item | Current Location | What It Does | Classification | Recommended Location | Migration Complexity |
|------|-----------------|--------------|----------------|---------------------|---------------------|
| **bb5-health-dashboard.py** | 5-project-memory/blackbox5/bin/ | Real-time system health monitoring with generic patterns | **GENERIC** - Could work with any project using queue.yaml/events.yaml | 2-engine/.autonomous/bin/ | Medium |
| **bb5-metrics-collector.py** | 5-project-memory/blackbox5/bin/ | Task execution metrics tracking | **GENERIC** - Generic metrics collection framework | 2-engine/.autonomous/bin/ | Medium |
| **bb5-queue-manager.py** | 5-project-memory/blackbox5/bin/ | Task queue management with ROI prioritization | **GENERIC** - Standard queue management pattern | 2-engine/.autonomous/bin/ | Medium |
| **bb5-reanalysis-engine.py** | 5-project-memory/blackbox5/bin/ | Task reanalysis and priority management | **GENERIC** - Could work with any project | 2-engine/.autonomous/bin/ | Medium |
| **skill-selection.yaml** | 5-project-memory/blackbox5/operations/ | Framework for skill selection during task execution | **GENERIC** - General skill routing framework | 2-engine/.autonomous/config/ | Low |
| **skill-metrics.yaml** | 5-project-memory/blackbox5/operations/ | Skill effectiveness tracking | **GENERIC** - Generic skill metrics pattern | 2-engine/.autonomous/config/ | Low |
| **skill-usage.yaml** | 5-project-memory/blackbox5/operations/ | Skill usage tracking | **GENERIC** - Generic usage tracking | 2-engine/.autonomous/config/ | Low |
| **template-system-guide.md** | 5-project-memory/blackbox5/.docs/ | Template naming conventions and usage | **GENERIC** - Could apply to any project | 2-engine/.autonomous/.docs/ | Low |

---

## Correctly Placed Items (No Action Needed)

**Engine (Generic):**
- `/Users/shaansisodia/.blackbox5/2-engine/.autonomous/bin/scout-analyze.py` - Generic repo analysis
- `/Users/shaansisodia/.blackbox5/2-engine/.autonomous/bin/intelligent-scout.sh` - Generic scout wrapper
- `/Users/shaansisodia/.blackbox5/2-engine/.autonomous/shell/ralf-loop.sh` - Generic RALF loop (accepts project path)
- `/Users/shaansisodia/.blackbox5/2-engine/.autonomous/lib/skill_router.py` - Generic skill routing
- `/Users/shaansisodia/.blackbox5/2-engine/.autonomous/config/skill-registry.yaml` - Generic skill registry
- `/Users/shaansisodia/.blackbox5/2-engine/.autonomous/skills/` - All BMAD skills are generic

**Project (Specific):**
- `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/.autonomous/agents/scout/scout-agent.sh` - BlackBox5-specific paths
- `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/.autonomous/agents/planner/planner-agent.sh` - BlackBox5-specific
- `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/.autonomous/agents/communications/` - Project-specific event queue

---

## Priority Recommendations

### HIGH PRIORITY (Migrate First)

1. **Move Agent Improvement Loop scripts** from 2-engine/.autonomous/bin/ to project:
   - `scout-intelligent.py`
   - `executor-implement.py`
   - `improvement-loop.py`
   - `planner-prioritize.py`
   - `verifier-validate.py`
   - `scout-task-based.py`

   **Rationale:** These scripts are hardcoded to analyze and improve BlackBox5 specifically. They reference `~/.blackbox5/5-project-memory/blackbox5` paths throughout and cannot function for other projects.

### MEDIUM PRIORITY

2. **Move skill framework** from project to engine:
   - `skill-selection.yaml`
   - `skill-metrics.yaml`
   - `skill-usage.yaml`

   **Rationale:** These are generic skill management frameworks that could benefit any project using the BMAD skill system.

3. **Move BB5 utilities** from project to engine (with renaming):
   - `bb5-health-dashboard.py` -> `health-dashboard.py`
   - `bb5-metrics-collector.py` -> `metrics-collector.py`
   - `bb5-queue-manager.py` -> `queue-manager.py`
   - `bb5-reanalysis-engine.py` -> `reanalysis-engine.py`

   **Rationale:** These are generic task management utilities that could work with any project using the queue/events system.

### LOW PRIORITY

4. **Move documentation patterns**:
   - `template-system-guide.md` to engine documentation

---

## Key Insight

The Agent Improvement Loop (scout-intelligent.py, executor-implement.py, improvement-loop.py, planner-prioritize.py, verifier-validate.py) represents a complete improvement system that is tightly coupled to BlackBox5. This entire system should reside in the project directory, not the engine. The engine should provide generic RALF loop infrastructure (which it does via ralf-loop.sh), while project-specific improvement agents belong in the project.
