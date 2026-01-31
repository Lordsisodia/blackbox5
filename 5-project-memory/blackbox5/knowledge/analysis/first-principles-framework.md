# First Principles Review Framework

**Purpose:** Comprehensive framework for systematic self-improvement through periodic reviews
**Version:** 1.0.0
**Created:** 2026-02-01

---

## Philosophy

### Why First Principles?

Traditional retrospectives ask "what happened?" First principles reviews ask "why did it happen and what does it mean for the system?"

The goal is not to document history but to **evolve the system** based on evidence.

### Core Principles

1. **Evidence Over Opinion**
   - Every finding must cite specific runs
   - Patterns require multiple data points
   - Decisions trace back to evidence

2. **System Over Symptoms**
   - Fix the process, not just the problem
   - Look for root causes, not proximate causes
   - Address categories, not incidents

3. **Action Over Analysis**
   - Reviews must result in decisions
   - Every pattern leads to a course correction
   - Analysis without action is waste

4. **Continuous Over Periodic**
   - Reviews are checkpoints, not the only improvement mechanism
   - Learnings captured continuously
   - Reviews synthesize and decide

---

## Review Architecture

### Trigger Mechanisms

```yaml
review_triggers:
  scheduled:
    frequency: every_5_runs
    condition: loop_number % 5 == 0
    priority: high
    override: true  # Takes precedence over normal planning

  event_driven:
    velocity_drop:
      condition: completion_rate < 70% for 3 consecutive runs
      priority: critical
    error_spike:
      condition: error_rate > 30% for 2 consecutive runs
      priority: critical
    manual:
      condition: operator_request == true
      priority: high
```

### Review States

```
IDLE → TRIGGERED → GATHERING → ANALYZING → DECIDING → DOCUMENTING → COMPLETE
```

**State Definitions:**
- **IDLE:** Normal operation, monitoring for triggers
- **TRIGGERED:** Review condition met, preparing to start
- **GATHERING:** Collecting data from last N runs
- **ANALYZING:** Identifying patterns and correlations
- **DECIDING:** Making course correction decisions
- **DOCUMENTING:** Writing review document
- **COMPLETE:** Review finished, improvements queued

---

## Pattern Recognition Framework

### Pattern Taxonomy

#### 1. Execution Patterns
**Definition:** How work gets done

**Examples:**
- Pre-execution research correlation with success
- Context level appropriateness
- Sub-agent deployment effectiveness
- Skill usage patterns

**Detection:**
```
For each run in last_5_runs:
  - Did it follow the process?
  - What was the outcome?
  - What was different from other runs?
```

#### 2. Outcome Patterns
**Definition:** Results and their predictors

**Examples:**
- Task types with highest failure rates
- Estimated vs actual duration trends
- Success rate by context level
- Quality gate pass/fail patterns

**Detection:**
```
Aggregate metrics across last_5_runs:
  - Success/failure by category
  - Duration trends
  - Rework frequency
  - Block reasons
```

#### 3. Learning Patterns
**Definition:** What we learn and how we use it

**Examples:**
- Learning quality (specific vs vague)
- Learning-to-improvement conversion
- Recurring themes across learnings
- Validated vs invalidated assumptions

**Detection:**
```
Analyze LEARNINGS.md files:
  - Categories of learnings
  - Actionability score
  - Pattern frequency
  - Implementation status
```

#### 4. Decision Patterns
**Definition:** How decisions are made

**Examples:**
- Decision reversibility distribution
- Decision outcomes vs expectations
- Decision speed vs quality tradeoffs
- Who/what drives decisions

**Detection:**
```
Review DECISIONS.md files:
  - Decision types
  - Rationale quality
  - Outcome alignment
  - Reversibility patterns
```

### Pattern Significance Scoring

```yaml
pattern_significance:
  frequency_weight: 0.4
  impact_weight: 0.4
  actionability_weight: 0.2

  score_calculation: |
    significance = (frequency * 0.4) + (impact * 0.4) + (actionability * 0.2)

  thresholds:
    critical: >= 0.8  # Immediate action required
    high: >= 0.6      # Action in next cycle
    medium: >= 0.4    # Monitor and consider
    low: < 0.4        # Note but defer
```

---

## Course Correction Framework

### Decision Types

#### 1. Process Changes
**When:** Execution patterns show systemic issues
**Examples:**
- Make pre-execution research mandatory
- Change context level assignment rules
- Modify quality gate requirements

**Implementation:**
- Update LEGACY.md or CLAUDE.md
- Document in operations/
- Train/notify affected agents

#### 2. Guidance Updates
**When:** Instructions unclear or incorrect
**Examples:**
- Clarify sub-agent deployment rules
- Update skill selection criteria
- Refine decision framework

**Implementation:**
- Update CLAUDE.md
- Version the guidance
- Communicate changes

#### 3. Infrastructure Changes
**When:** Tools/templates inadequate
**Examples:**
- Create new templates
- Add/remove skills
- Modify state tracking

**Implementation:**
- Update files in operations/ or .templates/
- Test with pilot runs
- Roll out gradually

#### 4. Skill Adjustments
**When:** Skills not effective
**Examples:**
- Tune skill triggers
- Consolidate redundant skills
- Add missing skills

**Implementation:**
- Update skill definitions
- Update skill-usage.yaml
- Retrain if necessary

### Decision Framework

```yaml
decision_criteria:
  must_have:
    - evidence_based: "Pattern appears in 2+ runs"
    - specific: "Exact change is defined"
    - reversible: "Can undo if it doesn't work"
    - validated: "Success criteria defined"

  should_have:
    - measurable: "Can track if it helped"
    - scoped: "Affects limited area"
    - aligned: "Supports core goals"

  nice_to_have:
    - automated: "Can be applied automatically"
    - immediate: "Benefit is immediate"
```

### Reversibility Levels

```yaml
reversibility:
  high:
    description: "Can undo in single run"
    examples:
      - "Try different context level"
      - "Use alternative skill"
      - "Adjust quality gate order"

  medium:
    description: "Can undo in 2-3 runs"
    examples:
      - "Modify template structure"
      - "Add new skill"
      - "Change default parameters"

  low:
    description: "Requires significant effort to undo"
    examples:
      - "Restructure folders"
      - "Change communication protocol"
      - "Modify core workflow"
```

---

## Review Quality Metrics

### Input Quality

```yaml
input_quality:
  data_completeness:
    - all_runs_documented: "THOUGHTS.md exists for all 5 runs"
    - results_recorded: "RESULTS.md exists for all 5 runs"
    - decisions_logged: "DECISIONS.md exists for all 5 runs"
    - learnings_captured: "LEARNINGS.md exists for all 5 runs"

  data_quality:
    - specific_learnings: "Learnings cite specific examples"
    - clear_decisions: "Decisions have rationale"
    - complete_thoughts: "Thoughts show reasoning process"
```

### Process Quality

```yaml
process_quality:
  coverage:
    - all_runs_reviewed: "Each of 5 runs analyzed"
    - all_categories_checked: "Execution, outcome, learning, decision patterns"
    - cross_run_analysis: "Comparisons made between runs"

  depth:
    - root_cause_identified: "Not just symptoms"
    - correlations_found: "Relationships between variables"
    - predictions_made: "Expected outcomes defined"
```

### Output Quality

```yaml
output_quality:
  actionability:
    - decisions_documented: "Specific course corrections defined"
    - improvements_queued: "Improvement tasks created"
    - metrics_defined: "Success criteria specified"

  completeness:
    - all_sections_filled: "Template fully completed"
    - evidence_cited: "Claims backed by data"
    - next_steps_clear: "Priorities unambiguous"
```

---

## Integration with Other Systems

### Improvement Pipeline

```
┌─────────────────────────────────────────────────────────────┐
│  FIRST PRINCIPLES REVIEW (every 5 runs)                    │
│  ├── Pattern Analysis                                       │
│  ├── Course Correction Decisions                           │
│  └── Improvement Tasks Created                             │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│  IMPROVEMENT QUEUE                                         │
│  ├── Prioritized by impact/effort                          │
│  ├── Assigned to appropriate agent                         │
│  └── Tracked through implementation                        │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│  IMPLEMENTATION                                            │
│  ├── Change made                                           │
│  ├── Metrics captured (before/after)                       │
│  └── Validation criteria checked                           │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│  NEXT REVIEW (validates improvement)                       │
│  ├── Did the change help?                                  │
│  ├── Should we keep it?                                    │
│  └── What else did we learn?                               │
└─────────────────────────────────────────────────────────────┘
```

### Learning Capture

Reviews synthesize individual learnings into system insights:

```
Individual Learning (per run)
    │
    ├── Pattern detected across multiple learnings
    │
    ▼
System Insight (in review)
    │
    ├── Course correction decision made
    │
    ▼
Improvement Task (queued)
    │
    ├── Implemented and validated
    │
    ▼
Guidance Update (permanent)
```

### Goal Tracking

Reviews validate progress toward improvement goals:

```yaml
goal_validation:
  CLAUDE.md_effectiveness:
    metric: "task_initiation_time"
    review_check: "Are we starting tasks faster?"

  LEGACY.md_efficiency:
    metric: "skill_selection_accuracy"
    review_check: "Are we using the right skills?"

  system_flow:
    metric: "missed_file_errors"
    review_check: "Are we finding the right files?"

  skills_optimization:
    metric: "skill_hit_rate"
    review_check: "Are skills triggering when needed?"
```

---

## Implementation Guide

### For Planner Agents

**When review is triggered:**

1. **Pause normal planning**
   ```yaml
   mode: REVIEW
   priority: highest
   reason: "First principles review due"
   ```

2. **Gather data**
   ```bash
   # Read last 5 runs
   for run in runs/executor/run-{N-4..N}/; do
     read THOUGHTS.md RESULTS.md DECISIONS.md LEARNINGS.md
   done
   ```

3. **Analyze patterns**
   - Use pattern recognition framework
   - Score pattern significance
   - Document findings

4. **Make decisions**
   - Apply decision framework
   - Assess reversibility
   - Define validation metrics

5. **Create outputs**
   - Review document → `knowledge/analysis/`
   - Improvement tasks → `.autonomous/tasks/improvements/`
   - State updates → `STATE.yaml`

6. **Resume planning**
   ```yaml
   mode: PLANNING
   next_review_run: current + 5
   ```

### For Executor Agents

**When executing improvement tasks from reviews:**

1. **Read the review**
   - Understand the pattern that prompted the improvement
   - Know the expected outcome
   - Note validation criteria

2. **Implement carefully**
   - Make reversible changes where possible
   - Document the change thoroughly
   - Capture baseline metrics

3. **Validate**
   - Check if success criteria are met
   - Document actual vs expected outcomes
   - Note any unexpected effects

---

## Example Reviews

### Example 1: Pre-Execution Research Value

**Pattern Detected:**
- Run 45: No pre-read, failed (assumed wrong file structure)
- Run 46: Pre-read 3 files, succeeded
- Run 47: No pre-read, partial success (had to backtrack)
- Run 48: Pre-read 5 files, succeeded
- Run 49: Pre-read 2 files, succeeded

**Analysis:**
- Success rate without pre-read: 0%
- Success rate with pre-read: 100%
- Pattern significance: 0.95 (critical)

**Decision:**
- Make pre-execution research mandatory for implement tasks
- Update LEGACY.md with file count thresholds
- Reversibility: High (can skip if needed)

**Validation:**
- Track success rate for next 5 runs
- Target: Maintain >90% success rate

### Example 2: Context Level Appropriateness

**Pattern Detected:**
- Context level 1-2 tasks: 95% completion, no overflows
- Context level 3 tasks: 60% completion, 40% had overflows
- Context level 4 tasks: 80% completion, used sub-agents

**Analysis:**
- Level 3 is a "danger zone" - too complex for direct, not complex enough for sub-agents
- Either split level 3 tasks or force sub-agent usage
- Pattern significance: 0.85 (critical)

**Decision:**
- Redefine context levels: 1-2 (direct), 3-4 (sub-agents)
- Update task estimation guidelines
- Reversibility: Medium (can adjust thresholds)

**Validation:**
- Monitor completion rates by level
- Target: >85% completion for all levels

---

## Appendix: Review Checklist

### Pre-Review
- [ ] Review trigger confirmed (run % 5 == 0)
- [ ] Last 5 runs identified
- [ ] All run files accessible
- [ ] Template ready

### During Review
- [ ] All 5 runs read and understood
- [ ] Execution patterns identified
- [ ] Outcome patterns identified
- [ ] Learning patterns identified
- [ ] Decision patterns identified
- [ ] Pattern significance scored
- [ ] Course corrections decided
- [ ] Improvements queued
- [ ] Next focus defined

### Post-Review
- [ ] Review document created
- [ ] STATE.yaml updated
- [ ] Events logged
- [ ] Improvement tasks created (if any)
- [ ] Next review scheduled
- [ ] Review quality self-assessed

---

**This framework is a living document.** Update it based on review learnings.
