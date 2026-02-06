# Agent Improvement Loop Design

**Task:** TASK-ARCH-002: Execute First Improvement Loop
**Status:** Design Document
**Created:** 2026-02-04

---

## Overview

This document proposes an **Agent Improvement Loop** - an autonomous system where agents continuously find, prioritize, and implement improvements in BlackBox5. This builds on the existing improvement pipeline but adds autonomous agent capabilities.

---

## Core Concept

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     AGENT IMPROVEMENT LOOP                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐  │
│   │   ANALYZE   │───▶│  PRIORITIZE │───▶│  IMPLEMENT  │───▶│   VALIDATE  │  │
│   │   (Scout)   │    │  (Planner)  │    │ (Executor)  │    │ (Verifier)  │  │
│   └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘  │
│          │                  │                  │                  │         │
│          ▼                  ▼                  ▼                  ▼         │
│   ┌─────────────────────────────────────────────────────────────────────┐  │
│   │                    CONTINUOUS FEEDBACK LOOP                          │  │
│   │  Learnings → Patterns → Improvements → Metrics → Learnings...        │  │
│   └─────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Agent Roles in Improvement Loop

### 1. Scout Agent (Analyzer)
**Purpose:** Continuously scan BlackBox5 for improvement opportunities

**Responsibilities:**
- Scan codebase for patterns, anti-patterns, and friction points
- Analyze run history (THOUGHTS.md, LEARNINGS.md files)
- Check for documentation drift
- Identify skill gaps or ineffective skills
- Monitor metrics for degradation

**Inputs:**
- Previous run folders (`runs/*/LEARNINGS.md`)
- Current codebase state
- Skill metrics (`operations/skill-metrics.yaml`)
- Improvement backlog (`operations/improvement-backlog.yaml`)

**Outputs:**
- Analysis reports with scored improvement opportunities
- Pattern detection (recurring issues)
- Quick wins (low effort, high impact)

**Trigger Conditions:**
- Every N runs (configurable, default: 5)
- When metrics degrade
- On-demand via `/improve` command

---

### 2. Planner Agent (Prioritizer)
**Purpose:** Convert analysis into actionable improvement tasks

**Responsibilities:**
- Review Scout's findings
- Score improvements (impact × effort × urgency)
- Create improvement tasks (IMP-*.md files)
- Update improvement backlog
- Decide which improvements to implement next

**Scoring Formula:**
```
score = (impact × 3) + (recency × 2) + (frequency × 2) - (effort × 1.5)

Where:
- impact: 1-5 (5 = affects all tasks)
- recency: 1-3 (3 = found in last run)
- frequency: 1-3 (3 = mentioned 5+ times)
- effort: 1-5 (5 = >2 hours)
```

**Outputs:**
- Prioritized improvement queue
- IMP-*.md task files
- Updated backlog.yaml

---

### 3. Executor Agent (Implementer)
**Purpose:** Execute improvement tasks

**Responsibilities:**
- Read improvement task (IMP-*.md)
- Implement the improvement
- Validate the change works
- Document in run folder
- Commit changes

**Same as existing RALF-Executor**, but specialized for improvements:
- Smaller, focused tasks
- Must include validation
- Must measure before/after

---

### 4. Verifier Agent (Validator)
**Purpose:** Ensure improvements actually work

**Responsibilities:**
- Verify improvement was implemented correctly
- Measure metrics before/after
- Check for regressions
- Validate against first principles
- Update improvement status

**Validation Checks:**
- [ ] Files modified as specified
- [ ] No syntax errors introduced
- [ ] Tests pass (if applicable)
- [ ] Metrics improved or maintained
- [ ] Documentation updated

---

## Improvement Loop Flow

### Phase 1: Trigger

**Automatic Triggers:**
1. **Scheduled:** Every 5 runs (configurable)
2. **Metric-based:** When skill effectiveness drops below threshold
3. **Event-based:** When 3+ learnings mention same pattern

**Manual Triggers:**
1. `/improve` - Run full improvement cycle
2. `/improve analyze` - Run Scout analysis only
3. `/improve quick` - Find and implement quick wins only

---

### Phase 2: Analysis (Scout)

```yaml
analysis_areas:
  - name: "skill_effectiveness"
    source: "operations/skill-metrics.yaml"
    check: "effectiveness_score < 70 OR success_rate < 80%"

  - name: "documentation_drift"
    source: "docs/ vs codebase"
    check: "Docs describe 'should be' not 'is'"

  - name: "recurring_issues"
    source: "runs/*/LEARNINGS.md"
    check: "Same issue mentioned 3+ times"

  - name: "process_friction"
    source: "THOUGHTS.md challenges sections"
    check: "Tasks taking >2x estimated time"

  - name: "missing_patterns"
    source: "codebase analysis"
    check: "Common patterns not abstracted"
```

**Output:** `analysis-report-[timestamp].yaml`

---

### Phase 3: Prioritization (Planner)

**Convert findings to improvements:**

```yaml
improvement:
  id: "IMP-[timestamp]-[seq]"
  source_analysis: "analysis-report-[timestamp]"
  category: "process|technical|documentation|skills|infrastructure"
  title: "Clear improvement title"
  description: "What to improve and why"
  impact_score: 1-5
  effort_score: 1-5
  frequency_score: 1-3
  total_score: [calculated]
  status: "pending"
```

**Queue Management:**
- Max 10 improvements in active queue
- High priority (>80 score) can preempt regular tasks
- Every 3rd task from main queue: check improvement queue

---

### Phase 4: Implementation (Executor)

**Same as RALF-Executor workflow:**
1. Read IMP-*.md task
2. Pre-execution research
3. Skill selection
4. Execute with verification
5. Document in run folder
6. Commit changes

**Additional Requirements:**
- Must measure baseline before changes
- Must document expected improvement
- Must include rollback plan

---

### Phase 5: Validation (Verifier)

**Post-implementation checks:**

```yaml
validation:
  improvement_id: "IMP-[timestamp]-[seq]"
  timestamp: "[ISO timestamp]"

  checks:
    - name: "files_modified"
      expected: [list of files]
      actual: [verified files]
      status: "pass|fail"

    - name: "metrics_comparison"
      before: [baseline metrics]
      after: [current metrics]
      improvement_pct: [calculated]

    - name: "regression_check"
      tests_passed: true|false
      no_new_errors: true|false

  result: "success|partial|failed"
  next_action: "complete|retry|rollback"
```

---

## Integration with Existing Systems

### 1. RALF Integration

The improvement loop runs **within** RALF:
- Scout = RALF agent with Scout prompt
- Planner = RALF agent with Planner prompt
- Executor = Existing RALF-Executor
- Verifier = RALF agent with Verifier prompt

### 2. Improvement Pipeline Integration

```
Existing Pipeline          Improvement Loop
─────────────────         ─────────────────
LEARNINGS.md    ───────▶  Scout Analysis
     │                         │
     ▼                         ▼
improvement-    ◀────────  Pattern Detection
backlog.yaml         │
     │               │
     ▼               ▼
IMP-*.md files  ◀─── Planner Prioritization
     │
     ▼
RALF-Executor   ───▶ Implementation
     │
     ▼
Validation      ◀─── Verifier Agent
```

### 3. Task System Integration

Improvement tasks are **first-class tasks**:
- Stored in `tasks/active/IMP-*/`
- Follow same task format
- Queued in `queue.yaml`
- Tracked in `tasks.yaml`

---

## Implementation Plan

### Step 1: Create Scout Agent (30 min)
- [ ] Write `prompts/agents/improvement-scout.md`
- [ ] Create `bin/scout-analyze.py` script
- [ ] Add analysis report template

### Step 2: Create Verifier Agent (20 min)
- [ ] Write `prompts/agents/improvement-verifier.md`
- [ ] Create `bin/verify-improvement.py` script

### Step 3: Update Planner (15 min)
- [ ] Add improvement scoring to Planner prompt
- [ ] Create `bin/prioritize-improvements.py`

### Step 4: Create Loop Orchestrator (25 min)
- [ ] Write `bin/improvement-loop.py`
- [ ] Add trigger conditions
- [ ] Integrate with RALF

### Step 5: Testing (20 min)
- [ ] Test Scout analysis
- [ ] Test improvement creation
- [ ] Test full loop

**Total: ~110 minutes**

---

## Success Metrics

| Metric | Before | Target | Measurement |
|--------|--------|--------|-------------|
| Improvement application rate | 2% | 50% | Improvements implemented / Learnings captured |
| Time from learning to task | Unknown | <5 runs | Timestamp analysis |
| Scout runs completed | 0 | 1 per 5 runs | Run counter |
| Validated improvements | 0 | 80% | With before/after metrics |

---

## First Implementation (TASK-ARCH-002)

For this first loop, let's implement:

1. **Scout Analysis** of root directory (TASK-ARCH-001A)
2. **Select top 3 improvements** from the analysis
3. **Implement** each improvement with verification
4. **Document** the process for future loops

This will validate the loop design while completing the assigned task.

---

## Next Steps

1. Review this design
2. Approve approach
3. Implement Scout agent
4. Run first analysis
5. Implement improvements
6. Document learnings

---

## Appendix: File Locations

```
2-engine/
└── .autonomous/
    ├── prompts/
    │   └── agents/
    │       ├── improvement-scout.md      # NEW
    │       └── improvement-verifier.md   # NEW
    └── bin/
        ├── scout-analyze.py              # NEW
        ├── prioritize-improvements.py    # NEW
        ├── verify-improvement.py         # NEW
        └── improvement-loop.py           # NEW

5-project-memory/blackbox5/
├── operations/
│   └── improvement-loop.yaml             # NEW (config)
└── .autonomous/
    └── analysis/
        └── scout-reports/                # NEW (analysis outputs)
```
