# Scout Validator Running Memory

**Updated:** Automatically during each run
**Purpose:** Track worker performance, maintain feedback loop

---

```yaml
running_memory:
  version: "1.0.0"
  agent: scout-validator
  last_updated: "2026-02-04T00:00:00Z"
  run_count: 0

current_state:
  status: idle  # idle, monitoring, validating, complete
  monitoring_run_id: null
  worker_status: unknown

worker_tracking:
  current_run:
    run_id: null
    source: null
    start_time: null
    patterns_found: 0
    tokens_used: 0

  history:
    # Last 10 runs

validation_queue:
  pending: []
  in_progress: null
  completed_today: 0

feedback:
  given_this_session: []
  worker_acknowledged: []
  worker_implemented: []

learning:
  worker_patterns:
    # Patterns in Worker's behavior

  common_mistakes:
    # Mistakes Worker often makes

  improvement_suggestions:
    # Suggestions to give Worker

  effective_strategies:
    # What works well

metrics:
  validation_accuracy: 0.0
  feedback_acceptance_rate: 0.0
  worker_improvement_rate: 0.0

session:
  start_time: null
  validations_completed: 0
  feedback_given: 0
```
