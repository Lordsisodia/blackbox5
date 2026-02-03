# Worker-Validator Coordination Guide

**Purpose:** How the 6 agents (3 worker-validator pairs) coordinate work
**Architecture:** Dual-RALF with parallel execution
**Communication:** File-based via shared state files

---

## Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    DUAL-RALF RESEARCH PIPELINE                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐      ┌──────────────┐                        │
│  │ Scout Worker │◄────►│Scout Validator│  (Extraction Phase)    │
│  │  (RALF Loop) │      │  (RALF Loop)  │                        │
│  └──────┬───────┘      └──────────────┘                        │
│         │                                                        │
│         ▼ patterns.yaml                                          │
│  ┌──────────────┐      ┌──────────────┐                        │
│  │Analyst Worker│◄────►│Analyst Validator│ (Analysis Phase)    │
│  │  (RALF Loop) │      │  (RALF Loop)  │                        │
│  └──────┬───────┘      └──────────────┘                        │
│         │                                                        │
│         ▼ analysis.yaml                                          │
│  ┌──────────────┐      ┌──────────────┐                        │
│  │Planner Worker│◄────►│Planner Validator│  (Planning Phase)   │
│  │  (RALF Loop) │      │  (RALF Loop)  │                        │
│  └──────┬───────┘      └──────────────┘                        │
│         │                                                        │
│         ▼ BB5 Tasks                                              │
│  ┌──────────────────────────────────────┐                      │
│  │         Blackbox5 Task Queue          │                      │
│  └──────────────────────────────────────┘                      │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

**Key Principle:** Workers and validators run in **parallel**, not sequentially.

---

## How Workers Know What To Do

### The Problem
Workers need to know what work to perform on each run. Without clear assignment, they would:
- Do redundant work
- Miss important tasks
- Conflict with other agents

### The Solution: Timeline Memory + Work Assignment Logic

Each worker has a `timeline-memory.md` file that:
1. **Persists across runs** - remembers what was done
2. **Contains work queue** - what needs to be done next
3. **Is auto-injected** - via SessionStart hook
4. **Has clear logic** - decision tree for work selection

### Work Assignment Decision Tree (All Workers)

```
START
  │
  ▼
┌─────────────────────────────┐
│ Read timeline-memory.md     │
│ (injected via SessionStart) │
└─────────────────────────────┘
  │
  ▼
┌─────────────────────────────────────┐
│ Check work_queue.priority_items     │
│ Not empty?                          │
└─────────────────────────────────────┘
  │
  ├── YES ──► Take first priority item
  │
  └── NO ──► Check work_queue.backlog
                │
                ├── NOT EMPTY ──► Take first backlog item
                │
                └── EMPTY ──► Check shared state (events.yaml)
                                  │
                                  ├── FOUND ──► Take from shared queue
                                  │
                                  └── EMPTY ──► EXIT (Status: IDLE)
```

---

## Worker-Validator Coordination Flow

### Phase 1: Scout Pair (Pattern Extraction)

```
Time ─────────────────────────────────────────────────────────────►

Scout Worker                          Scout Validator
     │                                       │
     │  1. Read timeline-memory.md           │
     │     (injected via hook)               │
     │                                       │
     │  2. Determine work from queue         │
     │     → github.com/repo1                │
     │                                       │
     │  3. Update timeline:                  │
     │     work_queue.in_progress = repo1    │
     │                                       │
     ▼                                       │
  ┌──────────────────┐                       │
  │ Extract patterns │                       │
  │ from repo1       │                       │
  │                  │                       │
  │ Save to:         │                       │
  │ data/patterns/   │                       │
  │ P-001.yaml       │                       │
  │ P-002.yaml       │                       │
  │ P-003.yaml       │                       │
  └────────┬─────────┘                       │
           │                                 │
           │ 4. Write THOUGHTS.md            │
           │    Write RESULTS.md             │
           │    Update timeline-memory.md    │
           │                                 │
           │ 5. Publish event:               │    1. Read own timeline-memory.md
           │    events.yaml:                 │       (injected via hook)
           │    pattern.extracted            │
           │                                 │
           │                           2. Find worker's latest run
           │                              in agents/scout-worker/runs/
           │                                 │
           │                           3. Read THOUGHTS.md, RESULTS.md
           │                              Read data/patterns/*.yaml
           │                                 │
           │                           4. Validate extraction quality
           │                              Check for missed patterns
           │                                 │
           │                           5. Write feedback:
           │◄───────────────────────────  communications/chat-log.yaml
           │                              "You missed decorator pattern..."
           │                                 │
           │                           6. Update timeline-memory.md
           │                              Record validation results
           │                                 │
     ┌─────┴─────┐                    ┌─────┴─────┐
     │  RUN END  │                    │  RUN END  │
     └───────────┘                    └───────────┘
           │                                 │
           ▼                                 ▼
     ┌───────────┐                    ┌───────────┐
     │ NEXT RUN  │                    │ NEXT RUN  │
     │           │                    │           │
     │ 1. Read   │                    │ 1. Read   │
     │    timeline│                   │    timeline│
     │    (injected)│                 │    (injected)│
     │           │                    │           │
     │ 2. Check  │                    │ 2. Find   │
     │    chat-log.yaml◄─────────────│    worker's│
     │    for feedback               │    new run │
     │    "You missed..."            │            │
     │           │                    │            │
     │ 3. Apply  │                    │ 3. Validate│
     │    feedback                   │    new work│
     │    "Watch for decorators"     │            │
     │           │                    │            │
     │ 4. Extract│                    │ 4. Provide │
     │    from   │                    │    feedback│
     │    repo2  │                    │            │
     │    (finds │                    │            │
     │    decorator!)                │            │
     └───────────┘                    └───────────┘
```

### Phase 2: Analyst Pair (Pattern Analysis)

```
Analyst Worker                        Analyst Validator
     │                                       │
     │ 1. Read timeline-memory.md            │
     │    (injected via hook)                │
     │                                       │
     │ 2. Check work_queue                   │
     │    Empty? Check events.yaml           │
     │    pattern.extracted event found      │
     │                                       │
     │ 3. Load P-001.yaml from data/patterns/│
     │                                       │
     ▼                                       │
  ┌──────────────────┐                       │
  │ Analyze pattern  │                       │
  │ value to BB5     │                       │
  │                  │                       │
  │ Score:           │                       │
  │ - value: 8.5     │                       │
  │ - complexity: 4.2│                       │
  │ - decision:      │                       │
  │   recommend      │                       │
  └────────┬─────────┘                       │
           │                                 │
           │ 4. Save to:                     │
           │    data/analysis/P-001.yaml     │
           │                                 │
           │ 5. Publish event:               │    1. Read own timeline-memory.md
           │    events.yaml:                 │       (injected via hook)
           │    analysis.complete            │
           │    decision: recommend          │
           │                                 │    2. Find worker's analysis
           │                                 │       in data/analysis/
           │                                 │
           │                                 │    3. Read analysis
           │                                 │       Check scoring rationale
           │                                 │
           │                                 │    4. Compare to historical
           │                                 │       model_accuracy data
           │                                 │       "Complexity seems low..."
           │                                 │
           │◄───────────────────────────────│    5. Write feedback:
           │    chat-log.yaml:               │       "Similar patterns scored 6..."
           │    "Complexity seems low..."    │
           │                                 │    6. Update model_accuracy
           │                                 │       Track prediction accuracy
```

### Phase 3: Planner Pair (Task Creation)

```
Planner Worker                        Planner Validator
     │                                       │
     │ 1. Read timeline-memory.md            │
     │    (injected via hook)                │
     │                                       │
     │ 2. Check work_queue                   │
     │    Empty? Check events.yaml           │
     │    analysis.complete with             │
     │    decision: recommend                │
     │                                       │
     │ 3. Load P-001 analysis                │
     │    from data/analysis/                │
     │                                       │
     ▼                                       │
  ┌──────────────────┐                       │
  │ Create BB5 task  │                       │
  │ from recommendation│                     │
  │                  │                       │
  │ Decompose into:  │                       │
  │ - core (4h)      │                       │
  │ - tests (2h)     │                       │
  │ - docs (1h)      │                       │
  │                  │                       │
  │ Total: 7h        │                       │
  │ Task: TASK-RAPS-001                   │
  └────────┬─────────┘                       │
           │                                 │
           │ 4. Create task package:         │
           │    tasks/active/TASK-RAPS-001/  │
           │                                 │
           │ 5. Add to queue.yaml            │    1. Read own timeline-memory.md
           │                                 │       (injected via hook)
           │                                 │
           │                                 │    2. Find new task in
           │                                 │       communications/queue.yaml
           │                                 │
           │                                 │    3. Read task plan
           │                                 │       Check subtask atomicity
           │                                 │       Verify estimates
           │                                 │
           │                                 │    4. Compare to templates
           │                                 │       "Auth patterns need 4 tasks..."
           │                                 │
           │◄───────────────────────────────│    5. Write feedback:
           │    chat-log.yaml:               │       "Add integration test..."
           │    "Consider adding..."         │
           │                                 │    6. Update plan_quality
           │                                 │       Track template effectiveness
```

---

## Communication File Reference

### Shared State Files (All Agents)

| File | Purpose | Who Writes | Who Reads |
|------|---------|------------|-----------|
| `communications/scout-state.yaml` | Scout queue/status | Scout Worker | Scout Validator |
| `communications/analyst-state.yaml` | Analyst queue/status | Analyst Worker | Analyst Validator |
| `communications/planner-state.yaml` | Planner queue/status | Planner Worker | Planner Validator |
| `communications/events.yaml` | Event bus | All Workers | All Validators |
| `communications/chat-log.yaml` | Feedback channel | Validators | Workers |
| `communications/heartbeat.yaml` | Health status | All | All |
| `communications/queue.yaml` | BB5 task queue | Planner Worker | BB5 System |

### Data Files

| File | Purpose | Who Writes | Who Reads |
|------|---------|------------|-----------|
| `data/patterns/{id}.yaml` | Extracted patterns | Scout Worker | Analyst Worker |
| `data/analysis/{id}.yaml` | Pattern analysis | Analyst Worker | Planner Worker |
| `tasks/active/TASK-*/` | BB5 task packages | Planner Worker | BB5 System |

### Agent Memory Files

| File | Purpose | Updated By |
|------|---------|------------|
| `agents/{agent}/timeline-memory.md` | Long-term memory | Agent itself |
| `agents/{agent}/running-memory.md` | Current run state | Agent itself |
| `agents/{agent}/memory/*.yaml` | Learning/strategy | Agent itself |

---

## Timing and Parallelism

### Key Insight: Runs Overlap

```
Time ─────────────────────────────────────────────────────────────►

Worker Run 1:    [████████████]  (extracting from repo1)
Validator Run 1:      [████████████]  (validating extraction)
                        ▲
                        └─ Validator starts after Worker,
                           but they overlap

Worker Run 2:              [████████████]  (extracting from repo2)
                              ▲
                              └─ Worker reads Validator's
                                 feedback from Run 1

Validator Run 2:                [████████████]  (validating repo2)
```

### Important Rules

1. **Workers don't wait for validators** - they run continuously
2. **Validators don't block workers** - they validate in parallel
3. **Feedback is consumed on NEXT run** - not during current run
4. **Timeline memory is updated at end** - persists across runs

---

## SessionStart Hook Integration

### What Gets Injected

The `session-start-timeline-memory.sh` hook automatically injects:

```markdown
## Agent Identity
You are the {agent} in the Dual-RALF Research Pipeline.
Session: {session_id} | Source: {source}

## Your Timeline Memory (Long-Term Context)
[Full timeline-memory.md content]

## Work Assignment Instructions
[Specific instructions for this agent type]
```

### Why This Matters

Without the hook, agents would:
- Not know their work history
- Not have access to work queue
- Not understand what to work on
- Lose context between runs

With the hook:
- Timeline memory is always present
- Work assignment is clear
- Context persists across runs
- Agents are self-directed

---

## Example: Complete Flow

### Initial State
- All timeline memories are empty
- No sources in queues
- Events.yaml is empty

### Step 1: Add Source to Queue
```bash
# Operator adds source
echo "github.com/user/auth-repo" >> sources.txt
```

### Step 2: Scout Worker First Run
1. Hook injects timeline-memory.md (empty)
2. Worker checks work_queue (empty)
3. Worker checks events.yaml (empty)
4. Worker finds source in sources.txt
5. Worker extracts patterns
6. Worker updates timeline with history
7. Worker publishes pattern.extracted event

### Step 3: Scout Validator First Run
1. Hook injects timeline-memory.md (empty)
2. Validator finds Worker's run
3. Validator reads THOUGHTS.md, RESULTS.md
4. Validator identifies missed pattern
5. Validator writes feedback to chat-log.yaml
6. Validator updates timeline with validation

### Step 4: Scout Worker Second Run
1. Hook injects timeline-memory.md (with history)
2. Worker reads chat-log.yaml feedback
3. Worker applies feedback ("watch for decorators")
4. Worker extracts from next source
5. Worker finds decorator pattern!
6. Worker updates timeline

### Step 5: Analyst Worker First Run
1. Hook injects timeline-memory.md
2. Worker checks events.yaml
3. Worker finds pattern.extracted event
4. Worker analyzes pattern P-001
5. Worker scores: value=8.5, complexity=4.2
6. Worker decides: recommend
7. Worker publishes analysis.complete event

### Step 6: Planner Worker First Run
1. Hook injects timeline-memory.md
2. Worker finds analysis.complete with recommend
3. Worker creates TASK-RAPS-001
4. Worker decomposes into subtasks
5. Worker adds to queue.yaml
6. BB5 system now has a new task!

---

## Summary

**The system works because:**

1. **Timeline memory** persists context across runs
2. **SessionStart hook** injects memory automatically
3. **Work assignment logic** is clear and deterministic
4. **File-based communication** enables parallel execution
5. **Workers and validators** run simultaneously
6. **Feedback loops** enable continuous improvement

**Each agent knows what to do because:**
- Their timeline memory tells them their history
- Their work queue tells them what's next
- The decision tree tells them how to choose
- The shared state files coordinate with other agents
