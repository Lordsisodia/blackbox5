# Planner Worker Timeline Memory

**Purpose:** Long-term memory of all task plans created and planning strategy evolution
**Updated:** Automatically at the end of each run
**Format:** YAML frontmatter with markdown body
**Injected via:** SessionStart hook

---

```yaml
timeline_memory:
  version: "1.0.0"
  agent: planner-worker
  created: "2026-02-04T00:00:00Z"
  last_updated: "2026-02-04T00:00:00Z"
  total_runs: 0

# History of all plans created
planning_history:
  # Example entry:
  # - run_id: "run-20260204-001"
  #   timestamp: "2026-02-04T10:20:00Z"
  #   pattern_id: "P-001"
  #   task_id: "TASK-RAPS-001"
  #   subtasks_created: 3
  #   estimated_hours: 7
  #   actual_hours: 8
  #   completion_status: "completed"
  #   quality_score: 0.90

# Planning templates by pattern type
templates:
  authentication:
    typical_subtasks: ["core", "tests", "docs", "integration"]
    typical_hours: [4, 2, 1, 2]
    success_rate: 0.0
    iterations_needed: []
  middleware:
    typical_subtasks: ["core", "tests", "docs", "examples"]
    typical_hours: [3, 2, 1, 1]
    success_rate: 0.0
    iterations_needed: []
  caching:
    typical_subtasks: ["core", "tests", "docs", "benchmarks"]
    typical_hours: [3, 2, 1, 1]
    success_rate: 0.0
    iterations_needed: []

# Estimation accuracy
estimation_accuracy:
  total_plans: 0
  accurate_estimates: 0  # within 20% of actual
  underestimated: 0
  overestimated: 0
  accuracy_rate: 0.0
  avg_estimation_error: 0.0  # percentage

# Task completion tracking
task_outcomes:
  completed_successfully: 0
  partially_completed: 0
  blocked: 0
  abandoned: 0
  success_rate: 0.0

# Current work context
current_context:
  last_recommendation_planned: null
  next_in_queue: null
  tasks_awaiting_execution: []
  queue_depth: 0

# Work queue
work_queue:
  priority_recommendations: []  # high-priority recommendations to plan
  backlog: []                   # pending recommendations
  in_progress: null             # currently planning
  tasks_created_today: 0
  total_hours_planned_today: 0
```

---

## How to Use This Memory

**At the start of each run:**
1. Read this file to understand your planning history
2. Check `templates` for pattern-type guidance
3. Review `estimation_accuracy` to calibrate estimates
4. Check `work_queue` for what to plan next

**Planning workflow:**
1. Select recommendation from `work_queue.priority_recommendations`
2. Use appropriate template from `templates`
3. Calibrate estimates based on `estimation_accuracy`
4. Create task package in BB5 format
5. Update this timeline with plan details

## Work Assignment Logic

**How you know what to plan:**

1. **Check `work_queue.priority_recommendations`** - High-priority items
2. **If empty, check communications/events.yaml** - For analysis.complete events with decision: recommend
3. **Check data/analysis/** - Find recommendations not yet planned
4. **Select one recommendation** - Never batch multiple
5. **Update `work_queue.in_progress`** - Mark what you're planning
6. **Create plan** - Decompose into subtasks
7. **Create BB5 task** - Full task package
8. **Update timeline** - Save plan and track outcomes

## Template Evolution

Your templates improve over time:
- Validator feedback refines subtask lists
- Actual outcomes calibrate hour estimates
- Success rates guide template selection
- Category expertise builds with practice

---

*This file is automatically injected into your context via the SessionStart hook.*
