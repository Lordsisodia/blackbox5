# THOUGHTS - TASK-001-B: Design Agent Interfaces

**Date:** 2026-02-10
**Task:** Design Agent Interfaces for Research Pipeline
**Agent:** bmad-architect

---

## Context

The Dual-RALF Research Pipeline has an existing architecture documented in:
- `DUAL-RALF-RESEARCH-ARCHITECTURE.md` - Main architecture with agent responsibilities
- `ARCHITECTURE-ALIGNMENT.md` - BB5 integration points
- `CURRENT-STATE.md` - Current file structure and status

The task requires creating detailed, machine-readable interface specifications for:
1. Scout Agent Interface
2. Analyst Agent Interface
3. Planner Agent Interface
4. Executor Agent Interface (new - needs design)
5. Communication Protocol
6. Storage Interfaces

---

## Analysis

### What Already Exists

**High-level design:**
- Worker-Validator pair concept (Scout-Validator, Analyst-Validator, Planner-Validator)
- File-based communication protocol
- Timeline memory and running memory for state
- BB5 alignment patterns (runs/, metrics/, state/)

**Agent prompts:**
- scout-worker.md - Already defines work assignment, phases, token budget
- analyst-worker.md - Already defines scoring algorithm, decision thresholds
- planner-worker.md - Already defines task decomposition, BB5 integration

### What's Missing

**What this task adds:**
1. **Formal interface schemas** - Structured YAML/JSON definitions of all inputs/outputs
2. **Executor Agent** - The 4th agent (was not in original Dual-RALF design)
3. **Machine-readable contracts** - For automated validation
4. **Storage schema documentation** - Detailed Neo4j, Redis, filesystem structures

### Design Decisions

#### 1. Agent Interface Format
I'll use **YAML frontmatter-style schemas** because:
- Easy to read by humans
- Machine-readable
- Already used throughout BB5 (queue.yaml, events.yaml, metadata.yaml)
- Can be validated with YAML parsers

#### 2. Four-Agent Pipeline
The task specifies **4 agents**, but the existing architecture has **6 agents** (worker + validator pairs).

**Design decision:** The task focuses on **worker agents** (the ones doing the work). Validators are coordinating agents that:
- Monitor worker output
- Provide feedback
- Learn and improve
- Do not have public-facing input/output contracts

**Why:** Worker agents have clear input (work queue) and output (tasks, patterns, analysis) contracts. Validators have private feedback mechanisms.

#### 3. Executor Agent Integration
The Executor Agent is the **BB5 executor** that processes tasks created by the Planner Worker.

**Design decision:** The Executor Agent uses the **same queue.yaml** interface as BB5's planner-executor loop. The research pipeline writes tasks to `communications/queue.yaml`, and BB5's executor reads from it.

---

## Process

### 1. Analyze Existing Architecture
Read DUAL-RALF-RESEARCH-ARCHITECTURE.md, ARCHITECTURE-ALIGNMENT.md, CURRENT-STATE.md

### 2. Extract Interface Requirements
From agent prompts, identify:
- Scout: Input contracts (source configs, scan rules), Output contracts (concept nodes, events)
- Analyst: Input contracts (patterns, context), Output contracts (rankings, recommendations, scoring algorithm)
- Planner: Input contracts (recommendations, state), Output contracts (task packages, plans, BB5 task structure)

### 3. Design Executor Interface
Executor Agent (BB5 executor) receives tasks from `communications/queue.yaml`

### 4. Define Communication Protocol
Create formal schema for:
- Redis channel schema (conceptual - using files instead)
- File-based protocol
- Event schema
- Message formats

### 5. Design Storage Interfaces
Document:
- Neo4j graph schema (for concept relationships)
- Redis data structures (for caching/state)
- File system layout
- State synchronization

### 6. Document Error Handling
Define retry logic, failure modes, recovery patterns

---

## Key Insights

1. **Worker-Validator separation is critical** - Workers execute, validators learn. They share state but have distinct interfaces.

2. **Event-driven architecture** - Agents communicate via events in events.yaml, not direct messaging.

3. **Token budget enforcement** - All agents must track and respect their token budgets with checkpoint support.

4. **Self-modification capability** - Agents update their timeline-memory and long-term memory during runs.

5. **BB5 alignment** - Research pipeline must match BB5's run/metrics/state patterns for consistency.

---

## Next Steps

1. Create INTERFACE-SPECIFICATIONS.md with all schemas
2. Update task status to completed
3. Write RESULTS.md summarizing deliverables
4. Commit changes
