# Analyst Worker Running Memory

```yaml
running_memory:
  version: "1.0.0"
  agent: analyst-worker
  last_updated: "2026-02-04T00:00:00Z"
  run_count: 0

current_state:
  status: idle
  current_pattern: null
  current_run_id: null
  tokens_used_this_run: 0
  tokens_budget: 4800

queue:
  pending_patterns: []
  in_progress: null
  completed_today: 0

analyses:
  completed_this_session: []
  decisions:
    recommend: 0
    defer: 0
    reject: 0

scoring_model:
  value_factors:
    relevance_to_bb5:
      weight: 0.4
      calibration: 1.0
    innovation_factor:
      weight: 0.2
      calibration: 1.0
    community_adoption:
      weight: 0.2
      calibration: 1.0
    maintainer_quality:
      weight: 0.1
      calibration: 1.0
    documentation_quality:
      weight: 0.1
      calibration: 1.0

  complexity_factors:
    lines_of_code:
      weight: 0.3
      calibration: 1.0
    dependency_count:
      weight: 0.3
      calibration: 1.0
    breaking_changes_risk:
      weight: 0.2
      calibration: 1.0
    testing_effort:
      weight: 0.2
      calibration: 1.0

learning:
  accurate_assessments: []
  inaccurate_assessments: []
  pattern_type_expertise: {}

metrics:
  avg_analysis_time: 0
  decision_accuracy: 0.0
  token_efficiency: 0.0
```
