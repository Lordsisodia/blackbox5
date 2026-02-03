# Planner Worker Running Memory

```yaml
running_memory:
  version: "1.0.0"
  agent: planner-worker
  last_updated: "2026-02-04T00:00:00Z"
  run_count: 0

current_state:
  status: idle
  current_recommendation: null
  current_run_id: null
  tokens_used_this_run: 0
  tokens_budget: 3600

queue:
  pending_recommendations: []
  in_progress: null
  completed_today: 0

tasks_created:
  this_session: []
  total_hours_estimated: 0
  total_hours_actual: 0

templates:
  effective:
    # Task structures that worked well
  ineffective:
    # Task structures that didn't work

estimation_accuracy:
  by_task_type: {}
  by_complexity: {}
  overall: 0.0

learning:
  decomposition_strategies: []
  dependency_patterns: []
  bb5_integration_patterns: []

metrics:
  avg_tasks_per_recommendation: 0
  estimation_error_rate: 0.0
  task_completion_rate: 0.0
```
