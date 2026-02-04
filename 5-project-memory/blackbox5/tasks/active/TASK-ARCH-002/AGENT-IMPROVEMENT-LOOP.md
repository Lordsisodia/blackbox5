# Agent Improvement Loop - Implementation Guide

**Version:** 1.0.0
**Status:** Operational
**Created:** 2026-02-04

---

## Quick Start

Run the Scout analysis:
```bash
python3 ~/.blackbox5/2-engine/.autonomous/bin/scout-analyze.py
```

View latest report:
```bash
cat ~/.blackbox5/5-project-memory/blackbox5/.autonomous/analysis/scout-reports/scout-report-*.yaml
```

---

## What Is the Agent Improvement Loop?

An autonomous system where agents continuously find, prioritize, and implement improvements in BlackBox5.

### Core Philosophy
> "The system should improve itself while humans sleep."

---

## How It Works

### 1. Scout Phase (Detection)
**Agent:** Improvement Scout
**Frequency:** Every 5 runs or on-demand

**What it does:**
- Scans skill metrics for ineffective skills
- Analyzes recent learnings for friction patterns
- Checks documentation for drift
- Identifies recurring issues

**Output:** Scout report with scored opportunities

### 2. Planning Phase (Prioritization)
**Agent:** Planner (existing)
**Trigger:** Scout report generated

**What it does:**
- Reviews opportunities
- Converts high-scoring items to IMP-*.md tasks
- Updates improvement backlog
- Queues tasks for execution

**Output:** IMP-*.md task files

### 3. Execution Phase (Implementation)
**Agent:** RALF-Executor (existing)
**Trigger:** IMP task in queue

**What it does:**
- Reads improvement task
- Implements the change
- Validates it works
- Commits changes

**Output:** Completed improvement + run documentation

### 4. Validation Phase (Verification)
**Agent:** Verifier (future)
**Trigger:** Improvement marked complete

**What it does:**
- Verifies improvement was implemented
- Measures before/after metrics
- Checks for regressions
- Updates improvement status

**Output:** Validation report

---

## Current Status

| Component | Status | Location |
|-----------|--------|----------|
| Scout Agent | ✅ Operational | `prompts/agents/improvement-scout.md` |
| Scout Script | ✅ Operational | `bin/scout-analyze.py` |
| Analysis Reports | ✅ Generating | `.autonomous/analysis/scout-reports/` |
| Planner Integration | 🔄 Next Phase | - |
| Verifier Agent | 📋 Planned | - |
| Automation | 📋 Planned | - |

---

## First Loop Results

### Scout Analysis (2026-02-04)

**Top Finding:** 23 skills have no effectiveness data

```yaml
Opportunity:
  Category: infrastructure
  Impact: 4/5 (affects all skill-based decisions)
  Effort: 3/5 (requires automation script)
  Frequency: 3/5 (ongoing issue)
  Total Score: 13.5 (HIGH PRIORITY)

  Evidence: skill-metrics.yaml shows all 23 skills with null values
  Action: Implement automatic skill metrics collection
  Related Task: TASK-ARCH-010 (Skill Metrics Collection)
```

**Validation:** This finding directly connects to the completed TASK-ARCH-010, proving the Scout correctly identifies real problems.

---

## Scoring System

### Formula
```
total_score = (impact × 3) + (frequency × 2) - (effort × 1.5)
```

### Impact Score (1-5)
- 5: Affects >50% of tasks or critical path
- 4: Affects 30-50% of tasks
- 3: Affects 10-30% of tasks
- 2: Affects <10% but noticeable
- 1: Minor inconvenience

### Effort Score (1-5)
- 5: >2 hours, complex changes
- 4: 1-2 hours, multiple files
- 3: 30-60 minutes, focused change
- 2: 10-30 minutes, simple change
- 1: <10 minutes, trivial change

### Frequency Score (1-3)
- 3: Mentioned 5+ times or daily occurrence
- 2: Mentioned 2-4 times or weekly occurrence
- 1: Mentioned once or occasional

---

## Usage

### Manual Trigger
```bash
# Run full analysis
python3 ~/.blackbox5/2-engine/.autonomous/bin/scout-analyze.py

# View report
cat ~/.blackbox5/5-project-memory/blackbox5/.autonomous/analysis/scout-reports/scout-report-*.yaml
```

### Future: Automated Triggers
- Every 5 runs (scheduled)
- When metrics degrade (event-based)
- When 3+ learnings mention same pattern (pattern-based)
- On-demand via `/improve` command (manual)

---

## Integration with Existing Systems

```
┌─────────────────────────────────────────────────────────────────┐
│                    EXISTING SYSTEMS                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  RALF ───────────────► Task Queue ───────────────► Executor     │
│   │                       │                            │        │
│   │                       ▼                            ▼        │
│   │               ┌─────────────┐              ┌─────────────┐  │
│   │               │ tasks.yaml  │              │  Results    │  │
│   │               │ queue.yaml  │              │   Commit    │  │
│   │               └─────────────┘              └─────────────┘  │
│   │                                                              │
│   ▼                                                              │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │              IMPROVEMENT LOOP (NEW)                          │ │
│ │                                                               │ │
│ │  Scout ──► Analysis ──► IMP-*.md ──► Queue ──► Execute      │ │
│ │   │          │            │           │          │           │ │
│ │   │          ▼            ▼           ▼          ▼           │ │
│ │   │    scout-reports/  tasks/    queue.yaml   Validation    │ │
│ │   │                                                          │ │
│ │   └──────────────────────────────────────────────────────┐  │ │
│ │                      Every 5 runs                         │  │ │
│ └─────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

---

## Success Metrics

| Metric | Before | Target | How to Measure |
|--------|--------|--------|----------------|
| Scout runs | 0 | 1 per 5 runs | Count scout-report files |
| Opportunities found | 0 | 5+ per run | Scout report summaries |
| High-priority items | 0 | 2+ per run | Score >10 |
| Time to implement | Unknown | <1 week | Task completion dates |

---

## Next Steps

### Immediate (Next Session)
1. Create Planner integration to convert opportunities to tasks
2. Test full loop: Scout → Planner → Executor
3. Document learnings

### Short Term (Next Week)
1. Automate Scout to run every 5 runs
2. Create Verifier agent
3. Build improvement dashboard

### Long Term (Next Month)
1. Self-healing: Agent implements its own improvements
2. Predictive: Scout identifies issues before they become problems
3. Metrics: 50% improvement application rate

---

## Files Reference

| File | Purpose |
|------|---------|
| `2-engine/.autonomous/prompts/agents/improvement-scout.md` | Scout agent prompt |
| `2-engine/.autonomous/bin/scout-analyze.py` | Analysis script |
| `5-project-memory/blackbox5/.autonomous/analysis/scout-reports/` | Analysis outputs |
| `5-project-memory/blackbox5/operations/improvement-pipeline.yaml` | Pipeline config |
| `5-project-memory/blackbox5/operations/improvement-backlog.yaml` | Improvement queue |

---

## Troubleshooting

### Scout finds no opportunities
- Check skill-metrics.yaml exists and is readable
- Verify recent run folders have LEARNINGS.md
- Ensure improvement-backlog.yaml is accessible

### Scores seem wrong
- Review impact/effort/frequency scoring in Scout prompt
- Adjust formula weights in scout-analyze.py
- Validate against first principles

### Loop not completing
- Check events.yaml for Scout completion
- Verify queue.yaml is being updated
- Ensure Executor is picking up IMP tasks

---

## Conclusion

The Agent Improvement Loop is operational and has already identified its first high-priority improvement. The foundation is in place for autonomous self-improvement.

**Key Achievement:** A system that can find its own problems.

**Next Milestone:** A system that can fix its own problems.
