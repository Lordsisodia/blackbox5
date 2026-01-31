# Project Relationships Analysis

**Task:** TASK-1769892005
**Date:** 2026-02-01
**Purpose:** Map cross-project dependencies within the BlackBox5 ecosystem

---

## Executive Summary

The BlackBox5 ecosystem consists of **5 interconnected projects** with varying levels of dependency. The most critical insight is that **blackbox5** (this project) serves as the improvement engine for the entire ecosystem, while **2-engine** provides the execution framework for all project memories.

### Key Findings

1. **Centralized Configuration**: `~/.claude/CLAUDE.md` affects all projects simultaneously
2. **Engine Dependency**: All project memories depend on 2-engine for BMAD skills and workflows
3. **Pattern Replication**: siso-internal serves as the gold standard for project organization
4. **Feedback Loop**: blackbox5 improvements flow back to the engine, benefiting all projects

---

## Project Inventory

### 1. blackbox5 (This Project)
- **Path**: `5-project-memory/blackbox5/`
- **Type**: Project Memory (Framework)
- **Purpose**: Self-improvement project for the Blackbox5 autonomous agent framework
- **Priority**: Critical
- **Status**: Active

**Key Files**:
- `STATE.yaml` - Comprehensive project state (590 lines)
- `goals.yaml` - 5 improvement goals defined
- `.autonomous/routes.yaml` - Full Blackbox5 access routes

### 2. siso-internal
- **Path**: `5-project-memory/siso-internal/`
- **Type**: Project Memory (Application)
- **Purpose**: SISO web application - reference implementation
- **Priority**: High
- **Status**: Active

**Key Files**:
- `STATE.yaml` - Single source of truth
- `.Autonomous/LEGACY.md` - Operational procedures
- `QUERIES.md` - Common queries for AI agents

### 3. 2-engine (RALF Engine)
- **Path**: `2-engine/.autonomous/`
- **Type**: Engine
- **Purpose**: Autonomous agent engine with BMAD framework
- **Priority**: Critical
- **Status**: Active

**Key Files**:
- `routes.yaml` - BMAD command routing
- `skills/` - 31 BMAD skills
- `workflows/` - Reusable workflow patterns
- `shell/ralf-loop.sh` - Core execution loop

### 4. team-entrepreneurship-memory
- **Path**: `5-project-memory/team-entrepreneurship-memory/`
- **Type**: Project Memory
- **Purpose**: Team entrepreneurship project
- **Priority**: Medium
- **Status**: Active

### 5. 6-roadmap
- **Path**: `6-roadmap/`
- **Type**: Research
- **Purpose**: Research, roadmaps, and strategic planning
- **Priority**: Medium
- **Status**: Active

---

## Dependency Analysis

### Dependency Graph

```
                    ~/.claude/CLAUDE.md
                           │
           ┌───────────────┼───────────────┐
           │               │               │
           ▼               ▼               ▼
    ┌──────────┐    ┌──────────┐    ┌──────────┐
    │blackbox5 │◄──►│ 2-engine │◄──►│siso-int. │
    └────┬─────┘    └────┬─────┘    └────┬─────┘
         │               │               │
         │               ▼               │
         │      ┌──────────┐            │
         │      │  team-   │            │
         │      │entreprene│            │
         │      └──────────┘            │
         │                              │
         └──────────►X◄─────────────────┘
              (pattern replication)
```

### Critical Dependencies

#### 1. blackbox5 → 2-engine
- **Type**: Core dependency
- **Impact**: Critical
- **References**:
  - `../../2-engine/.autonomous/routes.yaml`
  - `../../2-engine/.autonomous/skills/`
  - `../../2-engine/.autonomous/workflows/`
- **Notes**: blackbox5 cannot function without the engine's BMAD framework

#### 2. siso-internal → 2-engine
- **Type**: Tool usage
- **Impact**: High
- **Notes**: Uses BMAD skills for task execution

#### 3. blackbox5 ↔ siso-internal
- **Type**: Pattern reference
- **Impact**: Medium
- **Notes**: blackbox5 references siso-internal as gold standard

#### 4. All Projects → CLAUDE.md
- **Type**: Shared configuration
- **Impact**: Critical
- **Notes**: Changes affect all projects immediately

---

## Shared Files Analysis

### 1. ~/.claude/CLAUDE.md
- **Type**: User instructions
- **Impact**: Universal
- **Referenced in**:
  - `blackbox5/goals.yaml` (IG-001)
  - `blackbox5/decisions/technical/DEC-2026-02-01-continuous-improvement-framework.md`
  - `2-engine/.autonomous/skills/continuous-improvement.md`
- **Update Frequency**: Monthly
- **Risk**: High - changes affect all projects

### 2. 2-engine/.autonomous/routes.yaml
- **Type**: Configuration
- **Impact**: Critical
- **Referenced in**:
  - `blackbox5/.autonomous/routes.yaml`
  - `2-engine/.autonomous/prompts/ralf.md`
- **Purpose**: BMAD command routing

### 3. siso-internal/.Autonomous/LEGACY.md
- **Type**: Operational procedures
- **Impact**: High
- **Referenced in**:
  - `blackbox5/decisions/technical/DEC-2026-02-01-continuous-improvement-framework.md`
- **Purpose**: Legacy RALF procedures

---

## Common Patterns Detected

### Pattern 1: STATE.yaml as Single Source of Truth
**Projects using**: blackbox5, siso-internal, 6-roadmap

**Benefits**:
- Consistent project navigation
- Machine-readable status
- Self-documenting structure

**Implementation**:
```yaml
project:
  name: "project-name"
  version: "x.y.z"
  status: "active"
```

### Pattern 2: routes.yaml for Path Management
**Projects using**: blackbox5, 2-engine

**Benefits**:
- Centralized path management
- BMAD command routing
- Cross-project navigation

### Pattern 3: 6-Folder Organization
**Projects using**: blackbox5, siso-internal

**Structure**:
- `project/` - WHO are we?
- `plans/` - WHAT are we building?
- `decisions/` - WHY are we doing it this way?
- `knowledge/` - HOW does it work?
- `tasks/` - WHAT needs to be done?
- `operations/` - System operations

### Pattern 4: Autonomous Task System
**Projects using**: blackbox5, siso-internal

**Structure**:
- `tasks/active/` - Pending tasks
- `tasks/completed/` - Finished tasks
- `runs/` - Execution history

### Pattern 5: .docs/ System
**Projects using**: blackbox5

**Purpose**: AI-managed documentation separate from human docs

---

## Cross-Project Reference Patterns

### From grep analysis (50+ references found):

1. **Path References**:
   - `~/.blackbox5/` - Absolute home directory references
   - `../../2-engine/` - Relative path references
   - `5-project-memory/` - Project memory references

2. **File References**:
   - `CLAUDE.md` - Referenced in 20+ locations
   - `STATE.yaml` - Referenced in decision records
   - `routes.yaml` - Referenced in prompts and configs

3. **Common Reference Locations**:
   - `decisions/` - Technical decisions reference multiple projects
   - `.docs/` - Documentation references patterns from other projects
   - `runs/` - Execution logs reference cross-project files

---

## Recommendations for Context Gathering

### For Planner Agent

1. **Always read routes.yaml first** when planning cross-project tasks
2. **Check this project-map.yaml** to identify affected projects
3. **Reference STATE.yaml** for project structure understanding
4. **Consider CLAUDE.md impact** when planning improvements

### For Executor Agent

1. **Validate paths exist** before attempting reads
2. **Use routes.yaml** for path resolution, not hardcoded paths
3. **Cache frequently accessed** shared files
4. **Check for duplicate tasks** across project boundaries

### For Both Agents

1. **Follow the heuristic**: If BMAD commands involved → Read 2-engine/routes.yaml
2. **Follow the heuristic**: If project structure involved → Reference siso-internal
3. **Follow the heuristic**: If documentation involved → Check all .docs/ folders

---

## Risk Areas

### High Severity

1. **CLAUDE.md Changes**
   - Risk: Changes affect all projects simultaneously
   - Mitigation: Test in blackbox5 first, validate before applying

2. **Engine Updates**
   - Risk: 2-engine changes may break project integrations
   - Mitigation: Version routes.yaml, maintain backward compatibility

### Medium Severity

3. **Path References**
   - Risk: Hardcoded paths may break if structure changes
   - Mitigation: Use routes.yaml for all path resolution

4. **Skill Dependencies**
   - Risk: Skills may reference non-existent files
   - Mitigation: Validate paths before execution

---

## Impact on IG-003 (System Flow Improvement)

This analysis directly addresses **IG-003: Improve System Flow and Code Mapping**:

### Current Issues Addressed:
- ✅ **"Cross-project dependencies sometimes missed"** - Now documented in project-map.yaml
- ✅ **"Context gathering can be inefficient"** - Context gathering heuristics provided

### Improvement Ideas Implemented:
- ✅ **"Build project relationship map"** - Completed with this analysis
- ✅ **"Optimize context gatherer prompts"** - Recommendations provided
- ✅ **"Create dependency detection heuristics"** - Heuristics documented

### Success Criteria Tracking:
- **Fewer 'missed file' errors** - Can be measured by tracking errors before/after
- **Faster context acquisition** - Can be measured by run duration
- **Better cross-project awareness** - Achieved through project-map.yaml

---

## Next Steps

1. **Integrate project-map.yaml into run initialization**
   - Update run initialization to reference this map
   - Add validation that required projects exist

2. **Create cross-project task detection**
   - Add heuristic to detect when tasks span multiple projects
   - Auto-suggest reading project-map.yaml

3. **Monitor effectiveness**
   - Track 'missed file' errors over next 10 runs
   - Measure context gathering time
   - Review and update this map monthly

4. **Expand to other projects**
   - Create similar maps for siso-internal and team-entrepreneurship-memory
   - Document their specific cross-project dependencies

---

## Files Created

1. `operations/project-map.yaml` - Machine-readable project relationship map
2. `knowledge/analysis/project-relationships.md` - This analysis document

---

## Conclusion

The BlackBox5 ecosystem has clear dependency patterns centered around the 2-engine framework and shared configuration files. The most critical insight is that **improvements to blackbox5 flow back to the engine, benefiting all projects**. This creates a virtuous cycle where improving one project improves the entire ecosystem.

The project-map.yaml should be treated as a living document, updated whenever new cross-project dependencies are discovered or when project structures change.
