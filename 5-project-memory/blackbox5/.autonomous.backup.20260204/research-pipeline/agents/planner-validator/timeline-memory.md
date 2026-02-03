# Planner Validator Timeline Memory

**Purpose:** Long-term memory of all plan validations and strategy evolution
**Updated:** Automatically at the end of each run
**Format:** YAML frontmatter with markdown body
**Injected via:** SessionStart hook

---

```yaml
timeline_memory:
  version: "1.0.0"
  agent: planner-validator
  created: "2026-02-04T00:00:00Z"
  last_updated: "2026-02-04T00:00:00Z"
  total_runs: 0

# History of all plan validations
validation_history:
  # Example entry:
  # - run_id: "run-20260204-001"
  #   timestamp: "2026-02-04T10:25:00Z"
  #   worker_run_id: "run-20260204-001"
  #   task_id: "TASK-RAPS-001"
  #   subtasks_validated: 3
  #   estimate_accuracy: 0.85
  #   plan_quality: 0.90
  #   feedback_given: 2
  #   strategy_adjustments: ["add integration test subtask"]

# Plan quality tracking
plan_quality:
  atomic_subtasks_rate: 0.0      # % of subtasks that are atomic
  clear_criteria_rate: 0.0       # % with testable acceptance criteria
  correct_dependencies_rate: 0.0 # % with correct dependency mapping
  realistic_estimates_rate: 0.0  # % with realistic hour estimates
  overall_quality_trend: "stable" # improving|stable|declining

# Strategy effectiveness by pattern type
strategy_effectiveness:
  authentication:
    plans_validated: 0
    avg_quality: 0.0
    common_issues: []
    effective_practices: []
  middleware:
    plans_validated: 0
    avg_quality: 0.0
    common_issues: []
    effective_practices: []
  caching:
    plans_validated: 0
    avg_quality: 0.0
    common_issues: []
    effective_practices: []

# Worker behavior patterns
worker_patterns:
  planning_strengths: []      # what they do well
  planning_weaknesses: []     # what needs improvement
  estimation_tendencies: []   # over/under estimation patterns
  improvement_trends: []      # how they're improving

# Current monitoring context
current_context:
  monitoring_worker_run: null
  pending_validations: []
  plans_awaiting_outcome: []  # to track success/failure

# Strategy evolution
strategy_evolution:
  current_best_practices: []
  deprecated_approaches: []
  emerging_patterns: []
  recommended_focus: "completeness"  # completeness|accuracy|efficiency
```

---

## How to Use This Memory

**At the start of each run:**
1. Read this file to understand validation history
2. Check `plan_quality` metrics for trends
3. Review `strategy_effectiveness` for pattern-type guidance
4. Check `current_context` for what to validate

**Validation workflow:**
1. Find worker's plan to validate
2. Compare to `strategy_effectiveness` benchmarks
3. Check `worker_patterns` for known issues
4. Provide targeted feedback
5. Update this timeline with validation results

## Work Assignment Logic

**How you know what to validate:**

1. **Check `current_context.monitoring_worker_run`** - Specific run to check
2. **If null, find latest planner-worker run** - Look in planner-worker/runs/
3. **Read their task creation** - Check communications/queue.yaml
4. **Compare to plan_quality benchmarks** - Are subtasks atomic? Estimates realistic?
5. **Check strategy_effectiveness** - Any pattern-type specific issues?
6. **Validate and provide feedback** - Write to chat-log.yaml
7. **Update timeline** - Record validation and track outcomes

## Strategy Evolution

You drive planning strategy evolution by:
- Tracking which approaches lead to successful implementations
- Identifying common planning anti-patterns
- Calibrating estimation accuracy
- Validating template effectiveness

---

*This file is automatically injected into your context via the SessionStart hook.*
