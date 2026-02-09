# GSD-BlackBox5 Hybrid Roadmap

**Analysis Date:** 2026-02-07
**Source:** https://github.com/glittercowboy/get-shit-done
**Goal:** Adopt GSD simplicity with BlackBox5 power

---

## Executive Summary

Get-Shit-Done (GSD) is a lightweight spec-driven development framework that achieves remarkable effectiveness through:
1. **Context engineering** - XML-structured prompts
2. **Thin orchestration** - Spawning agents instead of doing work
3. **Fresh contexts** - 200k tokens per agent, zero accumulated garbage
4. **Simplicity** - 26 commands that "just work"

BlackBox5 has superior infrastructure (RALF, skills, memory systems) but suffers from complexity overhead. This roadmap defines the path to GSD-style simplicity while preserving BB5's power.

---

## Phase 1: XML Prompt Formatting (Immediate)

### 1.1 Adopt GSD Task Schema

**Current:** Markdown task descriptions
**Target:** XML-structured tasks

```xml
<task type="auto">
  <name>Task N: [Action-oriented name]</name>
  <files>path/to/file1.ts, path/to/file2.ts</files>
  <action>
    [Specific implementation instructions]
    [What to avoid and WHY]
    [Technical constraints]
  </action>
  <verify>[Command or check to prove completion]</verify>
  <done>[Measurable acceptance criteria]</done>
</task>
```

**Implementation:**
- [ ] Create XML task templates in `2-engine/.autonomous/templates/tasks/`
- [ ] Update all agent prompts to use XML structure
- [ ] Add validation for task XML schema
- [ ] Document migration path from markdown tasks

### 1.2 Semantic Container Tags

**Adopt these GSD patterns:**

| Tag | Purpose | BB5 Location |
|-----|---------|--------------|
| `<objective>` | Goal statement with Purpose/Output | Agent prompts |
| `<execution_context>` | File references using `@` prefix | Agent prompts |
| `<process>` | Step-by-step workflow | Agent prompts |
| `<role>` | Agent identity | Agent prompts |
| `<success_criteria>` | Checkbox validation | Task definitions |
| `<critical_rules>` | Non-negotiable constraints | Agent prompts |

### 1.3 Checkpoint System

**New for BB5 - Human-in-the-loop:**

```xml
<task type="checkpoint:human-verify" gate="blocking">
  <what-built>[What Claude automated]</what-built>
  <how-to-verify>
    [Exact steps to test]
  </how-to-verify>
  <resume-signal>Type "approved" or describe issues</resume-signal>
</task>
```

Types:
- `checkpoint:human-verify` - Visual/functional checks
- `checkpoint:decision` - Implementation choices
- `checkpoint:human-action` - Manual steps only

---

## Phase 2: Simplified CLI (High Priority)

### 2.1 Flat Command Namespace

**Current:** `bb5 goal:create`, `bb5 plan:create`, `bb5 task:create`
**Target:** GSD-style flat commands

| Current | Proposed | GSD Equivalent |
|---------|----------|----------------|
| `bb5 goal:create` | `bb5:new-goal` | `/gsd:new-milestone` |
| `bb5 plan:create` | `bb5:new-plan` | `/gsd:plan-phase` |
| `bb5 task:create` | `bb5:new-task` | `/gsd:plan-phase` |
| `bb5 task:current` | `bb5:progress` | `/gsd:progress` |
| `bb5 task:list` | `bb5:status` | `/gsd:progress` |
| N/A | `bb5:pause` | `/gsd:pause-work` |
| N/A | `bb5:resume` | `/gsd:resume-work` |
| N/A | `bb5:execute` | `/gsd:execute-phase` |
| N/A | `bb5:verify` | `/gsd:verify-work` |
| N/A | `bb5:quick` | `/gsd:quick` |

### 2.2 Smart Command Aliases

**Single-word execution:**
```bash
bb5:do "Implement user authentication"  # Creates, plans, executes
bb5:next                               # Execute next pending task
bb5:done                               # Mark current task complete
```

### 2.3 Context-Aware Commands

**Auto-detect current context:**
```bash
bb5:new           # Creates goal/plan/task based on current directory
bb5:link          # Links current item to parent (auto-detects type)
bb5:up            # Go up hierarchy (like current bb5 up)
bb5:down [id]     # Go down to child
```

---

## Phase 3: State Management Overhaul

### 3.1 STATE.md Digest Pattern

**Current:** `STATE.yaml` (machine-readable, unbounded)
**Target:** `STATE.md` (human-readable, <100 lines)

```markdown
# Project State

## Project Reference
See: PROJECT.md (updated 2026-02-07)
**Core value:** One-liner from PROJECT.md
**Current focus:** Current task/goal name

## Current Position
Goal: [X] of [Y] ([Goal name])
Plan: [A] of [B] in current goal
Task: [C] of [D] in current plan
Status: [Ready to plan / Planning / Ready to execute / In progress / Complete]
Last activity: 2026-02-07 — What happened
Progress: [░░░░░░░░░░] 0%

## Performance Metrics
**Velocity:**
- Total tasks completed: [N]
- Average duration: [X] min
- Total execution time: [X.X] hours

**Recent Trend:**
- Last 5 tasks: [durations]
- Trend: [Improving / Stable / Degrading]

## Accumulated Context
### Decisions
- [TASK-XXX]: Decision summary
- [GOAL-YYY]: Decision summary

### Pending Todos
- [From todos/ directory]

### Blockers/Concerns
- [Issues affecting future work]

## Session Continuity
Last session: 2026-02-07 14:30
Stopped at: Description of last action
Resume file: .continue-here.md (or "None")
```

### 3.2 Session Handoff Files

**New: `.continue-here.md`**

```yaml
---
goal: GOAL-XXX
plan: PLAN-YYY
task: TASK-ZZZ
total_tasks: 10
status: in_progress
last_updated: 2026-02-07T14:30:00Z
---
```

**Sections:**
- `<current_state>` - Where exactly are we?
- `<completed_work>` - Specific items done
- `<remaining_work>` - What's left
- `<decisions_made>` - Key decisions and why
- `<blockers>` - Stuck items
- `<context>` - Mental state
- `<next_action>` - First thing to do

**Commands:**
```bash
bb5:pause    # Creates .continue-here.md
bb5:resume   # Reads .continue-here.md, deletes after success
```

### 3.3 Enhanced RESULTS.md

**Add YAML frontmatter:**

```yaml
---
task: TASK-XXX
requires: [TASK-YYY, TASK-ZZZ]
provides: [deliverables list]
affects: [dependent tasks]
duration: 45min
completed: 2026-02-07T14:30:00Z
key-decisions:
  - "Decision 1"
patterns-established:
  - "Pattern: description"
---
```

---

## Phase 4: Agent Orchestration Improvements

### 4.1 Thin Orchestrator Pattern

**Current:** RALF does heavy lifting
**Target:** RALF coordinates only, agents do work

**Benefits:**
- Main context stays at 30-40%
- No context rot
- Parallel execution possible

### 4.2 Parallel Research Phase

**Current:** Sequential scout
**Target:** 4 parallel researchers (like GSD)

```
Research Phase:
├── Stack Researcher (technology investigation)
├── Features Researcher (feature analysis)
├── Architecture Researcher (system design)
└── Pitfalls Researcher (risk analysis)
```

**Implementation:**
- [ ] Create 4 specialized scout variants
- [ ] Add parallel execution to RALF
- [ ] Integrate findings before planning

### 4.3 Wave-Based Execution

**Current:** Sequential or limited parallel
**Target:** Dependency-based waves

```
Wave 1: Independent tasks (parallel)
Wave 2: Tasks depending on Wave 1 (parallel)
Wave 3: Tasks depending on Wave 2 (parallel)
```

### 4.4 Fresh Context Per Agent

**Current:** Shared context accumulates
**Target:** 200k fresh context per agent

**Implementation:**
- Spawn each agent with clean context
- Pass only relevant state
- Track context window usage

### 4.5 Planner + Checker Loop

**Current:** Single planner
**Target:** Iterative planning with validation

```
Planner creates plan → Checker validates → If fails, revise → Repeat until pass
```

### 4.6 Verifier + Debugger Loop

**Current:** Limited verification
**Target:** Explicit verification with auto-debug

```
Verifier checks work → If fails, Debugger diagnoses → Fix plan → Re-execute
```

---

## Phase 5: Documentation Consolidation

### 5.1 Single Entry Point

**Current:** Scattered documentation
**Target:** GSD-style consolidated README

**Per-project README.md:**
```markdown
# Project Name

## Quick Start
```bash
bb5:progress    # Where am I?
bb5:next        # Do next task
bb5:pause       # Take a break
```

## Project Files
- `PROJECT.md` - Vision and constraints
- `ROADMAP.md` - Where we're going
- `STATE.md` - Current position
- `tasks/` - Active and completed tasks

## Commands
See `bb5:help` for all commands.
```

### 5.2 Simplified File Structure

**Current:** Complex hierarchy
**Target:** Flatter structure

```
.autonomous/
├── PROJECT.md          # Project vision
├── ROADMAP.md          # Goals and plans
├── STATE.md            # Current position
├── tasks/
│   ├── active/         # Pending tasks
│   └── completed/      # Done tasks
├── runs/
│   └── run-YYYYMMDD_HHMMSS/
│       ├── THOUGHTS.md
│       ├── DECISIONS.md
│       └── RESULTS.md
└── todos/              # Captured ideas
```

---

## Phase 6: Git Integration

### 6.1 Atomic Commits

**Current:** Batch commits
**Target:** One commit per task

**Format:**
```
type(scope): description

- Detailed changes
- Task: TASK-XXX

Co-authored-by: Claude <claude@blackbox5.local>
```

### 6.2 Automatic Committing

**Add to bb5:execute:**
- Auto-commit after each task completion
- Enables git bisect for debugging
- Clear history of what changed when

---

## Implementation Priority

### Immediate (This Week)
1. XML task schema templates
2. Simplified CLI aliases (`bb5:new-goal`, etc.)
3. STATE.md format design

### Short-term (Next 2 Weeks)
1. Session handoff files (pause/resume)
2. Parallel research phase
3. Documentation consolidation

### Medium-term (Next Month)
1. Thin orchestrator refactor
2. Wave-based execution
3. Planner + checker loop
4. Verifier + debugger loop

### Long-term (Next Quarter)
1. Full GSD-BB5 hybrid maturity
2. Performance optimization
3. Advanced checkpoint system

---

## Success Metrics

| Metric | Current | Target |
|--------|---------|--------|
| Commands to start work | 5+ | 2 |
| Context window at phase end | 80%+ | 30-40% |
| Time to resume session | 10+ min | 1 min |
| Files to understand project | 10+ | 4 (PROJECT, ROADMAP, STATE, tasks) |
| Documentation entry points | Many | 1 |

---

## References

- GSD Framework: https://github.com/glittercowboy/get-shit-done
- Analysis Tasks: TASK-001, TASK-002
- Sub-agent Reports:
  - XML Patterns: a094601
  - Command Structure: a738a95
  - State Management: a9b13e7
  - Agent Orchestration: a9ee48f
