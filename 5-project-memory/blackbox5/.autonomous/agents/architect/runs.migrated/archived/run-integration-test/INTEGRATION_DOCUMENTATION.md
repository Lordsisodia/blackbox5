# RALF v2.3 Unified Loop Integration Documentation

**Agent:** Agent-2.3
**Date:** 2026-01-31
**Task:** TASK-1769799336 - Integrate All v2.3 Systems into Unified Loop
**Status:** COMPLETE
**Integration Tests:** 21/21 PASSED

---

## Overview

RALF v2.3 (The Integration Release) introduces enforcement systems that transform rules into automated validations. This document describes how all systems work together in the unified autonomous loop.

## Systems Integrated

| System | Purpose | Location |
|--------|---------|----------|
| **Phase Gates** | Validates phase completion criteria | `~/.blackbox5/2-engine/.autonomous/lib/phase_gates.py` |
| **Context Budget** | Monitors token usage, triggers actions | `~/.blackbox5/2-engine/.autonomous/lib/context_budget.py` |
| **Decision Registry** | Records decisions with reversibility tracking | `decision_registry.yaml` |
| **Goals System** | Prioritizes human-directed work | `~/.blackbox5/5-project-memory/ralf-core/.autonomous/goals/` |
| **Telemetry** | Tracks events, metrics, phases | `~/.blackbox5/2-engine/.autonomous/shell/telemetry.sh` |

---

## System Call Sequence

### Initialization (Loop Start)

```bash
# 1. Initialize telemetry
TELEMETRY_FILE=$(telemetry.sh init)

# 2. Initialize context budget
python3 context_budget.py init --run-dir "$RUN_DIR"

# 3. Initialize decision registry
cp templates/decision_registry.yaml "$RUN_DIR/decision_registry.yaml"
```

### Task Selection

```bash
# 4. Check for active goals first
ls ~/.blackbox5/5-project-memory/ralf-core/.autonomous/goals/active/*.md

# 5. Record telemetry
telemetry.sh phase "task_selection" "complete" "$TELEMETRY_FILE"
```

### Quick Flow Path (3 Phases)

```
┌─────────────────────────────────────────────────────────────────┐
│                       QUICK FLOW PATH                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐      │
│  │ QUICK-SPEC   │───>│  DEV-STORY   │───>│ CODE-REVIEW  │      │
│  │              │    │              │    │              │      │
│  │ • Gate Check │    │ • Gate Check │    │ • Gate Check │      │
│  │ • Budget Chk │    │ • Budget Chk │    │ • Budget Chk │      │
│  │ • Telemetry  │    │ • Telemetry  │    │ • Telemetry  │      │
│  └──────────────┘    └──────────────┘    └──────────────┘      │
│         │                   │                   │               │
│         v                   v                   v               │
│   [Spec File]          [Code Changes]       [Review OK]         │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Full BMAD Path (5 Phases)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         FULL BMAD PATH                                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌──────────┐   ┌─────────┐    │
│  │  ALIGN  │──>│  PLAN   │──>│ EXECUTE │──>│ VALIDATE │──>│  WRAP   │    │
│  │         │   │         │   │         │   │          │   │         │    │
│  │ • Gate  │   │ • Gate  │   │ • Gate  │   │ • Gate   │   │ • Gate  │    │
│  │ • Budget│   │ • Budget│   │ • Budget│   │ • Budget │   │ • Budget│    │
│  │ • Telem │   │ • Telem │   │ • Telem │   │ • Telem  │   │ • Telem │    │
│  │         │   │ • Decis │   │ • Decis │   │ • Verify │   │ • Decis │    │
│  └─────────┘   └─────────┘   └─────────┘   └──────────┘   └─────────┘    │
│      │             │             │              │              │          │
│      v             v             v              v              v          │
│  [Problem]    [Architecture]  [Implement]   [Validation]   [Docs +      │
│  Defined      + Decisions     + Test        Passed          Retro]       │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Phase Gate Integration

### Gate Check Command

```bash
python3 phase_gates.py check --phase [PHASE_NAME] --run-dir "$RUN_DIR"
```

### When to Check Gates

| Phase | Check Point | Action if Failed |
|-------|-------------|------------------|
| quick_spec | After spec created | Cannot proceed |
| dev_story | After implementation | Rollback and retry |
| code_review | After review | Return to dev_story |
| align | After alignment | Cannot proceed |
| plan | After planning | Cannot proceed |
| execute | After implementation | Rollback to plan |
| validate | After validation | Rollback to execute |
| wrap | After documentation | Cannot complete |

### Gate Marking

When all exit criteria are met:

```bash
python3 phase_gates.py mark --phase [PHASE_NAME] --run-dir "$RUN_DIR"
```

This creates:
- `.gate_[PHASE]_passed` - Entry gate marker for next phase
- `.phase_[PHASE]_criteria` - Exit criteria confirmation

---

## Context Budget Integration

### Checkpoints

| Threshold | Percentage | Action |
|-----------|-----------|--------|
| Sub-agent | 40% | Spawn sub-agent for remaining work |
| Warning | 70% | Summarize THOUGHTS.md |
| Critical | 85% | Spawn sub-agent urgently |
| Hard Limit | 95% | Force checkpoint and exit |

### Check Command

```bash
python3 context_budget.py check --run-dir "$RUN_DIR" --tokens [CURRENT_TOKENS]
```

### Auto-Actions

When a threshold is triggered:
1. Action is executed automatically
2. Event is logged to telemetry
3. State is saved to `context_budget.json`
4. Agent may need to delegate or compress context

---

## Decision Registry Integration

### When to Record Decisions

Record a decision in `decision_registry.yaml` when:
- Choosing between multiple implementation approaches
- Making architectural choices
- Setting constraints or scope boundaries
- Defining rollback strategies

### Decision Format

```yaml
decisions:
  - id: "DEC-{run_num}-{seq}"
    timestamp: "2026-01-31T10:15:00Z"
    phase: "PLAN"
    context: "Description of the decision context"

    options_considered:
      - id: "OPT-001"
        description: "Option 1 description"
        pros: ["Advantage 1", "Advantage 2"]
        cons: ["Disadvantage 1"]

    selected_option: "OPT-001"
    rationale: "Why this option was chosen"

    assumptions:
      - id: "ASM-001"
        statement: "Assumption being made"
        risk_level: "MEDIUM"
        verification_method: "How to verify"
        status: "PENDING_VERIFICATION"

    reversibility: "MEDIUM"
    rollback_complexity: "Description of rollback effort"
    rollback_steps:
      - "Step 1 to rollback"
      - "Step 2 to rollback"

    verification:
      required: true
      criteria:
        - "Criterion 1"
        - "Criterion 2"

    status: "DECIDED"
```

### Verification (During VALIDATE Phase)

For each decision with `verification.required: true`:
1. Check if assumptions were verified
2. Validate criteria are met
3. Update `status: "VERIFIED"`

---

## Goals System Integration

### Goal-Derived Task Priority

Goals created by humans get 90+ priority score, taking precedence over autonomous task generation.

### Task Selection Logic

```python
if active_goals_exist:
    # Read highest priority goal
    # Find first incomplete sub-goal
    # Create task from sub-goal
    # Priority score = 90+ (goal-derived)
else:
    # Run autonomous task generation
    # Analyze telemetry, first principles, gaps
    # Priority score = 60-80 (autonomous)
```

### Goals Directory Structure

```
~/.blackbox5/5-project-memory/ralf-core/.autonomous/goals/
├── active/
│   └── GOAL-001-ralf-v23-integration-release.md
├── completed/
│   └── GOAL-XXX-...
└── templates/
    └── goal-template.md
```

---

## Telemetry Integration

### Telemetry Events

| Event Type | When Logged | Example |
|------------|-------------|---------|
| `info` | General status updates | "RALF loop started" |
| `success` | Successful operations | "Changes committed" |
| `error` | Errors and failures | "Gate check failed" |
| `warning` | Warnings | "Context at 75%" |
| `phase` | Phase transitions | "Phase 'execution' is now in_progress" |

### Telemetry Metrics

```json
{
  "metrics": {
    "files_read": 0,
    "files_written": 0,
    "commands_executed": 0,
    "errors": 0,
    "warnings": 0
  }
}
```

### Telemetry Commands

```bash
# Initialize
TELEMETRY_FILE=$(telemetry.sh init)

# Log event
telemetry.sh event "info" "Message" "$TELEMETRY_FILE"

# Update phase
telemetry.sh phase "execution" "in_progress" "$TELEMETRY_FILE"

# Increment metric
telemetry.sh metric "files_read" "$TELEMETRY_FILE"

# Complete run
telemetry.sh complete "COMPLETE" "$TELEMETRY_FILE"

# Show status
telemetry.sh status "$TELEMETRY_FILE"
```

---

## Integration Test Suite

### Running Tests

```bash
# Run all integration tests
python3 ~/.blackbox5/2-engine/.autonomous/lib/integration_test.py run \
    --run-dir ~/.blackbox5/5-project-memory/ralf-core/.autonomous/runs/run-TEST

# List all tests
python3 ~/.blackbox5/2-engine/.autonomous/lib/integration_test.py list

# Quick verification
python3 ~/.blackbox5/2-engine/.autonomous/lib/integration_test.py verify-all
```

### Test Coverage

| System | Tests | Status |
|--------|-------|--------|
| Phase Gates | 4 tests | PASSED |
| Context Budget | 4 tests | PASSED |
| Decision Registry | 2 tests | PASSED |
| Goals System | 3 tests | PASSED |
| Telemetry | 3 tests | PASSED |
| Unified Loop | 5 tests | PASSED |

---

## Unified Loop Flowchart

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         RALF v2.3 UNIFIED LOOP                              │
└─────────────────────────────────────────────────────────────────────────────┘

                              ┌─────────────┐
                              │    START    │
                              └──────┬──────┘
                                     │
                                     v
                         ┌───────────────────────┐
                         │  Initialize Telemetry │
                         └───────────┬───────────┘
                                     │
                                     v
                         ┌───────────────────────┐
                         │ Initialize Context    │
                         │      Budget           │
                         └───────────┬───────────┘
                                     │
                                     v
                         ┌───────────────────────┐
                         │ Initialize Decision   │
                         │      Registry         │
                         └───────────┬───────────┘
                                     │
                                     v
                         ┌───────────────────────┐
                         │  Check Active Goals?  │
                         └─────┬────────────┬────┘
                               │ YES        │ NO
                               v            v
                    ┌──────────────┐   ┌──────────────────┐
                    │ Create Task  │   │  Autonomous Task │
                    │ from Goal    │   │    Generation    │
                    │ (Priority    │   │                  │
                    │   90+)       │   │ (Priority 60-80) │
                    └──────┬───────┘   └────────┬─────────┘
                           └─────────┬──────────┘
                                     │
                                     v
                         ┌───────────────────────┐
                         │  Select Path:         │
                         │  Quick vs Full BMAD   │
                         └───────────┬───────────┘
                                     │
                ┌────────────────────┴────────────────────┐
                │                                         │
                v                                         v
        ┌───────────────┐                       ┌────────────────┐
        │  QUICK FLOW   │                       │  FULL BMAD     │
        │               │                       │                │
        │ ┌───────────┐ │                       │ ┌───────────┐  │
        │ │Quick-Spec │ │                       │ │  Align    │  │
        │ │Gate Check │ │                       │ │Gate Check │  │
        │ └─────┬─────┘ │                       │ └─────┬─────┘  │
        │       v       │                       │       v        │
        │ ┌───────────┐ │                       │ ┌───────────┐  │
        │ │Dev-Story  │ │                       │ │   Plan    │  │
        │ │Gate Check │ │                       │ │Gate Check │  │
        │ │+Decisions │ │                       │ │+Decisions │  │
        │ └─────┬─────┘ │                       │ └─────┬─────┘  │
        │       v       │                       │       v        │
        │ ┌───────────┐ │                       │ ┌───────────┐  │
        │ │Code Review│ │                       │ │  Execute  │  │
        │ │Gate Check │ │                       │ │Gate Check │  │
        │ └─────┬─────┘ │                       │ │+Decisions │  │
        │       v       │                       │ └─────┬─────┘  │
        └───────┘       │                       │       v        │
                        │                       │ ┌───────────┐  │
                        │                       │ │ Validate  │  │
                        │                       │ │Gate Check │  │
                        │                       │ │Verify Dec │  │
                        │                       │ └─────┬─────┘  │
                        │                       │       v        │
                        │                       │ ┌───────────┐  │
                        │                       │ │   Wrap    │  │
                        │                       │ │Gate Check │  │
                        │                       │ │+Decisions │  │
                        │                       │ └─────┬─────┘  │
                        │                       └───────┘        │
                        └────────────────────┬──────────────────┘
                                             │
                                             v
                                 ┌───────────────────────┐
                                 │ Document Run:         │
                                 │ • THOUGHTS.md         │
                                 │ • DECISIONS.md        │
                                 │ • ASSUMPTIONS.md      │
                                 │ • LEARNINGS.md        │
                                 │ • RESULTS.md          │
                                 └───────────┬───────────┘
                                             │
                                             v
                                 ┌───────────────────────┐
                                 │ Update Task Status    │
                                 │ Move to Completed/    │
                                 └───────────┬───────────┘
                                             │
                                             v
                                 ┌───────────────────────┐
                                 │ Commit & Push         │
                                 └───────────┬───────────┘
                                             │
                                             v
                                 ┌───────────────────────┐
                                 │ Complete Telemetry    │
                                 └───────────┬───────────┘
                                             │
                                             v
                                 ┌───────────────────────┐
                                 │      COMPLETE ✓       │
                                 └───────────────────────┘
```

---

## Key Integration Points in ralf.md

The following sections in `~/.blackbox5/bin/ralf.md` contain the integration code:

| Section | Line Range | Purpose |
|---------|-----------|---------|
| Step 1: Load Context | 260-310 | Initialize telemetry, context budget, decision registry |
| Step 2: Task Selection | 312-370 | Check goals, select task, record telemetry |
| Step 2.5: Pre-Execution Research | 372-410 | Spawn research sub-agent before execution |
| Quick Flow Phases | 450-490 | Gate checks at each phase transition |
| Full BMAD Phases | 492-560 | Gate checks, decisions, verification |
| Context Budget Checks | Throughout | Check before operations, auto-actions |
| Telemetry Events | Throughout | Log all major events and phase changes |

---

## Troubleshooting

### Gate Check Fails

**Problem:** Phase gate validation fails
**Solution:**
1. Check missing requirements with `python3 phase_gates.py check --phase [PHASE] --run-dir [RUN_DIR]`
2. Create missing files or complete missing criteria
3. Mark criteria complete with `python3 phase_gates.py mark --phase [PHASE] --run-dir [RUN_DIR]`

### Context Budget Exceeded

**Problem:** Context at 85%+ threshold
**Solution:**
1. Run `python3 context_budget.py recommend --tokens [CURRENT]`
2. Spawn sub-agent for remaining work
3. Summarize THOUGHTS.md if at warning threshold

### Decision Registry Missing

**Problem:** Decision registry not initialized
**Solution:**
```bash
cp ~/.blackbox5/2-engine/.autonomous/prompt-progression/versions/v2.2/templates/decision_registry.yaml \
   "$RUN_DIR/decision_registry.yaml"
```

### Telemetry Not Recording

**Problem:** Events not appearing in telemetry
**Solution:**
1. Check `$TELEMETRY_FILE` is set
2. Verify telemetry.sh is executable
3. Run `telemetry.sh status` to check current state

---

## Completion Status

**Task:** TASK-1769799336 - Integrate All v2.3 Systems into Unified Loop
**Status:** COMPLETE
**Integration Tests:** 21/21 PASSED
**Date:** 2026-01-31

### Success Criteria Met

- [x] All v2.3 systems callable from ralf.md execution loop
- [x] Phase gates checked at each phase transition
- [x] Context budget monitored with auto-actions
- [x] Decision registry populated for all significant decisions
- [x] Goals system checked before autonomous task generation
- [x] Telemetry recorded throughout execution
- [x] End-to-end test of full loop successful

### Deliverables

1. **Integration Test Suite** - `~/.blackbox5/2-engine/.autonomous/lib/integration_test.py`
2. **This Documentation** - Integration guide and flowcharts
3. **Verified Integration** - All 21 tests passing

---

## Next Steps

With RALF v2.3 fully integrated:

1. **GOAL-001 (RALF v2.3 Integration Release)** - Mark sub-goal 8 complete
2. **Update ralf.md** - Ensure all agents use v2.3 enforcement
3. **Monitor Loop Health** - Use telemetry to track performance
4. **Add More BMAD Skills** - The integration is ready for additional skills
