# Scout Report: Data Flow and State Ownership Analysis

**Scout:** Architecture Analysis Agent
**Date:** 2026-02-06
**Status:** Complete

---

## Key Findings

### 1. Task State Flow Issues

**Current State Ownership Problems:**
- **Task status exists in multiple locations** with no clear single source of truth:
  - `queue.yaml` - queue status (90 tasks tracked)
  - Individual task files (`tasks/active/TASK-XXX/task.md`) - task status
  - `events.yaml` - event log with status changes
  - Timeline.yaml - milestone tracking

- **Status propagation is inconsistent**: The queue.yaml shows 25 completed, 5 in_progress, 60 pending, but individual task files may not reflect this consistently.

**Data Flow Diagram (Current):**
```
Task Creation → task.md (file)
      ↓
queue.yaml (manual sync) ← LLM-based (0% success rate)
      ↓
events.yaml (hook-based logging)
      ↓
timeline.yaml (milestones only)
```

**Structural Issues Identified:**
- **No clear state ownership**: Queue owns priority/ordering, task files own details, events own history
- **Race condition risk**: Multiple agents can modify queue.yaml simultaneously (no file locking)
- **Inconsistent formats**: queue.yaml uses YAML list, task.md uses markdown frontmatter

---

### 2. Agent Communication Flow

**Current Architecture:**
- **Events system**: `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/.autonomous/agents/communications/events.yaml` logs agent_start/agent_stop events
- **Queue system**: `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/.autonomous/agents/communications/queue.yaml` contains 90 tasks with full metadata

**Critical Issue - Agent Identity Loss:**
All events show `agent_type: "unknown"` and `agent_id: "unknown-XXXX"` because hooks cannot determine agent context. This makes the event log nearly useless for tracing.

**Communication Pattern:**
```
Hook (SessionStart) → Log event → Agent runs → Hook (Stop) → Log event
                              ↓
                    No inter-agent communication
```

---

### 3. Configuration Flow

**Routes.yaml Analysis:**
- **BlackBox5 routes**: `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/.autonomous/context/routes.yaml` - 96 lines, well-structured
- **Engine routes**: `/Users/shaansisodia/.blackbox5/.autonomous/routes.yaml` - 30 lines, template placeholders not filled
- **2-engine routes**: `/Users/shaansisodia/.blackbox5/2-engine/.autonomous/routes.yaml` - similar structure

**Configuration Propagation Issues:**
- **47 hardcoded paths** crossing engine/project boundaries
- **routes.yaml has incorrect paths** (10+ paths with wrong nesting)
- **No unified configuration loading**: Each component parses routes.yaml independently

---

### 4. Memory/Insights Flow

**Current State:**
- **Decisions**: `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/.autonomous/memory/decisions/registry.md` - Template exists, 0 decisions logged
- **Knowledge**: `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/knowledge/` - Research and analysis documents
- **Insights**: `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/knowledge/analysis/` - 20+ analysis files

**Insights Capture Problems:**
- **No automated insight extraction**: Analysis files created manually
- **No insight retrieval mechanism**: Knowledge exists but no query interface
- **Master inefficiency list** exists but no tracking of fixes

---

## State Ownership Matrix

| Component | Owns | Reads | Writes | Issues |
|-----------|------|-------|--------|--------|
| Task System | Task details, status | queue.yaml | task.md, queue.yaml | Dual write, no sync |
| Queue System | Priority, ordering | task.md | queue.yaml | Manual updates |
| Events System | Event history | N/A | events.yaml | No agent identity |
| Timeline | Milestones | tasks, events | timeline.yaml | Manual updates |
| Routes | Paths, config | N/A | routes.yaml | Hardcoded paths |
| Skills | Skill definitions | skill-usage.yaml | N/A | 0% usage recorded |

---

## Priority Recommendations

**CRITICAL (Fix Immediately):**

1. **Implement Single Source of Truth for Task State**
   - Make task.md files the canonical source
   - Generate queue.yaml from scanning task files
   - Remove manual queue updates

2. **Fix Agent Identity in Events**
   - Pass agent context via environment variables
   - Update hooks to capture agent_type/agent_id
   - Currently all events show "unknown"

**HIGH (Fix This Week):**

3. **Add File Locking for Queue Updates**
   - Race condition in queue.yaml updates
   - Multiple agents can corrupt the file

4. **Create Storage Abstraction Layer**
   - Direct YAML manipulation throughout codebase
   - No transaction support
   - Hard to test, hard to change backends

**MEDIUM (Fix When Convenient):**

5. **Unify Configuration Loading**
   - Centralize routes.yaml parsing
   - Remove 47 hardcoded paths
   - Create path resolution library

6. **Implement Automated Insight Capture**
   - Extract insights from run folders automatically
   - Create query interface for knowledge base

---

## Files Analyzed

Key files examined:
- `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/.autonomous/agents/communications/queue.yaml` (1975 lines, 90 tasks)
- `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/.autonomous/agents/communications/events.yaml` (2830+ events)
- `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/.autonomous/context/routes.yaml`
- `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/.autonomous/analysis/STRUCTURAL_ISSUES_MASTER_LIST.md`
- `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/knowledge/analysis/master-inefficiency-list.md`
- 80+ task files in `tasks/active/`

---

## Related Tasks

This analysis relates to:
- TASK-ARCH-016: Agent Execution Flow
- TASK-ARCH-003: SSOT Violations (completed)
- TASK-ARCH-060 through TASK-ARCH-067: Engine/Project boundary fixes
- TASK-PROC-004: Task-to-Completion Pipeline Stall
