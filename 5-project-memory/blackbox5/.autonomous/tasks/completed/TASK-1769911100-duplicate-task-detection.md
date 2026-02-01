# TASK-1769911100: Implement Duplicate Task Detection System

**Type:** implement
**Priority:** high
**Status:** pending
**Created:** 2026-02-01T14:55:00Z
**Improvement:** IMP-1769903003

## Objective

Create a duplicate task detection system that prevents redundant work by checking for similar completed or in-progress tasks before creating new ones.

## Context

**Critical Issue Found:** TASK-1769914000 (Improvement Metrics Dashboard) was executed TWICE:
- Run 0032: Created the dashboard
- Run 0034: Re-executed same task (just verified and marked complete)

**Impact:**
- Wasted executor time (~30 minutes duplicated)
- Pollution of run history
- Queue inefficiency
- Could cause conflicts or data corruption

**Root Cause:** No duplicate detection in task creation workflow. Executor claimed task that was already completed.

**Supporting Evidence:**
- 7+ learnings mention duplicate task issues
- L-1769861933-002: "Check Completed Tasks First"
- L-20260131-060933-L002: "Duplicate Prevention"
- L-1769807450-002: "Pre-Execution Research Value"

## Success Criteria

- [ ] Duplicate detection library created in `2-engine/.autonomous/lib/duplicate_detector.py`
- [ ] Keyword similarity matching algorithm (80% threshold)
- [ ] Searches both active/ and completed/ task directories
- [ ] Integrated into Planner task creation workflow
- [ ] Integrated into Executor task claiming workflow
- [ ] Warning logged when potential duplicate detected
- [ ] Block task claim if duplicate confirmed
- [ ] Tested with known duplicate scenarios (including TASK-1769914000 case)
- [ ] Documentation created in `operations/.docs/duplicate-detection-guide.md`

## Approach

### Phase 1: Create Detection Library (20 min)
1. Create `2-engine/.autonomous/lib/duplicate_detector.py`
2. Implement similarity algorithms:
   - Keyword extraction (n-grams, TF-IDF)
   - Fuzzy string matching (Levenshtein distance)
   - Semantic similarity (optional, if time permits)
3. Add functions:
   - `check_duplicate(task_title, task_description)` → returns similarity score
   - `search_similar_tasks(task_data)` → returns list of similar tasks
   - `is_duplicate(task_data, threshold=0.8)` → returns boolean

### Phase 2: Integrate into Planner (10 min)
1. Modify Planner prompt to call duplicate checker before task creation
2. Add check to "Pre-Planning Research" section
3. Log duplicate detection attempts
4. If duplicate found: skip creation, log finding

### Phase 3: Integrate into Executor (10 min)
1. Add duplicate check in Executor task claiming workflow
2. Before claiming task: check if already in completed/
3. If duplicate found: skip claim, log warning, move to next task
4. Update events.yaml with duplicate detection

### Phase 4: Test and Validate (10 min)
1. Test with TASK-1769914000 scenario (should detect duplicate)
2. Test with non-duplicate tasks (should not false positive)
3. Verify detection accuracy with known cases
4. Monitor for false positives/negatives

## Files to Modify

- `2-engine/.autonomous/lib/duplicate_detector.py` (create)
  - Core duplicate detection logic
  - Similarity algorithms
  - Search functions

- `2-engine/.autonomous/prompts/system/planner/variations/v2-legacy-based.md`
  - Add duplicate check to task creation workflow
  - Section: "Pre-Planning Research"

- `2-engine/.autonomous/prompts/system/executor/variations/v2-legacy-based.md`
  - Add duplicate check to task claiming workflow
  - Section: "Claim Task"

- `operations/.docs/duplicate-detection-guide.md` (create)
  - How duplicate detection works
  - Thresholds and tuning
  - Troubleshooting

## Notes

**Detection Strategy:**
1. Extract keywords from task title and description
2. Search active/ and completed/ for similar keywords
3. Calculate similarity score (0-1)
4. If score > 0.8: flag as duplicate
5. Require manual review for 0.6-0.8 range

**Example Implementation:**
```python
def extract_keywords(text):
    """Extract important keywords from task text"""
    stopwords = ['create', 'implement', 'fix', 'analyze', 'the', 'a', 'an']
    words = text.lower().split()
    return [w for w in words if w not in stopwords and len(w) > 3]

def calculate_similarity(task1, task2):
    """Calculate similarity between two tasks"""
    keywords1 = extract_keywords(task1['title'] + ' ' + task1.get('description', ''))
    keywords2 = extract_keywords(task2['title'] + ' ' + task2.get('description', ''))

    intersection = set(keywords1) & set(keywords2)
    union = set(keywords1) | set(keywords2)

    return len(intersection) / len(union) if union else 0
```

**Dependencies:**
- Related to improvement IMP-1769903003
- Blocks IMP-1769903002 (pre-execution research)
- Connected to IMP-1769903001 (roadmap sync)

**Estimated Time:** 50 minutes
**Context Level:** 2 (moderate complexity)
**Risk:** Low (new feature, doesn't break existing functionality)

**Warnings:**
- Set threshold carefully to avoid false positives
- Monitor initial detections to tune algorithm
- Log all detection attempts for analysis
