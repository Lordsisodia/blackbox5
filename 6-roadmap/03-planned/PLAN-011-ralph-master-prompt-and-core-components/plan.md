# PLAN-011: Ralph Master Prompt and Core Components

**Status:** Planned  
**Priority:** Critical  
**Created:** 2026-01-30  
**Owner:** Ralph Agent System  

---

## Overview

This plan defines the work needed to complete Ralph's core infrastructure in Blackbox5, specifically focusing on:
1. Master system prompts for Ralph's autonomous loop behavior
2. Sub-agent prompt templates
3. Project selection and prioritization framework
4. Full Blackbox5 integration

---

## Background

### What is Ralph?

Ralph (based on the Ralph Technique by Jeffrey Huntley) is an autonomous AI coding loop that ships features while you sleep. The core concept is:

```bash
while true; do
  cat prompt.md | claude --dangerously-skip-permissions
done
```

### Key Principles from the Ralph Technique

1. **One task per loop** - Each iteration completes exactly one task
2. **Context preservation** - Use sub-agents for searches to keep main context clean
3. **Progress tracking** - Structured files (fix_plan.md, prd.json) track completion
4. **Exit conditions** - Loop stops when "PROMISE_COMPLETE" is returned
5. **No placeholders** - Every test must actually test something

### Current State in Blackbox5

**What Exists:**
- Ralph Runtime (`2-engine/07-operations/environment/lib/ralph-runtime/`)
- Ralphy Integration with Blackbox5 (`2-engine/07-operations/runtime/ralphy/`)
- Agent Manifest (`2-engine/02-agents/implementations/04-specialists/4-specialists/ralph-agent/`)
- Session tracking structure (`1-docs/core/ralph-loop-sessions/`)
- 2 completed work sessions (Jan 2025, Jan 2026)

**What's Missing:**
- Ralph-specific system prompt (the manifest references a non-existent file)
- Sub-agent prompt templates
- Project selection framework
- Full integration with Blackbox5's First Principles engine

---

## Task Breakdown

### Phase 1: Core Ralph System Prompts (CRITICAL)

#### Task 1.1: Create Ralph Master System Prompt
**Location:** `2-engine/02-agents/implementations/04-specialists/4-specialists/ralph-agent/PROMPT.md`

**Requirements:**
- Define Ralph's autonomous loop behavior
- Integrate with existing `protocol.md` requirements
- Include First Principles decision-making hooks
- Define sub-agent spawning rules
- Specify Blackbox5 memory integration

**Key Sections:**
1. Ralph Identity & Purpose
2. Autonomous Loop Protocol
3. Task Selection Logic
4. Sub-Agent Management
5. Progress Tracking Requirements
6. Blackbox5 Integration Points
7. Exit Conditions
8. Error Handling & Recovery

---

#### Task 1.2: Create Ralph Sub-Agent Prompts
**Location:** `2-engine/02-agents/implementations/04-specialists/4-specialists/ralph-agent/prompts/`

**Sub-agents needed:**
- `validation-agent.md` - Validate implementations against specs
- `documentation-agent.md` - Update docs based on changes
- `research-agent.md` - Deep research on unknown areas
- `fix-agent.md` - Implement fixes for detected issues
- `test-agent.md` - Write and run tests

Each prompt must:
- Inherit from core prompt
- Define specific task scope
- Specify inputs/outputs
- Include completion criteria

---

#### Task 1.3: Create Ralph Context Templates
**Location:** `2-engine/02-agents/implementations/04-specialists/4-specialists/ralph-agent/context/`

**Files:**
- `current-focus.md` - What Ralph is currently working on
- `blackbox5-snapshot.md` - System state snapshot template
- `session-template.md` - New session initialization template
- `progress-tracker.md` - Track completed/in-progress tasks

---

### Phase 2: Ralph Project Selection Framework (HIGH)

#### Task 2.1: Create Project Prioritization Matrix
**Location:** `2-engine/07-operations/environment/lib/ralph-runtime/project_selector.py`

**Criteria:**
- Impact (1-10): How much value does this deliver?
- Urgency (1-10): How soon is this needed?
- Dependencies (count): How many blockers?
- Risk (1-10): How likely to fail?
- Effort (hours): Estimated time required

**Scoring Algorithm:**
```
priority_score = (impact * 2 + urgency) / (dependencies + 1) - (risk * 0.5)
```

---

#### Task 2.2: Create Ralph Work Queue Generator
**Location:** `2-engine/07-operations/environment/lib/ralph-runtime/work_queue.py`

**Functions:**
- Parse `6-roadmap/` for candidate projects
- Filter by readiness criteria:
  - Has PRD or plan document
  - Dependencies are complete
  - Not blocked by other work
- Generate ranked backlog
- Update queue after each completed task

---

#### Task 2.3: Create Dependency Analyzer
**Location:** `2-engine/07-operations/environment/lib/ralph-runtime/dependency_analyzer.py`

**Features:**
- Parse plan files for dependency declarations
- Build dependency graph
- Identify critical path
- Suggest parallelizable work
- Detect circular dependencies

---

### Phase 3: Ralph Execution Loop (HIGH)

#### Task 3.1: Complete Ralph Runtime Integration
**Location:** `2-engine/07-operations/environment/lib/ralph-runtime/`

**Enhancements to existing `ralph_runtime.py`:**
- Connect to Blackbox5 AgentMemory
- Implement session checkpoint/resume
- Add progress tracking to `5-project-memory/`
- Integrate with ModelRouter for cost optimization

---

#### Task 3.2: Create Ralph CLI Interface
**Location:** `2-engine/07-operations/commands/run/ralph-cli.sh`

**Commands:**
```bash
ralph-cli.sh start --project <name>     # Start Ralph on a project
ralph-cli.sh pause                      # Pause current session
ralph-cli.sh resume                     # Resume paused session
ralph-cli.sh status                     # Show current status
ralph-cli.sh stop                       # Stop gracefully
ralph-cli.sh logs                       # Show recent logs
ralph-cli.sh next-task                  # Show what Ralph will work on next
```

---

#### Task 3.3: Create Ralph Monitoring Dashboard
**Location:** `2-engine/07-operations/monitoring/ralph-dashboard/`

**Features:**
- Real-time session status
- Progress visualization
- Error alerting
- Cost tracking
- Performance metrics

---

### Phase 4: Ralph-Blackbox5 Integration (MEDIUM)

#### Task 4.1: Integrate with First Principles Engine
**Location:** `2-engine/07-operations/environment/lib/ralph-runtime/fp_integration.py`

**Features:**
- Ralph uses FP decision-making for project selection
- Document decisions in `data/decisions/records/`
- ADI cycle for complex choices
- Principle-based reasoning

---

#### Task 4.2: Integrate with BMAD Agents
**Location:** `2-engine/07-operations/environment/lib/ralph-runtime/bmad_bridge.py`

**Features:**
- Ralph can spawn analyst, architect, dev agents
- Handoff protocols between Ralph and specialists
- Context passing between agents
- Result aggregation

---

#### Task 4.3: Integrate with Memory System
**Location:** `2-engine/07-operations/environment/lib/ralph-runtime/memory_bridge.py`

**Features:**
- Ralph sessions stored in `5-project-memory/`
- Insights extracted and indexed
- Cross-session learning
- Pattern recognition

---

## Supporting Files Structure

```
2-engine/02-agents/implementations/04-specialists/4-specialists/ralph-agent/
├── PROMPT.md                          # Master system prompt
├── protocol.md                        # Existing - Ralph communication protocol
├── manifest.json                      # Existing - Agent configuration
├── prompts/                           # Sub-agent prompts
│   ├── validation-agent.md
│   ├── documentation-agent.md
│   ├── research-agent.md
│   ├── fix-agent.md
│   └── test-agent.md
├── context/                           # Context templates
│   ├── current-focus.md
│   ├── blackbox5-snapshot.md
│   ├── session-template.md
│   └── progress-tracker.md
└── work/                              # Existing - Work output

2-engine/07-operations/environment/lib/ralph-runtime/
├── ralph_runtime.py                   # Existing - Main orchestrator
├── project_selector.py                # NEW - Task 2.1
├── work_queue.py                      # NEW - Task 2.2
├── dependency_analyzer.py             # NEW - Task 2.3
├── fp_integration.py                  # NEW - Task 4.1
├── bmad_bridge.py                     # NEW - Task 4.2
├── memory_bridge.py                   # NEW - Task 4.3
└── prompts/                           # NEW - Runtime prompt templates
    ├── loop-prompt.md
    ├── task-selection-prompt.md
    └── completion-prompt.md

2-engine/07-operations/commands/run/
├── ralph-cli.sh                       # NEW - Task 3.2
├── ralph-loop.sh                      # Existing
└── ralph-runtime.sh                   # Existing

2-engine/07-operations/monitoring/
└── ralph-dashboard/                   # NEW - Task 3.3
    ├── dashboard.py
    ├── static/
    └── templates/
```

---

## Success Criteria

### Phase 1 Complete When:
- [ ] Ralph Master Prompt exists and is loadable
- [ ] All 5 sub-agent prompts created
- [ ] Context templates are functional
- [ ] Prompts follow Blackbox5 conventions

### Phase 2 Complete When:
- [ ] Project selector can rank roadmap items
- [ ] Work queue generator produces valid queues
- [ ] Dependency analyzer detects circular deps
- [ ] Integration tests pass

### Phase 3 Complete When:
- [ ] Ralph sessions tracked in AgentMemory
- [ ] CLI commands work end-to-end
- [ ] Dashboard shows real-time status
- [ ] Checkpoint/resume works

### Phase 4 Complete When:
- [ ] FP decisions documented
- [ ] BMAD agent spawning works
- [ ] Memory integration stores insights
- [ ] Cross-session learning active

---

## Dependencies

**Blocked By:**
- PLAN-008 (Critical API mismatches) - Core infrastructure must be stable

**Blocks:**
- Future autonomous work loops
- Self-improving Blackbox5 system

---

## Notes

### Ralph Technique References
- Original: Jeffrey Huntley (July 2025)
- GitHub: snarktank/ralph
- Related: Matt Pocock's "Effective Harnesses for Long-Running Agents"

### Key Design Decisions
1. One task per loop - keeps context clean
2. Sub-agents for search - preserves main context window
3. Structured progress tracking - machine and human readable
4. Exit conditions - prevents infinite loops
5. Full Blackbox5 integration - leverages existing infrastructure

---

## Next Steps

1. **Immediate:** Create Task 1.1 (Ralph Master Prompt)
2. **This Week:** Complete Phase 1 (all prompts)
3. **Next Week:** Begin Phase 2 (project selection)
4. **Ongoing:** Integration testing with existing Blackbox5 systems
