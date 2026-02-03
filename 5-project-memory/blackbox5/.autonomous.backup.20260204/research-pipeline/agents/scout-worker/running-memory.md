# Scout Worker Running Memory

**Updated:** Automatically during each run
**Purpose:** Maintain context across runs, enable learning

---

```yaml
running_memory:
  version: "1.0.0"
  agent: scout-worker
  last_updated: "2026-02-04T00:00:00Z"
  run_count: 0

current_state:
  status: idle  # idle, scanning, extracting, complete, error
  current_source: null
  current_run_id: null
  tokens_used_this_run: 0
  tokens_budget: 3000

queue:
  pending_sources: []
  in_progress: null
  completed_today: 0
  failed_today: 0

patterns:
  extracted_this_session: []
  awaiting_validation: []
  validated_count: 0

learning:
  extraction_strategies:
    - strategy: "auth-pattern-extraction"
      effectiveness: 0.0
      uses: 0

  source_types_mastered: []

  common_patterns:
    # Populated as patterns are discovered

  mistakes:
    # Log of mistakes to avoid

validator_feedback:
  pending: []
  incorporated: []

metrics:
  avg_patterns_per_source: 0
  avg_tokens_per_pattern: 0
  success_rate: 0.0

session:
  start_time: null
  sources_scanned: 0
  patterns_found: 0
```

---

## Dynamic Updates

This file is READ and UPDATED by the Scout Worker during every run:
- **At start:** Load current state
- **During run:** Update progress, learnings
- **At end:** Save final state, metrics

This enables the Worker to:
1. Remember what it learned in previous runs
2. Track its own performance
3. Apply validator feedback
4. Improve extraction strategies over time
