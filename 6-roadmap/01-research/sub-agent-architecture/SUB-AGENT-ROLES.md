# Sub-Agent Roles (Refined)

**Date:** 2026-02-07

---

## Core Sub-Agents (We Need These)

### 1. Task Validator
Validates that completed work matches requirements.

**When:** After main agent claims task completion
**Inputs:** Task requirements, claimed changes, actual changes
**Outputs:** PASS/FAIL/PARTIAL report with specific issues

---

### 2. Bookkeeper
Maintains BlackBox5 administrative hygiene.

**When:** Task checkpoint/completion
**Inputs:** Task status, changes made, run folder
**Outputs:** Updated THOUGHTS.md, DECISIONS.md, TIMELINE.md, task status

---

### 3. Superintelligence (The Real One)
Complex problem analysis through parallel expert sub-agents.

**When:** Architecture questions, complex decisions, novel problems
**Process:**
1. Spawns 5 parallel context-gathering sub-agents
2. Each agent researches different aspects
3. Synthesizes findings into recommendation

**Parallel Sub-Agents:**
- `si-context-scanner` - Scan relevant projects/folders
- `si-goal-analyzer` - Analyze and clarify the goal
- `si-constraint-finder` - Identify constraints and requirements
- `si-pattern-researcher` - Research similar solutions
- `si-risk-analyzer` - Identify risks and edge cases

---

### 4. Context Gatherer
Pre-task context collection for any complex work.

**When:** Before complex tasks
**Inputs:** Task description, scope hints
**Outputs:** Structured project summary, relevant files, dependency map

---

## What About Orchestrator?

**Clarification:** Orchestrator is not a separate sub-agent. It's a **pattern**.

The main agent IS the orchestrator. It decides:
- Which sub-agents to spawn
- In what order
- What context to pass
- How to synthesize results

Sub-agents don't orchestrate other sub-agents (avoids complexity).

---

## BMAD Roles Status

**Current State:** BMAD sub-agents don't actually exist as separate implementations.

**Decision:** Keep them as conceptual roles, not actual sub-agents.

Instead of BMAD sub-agents, we have:
- **Skills** for BMAD workflows (already exist)
- **Sub-agents** for cross-cutting concerns (validator, bookkeeper, superintelligence)

This is simpler and matches reality.

---

## Sub-Agent Call Patterns

### Simple Task
```
Main Agent -> Does work -> Calls Validator -> Calls Bookkeeper -> Done
```

### Complex Task
```
Main Agent -> Calls Context Gatherer
          -> Does work
          -> Calls Validator
          -> Calls Bookkeeper
          -> Done
```

### Superintelligence Task
```
Main Agent -> Calls Superintelligence
          -> Superintelligence spawns 5 parallel research agents
          -> Synthesizes results
          -> Returns recommendation
          -> Main Agent acts on recommendation
          -> Calls Validator
          -> Calls Bookkeeper
          -> Done
```

---

## Research Needed

Before finalizing, we need sub-agents to research:

1. **BlackBox5 Workflow Researcher** - Map all workflows (Scout, Planner, Analysis, RALF, etc.)
2. **Custom Prompt Researcher** - Document all custom prompts and when they're used
3. **Integration Points Researcher** - Find where sub-agents should hook into existing workflows

These research sub-agents will run in parallel to build our understanding.
