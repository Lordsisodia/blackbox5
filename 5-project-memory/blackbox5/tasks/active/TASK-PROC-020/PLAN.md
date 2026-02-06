# PLAN.md: Duplicate Task Detection System

**Task:** TASK-PROC-020 - Duplicate Task Directories for Same Work  
**Status:** In Progress  
**Priority:** MEDIUM  
**Created:** 2026-02-06  
**Importance Score:** 75/100

---

## 1. First Principles Analysis

### Why Do Duplicate Tasks Get Created?

| Root Cause | Frequency | Example |
|------------|-----------|---------|
| Different naming conventions | High | TASK-ARCH-016 vs TASK-ARCH-016-agent-execution-flow |
| Multiple agents creating tasks | High | Scout vs user created |
| Lack of search before create | Medium | No automated check |
| Different ID schemes | Medium | Timestamp vs semantic |

### What Problems Do Duplicate Tasks Cause?

1. **Wasted Effort**: Multiple agents working on same problem
2. **Context Fragmentation**: Knowledge scattered
3. **Confusion**: Unclear which task is canonical
4. **Maintenance Burden**: More tasks to track

### How Can We Prevent Duplicates?

**Detection Strategies:**

| Strategy | Method | Effectiveness |
|----------|--------|---------------|
| Keyword matching | Compare titles | 70% |
| Semantic similarity | TF-IDF/embedding | 85% |
| Category matching | Same category | 60% |
| File path similarity | Similar targets | 75% |

---

## 2. Current State Assessment

### Task Creation Process

Current flow in `bb5-create`:
1. Generate TASK-ID
2. Create directory
3. Populate from template
4. **No duplicate detection**

### Existing Duplicate Examples

| Primary Task | Duplicate Task | Similarity |
|--------------|----------------|------------|
| TASK-ARCH-016 | TASK-ARCH-016-agent-execution-flow | 95% |
| TASK-DEV-011 | TASK-DOCS-010-youtube-pipeline-plan | 80% |
| AGENT-SYSTEM-AUDIT | TASK-AUTO-010-agent-system-audit | 85% |

---

## 3. Proposed Solution

### Duplicate Detection Algorithm

```python
def detect_duplicates(new_task_name, threshold=0.7):
    existing_tasks = load_all_active_tasks()
    candidates = []
    
    for task in existing_tasks:
        scores = {
            'title_jaccard': jaccard_similarity(new_task_name, task.title),
            'keyword_overlap': keyword_overlap_score(new_task_name, task.title),
            'category_match': 1.0 if same category else 0.0
        }
        
        similarity = weighted_composite(scores)
        if similarity >= threshold:
            candidates.append((task.id, similarity))
    
    return sorted(candidates, key=lambda x: x[1], reverse=True)
```

### User Confirmation Flow

```
bb5 task:create "Implement YouTube scraper"
→ Found 2 potential duplicates:
  1. TASK-DEV-011-youtube-automation (87%)
  2. ACTION-PLAN-youtube-pipeline (82%)
→ Options: [1] View [2] View [3] Create anyway [4] Cancel [5] Merge
```

---

## 4. Implementation Plan

### Phase 1: Create Detection Script (2-3 hours)

1. Create `bin/bb5-detect-duplicates`
2. Implement similarity calculation
3. Load and parse task files
4. Configurable threshold

### Phase 2: Integrate with Task Creation (1-2 hours)

1. Modify `bb5-create`
2. Add duplicate check
3. Show interactive prompt
4. Add `--force` flag

### Phase 3: Add Similarity Scoring (2-3 hours)

1. Add TF-IDF vectorization
2. File path extraction
3. Composite scoring
4. Detailed reporting

### Phase 4: Create Merge Workflow (2-3 hours)

1. Create `bb5-task-merge`
2. Compare side-by-side
3. Interactive selection
4. Preserve history

### Phase 5: Test and Document (1-2 hours)

1. Test with known duplicates
2. Test edge cases
3. Update documentation

---

## 5. Success Criteria

| Criterion | Target | Verification |
|-----------|--------|--------------|
| Duplicate detection | 100% | Known duplicates detected |
| Similarity scoring | >85% | Manual review of 20 cases |
| User confirmation | Interactive | Test with bb5 task:create |
| False positive rate | <10% | Review flagged tasks |
| Documentation | Complete | README updated |

---

## 6. Estimated Timeline

| Phase | Estimated Time | Cumulative |
|-------|----------------|------------|
| Phase 1: Detection | 2-3 hours | 2-3 hours |
| Phase 2: Integration | 1-2 hours | 3-5 hours |
| Phase 3: Scoring | 2-3 hours | 5-8 hours |
| Phase 4: Merge | 2-3 hours | 7-11 hours |
| Phase 5: Test | 1-2 hours | 8-13 hours |

**Total:** 8-13 hours

---

*Plan created based on duplicate task analysis*
