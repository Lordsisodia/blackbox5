# Analyst Validator Timeline Memory

**Purpose:** Long-term memory of all analysis validations and model improvements
**Updated:** Automatically at the end of each run
**Format:** YAML frontmatter with markdown body
**Injected via:** SessionStart hook

---

```yaml
timeline_memory:
  version: "1.0.0"
  agent: analyst-validator
  created: "2026-02-04T00:00:00Z"
  last_updated: "2026-02-04T00:00:00Z"
  total_runs: 0

# History of all validation runs
validation_history:
  # Example entry:
  # - run_id: "run-20260204-001"
  #   timestamp: "2026-02-04T10:15:00Z"
  #   worker_run_id: "run-20260204-001"
  #   pattern_id: "P-001"
  #   predicted_value: 8.5
  #   predicted_complexity: 4.2
  #   scoring_accuracy: 0.90
  #   feedback_given: 1
  #   model_adjustments: ["increase auth complexity +0.5"]

# Model accuracy tracking
model_accuracy:
  value_predictions:
    total: 0
    accurate: 0  # within 1 point of actual
    overestimated: 0
    underestimated: 0
    accuracy_rate: 0.0

  complexity_predictions:
    total: 0
    accurate: 0  # within 1 point of actual
    overestimated: 0
    underestimated: 0
    accuracy_rate: 0.0

  decision_accuracy:
    recommend_success_rate: 0.0
    defer_appropriateness: 0.0
    reject_accuracy: 0.0

# Bias detection
bias_tracking:
  detected_biases: []
  # Example:
  # - type: "complexity_underestimation"
  #   category: "authentication"
  #   severity: "medium"
  #   evidence: ["P-001", "P-002"]
  #   adjustment: "+1 to auth complexity"

# Worker behavior patterns
worker_patterns:
  scoring_tendencies: []     # consistent scoring patterns
  calibration_issues: []     # areas needing calibration
  improvement_areas: []      # where worker is improving
  strengths: []              # what they do well

# Current monitoring context
current_context:
  monitoring_worker_run: null
  pending_validations: []
  patterns_awaiting_outcome: []  # to track actual vs predicted

# Strategy effectiveness
validation_strategy:
  effective_approaches: []
  ineffective_approaches: []
  calibration_methods: []    # what works for calibrating
  feedback_strategies: []    # what feedback drives improvement
```

---

## How to Use This Memory

**At the start of each run:**
1. Read this file to understand validation history
2. Check `model_accuracy` for calibration needs
3. Review `bias_tracking` for known issues
4. Check `current_context` for what to validate

**Validation workflow:**
1. Find worker's analysis to validate
2. Compare prediction to `model_accuracy` history
3. Check for `bias_tracking` patterns
4. Provide calibration feedback
5. Update this timeline with results

## Work Assignment Logic

**How you know what to validate:**

1. **Check `current_context.monitoring_worker_run`** - Specific run to check
2. **If null, find latest analyst-worker run** - Look in analyst-worker/runs/
3. **Read their analysis** - Check data/analysis/ for new files
4. **Compare to model_accuracy** - Is prediction realistic?
5. **Check bias_tracking** - Any known biases for this category?
6. **Validate and provide feedback** - Write to chat-log.yaml
7. **Update timeline** - Record validation and accuracy

## Model Calibration

You help calibrate the scoring model by:
- Tracking prediction vs actual outcomes
- Identifying systematic biases
- Suggesting weight adjustments
- Validating category-specific patterns

---

*This file is automatically injected into your context via the SessionStart hook.*
