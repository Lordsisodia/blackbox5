# BlackBox5 Sub-Agent Team

**Purpose:** Curated sub-agent team for BlackBox5 self-improvement
**Goal:** Continuous recursive self-improvement
**Date:** 2026-02-07

---

## Philosophy

BlackBox5's sole purpose is to improve itself. Every sub-agent serves this goal.

**No UI agents. No external-facing agents.** Only agents that help BlackBox5 understand, plan, and improve itself.

---

## Core Sub-Agent Team

### 1. First Principles Agent (NEW)
**Purpose:** Break down any problem to fundamental truths

**When:** Before solving any significant problem

**Process:**
1. Strip away assumptions
2. Identify fundamental truths
3. Build up from basics
4. Question "why" recursively

**Inputs:**
- Problem statement
- Current approach (if any)
- Constraints

**Outputs:**
```yaml
first_principles_analysis:
  problem_statement: "..."
  assumptions_challenged:
    - assumption: "..."
      why_it_might_be_wrong: "..."
  fundamental_truths:
    - "..."
  build_up_approach:
    - "Start with..."
    - "Then add..."
  what_we_should_actually_do: "..."
  confidence: 0-100
```

**Always runs first** before other agents tackle a problem.

---

### 2. Context Scout
**Purpose:** Deep reconnaissance of BlackBox5 itself

**When:** Starting any improvement work

**Scans:**
- Current codebase structure
- Recent changes and patterns
- Existing documentation
- Past decisions (DECISIONS.md files)
- Past learnings (LEARNINGS.md files)
- Current STATE.yaml
- Active tasks and queue

**Outputs:**
```yaml
context_report:
  blackbox5_state:
    version: "..."
    last_major_change: "..."
    active_workflows: [...]
  relevant_history:
    similar_past_work: [...]
    lessons_from_past: [...]
  current_architecture:
    key_components: [...]
    recent_changes: [...]
  improvement_opportunities:
    - area: "..."
      evidence: "..."
      suggestion: "..."
```

---

### 3. Concept Analyzer
**Purpose:** Understand and map concepts across BlackBox5

**When:** Encountering new patterns, refactoring, or integrating discoveries

**Analyzes:**
- What concepts exist in BlackBox5
- How concepts relate to each other
- Where concepts are implemented
- Concept gaps (things we need but don't have)

**Outputs:**
```yaml
concept_map:
  concepts:
    - name: "..."
      definition: "..."
      implemented_in: [...]
      related_to: [...]
      maturity: 0-100
  gaps:
    - missing_concept: "..."
      why_needed: "..."
      suggested_approach: "..."
  consolidation_opportunities:
    - "Concept X and Y are similar, should merge"
```

---

### 4. Research Agent
**Purpose:** External research for BlackBox5 improvement

**When:** Need to understand best practices, patterns, or solutions

**Researches:**
- Similar systems and how they work
- Best practices for our patterns
- New approaches to our problems
- What others have learned

**Outputs:**
```yaml
research_report:
  query: "..."
  sources_considered: [...]
  key_findings:
    - finding: "..."
      source: "..."
      applicability_to_bb5: "..."
  recommendations:
    - action: "..."
      rationale: "..."
      effort_estimate: "..."
```

---

### 5. Architect
**Purpose:** Design improvements to BlackBox5 systems

**When:** Making structural changes, adding new capabilities

**Designs:**
- System architecture
- Component interactions
- Data flows
- Integration points

**Outputs:**
```yaml
architecture_design:
  problem: "..."
  proposed_solution:
    overview: "..."
    components:
      - name: "..."
        responsibility: "..."
        interfaces: [...]
    data_flows:
      - "..."
  trade_offs:
    - option: "..."
      pros: [...]
      cons: [...]
  migration_path:
    - phase: "..."
      changes: [...]
```

---

### 6. Planner
**Purpose:** Create actionable improvement plans

**When:** Ready to implement an improvement

**Creates:**
- Task breakdowns
- Dependency mapping
- Sequencing
- Success criteria

**Outputs:**
```yaml
improvement_plan:
  objective: "..."
  success_criteria:
    - "..."
  tasks:
    - id: "..."
      description: "..."
      dependencies: [...]
      estimated_effort: "..."
  risks:
    - risk: "..."
      mitigation: "..."
  validation_approach: "..."
```

---

### 7. Documentation Agent
**Purpose:** Maintain and improve BlackBox5 documentation

**When:** After changes, or when docs are stale

**Maintains:**
- THOUGHTS.md clarity
- DECISIONS.md completeness
- Architecture docs accuracy
- README freshness
- Concept documentation

**Outputs:**
```yaml
documentation_report:
  files_updated:
    - file: "..."
      changes: "..."
  gaps_filled:
    - "..."
  recommendations:
    - "..."
```

---

### 8. Validator
**Purpose:** Verify improvements actually work

**When:** After implementing changes

**Validates:**
- Changes match requirements
- Nothing broke
- Tests pass
- Documentation is accurate
- System still functions

**Outputs:**
```yaml
validation_report:
  status: PASS | PARTIAL | FAIL
  checks:
    - check: "..."
      result: PASS | FAIL
      evidence: "..."
  issues:
    - severity: critical | warning | info
      description: "..."
  confidence: 0-100
```

---

### 9. Bookkeeper
**Purpose:** Maintain BlackBox5 organizational hygiene

**When:** Task completion, state changes

**Updates:**
- STATE.yaml
- Timeline
- Task statuses
- Queue management
- Run folder organization

**Outputs:**
```yaml
bookkeeping_report:
  updates_made:
    - file: "..."
      change: "..."
  state_snapshot:
    active_tasks: N
    completed_tasks: N
    current_focus: "..."
```

---

## Superintelligence = Parallel First Principles + Team

Superintelligence isn't a separate agent. It's a **pattern**:

```
For complex problems:
  1. First Principles Agent (always first)
  2. Parallel specialist agents:
     - Context Scout
     - Research Agent
     - Concept Analyzer
     - Architect (if structural)
  3. Synthesis
  4. Planner (creates implementation plan)
  5. Execute
  6. Validator (verifies)
  7. Bookkeeper (updates state)
```

---

## Agent Selection Flow

```
New Improvement Opportunity
           ↓
   First Principles Agent
           ↓
   Context Scout (understand current state)
           ↓
   Is this well understood?
      ↓ YES          ↓ NO
  Research Agent    Research Agent
  +                 +
  Concept Analyzer  Concept Analyzer
           ↓
   Architect (if structural changes needed)
           ↓
   Planner (create tasks)
           ↓
   Execute (main agent or RALF)
           ↓
   Validator (verify)
           ↓
   Bookkeeper (update state)
```

---

## BMAD Skills vs Sub-Agents

**Keep BMAD as skills** because:
- They're user-facing personas (John, Alex, Mary)
- They work well for human interaction
- Sub-agents are for BlackBox5's internal self-improvement

**Sub-agents are internal**:
- No personas needed
- Focused on BlackBox5 itself
- Can run in parallel
- Don't need human-friendly output

---

## Implementation Priority

### Phase 1: Core (Week 1-2)
1. **First Principles Agent** - Foundation for all thinking
2. **Context Scout** - Understand current state
3. **Validator** - Verify improvements
4. **Bookkeeper** - Maintain state

### Phase 2: Intelligence (Week 3-4)
5. **Research Agent** - External knowledge
6. **Concept Analyzer** - Map understanding
7. **Architect** - Design improvements

### Phase 3: Execution (Week 5)
8. **Planner** - Create actionable plans
9. **Documentation Agent** - Maintain docs

### Phase 4: Integration (Week 6)
10. Superintelligence pattern (parallel execution)
11. Hook into existing workflows
12. Performance optimization

---

## Key Difference from Before

**Previous thinking:** Generic sub-agents for any task
**Now:** Curated team specifically for BlackBox5 self-improvement

**Removed:**
- UI/UX agents (not relevant to self-improvement)
- Generic BMAD sub-agents (keep as skills)
- External-facing agents

**Added:**
- First Principles Agent (fundamental)
- Context Scout (self-awareness)
- Concept Analyzer (understanding)
- Research Agent (external learning)

---

## Success Metrics

How do we know the sub-agent team is working?

1. **Lines Per Minute (LPM)** increases
2. **Task completion rate** improves
3. **Documentation quality** scores higher
4. **Fewer regressions** (Validator catching issues)
5. **Better decisions** (First Principles + Research)
6. **Faster planning** (Planner + Context Scout)

---

## Next Steps

1. Design First Principles Agent interface
2. Design Context Scout interface
3. Create proof-of-concept with these two
4. Test on actual BlackBox5 improvement task
5. Iterate based on results
