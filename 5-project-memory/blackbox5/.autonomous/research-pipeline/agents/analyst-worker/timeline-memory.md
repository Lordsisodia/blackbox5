# Analyst Worker Timeline Memory

**Purpose:** Long-term memory of all analyses performed and scoring model evolution
**Updated:** Automatically at the end of each run
**Format:** YAML frontmatter with markdown body
**Injected via:** SessionStart hook

---

```yaml
timeline_memory:
  version: "1.0.0"
  agent: analyst-worker
  created: "2026-02-04T00:00:00Z"
  last_updated: "2026-02-04T00:00:00Z"
  total_runs: 0

# History of all analyses performed
analysis_history:
  # Example entry:
  # - run_id: "run-20260204-001"
  #   timestamp: "2026-02-04T10:10:00Z"
  #   pattern_id: "P-001"
  #   pattern_category: "authentication"
  #   value_score: 8.5
  #   complexity_score: 4.2
  #   decision: "recommend"
  #   confidence: 0.85
  #   tokens_used: 4200
  #   status: "success"

# Scoring model calibration
scoring_model:
  value_factors:
    relevance_to_bb5:
      weight: 1.0
      calibration_history: []  # how scores matched reality
    innovation_factor:
      weight: 1.0
      calibration_history: []
    community_adoption:
      weight: 1.0
      calibration_history: []
    maintainer_quality:
      weight: 1.0
      calibration_history: []
    documentation_quality:
      weight: 1.0
      calibration_history: []

  complexity_factors:
    lines_of_code:
      weight: 1.0
      calibration_history: []
    dependency_count:
      weight: 1.0
      calibration_history: []
    breaking_changes_risk:
      weight: 1.0
      calibration_history: []
    testing_effort:
      weight: 1.0
      calibration_history: []
    learning_curve:
      weight: 1.0
      calibration_history: []

# Decision accuracy tracking
decision_accuracy:
  total_recommendations: 0
  successful_implementations: 0
  deferred_revisited: 0
  rejected_correctly: 0
  accuracy_rate: 0.0

# Pattern category expertise
category_expertise:
  authentication:
    analyses_count: 0
    avg_confidence: 0.0
    common_patterns: []
  middleware:
    analyses_count: 0
    avg_confidence: 0.0
    common_patterns: []
  caching:
    analyses_count: 0
    avg_confidence: 0.0
    common_patterns: []
  database:
    analyses_count: 0
    avg_confidence: 0.0
    common_patterns: []

# Current work context
current_context:
  last_pattern_analyzed: null
  next_in_queue: null
  patterns_awaiting_planning: []
  queue_depth: 0

# Work queue
work_queue:
  priority_patterns: []    # high-priority patterns to analyze
  backlog: []              # pending patterns
  in_progress: null        # currently analyzing
  completed_today: 0
  recommendations_made_today: 0
```

---

## How to Use This Memory

**At the start of each run:**
1. Read this file to understand your scoring history
2. Check `scoring_model` for calibration data
3. Review `category_expertise` for relevant patterns
4. Check `work_queue` for what to analyze next

**Analysis workflow:**
1. Select pattern from `work_queue.priority_patterns`
2. Apply calibrated scoring model
3. Document rationale in THOUGHTS.md
4. Save analysis to data/analysis/
5. Update this timeline

## Work Assignment Logic

**How you know what to analyze:**

1. **Check `work_queue.priority_patterns`** - High-priority items
2. **If empty, check communications/events.yaml** - For pattern.extracted events
3. **Check data/patterns/** - Find patterns without analysis
4. **Select one pattern** - Never batch multiple
5. **Update `work_queue.in_progress`** - Mark what you're analyzing
6. **Do the analysis** - Score value and complexity
7. **Update timeline** - Save results and refine model

## Scoring Model Evolution

Your scoring model improves over time:
- Validator feedback adjusts weights
- Implementation outcomes calibrate accuracy
- Category expertise builds with practice
- Decision history refines thresholds

---

*This file is automatically injected into your context via the SessionStart hook.*
