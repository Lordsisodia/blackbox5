# Sub-Agent Architecture Research Synthesis

**Date:** 2026-02-07
**Sources:** 3 parallel research sub-agents

---

## Key Findings

### BlackBox5 Has 8 Major Workflows

1. **Scout** - Discovers external patterns (GitHub repos)
2. **Analyzer** - Analyzes patterns, creates summaries
3. **Planner** - Creates integration plans and tasks
4. **RALF (Dual)** - Planner + Executor continuous loop
5. **Dual-RALF Research Pipeline** - 6-agent parallel system
6. **BB5 CLI** - Navigation and task management
7. **Redis-Based System** - Production multi-agent orchestration
8. **Research-to-Implementation Flow** - End-to-end pipeline

### 35+ Custom Prompts Exist

**Categories:**
- RALF Core (blackbox5.md, ralf.md, ralf-executor.md, etc.)
- RALF Identity (identity.md, executor-identity.md, planner-identity.md)
- RALF Agents (intelligent-scout.md, improvement-scout.md, six-agent-pipeline.md)
- Claude Config (CLAUDE.md, OUTPUT_STYLE.md)
- Claude Agents (7 agent definitions)
- BMAD Skills (9 skills with personas)
- Superintelligence Protocol (7-step process)

### 7 Critical Integration Points Found

| Priority | Location | Trigger | Current Hook |
|----------|----------|---------|--------------|
| 1 | `bb5-claim` | Task claimed | Run folder creation |
| 2 | `bb5-complete` | Task completion | Validation → RETAIN |
| 3 | `session-start-blackbox5.sh` | Session start | Agent detection |
| 4 | `stop-validate-docs.sh` | Session end | Doc validation |
| 5 | `storage_backend.py` | Queue operations | File locking |
| 6 | `bb5-timeline` | Timeline updates | Event append |
| 7 | `bb5-generate-state.py` | State updates | After generation |

---

## Refined Sub-Agent Architecture

Based on research, here are the **actual sub-agents we need**:

### Core Sub-Agents (Must Have)

#### 1. **Task Validator** (Validator)
**Hook:** `bb5-complete` after validation, before RETAIN

**Purpose:** Verify task completion against requirements

**Inputs:**
- Task requirements (from task.md)
- Claimed changes (from main agent)
- Git diff or file changes
- Test results

**Outputs:**
```yaml
validation_report:
  status: PASS | FAIL | PARTIAL
  score: 0-100
  issues:
    - severity: critical|warning|info
      description: "..."
      location: "file:line"
  recommendations:
    - "..."
```

**Context:**
- Read-only access to task files and code
- Can run tests, linters, type checks
- Cannot modify files

---

#### 2. **Bookkeeper**
**Hook:** `bb5-complete` after RETAIN, before archiving

**Purpose:** Maintain BlackBox5 administrative hygiene

**Inputs:**
- Task ID and final status
- Run folder path
- Changes summary
- Validation report

**Outputs:**
- Updated THOUGHTS.md (summarized)
- Updated DECISIONS.md (key decisions extracted)
- Updated LEARNINGS.md (lessons learned)
- Updated TIMELINE.md (progress entry)
- Updated task status

**Context:**
- Write access to run folder documentation
- Read access to task structure
- Can read previous runs for context

---

#### 3. **Superintelligence** (SI)
**Trigger:** Complex architecture/design questions

**Purpose:** Multi-perspective analysis through parallel sub-agents

**Architecture:**
```
Superintelligence (orchestrator)
  ├── si-context-scanner (parallel)
  ├── si-goal-analyzer (parallel)
  ├── si-constraint-finder (parallel)
  ├── si-pattern-researcher (parallel)
  └── si-risk-analyzer (parallel)
       ↓
  Synthesizer Agent
       ↓
  Final Recommendation
```

**Parallel Sub-Agents:**

| Sub-Agent | Purpose | Research Focus |
|-----------|---------|----------------|
| `si-context-scanner` | Scan relevant projects/folders | File structure, dependencies, existing code |
| `si-goal-analyzer` | Analyze and clarify the goal | Requirements, constraints, success criteria |
| `si-constraint-finder` | Identify constraints | Technical, business, time, resource limits |
| `si-pattern-researcher` | Research similar solutions | Best practices, prior art, examples |
| `si-risk-analyzer` | Identify risks and edge cases | Failure modes, assumptions, unknowns |

**Outputs:**
```yaml
superintelligence_report:
  recommendation: "..."
  confidence: 0-100
  key_assumptions:
    - "..."
  risks:
    - severity: high|medium|low
      description: "..."
      mitigation: "..."
  alternatives_considered:
    - approach: "..."
      rejected_because: "..."
  implementation_path:
    - "Step 1"
    - "Step 2"
  research_findings:
    context_scanner: {...}
    goal_analyzer: {...}
    constraint_finder: {...}
    pattern_researcher: {...}
    risk_analyzer: {...}
```

---

#### 4. **Context Gatherer**
**Trigger:** Before complex tasks

**Purpose:** Pre-task context collection

**Inputs:**
- Task description
- Project scope hints
- File patterns to look for

**Outputs:**
```yaml
context_report:
  project_summary:
    name: "..."
    type: "..."
    key_files: [...]
  relevant_files:
    - path: "..."
      relevance: 0-100
      reason: "..."
  dependency_map:
    - component: "..."
      depends_on: [...]
  architecture_overview: "..."
  suggested_approach: "..."
```

---

### BMAD Roles: Keep as Skills (Not Sub-Agents)

**Decision:** BMAD roles (pm, architect, analyst, etc.) remain as **skills**, not sub-agents.

**Rationale:**
- They already work well as prompt-based skills
- Converting adds overhead without clear benefit
- Main agent can invoke them directly for quick tasks
- For complex BMAD work, use Superintelligence sub-agent

---

## Sub-Agent Call Patterns

### Simple Task Flow
```
Main Agent
  ├── Does work
  ├── Calls Validator (sequential)
  └── Calls Bookkeeper (sequential)
       └── Done
```

### Complex Task Flow
```
Main Agent
  ├── Calls Context Gatherer (sequential)
  ├── Does work (with context)
  ├── Calls Validator (sequential)
  └── Calls Bookkeeper (sequential)
       └── Done
```

### Superintelligence Flow
```
Main Agent
  ├── Calls Superintelligence (sequential)
  │     └── Spawns 5 parallel research agents
  │     └── Synthesizes results
  │     └── Returns recommendation
  ├── Acts on recommendation
  ├── Calls Validator (sequential)
  └── Calls Bookkeeper (sequential)
       └── Done
```

---

## Implementation Priority

### Phase 1: Foundation (Week 1)
1. **Validator** - Highest impact, clear scope
2. **Bookkeeper** - Automates current manual burden

### Phase 2: Intelligence (Week 2-3)
3. **Context Gatherer** - Enables better task prep
4. **Superintelligence** - Complex problem solving

### Phase 3: Refinement (Week 4)
5. Performance optimization
6. Cost analysis
7. Hook integration

---

## Hook Integration Plan

### Immediate (Phase 1)
- Modify `bb5-complete` to call Validator after validation
- Modify `bb5-complete` to call Bookkeeper after RETAIN

### Later (Phase 2)
- Add Context Gatherer call to `bb5-claim` (optional enrichment)
- Add Superintelligence trigger to complex task detection

---

## Key Insights

1. **Validator and Bookkeeper are the highest value** - They solve real pain points (tasks not validated, docs not updated)

2. **Superintelligence should spawn 5 parallel agents** - Not just one. Each researches a different dimension.

3. **BMAD skills stay as skills** - No need to convert to sub-agents

4. **Integration points already exist** - The hook system in `.claude/hooks/` is ready

5. **File-based communication** - Match existing BlackBox5 patterns (YAML files, not APIs)

---

## Open Questions

1. Token/cost overhead of sub-agents vs direct skills?
2. How to handle sub-agent failures?
3. Should sub-agents write to dedicated files or modify existing?
4. How much context to pass to parallel Superintelligence agents?

---

## Files Referenced

- `~/.blackbox5/bin/bb5-complete` - Task completion with validation
- `~/.blackbox5/bin/bb5-claim` - Task claiming with run folder creation
- `~/.blackbox5/.claude/hooks/session-start-blackbox5.sh` - Session start
- `~/.blackbox5/.claude/hooks/stop-validate-docs.sh` - Session end validation
- `~/.blackbox5/2-engine/.autonomous/prompts/` - RALF prompts
- `~/.claude/skills/` - BMAD skills
- `~/.blackbox5/6-roadmap/01-research/superintelligence-protocol/` - SI protocol
