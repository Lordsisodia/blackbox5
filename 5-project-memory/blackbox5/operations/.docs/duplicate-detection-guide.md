# Duplicate Detection Guide

**Version:** 1.0.0
**Created:** 2026-02-01
**Author:** RALF-Executor (TASK-1769911100)

---

## Overview

The Duplicate Detection System prevents redundant work by identifying similar tasks before execution. It uses keyword similarity matching with an 80% threshold to flag potential duplicates.

**Critical Issue Addressed:** TASK-1769914000 (Improvement Metrics Dashboard) was executed twice, wasting ~30 minutes of executor time and polluting run history.

---

## How It Works

### Algorithm: Jaccard Similarity

The system uses Jaccard similarity to compare tasks:

```
Jaccard = |keywords_intersection| / |keywords_union|
```

**Process:**
1. Extract keywords from task title and description
2. Filter out stopwords (common words like "the", "create", "implement")
3. Calculate similarity score (0-1, where 1 = identical)
4. Flag as duplicate if score ≥ 0.8 (80%)

**Example:**
```
Task 1: "Create Improvement Metrics Dashboard"
Task 2: "Implement Dashboard for Improvement Metrics"

Keywords 1: {improvement, metrics, dashboard}
Keywords 2: {dashboard, improvement, metrics}

Jaccard = 3 / 3 = 1.0 (100% match) → DUPLICATE
```

---

## Usage

### 1. Planner: Before Creating Tasks

```bash
# Step 1: Create the task file
TASK_ID="TASK-$(date +%s)"
TASK_FILE="$RALF_PROJECT_DIR/.autonomous/tasks/active/${TASK_ID}-my-task.md"
# ... write task content ...

# Step 2: Check for duplicates
python3 $RALF_ENGINE_DIR/lib/duplicate_detector.py "$TASK_FILE"

# Step 3: If exit code 1, review output:
# - Lists similar tasks found
# - Shows similarity scores
# - Indicates if any are > 80% (duplicate)

# Step 4: Decide:
# - Skip if duplicate (don't create task)
# - Continue if not duplicate
# - Merge if partially duplicate
```

### 2. Executor: Before Claiming Tasks

```bash
# Step 1: List active tasks
ls $RALF_PROJECT_DIR/.autonomous/tasks/active/

# Step 2: Before claiming, check for duplicates
python3 $RALF_ENGINE_DIR/lib/duplicate_detector.py <task-file.md>

# Step 3: If duplicate detected:
# - Skip claiming the task
# - Log detection to events.yaml
# - Report to Planner via chat-log.yaml
# - Move to next task

# Step 4: If not duplicate:
# - Claim the task (write "started" event)
# - Proceed with execution
```

---

## Thresholds and Tuning

### Default Threshold: 80%

The 80% threshold balances:
- **False positives:** Too low (e.g., 60%) → many non-duplicates flagged
- **False negatives:** Too high (e.g., 95%) → duplicates missed

### When to Adjust Threshold

| Situation | Recommended Threshold | Rationale |
|-----------|----------------------|-----------|
| **General use** | 80% | Balanced detection |
| **Strict mode** | 70% | Catch more duplicates, review more |
| **Permissive mode** | 90% | Only flag near-identical tasks |
| **New project** | 75% | More cautious early on |
| **Mature project** | 85% | More confident patterns established |

### Custom Threshold

```python
from pathlib import Path
import sys

# Add library path
sys.path.insert(0, '/path/to/2-engine/.autonomous/lib')

from duplicate_detector import DuplicateDetector

# Create detector with custom threshold
detector = DuplicateDetector(similarity_threshold=0.75)  # 75%

# Check for duplicates
is_dup, similar = detector.is_duplicate(
    title="Task Title",
    description="Task description goes here"
)

print(f"Is duplicate: {is_dup}")
for task in similar[:5]:
    print(f"  - {task['title']} ({task['similarity']:.2%})")
```

---

## Troubleshooting

### Problem: "File does not exist" error

**Cause:** Duplicate detector can't find task directories.

**Solution:**
```bash
# Check if tasks directory exists
ls $RALF_PROJECT_DIR/.autonomous/tasks/

# If missing, create it
mkdir -p $RALF_PROJECT_DIR/.autonomous/tasks/{active,completed}
```

---

### Problem: Too many false positives

**Symptom:** Many tasks flagged as duplicates but aren't truly duplicates.

**Solutions:**
1. **Lower threshold:** Change from 80% to 85%
   ```python
   detector = DuplicateDetector(similarity_threshold=0.85)
   ```

2. **Improve task descriptions:** Add unique keywords to task descriptions

3. **Review stopwords:** Add common project-specific terms to STOPWORDS

---

### Problem: Missing duplicates (false negatives)

**Symptom:** Duplicate tasks not being detected.

**Solutions:**
1. **Raise threshold:** Change from 80% to 75%
   ```python
   detector = DuplicateDetector(similarity_threshold=0.75)
   ```

2. **Improve task titles:** Make titles more descriptive

3. **Review algorithm:** Current algorithm is keyword-based; semantic matching not supported

---

### Problem: Similarity score seems wrong

**Symptom:** Score is unexpectedly high or low.

**Debug:**
```python
from duplicate_detector import DuplicateDetector

detector = DuplicateDetector()

# Extract keywords to see what's being compared
task1_keywords = detector.extract_keywords("Task 1 text here")
task2_keywords = detector.extract_keywords("Task 2 text here")

print(f"Task 1 keywords: {task1_keywords}")
print(f"Task 2 keywords: {task2_keywords}")

# Calculate similarity manually
similarity = detector.calculate_jaccard_similarity(task1_keywords, task2_keywords)
print(f"Similarity: {similarity:.2%}")
```

---

## Integration Points

### Planner Prompt

Location: `2-engine/.autonomous/prompts/system/planner/variations/v2-legacy-based.md`

Section: **Step 3: Create Tasks** → **Pre-Planning Research (CRITICAL)**

Added automatic duplicate detection before task creation.

### Executor Prompt

Location: `2-engine/.autonomous/prompts/system/executor/variations/v2-legacy-based.md`

Section: **Step 2: Pre-Execution Verification**

Added automatic duplicate detection before task claiming.

---

## Performance

### Scalability

- **Search time:** O(n × m) where n = number of tasks, m = keywords per task
- **Typical performance:** < 1 second for 100+ tasks
- **Optimization:** Only scans active/ and completed/ directories

### Limitations

1. **Keyword-based:** Does not understand semantics (e.g., "build" vs "construct")
2. **English only:** Stopwords and tokenization optimized for English
3. **No machine learning:** Uses exact string matching, not embeddings

### Future Improvements

1. **Semantic similarity:** Integrate sentence transformers
2. **Task embedding:** Pre-compute embeddings for faster search
3. **Fuzzy matching:** Add Levenshtein distance for typos
4. **Multi-language support:** Language-aware stopwords

---

## Testing

### Test with Known Duplicate

```bash
# Test TASK-1769914000 (known duplicate scenario)
python3 $RALF_ENGINE_DIR/lib/duplicate_detector.py \
  $RALF_PROJECT_DIR/.autonomous/tasks/completed/TASK-1769914000-improvement-metrics-dashboard.md

# Expected: No duplicates (since original not in database)
# To test true duplicate detection, copy task to active/ and re-run
```

### Test with Non-Duplicate

```bash
# Test unique task
python3 $RALF_ENGINE_DIR/lib/duplicate_detector.py \
  $RALF_PROJECT_DIR/.autonomous/tasks/active/TASK-1769911100-duplicate-task-detection.md

# Expected: "✅ No duplicates found."
```

---

## Monitoring

### Metrics to Track

1. **Duplicate detection rate:** % of tasks flagged as duplicates
2. **True positive rate:** % of flagged tasks that are actual duplicates
3. **False positive rate:** % of flagged tasks that are not duplicates
4. **Time saved:** Executor hours saved by preventing duplicates

### Logging

All duplicate detections should be logged to events.yaml:

```yaml
events:
  - timestamp: "2026-02-01T02:15:00Z"
    task_id: "TASK-1769911100"
    type: duplicate_detected
    data:
      similar_tasks:
        - title: "Create Improvement Metrics Dashboard"
          similarity: 0.95
          path: "/path/to/completed/task.md"
    action: skipped_claim
```

---

## Related Documentation

- **Task Acceptance Criteria:** `operations/.docs/task-acceptance-criteria-guide.md`
- **Validation Checklist:** `operations/validation-checklist.yaml`
- **Executor Monitoring:** `operations/.docs/executor-monitoring-guide.md`

---

## Changelog

### v1.0.0 (2026-02-01)
- Initial implementation
- Jaccard similarity algorithm
- 80% default threshold
- Integration with Planner and Executor
- CLI interface for testing
