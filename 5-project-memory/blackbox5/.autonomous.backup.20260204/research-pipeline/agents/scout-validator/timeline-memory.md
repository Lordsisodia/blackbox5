# Scout Validator Timeline Memory

**Purpose:** Long-term memory of all validations performed and patterns observed
**Updated:** Automatically at the end of each run
**Format:** YAML frontmatter with markdown body
**Injected via:** SessionStart hook

---

```yaml
timeline_memory:
  version: "1.0.0"
  agent: scout-validator
  created: "2026-02-04T00:00:00Z"
  last_updated: "2026-02-04T00:00:00Z"
  total_runs: 0

# History of all validations performed
validation_history:
  # Example entry:
  # - run_id: "run-20260204-001"
  #   timestamp: "2026-02-04T10:05:00Z"
  #   worker_run_id: "run-20260204-001"
  #   source: "github.com/user/repo"
  #   patterns_validated: 3
  #   quality_score: 0.85
  #   feedback_given: 2
  #   feedback_types: ["suggestion", "praise"]
  #   issues_found: ["missed decorator pattern"]

# Worker behavior patterns observed
worker_patterns:
  # Patterns in worker's behavior over time
  extraction_strengths: []    # What they do well
  extraction_weaknesses: []   # What they miss
  improvement_trends: []      # How they're improving
  recurring_issues: []        # Issues that keep appearing

# Quality metrics over time
quality_tracking:
  completeness_scores: []     # History of completeness ratings
  accuracy_scores: []         # History of accuracy ratings
  efficiency_scores: []       # Token efficiency over time
  overall_trend: "improving"  # improving|stable|declining

# Feedback effectiveness
feedback_tracking:
  suggestions_made: 0
  suggestions_implemented: 0
  implementation_rate: 0.0    # % of feedback acted upon
  most_effective_feedback: [] # What types work best

# Current monitoring context
current_context:
  monitoring_worker_run: null  # Which worker run to check
  pending_validations: []      # Runs waiting for validation
  last_feedback_timestamp: null

# Strategy evolution
validation_strategy:
  current_focus: "completeness"  # completeness|accuracy|efficiency
  effective_approaches: []       # What's working
  ineffective_approaches: []     # What's not working
  recommended_adjustments: []    # How to improve validation
```

---

## How to Use This Memory

**At the start of each run:**
1. Read this file to understand worker's history
2. Check `current_context` for what to validate
3. Review `worker_patterns` to know what to look for
4. Use `quality_tracking` to spot trends

**Validation workflow:**
1. Find worker's current run (check their timeline-memory.md)
2. Read their output
3. Compare to patterns in `worker_patterns`
4. Provide targeted feedback based on history
5. Update this timeline with your observations

## Work Assignment Logic

**How you know what to validate:**

1. **Check `current_context.monitoring_worker_run`** - Specific run to check
2. **If null, find latest worker run** - Look in scout-worker/runs/
3. **Read worker's timeline-memory.md** - Understand what they worked on
4. **Read their THOUGHTS.md and RESULTS.md** - See their actual output
5. **Validate and provide feedback** - Write to chat-log.yaml
6. **Update this timeline** - Record your validation

## Coordination with Worker

You don't assign work to the worker - you:
- Observe what they do
- Validate their output
- Provide feedback
- Track patterns over time

The worker decides what to work on based on the shared queue.

---

*This file is automatically injected into your context via the SessionStart hook.*
