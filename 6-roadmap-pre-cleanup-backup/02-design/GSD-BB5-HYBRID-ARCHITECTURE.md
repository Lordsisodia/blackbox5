# GSD-BlackBox5 Hybrid Architecture

**Status:** Design Complete
**Goal:** Adopt GSD simplicity without losing BB5 power
**Migration:** Non-disruptive, existing workflows preserved

---

## Core Philosophy

> "Complexity should be in the system, not in the workflow"

Users experience simple, intuitive commands while the system handles sophisticated orchestration behind the scenes.

---

## Architecture Layers

### 1. Command Layer: GSD-Style Simplicity

**New flat command namespace:**

| GSD Command | BB5 Equivalent | Purpose |
|-------------|----------------|---------|
| `bb5:new-project` | `bb5 goal:create` + setup | Initialize project |
| `bb5:plan` | Research + `bb5 plan:create` | Research + plan |
| `bb5:execute` | RALF execution | Execute task |
| `bb5:next` | Get current + execute | Do next task |
| `bb5:progress` | `bb5 whereami` | "Where am I?" |
| `bb5:pause` | NEW | Create handoff state |
| `bb5:resume` | NEW | Restore session |
| `bb5:quick` | `bmad-quick-flow` | Ad-hoc task |

**Implementation:** Thin bash wrapper maps simple commands to BB5 infrastructure.

---

### 2. Task Layer: XML Schema

**Adopt GSD's XML task format:**

```xml
<task type="auto" id="TASK-XXX">
  <name>Create login endpoint</name>
  <files>src/app/api/auth/login/route.ts</files>
  <action>Use jose for JWT (not jsonwebtoken)</action>
  <verify>curl -X POST localhost:3000/api/auth/login</verify>
  <done>Valid credentials return cookie</done>
</task>
```

**Checkpoint tasks (human-in-the-loop):**

```xml
<task type="checkpoint:human-verify" gate="blocking">
  <what-built>Login form implemented</what-built>
  <how-to-verify>1. Go to /login 2. Try logging in</how-to-verify>
  <resume-signal>Type "approved" or describe issues</resume-signal>
</task>
```

**Migration:** XML tasks alongside existing markdown, agents parse both.

---

### 3. State Layer: STATE.md Digest

**Replace unbounded STATE.yaml with bounded STATE.md:**

```markdown
# Project State

## Current Position
Goal: [X] of [Y] ([Goal name])
Plan: [A] of [B] in current goal
Task: [C] of [D] in current plan
Status: [In progress]
Progress: [░░░░░░░░░░] 35%

## Performance Metrics
- Total tasks completed: 45
- Average duration: 45 min
- Trend: Improving

## Session Continuity
Last session: 2026-02-07 14:30
Resume file: .continue-here.md
```

**Session handoff:**
- `bb5:pause` → Creates `.continue-here.md`
- `bb5:resume` → Reads handoff file, restores context

---

### 4. Orchestration Layer: Thin Orchestrator

**Current (Heavy):** RALF does research + planning, context grows to 80%+

**Target (Thin):** RALF coordinates only, context stays at 30-40%

```
┌─────────────────────────────────────┐
│ RALF Orchestrator (coordinates)     │
│ Context: 30-40%                     │
├─────────────────────────────────────┤
│ ┌─────────┐ ┌─────────┐ ┌────────┐ │
│ │ Research│ │ Planner │ │Executor│ │
│ │  200k   │ │  200k   │ │  200k  │ │
│ │  fresh  │ │  fresh  │ │ fresh  │ │
│ └─────────┘ └─────────┘ └────────┘ │
└─────────────────────────────────────┘
```

**Parallel Research:**
- Stack researcher (technology)
- Features researcher (requirements)
- Architecture researcher (patterns)
- Pitfalls researcher (risks)

**Wave-Based Execution:**
- Wave 1: Independent tasks (parallel)
- Wave 2: Tasks depending on Wave 1 (parallel)
- Wave 3: Sequential final tasks

---

### 5. Agent Layer: Preserved BB5 Power

**All essential BB5 features preserved:**

| Feature | Preservation Strategy |
|---------|----------------------|
| **RALF** | Thin orchestrator mode |
| **23+ Skills** | Auto-invoke via XML task type |
| **ChromaDB Memory** | Selective load into fresh context |
| **Multi-Agent** | Spawn with clean contexts |
| **Superintelligence Protocol** | XML task type trigger |
| **BMAD Roles** | Map to XML task agents |

**Skill auto-invocation:**
```xml
<task type="skill:bmad-architect" confidence="85%">
  <name>Design authentication system</name>
</task>
```

---

### 6. Memory Layer: Selective Context Loading

**Load only relevant memories into fresh agent contexts:**

```
ChromaDB (all memories)
       │
       ▼ (vector search, relevance ≥ 0.7)
Relevant Context (top 10)
       │
       ▼ (spawn with fresh context)
Agent Context (200k)
```

---

## Migration Path (Non-Disruptive)

### Phase 1: Foundation (Week 1-2)
- Create `bb5` command wrapper
- Add STATE.md alongside STATE.yaml
- Implement `bb5:pause` / `bb5:resume`

### Phase 2: XML Integration (Week 3-4)
- Create XML task templates
- Update agents to parse both formats
- Add XML validation

### Phase 3: Thin Orchestrator (Week 5-8)
- Implement parallel research
- Add wave-based execution
- Fresh context per agent

### Phase 4: Optimization (Week 9-12)
- Planner + Checker loop
- Verifier + Debugger loop
- Atomic commits per task

**Existing workflows continue working throughout.**

---

## Key Trade-offs

| Decision | Trade-off | Mitigation |
|----------|-----------|------------|
| XML tasks | More verbose | Templates, validation |
| Thin orchestrator | More complex coordination | Clear agent contracts |
| Fresh context | Higher token usage | Selective loading, parallel savings |
| Dual state files | Maintenance overhead | Automated sync |

---

## Success Metrics

| Metric | Current | Target |
|--------|---------|--------|
| Commands to start | 5+ | 2 |
| Context at phase end | 80%+ | 30-40% |
| Time to resume | 10+ min | 1 min |
| Files to understand | 10+ | 4 |
| Task completion rate | 70% | 90% |
| Average task duration | 2 hours | 1 hour |

---

## Critical Implementation Files

1. `/Users/shaansisodia/.blackbox5/bin/bb5` - Command wrapper
2. `/Users/shaansisodia/.blackbox5/2-engine/.autonomous/templates/task.xml` - XML schema
3. `/Users/shaansisodia/.blackbox5/2-engine/core/orchestration/thin_orchestrator.py` - Thin orchestrator
4. `/Users/shaansisodia/.blackbox5/2-engine/.autonomous/workflows/parallel-research.yaml` - Parallel research
5. `/Users/shaansisodia/.blackbox5/bin/bb5-pause` and `bb5-resume` - Session handoff

---

## Design Document

Full architectural design: See sub-agent report `a9f6d55`
