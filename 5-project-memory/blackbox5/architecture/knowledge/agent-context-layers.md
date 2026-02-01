# Agent Context Layers - Planning Document

**Date**: 2026-01-31
**Type**: Planning Session Output
**Status**: Proposed

---

## Summary

Planning session to define the layers of context that autonomous agents (RALF) need to work effectively within Blackbox5.

---

## The Problem

The user asked: "Why is STATE.yaml in the root and timeline in the _meta folder?"

This highlighted architectural inconsistency in our project memory structure. More importantly, it revealed that we haven't clearly defined what context agents need and where it should live.

---

## Layers of Context Required

### Layer 1: System Context (The "Where")

**What agents need to know**:
- Where everything is located in Blackbox5
- Directory structure and purposes
- Where to put new code/files
- Critical file locations

**Current sources**:
- SYSTEM-MAP.yaml (machine-readable structure)
- ARCHITECTURE.md (comprehensive system design)
- CORE-STRUCTURE.md (engine navigation)

**Gap**: No single "where everything goes" document

**Solution**: Create ARCHITECTURE-GUIDE.md at Blackbox5 root

---

### Layer 2: Project Context (The "What")

**What agents need to know**:
- Current project goals and objectives
- Active features being built
- Current project state
- What's been done vs what's pending

**Current sources**:
- STATE.yaml (single source of truth)
- timeline.yaml (milestones)
- WORK-LOG.md (chronological work)
- ACTIVE.md (dashboard)

**Gap**: Inconsistent file locations (STATE at root, timeline in _meta)

**Solution**: Standardize all state files at root level

---

### Layer 3: Task Context (The "Now")

**What agents need to know**:
- Active tasks for the current project
- Task dependencies and priorities
- Recent completed tasks
- What's blocking what

**Current sources**:
- tasks/active/ folder
- tasks/completed/ folder
- STATE.yaml active_tasks section

**Gap**: Tasks are scattered across files

**Solution**: Include in consolidated context.yaml

---

### Layer 4: Agent Context (The "Self")

**What agents need to know**:
- Agent's own timeline/changelog
- Previous runs and their outcomes
- Learnings and patterns
- Version history

**Current sources**:
- runs/ folders (per-run documentation)
- decision_registry.md (global decisions)

**Gap**: No unified agent timeline/changelog

**Solution**: Create timeline.yaml in ralf-core/.autonomous/

---

### Layer 5: Changelog Context (The "History")

**What agents need to know**:
- What changed recently
- Why things changed (decisions)
- Agent evolution
- Project evolution

**Current sources**:
- decisions/ folder
- WORK-LOG.md
- Git history

**Gap**: No consolidated changelog

**Solution**: Include in context.yaml changelog section

---

## Proposed Solution: context.yaml

A single auto-generated YAML file that aggregates all context layers:

```yaml
# context.yaml - Complete context for autonomous agents
# Auto-generated from STATE.yaml, timeline.yaml, run folders

system:
  version: "2.0"
  architecture_version: "5.0.0"
  last_updated: "2026-01-31T19:30:00Z"

  paths:
    engine: "2-engine/"
    core: "2-engine/core/"
    runtime: "2-engine/runtime/"
    tools: "2-engine/tools/"
    docs: "1-docs/"

  consolidation:
    completed: true
    old_paths_deprecated: true
    mappings:
      "2-engine/01-core/": "2-engine/core/"
      "2-engine/02-agents/": "2-engine/core/agents/"
      # ... etc

project:
  name: "siso-internal"
  status: "active"

  goals:
    primary: "Build user profile system"
    secondary: ["GitHub integration", "Project memory reorganization"]

  active_features:
    - id: "user-profile"
      name: "User Profile Page"
      status: "planning_complete"
      progress: 50

  current_state:
    tasks_completed: 4
    tasks_total: 23
    milestones_completed: 6
    milestones_total: 9

tasks:
  active:
    - id: "TASK-2026-01-18-005"
      name: "Sync User Profile to GitHub"
      priority: "high"

  recent_completed:
    - id: "TASK-2026-01-18-004"
      name: "Project Memory System Migration"
      completed_at: "2026-01-19"

agent:
  name: "RALF"
  version: "2.5"

  timeline:
    - date: "2026-01-31"
      event: "Fixed YAML agent loading"
      version: "2.5"

  recent_runs:
    - run_id: "run-20260131-182500"
      task: "TASK-001"
      status: "completed"
      summary: "Fixed RALF loop continuity"

changelog:
  project:
    - date: "2026-01-19"
      change: "Reduced folders from 18 to 6"
      type: "reorganization"

  agent:
    - date: "2026-01-31"
      change: "Simplified task selection, removed telemetry"
      version: "2.5"
```

---

## File Location Standardization

**Current Inconsistency**:
- STATE.yaml → root
- timeline.yaml → _meta/
- WORK-LOG.md → root
- ACTIVE.md → root

**Proposed Standard**:
All project state files at root for discoverability:

| File | Location | Purpose |
|------|----------|---------|
| STATE.yaml | Root | Single source of truth |
| timeline.yaml | Root | Milestones and events |
| context.yaml | .autonomous/ | Auto-generated agent context |
| WORK-LOG.md | Root | Chronological work log |
| ACTIVE.md | Root | Dashboard of active work |

---

## Implementation Plan

1. **Create ARCHITECTURE-GUIDE.md** at Blackbox5 root
   - Consolidate SYSTEM-MAP.yaml, ARCHITECTURE.md, CORE-STRUCTURE.md
   - Focus on "where everything goes"
   - Include consolidation mappings

2. **Create context.yaml generator script**
   - Read from STATE.yaml, timeline.yaml, run folders
   - Generate consolidated context.yaml
   - Run before each RALF invocation

3. **Standardize file locations**
   - Move timeline.yaml from _meta/ to root
   - Update all references
   - Deprecate _meta/ folder

4. **Create agent changelog system**
   - timeline.yaml in ralf-core/.autonomous/
   - Track agent versions, changes, learnings

5. **Update ralf.md**
   - Load context.yaml as primary context source
   - Reference ARCHITECTURE-GUIDE.md

---

## Open Questions

1. Should context.yaml be checked into git or gitignored (auto-generated)?
2. How often should context.yaml be regenerated?
3. Should there be a context.yaml per project or a global one?
4. How do we handle agent context across multiple projects?

---

## Related Documents

- DEC-2026-01-31-agent-context-architecture.md (decision record)
- SYSTEM-MAP.yaml (machine-readable structure)
- AGENTS.md (behavioral contract)
- ralf.md (RALF prompt)

---

**Next Step**: Create ARCHITECTURE-GUIDE.md
