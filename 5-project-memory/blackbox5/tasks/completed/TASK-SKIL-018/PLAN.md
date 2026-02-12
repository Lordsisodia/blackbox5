# PLAN.md: Add Skill Trigger Accuracy Tracking

**Task ID:** TASK-SKIL-018
**Status:** Planning
**Priority:** MEDIUM
**Created:** 2026-02-05
**Estimated Effort:** 30 minutes
**Source:** Scout opportunity skill-004 (Score: 11.0)

---

## 1. First Principles Analysis

### Why Track Trigger Accuracy?

1. **Measure Effectiveness**: Know if skill selection is correct
2. **Optimize Triggers**: Improve auto-trigger rules
3. **Data-Driven Decisions**: Replace guesswork with metrics
4. **Continuous Improvement**: Identify which skills work best
5. **ROI Validation**: Prove value of skill system

### What Happens Without Accuracy Data?

| Problem | Impact | Severity |
|---------|--------|----------|
| Blind selection | Don't know if skill was right choice | High |
| Wasted invocations | Wrong skills used repeatedly | Medium |
| Poor optimization | Can't improve trigger rules | Medium |
| Unknown ROI | Can't prove skill system value | Low |
| User frustration | Skills invoked inappropriately | Medium |

### How Should Accuracy Be Tracked?

**Post-Task Validation:**
- After task completion, validate skill choice
- Track: Was skill used? Was it helpful? Would use again?
- Store in skill-metrics.yaml
- Calculate trigger_accuracy metric

---

## 2. Current State Assessment

### Current Skill Metrics

**File:** `operations/skill-metrics.yaml`

**Current State:**
- 22 skills with `usage_count: 0`
- All metrics `null`
- Only 1 test entry
- No trigger accuracy data

**Metrics Schema:**
```yaml
metrics_schema:
  components:
    - name: trigger_accuracy
      weight: 0.2
      description: How often skill was right choice
      formula: correct_selections / total_selections * 100
```

### Skill Selection Process

**Current Flow:**
1. Task received
2. Check skill-selection.yaml for matching skills
3. Calculate confidence (>=70% to invoke)
4. Invoke skill or proceed normally
5. Task completes
6. (Missing: Validate if skill was correct)

**Gap:** No feedback loop to validate skill selection

---

## 3. Proposed Solution

### Post-Task Validation Hook

**Add to task completion workflow:**

```python
# lib/skill_validation.py

def validate_skill_selection(task_id: str, skill_used: str = None):
    """
    Validate whether skill selection was correct.
    Called after task completion.
    """
    task = load_task(task_id)

    # Determine what should have been used
    applicable_skills = find_applicable_skills(task)

    # Record validation
    validation = {
        'task_id': task_id,
        'skill_used': skill_used,
        'skills_recommended': applicable_skills,
        'was_correct': skill_used in applicable_skills if skill_used else len(applicable_skills) == 0,
        'timestamp': datetime.now().isoformat()
    }

    # Store validation
    append_to_skill_metrics(validation)

    return validation
```

### Validation Questions

**After task completion, ask:**
1. Was a skill invoked for this task? (Yes/No)
2. If yes: Was it the right skill? (Yes/No/Partially)
3. Would you use this skill again for similar tasks? (Yes/No)
4. What skill (if any) should have been used?

### Metric Calculation

**Trigger Accuracy Formula:**
```python
trigger_accuracy = (
    correct_selections / total_selections
) * 100

# Where:
# - correct_selections: skill was invoked and was appropriate
# - total_selections: all tasks where skill was considered
```

---

## 4. Implementation Plan

### Phase 1: Design Validation (10 min)

1. **Define validation criteria**
   - What makes a skill selection "correct"?
   - How to handle partial matches?
   - What data to collect?

2. **Design data structure**
   ```yaml
   # In skill-metrics.yaml
   task_outcomes:
     - task_id: "TASK-xxx"
       timestamp: "2026-02-01T12:00:00Z"
       skill_used: "skill-name"
       was_correct: true
       would_use_again: true
   ```

3. **Determine integration point**
   - Hook into task completion
   - CLI command for validation
   - Automated vs manual validation

### Phase 2: Implement Validation Hook (15 min)

1. **Create validation module**
   - `lib/skill_validation.py`
   - `validate_skill_selection()` function
   - Metric calculation

2. **Add to task completion**
   - Hook into bb5-task completion
   - Or add to task completion script
   - Store validation results

3. **Update skill-metrics.yaml**
   - Add task_outcomes section
   - Update trigger_accuracy calculation

### Phase 3: Test and Document (5 min)

1. **Test validation**
   - Complete a task with skill
   - Verify validation recorded
   - Check metrics updated

2. **Document process**
   - Add to skill-metrics-guide.md
   - Document validation criteria
   - Add examples

---

## 5. Success Criteria

- [ ] Validation criteria defined
- [ ] Validation module implemented
- [ ] Hook integrated with task completion
- [ ] skill-metrics.yaml updated with outcomes
- [ ] trigger_accuracy calculated automatically
- [ ] Test validation completed
- [ ] Documentation updated

---

## 6. Estimated Timeline

| Phase | Duration | Cumulative |
|-------|----------|------------|
| Phase 1: Design | 10 min | 10 min |
| Phase 2: Implement | 15 min | 25 min |
| Phase 3: Test & Doc | 5 min | 30 min |
| **Total** | **30 min** | **~30 min** |

---

## 7. Rollback Strategy

If validation causes issues:

1. **Immediate:** Disable validation hook
   ```bash
   export BB5_SKILL_VALIDATION=false
   ```

2. **Revert:** Remove validation from task completion
3. **Fix:** Debug and re-implement

---

## 8. Files to Modify/Create

### New Files

| File | Purpose | Lines |
|------|---------|-------|
| `lib/skill_validation.py` | Validation logic | ~100 |

### Modified Files

| File | Changes | Lines |
|------|---------|-------|
| `operations/skill-metrics.yaml` | Add task_outcomes section | +30 |
| `bin/bb5-task` | Add validation hook | +10 |
| `.docs/skill-metrics-guide.md` | Document validation | +20 |

---

## 9. Validation Criteria Definition

**Correct Selection:**
- Skill was invoked AND task benefited from skill
- No skill invoked AND no skill was needed

**Incorrect Selection:**
- Skill invoked but not helpful
- Wrong skill invoked
- Skill needed but not invoked

**Partial:**
- Skill helped but wasn't optimal
- Multiple skills could have worked

---

*Plan created: 2026-02-06*
*Ready for implementation*
