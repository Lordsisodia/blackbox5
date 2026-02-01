# DEC-2026-01-31: Agent Context Architecture

**Status**: Proposed
**Date**: 2026-01-31
**Author**: Claude (with User)
**Type**: Architectural

---

## Context

During a planning session, we identified that RALF autonomous agents need comprehensive context to work effectively. The user asked: "Why is STATE.yaml in the root and timeline in the _meta folder?" - highlighting the architectural inconsistency in our project memory structure.

This decision record captures our planning session and proposes a unified context system.

---

## Problem Statement

RALF autonomous agents need multiple layers of context to work effectively:

1. **System Context**: Where everything is in Blackbox5 (architecture, directories, consolidation status)
2. **Project Context**: Goals, active features, current state
3. **Task Context**: What needs to be done, dependencies, priorities
4. **Agent Context**: Agent's own timeline, previous runs, learnings
5. **Changelog Context**: What changed recently and why

**Current Issues**:
- STATE.yaml is at root, timeline.yaml is in _meta/ (inconsistent location)
- No single consolidated context file for agents
- Architecture knowledge is spread across multiple files
- No standardized agent changelog/timeline system

---

## Decision

Create a unified **Agent Context System** with the following components:

### 1. Architecture Guide Document

**Location**: `~/.blackbox5/ARCHITECTURE-GUIDE.md`

**Purpose**: Single source of truth for "where everything goes" in Blackbox5

**Contents**:
- Layer 1: Project Layout (The "Where") - Directory structure, critical paths
- Layer 2: Navigation Guide (The "How") - How to find agents, tools, memory
- Layer 3: Component Interactions (The "Why") - How systems work together
- Layer 4: Current State (The "Now") - Consolidation status, old vs new paths

**Update Policy**: Updated whenever structure changes

### 2. Project Context YAML

**Location**: `5-project-memory/<project>/.autonomous/context.yaml`

**Purpose**: Auto-generated consolidated context for agents

**Structure**:
```yaml
system:
  version: "2.0"
  architecture_version: "5.0.0"
  paths: { engine, core, runtime, tools, docs }
  consolidation: { completed, mappings }

project:
  name: "project-name"
  status: "active"
  goals: { primary, secondary }
  active_features: [...]
  current_state: { tasks_completed, tasks_total, ... }

tasks:
  active: [...]
  recent_completed: [...]

agent:
  name: "RALF"
  version: "2.5"
  timeline: [...]
  recent_runs: [...]

changelog:
  project: [...]
  agent: [...]
```

**Generation**: Script that aggregates from STATE.yaml, timeline.yaml, run folders

### 3. Standardized File Locations

**Decision**: All project state files go at root level for discoverability

| File | Location | Purpose |
|------|----------|---------|
| STATE.yaml | Root | Single source of truth |
| timeline.yaml | Root | Milestones and events |
| context.yaml | .autonomous/ | Auto-generated agent context |
| WORK-LOG.md | Root | Chronological work log |
| ACTIVE.md | Root | Dashboard of active work |

**Migration**: Move timeline.yaml from _meta/ to root for consistency

### 4. Agent Changelog System

**Location**: `5-project-memory/ralf-core/.autonomous/timeline.yaml`

**Purpose**: Track agent evolution, versions, and changes

**Format**: Same structure as project timeline.yaml for consistency

---

## Rationale

1. **Single File for Agents**: Agents need one file to load, not multiple
2. **YAML for Machines**: Easier for AI to parse than markdown
3. **Auto-Generated**: Ensures consistency, reduces manual work
4. **Consistent Locations**: All state files at root for discoverability
5. **Versioned Context**: Agents know if context has changed

---

## Implementation Steps

1. [ ] Create ARCHITECTURE-GUIDE.md at Blackbox5 root
2. [ ] Create context.yaml generator script
3. [ ] Move timeline.yaml to root (deprecate _meta/)
4. [ ] Create agent changelog system for RALF
5. [ ] Update ralf.md to load context.yaml
6. [ ] Document the new system

---

## Alternatives Considered

| Alternative | Pros | Cons | Decision |
|-------------|------|------|----------|
| Keep current structure | No migration work | Inconsistent, hard for agents | Rejected |
| JSON instead of YAML | Faster parsing | Harder for humans to edit | Rejected |
| Multiple context files | Separation of concerns | Agents load many files | Rejected |
| Database storage | Queryable | Adds complexity | Rejected |

---

## Impact

- **Consistency**: All state files in predictable locations
- **Agent Efficiency**: Single context file to load
- **Maintainability**: Auto-generated from existing sources
- **Clarity**: Architecture guide answers "where everything goes"

---

## Related

- SYSTEM-MAP.yaml (machine-readable structure)
- AGENTS.md (behavioral contract)
- ralf.md (RALF prompt)

---

**Next Action**: Create ARCHITECTURE-GUIDE.md and context.yaml generator
